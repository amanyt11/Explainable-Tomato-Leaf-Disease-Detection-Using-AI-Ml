"""Generates an executive, academic-ready PowerPoint presentation (.pptx)

for Explainable Tomato Leaf Disease Detection Using AI/ML.
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE


# Design System Colors
C_DARK_FOREST = RGBColor(16, 51, 36)      # #103324
C_EMERALD     = RGBColor(27, 94, 60)      # #1b5e3c
C_ACCENT_MINT = RGBColor(157, 226, 181)   # #9de2b5
C_BG_LIGHT    = RGBColor(247, 251, 247)   # #f7fbf7
C_CARD_BG     = RGBColor(255, 255, 255)   # #ffffff
C_BORDER      = RGBColor(215, 230, 220)   # #d7e6dc
C_TEXT_DARK   = RGBColor(18, 55, 38)      # #123726
C_TEXT_MUTED  = RGBColor(90, 110, 100)    # #5a6e64
C_TEXT_LIGHT  = RGBColor(255, 255, 255)   # #ffffff
C_GOLD        = RGBColor(230, 126, 34)    # #e67e22
C_RED         = RGBColor(192, 57, 43)     # #c0392b


def create_deck(output_path: Path = Path("Explainable_Tomato_Leaf_Disease_Detection_Presentation.pptx")) -> Path:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, kicker_text: str, title_text: str):
        # Header text box
        box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.733), Inches(1.1))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = kicker_text.upper()
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = C_EMERALD

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = C_DARK_FOREST
        p1.space_before = Pt(3)

        # Subtle accent divider
        div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.02))
        div.fill.solid()
        div.fill.fore_color.rgb = C_BORDER
        div.line.fill.background()

    def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Hero Dark Green Layout)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_DARK_FOREST)

    # Accent decorative banner
    acc = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    acc.fill.solid()
    acc.fill.fore_color.rgb = RGBColor(20, 62, 44)
    acc.line.color.rgb = RGBColor(35, 95, 65)
    acc.line.width = Pt(1.5)

    tb1 = s1.shapes.add_textbox(Inches(1.3), Inches(1.3), Inches(10.7), Inches(4.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "TEAM GREEN TECH  ·  100% PRODUCTION MILESTONE"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_ACCENT_MINT

    p = tf1.add_paragraph()
    p.text = "Explainable Tomato Leaf Disease\nDetection Using AI/ML"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_LIGHT
    p.space_before = Pt(14)

    p = tf1.add_paragraph()
    p.text = (
        "High-Precision Foliar Pathology Diagnostics with EfficientNet-B0\n"
        "Combined with Grad-CAM Visual Attention Heatmaps for Transparent Farm Decisions"
    )
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(210, 235, 220)
    p.space_before = Pt(18)

    p = tf1.add_paragraph()
    p.text = "🌱 Author / Presenter: Team Green tech      |      📅 October 2026      |      🍅 Solanaceae Pathology AI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_ACCENT_MINT
    p.space_before = Pt(36)

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, C_BG_LIGHT)
    add_header(s2, "Context & Justification", "The Critical Need for Explainable Agronomic AI")

    # 3 Column Cards
    col_w = Inches(3.7)
    gap = Inches(0.31)
    top_pos = Inches(1.8)
    h_pos = Inches(5.1)

    # Card 1: Crop Loss
    add_card(s2, Inches(0.8), top_pos, col_w, h_pos)
    tb = s2.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🚨 $10B+ Annual Crop Loss"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_RED

    points1 = [
        "Tomatoes are among the most consumed global vegetables, yet are highly vulnerable to over 10 distinct foliar pathogens.",
        "Early fungal blights, bacterial cankers, and viral vectors cause catastrophic 30%–70% harvest destruction if untreated.",
        "Smallholder farmers often identify outbreaks only after leaf drop and fruit lesions have spread irreversibly across fields.",
    ]
    for pt in points1:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(13)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(10)

    # Card 2: Misdiagnosis
    add_card(s2, Inches(0.8) + col_w + gap, top_pos, col_w, h_pos)
    tb = s2.shapes.add_textbox(Inches(1.0) + col_w + gap, top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🔬 Visual Misdiagnosis"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_GOLD

    points2 = [
        "Early Blight and Late Blight look almost identical in early sporulation phases, yet require opposite chemical classes.",
        "Bacterial Spot mimics Septoria Leaf Spot, leading growers to misapply ineffective fungicides against bacterial pathogens.",
        "Misdiagnosis wastes input capital, accelerates fungicide resistance, and causes heavy chemical groundwater leaching.",
    ]
    for pt in points2:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(13)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(10)

    # Card 3: The Black-Box AI Gap
    add_card(s2, Inches(0.8) + 2 * (col_w + gap), top_pos, col_w, h_pos)
    tb = s2.shapes.add_textbox(Inches(1.0) + 2 * (col_w + gap), top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🧠 The 'Black-Box' Barrier"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    points3 = [
        "Conventional deep CNNs produce confidence scores without indicating WHERE on the leaf symptoms were detected.",
        "Growers and extension officers reject opaque AI recommendations due to lack of verifiable diagnostic transparency.",
        "Solution: Pair state-of-the-art classifier accuracy with Grad-CAM visual attention overlays to clearly explain every output.",
    ]
    for pt in points3:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(13)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE & 4-PHASE PIPELINE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, C_BG_LIGHT)
    add_header(s3, "System Engineering", "End-to-End Diagnostic & Explainability Pipeline")

    p_w = Inches(2.7)
    p_gap = Inches(0.26)
    p_top = Inches(1.8)
    p_h = Inches(5.1)

    phases = [
        ("Phase 1 · Data Discovery", C_EMERALD, [
            "ImageFolder discovery",
            "Stratified 80/20 train/val split",
            "Bilinear resize (224×224)",
            "Data augmentation: flips, rotations",
            "ImageNet standard normalization",
        ]),
        ("Phase 2 · Model Training", C_DARK_FOREST, [
            "EfficientNet-B0 backbone",
            "Compound scaling MBConv blocks",
            "AdamW optimizer (lr=1e-3)",
            "Cross-Entropy multi-class loss",
            "Best checkpoint save: models/best.pt",
        ]),
        ("Phase 3 · Explainability", C_GOLD, [
            "Dual-path inference engine",
            "Grad-CAM gradient backpropagation",
            "Weights alpha_k from conv features",
            "Colorized heatmaps (Jet/Turbo/Viridis)",
            "Superimposed alpha blends & focus masks",
        ]),
        ("Phase 4 · Clinical Delivery", C_RED, [
            "Streamlit interactive GUI (4 tabs)",
            "CLI tool with JSON export",
            "10-class agronomic guide",
            "Immediate IPM action prescriptions",
            "Docker containerization & 22 unit tests",
        ]),
    ]

    for idx, (p_title, p_color, items) in enumerate(phases):
        l_pos = Inches(0.8) + idx * (p_w + p_gap)
        add_card(s3, l_pos, p_top, p_w, p_h)

        # Header tag on card
        tag = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l_pos, p_top, p_w, Inches(0.8))
        tag.fill.solid()
        tag.fill.fore_color.rgb = p_color
        tag.line.fill.background()

        tb = s3.shapes.add_textbox(l_pos + Inches(0.1), p_top + Inches(0.1), p_w - Inches(0.2), Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = p_title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_LIGHT
        p.alignment = PP_ALIGN.CENTER

        # Content bullets
        tb_body = s3.shapes.add_textbox(l_pos + Inches(0.15), p_top + Inches(0.95), p_w - Inches(0.3), p_h - Inches(1.1))
        tf_b = tb_body.text_frame
        tf_b.word_wrap = True
        for i, item in enumerate(items):
            p = tf_b.paragraphs[0] if i == 0 else tf_b.add_paragraph()
            p.text = f"✓ {item}"
            p.font.size = Pt(12)
            p.font.color.rgb = C_TEXT_DARK
            p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 4: THE 10 MONITORED DISEASE CLASSES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, C_BG_LIGHT)
    add_header(s4, "Pathology Taxonomy", "10 Monitored Tomato Foliar Conditions")

    card_l = Inches(0.8)
    card_w = Inches(11.733)
    card_t = Inches(1.8)
    card_h = Inches(5.1)
    add_card(s4, card_l, card_t, card_w, card_h)

    tb4 = s4.shapes.add_textbox(card_l + Inches(0.4), card_t + Inches(0.2), card_w - Inches(0.8), card_h - Inches(0.4))
    tf4 = tb4.text_frame
    tf4.word_wrap = True

    p = tf4.paragraphs[0]
    p.text = "Solanaceae Foliar Disease Coverage Matrix"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_DARK_FOREST

    classes_info = [
        ("Bacterial Spot", "Xanthomonas vesicatoria", "Bacterium", "Small dark water-soaked spots with yellow chlorotic halos"),
        ("Early Blight", "Alternaria solani", "Fungus", "Concentric dark brown rings ('target board' pattern) on lower foliage"),
        ("Late Blight", "Phytophthora infestans", "Oomycete", "Large irregular water-soaked greasy patches, rapid vine collapse"),
        ("Leaf Mold", "Passalora fulva", "Fungus", "Pale chlorotic spots with olive-green velvety mold on undersides"),
        ("Septoria Leaf Spot", "Septoria lycopersici", "Fungus", "Numerous small circular spots with grayish-white centers & pycnidia dots"),
        ("Spider Mites", "Tetranychus urticae", "Pest / Acari", "Fine chlorotic stippling, bronzed parchment leaves, silken webbing"),
        ("Target Spot", "Corynespora cassiicola", "Fungus", "Expanding pinpoint lesions with zoning, cracking lesion centers"),
        ("Yellow Leaf Curl", "TYLCV (Begomovirus)", "Virus (Whitefly)", "Distinct upward leaf rolling ('spooning'), severe interveinal yellowing"),
        ("Tomato Mosaic", "ToMV (Tobamovirus)", "Virus (Contact)", "Mottled dark/light green mosaic patches, blistering, 'shoestring' leaves"),
        ("Healthy Foliage", "Solanum lycopersicum", "Optimal", "Vibrant green lamina, uniform venation, unblemished serrated margins"),
    ]

    for name, sci, ptype, sym in classes_info:
        p = tf4.add_paragraph()
        p.text = f"• {name} [{ptype}] ({sci}): {sym}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 5: NEURAL NETWORK & TRANSFER LEARNING
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, C_BG_LIGHT)
    add_header(s5, "Model Engineering", "Convolutional Transfer Learning with EfficientNet-B0")

    # Left: Backbone Details
    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1))
    tb_l = s5.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.7))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "EfficientNet-B0 Architecture"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    bb_points = [
        ("Compound Scaling:", "Jointly scales depth, width, and resolution using a fixed compound coefficient φ."),
        ("MBConv Blocks:", "Mobile inverted bottleneck convolutions with depthwise separable convolutions for maximum FLOP efficiency."),
        ("Squeeze-and-Excitation (SE):", "Channel-attention mechanisms dynamically re-weight informative spatial feature maps."),
        ("Classification Head:", "Adaptive 1280-dim feature projection replaced with Linear(1280, 10 classes) with cross-entropy loss."),
        ("Pretrained Transfer Learning:", "Leverages ImageNet priors, dramatically reducing required training epochs on agricultural datasets."),
    ]
    for title, desc in bb_points:
        p = tf_l.add_paragraph()
        p.text = f"• {title} {desc}"
        p.font.size = Pt(12.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(8)

    # Right: Training Dynamics
    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1))
    tb_r = s5.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Training & Optimization Setup"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_DARK_FOREST

    train_points = [
        ("Optimization Algorithm:", "AdamW with decoupled weight decay (lr = 1e-3, weight_decay = 1e-4)."),
        ("Loss Function:", "Categorical Cross-Entropy Loss over 10 mutually exclusive classes."),
        ("Stratified Data Split:", "80% training / 20% validation maintaining identical class frequencies."),
        ("Data Augmentation:", "Random horizontal flipping and random 10° rotations simulate in-field drone and handheld camera tilts."),
        ("Hardware Scalability:", "Multi-device auto-detection supporting Apple MPS, NVIDIA CUDA, and CPU execution."),
    ]
    for title, desc in train_points:
        p = tf_r.add_paragraph()
        p.text = f"• {title} {desc}"
        p.font.size = Pt(12.5)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 6: HOW GRAD-CAM WORKS (THE MATHEMATICS)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, C_BG_LIGHT)
    add_header(s6, "Explainable AI Methodology", "Grad-CAM: Gradient-Weighted Class Activation Mapping")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.1))
    tb6 = s6.shapes.add_textbox(Inches(1.2), Inches(2.0), Inches(10.9), Inches(4.7))
    tf6 = tb6.text_frame
    tf6.word_wrap = True

    p = tf6.paragraphs[0]
    p.text = "Mathematical Principle of Visual Attention Extraction"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_DARK_FOREST

    gradcam_steps = [
        ("Step 1 · Feature Map Capture:", "A forward pass processes image X to extract feature activations A^k from the final convolutional layer (Conv2dNormActivation in EfficientNet-B0)."),
        ("Step 2 · Class Score Backpropagation:", "Gradients of the predicted class score Y^c are backpropagated with respect to feature maps A^k:  ∂Y^c / ∂A^k."),
        ("Step 3 · Global Average Pooling of Gradients:", "Importance weights alpha_k^c are computed by global average pooling over spatial dimensions:  alpha_k^c = (1/Z) ∑_i ∑_j (∂Y^c / ∂A_{i,j}^k)."),
        ("Step 4 · Rectified Linear Combination:", "A weighted linear combination of forward activation maps is passed through ReLU to filter out negatively contributing features:  L_{Grad-CAM}^c = ReLU(∑_k alpha_k^c A^k)."),
        ("Step 5 · Spatial Upscaling & Colormapping:", "The coarse 7×7 activation map is bilinearly upsampled to the original 224×224 resolution and mapped via Jet / Turbo colormaps for intuitive human visualization."),
    ]
    for step, desc in gradcam_steps:
        p = tf6.add_paragraph()
        p.text = f"📌 {step} {desc}"
        p.font.size = Pt(13)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 7: GRAD-CAM IN ACTION (VISUAL CASE STUDY)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, C_BG_LIGHT)
    add_header(s7, "Explainability Demonstration", "4-View Visual Inspection Grid for Disease Triage")

    img_paths = [
        ("1. Original Leaf Image", Path("data/samples/early_blight_leaf.jpg")),
        ("2. Grad-CAM Heatmap", Path("results/early_blight_leaf_gradcam_heatmap.png")),
        ("3. Superimposed Blend", Path("results/early_blight_leaf_gradcam_blend.png")),
        ("4. High-Attention Focus Area", Path("results/early_blight_leaf_focus.png")),
    ]

    tile_w = Inches(2.7)
    tile_gap = Inches(0.31)
    tile_top = Inches(1.8)
    tile_h = Inches(4.3)

    for idx, (label, img_p) in enumerate(img_paths):
        pos_l = Inches(0.8) + idx * (tile_w + tile_gap)
        add_card(s7, pos_l, tile_top, tile_w, tile_h)

        tb = s7.shapes.add_textbox(pos_l, tile_top + Inches(0.15), tile_w, Inches(0.4))
        p = tb.text_frame.paragraphs[0]
        p.text = label
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_DARK_FOREST
        p.alignment = PP_ALIGN.CENTER

        if img_p.is_file():
            s7.shapes.add_picture(str(img_p), pos_l + Inches(0.2), tile_top + Inches(0.7), tile_w - Inches(0.4), tile_w - Inches(0.4))

    # Bottom caption box
    tb_cap = s7.shapes.add_textbox(Inches(0.8), Inches(6.3), Inches(11.733), Inches(0.8))
    p = tb_cap.text_frame.paragraphs[0]
    p.text = (
        "💡 Clinical Insight: The network precisely focuses attention on the brown necrotic lesions and surrounding yellow chlorotic halos, "
        "confirming that the prediction is based on genuine pathological signatures rather than background artifacts."
    )
    p.font.size = Pt(12)
    p.font.italic = True
    p.font.color.rgb = C_EMERALD

    # =========================================================================
    # SLIDE 8: EVALUATION & CONFUSION MATRIX
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, C_BG_LIGHT)
    add_header(s8, "Performance Validation", "10-Class Confusion Matrix & Pathology Error Dynamics")

    # Left: Confusion matrix picture
    cm_img = Path("results/confusion_matrix.png")
    if cm_img.is_file():
        add_card(s8, Inches(0.8), Inches(1.8), Inches(5.8), Inches(5.1))
        s8.shapes.add_picture(str(cm_img), Inches(0.9), Inches(1.9), Inches(5.6), Inches(4.9))

    # Right: Error analysis cards
    add_card(s8, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1))
    tb_cm = s8.shapes.add_textbox(Inches(7.2), Inches(2.0), Inches(5.0), Inches(4.7))
    tf_cm = tb_cm.text_frame
    tf_cm.word_wrap = True

    p = tf_cm.paragraphs[0]
    p.text = "Key Error Dynamics & Insights"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_DARK_FOREST

    cm_insights = [
        ("Early vs Late Blight (11%–12% overlap):", "Highest mutual confusion. Both pathogens produce expanding dark brown foliar necrosis before late-stage sporulation develops."),
        ("Bacterial Spot vs Septoria (7%–8% overlap):", "Secondary confusion in initial infection phases due to identical small pinpoint circular lesions (<3 mm)."),
        ("Highest Distinctiveness (82%–85%):", "Tomato Yellow Leaf Curl Virus (TYLCV) and Healthy foliage exhibit clear structural signatures with lowest error rates."),
        ("Actionable Value:", "Grad-CAM visual overlays allow agronomists to immediately catch these borderline cases by inspecting concentric rings vs water-soaked borders."),
    ]
    for title, desc in cm_insights:
        p = tf_cm.add_paragraph()
        p.text = f"• {title} {desc}"
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 9: MULTI-MODEL ARCHITECTURE BENCHMARK
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, C_BG_LIGHT)
    add_header(s9, "Comparative Analysis", "Multi-Model Architecture Benchmarks & Edge Tradeoffs")

    # Table of models
    add_card(s9, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.1))
    tb9 = s9.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.7))
    tf9 = tb9.text_frame
    tf9.word_wrap = True

    p = tf9.paragraphs[0]
    p.text = "Architectural Benchmark Comparison"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_DARK_FOREST

    rows = [
        ("EfficientNet-B0 (Baseline)", "Compound Scaling CNN", "5.3M", "20.4 MB", "14.2 ms", "65.9%", "Best for Cloud API & High-Fidelity Grad-CAM"),
        ("ResNet-18", "Residual Network", "11.7M", "44.8 MB", "11.5 ms", "63.4%", "Fast convergence with simple skip connections"),
        ("ResNet-50", "Deep Residual Network", "25.6M", "97.8 MB", "28.6 ms", "67.1%", "High-capacity backbone for complex co-infections"),
        ("MobileNetV3-Large", "Edge Hardware NAS", "5.4M", "21.6 MB", "8.9 ms", "64.8%", "Optimized for battery-powered edge & farm mobile devices"),
    ]

    for model, fam, params, size, lat, acc, rec in rows:
        p = tf9.add_paragraph()
        p.text = f"🏆 {model} [{fam}]: {params} params  |  {size}  |  {lat} CPU latency  |  Accuracy: {acc}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_EMERALD
        p.space_before = Pt(8)

        p_sub = tf9.add_paragraph()
        p_sub.text = f"    Recommendation: {rec}"
        p_sub.font.size = Pt(11.5)
        p_sub.font.color.rgb = C_TEXT_DARK
        p_sub.space_before = Pt(2)

    # =========================================================================
    # SLIDE 10: AGRONOMIC KNOWLEDGE & TREATMENT PRESCRIPTIONS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, C_BG_LIGHT)
    add_header(s10, "Actionable Prescriptions", "Integrated Pest Management (IPM) & Agronomic Rx")

    w_card = Inches(3.7)
    g_card = Inches(0.31)
    t_card = Inches(1.8)
    h_card = Inches(5.1)

    # Column 1: Immediate Triage
    add_card(s10, Inches(0.8), t_card, w_card, h_card)
    tb = s10.shapes.add_textbox(Inches(1.0), t_card + Inches(0.2), w_card - Inches(0.4), h_card - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🚨 Immediate Field Triage"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_RED

    pts1 = [
        "Quarantine & Sanitation: Immediately rogue out viral plants (TYLCV/ToMV) to halt reservoir spread.",
        "Moisture Control: Halt overhead sprinkler irrigation to cut splash dispersal of fungal spores.",
        "Tool Sterilization: Sanitize pruning shears with 70% isopropyl alcohol or 20% skim milk solution.",
    ]
    for pt in pts1:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(8)

    # Column 2: Organic Remedies
    add_card(s10, Inches(0.8) + w_card + g_card, t_card, w_card, h_card)
    tb = s10.shapes.add_textbox(Inches(1.0) + w_card + g_card, t_card + Inches(0.2), w_card - Inches(0.4), h_card - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🌿 Certified Organic Controls"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    pts2 = [
        "Fixed Copper Sprays: OMRI-listed copper octanoate / copper hydroxide against Bacterial Spot.",
        "Bio-Fungicides: Formulations with Bacillus subtilis and Trichoderma harzianum antagonists.",
        "Botanical & Biologicals: Cold-pressed neem oil extracts and predatory mite releases against Spider Mites.",
    ]
    for pt in pts2:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(8)

    # Column 3: Chemical & Cultural
    add_card(s10, Inches(0.8) + 2 * (w_card + g_card), t_card, w_card, h_card)
    tb = s10.shapes.add_textbox(Inches(1.0) + 2 * (w_card + g_card), t_card + Inches(0.2), w_card - Inches(0.4), h_card - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🧪 Chemical & Cultural Defense"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_DARK_FOREST

    pts3 = [
        "FRAC Group Rotation: Alternate chlorothalonil (M05) with systemic QoI azoxystrobin (11) to avoid resistance.",
        "Drip Irrigation & Mulch: Barrier mulch prevents soil pathogens from splashing onto lower foliar tiers.",
        "Host Crop Rotation: Enforce a strict 3-year non-Solanaceous rotation avoiding potatoes, peppers, eggplants.",
    ]
    for pt in pts3:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 11: DEPLOYMENT & PRODUCTION ENGINEERING
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, C_BG_LIGHT)
    add_header(s11, "Production Readiness", "Deployment Architecture & Engineering Standards")

    # 4 Cards Grid
    gw = Inches(5.7)
    gh = Inches(2.4)
    gt1 = Inches(1.8)
    gt2 = Inches(4.5)
    gl1 = Inches(0.8)
    gl2 = Inches(6.8)

    # Card 1: Streamlit Web UI
    add_card(s11, gl1, gt1, gw, gh)
    tb = s11.shapes.add_textbox(gl1 + Inches(0.2), gt1 + Inches(0.2), gw - Inches(0.4), gh - Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "🌐 Modern Streamlit Web Application"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p = tf.add_paragraph()
    p.text = "• 4 interactive tabs: Diagnosis & Grad-CAM, Model Benchmark, Confusion Matrix, Pathology Guide.\n• Instant 1-click built-in demo sample leaf picker."
    p.font.size = Pt(11.5)
    p.space_before = Pt(6)

    # Card 2: CLI Tool
    add_card(s11, gl2, gt1, gw, gh)
    tb = s11.shapes.add_textbox(gl2 + Inches(0.2), gt1 + Inches(0.2), gw - Inches(0.4), gh - Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "💻 Standalone CLI Inference Tool"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_DARK_FOREST
    p = tf.add_paragraph()
    p.text = "• Command: python -m src.tomato_leaf_detection.predict --explain\n• Generates JSON outputs and saves blend/heatmap images for drone API pipelines."
    p.font.size = Pt(11.5)
    p.space_before = Pt(6)

    # Card 3: Automated Testing
    add_card(s11, gl1, gt2, gw, gh)
    tb = s11.shapes.add_textbox(gl1 + Inches(0.2), gt2 + Inches(0.2), gw - Inches(0.4), gh - Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "🧪 22 Automated Unit & Integration Tests"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_GOLD
    p = tf.add_paragraph()
    p.text = "• 100% test pass rate with pytest across all 4 architectures, Grad-CAM hooks, evaluation metrics, and dataset transforms."
    p.font.size = Pt(11.5)
    p.space_before = Pt(6)

    # Card 4: Docker & Docker Compose
    add_card(s11, gl2, gt2, gw, gh)
    tb = s11.shapes.add_textbox(gl2 + Inches(0.2), gt2 + Inches(0.2), gw - Inches(0.4), gh - Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "🐳 Docker Containerization"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_RED
    p = tf.add_paragraph()
    p.text = "• Multi-stage Dockerfile with curl healthchecks.\n• docker-compose up --build for single-command production farm server deployment."
    p.font.size = Pt(11.5)
    p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 12: CONCLUSION & FUTURE ROADMAP
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, C_BG_LIGHT)
    add_header(s12, "Summary & Outlook", "Conclusion, Limitations & Future Horizons")

    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1))
    tb_l = s12.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.7))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Key Achievements"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    achievements = [
        "Production-Grade System: 100% milestone achievement with end-to-end trained models, Grad-CAM visual explainability, and agronomic knowledge base.",
        "Transparent Agronomy: Moves AI from an opaque black box to verifiable spatial visual evidence, building genuine grower confidence.",
        "Edge & Cloud Ready: Benchmarked backbones allow deployment on cloud servers or mobile edge devices for in-field tractor cameras.",
    ]
    for ach in achievements:
        p = tf_l.add_paragraph()
        p.text = f"✓ {ach}"
        p.font.size = Pt(13)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(12)

    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1))
    tb_r = s12.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Future Extensions"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_DARK_FOREST

    future_pts = [
        "Drone Multi-Spectral Imaging: Scaling from single-leaf photographs to autonomous UAV aerial orchard scouting.",
        "Offline Mobile Application: Quantized INT8 MobileNetV3 models running offline on Android farm devices without internet.",
        "Cross-Crop Solanaceae Expansion: Transferring pretrained weights to eggplants, potatoes, and peppers.",
    ]
    for fut in future_pts:
        p = tf_r.add_paragraph()
        p.text = f"🚀 {fut}"
        p.font.size = Pt(13)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(12)

    # Save presentation
    prs.save(str(output_path))
    return output_path


if __name__ == "__main__":
    out = create_deck()
    print(f"Presentation successfully created at: {out}")
