"""Explainable Tomato Leaf Disease Detection — 3-Model Softmax Voting Ensemble
=============================================================================
Course / Project: Explainable Tomato Leaf Disease Detection Using AI/ML
Team Name: Team Green tech (IML-V-2026-T030)
Members:
  - Sarthak Negi (24151534) — Data pipeline, Augmentation, Ensemble & Softmax Voting
  - Prerna (24151435) — MobileNetV2 Transfer Learning, Evaluation & Pathology Analysis
  - Disha (24152259) — Dataset Cleaning, DenseNet121 & ResNet50 Transfer Learning

Architecture:
  - Backbones: MobileNetV2, DenseNet121, ResNet50 (ImageNet Pretrained)
  - Training: Batch size 8, 2-stage transfer learning (Feature extraction -> Fine-tuning)
  - Ensemble Mechanism: Softmax Probability Averaging (Softmax Voting)
  - Outputs:
      - models/mobilenet_v2.pt
      - models/densenet121.pt
      - models/resnet50.pt
      - augmentation_preview.png
      - confusion_matrix.png
      - results/ensemble_evaluation_report.json
"""

import argparse
import json
import os
import random
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import classification_report, confusion_matrix
from torch.utils.data import DataLoader, Dataset, Subset, random_split
import torchvision.transforms as T
from torchvision.datasets import ImageFolder
from torchvision.models import (
    DenseNet121_Weights,
    MobileNet_V2_Weights,
    ResNet50_Weights,
    densenet121,
    mobilenet_v2,
    resnet50,
)

# Standard ImageNet normalization constants
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]
IMG_SIZE = 224
BATCH_SIZE = 8
SEED = 42

def set_seed(seed: int = SEED) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def get_device(device_str: str = "auto") -> torch.device:
    if device_str != "auto":
        return torch.device(device_str)
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


# =============================================================================
# 1. DATA AUGMENTATION & TRANSFORMS
# =============================================================================

def get_train_transform() -> T.Compose:
    """Data augmentation pipeline: random flips, rotation, zoom, contrast & brightness."""
    return T.Compose([
        T.Resize((IMG_SIZE, IMG_SIZE)),
        T.RandomHorizontalFlip(p=0.5),
        T.RandomRotation(degrees=15),
        T.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.1),
        T.RandomAffine(degrees=0, scale=(0.85, 1.15)),
        T.ToTensor(),
        T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])


def get_eval_transform() -> T.Compose:
    """Deterministic transform for validation and test sets."""
    return T.Compose([
        T.Resize((IMG_SIZE, IMG_SIZE)),
        T.ToTensor(),
        T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])


class TransformedSubset(Dataset):
    """Wraps a Subset with a specific transform."""
    def __init__(self, subset: Subset, transform: T.Compose):
        self.subset = subset
        self.transform = transform

    def __getitem__(self, idx: int):
        img, target = self.subset.dataset[self.subset.indices[idx]]
        if self.transform is not None:
            img = self.transform(img)
        return img, target

    def __len__(self) -> int:
        return len(self.subset)


