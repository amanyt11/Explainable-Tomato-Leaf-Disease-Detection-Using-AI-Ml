"""Fine-tune the 3 ensemble backbones with lr=1e-4 to reach >95% ensemble accuracy."""

import json
import shutil
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
from train_ensemble import (
    load_data,
    build_mobilenet_v2,
    build_densenet121,
    build_resnet50,
    evaluate_ensemble,
    plot_and_save_confusion_matrix,
    get_device,
    set_seed,
    SEED,
)

def finetune_model(model, train_loader, val_loader, device, ckpt_path, epochs=2, lr=1e-4):
    model.to(device)
    # Load current checkpoint
    if ckpt_path.exists():
        data = torch.load(ckpt_path, map_location=device)
        model.load_state_dict(data["state_dict"] if "state_dict" in data else data)
        print(f"Loaded existing checkpoint from {ckpt_path}")

    # Unfreeze top layers
    for param in model.parameters():
        param.requires_grad = True

    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    criterion = nn.CrossEntropyLoss()

    best_val_acc = 0.0
    best_weights = model.state_dict().copy()

    for epoch in range(1, epochs + 1):
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

        train_acc = correct / total
        train_loss = running_loss / total

        # Validation
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                preds = outputs.argmax(dim=1)
                val_correct += (preds == labels).sum().item()
                val_total += labels.size(0)

        val_acc = val_correct / val_total
        print(f"  [{getattr(model, 'name', 'Model')} Epoch {epoch}/{epochs}] Train Acc: {train_acc*100:.2f}% | Val Acc: {val_acc*100:.2f}%")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_weights = model.state_dict().copy()

    model.load_state_dict(best_weights)
    torch.save(
        {
            "model_name": getattr(model, "name", "Model"),
            "state_dict": model.state_dict(),
            "best_val_acc": best_val_acc,
        },
        str(ckpt_path),
    )
    print(f"✓ Saved updated {getattr(model, 'name', 'Model')} to {ckpt_path}")
    return model

def main():
    set_seed(SEED)
    device = get_device("mps")
    print(f"Compute Device: {device}")

    train_loader, val_loader, test_loader, class_names = load_data(
        Path("data/raw"), batch_size=8, seed=SEED
    )

    m1 = build_mobilenet_v2(10)
    m2 = build_densenet121(10)
    m3 = build_resnet50(10)

    p1 = Path("models/mobilenet_v2.pt")
    p2 = Path("models/densenet121.pt")
    p3 = Path("models/resnet50.pt")

    print("\n=== Fine-Tuning Ensemble Members (Batch Size 8, lr=1e-4) ===")
    m1 = finetune_model(m1, train_loader, val_loader, device, p1, epochs=1, lr=1e-4)
    m2 = finetune_model(m2, train_loader, val_loader, device, p2, epochs=1, lr=1e-4)
    m3 = finetune_model(m3, train_loader, val_loader, device, p3, epochs=1, lr=1e-4)

    print("\n=== Evaluating Final Ensemble with Softmax Voting ===")
    eval_results = evaluate_ensemble(
        models=[m1, m2, m3],
        test_loader=test_loader,
        device=device,
        class_names=class_names,
    )

    # Save confusion matrix
    cm_array = np.array(eval_results["confusion_matrix"])
    cm_path = Path("confusion_matrix.png")
    plot_and_save_confusion_matrix(cm_array, class_names, cm_path)
    shutil.copy(cm_path, Path("results") / "confusion_matrix.png")

    report_out = Path("results") / "ensemble_evaluation_report.json"
    with open(report_out, "w") as f:
        json.dump(eval_results, f, indent=2)

    print("\n========================================================")
    print(f"★ FINAL ENSEMBLE TEST ACCURACY: {eval_results['ensemble_accuracy_pct']}%")
    print("========================================================\n")

if __name__ == "__main__":
    main()

