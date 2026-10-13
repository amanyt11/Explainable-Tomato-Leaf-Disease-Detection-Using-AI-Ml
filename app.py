from pathlib import Path
from typing import Any, Optional

import streamlit as st
import torch
from PIL import Image
from torchvision import transforms

from src.tomato_leaf_detection import PROJECT_NAME
from src.tomato_leaf_detection.model import build_model


@st.cache_resource
def load_checkpoint(path: str) -> tuple[Any, list[str], int]:
    checkpoint = torch.load(path, map_location="cpu", weights_only=False)
    class_names = checkpoint["class_names"]
    image_size = checkpoint.get("image_size", 224)
    model = build_model(class_names, pretrained=False)
    model.load_state_dict(checkpoint["model_state"])
    model.eval()
    return model, class_names, image_size


def predict(model: Any, class_names: list[str], image: Image.Image, image_size: int) -> tuple[str, float]:
    preprocessing = transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        ]
    )
    with torch.no_grad():
        probabilities = torch.softmax(model(preprocessing(image.convert("RGB")).unsqueeze(0)), dim=1)[0]
    index = int(probabilities.argmax())
    return class_names[index], float(probabilities[index])


st.set_page_config(page_title=PROJECT_NAME, page_icon="🍅")
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f7fbf7 0%, #f4f7f5 52%, #eef7f1 100%);
    }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 1180px; padding-top: 3.5rem; }
    .hero {
        background: linear-gradient(120deg, #123a2a 0%, #1d5c40 65%, #2d7b51 100%);
        border-radius: 26px;
        padding: 2.6rem 3rem 2.4rem;
        color: white;
        box-shadow: 0 16px 38px rgba(18, 58, 42, .18);
        margin-bottom: 1.25rem;
    }
    .hero-kicker {
        color: #b8e8c9;
        font-size: .78rem;
        font-weight: 700;
        letter-spacing: .16em;
        text-transform: uppercase;
        margin-bottom: .7rem;
    }
    .hero h1 { color: white; font-size: 2.55rem; line-height: 1.1; margin: 0; }
    .hero p { color: #d9f0e0; font-size: 1.05rem; margin: 1rem 0 0; }
    .metric-card {
        background: rgba(255,255,255,.86);
        border: 1px solid #dbe9df;
        border-radius: 16px;
        padding: 1rem 1.15rem;
        min-height: 92px;
    }
    .metric-label { color: #6a7d71; font-size: .78rem; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; }
    .metric-value { color: #16432e; font-size: 1.45rem; font-weight: 750; margin-top: .35rem; }
    .section-title { color: #16432e; font-size: 1.35rem; font-weight: 750; margin: .8rem 0 .2rem; }
    .section-subtitle { color: #718178; margin-bottom: 1rem; }
    div[data-testid="stFileUploader"] {
        background: rgba(255,255,255,.78);
        border: 1.5px dashed #85b79a;
        border-radius: 18px;
        padding: .65rem;
    }
    .status-pill {
        display: inline-block;
        background: #d9f2e1;
        color: #17633b;
        border-radius: 999px;
        padding: .28rem .7rem;
        font-size: .78rem;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Team Green tech · AI/ML plant health</div>
        <h1>Explainable Tomato Leaf<br> Disease Detection</h1>
        <p>Upload a leaf image to identify its condition with our baseline computer-vision model.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_columns = st.columns(4)
metrics = [
    ("Project progress", "25%"),
    ("Model", "EfficientNet-B0"),
    ("Disease classes", "10"),
    ("Validation accuracy", "65.9%"),
]
for column, (label, value) in zip(metric_columns, metrics):
    column.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="section-title">Run a leaf health check</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Use a clear, well-lit photo with the leaf filling most of the frame.</div>',
    unsafe_allow_html=True,
)

upload_column, info_column = st.columns([1.45, 1], gap="large")
with upload_column:
    uploaded_file = st.file_uploader(
        "Upload a tomato leaf image",
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG and PNG. Maximum size: 200 MB.",
    )
with info_column:
    st.markdown(
        """
        <div class="metric-card">
        <span class="status-pill">● Baseline model ready</span>
        <div style="margin-top: .85rem; color: #53645a; line-height: 1.55;">
        Your image is processed locally by the trained classifier.
        Explainability heatmaps are planned for the next milestone.
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

checkpoint_path = Path(
    st.sidebar.text_input("Checkpoint path", "models/best.pt")
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.divider()
    preview_column, result_column = st.columns([1, 1], gap="large")
    with preview_column:
        st.markdown('<div class="section-title">Image preview</div>', unsafe_allow_html=True)
        st.image(image, use_container_width=True)
    with result_column:
        st.markdown('<div class="section-title">Analysis result</div>', unsafe_allow_html=True)
        if not checkpoint_path.is_file():
            st.info(
                "No trained checkpoint was found. Place the dataset in `data/raw/` "
                "and run the training command from the README."
            )
        else:
            try:
                model, class_names, image_size = load_checkpoint(str(checkpoint_path))
                label, confidence = predict(model, class_names, image, image_size)
                st.success(f"Prediction: {label.replace('___', ' · ').replace('_', ' ')}")
                st.metric("Confidence", f"{confidence:.1%}")
                st.progress(confidence, text="Model confidence")
                st.caption(
                    "This is a baseline classifier prediction. Visual explanation overlays "
                    "will be added in the next milestone."
                )
            except (KeyError, RuntimeError, ValueError) as exc:
                st.error(f"Unable to load or use the checkpoint: {exc}")