def generate_augmentation_preview(
    raw_folder_path: Path,
    out_path: Path = Path("augmentation_preview.png"),
) -> Path:
    """Generate and save visual inspection grid of original vs augmented samples."""
    from PIL import Image

    # Find sample images across classes
    sample_files = []
    classes = sorted([d.name for d in raw_folder_path.iterdir() if d.is_dir() and not d.name.startswith(".")])
    for cls in classes[:3]:
        cls_dir = raw_folder_path / cls
        files = [f for f in cls_dir.iterdir() if f.suffix.lower() in (".jpg", ".jpeg", ".png")]
        if files:
            sample_files.append((cls.replace("Tomato___", "").replace("_", " "), files[0]))

    if not sample_files:
        print("No sample images found for augmentation preview.")
        return out_path

    # Define individual augmentations for clear side-by-side demonstration
    aug_variants = [
        ("Original (Resize 224×224)", T.Compose([T.Resize((IMG_SIZE, IMG_SIZE))])),
        ("Horizontal Flip (p=1.0)", T.Compose([T.Resize((IMG_SIZE, IMG_SIZE)), T.RandomHorizontalFlip(p=1.0)])),
        ("Rotation (15°)", T.Compose([T.Resize((IMG_SIZE, IMG_SIZE)), T.RandomRotation(degrees=(15, 15))])),
        ("Brightness & Contrast", T.Compose([T.Resize((IMG_SIZE, IMG_SIZE)), T.ColorJitter(brightness=0.3, contrast=0.3)])),
        ("Random Zoom & Affine", T.Compose([T.Resize((IMG_SIZE, IMG_SIZE)), T.RandomAffine(degrees=0, scale=(1.15, 1.15))])),
    ]

    fig, axes = plt.subplots(len(sample_files), len(aug_variants), figsize=(15, 3.2 * len(sample_files)))
    if len(sample_files) == 1:
        axes = np.expand_dims(axes, 0)

    for r_idx, (label, img_file) in enumerate(sample_files):
        img_raw = Image.open(img_file).convert("RGB")
        for c_idx, (aug_name, trans) in enumerate(aug_variants):
            aug_img = trans(img_raw)
            ax = axes[r_idx, c_idx]
            ax.imshow(aug_img)
            ax.axis("off")
            if r_idx == 0:
                ax.set_title(aug_name, fontsize=11, fontweight="bold", pad=8)
            if c_idx == 0:
                ax.text(
                    -0.08,
                    0.5,
                    label,
                    transform=ax.transAxes,
                    rotation=90,
                    va="center",
                    ha="right",
                    fontsize=10,
                    fontweight="bold",
                )

    fig.suptitle("Data Augmentation Pipeline Preview — Team Green tech", fontsize=14, fontweight="bold", y=0.98)
    fig.tight_layout(rect=[0.05, 0.02, 0.98, 0.95])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(out_path), dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"✓ Saved data augmentation preview to: {out_path}")
    return out_path


# =============================================================================
# 2. DATASET PIPELINE (TRAIN/VAL SPLIT 80/20, VAL AS TEST SET)
# =============================================================================

def load_data(
    data_dir: Path,
    batch_size: int = BATCH_SIZE,
    seed: int = SEED,
) -> Tuple[DataLoader, DataLoader, DataLoader, List[str]]:
    """Loads Kaggle tomatoleaf dataset.

    - Splits train folder 80/20 into training and validation sets.
    - Sets aside the original val folder as test set.
    """
    train_dir = data_dir / "train"
    val_dir = data_dir / "val"

    if not train_dir.exists():
        raise FileNotFoundError(f"Train directory not found at: {train_dir}")
    if not val_dir.exists():
        raise FileNotFoundError(f"Val/Test directory not found at: {val_dir}")

    # Discover classes
    full_train_raw = ImageFolder(str(train_dir))
    test_raw = ImageFolder(str(val_dir), transform=get_eval_transform())
    class_names = full_train_raw.classes

    # Split train 80/20 stratified/random
    n_total = len(full_train_raw)
    n_train = int(0.8 * n_total)
    n_val = n_total - n_train

    gen = torch.Generator().manual_seed(seed)
    train_sub, val_sub = random_split(full_train_raw, [n_train, n_val], generator=gen)

    train_dataset = TransformedSubset(train_sub, get_train_transform())
    val_dataset = TransformedSubset(val_sub, get_eval_transform())
    test_dataset = test_raw

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    print(f"Data Pipeline Initialized:")
    print(f"  • Classes ({len(class_names)}): {class_names}")
    print(f"  • Training Samples: {len(train_dataset)} (80% split)")
    print(f"  • Validation Samples: {len(val_dataset)} (20% split)")
    print(f"  • Test Samples: {len(test_dataset)} (held-out val set)")
    print(f"  • Batch size: {batch_size}")

    return train_loader, val_loader, test_loader, class_names


# =============================================================================
# 3. THREE BACKBONE MODELS (MobileNetV2, DenseNet121, ResNet50)
# =============================================================================

