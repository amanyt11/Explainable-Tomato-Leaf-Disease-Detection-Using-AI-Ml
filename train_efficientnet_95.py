"""Train EfficientNet-B0 using 2-stage transfer learning to reach >95% accuracy."""

from pathlib import Path
import torch
import torch.nn as nn
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights

from train_ensemble import load_data, get_device, set_seed, SEED

def main():
    set_seed(SEED)
    device = get_device("mps")
    print(f"Device: {device}")

    train_loader, val_loader, test_loader, class_names = load_data(
        Path("data/raw"), batch_size=8, seed=SEED
    )

    # Pretrained ImageNet weights
    weights = EfficientNet_B0_Weights.DEFAULT
    model = efficientnet_b0(weights=weights)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, len(class_names))
    model.to(device)

    criterion = nn.CrossEntropyLoss()

    # Stage 1: Freeze backbone, train only classification head
    print("\n--- Stage 1: Warm up head (backbone frozen) ---")
    for name, p in model.named_parameters():
        if "classifier" not in name:
            p.requires_grad = False
        else:
            p.requires_grad = True

    opt_stage1 = torch.optim.AdamW(model.classifier.parameters(), lr=1e-3, weight_decay=1e-4)

    for epoch in range(1, 2):
        model.train()
        correct, total = 0, 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            opt_stage1.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            opt_stage1.step()
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
        print(f"Stage 1 Train Acc: {correct / total * 100:.2f}%")

    # Stage 2: Unfreeze backbone with small lr
    print("\n--- Stage 2: Fine-tune backbone (lr=1e-4) ---")
    for p in model.parameters():
        p.requires_grad = True

    opt_stage2 = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-4)

    best_val_acc = 0.0
    best_weights = model.state_dict().copy()

    for epoch in range(1, 2):
        model.train()
        correct, total = 0, 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            opt_stage2.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            opt_stage2.step()
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        train_acc = correct / total

        # Validation
        model.eval()
        val_correct, val_total = 0, 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                preds = outputs.argmax(dim=1)
                val_correct += (preds == labels).sum().item()
                val_total += labels.size(0)

        val_acc = val_correct / val_total
        print(f"Stage 2 Epoch {epoch}: Train Acc: {train_acc*100:.2f}%, Val Acc: {val_acc*100:.2f}%")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_weights = model.state_dict().copy()

    model.load_state_dict(best_weights)

    # Test set evaluation
    test_correct, test_total = 0, 0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            preds = outputs.argmax(dim=1)
            test_correct += (preds == labels).sum().item()
            test_total += labels.size(0)

    test_acc = test_correct / test_total
    print(f"\n★ EfficientNet-B0 Test Accuracy: {test_acc*100:.2f}%")

    ckpt_path = Path("models/best.pt")
    torch.save(
        {
            "model_state": model.state_dict(),
            "class_names": class_names,
            "image_size": 224,
            "architecture": "efficientnet_b0",
            "best_val_acc": best_val_acc,
            "test_acc": test_acc,
        },
        str(ckpt_path),
    )
    print(f"✓ Saved models/best.pt with test accuracy: {test_acc*100:.2f}%")

if __name__ == "__main__":
    main()

