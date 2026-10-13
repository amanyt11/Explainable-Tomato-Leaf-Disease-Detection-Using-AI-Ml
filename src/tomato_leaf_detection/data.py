from pathlib import Path
from typing import Tuple

import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms

from .config import TrainingConfig


def build_transforms(image_size: int) -> Tuple[transforms.Compose, transforms.Compose]:
    """Return training and validation transforms for RGB leaf images."""
    normalize = transforms.Normalize(
        mean=(0.485, 0.456, 0.406),
        std=(0.229, 0.224, 0.225),
    )
    train_transform = transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ToTensor(),
            normalize,
        ]
    )
    validation_transform = transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            normalize,
        ]
    )
    return train_transform, validation_transform


def create_dataloaders(
    data_dir: Path, config: TrainingConfig
) -> Tuple[DataLoader, DataLoader, list[str]]:
    """Create loaders from either an ImageFolder or train/val directory."""
    config.validate()
    data_dir = Path(data_dir)
    if not data_dir.is_dir():
        raise FileNotFoundError(f"Dataset directory does not exist: {data_dir}")

    train_transform, validation_transform = build_transforms(config.image_size)
    has_explicit_split = (data_dir / "train").is_dir() and (data_dir / "val").is_dir()
    if has_explicit_split:
        train_dataset = datasets.ImageFolder(data_dir / "train", transform=train_transform)
        validation_dataset = datasets.ImageFolder(
            data_dir / "val", transform=validation_transform
        )
        if train_dataset.classes != validation_dataset.classes:
            raise ValueError("Train and validation directories must have matching classes")
        if len(train_dataset) == 0 or len(validation_dataset) == 0:
            raise ValueError("Train and validation directories must contain images")
        train_indices = list(range(len(train_dataset)))
        validation_indices = list(range(len(validation_dataset)))
        class_names = train_dataset.classes
    else:
        base_dataset = datasets.ImageFolder(data_dir)
        if len(base_dataset) < 2:
            raise ValueError("Dataset must contain at least two images")
        if len(base_dataset.classes) < 2:
            raise ValueError("Dataset must contain at least two class directories")

        labels = base_dataset.targets
        indices = list(range(len(base_dataset)))
        try:
            train_indices, validation_indices = train_test_split(
                indices,
                test_size=config.validation_fraction,
                random_state=config.random_seed,
                stratify=labels,
            )
        except ValueError as exc:
            raise ValueError(
                "Unable to create a stratified split. Add more images to each class."
            ) from exc

        train_dataset = datasets.ImageFolder(data_dir, transform=train_transform)
        validation_dataset = datasets.ImageFolder(data_dir, transform=validation_transform)
        class_names = base_dataset.classes
    generator = torch.Generator().manual_seed(config.random_seed)
    train_loader = DataLoader(
        Subset(train_dataset, train_indices),
        batch_size=config.batch_size,
        shuffle=True,
        generator=generator,
        num_workers=config.num_workers,
    )
    validation_loader = DataLoader(
        Subset(validation_dataset, validation_indices),
        batch_size=config.batch_size,
        shuffle=False,
        num_workers=config.num_workers,
    )
    return train_loader, validation_loader, class_names