def build_mobilenet_v2(num_classes: int = 10, pretrained: bool = True) -> nn.Module:
    weights = MobileNet_V2_Weights.DEFAULT if pretrained else None
    model = mobilenet_v2(weights=weights)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(in_features, 128),
        nn.ReLU(),
        nn.Dropout(p=0.2),
        nn.Linear(128, num_classes),
    )
    setattr(model, "name", "MobileNetV2")
    return model


def build_densenet121(num_classes: int = 10, pretrained: bool = True) -> nn.Module:
    weights = DenseNet121_Weights.DEFAULT if pretrained else None
    model = densenet121(weights=weights)
    in_features = model.classifier.in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(in_features, 128),
        nn.ReLU(),
        nn.Dropout(p=0.2),
        nn.Linear(128, num_classes),
    )
    setattr(model, "name", "DenseNet121")
    return model


def build_resnet50(num_classes: int = 10, pretrained: bool = True) -> nn.Module:
    weights = ResNet50_Weights.DEFAULT if pretrained else None
    model = resnet50(weights=weights)
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(in_features, 128),
        nn.ReLU(),
        nn.Dropout(p=0.2),
        nn.Linear(128, num_classes),
    )
    setattr(model, "name", "ResNet50")
    return model


# =============================================================================
# 4. TWO-STAGE TRANSFER LEARNING TRAINING LOOP
# =============================================================================

def set_backbone_trainable(model: nn.Module, model_name: str, trainable: bool, unfreeze_last_n: int = 30) -> None:
    """Freeze or unfreeze backbone layers."""
    if not trainable:
        for param in model.parameters():
            param.requires_grad = False
        # Head is always trainable
        head = model.classifier if hasattr(model, "classifier") else model.fc
        for param in head.parameters():
            param.requires_grad = True
    else:
        # Fine-tuning: unfreeze last n layers
        all_params = list(model.parameters())
        for param in all_params:
            param.requires_grad = False
        # Unfreeze top layers + classifier head
        for param in all_params[-unfreeze_last_n:]:
            param.requires_grad = True


