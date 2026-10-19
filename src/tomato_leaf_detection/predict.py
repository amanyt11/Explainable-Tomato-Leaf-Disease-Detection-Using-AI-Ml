"""Command-line interface for tomato leaf disease prediction and Grad-CAM explainability."""

import argparse
import json
from pathlib import Path
from typing import Optional

import torch
from PIL import Image

from .config import DEFAULT_CHECKPOINT
from .disease_info import get_disease_profile
from .explainability import explain_prediction
from .model import build_model


def predict_image(
    image_path: Path,
    checkpoint_path: Path = DEFAULT_CHECKPOINT,
    explain: bool = False,
    output_dir: Optional[Path] = None,
    colormap: str = "jet",
    alpha: float = 0.45,
) -> dict:
    """Run inference and optional Grad-CAM explainability on an image file."""
    image_path = Path(image_path)
    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found at {image_path}")

    checkpoint_path = Path(checkpoint_path)
    if not checkpoint_path.is_file():
        raise FileNotFoundError(f"Checkpoint not found at {checkpoint_path}")

    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    class_names = checkpoint["class_names"]
    image_size = checkpoint.get("image_size", 224)

    model = build_model(class_names, pretrained=False)
    model.load_state_dict(checkpoint["model_state"])
    model.eval()

    image = Image.open(image_path)
    explanation = explain_prediction(
        model=model,
        image=image,
        class_names=class_names,
        image_size=image_size,
        colormap_name=colormap,
        alpha=alpha,
    )

    pred_label = explanation["predicted_label"]
    profile = get_disease_profile(pred_label)

    output_files = {}
    if explain and output_dir is not None:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        stem = image_path.stem

        blend_path = out_path / f"{stem}_gradcam_blend.png"
        heatmap_path = out_path / f"{stem}_gradcam_heatmap.png"
        focus_path = out_path / f"{stem}_focus.png"

        explanation["blended_image"].save(blend_path)
        explanation["heatmap_image"].save(heatmap_path)
        explanation["focus_image"].save(focus_path)

        output_files["blended_image"] = str(blend_path)
        output_files["heatmap_image"] = str(heatmap_path)
        output_files["focus_image"] = str(focus_path)

    return {
        "image": str(image_path),
        "predicted_label": pred_label,
        "display_name": profile.display_name,
        "scientific_name": profile.scientific_name,
        "pathogen_type": profile.pathogen_type,
        "severity": profile.severity,
        "confidence": explanation["confidence"],
        "top_predictions": explanation["top_predictions"],
        "symptoms": profile.symptoms,
        "immediate_actions": profile.immediate_actions,
        "organic_treatment": profile.organic_treatment,
        "saved_explanations": output_files,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Predict tomato leaf disease from image")
    parser.add_argument("--image", type=Path, required=True, help="Path to leaf image")
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT, help="Checkpoint path")
    parser.add_argument("--explain", action="store_true", help="Generate Grad-CAM visual explanations")
    parser.add_argument("--output-dir", type=Path, default=Path("results"), help="Folder to save explanation images")
    parser.add_argument("--colormap", default="jet", help="Colormap for Grad-CAM (jet, turbo, viridis, plasma)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = predict_image(
        image_path=args.image,
        checkpoint_path=args.checkpoint,
        explain=args.explain,
        output_dir=args.output_dir if args.explain else None,
        colormap=args.colormap,
    )
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("=" * 60)
        print("🍅 Tomato Leaf Disease Diagnosis")
        print("=" * 60)
        print(f"Condition:        {results['display_name']} ({results['predicted_label']})")
        print(f"Confidence:       {results['confidence']:.1%}")
        print(f"Pathogen:         {results['pathogen_type']} ({results['scientific_name']})")
        print(f"Severity:         {results['severity']}")
        print("\nTop Probabilities:")
        for top in results["top_predictions"]:
            print(f"  {top['rank']}. {top['class_name']}: {top['probability']:.1%}")
        print("\nPrimary Symptoms:")
        for s in results["symptoms"]:
            print(f"  • {s}")
        print("\nImmediate Action:")
        for a in results["immediate_actions"]:
            print(f"  ✓ {a}")
        if results.get("saved_explanations"):
            print("\nSaved Visual Explanations:")
            for k, v in results["saved_explanations"].items():
                print(f"  - {k}: {v}")
        print("=" * 60)


if __name__ == "__main__":
    main()
