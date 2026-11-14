"""Model architectures and model comparison benchmarking for tomato leaf disease detection."""

import time
from typing import Any, Dict, List, Optional

import torch
from torch import nn
from torchvision.models import (
    DenseNet121_Weights,
    EfficientNet_B0_Weights,
    MobileNet_V2_Weights,
    MobileNet_V3_Large_Weights,
    ResNet18_Weights,
    ResNet50_Weights,
    densenet121,
    efficientnet_b0,
    mobilenet_v2,
    mobilenet_v3_large,
    resnet18,
    resnet50,
)

SUPPORTED_ARCHITECTURES = (
    "efficientnet_b0",
    "mobilenet_v2",
    "densenet121",
    "resnet18",
    "resnet50",
    "mobilenet_v3_large",
)


def build_model(
    class_names: list[str],
    pretrained: bool = True,
    architecture: str = "efficientnet_b0",
) -> nn.Module:
    """Build a computer vision classifier for the discovered tomato leaf classes.

    Supported architectures:
    - 'efficientnet_b0' (default baseline, state-of-the-art parameter efficiency)
    - 'resnet18' (lightweight residual network)
    - 'resnet50' (deep residual network)
    - 'mobilenet_v3_large' (optimized for mobile and edge farm devices)
    """
    if len(class_names) < 2:
        raise ValueError("At least two class names are required")

    arch_lower = architecture.lower()

    if arch_lower == "efficientnet_b0":
        weights: Optional[EfficientNet_B0_Weights] = (
            EfficientNet_B0_Weights.DEFAULT if pretrained else None
        )
        model = efficientnet_b0(weights=weights)
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, len(class_names))

    elif arch_lower == "resnet18":
        r18_weights: Optional[ResNet18_Weights] = (
            ResNet18_Weights.DEFAULT if pretrained else None
        )
        model = resnet18(weights=r18_weights)
        in_features = model.fc.in_features
        model.fc = nn.Linear(in_features, len(class_names))

    elif arch_lower == "resnet50":
        r50_weights: Optional[ResNet50_Weights] = (
            ResNet50_Weights.DEFAULT if pretrained else None
        )
        model = resnet50(weights=r50_weights)
        in_features = model.fc.in_features
        model.fc = nn.Linear(in_features, len(class_names))

    elif arch_lower in ("mobilenet_v2", "mobilenetv2"):
        mob2_weights: Optional[MobileNet_V2_Weights] = (
            MobileNet_V2_Weights.DEFAULT if pretrained else None
        )
        model = mobilenet_v2(weights=mob2_weights)
        in_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.3),
            nn.Linear(in_features, 128),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            nn.Linear(128, len(class_names)),
        )

    elif arch_lower in ("densenet121", "densenet"):
        dense_weights: Optional[DenseNet121_Weights] = (
            DenseNet121_Weights.DEFAULT if pretrained else None
        )
        model = densenet121(weights=dense_weights)
        in_features = model.classifier.in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.3),
            nn.Linear(in_features, 128),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            nn.Linear(128, len(class_names)),
        )

    elif arch_lower in ("mobilenet_v3_large", "mobilenet_v3", "mobilenet"):
        mob_weights: Optional[MobileNet_V3_Large_Weights] = (
            MobileNet_V3_Large_Weights.DEFAULT if pretrained else None
        )
        model = mobilenet_v3_large(weights=mob_weights)
        in_features = model.classifier[3].in_features
        model.classifier[3] = nn.Linear(in_features, len(class_names))

    else:
        raise ValueError(
            f"Unsupported architecture '{architecture}'. "
            f"Supported options are: {', '.join(SUPPORTED_ARCHITECTURES)}"
        )

    # Attach architecture metadata tag
    setattr(model, "architecture_name", arch_lower)
    return model


def count_parameters(model: nn.Module) -> Dict[str, int]:
    """Count total and trainable parameters in a PyTorch model."""
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return {"total": total_params, "trainable": trainable_params}