def train_single_model(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    device: torch.device,
    save_path: Path,
    epochs_phase1: int = 3,
    epochs_phase2: int = 2,
    patience: int = 3,
) -> nn.Module:
    """Two-stage training: Phase 1 (Frozen base) -> Phase 2 (Fine-tuning top 30 layers)."""
    model_name = getattr(model, "name", "Model")
    print(f"\n========================================================")
    print(f" Training Backbone: {model_name}")
    print(f"========================================================")
    model.to(device)
    criterion = nn.CrossEntropyLoss()

    best_val_acc = 0.0
    best_weights = None

    # PHASE 1: Train Head Only
    print(f"--- Phase 1: Training Classification Head ({epochs_phase1} epochs, lr=1e-3) ---")
    set_backbone_trainable(model, model_name, trainable=False)
    optimizer = torch.optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=1e-3, weight_decay=1e-4)

    for epoch in range(1, epochs_phase1 + 1):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for b_idx, (images, labels) in enumerate(train_loader):
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
            if (b_idx + 1) % 250 == 0:
                print(f"    [P1 Batch {b_idx + 1}/{len(train_loader)}] loss: {running_loss/total:.4f}, acc: {correct/total*100:.2f}%")

        train_acc = correct / total
        train_loss = running_loss / total

        # Validation
        model.eval()
        val_correct = 0
        val_total = 0
        val_loss_sum = 0.0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss_sum += loss.item() * images.size(0)
                preds = outputs.argmax(dim=1)
                val_correct += (preds == labels).sum().item()
                val_total += labels.size(0)

        val_acc = val_correct / val_total
        val_loss = val_loss_sum / val_total

        print(f"  [P1 Epoch {epoch}/{epochs_phase1}] Train Loss: {train_loss:.4f}, Train Acc: {train_acc*100:.2f}% | Val Loss: {val_loss:.4f}, Val Acc: {val_acc*100:.2f}%")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_weights = model.state_dict().copy()

    # PHASE 2: Fine-Tuning Top 30 Layers
    if epochs_phase2 > 0:
        print(f"\n--- Phase 2: Fine-Tuning Last 30 Layers ({epochs_phase2} epochs, lr=1e-5) ---")
        set_backbone_trainable(model, model_name, trainable=True, unfreeze_last_n=30)
        optimizer_ft = torch.optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=1e-5, weight_decay=1e-4)

        for epoch in range(1, epochs_phase2 + 1):
            model.train()
            running_loss = 0.0
            correct = 0
            total = 0

            for b_idx, (images, labels) in enumerate(train_loader):
                images, labels = images.to(device), labels.to(device)
                optimizer_ft.zero_grad()
                outputs = model(images)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer_ft.step()

                running_loss += loss.item() * images.size(0)
                preds = outputs.argmax(dim=1)
                correct += (preds == labels).sum().item()
                total += labels.size(0)
                if (b_idx + 1) % 250 == 0:
                    print(f"    [P2 Batch {b_idx + 1}/{len(train_loader)}] loss: {running_loss/total:.4f}, acc: {correct/total*100:.2f}%")

            train_acc = correct / total
            train_loss = running_loss / total

            model.eval()
            val_correct = 0
            val_total = 0
            val_loss_sum = 0.0
            with torch.no_grad():
                for images, labels in val_loader:
                    images, labels = images.to(device), labels.to(device)
                    outputs = model(images)
                    loss = criterion(outputs, labels)
                    val_loss_sum += loss.item() * images.size(0)
                    preds = outputs.argmax(dim=1)
                    val_correct += (preds == labels).sum().item()
                    val_total += labels.size(0)

            val_acc = val_correct / val_total
            val_loss = val_loss_sum / val_total

            print(f"  [P2 Epoch {epoch}/{epochs_phase2}] Train Loss: {train_loss:.4f}, Train Acc: {train_acc*100:.2f}% | Val Loss: {val_loss:.4f}, Val Acc: {val_acc*100:.2f}%")

            if val_acc > best_val_acc:
                best_val_acc = val_acc
                best_weights = model.state_dict().copy()

    if best_weights is not None:
        model.load_state_dict(best_weights)

    save_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_name": model_name,
            "state_dict": model.state_dict(),
            "best_val_acc": best_val_acc,
        },
        str(save_path),
    )
    print(f"✓ Saved {model_name} checkpoint (Best Val Acc: {best_val_acc*100:.2f}%) to: {save_path}")
    return model


# =============================================================================
# 5. ENSEMBLE EVALUATION VIA SOFTMAX VOTING
# =============================================================================

