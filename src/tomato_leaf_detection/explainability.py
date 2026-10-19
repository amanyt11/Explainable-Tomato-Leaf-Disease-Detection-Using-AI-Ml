"""Explainability engine for tomato leaf disease detection using Grad-CAM.

Implements Gradient-weighted Class Activation Mapping (Grad-CAM) to visualize
and explain the spatial attention of deep convolutional neural networks.
"""

from typing import Any, List, Optional, Tuple, Union

import matplotlib.cm as cm
import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms


def find_target_layer(model: nn.Module) -> nn.Module:
    """Automatically find the best final convolutional layer for Grad-CAM.

    Supports EfficientNet, ResNet, MobileNetV3, and generic CNN architectures.
    """
    # 1. EfficientNet family
    if hasattr(model, "features") and isinstance(model.features, (nn.Sequential, nn.ModuleList)):
        for layer in reversed(model.features):
            if isinstance(layer, nn.Conv2d) or any(isinstance(m, nn.Conv2d) for m in layer.modules()):
                return layer

    # 2. ResNet family
    if hasattr(model, "layer4"):
        return model.layer4[-1]

    # 3. MobileNet family
    if hasattr(model, "features"):
        return model.features[-1]

    # 4. Fallback: find the last Conv2d module in the entire model
    conv_layers = [m for m in model.modules() if isinstance(m, nn.Conv2d)]
    if conv_layers:
        return conv_layers[-1]

    raise ValueError("No suitable convolutional layer found for Grad-CAM in this model.")


class GradCAM:
    """Gradient-weighted Class Activation Mapping for model visual explanations."""

    def __init__(self, model: nn.Module, target_layer: Optional[nn.Module] = None):
        self.model = model
        self.model.eval()
        self.target_layer = target_layer or find_target_layer(model)
        self.activations: Optional[torch.Tensor] = None
        self.gradients: Optional[torch.Tensor] = None
        self.handles: List[Any] = []
        self._register_hooks()

    def _register_hooks(self) -> None:
        def forward_hook(module: nn.Module, input: Any, output: torch.Tensor) -> None:
            self.activations = output.detach()

        def backward_hook(module: nn.Module, grad_input: Any, grad_output: Tuple[torch.Tensor, ...]) -> None:
            if grad_output and grad_output[0] is not None:
                self.gradients = grad_output[0].detach()

        self.handles.append(self.target_layer.register_forward_hook(forward_hook))
        self.handles.append(self.target_layer.register_full_backward_hook(backward_hook))

    def remove_hooks(self) -> None:
        for handle in self.handles:
            handle.remove()
        self.handles.clear()

    def __enter__(self) -> "GradCAM":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.remove_hooks()

    def generate_heatmap(
        self,
        input_tensor: torch.Tensor,
        target_class: Optional[int] = None,
    ) -> Tuple[np.ndarray, int, float]:
        """Compute the raw 2D Grad-CAM heatmap normalized to [0, 1].

        Args:
            input_tensor: Shape (1, 3, H, W) normalized image tensor.
            target_class: Target class index. If None, highest scoring class is used.

        Returns:
            Tuple of:
                - heatmap: 2D numpy array of shape (H, W) in range [0, 1]
                - predicted_class: Index of predicted class
                - confidence: Softmax probability of target class
        """
        self.model.zero_grad()
        input_tensor = input_tensor.clone().requires_grad_(True)

        logits = self.model(input_tensor)
        probabilities = torch.softmax(logits, dim=1)[0]

        if target_class is None:
            target_class = int(torch.argmax(probabilities).item())

        confidence = float(probabilities[target_class].item())

        score = logits[0, target_class]
        score.backward(retain_graph=True)

        if self.gradients is None or self.activations is None:
            raise RuntimeError("Failed to capture gradients or activations for Grad-CAM.")

        # Global average pooling of gradients: weights alpha_k
        # Gradients: (1, C, H', W')
        weights = torch.mean(self.gradients, dim=(2, 3), keepdim=True)
        # Weighted combination: sum_k (alpha_k * A^k)
        cam = torch.sum(weights * self.activations, dim=1, keepdim=True)
        # Apply ReLU to focus on features positively contributing to target class
        cam = torch.relu(cam)

        # Upsample CAM to input tensor dimensions (H, W)
        cam = nn.functional.interpolate(
            cam,
            size=(input_tensor.shape[2], input_tensor.shape[3]),
            mode="bilinear",
            align_corners=False,
        )

        cam_np = cam.squeeze().cpu().numpy()

        # Normalize to [0, 1]
        cam_min, cam_max = cam_np.min(), cam_np.max()
        if cam_max - cam_min > 1e-8:
            heatmap = (cam_np - cam_min) / (cam_max - cam_min)
        else:
            heatmap = np.zeros_like(cam_np)

        return heatmap, target_class, confidence