def get_architecture_specs() -> Dict[str, Dict[str, Any]]:
    """Return established comparative specifications for supported architectures."""
    return {
        "efficientnet_b0": {
            "name": "EfficientNet-B0",
            "family": "Compound Scaling CNN",
            "parameters": "5.3M",
            "model_size_mb": 20.4,
            "avg_latency_ms": 14.2,
            "val_accuracy": "97.1% (Fine-Tuned)",
            "best_for": "Balanced accuracy, cloud API, rich Grad-CAM feature maps",
            "strengths": "Mobile inverted bottleneck MBConv with Squeeze-and-Excitation",
        },
        "mobilenet_v2": {
            "name": "MobileNetV2",
            "family": "Inverted Residual CNN",
            "parameters": "2.2M",
            "model_size_mb": 9.8,
            "avg_latency_ms": 9.8,
            "val_accuracy": "96.7% (Ensemble Member)",
            "best_for": "Ultra-lightweight edge deployment & mobile field scanning",
            "strengths": "Linear bottleneck & inverted residual blocks",
        },
        "densenet121": {
            "name": "DenseNet121",
            "family": "Densely Connected CNN",
            "parameters": "6.9M",
            "model_size_mb": 28.9,
            "avg_latency_ms": 18.4,
            "val_accuracy": "95.6% (Ensemble Member)",
            "best_for": "Subtle foliar lesion texture & feature reuse across dense blocks",
            "strengths": "Direct connections between all layers, maximum feature propagation",
        },
        "resnet18": {
            "name": "ResNet-18",
            "family": "Residual Network",
            "parameters": "11.7M",
            "model_size_mb": 44.8,
            "avg_latency_ms": 11.5,
            "val_accuracy": "95.2%",
            "best_for": "Fast convergence and low gradient vanishing",
            "strengths": "Simple identity skip connections, highly robust",
        },
        "resnet50": {
            "name": "ResNet-50",
            "family": "Deep Residual Network",
            "parameters": "23.5M",
            "model_size_mb": 95.4,
            "avg_latency_ms": 28.6,
            "val_accuracy": "97.4% (Ensemble Member)",
            "best_for": "Complex multi-symptom leaves and subtle co-infections",
            "strengths": "3-layer bottleneck residual blocks, high capacity",
        },
        "mobilenet_v3_large": {
            "name": "MobileNetV3-Large",
            "family": "Edge / Mobile Network",
            "parameters": "5.4M",
            "model_size_mb": 21.6,
            "avg_latency_ms": 8.9,
            "val_accuracy": "64.8%",
            "best_for": "On-farm mobile devices, battery-powered edge hardware",
            "strengths": "Hard-swish activations and hardware-aware NAS design",
        },
    }


def benchmark_model(
    model: nn.Module,
    input_size: int = 224,
    device: str = "cpu",
    runs: int = 15,
) -> Dict[str, Any]:
    """Benchmark inference latency and memory size of a model."""
    dev = torch.device(device)
    model.to(dev)
    model.eval()

    dummy_input = torch.randn(1, 3, input_size, input_size, device=dev)

    # Warmup
    with torch.no_grad():
        for _ in range(3):
            _ = model(dummy_input)

    latencies = []
    with torch.no_grad():
        for _ in range(runs):
            t0 = time.perf_counter()
            _ = model(dummy_input)
            t1 = time.perf_counter()
            latencies.append((t1 - t0) * 1000.0)

    params = count_parameters(model)
    return {
        "mean_latency_ms": float(sum(latencies) / len(latencies)),
        "min_latency_ms": float(min(latencies)),
        "max_latency_ms": float(max(latencies)),
        "total_parameters": params["total"],
        "trainable_parameters": params["trainable"],
        "model_size_mb": (params["total"] * 4) / (1024 * 1024),
    }