def evaluate_ensemble(
    models: List[nn.Module],
    test_loader: DataLoader,
    device: torch.device,
    class_names: List[str],
) -> Dict[str, Any]:
    """Evaluates individual models and Softmax Voting Ensemble on test_loader."""
    for m in models:
        m.to(device)
        m.eval()

    all_probs: List[List[np.ndarray]] = [[] for _ in range(len(models))]
    y_true: List[int] = []

    print("\nRunning test evaluation across models and ensemble...")
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            y_true.extend(labels.cpu().numpy().tolist())

            for m_idx, m in enumerate(models):
                logits = m(images)
                probs = torch.softmax(logits, dim=1).cpu().numpy()
                all_probs[m_idx].append(probs)

    y_true_np = np.array(y_true)

    # Individual model metrics
    individual_results = {}
    model_preds = []
    for m_idx, m in enumerate(models):
        m_name = getattr(m, "name", f"Model_{m_idx}")
        m_prob_all = np.concatenate(all_probs[m_idx], axis=0)
        m_pred = np.argmax(m_prob_all, axis=1)
        model_preds.append(m_pred)
        acc = float(np.mean(m_pred == y_true_np)) * 100.0
        individual_results[m_name] = {
            "accuracy_pct": round(acc, 2),
            "probs": m_prob_all,
            "preds": m_pred,
        }
        print(f"  • {m_name} Test Accuracy: {acc:.2f}%")

    # Softmax Voting Ensemble: Average probabilities
    stacked_probs = np.stack([res["probs"] for res in individual_results.values()], axis=0) # [3, N, 10]
    ensemble_probs = np.mean(stacked_probs, axis=0) # [N, 10]
    ensemble_preds = np.argmax(ensemble_probs, axis=1)
    ensemble_acc = float(np.mean(ensemble_preds == y_true_np)) * 100.0
    print(f"\n★ Softmax Voting Ensemble Test Accuracy: {ensemble_acc:.2f}%")

    # Confusion Matrix
    cm = confusion_matrix(y_true_np, ensemble_preds, labels=list(range(len(class_names))))
    report_dict = classification_report(
        y_true_np, ensemble_preds, target_names=class_names, output_dict=True, zero_division=0
    )

    # Analyze errors
    confused_pairs = []
    for i in range(len(class_names)):
        for j in range(len(class_names)):
            if i != j and cm[i, j] > 0:
                confused_pairs.append({
                    "true_class": class_names[i].replace("Tomato___", "").replace("_", " "),
                    "pred_class": class_names[j].replace("Tomato___", "").replace("_", " "),
                    "count": int(cm[i, j]),
                })
    confused_pairs.sort(key=lambda x: x["count"], reverse=True)

    return {
        "individual": {k: v["accuracy_pct"] for k, v in individual_results.items()},
        "ensemble_accuracy_pct": round(ensemble_acc, 2),
        "confusion_matrix": cm.tolist(),
        "classification_report": report_dict,
        "confused_pairs": confused_pairs,
    }


def plot_and_save_confusion_matrix(
    cm: np.ndarray,
    class_names: List[str],
    out_path: Path = Path("confusion_matrix.png"),
) -> Path:
    """Plot high-contrast, publication-grade confusion matrix heatmap."""
    clean_names = [c.replace("Tomato___", "").replace("_", " ") for c in class_names]

    fig, ax = plt.subplots(figsize=(11, 9))
    im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
    cbar = ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.set_ylabel("Diagnostic Prediction Count", rotation=-90, va="bottom", fontsize=10)

    ax.set(
        xticks=np.arange(cm.shape[1]),
        yticks=np.arange(cm.shape[0]),
        xticklabels=clean_names,
        yticklabels=clean_names,
        title="Tomato Leaf Disease Confusion Matrix (3-Model Softmax Voting Ensemble)",
        ylabel="True Pathology Ground Truth",
        xlabel="Model Ensemble Diagnostic Prediction",
    )

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor", fontsize=9)
    plt.setp(ax.get_yticklabels(), fontsize=9)

    # Annotate numbers
    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            val = cm[i, j]
            ax.text(
                j,
                i,
                format(val, "d"),
                ha="center",
                va="center",
                color="white" if val > thresh else "black",
                fontweight="bold" if val > 0 else "normal",
                fontsize=9,
            )

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(out_path), dpi=250, bbox_inches="tight")
    plt.close(fig)
    print(f"✓ Saved confusion matrix plot to: {out_path}")
    return out_path


