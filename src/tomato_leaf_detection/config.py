from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TrainingConfig:
    """Settings shared by training and inference."""

    image_size: int = 224
    batch_size: int = 32
    validation_fraction: float = 0.2
    random_seed: int = 42
    learning_rate: float = 1e-3
    weight_decay: float = 1e-4
    num_workers: int = 0

    def validate(self) -> None:
        if not 0 < self.validation_fraction < 1:
            raise ValueError("validation_fraction must be between 0 and 1")
        if self.image_size <= 0 or self.batch_size <= 0:
            raise ValueError("image_size and batch_size must be positive")


DEFAULT_DATA_DIR = Path("data/raw")
DEFAULT_CHECKPOINT = Path("models/best.pt")