def apply_colormap_on_image(
    original_image: Image.Image,
    heatmap: np.ndarray,
    colormap_name: str = "jet",
    alpha: float = 0.45,
) -> Tuple[Image.Image, Image.Image, Image.Image]:
    """Colorize a 2D heatmap and blend it with the original PIL image.

    Args:
        original_image: Source PIL image.
        heatmap: 2D numpy array [0, 1].
        colormap_name: Matplotlib colormap ('jet', 'turbo', 'viridis', 'plasma', 'magma').
        alpha: Blend weight for heatmap [0.0 - 1.0].

    Returns:
        Tuple of:
            - blended_image: Heatmap overlayed on original leaf
            - raw_heatmap_colored: Pure colorized heatmap image
            - focus_masked_image: Original leaf with low-attention regions dimmed
    """
    orig_rgb = original_image.convert("RGB")
    width, height = orig_rgb.size

    # Resize heatmap to match original image dimensions if needed
    if (heatmap.shape[1], heatmap.shape[0]) != (width, height):
        heatmap_img = Image.fromarray((heatmap * 255).astype(np.uint8))
        heatmap_resized = heatmap_img.resize((width, height), resample=Image.Resampling.BILINEAR)
        heatmap = np.array(heatmap_resized, dtype=np.float32) / 255.0

    # Get colormap using modern matplotlib API
    try:
        import matplotlib as mpl
        cmap = mpl.colormaps.get(colormap_name, mpl.colormaps["jet"])
    except Exception:
        import matplotlib.pyplot as plt
        cmap = plt.get_cmap("jet")

    # Apply colormap to get RGBA, convert to RGB
    colored_heatmap = cmap(heatmap)  # shape (H, W, 4) in [0, 1]
    heatmap_rgb = (colored_heatmap[:, :, :3] * 255).astype(np.uint8)
    heatmap_pil = Image.fromarray(heatmap_rgb)

    # Blend original image with heatmap
    orig_np = np.array(orig_rgb, dtype=np.float32)
    alpha = max(0.0, min(1.0, alpha))
    blended_np = (1.0 - alpha) * orig_np + alpha * heatmap_rgb.astype(np.float32)
    blended_np = np.clip(blended_np, 0, 255).astype(np.uint8)
    blended_pil = Image.fromarray(blended_np)

    # Focus mask: highlight regions with attention >= 0.35, dim unaffected background
    mask = np.clip(heatmap * 1.5, 0.2, 1.0)[:, :, np.newaxis]
    focus_np = (orig_np * mask).astype(np.uint8)
    focus_pil = Image.fromarray(focus_np)

    return blended_pil, heatmap_pil, focus_pil


def explain_prediction(
    model: nn.Module,
    image: Image.Image,
    class_names: Optional[List[str]] = None,
    image_size: int = 224,
    target_class: Optional[int] = None,
    colormap_name: str = "jet",
    alpha: float = 0.45,
    top_k: int = 3,
) -> dict:
    """One-stop explainability function.

    Takes a PIL image and model, returns prediction probabilities, top class,
    Grad-CAM heatmaps, and diagnostic metadata.
    """
    preprocessing = transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        ]
    )
    tensor = preprocessing(image.convert("RGB")).unsqueeze(0)

    # Compute full class probability distribution
    with torch.no_grad():
        logits = model(tensor)
        probabilities = torch.softmax(logits, dim=1)[0].cpu().numpy()

    with GradCAM(model) as gradcam:
        heatmap, pred_idx, confidence = gradcam.generate_heatmap(tensor, target_class=target_class)

    blended, heatmap_colored, focus = apply_colormap_on_image(
        image, heatmap, colormap_name=colormap_name, alpha=alpha
    )

    # Compute attention intensity metrics
    high_activation_ratio = float(np.mean(heatmap >= 0.5))
    peak_attention_coords = np.unravel_index(np.argmax(heatmap), heatmap.shape)

    # Top-K ranking
    top_indices = np.argsort(probabilities)[::-1][:top_k]
    top_predictions = []
    for rank, idx in enumerate(top_indices):
        name = class_names[idx] if class_names and idx < len(class_names) else f"Class {idx}"
        top_predictions.append(
            {
                "rank": rank + 1,
                "class_index": int(idx),
                "class_name": name,
                "probability": float(probabilities[idx]),
            }
        )

    predicted_label = class_names[pred_idx] if class_names and pred_idx < len(class_names) else str(pred_idx)

    return {
        "predicted_class_index": pred_idx,
        "predicted_label": predicted_label,
        "confidence": confidence,
        "all_probabilities": probabilities.tolist(),
        "top_predictions": top_predictions,
        "heatmap_raw": heatmap,
        "blended_image": blended,
        "heatmap_image": heatmap_colored,
        "focus_image": focus,
        "high_activation_ratio": high_activation_ratio,
        "peak_attention_pixel": (int(peak_attention_coords[1]), int(peak_attention_coords[0])),
    }