# =============================================================================
# 6. MAIN EXECUTION ROUTINE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Train & Evaluate Softmax Voting Ensemble")
    parser.add_argument("--data-dir", default="data/raw", help="Path to raw dataset folder containing train/ and val/")
    parser.add_argument("--batch-size", type=int, default=8, help="Batch size (default: 8 as specified in report)")
    parser.add_argument("--device", default="auto", help="Execution device: auto, cpu, mps, cuda")
    parser.add_argument("--preview-only", action="store_true", help="Only generate augmentation preview and exit")
    parser.add_argument("--epochs-p1", type=int, default=3, help="Phase 1 epochs (frozen backbone)")
    parser.add_argument("--epochs-p2", type=int, default=2, help="Phase 2 epochs (fine tuning top 30 layers)")
    parser.add_argument("--quick-eval", action="store_true", help="Run benchmark evaluation across models and ensemble")
    args = parser.parse_args()

    set_seed(SEED)
    device = get_device(args.device)
    print(f"Active Compute Device: {device}")

    data_dir = Path(args.data_dir)

    # 1. Generate augmentation preview
    preview_path = Path("augmentation_preview.png")
    generate_augmentation_preview(data_dir / "train", preview_path)
    # Also save to results/
    Path("results").mkdir(exist_ok=True)
    import shutil
    shutil.copy(preview_path, Path("results") / "augmentation_preview.png")

    if args.preview_only:
        print("Preview generated. Exiting.")
        return

    # 2. Load dataset
    train_loader, val_loader, test_loader, class_names = load_data(
        data_dir=data_dir, batch_size=args.batch_size, seed=SEED
    )
    num_classes = len(class_names)

    # 3. Instantiate the 3 models
    m_mobilenet = build_mobilenet_v2(num_classes=num_classes, pretrained=True)
    m_densenet = build_densenet121(num_classes=num_classes, pretrained=True)
    m_resnet = build_resnet50(num_classes=num_classes, pretrained=True)

    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    mob_ckpt = models_dir / "mobilenet_v2.pt"
    dense_ckpt = models_dir / "densenet121.pt"
    res_ckpt = models_dir / "resnet50.pt"

    # Train or load weights
    if not args.quick_eval:
        m_mobilenet = train_single_model(
            m_mobilenet, train_loader, val_loader, device, mob_ckpt,
            epochs_phase1=args.epochs_p1, epochs_phase2=args.epochs_p2
        )
        m_densenet = train_single_model(
            m_densenet, train_loader, val_loader, device, dense_ckpt,
            epochs_phase1=args.epochs_p1, epochs_phase2=args.epochs_p2
        )
        m_resnet = train_single_model(
            m_resnet, train_loader, val_loader, device, res_ckpt,
            epochs_phase1=args.epochs_p1, epochs_phase2=args.epochs_p2
        )
    else:
        # Load weights if available, otherwise initialize with pretrained
        for m, ckpt in [(m_mobilenet, mob_ckpt), (m_densenet, dense_ckpt), (m_resnet, res_ckpt)]:
            if ckpt.exists():
                data = torch.load(str(ckpt), map_location=device)
                m.load_state_dict(data["state_dict"] if "state_dict" in data else data)
                print(f"Loaded existing weights for {m.name} from {ckpt}")
            else:
                print(f"Checkpoint for {m.name} not found, initializing fresh head.")

    # 4. Evaluate Ensemble with Softmax Voting
    eval_results = evaluate_ensemble(
        models=[m_mobilenet, m_densenet, m_resnet],
        test_loader=test_loader,
        device=device,
        class_names=class_names,
    )

    # 5. Plot and save confusion matrix
    cm_array = np.array(eval_results["confusion_matrix"])
    cm_path = Path("confusion_matrix.png")
    plot_and_save_confusion_matrix(cm_array, class_names, cm_path)
    shutil.copy(cm_path, Path("results") / "confusion_matrix.png")

    # 6. Save JSON report
    report_out = Path("results") / "ensemble_evaluation_report.json"
    with open(report_out, "w") as f:
        json.dump(eval_results, f, indent=2)
    print(f"✓ Saved ensemble evaluation report to: {report_out}")

    print("\n========================================================")
    print(" SUMMARY OF FINAL ENSEMBLE BENCHMARKS")
    print("========================================================")
    print(f"MobileNetV2 Test Accuracy: {eval_results['individual'].get('MobileNetV2', 'N/A')}%")
    print(f"DenseNet121 Test Accuracy: {eval_results['individual'].get('DenseNet121', 'N/A')}%")
    print(f"ResNet50 Test Accuracy:    {eval_results['individual'].get('ResNet50', 'N/A')}%")
    print(f"Ensemble Test Accuracy:    {eval_results['ensemble_accuracy_pct']}%")
    if eval_results["confused_pairs"]:
        top = eval_results["confused_pairs"][0]
        print(f"Top Confused Pair: {top['true_class']} -> {top['pred_class']} ({top['count']} errors)")
    print("========================================================\n")


if __name__ == "__main__":
    main()
