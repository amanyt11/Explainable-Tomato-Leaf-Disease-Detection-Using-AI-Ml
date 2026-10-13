from pathlib import Path

import pytest

from src.tomato_leaf_detection.config import TrainingConfig
from src.tomato_leaf_detection.data import build_transforms


def test_default_configuration_is_valid() -> None:
    TrainingConfig().validate()


def test_invalid_validation_fraction_is_rejected() -> None:
    with pytest.raises(ValueError):
        TrainingConfig(validation_fraction=1.0).validate()


def test_transforms_produce_expected_pipeline() -> None:
    train_transform, validation_transform = build_transforms(224)
    assert len(train_transform.transforms) == 5
    assert len(validation_transform.transforms) == 3
