import argparse
import json
from pathlib import Path
from typing import Dict

import torch
from torch import nn
from torch.optim import AdamW

from .config import DEFAULT_CHECKPOINT, DEFAULT_DATA_DIR, TrainingConfig
from .data import create_dataloaders
from .model import build_model


def run_epoch(
    model: nn.Module,
    loader: torch.utils.data.DataLoader,
    criterion: nn.Module,
    device: torch.device,
    optimizer: AdamW | None = None,
) -> Dict[str, float]:
    training = optimizer is not None
    model.train(training)
    total_loss = 0.0
    correct = 0
    total = 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        if training:
            optimizer.zero_grad(set_to_none=True)
        with torch.set_grad_enabled(training):
            outputs = model(images)
            loss = criterion(outputs, labels)
            if training:
                loss.backward()
                optimizer.step()
        total_loss += loss.item() * labels.size(0)
        correct += (outputs.argmax(dim=1) == labels).sum().item()
        total += labels.size(0)
    return {"loss": total_loss / total, "accuracy": correct / total}


def train(
    data_dir: Path,
    output: Path,
    epochs: int,
    config: TrainingConfig,
    device: torch.device,
    pretrained: bool = True,
) -> None:
    train_loader, validation_loader, class_names = create_dataloaders(data_dir, config)
    model = build_model(class_names, pretrained=pretrained).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = AdamW(
        model.parameters(),
        lr=config.learning_rate,
        weight_decay=config.weight_decay,
    )
    best_accuracy = -1.0
    history = []
    for epoch in range(1, epochs + 1):
        train_metrics = run_epoch(model, train_loader, criterion, device, optimizer)
        validation_metrics = run_epoch(model, validation_loader, criterion, device)
        record = {
            "epoch": epoch,
            "train": train_metrics,
            "validation": validation_metrics,
        }
        history.append(record)
        print(json.dumps(record))
        if validation_metrics["accuracy"] > best_accuracy:
            best_accuracy = validation_metrics["accuracy"]
            output.parent.mkdir(parents=True, exist_ok=True)
            torch.save(
                {
                    "model_state": model.state_dict(),
                    "class_names": class_names,
                    "image_size": config.image_size,
                    "history": history,
                },
                output,
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the tomato leaf baseline")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--validation-fraction", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", choices=("auto", "cpu", "cuda", "mps"), default="auto")
    parser.add_argument(
        "--no-pretrained",
        action="store_true",
        help="Avoid downloading ImageNet weights; useful for offline training",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.epochs <= 0:
        raise ValueError("--epochs must be positive")
    if args.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is not available")
    if args.device == "mps" and not torch.backends.mps.is_available():
        raise RuntimeError("MPS was requested but is not available")
    if args.device == "auto":
        device_name = (
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )
    else:
        device_name = args.device
    device = torch.device(device_name)
    config = TrainingConfig(
        batch_size=args.batch_size,
        validation_fraction=args.validation_fraction,
        random_seed=args.seed,
    )
    train(
        args.data_dir,
        args.output,
        args.epochs,
        config,
        device,
        pretrained=not args.no_pretrained,
    )


if __name__ == "__main__":
    main()
