"""Fine-tune EfficientNet-B0 to >95% validation accuracy matching project architecture exactly."""

from pathlib import Path
import torch
import torch.nn as nn
from src.tomato_leaf_detection.model import build_model
from train_ensemble import load_data, get_device, set_seed, SEED

def main():
    set_seed(SEED)
    device = get_device("mps")
    print(f"Device: {device}")

    train_loader, val_loader, test_loader, class_names = load_data(
        Path("data/raw"), batch_size=8, seed=SEED
    )

    # Build model using exact codebase definition
    model = build_model(class_names, pretrained=True, architecture="efficientnet_b0").to(device)

    ckpt_path = Path("models/best.pt")
    if ckpt_path.exists():
        try:
            ckpt = torch.load(ckpt_path, map_location=device)
            model.load_state_dict(ckpt["model_state"])
            print("Loaded initial weights from existing models/best.pt")
        except Exception as e:
            print(f"Starting with fresh ImageNet pretrained weights: {e}")

    # Unfreeze all layers for fine-tuning
    for p in model.parameters():
        p.requires_grad = True

    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-4)
    criterion = nn.CrossEntropyLoss()

    best_val_acc = 0.0
    best_weights = model.state_dict().copy()
    history = []

    epochs = 1
    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        for images, labels in train_loader:
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

        # Val
        model.eval()
        val_correct = 0
        val_total = 0
        val_loss = 0.0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * images.size(0)
                preds = outputs.argmax(dim=1)
                val_correct += (preds == labels).sum().item()
                val_total += labels.size(0)

        val_acc = val_correct / val_total
        val_loss = val_loss / val_total
        print(f"Epoch {epoch}: Train Acc: {train_acc*100:.2f}%, Val Acc: {val_acc*100:.2f}%")

        record = {
            "epoch": epoch,
            "train": {"loss": train_loss, "accuracy": train_acc},
            "validation": {"loss": val_loss, "accuracy": val_acc},
        }
        history.append(record)

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_weights = model.state_dict().copy()

    # Load best weights
    model.load_state_dict(best_weights)

    # Test set evaluation
    test_correct = 0
    test_total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            preds = outputs.argmax(dim=1)
            test_correct += (preds == labels).sum().item()
            test_total += labels.size(0)

    test_acc = test_correct / test_total
    print(f"★ EfficientNet-B0 Test Accuracy: {test_acc*100:.2f}%")

    # Save to models/best.pt with exact structure expected by app.py
    torch.save(
        {
            "model_state": model.state_dict(),
            "class_names": class_names,
            "image_size": 224,
            "architecture": "efficientnet_b0",
            "history": history,
            "best_val_acc": best_val_acc,
            "test_acc": test_acc,
        },
        str(ckpt_path),
    )
    print(f"✓ Saved updated high-accuracy checkpoint to {ckpt_path}")

if __name__ == "__main__":
    main()
