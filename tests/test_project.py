"""Comprehensive test suite for the explainable tomato leaf disease detection package."""

from pathlib import Path

import numpy as np
import pytest
import torch
from PIL import Image

from src.tomato_leaf_detection.config import TrainingConfig
from src.tomato_leaf_detection.data import build_transforms
from src.tomato_leaf_detection.disease_info import (
    DISEASE_PROFILES,
    DiseaseProfile,
    get_disease_profile,
)
from src.tomato_leaf_detection.evaluate import (
    analyze_confusion_errors,
    get_baseline_benchmark_data,
    plot_confusion_matrix,
)
from src.tomato_leaf_detection.explainability import (
    GradCAM,
    apply_colormap_on_image,
    explain_prediction,
    find_target_layer,
)
from src.tomato_leaf_detection.model import (
    SUPPORTED_ARCHITECTURES,
    benchmark_model,
    build_model,
    count_parameters,
    get_architecture_specs,
)
from src.tomato_leaf_detection.predict import predict_image

SAMPLE_CLASSES = [
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___healthy",
]


# =============================================================================
# 1. Configuration & Data Tests
# =============================================================================


def test_default_configuration_is_valid() -> None:
    TrainingConfig().validate()


def test_invalid_validation_fraction_is_rejected() -> None:
    with pytest.raises(ValueError):
        TrainingConfig(validation_fraction=1.0).validate()
    with pytest.raises(ValueError):
        TrainingConfig(validation_fraction=0.0).validate()


def test_invalid_image_or_batch_size_is_rejected() -> None:
    with pytest.raises(ValueError):
        TrainingConfig(image_size=0).validate()
    with pytest.raises(ValueError):
        TrainingConfig(batch_size=-4).validate()


def test_transforms_produce_expected_pipeline() -> None:
    train_transform, validation_transform = build_transforms(224)
    assert len(train_transform.transforms) == 5
    assert len(validation_transform.transforms) == 3


# =============================================================================
# 2. Multi-Model Architecture Tests
# =============================================================================


@pytest.mark.parametrize("arch", SUPPORTED_ARCHITECTURES)
def test_all_supported_architectures_instantiate(arch: str) -> None:
    model = build_model(SAMPLE_CLASSES, pretrained=False, architecture=arch)
    assert isinstance(model, torch.nn.Module)
    params = count_parameters(model)
    assert params["total"] > 1_000_000
    assert params["trainable"] == params["total"]


def test_unsupported_architecture_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Unsupported architecture"):
        build_model(SAMPLE_CLASSES, pretrained=False, architecture="transformer_v99")


def test_insufficient_classes_raises_value_error() -> None:
    with pytest.raises(ValueError, match="At least two class names"):
        build_model(["SingleClass"], pretrained=False)


def test_architecture_specs_coverage() -> None:
    specs = get_architecture_specs()
    for arch in SUPPORTED_ARCHITECTURES:
        assert arch in specs
        assert "parameters" in specs[arch]
        assert "model_size_mb" in specs[arch]
        assert "avg_latency_ms" in specs[arch]


def test_benchmark_model_runs() -> None:
    model = build_model(SAMPLE_CLASSES, pretrained=False, architecture="mobilenet_v3_large")
    metrics = benchmark_model(model, input_size=64, runs=2)
    assert "mean_latency_ms" in metrics
    assert "model_size_mb" in metrics
    assert metrics["mean_latency_ms"] >= 0.0


# =============================================================================
# 3. Explainability & Grad-CAM Tests
# =============================================================================


def test_find_target_layer_for_all_architectures() -> None:
    for arch in SUPPORTED_ARCHITECTURES:
        model = build_model(SAMPLE_CLASSES, pretrained=False, architecture=arch)
        layer = find_target_layer(model)
        assert layer is not None


def test_gradcam_generates_valid_normalized_heatmap() -> None:
    model = build_model(SAMPLE_CLASSES, pretrained=False, architecture="efficientnet_b0")
    dummy_input = torch.randn(1, 3, 128, 128)

    with GradCAM(model) as gradcam:
        heatmap, pred_idx, conf = gradcam.generate_heatmap(dummy_input, target_class=1)

    assert heatmap.shape == (128, 128)
    assert 0 <= pred_idx < len(SAMPLE_CLASSES)
    assert 0.0 <= conf <= 1.0
    assert heatmap.min() >= 0.0
    assert heatmap.max() <= 1.0


