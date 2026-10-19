"""Explainable Tomato Leaf Disease Detection Web Application.

A full-featured diagnostic and model explainability suite using Grad-CAM,
multi-architecture comparison, confusion matrix analytics, and agronomic guidance.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import streamlit as st
import torch
from PIL import Image

from src.tomato_leaf_detection import PROJECT_NAME
from src.tomato_leaf_detection.config import DEFAULT_CHECKPOINT
from src.tomato_leaf_detection.disease_info import DISEASE_PROFILES, get_disease_profile
from src.tomato_leaf_detection.evaluate import (
    get_baseline_benchmark_data,
    plot_confusion_matrix,
)
from src.tomato_leaf_detection.explainability import explain_prediction
from src.tomato_leaf_detection.model import (
    SUPPORTED_ARCHITECTURES,
    benchmark_model,
    build_model,
    get_architecture_specs,
)

# Page configuration
st.set_page_config(
    page_title=f"{PROJECT_NAME} · 100% Milestone",
    page_icon="🍅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Design & CSS
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f7fbf7 0%, #f4f7f5 52%, #eef7f1 100%);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 1220px; padding-top: 2rem; padding-bottom: 3rem; }
    
    .hero {
        background: linear-gradient(120deg, #103324 0%, #174d34 60%, #246a44 100%);
        border-radius: 24px;
        padding: 2.2rem 2.8rem;
        color: white;
        box-shadow: 0 16px 36px rgba(16, 51, 36, 0.16);
        margin-bottom: 1.5rem;
        transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease;
    }
    .hero:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 42px rgba(16, 51, 36, 0.22);
    }
    .hero-kicker {
        color: #9de2b5;
        font-size: 0.8rem;
        font-weight: 750;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .hero h1 { color: #ffffff; font-size: 2.4rem; line-height: 1.15; margin: 0; font-weight: 800; }
    .hero p { color: #d3ecd9; font-size: 1.05rem; margin: 0.8rem 0 0; max-width: 820px; }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid #d7e6dc;
        border-radius: 16px;
        padding: 1rem 1.2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 0.5rem;
        transition: all 0.32s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(16, 51, 36, 0.1);
        border-color: #82b998;
    }
    .metric-label {
        color: #647a6c;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .metric-value {
        color: #123d28;
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 0.25rem;
    }
    
    .status-badge {
        display: inline-block;
        border-radius: 999px;
        padding: 0.3rem 0.8rem;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        transition: all 0.25s ease;
    }
    .badge-green { background: #d7f5e1; color: #116936; border: 1px solid #b2e6c3; }
    .badge-orange { background: #fef0db; color: #b25e07; border: 1px solid #f9dab3; }
    .badge-red { background: #fde8e8; color: #b91c1c; border: 1px solid #f8b4b4; }
    
    .section-title {
        color: #123d28;
        font-size: 1.35rem;
        font-weight: 800;
        margin: 1.2rem 0 0.4rem;
    }
    .section-subtitle {
        color: #647a6c;
        font-size: 0.95rem;
        margin-bottom: 1.2rem;
    }
    
    .treatment-card {
        background: #ffffff;
        border-radius: 16px;
        border: 1px solid #e1ede5;
        padding: 1.4rem;
        box-shadow: 0 6px 18px rgba(18, 61, 40, 0.05);
        margin-top: 1rem;
        transition: all 0.32s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .treatment-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(18, 61, 40, 0.1);
        border-color: #82b998;
    }
    .treatment-header {
        font-size: 1.15rem;
        font-weight: 750;
        color: #123d28;
        margin-bottom: 0.6rem;
    }

    /* Smooth Micro-interactions & Transitions */
    .stButton>button {
        transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        border: 1px solid #c9dec5 !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(18, 61, 40, 0.16) !important;
        border-color: #246a44 !important;
    }
    .stButton>button:active {
        transform: translateY(0px) !important;
    }

    div[data-baseweb="tab-list"] button {
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.1rem !important;
    }
    div[data-baseweb="tab-list"] button:hover {
        background: rgba(36, 106, 68, 0.08) !important;
    }

    img {
        border-radius: 14px;
        transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s ease !important;
    }
    img:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
    }

    div[data-testid="stProgress"] > div > div > div {
        transition: width 0.65s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    @keyframes smoothSlideUp {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .fade-in {
        animation: smoothSlideUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_checkpoint_cached(path_str: str) -> Tuple[Any, List[str], int, str]:
    """Load model checkpoint with cached resource management."""
    checkpoint = torch.load(path_str, map_location="cpu", weights_only=False)
    class_names = checkpoint["class_names"]
    image_size = checkpoint.get("image_size", 224)
    arch = checkpoint.get("architecture", "efficientnet_b0")

    model = build_model(class_names, pretrained=False, architecture=arch)
    model.load_state_dict(checkpoint["model_state"])
    model.eval()
    return model, class_names, image_size, arch


# Sidebar Navigation & Settings
with st.sidebar:
    st.markdown("### ⚙️ Diagnostic Settings")
    ckpt_input = st.text_input("Checkpoint Path", str(DEFAULT_CHECKPOINT))
    ckpt_path = Path(ckpt_input)

    st.divider()
    st.markdown("### 🎨 Explainability (Grad-CAM)")
    selected_cmap = st.selectbox(
        "Colormap",
        options=["jet", "turbo", "viridis", "plasma", "magma"],
        index=0,
        help="Color mapping applied to the Grad-CAM activation intensities.",
    )
    overlay_alpha = st.slider(
        "Heatmap Overlay Blend",
        min_value=0.1,
        max_value=0.9,
        value=0.5,
        step=0.05,
        help="Higher alpha intensifies the colored heatmap over the leaf texture.",
    )

    st.divider()
    st.markdown("### 📊 Project Presentation")
    pptx_file = Path("Explainable_Tomato_Leaf_Disease_Detection_Presentation.pptx")
    if pptx_file.is_file():
        with open(pptx_file, "rb") as f:
            st.download_button(
                label="📥 Download PowerPoint (.pptx)",
                data=f.read(),
                file_name="Explainable_Tomato_Leaf_Disease_Detection_Presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True,
            )

    st.divider()
    st.markdown("### ℹ️ System Information")
    st.caption("• **Milestone:** 100% Production Complete")
    st.caption("• **Backbone:** EfficientNet-B0")
    st.caption("• **Explainability:** Grad-CAM Class Activation Mapping")
    st.caption("• **Team:** Green tech AI/ML")


# Hero Banner
st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Team Green tech · Complete 100% Production Suite</div>
        <h1>Explainable Tomato Leaf<br> Disease Detection Using AI/ML</h1>
        <p>
            Accurate computer vision diagnostics powered by EfficientNet-B0 combined with
            Grad-CAM visual attention overlays to clearly explain <em>why</em> each disease is detected.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Top KPI Metric Cards
col1, col2, col3, col4 = st.columns(4)
metrics = [
    ("Milestone Progress", "100% Complete"),
    ("Primary Model", "EfficientNet-B0"),
    ("Disease Classes", "10 Monitored"),
    ("Explainability", "Grad-CAM Active"),
]
for col, (label, val) in zip([col1, col2, col3, col4], metrics):
    col.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{val}</div></div>',
        unsafe_allow_html=True,
    )

# Tabbed Interface
tab_diagnosis, tab_models, tab_evaluation, tab_guide = st.tabs(
    [
        "🔬 Leaf Health Diagnosis & Grad-CAM",
        "⚡ Multi-Model Architecture Comparison",
        "📊 Model Evaluation & Confusion Matrix",
        "📖 Plant Pathology Guide & Reference",
    ]
)

# Checkpoint verification
checkpoint_loaded = False
model, class_names, image_size, arch = None, [], 224, "efficientnet_b0"

if ckpt_path.is_file():
    try:
        model, class_names, image_size, arch = load_checkpoint_cached(str(ckpt_path))
        checkpoint_loaded = True
    except Exception as exc:
        st.error(f"Error loading checkpoint from `{ckpt_path}`: {exc}")
else:
    st.warning(
        f"⚠️ Checkpoint not found at `{ckpt_path}`. "
        f"Run training first or verify the path in the sidebar."
    )


# -----------------------------------------------------------------------------
# TAB 1: DIAGNOSIS & GRAD-CAM EXPLAINABILITY
# -----------------------------------------------------------------------------
with tab_diagnosis:
    st.markdown('<div class="section-title">Upload Leaf Image or Choose a Built-in Sample</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Select a pre-loaded botanical sample leaf or upload your own leaf photo.</div>',
        unsafe_allow_html=True,
    )

    # Built-in sample buttons
    sample_dir = Path("data/samples")
    sample_map = {
        "Early Blight": sample_dir / "early_blight_leaf.jpg",
        "Late Blight": sample_dir / "late_blight_leaf.jpg",
        "Bacterial Spot": sample_dir / "bacterial_spot_leaf.jpg",
        "Septoria Leaf Spot": sample_dir / "septoria_leaf_spot_leaf.jpg",
        "Yellow Leaf Curl": sample_dir / "yellow_leaf_curl_leaf.jpg",
        "Healthy Leaf": sample_dir / "healthy_leaf.jpg",
    }

    st.markdown("**Instant Demo Samples:**")
    sample_cols = st.columns(len(sample_map))
    selected_sample = None
    for col, (name, path) in zip(sample_cols, sample_map.items()):
        if path.is_file():
            if col.button(f"🍃 {name}", key=f"btn_{name}", use_container_width=True):
                st.session_state["active_sample"] = str(path)

    active_sample_path = st.session_state.get("active_sample", None)

    upload_col, info_col = st.columns([1.5, 1], gap="large")
    with upload_col:
        uploaded_file = st.file_uploader(
            "Or upload custom leaf image",
            type=["jpg", "jpeg", "png"],
            help="High-resolution RGB photos showing clear leaf surface symptoms give the best diagnostic accuracy.",
        )
    with info_col:
        st.markdown(
            f"""
            <div class="metric-card">
                <span class="status-badge {'badge-green' if checkpoint_loaded else 'badge-red'}">
                    {'● Model Ready & Loaded' if checkpoint_loaded else '○ Checkpoint Missing'}
                </span>
                <div style="margin-top: 0.8rem; color: #435b4e; font-size: 0.92rem; line-height: 1.55;">
                    <b>Explainable AI Active:</b> Every prediction is accompanied by a
                    <b>Grad-CAM attention heatmap</b> highlighting the specific lesion or chlorosis
                    patterns that caused the model's classification.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Determine input image
    image_to_process: Optional[Image.Image] = None
    image_source_name = ""

    if uploaded_file is not None:
        image_to_process = Image.open(uploaded_file)
        image_source_name = uploaded_file.name
    elif active_sample_path and Path(active_sample_path).is_file():
        image_to_process = Image.open(active_sample_path)
        image_source_name = Path(active_sample_path).name

    if image_to_process is not None:
        if not checkpoint_loaded:
            st.error("Cannot run inference: checkpoint is not loaded.")
        else:
            with st.spinner("Analyzing leaf pathology & generating Grad-CAM visual explanations..."):
                explanation = explain_prediction(
                    model=model,
                    image=image_to_process,
                    class_names=class_names,
                    image_size=image_size,
                    colormap_name=selected_cmap,
                    alpha=overlay_alpha,
                    top_k=3,
                )

            pred_label = explanation["predicted_label"]
            confidence = explanation["confidence"]
            profile = get_disease_profile(pred_label)

            st.divider()

            # Diagnostic summary banner
            sev_badge_class = (
                "badge-green" if profile.severity in ("None", "Low")
                else "badge-orange" if profile.severity in ("Moderate", "Moderate to High")
                else "badge-red"
            )

            st.markdown(
                f"""
                <div class="fade-in" style="background: white; border-radius: 18px; padding: 1.4rem 1.8rem; border-left: 8px solid {profile.color_code}; box-shadow: 0 8px 24px rgba(0,0,0,0.06); margin-bottom: 1.5rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div>
                            <span class="status-badge {sev_badge_class}">Severity: {profile.severity}</span>
                            <span style="margin-left: 0.6rem; color: #647a6c; font-size: 0.85rem;">Source: <code>{image_source_name}</code></span>
                            <h2 style="color: #123d28; margin: 0.4rem 0 0.1rem; font-size: 1.85rem;">{profile.display_name}</h2>
                            <div style="color: #4b6355; font-style: italic; font-size: 0.95rem;">{profile.scientific_name} ({profile.pathogen_type})</div>
                        </div>
                        <div style="text-align: right; margin-top: 0.5rem;">
                            <div style="font-size: 0.78rem; font-weight: 700; color: #647a6c; text-transform: uppercase;">Confidence Score</div>
                            <div style="font-size: 2.1rem; font-weight: 850; color: {profile.color_code};">{confidence:.1%}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # 4-View Visual Explanation Grid
            st.markdown("### 🖼️ Visual Explanation Inspection (Grad-CAM)")
            v1, v2, v3, v4 = st.columns(4)
            with v1:
                st.markdown("**1. Original Leaf Image**")
                st.image(image_to_process, use_container_width=True)
            with v2:
                st.markdown(f"**2. Grad-CAM Heatmap ({selected_cmap.title()})**")
                st.image(explanation["heatmap_image"], use_container_width=True)
            with v3:
                st.markdown("**3. Superimposed Blend**")
                st.image(explanation["blended_image"], use_container_width=True)
            with v4:
                st.markdown("**4. High-Attention Focus Area**")
                st.image(explanation["focus_image"], use_container_width=True)

            st.caption(
                f"Peak network spatial attention is centered at pixel coordinates "
                f"**{explanation['peak_attention_pixel']}**, with "
                f"**{explanation['high_activation_ratio']:.1%}** of the leaf area exhibiting strong disease activation."
            )

            st.divider()

            # Top Candidates & Treatment Guidelines
            prob_col, detail_col = st.columns([1, 1.4], gap="large")

            with prob_col:
                st.markdown("### 📊 Top Prediction Probabilities")
                for item in explanation["top_predictions"]:
                    c_name = item["class_name"].replace("Tomato___", "").replace("_", " ")
                    p_val = item["probability"]
                    st.write(f"**#{item['rank']} · {c_name}** ({p_val:.1%})")
                    st.progress(p_val)

            with detail_col:
                st.markdown("### 📋 Agronomic Diagnosis & Prescriptions")

                # Symptoms
                with st.expander("🔍 Key Visual Symptoms Identified", expanded=True):
                    for symptom in profile.symptoms:
                        st.markdown(f"• {symptom}")

                # Immediate actions
                with st.expander("🚨 Immediate Action Steps", expanded=True):
                    for action in profile.immediate_actions:
                        st.markdown(f"✓ **{action}**")

                # Organic and chemical options
                with st.expander("🌿 Organic & Cultural Remedies", expanded=False):
                    for org in profile.organic_treatment:
                        st.markdown(f"• {org}")

                with st.expander("🧪 Chemical & Conventional Controls", expanded=False):
                    for chem in profile.chemical_treatment:
                        st.markdown(f"• {chem}")

                with st.expander("🛡️ Long-term Field Prevention", expanded=False):
                    for prev in profile.prevention:
                        st.markdown(f"• {prev}")


# -----------------------------------------------------------------------------
# TAB 2: MULTI-MODEL ARCHITECTURE COMPARISON
# -----------------------------------------------------------------------------
with tab_models:
    st.markdown('<div class="section-title">Comparative Architecture Benchmarks</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Evaluating convolutional backbones on parameter efficiency, latency, and deployment suitability.</div>',
        unsafe_allow_html=True,
    )

    specs = get_architecture_specs()

    # Comparison summary cards
    arch_cols = st.columns(len(specs))
    for col, (key, info) in zip(arch_cols, specs.items()):
        is_active = key == arch
        with col:
            st.markdown(
                f"""
                <div class="metric-card" style="border: {'2px solid #2d7b51' if is_active else '1px solid #d7e6dc'};">
                    <span class="status-badge {'badge-green' if is_active else 'badge-orange'}">
                        {'Active Model' if is_active else info['family']}
                    </span>
                    <h3 style="color: #123d28; margin: 0.6rem 0 0.2rem; font-size: 1.25rem;">{info['name']}</h3>
                    <div style="font-size: 0.85rem; color: #53645a; margin-bottom: 0.6rem;">
                        <b>Params:</b> {info['parameters']}<br>
                        <b>Model Size:</b> {info['model_size_mb']} MB<br>
                        <b>Avg Latency:</b> {info['avg_latency_ms']} ms<br>
                        <b>Val Accuracy:</b> {info['val_accuracy']}
                    </div>
                    <div style="font-size: 0.78rem; color: #1a4d34; background: #eaf5ee; border-radius: 8px; padding: 0.4rem 0.6rem;">
                        <b>Best For:</b> {info['best_for']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### ⏱️ Run Live On-Device Latency Benchmark")
    st.write(
        "Benchmark live forward-pass latency and memory footprint directly on your machine:"
    )

    benchmark_arch = st.selectbox(
        "Select architecture to benchmark live",
        options=SUPPORTED_ARCHITECTURES,
        index=0,
    )

    if st.button("🚀 Run Live Benchmark", key="run_benchmark_btn"):
        with st.spinner(f"Benchmarking {benchmark_arch} across 20 iterations..."):
            dummy_classes = class_names if class_names else [f"class_{i}" for i in range(10)]
            test_model = build_model(dummy_classes, pretrained=False, architecture=benchmark_arch)
            bench_results = benchmark_model(test_model, input_size=224, runs=20)

            b1, b2, b3, b4 = st.columns(4)
            b1.metric("Mean Latency", f"{bench_results['mean_latency_ms']:.2f} ms")
            b2.metric("Min Latency", f"{bench_results['min_latency_ms']:.2f} ms")
            b3.metric("Total Parameters", f"{bench_results['total_parameters']:,}")
            b4.metric("Model Footprint", f"{bench_results['model_size_mb']:.1f} MB")

    st.divider()

    # Comparative table
    st.markdown("### 📋 Architecture Feature Comparison Table")
    df_compare = pd.DataFrame(
        [
            {
                "Architecture": info["name"],
                "Family": info["family"],
                "Parameters": info["parameters"],
                "Size (MB)": info["model_size_mb"],
                "Latency (ms)": info["avg_latency_ms"],
                "Validation Accuracy": info["val_accuracy"],
                "Target Deployment": info["best_for"],
            }
            for info in specs.values()
        ]
    )
    st.dataframe(df_compare, use_container_width=True, hide_index=True)


# -----------------------------------------------------------------------------
# TAB 3: MODEL EVALUATION & CONFUSION MATRIX
# -----------------------------------------------------------------------------
with tab_evaluation:
    st.markdown('<div class="section-title">Validation Evaluation & Error Dynamics</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Reproducible classification metrics, full 10-class confusion matrix, and error analysis.</div>',
        unsafe_allow_html=True,
    )

    bench_data = get_baseline_benchmark_data()

    # KPI summary
    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Overall Accuracy", f"{bench_data['accuracy']:.1%}")
    e2.metric("Macro Precision", f"{bench_data['macro_precision']:.1%}")
    e3.metric("Macro Recall", f"{bench_data['macro_recall']:.1%}")
    e4.metric("Macro F1-Score", f"{bench_data['macro_f1']:.1%}")

    st.divider()

    # Confusion Matrix Visualization
    matrix_col, error_col = st.columns([1.3, 1], gap="large")

    with matrix_col:
        st.markdown("### 🔲 10-Class Confusion Matrix")
        normalize_cm = st.checkbox("Normalize Matrix Rows (Percentages)", value=True)
        cm_np = np.array(bench_data["confusion_matrix"])

        fig = plot_confusion_matrix(
            cm=cm_np,
            class_names=bench_data["class_names"],
            normalize=normalize_cm,
            title="Normalized Confusion Matrix" if normalize_cm else "Raw Confusion Matrix",
        )
        st.pyplot(fig)

    with error_col:
        st.markdown("### ⚠️ Top Confused Class Pairings")
        st.write("Pathology error dynamics identified during validation evaluation:")

        for conf in bench_data["top_confusions"]:
            t_name = conf["true_class"].replace("Tomato___", "").replace("_", " ")
            p_name = conf["predicted_class"].replace("Tomato___", "").replace("_", " ")
            st.markdown(
                f"""
                <div style="background: white; border-radius: 12px; padding: 0.8rem 1rem; border-left: 4px solid #e74c3c; margin-bottom: 0.6rem; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
                    <div style="font-weight: 750; color: #123d28; font-size: 0.95rem;">{t_name} ➔ {p_name}</div>
                    <div style="font-size: 0.82rem; color: #647a6c; margin-top: 0.2rem;">
                        <b>{conf['error_count']} misclassified samples</b> ({conf['error_rate_in_true']:.1%} of true class)
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("### 💡 Key Agronomic Insights")
        for insight in bench_data["key_insights"]:
            st.markdown(f"• {insight}")


# -----------------------------------------------------------------------------
# TAB 4: PLANT PATHOLOGY GUIDE & REFERENCE
# -----------------------------------------------------------------------------
with tab_guide:
    st.markdown('<div class="section-title">Botanical Pathology Field Encyclopedia</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Reference guide for all 10 monitored tomato foliar conditions.</div>',
        unsafe_allow_html=True,
    )

    for profile in DISEASE_PROFILES.values():
        with st.expander(f"🍅 {profile.display_name} ({profile.scientific_name})"):
            c_a, c_b = st.columns([1, 1])
            with c_a:
                st.markdown(f"**Pathogen Type:** {profile.pathogen_type}")
                st.markdown(f"**Severity Level:** {profile.severity}")
                st.markdown("**Visual Symptoms:**")
                for s in profile.symptoms:
                    st.markdown(f"- {s}")
                st.markdown("**Immediate Actions:**")
                for a in profile.immediate_actions:
                    st.markdown(f"- {a}")
            with c_b:
                st.markdown("**Organic Management:**")
                for o in profile.organic_treatment:
                    st.markdown(f"- {o}")
                st.markdown("**Chemical Controls:**")
                for c in profile.chemical_treatment:
                    st.markdown(f"- {c}")
                st.markdown("**Long-term Prevention:**")
                for p in profile.prevention:
                    st.markdown(f"- {p}")

    st.divider()
    st.markdown("### 📜 Project Limitations & Ethical Deployment Principles")
    st.markdown(
        """
        1. **Foliar Exclusivity:** The baseline model is trained specifically on leaf surface photographs. Symptoms presenting primarily on roots, stems, or internal fruit flesh require complementary diagnostic protocols.
        2. **Dual & Co-infections:** Field plants subjected to both fungal and viral co-infections may exhibit combined symptom morphology. Grad-CAM visual attention overlays should always be cross-referenced with human agricultural scouting.
        3. **Lighting & Optical Resolution:** Severe shadows, severe blur, or low illumination can diminish feature extraction fidelity. Always capture clear, well-lit photographs with the leaf blade occupying the majority of the frame.
        """
    )
