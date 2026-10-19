"""Explainable tomato leaf disease detection package with Grad-CAM and multi-model benchmarking."""

from .config import DEFAULT_CHECKPOINT, DEFAULT_DATA_DIR, TrainingConfig
from .disease_info import DISEASE_PROFILES, DiseaseProfile, get_disease_profile
from .evaluate import evaluate_model, get_baseline_benchmark_data, plot_confusion_matrix
from .explainability import GradCAM, apply_colormap_on_image, explain_prediction
from .model import SUPPORTED_ARCHITECTURES, benchmark_model, build_model, count_parameters

PROJECT_NAME = "Explainable-Tomato-Leaf-Disease-Detection-Using-AI-Ml"
__version__ = "1.0.0"

__all__ = [
    "PROJECT_NAME",
    "__version__",
    "TrainingConfig",
    "DEFAULT_DATA_DIR",
    "DEFAULT_CHECKPOINT",
    "build_model",
    "SUPPORTED_ARCHITECTURES",
    "count_parameters",
    "benchmark_model",
    "GradCAM",
    "explain_prediction",
    "apply_colormap_on_image",
    "DiseaseProfile",
    "DISEASE_PROFILES",
    "get_disease_profile",
    "evaluate_model",
    "plot_confusion_matrix",
    "get_baseline_benchmark_data",
]