def test_colormap_blending_produces_pil_images() -> None:
    orig = Image.new("RGB", (100, 100), color=(30, 120, 40))
    raw_hm = np.random.uniform(0.0, 1.0, (100, 100)).astype(np.float32)

    blended, colored_hm, focus = apply_colormap_on_image(
        original_image=orig,
        heatmap=raw_hm,
        colormap_name="turbo",
        alpha=0.6,
    )

    assert isinstance(blended, Image.Image)
    assert isinstance(colored_hm, Image.Image)
    assert isinstance(focus, Image.Image)
    assert blended.size == (100, 100)


def test_explain_prediction_end_to_end() -> None:
    model = build_model(SAMPLE_CLASSES, pretrained=False, architecture="efficientnet_b0")
    dummy_img = Image.new("RGB", (160, 160), color=(50, 150, 60))

    result = explain_prediction(
        model=model,
        image=dummy_img,
        class_names=SAMPLE_CLASSES,
        image_size=160,
        top_k=2,
    )

    assert "predicted_label" in result
    assert result["predicted_label"] in SAMPLE_CLASSES
    assert len(result["top_predictions"]) == 2
    assert "blended_image" in result
    assert "peak_attention_pixel" in result


# =============================================================================
# 4. Agronomic Disease Knowledge Tests
# =============================================================================


def test_all_ten_classes_have_profiles() -> None:
    assert len(DISEASE_PROFILES) == 10
    for key, profile in DISEASE_PROFILES.items():
        assert isinstance(profile, DiseaseProfile)
        assert len(profile.symptoms) >= 2
        assert len(profile.immediate_actions) >= 2
        assert len(profile.organic_treatment) >= 1
        assert len(profile.chemical_treatment) >= 1
        assert len(profile.prevention) >= 1


def test_get_disease_profile_fallback() -> None:
    profile = get_disease_profile("NonExistent_disease_name")
    assert profile is not None
    assert "NonExistent" in profile.display_name


# =============================================================================
# 5. Evaluation & Confusion Matrix Tests
# =============================================================================


def test_baseline_benchmark_data_structure() -> None:
    data = get_baseline_benchmark_data()
    assert len(data["class_names"]) == 10
    assert 0.0 < data["accuracy"] < 1.0
    assert len(data["confusion_matrix"]) == 10
    assert len(data["top_confusions"]) > 0


def test_analyze_confusion_errors() -> None:
    cm = np.array(
        [
            [10, 2, 0],
            [1, 9, 3],
            [0, 1, 10],
        ]
    )
    names = ["C0", "C1", "C2"]
    confusions = analyze_confusion_errors(cm, names)
    assert len(confusions) > 0
    # Top error should be C1 -> C2 (count = 3)
    assert confusions[0]["true_class"] == "C1"
    assert confusions[0]["predicted_class"] == "C2"
    assert confusions[0]["error_count"] == 3


def test_plot_confusion_matrix_returns_figure() -> None:
    cm = np.eye(4, dtype=int)
    fig = plot_confusion_matrix(cm, SAMPLE_CLASSES, normalize=True)
    assert fig is not None


# =============================================================================
# 6. Predict CLI Integration Test
# =============================================================================


def test_predict_image_with_checkpoint(tmp_path: Path) -> None:
    ckpt_path = Path("models/best.pt")
    if not ckpt_path.is_file():
        pytest.skip("models/best.pt not found on disk")

    sample_img_path = tmp_path / "test_leaf.jpg"
    img = Image.new("RGB", (224, 224), color=(34, 139, 34))
    img.save(sample_img_path)

    out_dir = tmp_path / "explanations"
    results = predict_image(
        image_path=sample_img_path,
        checkpoint_path=ckpt_path,
        explain=True,
        output_dir=out_dir,
    )

    assert "predicted_label" in results
    assert "confidence" in results
    assert len(results["top_predictions"]) >= 1
    assert "blended_image" in results["saved_explanations"]
    assert Path(results["saved_explanations"]["blended_image"]).is_file()
