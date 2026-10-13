from typing import Optional

import torch
from torch import nn
from torchvision.models import EfficientNet_B0_Weights, efficientnet_b0


def build_model(
    class_names: list[str], pretrained: bool = True
) -> nn.Module:
    """Build an EfficientNet-B0 classifier for the discovered classes."""
    if len(class_names) < 2:
        raise ValueError("At least two class names are required")
    weights: Optional[EfficientNet_B0_Weights] = (
        EfficientNet_B0_Weights.DEFAULT if pretrained else None
    )
    model = efficientnet_b0(weights=weights)
    input_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(input_features, len(class_names))
    return model
