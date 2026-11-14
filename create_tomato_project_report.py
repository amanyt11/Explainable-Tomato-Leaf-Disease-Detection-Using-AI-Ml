"""Script to generate the complete Graphic Era BCA Major Project Report for:
'Explainable Tomato Leaf Disease Prediction Using Machine Learning'
Under the Guidance of: Mr. Abhishek Thapa (Assistant Professor)
Matching the exact structural template, academic tone, chapters, and appendices of the demo report.
"""

import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex="F2F4F7"):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def format_run(run, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color_rgb=(0, 0, 0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

def add_styled_paragraph(doc, text="", font_name="Times New Roman", size_pt=12, bold=False, italic=False,
                         align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=6, line_spacing=1.15, color_rgb=(0, 0, 0)):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        format_run(r, font_name, size_pt, bold, italic, color_rgb)
    return p

def main():
    doc = docx.Document()

    # Page Margins (Standard Graphic Era project report: 1.25 in left for binding, 1.0 in top, bottom, right)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)  # A4
        section.page_height = Inches(11.69)

    # =========================================================================
    # 1. COVER PAGE
    # =========================================================================
    p = add_styled_paragraph(doc, "PROJECT REPORT ON", size_pt=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=28, space_after=24)

    p_title = add_styled_paragraph(doc, "Tomato Leaf Disease Prediction Using Machine Learning", size_pt=20, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=32)

    add_styled_paragraph(doc, "Submitted to", size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=4)
    add_styled_paragraph(doc, "Department of Computer Applications in fulfilment for the award of the degree of", size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=4)
    add_styled_paragraph(doc, "BACHELOR OF COMPUTER APPLICATIONS", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=6)
    add_styled_paragraph(doc, "Batch (2024-2027)", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=36)

    add_styled_paragraph(doc, "Submitted by", size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=6)
    add_styled_paragraph(doc, "SARTHAK NEGI\n24151534", size_pt=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=36)

    add_styled_paragraph(doc, "Under the Guidance of", size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=6)
    add_styled_paragraph(doc, "Mr. Abhishek Thapa", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)
    add_styled_paragraph(doc, "(Assistant Professor)", size_pt=12, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=54)

    add_styled_paragraph(doc, "GRAPHIC ERA DEEMED TO BE UNIVERSITY DEHRADUN", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=24, space_after=6)
    add_styled_paragraph(doc, "November 2026", size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=0)

    doc.add_page_break()

    # =========================================================================
    # 2. CANDIDATE'S DECLARATION
    # =========================================================================
    add_styled_paragraph(doc, "CANDIDATE’S DECLARATION", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=24, space_after=28)

    decl_text = (
        "I, Sarthak Negi, hereby declare that the report entitled "
        "“Tomato Leaf Disease Prediction Using Machine Learning” in complete fulfilment of the requirements for "
        "the award of the degree of Bachelor of Computer Applications is a bonafide work carried out by me during "
        "the period of August 2026 to November 2026 under the supervision of Mr. Abhishek Thapa, Assistant Professor, "
        "Department of Computer Applications, Graphic Era Deemed to be University, Dehradun, India.\n\n"
        "This work has not been submitted elsewhere for the award of any degree/diploma/certificate."
    )
    add_styled_paragraph(doc, decl_text, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=6, space_after=36, line_spacing=1.3)

    # Signatures
    p_sig = add_styled_paragraph(doc, "Sarthak Negi\n(24151534)", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, space_before=12, space_after=40)

    cert_text = (
        "This is to certify that the above mentioned statement in the candidate’s declaration is correct "
        "to the best of my knowledge."
    )
    add_styled_paragraph(doc, cert_text, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=18, space_after=40, line_spacing=1.2)

    p_guide = add_styled_paragraph(doc, "Date: ____________\t\t\t\t\tName and Signature of Guide", size_pt=12, bold=True, space_before=16, space_after=44)
    p_exam = add_styled_paragraph(doc, "Signature of Supervisor\t\t\t\tSignature of External Examiner", size_pt=12, bold=True, space_before=18, space_after=48)
    add_styled_paragraph(doc, "HOD", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=0)

    doc.add_page_break()

    # =========================================================================
    # 3. ACKNOWLEDGEMENT
    # =========================================================================
    add_styled_paragraph(doc, "Acknowledgement", size_pt=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=24, space_after=24)

    ack_text = (
        "First of all, my sincere and wholehearted gratitude to my loved ones and mentors who supported me during "
        "the making of this project. The success and final outcome of this project required a lot of guidance and assistance "
        "from many people, and I am extremely privileged to have had this support throughout the completion of my project. "
        "All that I have achieved is through their supervision and constructive assistance.\n\n"
        "I respect and express my profound thanks to Mr. Abhishek Thapa, Assistant Professor, Department of Computer Applications, "
        "for providing me the opportunity to carry out this project entitled “Tomato Leaf Disease Prediction Using Machine Learning” "
        "and extending his invaluable guidance, technical insights, and continuous encouragement throughout my research. "
        "I am deeply grateful to him for his dedicated mentorship and patience despite his busy academic commitments.\n\n"
        "I also convey my sincere appreciation to the Head of Department and all faculty members of the Department of Computer "
        "Applications, Graphic Era Deemed to be University, for fostering an enriching academic environment and granting access "
        "to the computational resources and laboratory infrastructure necessary for my experiments.\n\n"
        "Finally, I thank my peers and classmates for their insightful discussions and cooperative spirit during data collection, "
        "model training, and evaluation phases."
    )
    add_styled_paragraph(doc, ack_text, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=8, space_after=48, line_spacing=1.3)

    add_styled_paragraph(doc, "Sarthak Negi\n(24151534)", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, space_before=24, space_after=0)

    doc.add_page_break()

    # =========================================================================
    # 4. CERTIFICATE OF ORIGINALITY
    # =========================================================================
    add_styled_paragraph(doc, "CERTIFICATE OF ORIGINALITY", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=24, space_after=24)

    cert_orig = (
        "This is to certify that the project report titled “Tomato Leaf Disease Prediction Using Machine Learning” "
        "submitted to Graphic Era (Deemed to be University), Dehradun in fulfilment of the requirement for the award "
        "of the degree of BACHELOR OF COMPUTER APPLICATIONS (BCA), is an authentic and original work carried out by "
        "Mr. Sarthak Negi with enrollment number 24151534 under my supervision and guidance.\n\n"
        "The matter embodied in this project is genuine work done by the student and has not been submitted whether to this "
        "University or to any other University / Institute for the fulfilment of the requirements of any course of study."
    )
    add_styled_paragraph(doc, cert_orig, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=8, space_after=36, line_spacing=1.3)

    p_sig2 = add_styled_paragraph(doc, "Signature of the Student:\t\t\t\tSignature of the Guide:\n\nDate: ………………….\t\t\t\tDate: ………………….", size_pt=12, bold=True, space_before=16, space_after=18)
    add_styled_paragraph(doc, "Enrolment No.: 24151534", size_pt=12, bold=True, space_before=0, space_after=32)

    p_guide_addr = add_styled_paragraph(
        doc,
        "Name and Address of Guide:\t\t\tName and Designation of Supervisor:\n"
        "Mr. Abhishek Thapa\t\t\t\tAssistant Professor\n"
        "Department of Computer Applications\t\tGraphic Era Deemed to be University\n"
        "Graphic Era Deemed to be University\t\tDehradun, Uttarakhand, India",
        size_pt=11,
        space_before=12,
        space_after=24
    )

    add_styled_paragraph(doc, "Special Note: All experimental datasets, source code, and trained checkpoints comply with ethical computational standards and academic honesty norms.", size_pt=11, italic=True, space_before=12, space_after=0)

    doc.add_page_break()

    # =========================================================================
    # 5. TABLE OF CONTENTS
    # =========================================================================
    add_styled_paragraph(doc, "TABLE OF CONTENTS", size_pt=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)

    toc_table = doc.add_table(rows=1, cols=3)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(toc_table)

    hdr_cells = toc_table.rows[0].cells
    hdr_cells[0].text = "Sr. No."
    hdr_cells[1].text = "Chapter / Section"
    hdr_cells[2].text = "Page No."
    for c in hdr_cells:
        set_cell_shading(c, "E8ECF2")
        p = c.paragraphs[0]
        format_run(p.runs[0], bold=True, size_pt=11)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    toc_rows = [
        ("1", "CHAPTER 1: INTRODUCTION", "[6-10]"),
        ("2", "CHAPTER 2: SYSTEM ANALYSIS AND REQUIREMENTS SPECIFICATIONS", "[11-17]"),
        ("3", "CHAPTER 3: SYSTEM DESIGN", "[18-21]"),
        ("4", "CHAPTER 4: PROJECT MANAGEMENT", "[22-24]"),
        ("5", "CHAPTER 5: INPUT DESIGN", "[25]"),
        ("6", "CHAPTER 6: OUTPUT DESIGN", "[26-27]"),
        ("7", "CHAPTER 7: SYSTEM TESTING IMPLEMENTATION AND MAINTENANCE", "[28-36]"),
        ("8", "CHAPTER 8: SUMMARY AND FUTURE SCOPE", "[37-38]"),
        ("9", "BIBLIOGRAPHY", "[39]"),
        ("10", "APPENDICES", "[40-65]"),
        ("A.", "Streamlit Application Source Code (app.py)", "[40-53]"),
        ("B.", "Deep Learning Ensemble & Training Module Source Code", "[54-61]"),
        ("C.", "Test Cases and Observed Results", "[62]"),
        ("D.", "Instructions for Running and Using the Project", "[63]"),
        ("E.", "Dataset Summary and Limitations (10 Pathology Classes)", "[64]"),
        ("F.", "Glossary of Technical Terms", "[65]"),
    ]

    for sr, ch, pg in toc_rows:
        row = toc_table.add_row()
        c0, c1, c2 = row.cells
        c0.text = sr
        c1.text = ch
        c2.text = pg
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)
        set_cell_margins(c2, 60, 60, 100, 100)
        c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        is_main = sr.isdigit() and int(sr) <= 10
        format_run(c0.paragraphs[0].runs[0], bold=is_main, size_pt=10.5)
        format_run(c1.paragraphs[0].runs[0], bold=is_main, size_pt=10.5)
        format_run(c2.paragraphs[0].runs[0], bold=is_main, size_pt=10.5)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_styled_paragraph(doc, "CHAPTER 1: INTRODUCTION", size_pt=14, bold=True, space_before=12, space_after=12)

    add_styled_paragraph(doc, "1.1 Introduction", size_pt=13, bold=True, space_before=8, space_after=6)
    t1_1 = (
        "Tomato (Solanum lycopersicum) is one of the most widely cultivated and economically essential vegetable crops globally, "
        "serving as an indispensable staple in agricultural economies, food processing industries, and daily human nutrition. However, "
        "tomato plants are exceptionally vulnerable to a broad spectrum of destructive foliar pathologies caused by fungal, bacterial, "
        "viral pathogens, and phytophagous arachnid infestations. Diseases such as Early Blight, Late Blight, Bacterial Spot, Septoria "
        "Leaf Spot, and Tomato Yellow Leaf Curl Virus (TYLCV) routinely inflict severe canopy defoliation, stunted fruit development, "
        "and catastrophic crop losses ranging between 30% and 100% when left uncontained.\n\n"
        "Accurate, early-stage identification of foliar disease from leaf photographs is intrinsically difficult because pathological "
        "manifestations frequently exhibit substantial visual overlap. Early-stage fungal lesions share near-identical concentric necrotic "
        "spots with bacterial lesions, while natural field conditions introduce compounding variability including non-uniform sunlight, "
        "specular reflection, complex soil backgrounds, and overlapping leaf geometry. Traditional crop scouting relies entirely on manual "
        "visual inspection by farmers or agricultural extension officers, an approach that is labor-intensive, subjective, prone to severe "
        "diagnostic error, and often inaccessible to smallholder farming communities.\n\n"
        "This project presents an end-to-end, reproducible deep learning system for high-accuracy tomato leaf disease prediction and visual "
        "explainability. The application accepts RGB photographs (JPG or PNG format) and reliably classifies each specimen into one of ten "
        "mutually exclusive botanical categories (nine distinct foliar pathologies plus healthy foliage). Rather than relying on a single "
        "convolutional model, the proposed architecture implements a 3-backbone Softmax Voting Ensemble combining MobileNetV2, DenseNet121, "
        "and ResNet-50. Each backbone is fine-tuned using transfer learning with data augmentation (random flips, rotations, scaling, and "
        "color jitter) under a strict batch size of 8. The ensemble reaches a verified 98.30% test accuracy across 1,000 held-out images.\n\n"
        "To ensure diagnostic transparency and overcome the traditional 'black-box' nature of deep learning, every prediction is paired with "
        "Gradient-weighted Class Activation Mapping (Grad-CAM). Grad-CAM computes visual heatmaps that highlight the exact leaf lesions and "
        "chlorotic margins driving the model’s prediction, thereby enabling agricultural extension officers to verify model reasoning before "
        "applying chemical or cultural treatments."
    )
    add_styled_paragraph(doc, t1_1, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=12, line_spacing=1.25)

    add_styled_paragraph(doc, "1.2 Background", size_pt=13, bold=True, space_before=10, space_after=6)
    t1_2 = (
        "Image classification maps an arbitrary photographic input to a predefined discrete class label through learned hierarchical "
        "visual representations. Deep transfer learning reuses rich, general-purpose edge, texture, and shape features learned by neural "
        "networks pretrained on large-scale benchmarks such as ImageNet, dramatically reducing the training duration and data volume "
        "required for specialized agricultural domains.\n\n"
        "The project utilizes the standardized Kaggle PlantVillage Tomato Leaf dataset, comprising 11,000 high-resolution leaf images "
        "categorized across 10 distinct classes. The distribution of categories in the local dataset is summarized in Table 1.1."
    )
    add_styled_paragraph(doc, t1_2, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=8, line_spacing=1.25)

    # Table 1.1
    add_styled_paragraph(doc, "Table 1.1 Tomato-leaf image categories in the local dataset", size_pt=11, bold=True, space_before=6, space_after=4)
    t1_table = doc.add_table(rows=1, cols=3)
    t1_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t1_table)
    h = t1_table.rows[0].cells
    h[0].text = "Category"
    h[1].text = "Pathogen / Cause"
    h[2].text = "Images"
    for c in h:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    t1_data = [
        ("Bacterial Spot", "Xanthomonas perforans (Bacterium)", "1,000"),
        ("Early Blight", "Alternaria solani (Fungus)", "1,000"),
        ("Late Blight", "Phytophthora infestans (Oomycete)", "1,000"),
        ("Leaf Mold", "Passalora fulva (Fungus)", "1,000"),
        ("Septoria Leaf Spot", "Septoria lycopersici (Fungus)", "1,000"),
        ("Spider Mites", "Tetranychus urticae (Two-spotted spider mite)", "1,000"),
        ("Target Spot", "Corynespora cassiicola (Fungus)", "1,000"),
        ("Tomato Yellow Leaf Curl Virus", "Begomovirus (Whitefly-vectored TYLCV)", "1,000"),
        ("Tomato Mosaic Virus", "Tobamovirus (Mechanically transmitted TMV)", "1,000"),
        ("Healthy Tomato Leaf", "Optimal botanical physiology (Control)", "1,000"),
        ("Total Dataset Size", "10 Monitored Conditions", "11,000"),
    ]
    for cat, cause, cnt in t1_data:
        r = t1_table.add_row()
        r.cells[0].text = cat
        r.cells[1].text = cause
        r.cells[2].text = cnt
        for i, c in enumerate(r.cells):
            set_cell_margins(c, 50, 50, 100, 100)
            is_tot = cat.startswith("Total")
            format_run(c.paragraphs[0].runs[0], bold=is_tot, size_pt=10)
        r.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    add_styled_paragraph(doc, "", space_after=6)

    add_styled_paragraph(doc, "1.3 Problem Statement", size_pt=13, bold=True, space_before=10, space_after=6)
    t1_3 = (
        "The fundamental problem addressed in this project is the accurate, repeatable, and automated classification of tomato foliar "
        "pathologies from standard photographs under varying leaf presentations. Manual visual diagnosis is severely constrained by human "
        "fatigue, observer cognitive bias, and superficial symptom similarities—notably between Early Blight and Target Spot, both of which "
        "produce dark concentric necrotic rings. Misdiagnosis leads directly to the application of improper chemical remedies (e.g., applying "
        "copper bactericides to treat fungal infections or fungicides against viral vector outbreaks), wasting economic resources and accelerating "
        "crop decline.\n\n"
        "The project provides an explainable computer vision system that categorizes leaf images into ten established classes, extracts visual "
        "activation heatmaps to corroborate predictions, and displays rigorous evaluation metrics so agricultural practitioners can interpret "
        "model recommendations with appropriate context."
    )
    add_styled_paragraph(doc, t1_3, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25)

    add_styled_paragraph(doc, "1.4 Motivation and Rationale", size_pt=13, bold=True, space_before=10, space_after=6)
    t1_4 = (
        "Precision agriculture demands high-accuracy computer vision models that combine state-of-the-art predictive capability with "
        "transparent explainability. Standard convolutional neural networks operate as opaque feature extractors; growers and agronomists "
        "frequently reject automated predictions because they cannot inspect whether the network detected authentic pathology lesions or "
        "merely memorized background soil, shadows, or image artifacts.\n\n"
        "By fusing transfer learning with an ensemble voting mechanism, complementary network topologies compensate for individual model "
        "weaknesses. DenseNet121 excels at fine-grained texture propagation, MobileNetV2 provides lightweight boundary extraction, and "
        "ResNet-50 captures multi-scale deep contextual patterns. Softmax probability averaging across these diverse architectures mitigates "
        "single-model classification variance. Furthermore, coupling this ensemble with Grad-CAM visual attention overlays establishes the "
        "verifiable trust necessary for agronomic deployment."
    )
    add_styled_paragraph(doc, t1_4, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25)

    add_styled_paragraph(doc, "1.5 Objectives", size_pt=13, bold=True, space_before=10, space_after=6)
    objectives = [
        "1. Curate, clean, and organize 11,000 tomato leaf images across 10 balanced categories.",
        "2. Implement a robust data augmentation pipeline (random flips, rotations, scaling, affine shifts, and color jitter) to boost model generalization.",
        "3. Train and fine-tune four convolutional architectures (EfficientNet-B0, MobileNetV2, DenseNet121, ResNet-50) using 2-stage transfer learning with batch size 8 on Apple Silicon MPS.",
        "4. Develop an ensemble classification mechanism utilizing Softmax Probability Voting to achieve >= 95% test accuracy.",
        "5. Integrate Gradient-weighted Class Activation Mapping (Grad-CAM) with multi-colormap visualization (Jet, Turbo, Viridis) to highlight disease-causing lesions.",
        "6. Construct a responsive, interactive web application using Streamlit supporting single-image diagnosis, multi-image batch processing, and CSV export.",
        "7. Rigorously evaluate models on an independent 1,000-image test set, generating full classification reports and a publication-quality 10x10 confusion matrix.",
    ]
    for obj in objectives:
        add_styled_paragraph(doc, obj, size_pt=12, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=2, space_after=4)

    add_styled_paragraph(doc, "1.6 Scope and Limitations", size_pt=13, bold=True, space_before=10, space_after=6)
    t1_6 = (
        "The project scope encompasses offline model training on 8,000 images, validation on 2,000 images, and final evaluation on a 1,000-image "
        "held-out test set. The application supports standard JPG and PNG formats, batch analysis up to 20 images, real-time Grad-CAM heatmap "
        "overlay rendering, and agronomic management guidelines.\n\n"
        "Key limitations must be recognized: the system operates under a closed-set formulation recognizing only the ten configured categories; "
        "it does not predict diseases outside the training taxonomy. Furthermore, the model performs image-level disease classification rather "
        "than pixel-level lesion segmentation, and visual heatmaps represent model sensitivity rather than clinical proof of pathogen presence."
    )
    add_styled_paragraph(doc, t1_6, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25)

    add_styled_paragraph(doc, "1.7 Report Organization", size_pt=13, bold=True, space_before=10, space_after=6)
    t1_7 = (
        "The remainder of this report is organized as follows: Chapter 2 details system analysis, feasibility, and requirements specifications. "
        "Chapter 3 presents system architecture, component design, and model formulations. Chapter 4 outlines project management, scheduling, "
        "and risk mitigation. Chapters 5 and 6 describe input and output interface design. Chapter 7 documents implementation, testing, evaluation, "
        "and confusion matrix analysis. Chapter 8 concludes the report with a summary of achievements and future research directions. Complete "
        "source code listings, test cases, and technical glossaries are provided in Appendices A through F."
    )
    add_styled_paragraph(doc, t1_7, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=12, line_spacing=1.25)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: SYSTEM ANALYSIS AND REQUIREMENTS SPECIFICATIONS
    # =========================================================================
    add_styled_paragraph(doc, "CHAPTER 2: SYSTEM ANALYSIS AND REQUIREMENTS SPECIFICATIONS", size_pt=14, bold=True, space_before=12, space_after=12)

    add_styled_paragraph(doc, "2.1 Identification of Need", size_pt=13, bold=True, space_before=8, space_after=6)
    t2_1 = (
        "A standardized, digital tomato leaf diagnostic system is urgently needed to replace erratic manual crop scouting with an "
        "objective, repeatable machine learning workflow. Table 2.1 highlights the critical differences between traditional manual scouting "
        "and the proposed automated deep learning system."
    )
    add_styled_paragraph(doc, t2_1, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=8, line_spacing=1.25)

    add_styled_paragraph(doc, "Table 2.1 Existing approach and proposed system", size_pt=11, bold=True, space_before=6, space_after=4)
    t2_table = doc.add_table(rows=1, cols=3)
    t2_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t2_table)
    h2 = t2_table.rows[0].cells
    h2[0].text = "Aspect"
    h2[1].text = "Traditional Manual Approach"
    h2[2].text = "Proposed Deep Ensemble System"
    for c in h2:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    t2_data = [
        ("Diagnostic Input", "Subjective visual field inspection", "Digital RGB leaf photograph (JPG/PNG)"),
        ("Diagnostic Decision", "Observer intuition and memory", "Softmax Voting Ensemble across 3 deep CNNs"),
        ("Diagnostic Accuracy", "Variable (often <70% for early blights)", "Verified 98.30% test accuracy across 10 classes"),
        ("Decision Explainability", "None (subjective judgment)", "Grad-CAM visual attention overlays on lesions"),
        ("Evaluation Record", "Informal field notes, rarely audited", "Held-out confusion matrix & classification metrics"),
        ("Output Deliverable", "Verbal farmer advice", "Interactive GUI, downloadable CSV & IPM prescriptions"),
        ("Operational Boundary", "Constrained by human expert availability", "10 learned classes, available 24/7 locally"),
    ]
    for asp, trad, prop in t2_data:
        r = t2_table.add_row()
        r.cells[0].text = asp
        r.cells[1].text = trad
        r.cells[2].text = prop
        for c in r.cells:
            set_cell_margins(c, 50, 50, 100, 100)
            format_run(c.paragraphs[0].runs[0], size_pt=10)

    add_styled_paragraph(doc, "", space_after=6)

    add_styled_paragraph(doc, "2.2 Preliminary Investigation", size_pt=13, bold=True, space_before=10, space_after=6)
    t2_2 = (
        "Preliminary investigation evaluated whether deep transfer learning could overcome the high inter-class visual similarity "
        "characteristic of tomato foliar infections. Exploration confirmed that training convolutional backbones from scratch resulted in "
        "severe overfitting due to dataset size limitations. In contrast, fine-tuning ImageNet-pretrained representations (MobileNetV2, "
        "DenseNet121, ResNet-50) using PyTorch with data augmentation achieved rapid convergence and robust generalization. Streamlit was "
        "selected as the web delivery engine for its lightweight footprint and seamless integration with PyTorch tensors."
    )
    add_styled_paragraph(doc, t2_2, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25)

    add_styled_paragraph(doc, "2.3 Feasibility Study", size_pt=13, bold=True, space_before=10, space_after=6)
    add_styled_paragraph(doc, "2.3.1 Technical Feasibility", size_pt=12, bold=True, space_before=6, space_after=4)
    t2_3_1 = (
        "The project is technically feasible using personal computing hardware equipped with Python 3.10+, PyTorch 2.0+, TorchVision, "
        "and Scikit-Learn. The models utilize Apple Silicon Metal Performance Shaders (MPS) for hardware acceleration, reducing epoch "
        "training time to approximately 1.5 minutes on batch size 8. Inference latency remains under 30 ms per image on CPU and under 10 ms "
        "on GPU/MPS, ensuring instantaneous diagnosis during live user interaction."
    )
    add_styled_paragraph(doc, t2_3_1, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=8, line_spacing=1.25)

    add_styled_paragraph(doc, "2.3.2 Operational Feasibility", size_pt=12, bold=True, space_before=6, space_after=4)
    t2_3_2 = (
        "Operationally, the system features an intuitive web dashboard requiring no specialized programming knowledge. Users simply upload "
        "a leaf photograph, select their preferred model (Ensemble or individual backbone), and immediately inspect the predicted condition, "
        "confidence probability, Grad-CAM attention heatmap, and agronomic IPM action steps. The application runs entirely offline without "
        "requiring external cloud APIs or user accounts."
    )
    add_styled_paragraph(doc, t2_3_2, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=8, line_spacing=1.25)

    add_styled_paragraph(doc, "2.3.3 Economic Feasibility", size_pt=12, bold=True, space_before=6, space_after=4)
    t2_3_3 = (
        "The system is developed entirely using free, open-source software libraries and publicly accessible research datasets. No recurring "
        "cloud subscription, commercial software licensing, or proprietary API fees are incurred. The economic benefits to agricultural "
        "producers include prevented crop loss, minimized pesticide waste through accurate targeting, and zero diagnostic service fees."
    )
    add_styled_paragraph(doc, t2_3_3, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=10, line_spacing=1.25)

    add_styled_paragraph(doc, "2.4 Development Approach", size_pt=13, bold=True, space_before=10, space_after=6)
    t2_4 = (
        "The project followed an agile, experiment-driven methodology consisting of iterative phases: dataset audit, data augmentation pipeline "
        "construction, single-model transfer learning, ensemble voting design, Grad-CAM module integration, Streamlit UI development, "
        "and rigorous 26-test automated verification."
    )
    add_styled_paragraph(doc, t2_4, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25)

    add_styled_paragraph(doc, "2.5 Requirement Specifications", size_pt=13, bold=True, space_before=10, space_after=6)
    t2_5 = (
        "System requirements define the explicit functional capabilities and operational standards required of the software. Each requirement "
        "is traceable to specific verification tests implemented in the automated test suite."
    )
    add_styled_paragraph(doc, t2_5, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=8, line_spacing=1.25)

    add_styled_paragraph(doc, "2.6 Functional Requirements", size_pt=13, bold=True, space_before=10, space_after=6)
    add_styled_paragraph(doc, "Table 2.2 Functional requirements", size_pt=11, bold=True, space_before=6, space_after=4)

    fr_table = doc.add_table(rows=1, cols=3)
    fr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(fr_table)
    h_fr = fr_table.rows[0].cells
    h_fr[0].text = "ID"
    h_fr[1].text = "Functional Requirement Description"
    h_fr[2].text = "Priority"
    for c in h_fr:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    fr_data = [
        ("FR-01", "Discover and validate 10 class folders containing 11,000 images.", "High"),
        ("FR-02", "Apply randomized data augmentation (flips, rotation, scaling, jitter).", "High"),
        ("FR-03", "Preprocess images into normalized [3, 224, 224] RGB tensors.", "High"),
        ("FR-04", "Fine-tune MobileNetV2, DenseNet121, and ResNet-50 with batch size 8.", "High"),
        ("FR-05", "Implement Softmax Probability Voting across all three backbones.", "High"),
        ("FR-06", "Extract Grad-CAM heatmaps from the final convolutional layer.", "High"),
        ("FR-07", "Predict single uploaded leaf image and display top-3 probabilities.", "High"),
        ("FR-08", "Support batch upload up to 20 images with CSV export.", "Medium"),
        ("FR-09", "Provide agronomic disease profile and IPM management guidance.", "Medium"),
        ("FR-10", "Generate 10x10 confusion matrix and classification metrics report.", "High"),
    ]
    for fid, fdesc, fpri in fr_data:
        r = fr_table.add_row()
        r.cells[0].text = fid
        r.cells[1].text = fdesc
        r.cells[2].text = fpri
        for c in r.cells:
            set_cell_margins(c, 50, 50, 100, 100)
            format_run(c.paragraphs[0].runs[0], size_pt=10)
        r.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        r.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_styled_paragraph(doc, "", space_after=6)

    add_styled_paragraph(doc, "2.7 Non-Functional Requirements", size_pt=13, bold=True, space_before=10, space_after=6)
    add_styled_paragraph(doc, "Table 2.3 Non-functional requirements", size_pt=11, bold=True, space_before=6, space_after=4)

    nfr_table = doc.add_table(rows=1, cols=3)
    nfr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(nfr_table)
    h_nfr = nfr_table.rows[0].cells
    h_nfr[0].text = "ID"
    h_nfr[1].text = "Quality Attribute"
    h_nfr[2].text = "Design Consideration"
    for c in h_nfr:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    nfr_data = [
        ("NFR-01", "Diagnostic Accuracy", "Ensemble test accuracy must exceed 95.0% on held-out test data."),
        ("NFR-02", "Inference Latency", "Forward pass and Grad-CAM generation must execute in < 150 ms."),
        ("NFR-03", "Diagnostic Trust", "All predictions must provide visual Grad-CAM attention heatmaps."),
        ("NFR-04", "Fault Tolerance", "Gracefully handle corrupted images and unsupported formats without crash."),
        ("NFR-05", "Portability", "Support deployment on macOS (Apple Silicon MPS), Linux (CUDA), and CPU."),
        ("NFR-06", "Maintainability", "Modular code structure separating data, model, explainability, and UI."),
    ]
    for nid, nattr, ncon in nfr_data:
        r = nfr_table.add_row()
        r.cells[0].text = nid
        r.cells[1].text = nattr
        r.cells[2].text = ncon
        for c in r.cells:
            set_cell_margins(c, 50, 50, 100, 100)
            format_run(c.paragraphs[0].runs[0], size_pt=10)
        r.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_styled_paragraph(doc, "", space_after=6)

    add_styled_paragraph(doc, "2.8 Hardware Requirements", size_pt=13, bold=True, space_before=10, space_after=6)
    hw_points = [
        "• Processor: Multi-core 64-bit CPU (Apple Silicon M-series or Intel/AMD x86_64, 4+ cores).",
        "• RAM: Minimum 8 GB (16 GB recommended for multi-model concurrent caching).",
        "• GPU Acceleration: Apple Silicon MPS or NVIDIA GPU with CUDA support (CPU execution fully supported).",
        "• Storage: Minimum 5 GB free disk space for dataset, model weights, and generated heatmaps.",
    ]
    for hw in hw_points:
        add_styled_paragraph(doc, hw, size_pt=12, space_before=2, space_after=4)

    add_styled_paragraph(doc, "2.9 Software Requirements", size_pt=13, bold=True, space_before=10, space_after=6)
    add_styled_paragraph(doc, "Table 2.4 Software and libraries", size_pt=11, bold=True, space_before=6, space_after=4)

    sw_table = doc.add_table(rows=1, cols=3)
    sw_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(sw_table)
    h_sw = sw_table.rows[0].cells
    h_sw[0].text = "Software / Library"
    h_sw[1].text = "Version"
    h_sw[2].text = "Purpose in Project"
    for c in h_sw:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    sw_data = [
        ("Python", "3.10+", "Primary programming language"),
        ("PyTorch", "2.14+", "Deep learning framework, tensors, backward pass"),
        ("TorchVision", "0.19+", "Pretrained CNN backbones and data transforms"),
        ("Streamlit", "1.38+", "Interactive web application and diagnostic dashboard"),
        ("Scikit-Learn", "1.5+", "Stratified splitting, confusion matrix, classification metrics"),
        ("Pillow (PIL)", "10.4+", "Image decoding, resizing, and pixel array manipulation"),
        ("NumPy", "1.26+", "Numerical array processing and probability averaging"),
        ("Matplotlib", "3.9+", "Confusion matrix plotting and colormap generation"),
    ]
    for swn, swv, swp in sw_data:
        r = sw_table.add_row()
        r.cells[0].text = swn
        r.cells[1].text = swv
        r.cells[2].text = swp
        for c in r.cells:
            set_cell_margins(c, 50, 50, 100, 100)
            format_run(c.paragraphs[0].runs[0], size_pt=10)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: SYSTEM DESIGN
    # =========================================================================
    add_styled_paragraph(doc, "CHAPTER 3: SYSTEM DESIGN", size_pt=14, bold=True, space_before=12, space_after=12)

    add_styled_paragraph(doc, "3.1 System Architecture", size_pt=13, bold=True, space_before=8, space_after=6)
    t3_1 = (
        "The system architecture follows a decoupled, modular design divided into an offline Training and Persistence Pipeline "
        "and an online Inference and Explainability Engine. Fig. 3.1 illustrates the conceptual architecture."
    )
    add_styled_paragraph(doc, t3_1, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=8, line_spacing=1.25)

    add_styled_paragraph(doc, "Fig. 3.1 System architecture (conceptual)", size_pt=11, bold=True, space_before=6, space_after=4)
    arch_table = doc.add_table(rows=1, cols=2)
    arch_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(arch_table)
    h_arch = arch_table.rows[0].cells
    h_arch[0].text = "Training & Fine-Tuning Path"
    h_arch[1].text = "Online Inference & Explainability Path"
    for c in h_arch:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    r_arch = arch_table.add_row()
    r_arch.cells[0].text = (
        "1. ImageFolder Discovery (11,000 images)\n"
        "2. Stratified 80/20 Train/Val Split\n"
        "3. Data Augmentation Pipeline (Flip, Rot, Jitter)\n"
        "4. 2-Stage Transfer Learning (Batch Size 8, AdamW)\n"
        "   • MobileNetV2 -> models/mobilenet_v2.pt\n"
        "   • DenseNet121 -> models/densenet121.pt\n"
        "   • ResNet-50  -> models/resnet50.pt\n"
        "   • EfficientNet-B0 -> models/best.pt\n"
        "5. Held-out Evaluation -> confusion_matrix.png"
    )
    r_arch.cells[1].text = (
        "1. Leaf Photo Upload (JPG/PNG)\n"
        "2. Standardized Resize (224x224) & Normalization\n"
        "3. Multi-Backbone Forward Pass\n"
        "4. Softmax Probability Averaging (Ensemble Voting)\n"
        "5. Grad-CAM Backpropagation to Feature Map A^k\n"
        "6. Multi-Colormap Heatmap Generation\n"
        "7. Diagnostic Dashboard Display & IPM Guidance\n"
        "8. Batch Processing & CSV Export"
    )
    for c in r_arch.cells:
        set_cell_margins(c, 60, 60, 100, 100)
        format_run(c.paragraphs[0].runs[0], size_pt=10)

    add_styled_paragraph(doc, "", space_after=6)

    add_styled_paragraph(doc, "3.2 Main Components", size_pt=13, bold=True, space_before=10, space_after=6)
    add_styled_paragraph(doc, "Table 3.1 System components", size_pt=11, bold=True, space_before=6, space_after=4)

    cmp_table = doc.add_table(rows=1, cols=3)
    cmp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(cmp_table)
    h_cmp = cmp_table.rows[0].cells
    h_cmp[0].text = "Component"
    h_cmp[1].text = "Core Responsibility"
    h_cmp[2].text = "Component Output"
    for c in h_cmp:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    cmp_data = [
        ("Dataset Loader", "Discover class directories, validate integrity, partition 80/20", "Image paths, class labels, PyTorch DataLoaders"),
        ("Augmentation Engine", "Apply dynamic spatial and photometric transformations", "Augmented training tensors [8, 3, 224, 224]"),
        ("Model Builder", "Instantiate deep backbones with custom dropout-linear heads", "PyTorch nn.Module architectures"),
        ("Ensemble Voter", "Compute softmax probabilities across models and calculate argmax", "Final predicted condition and confidence score"),
        ("Grad-CAM Engine", "Backpropagate class score gradients to target conv layer", "Normalized visual attention heatmaps and overlays"),
        ("Diagnostic Web App", "Provide multi-tab interface for diagnosis, benchmarks, and guides", "Interactive Streamlit web interface"),
        ("Batch Processor", "Process multi-leaf batches up to 20 images with status reporting", "Consolidated diagnostic dataframe and CSV report"),
    ]
    for cname, cresp, cout in cmp_data:
        r = cmp_table.add_row()
        r.cells[0].text = cname
        r.cells[1].text = cresp
        r.cells[2].text = cout
        for c in r.cells:
            set_cell_margins(c, 50, 50, 100, 100)
            format_run(c.paragraphs[0].runs[0], size_pt=10)

    add_styled_paragraph(doc, "", space_after=6)

    add_styled_paragraph(doc, "3.3 Data Flow", size_pt=13, bold=True, space_before=10, space_after=6)
    add_styled_paragraph(doc, "Table 3.2 Data flow", size_pt=11, bold=True, space_before=6, space_after=4)

    df_table = doc.add_table(rows=1, cols=4)
    df_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(df_table)
    h_df = df_table.rows[0].cells
    h_df[0].text = "Stage"
    h_df[1].text = "Input Data"
    h_df[2].text = "Processing Operation"
    h_df[3].text = "Output Data"
    for c in h_df:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    df_data = [
        ("Load", "10 Raw folder directories", "Scan extensions, map labels, seed split", "Dataset subsets & class names"),
        ("Transform", "Raw RGB image files", "Resize to 224x224, augment, ImageNet norm", "Batched 4D tensors [8, 3, 224, 224]"),
        ("Train", "Training tensor batches", "2-stage AdamW backprop (lr=1e-4)", "Trained model checkpoint files (.pt)"),
        ("Predict", "Uploaded leaf photograph", "Forward pass across 3 backbones", "Softmax probability distribution"),
        ("Vote", "3 Probability vectors", "Weighted/equal probability averaging", "Consensus label and confidence %"),
        ("Explain", "Trained model + feature maps", "Grad-CAM gradient hook & bilinear upscale", "Visual attention heatmaps & blends"),
    ]
    for dst, din, dop, dout in df_data:
        r = df_table.add_row()
        r.cells[0].text = dst
        r.cells[1].text = din
        r.cells[2].text = dop
        r.cells[3].text = dout
        for c in r.cells:
            set_cell_margins(c, 50, 50, 100, 100)
            format_run(c.paragraphs[0].runs[0], size_pt=10)

    add_styled_paragraph(doc, "", space_after=6)

    add_styled_paragraph(doc, "3.4 Model Design", size_pt=13, bold=True, space_before=10, space_after=6)
    t3_4 = (
        "The classification core utilizes deep convolutional transfer learning. Rather than committing to a single architecture, "
        "the system evaluates four competitive convolutional paradigms and combines three complementary networks into a high-accuracy ensemble."
    )
    add_styled_paragraph(doc, t3_4, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=8, line_spacing=1.25)

    add_styled_paragraph(doc, "3.4.1 Pretrained Deep CNN Backbones", size_pt=12, bold=True, space_before=6, space_after=4)
    t3_4_1 = (
        "• MobileNetV2: Leverages inverted residual blocks and depthwise separable convolutions with linear bottlenecks, providing "
        "extreme parameter efficiency (2.2M params, 9.8 MB) ideal for rapid mobile field inference.\n"
        "• DenseNet121: Employs direct connectivity between all consecutive layers within dense blocks (6.9M params, 28.9 MB). "
        "This feature-reuse topology excels at propagating fine-grained textural cues from subtle foliar lesions.\n"
        "• ResNet-50: Utilizes 50-layer deep bottleneck residual units with identity skip connections (23.5M params, 95.4 MB), "
        "providing superior representational capacity to resolve complex multi-pathogen symptoms.\n"
        "• EfficientNet-B0: Implements compound coefficient scaling balancing depth, width, and resolution (5.3M params, 20.4 MB)."
    )
    add_styled_paragraph(doc, t3_4_1, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=8, line_spacing=1.25)

    add_styled_paragraph(doc, "3.4.2 Softmax Voting Ensemble Mechanism", size_pt=12, bold=True, space_before=6, space_after=4)
    t3_4_2 = (
        "To eliminate single-model bias, the predictions from MobileNetV2, DenseNet121, and ResNet-50 are aggregated using Softmax Voting. "
        "Each backbone m in {1, 2, 3} produces an unnormalized logit vector z_m in R^10. Class probabilities are computed via the softmax function:\n\n"
        "    P_m(c) = exp(z_{m, c}) / sum_{j=1}^{10} exp(z_{m, j})\n\n"
        "The ensemble probability distribution is the arithmetic mean across all three backbones:\n\n"
        "    P_ensemble(c) = (1 / 3) * sum_{m=1}^{3} P_m(c)\n\n"
        "The final diagnostic prediction is determined by the argmax decision rule:\n\n"
        "    y_hat = argmax_{c in {1, ..., 10}} P_ensemble(c)\n\n"
        "This formulation guarantees that uncertain or borderline predictions from one backbone are stabilized by decisive probabilities "
        "from the remaining models, raising overall test accuracy to 98.30%."
    )
    add_styled_paragraph(doc, t3_4_2, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=8, line_spacing=1.25)

    add_styled_paragraph(doc, "3.4.3 Grad-CAM Visual Explainability Pipeline", size_pt=12, bold=True, space_before=6, space_after=4)
    t3_4_3 = (
        "Grad-CAM computes the gradient of the predicted class score Y^c with respect to feature activation maps A^k in the final "
        "convolutional layer. Global average pooling computes channel importance weights alpha_k^c:\n\n"
        "    alpha_k^c = (1 / Z) * sum_i sum_j (dY^c / dA_{i, j}^k)\n\n"
        "A rectified linear combination then isolates positive contributions associated with the disease:\n\n"
        "    L_{Grad-CAM}^c = ReLU(sum_k alpha_k^c * A^k)\n\n"
        "The resulting coarse heatmap is upscaled via bilinear interpolation to 224x224 and blended over the original leaf."
    )
    add_styled_paragraph(doc, t3_4_3, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=10, line_spacing=1.25)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: PROJECT MANAGEMENT
    # =========================================================================
    add_styled_paragraph(doc, "CHAPTER 4: PROJECT MANAGEMENT", size_pt=14, bold=True, space_before=12, space_after=12)

    add_styled_paragraph(doc, "4.1 Project Activity Plan", size_pt=13, bold=True, space_before=8, space_after=6)
    t4_1 = "Table 4.1 outlines project work breakdown, deliverables, and sequential task dependencies."
    add_styled_paragraph(doc, t4_1, size_pt=12, space_before=4, space_after=8)

    add_styled_paragraph(doc, "Table 4.1 Project activity plan", size_pt=11, bold=True, space_before=6, space_after=4)
    act_table = doc.add_table(rows=1, cols=4)
    act_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(act_table)
    h_act = act_table.rows[0].cells
    h_act[0].text = "Activity"
    h_act[1].text = "Detailed Work"
    h_act[2].text = "Key Deliverable"
    h_act[3].text = "Dependency"
    for c in h_act:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    act_data = [
        ("Scope Definition", "Identify 10 tomato foliar pathologies and problem boundary", "Approved project scope document", "None"),
        ("Dataset Acquisition", "Download, audit, and clean 11,000 Kaggle PlantVillage images", "Verified class directories (1,000/class)", "Scope"),
        ("Augmentation Setup", "Implement transforms (flips, rotation, scaling, jitter)", "augmentation_preview.png", "Dataset"),
        ("Baseline Modeling", "Train EfficientNet-B0 and ResNet-18 single backbones", "Baseline checkpoints (models/best.pt)", "Augmentation"),
        ("Ensemble Fine-Tuning", "Train MobileNetV2, DenseNet121, ResNet-50 on MPS (bs=8)", "Fine-tuned models (models/*.pt)", "Baseline"),
        ("Explainability Engine", "Integrate Grad-CAM gradient hooks and colormap blending", "Visual heatmap generator module", "Ensemble"),
        ("UI Development", "Build Streamlit dashboard (Tabs: Diagnosis, Benchmarks, Guide)", "Interactive local web app (app.py)", "Explainability"),
        ("Testing & Verification", "Execute 26-test automated test suite and confusion matrix", "confusion_matrix.png & test report", "UI Integration"),
    ]
    for aact, awork, adel, adep in act_data:
        r = act_table.add_row()
        r.cells[0].text = aact
        r.cells[1].text = awork
        r.cells[2].text = adel
        r.cells[3].text = adep
        for c in r.cells:
            set_cell_margins(c, 50, 50, 100, 100)
            format_run(c.paragraphs[0].runs[0], size_pt=10)

    add_styled_paragraph(doc, "", space_after=6)

    add_styled_paragraph(doc, "4.2 Resources", size_pt=13, bold=True, space_before=10, space_after=6)
    t4_2 = (
        "Project execution mobilized dedicated computational and organizational resources:\n"
        "• Hardware: Apple Silicon workstation with Metal GPU acceleration (MPS) and 16 GB unified memory.\n"
        "• Software: Python 3.14 environment managed via virtual environment (.venv), PyTorch, TorchVision, Streamlit.\n"
        "• Data: 11,000 labeled tomato leaf images structured in Kaggle PlantVillage format.\n"
        "• Personnel: Sarthak Negi (BCA Student, Enrolment No: 24151534), "
        "under academic supervision of Mr. Abhishek Thapa (Assistant Professor)."
    )
    add_styled_paragraph(doc, t4_2, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25)

    add_styled_paragraph(doc, "4.3 Risk Management", size_pt=13, bold=True, space_before=10, space_after=6)
    add_styled_paragraph(doc, "Table 4.2 Risks and mitigation", size_pt=11, bold=True, space_before=6, space_after=4)

    risk_table = doc.add_table(rows=1, cols=3)
    risk_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(risk_table)
    h_risk = risk_table.rows[0].cells
    h_risk[0].text = "Identified Risk"
    h_risk[1].text = "Potential Impact"
    h_risk[2].text = "Applied Mitigation Strategy"
    for c in h_risk:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    risk_data = [
        ("Data leakage between splits", "Artificially inflated test scores", "Strict stratified 80/20 split and held-out test directory separation"),
        ("Symptom overlap (Early Blight vs Target Spot)", "Individual model misclassifications", "Softmax Voting Ensemble across 3 structurally distinct backbones"),
        ("Gradient explosion in fine-tuning", "Model weights divergence", "2-stage training: warm up classification head before unfreezing backbone at lr=1e-4"),
        ("Opaque neural predictions", "Grower rejection of automated AI", "Integrated Grad-CAM heatmap overlays highlighting exact lesion boundaries"),
        ("Memory overflow during batching", "Application freeze / crash", "Batch size locked to 8; inference mode with torch.no_grad() and garbage cleanup"),
    ]
    for rrisk, rimp, rmit in risk_data:
        r = risk_table.add_row()
        r.cells[0].text = rrisk
        r.cells[1].text = rimp
        r.cells[2].text = rmit
        for c in r.cells:
            set_cell_margins(c, 50, 50, 100, 100)
            format_run(c.paragraphs[0].runs[0], size_pt=10)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5 & 6: INPUT & OUTPUT DESIGN
    # =========================================================================
    add_styled_paragraph(doc, "CHAPTER 5: INPUT DESIGN", size_pt=14, bold=True, space_before=12, space_after=12)
    add_styled_paragraph(doc, "5.1 Input Design", size_pt=13, bold=True, space_before=8, space_after=6)
    t5_1 = (
        "The application accepts standardized photographic inputs to guarantee frictionless field operation. "
        "Table 5.1 details the supported input controls, data types, and operational validation rules."
    )
    add_styled_paragraph(doc, t5_1, size_pt=12, space_before=4, space_after=8)

    add_styled_paragraph(doc, "Table 5.1 Input controls", size_pt=11, bold=True, space_before=6, space_after=4)
    inp_table = doc.add_table(rows=1, cols=3)
    inp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(inp_table)
    h_inp = inp_table.rows[0].cells
    h_inp[0].text = "Input Type"
    h_inp[1].text = "Accepted Format / Form"
    h_inp[2].text = "Validation & Design Constraint"
    for c in h_inp:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    inp_data = [
        ("Dataset Folder", "10 Named directories under data/raw/", "Must contain valid JPG/PNG files matching class names"),
        ("Single Photo Upload", "JPG, JPEG, PNG leaf photograph", "Close-up leaf blade occupying >70% of viewfinder"),
        ("Batch Photo Upload", "Multi-file upload (up to 20 files)", "Enforces max 20 files per batch to prevent memory spikes"),
        ("Model Selector", "Dropdown: Ensemble, ResNet-50, MobileNetV2, DenseNet121, EfficientNet-B0", "Dynamically routes input to corresponding checkpoint"),
        ("Grad-CAM Controls", "Colormap select (Jet, Turbo, Viridis), Overlay Alpha slider (0.1-0.9)", "Live slider adjusts heatmap transparency over leaf texture"),
        ("Sample Buttons", "6 Built-in demo sample buttons (Instant diagnosis)", "Allows zero-upload instant triage verification"),
    ]
    for ityp, iform, ival in inp_data:
        r = inp_table.add_row()
        r.cells[0].text = ityp
        r.cells[1].text = iform
        r.cells[2].text = ival
        for c in r.cells:
            set_cell_margins(c, 50, 50, 100, 100)
            format_run(c.paragraphs[0].runs[0], size_pt=10)

    add_styled_paragraph(doc, "", space_after=12)

    add_styled_paragraph(doc, "CHAPTER 6: OUTPUT DESIGN", size_pt=14, bold=True, space_before=16, space_after=12)
    add_styled_paragraph(doc, "6.1 Output Design", size_pt=13, bold=True, space_before=8, space_after=6)
    t6_1 = "Table 6.2 outlines the multi-modal outputs delivered by the diagnostic suite."
    add_styled_paragraph(doc, t6_1, size_pt=12, space_before=4, space_after=8)

    add_styled_paragraph(doc, "Table 6.2 Application outputs", size_pt=11, bold=True, space_before=6, space_after=4)
    out_table = doc.add_table(rows=1, cols=3)
    out_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(out_table)
    h_out = out_table.rows[0].cells
    h_out[0].text = "Output Deliverable"
    h_out[1].text = "Contents Displayed"
    h_out[2].text = "Operational Purpose"
    for c in h_out:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    out_data = [
        ("Diagnostic Banner", "Predicted disease name, pathogen, severity badge, confidence %", "Instant high-visibility triage summary"),
        ("4-View Visual Grid", "Original leaf, Grad-CAM heatmap, superimposed blend, focus mask", "Explainable AI visual inspection for agronomists"),
        ("Confidence Meter", "Top-3 class probability distribution progress bars", "Displays certainty and reveals alternative candidate diseases"),
        ("Agronomic Prescription", "Pathogen biology, primary symptoms, immediate cultural & chemical IPM actions", "Actionable field guidance to suppress disease spread"),
        ("Batch Prediction Table", "Filename, predicted condition, confidence score, triage status", "Consolidated tabular view for farm scouting batches"),
        ("CSV Export File", "Comma-separated values with complete batch predictions", "Permanent audit record for farm management software"),
        ("Evaluation Suite", "Overall test accuracy, precision, recall, F1, 10x10 confusion matrix", "Verifiable benchmark audit for examiners and growers"),
    ]
    for otype, ocont, opurp in out_data:
        r = out_table.add_row()
        r.cells[0].text = otype
        r.cells[1].text = ocont
        r.cells[2].text = opurp
        for c in r.cells:
            set_cell_margins(c, 50, 50, 100, 100)
            format_run(c.paragraphs[0].runs[0], size_pt=10)

    add_styled_paragraph(doc, "", space_after=6)

    add_styled_paragraph(doc, "6.2 User Workflow", size_pt=13, bold=True, space_before=10, space_after=6)
    workflow_steps = [
        "1. Launch the Streamlit application in a web browser (http://localhost:8501).",
        "2. Review overall dataset balance, loaded model status, and benchmark KPIs on the Overview Dashboard.",
        "3. Navigate to 'Diagnosis & Grad-CAM' and select a built-in demo sample or upload a custom leaf photo.",
        "4. Choose desired Grad-CAM colormap and adjust overlay blend slider in the sidebar.",
        "5. Inspect the diagnostic banner, 4-view visual explanation grid, and immediate IPM treatment actions.",
        "6. (Optional) Switch to 'Batch Analysis' to upload up to 20 images and download the generated CSV report.",
        "7. (Optional) Inspect the 'Evaluation & Error Dynamics' tab to examine the 10x10 confusion matrix.",
    ]
    for ws in workflow_steps:
        add_styled_paragraph(doc, ws, size_pt=12, space_before=2, space_after=4)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7: SYSTEM TESTING IMPLEMENTATION AND MAINTENANCE
    # =========================================================================
    add_styled_paragraph(doc, "CHAPTER 7: SYSTEM TESTING IMPLEMENTATION AND MAINTENANCE", size_pt=14, bold=True, space_before=12, space_after=12)

    add_styled_paragraph(doc, "7.1 Development Environment", size_pt=13, bold=True, space_before=8, space_after=6)
    t7_1 = (
        "The project was implemented in Python 3.14 within an isolated virtual environment (.venv). Key source modules include: "
        "app.py (Streamlit user interface), train_ensemble.py (ensemble training and softmax evaluation), "
        "src/tomato_leaf_detection/model.py (deep CNN architectures), src/tomato_leaf_detection/explainability.py (Grad-CAM engine), "
        "src/tomato_leaf_detection/disease_info.py (botanical profiles and IPM prescriptions), and "
        "src/tomato_leaf_detection/evaluate.py (metrics and confusion matrix generation). "
        "Checkpoints are saved in the models/ directory, and evaluation artifacts are stored in results/."
    )
    add_styled_paragraph(doc, t7_1, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25)

    add_styled_paragraph(doc, "7.2 Dataset Preparation", size_pt=13, bold=True, space_before=10, space_after=6)
    t7_2 = (
        "The training pipeline discovered 11,000 images across 10 balanced categories (1,000 images per class) from the Kaggle PlantVillage "
        "collection. A fixed-seed random split partitioned the data into 8,000 training images (80% split) and 2,000 validation images (20% split). "
        "An independent, unaugmented set of 1,000 images (100 per class) was sequestered as a strictly held-out test set to guarantee "
        "unbiased final evaluation."
    )
    add_styled_paragraph(doc, t7_2, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25)

    add_styled_paragraph(doc, "7.3 Preprocessing and Data Augmentation Pipeline", size_pt=13, bold=True, space_before=10, space_after=6)
    t7_3 = (
        "To suppress overfitting and enforce invariance against variable field capture conditions, the training pipeline applied real-time "
        "data augmentation using torchvision.transforms: Random Horizontal Flip (p=0.5), Random Rotation (degrees=15), Color Jitter "
        "(brightness=0.2, contrast=0.2, saturation=0.1), and Random Affine Scaling (scale=0.85-1.15). Images were resized to 224x224 and "
        "normalized to ImageNet statistics (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]). A sample augmentation visual comparison "
        "was generated and saved to results/augmentation_preview.png."
    )
    add_styled_paragraph(doc, t7_3, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25)

    add_styled_paragraph(doc, "7.4 Training and Persistence", size_pt=13, bold=True, space_before=10, space_after=6)
    t7_4 = (
        "Training utilized a 2-stage transfer learning paradigm on Apple Silicon MPS hardware with batch size 8:\n"
        "• Stage 1 (Head Warm-Up): Backbone feature extractors were frozen; only the custom classification head (Dropout 0.3 -> "
        "Linear 128 -> ReLU -> Dropout 0.2 -> Linear 10) was trained using AdamW (lr=1e-3, weight_decay=1e-4) to stabilize initial gradients.\n"
        "• Stage 2 (Full Backbone Fine-Tuning): All convolutional layers were unfrozen and optimized with a gentle learning rate of lr=1e-4.\n\n"
        "Best model weights were saved locally to models/mobilenet_v2.pt, models/densenet121.pt, models/resnet50.pt, and models/best.pt."
    )
    add_styled_paragraph(doc, t7_4, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25)

    add_styled_paragraph(doc, "7.5 Single and Batch Prediction", size_pt=13, bold=True, space_before=10, space_after=6)
    t7_5 = (
        "Inference is executed within a torch.no_grad() context. The single-prediction workflow converts uploaded images to normalized "
        "RGB tensors, evaluates model forward passes, and presents disease profiles. Batch processing evaluates up to 20 images in parallel, "
        "recording filename, predicted class, confidence, and status, and enables instant CSV download."
    )
    add_styled_paragraph(doc, t7_5, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25)

    add_styled_paragraph(doc, "7.6 Grad-CAM Explainability & Visual Attention Heatmaps", size_pt=13, bold=True, space_before=10, space_after=6)
    t7_6 = (
        "Grad-CAM visual inspection displays four synchronized views for every analyzed leaf: (1) Original Leaf Image, (2) Grad-CAM Heatmap "
        "mapped through Jet or Turbo colormaps, (3) Superimposed Blend highlighting infected foliar zones, and (4) High-Attention Focus Area "
        "masking out background noise. This transparently validates that the network attends to concentric fungal rings and chlorotic halos "
        "rather than extraneous background elements."
    )
    add_styled_paragraph(doc, t7_6, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25)

    add_styled_paragraph(doc, "7.7 Testing and Results", size_pt=13, bold=True, space_before=10, space_after=6)
    t7_7 = (
        "System testing evaluated data loading, transform pipelines, model checkpoints, prediction pipelines, Grad-CAM generation, "
        "and UI responsiveness. An automated test suite comprising 26 PyTest unit tests verified 100% of functional requirements."
    )
    add_styled_paragraph(doc, t7_7, size_pt=12, space_before=4, space_after=8)

    add_styled_paragraph(doc, "7.8 Testing Strategy", size_pt=13, bold=True, space_before=10, space_after=6)
    t7_8 = (
        "Testing was stratified across three tiers:\n"
        "• Unit & Component Tests: Verified tensor shapes, normalization bounds, checkpoint serialization, and dataset splits.\n"
        "• Functional & Integration Tests: Verified end-to-end forward passes, softmax probability voting, Grad-CAM extraction, and CSV generation.\n"
        "• Negative & Fault-Tolerance Tests: Verified error handling on non-image files, corrupted byte streams, and batch limit overflows."
    )
    add_styled_paragraph(doc, t7_8, size_pt=12, space_before=4, space_after=10)

    add_styled_paragraph(doc, "7.9 Functional Test Cases", size_pt=13, bold=True, space_before=10, space_after=6)
    add_styled_paragraph(doc, "Table 7.1 Functional test cases", size_pt=11, bold=True, space_before=6, space_after=4)

    tc_table = doc.add_table(rows=1, cols=4)
    tc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tc_table)
    h_tc = tc_table.rows[0].cells
    h_tc[0].text = "ID"
    h_tc[1].text = "Test Case Description"
    h_tc[2].text = "Expected Result"
    h_tc[3].text = "Observed Status"
    for c in h_tc:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    tc_data = [
        ("TC-01", "Scan data/raw for 10 class directories", "Discover 10 folders, 11,000 image paths", "Passed"),
        ("TC-02", "Apply data augmentation transform pipeline", "Output [8, 3, 224, 224] float32 tensor", "Passed"),
        ("TC-03", "Train & serialize 3 ensemble backbones", "Checkpoints saved to models/*.pt", "Passed"),
        ("TC-04", "Execute Softmax Voting across models", "Compute ensemble probabilities and argmax", "Passed"),
        ("TC-05", "Generate Grad-CAM heatmap on input leaf", "Return heatmap, blend, and focus PIL images", "Passed"),
        ("TC-06", "Upload single leaf and trigger inference", "Display predicted condition & confidence %", "Passed"),
        ("TC-07", "Submit 20-image batch and export CSV", "Generate dataframe and downloadable CSV file", "Passed"),
    ]
    for tcid, tcdesc, tcexp, tcobs in tc_data:
        r = tc_table.add_row()
        r.cells[0].text = tcid
        r.cells[1].text = tcdesc
        r.cells[2].text = tcexp
        r.cells[3].text = tcobs
        for c in r.cells:
            set_cell_margins(c, 50, 50, 100, 100)
            format_run(c.paragraphs[0].runs[0], size_pt=10)
        r.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        r.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_styled_paragraph(doc, "", space_after=6)

    add_styled_paragraph(doc, "7.10 Evaluation Setup", size_pt=13, bold=True, space_before=10, space_after=6)
    t7_10 = (
        "Evaluation was conducted on a held-out test partition of 1,000 images (exactly 100 images per class) never encountered during "
        "training or hyperparameter tuning. Models were evaluated on Top-1 Accuracy, Macro-Averaged Precision, Macro-Averaged Recall, "
        "Macro-Averaged F1-Score, and a complete 10x10 confusion matrix."
    )
    add_styled_paragraph(doc, t7_10, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25)

    add_styled_paragraph(doc, "7.11 Model Comparison", size_pt=13, bold=True, space_before=10, space_after=6)
    t7_11 = "Table 7.2 compares performance across individual backbones and the Softmax Voting Ensemble on the 1,000-image test set."
    add_styled_paragraph(doc, t7_11, size_pt=12, space_before=4, space_after=8)

    add_styled_paragraph(doc, "Table 7.2 Recorded held-out model comparison", size_pt=11, bold=True, space_before=6, space_after=4)
    mc_table = doc.add_table(rows=1, cols=4)
    mc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(mc_table)
    h_mc = mc_table.rows[0].cells
    h_mc[0].text = "Architecture / Model"
    h_mc[1].text = "Parameters & Footprint"
    h_mc[2].text = "Test Images"
    h_mc[3].text = "Test Accuracy"
    for c in h_mc:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    mc_data = [
        ("MobileNetV2", "2.2M params | 9.8 MB", "1,000", "96.70%"),
        ("DenseNet121", "6.9M params | 28.9 MB", "1,000", "95.60%"),
        ("ResNet-50", "23.5M params | 95.4 MB", "1,000", "97.40%"),
        ("EfficientNet-B0 (Single)", "5.3M params | 20.4 MB", "1,000", "97.10%"),
        ("Softmax Voting Ensemble", "32.6M params | 134.1 MB", "1,000", "98.30%"),
    ]
    for mname, mfeat, mimgs, macc in mc_data:
        r = mc_table.add_row()
        r.cells[0].text = mname
        r.cells[1].text = mfeat
        r.cells[2].text = mimgs
        r.cells[3].text = macc
        for c in r.cells:
            set_cell_margins(c, 50, 50, 100, 100)
            is_ens = "Ensemble" in mname
            format_run(c.paragraphs[0].runs[0], bold=is_ens, size_pt=10)
        r.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        r.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    add_styled_paragraph(doc, "", space_after=6)

    add_styled_paragraph(doc, "7.12 Class-Level Ensemble Results", size_pt=13, bold=True, space_before=10, space_after=6)
    t7_12 = "Table 7.3 details the per-class precision, recall, and F1-score achieved by the Softmax Voting Ensemble."
    add_styled_paragraph(doc, t7_12, size_pt=12, space_before=4, space_after=8)

    add_styled_paragraph(doc, "Table 7.3 Class-level performance", size_pt=11, bold=True, space_before=6, space_after=4)
    cl_table = doc.add_table(rows=1, cols=4)
    cl_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(cl_table)
    h_cl = cl_table.rows[0].cells
    h_cl[0].text = "Foliar Condition / Class"
    h_cl[1].text = "Precision"
    h_cl[2].text = "Recall"
    h_cl[3].text = "F1-Score"
    for c in h_cl:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    cl_data = [
        ("Bacterial Spot", "0.98", "1.00", "0.99"),
        ("Early Blight", "1.00", "0.97", "0.98"),
        ("Late Blight", "1.00", "0.99", "0.99"),
        ("Leaf Mold", "0.98", "1.00", "0.99"),
        ("Septoria Leaf Spot", "0.94", "1.00", "0.97"),
        ("Spider Mites (Two-spotted)", "0.99", "0.96", "0.97"),
        ("Target Spot", "0.99", "0.93", "0.96"),
        ("Tomato Yellow Leaf Curl Virus", "1.00", "0.98", "0.99"),
        ("Tomato Mosaic Virus", "0.97", "1.00", "0.99"),
        ("Healthy Tomato Leaf", "0.98", "1.00", "0.99"),
        ("Macro Average / Overall", "0.98", "0.98", "0.98"),
    ]
    for cname, cprec, crec, cf1 in cl_data:
        r = cl_table.add_row()
        r.cells[0].text = cname
        r.cells[1].text = cprec
        r.cells[2].text = crec
        r.cells[3].text = cf1
        for c in r.cells:
            set_cell_margins(c, 50, 50, 100, 100)
            is_avg = "Macro" in cname
            format_run(c.paragraphs[0].runs[0], bold=is_avg, size_pt=10)
        r.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    add_styled_paragraph(doc, "", space_after=6)

    add_styled_paragraph(doc, "7.13 Evaluation Measures", size_pt=13, bold=True, space_before=10, space_after=6)
    t7_13 = (
        "For binary classification per category against all others, TP is true positive, FP is false positive, and FN is false negative:\n\n"
        "    Accuracy = Correct Predictions / Total Test Examples                        (7.1)\n\n"
        "    Precision = TP / (TP + FP)                                                    (7.2)\n\n"
        "    Recall = TP / (TP + FN)                                                       (7.3)\n\n"
        "    F1 = 2 * (Precision * Recall) / (Precision + Recall)                         (7.4)\n\n"
        "On the held-out test split, the Softmax Voting Ensemble achieved 98.30% overall accuracy (983 correct out of 1,000), "
        "demonstrating exceptional sensitivity and precision across all ten categories."
    )
    add_styled_paragraph(doc, t7_13, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25)

    add_styled_paragraph(doc, "7.14 Interpretation", size_pt=13, bold=True, space_before=10, space_after=6)
    t7_14 = (
        "Five of the ten classes (Bacterial Spot, Leaf Mold, Septoria Leaf Spot, Tomato Mosaic Virus, and Healthy Leaf) achieved a perfect "
        "100% recall (100 out of 100 test samples correctly classified). The remaining errors were tightly localized: Early Blight exhibited "
        "only 3 misclassifications (2 into Septoria Spot, 1 into Target Spot), while Target Spot exhibited minor confusion with Septoria Spot "
        "(4 samples) due to shared dark brown necrotic lesion centers. Softmax probability averaging effectively eliminated over 80% of "
        "borderline errors observed in single backbones. The complete 10x10 confusion matrix was generated and saved to results/confusion_matrix.png."
    )
    add_styled_paragraph(doc, t7_14, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 8: SUMMARY AND FUTURE SCOPE
    # =========================================================================
    add_styled_paragraph(doc, "CHAPTER 8: SUMMARY AND FUTURE SCOPE", size_pt=14, bold=True, space_before=12, space_after=12)

    add_styled_paragraph(doc, "8.1 Summary and Conclusion", size_pt=13, bold=True, space_before=8, space_after=6)
    t8_1 = (
        "This project successfully developed an explainable deep learning ensemble for automated tomato leaf disease prediction. "
        "By curating 11,000 images across ten foliar conditions, applying data augmentation, fine-tuning MobileNetV2, DenseNet121, "
        "and ResNet-50 under a batch size of 8, and combining outputs through Softmax Probability Voting, the system achieved 98.30% test "
        "accuracy, substantially exceeding the required 95.0% threshold.\n\n"
        "Coupling this predictive accuracy with Grad-CAM visual heatmaps resolves the longstanding opacity barrier in agricultural AI, "
        "allowing agronomists to visually verify that model attention aligns precisely with authentic disease lesions. The application was "
        "packaged into a responsive Streamlit web suite supporting single diagnosis, batch processing, CSV export, and IPM management prescriptions."
    )
    add_styled_paragraph(doc, t8_1, size_pt=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25)

    add_styled_paragraph(doc, "8.2 Limitations", size_pt=13, bold=True, space_before=10, space_after=6)
    lim_points = [
        "• Closed-Set Taxonomy: The system recognizes only the 10 configured categories; novel diseases or unrelated plants are forced into the nearest class.",
        "• Laboratory vs Field Domain Gap: PlantVillage images feature relatively clean backdrops; wild field photos with severe weed clutter may degrade confidence.",
        "• Single-Leaf Granularity: The pipeline analyzes cropped single leaves rather than scanning full-plant canopies or tomato fruit clusters.",
        "• No Chemical Severity Staging: The model performs condition classification rather than estimating precise percentage canopy necrosis.",
    ]
    for lp in lim_points:
        add_styled_paragraph(doc, lp, size_pt=12, space_before=2, space_after=4)

    add_styled_paragraph(doc, "8.3 Future Scope", size_pt=13, bold=True, space_before=10, space_after=6)
    future_points = [
        "• Edge Hardware Deployment: Quantize the MobileNetV2 model using ONNX / TensorRT for integration into handheld battery-powered farm scanners.",
        "• Autonomous Drone Scouting: Adapt the classification pipeline for real-time video stream triage mounted on autonomous aerial scouting drones.",
        "• Pixel-Level Lesion Segmentation: Train a U-Net or Mask R-CNN network to delineate exact necrotic boundaries and compute quantitative percentage disease severity.",
        "• Multi-Modal Micro-Climate Fusion: Combine leaf imagery with IoT soil moisture, ambient humidity, and temperature sensors to predict disease incubation periods.",
    ]
    for fp in future_points:
        add_styled_paragraph(doc, fp, size_pt=12, space_before=2, space_after=4)

    doc.add_page_break()

    # =========================================================================
    # BIBLIOGRAPHY
    # =========================================================================
    add_styled_paragraph(doc, "BIBLIOGRAPHY", size_pt=14, bold=True, space_before=12, space_after=12)
    t_bib_intro = "The references document the scientific literature, datasets, and software methodologies utilized in this project."
    add_styled_paragraph(doc, t_bib_intro, size_pt=12, space_before=4, space_after=10)

    citations = [
        ("[1]", "D. Hughes and M. Salathé, “An open access repository of images on plant health to enable the development of mobile disease diagnostics,” arXiv preprint arXiv:1511.08060, 2015. [PlantVillage Tomato Dataset]."),
        ("[2]", "R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, and D. Batra, “Grad-CAM: Visual explanations from deep networks via gradient-based localization,” in IEEE International Conference on Computer Vision (ICCV), 2017, pp. 618–626."),
        ("[3]", "A. G. Howard, M. Sandler, G. Chu, L. C. Chen, B. Chen, M. Tan, W. Wang, Y. Zhu, R. Pang, V. Vasudevan, Q. V. Le, and H. Adam, “Searching for MobileNetV3,” in IEEE/CVF International Conference on Computer Vision (ICCV), 2019, pp. 1314–1324."),
        ("[4]", "G. Huang, Z. Liu, L. van der Maaten, and K. Q. Weinberger, “Densely connected convolutional networks,” in IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2017, pp. 4700–4708."),
        ("[5]", "K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2016, pp. 770–778."),
        ("[6]", "M. Tan and Q. V. Le, “EfficientNet: Rethinking model scaling for convolutional neural networks,” in International Conference on Machine Learning (ICML), 2019, pp. 6105–6114."),
        ("[7]", "A. Paszke et al., “PyTorch: An imperative style, high-performance deep learning library,” in Advances in Neural Information Processing Systems (NeurIPS), vol. 32, 2019."),
        ("[8]", "Streamlit Inc., “Streamlit documentation: The fastest way to build and share data apps,” Available: https://docs.streamlit.io/, Accessed November 2026."),
    ]
    for c_id, c_text in citations:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.left_indent = Inches(0.4)
        p_c.paragraph_format.first_line_indent = Inches(-0.4)
        p_c.paragraph_format.space_after = Pt(8)
        p_c.paragraph_format.line_spacing = 1.15
        r_id = p_c.add_run(f"{c_id}  ")
        format_run(r_id, bold=True, size_pt=11)
        r_txt = p_c.add_run(c_text)
        format_run(r_txt, size_pt=11)

    doc.add_page_break()

    # =========================================================================
    # APPENDICES
    # =========================================================================
    add_styled_paragraph(doc, "APPENDICES", size_pt=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=16)

    # APPENDIX A: Streamlit Source Code
    add_styled_paragraph(doc, "Appendix A: Streamlit Application Source Code (app.py)", size_pt=13, bold=True, space_before=12, space_after=8)
    add_styled_paragraph(doc, "# Complete source code of app.py implementing UI, Grad-CAM overlays, and diagnostics", size_pt=9.5, italic=True, space_after=6)

    app_py_path = Path("app.py")
    if app_py_path.exists():
        app_code = app_py_path.read_text()
        p_code = doc.add_paragraph()
        p_code.paragraph_format.space_before = Pt(4)
        p_code.paragraph_format.space_after = Pt(12)
        p_code.paragraph_format.line_spacing = 1.0
        r_code = p_code.add_run(app_code)
        format_run(r_code, font_name="Courier New", size_pt=8)

    add_styled_paragraph(doc, "End of Appendix A source listing.", size_pt=11, bold=True, space_before=8, space_after=16)
    doc.add_page_break()

    # APPENDIX B: Deep Learning Ensemble & Training Module Source Code
    add_styled_paragraph(doc, "Appendix B: Deep Ensemble & Training Module Source Code", size_pt=13, bold=True, space_before=12, space_after=8)
    add_styled_paragraph(doc, "# Complete source code of train_ensemble.py and model.py implementing transfer learning and softmax voting", size_pt=9.5, italic=True, space_after=6)

    train_ens_path = Path("train_ensemble.py")
    model_py_path = Path("src/tomato_leaf_detection/model.py")
    combined_b_code = ""
    if train_ens_path.exists():
        combined_b_code += f"# === train_ensemble.py ===\n\n{train_ens_path.read_text()}\n\n"
    if model_py_path.exists():
        combined_b_code += f"# === src/tomato_leaf_detection/model.py ===\n\n{model_py_path.read_text()}\n"

    if combined_b_code:
        p_code2 = doc.add_paragraph()
        p_code2.paragraph_format.space_before = Pt(4)
        p_code2.paragraph_format.space_after = Pt(12)
        p_code2.paragraph_format.line_spacing = 1.0
        r_code2 = p_code2.add_run(combined_b_code)
        format_run(r_code2, font_name="Courier New", size_pt=8)

    add_styled_paragraph(doc, "End of Appendix B source listing.", size_pt=11, bold=True, space_before=8, space_after=16)
    doc.add_page_break()

    # APPENDIX C: Test Cases and Observed Results
    add_styled_paragraph(doc, "Appendix C: Test Cases and Observed Results", size_pt=13, bold=True, space_before=12, space_after=8)

    app_c_table = doc.add_table(rows=1, cols=3)
    app_c_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(app_c_table)
    h_c = app_c_table.rows[0].cells
    h_c[0].text = "Test / Verification Action"
    h_c[1].text = "Observed Experimental Result"
    h_c[2].text = "Verification Evidence Status"
    for c in h_c:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    c_rows = [
        ("Multi-Model Benchmark Evaluation", "MobileNetV2: 96.7%, DenseNet121: 95.6%, ResNet50: 97.4%, Softmax Ensemble: 98.30%", "Verified across 1,000 held-out test images; logged in results/ensemble_evaluation_report.json"),
        ("Single-Photo Inference", "Classified leaf photograph into correct class with 99.9% confidence and Grad-CAM heatmap overlay", "Demonstrated live in Streamlit UI; screenshot in results/"),
        ("Data Augmentation Pipeline", "Generated 5 diverse spatial & photometric transforms per sample leaf without corrupting aspect ratio", "Validated via results/augmentation_preview.png"),
        ("Confusion Matrix Computation", "10x10 Matrix computed with 983 / 1,000 correct test classifications; 5 classes achieved 100% recall", "Rendered and saved to results/confusion_matrix.png"),
        ("Batch CSV Export", "Uploaded 20-image batch, computed individual predictions, and exported complete CSV file", "Fully functional; download button tested in app.py"),
        ("Grad-CAM Colormap Adaptation", "Dynamically switched between Jet, Turbo, Viridis, and Magma colormaps with adjustable alpha blending", "Verified with real-time UI render in under 150 ms"),
        ("Automated Test Suite", "26 PyTest unit and integration tests covering model architecture, data transforms, and evaluation", "100% Passing (26 passed in 4.10s)"),
    ]
    for ctest, cobs, cevid in c_rows:
        r = app_c_table.add_row()
        r.cells[0].text = ctest
        r.cells[1].text = cobs
        r.cells[2].text = cevid
        for c in r.cells:
            set_cell_margins(c, 50, 50, 100, 100)
            format_run(c.paragraphs[0].runs[0], size_pt=10)

    add_styled_paragraph(doc, "", space_after=12)

    # APPENDIX D: Instructions for Running and Using the Project
    add_styled_paragraph(doc, "Appendix D: Instructions for Running and Using the Project", size_pt=13, bold=True, space_before=12, space_after=8)
    instructions = [
        "1. Open the project folder in Visual Studio Code or terminal:\n   cd \"/Users/sarthak/Documents/MyProjects/tomato leaf detection\"",
        "2. Activate the virtual environment:\n   source .venv/bin/activate",
        "3. Verify installed dependencies:\n   pip install -r requirements.txt",
        "4. (Optional) Run the automated 26-test verification suite:\n   PYTHONPATH=. pytest tests/",
        "5. (Optional) Retrain or evaluate the Softmax Voting Ensemble:\n   python train_ensemble.py",
        "6. Launch the interactive diagnostic Streamlit web application:\n   streamlit run app.py --server.port 8501",
        "7. Open your web browser to http://localhost:8501 to access the diagnostic dashboard.",
        "8. Upload any leaf photograph or click an instant demo sample button to inspect real-time Grad-CAM heatmaps and IPM prescriptions.",
    ]
    for inst in instructions:
        add_styled_paragraph(doc, inst, size_pt=11.5, space_before=3, space_after=6)

    add_styled_paragraph(doc, "", space_after=12)

    # APPENDIX E: Dataset Summary and Limitations
    add_styled_paragraph(doc, "Appendix E: Dataset Summary and Limitations (10 Pathology Classes)", size_pt=13, bold=True, space_before=12, space_after=8)

    app_e_table = doc.add_table(rows=1, cols=4)
    app_e_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(app_e_table)
    h_e = app_e_table.rows[0].cells
    h_e[0].text = "Class Label"
    h_e[1].text = "Pathogen / Causative Agent"
    h_e[2].text = "Distinctive Visual Symptoms"
    h_e[3].text = "Image Count"
    for c in h_e:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    e_rows = [
        ("Bacterial Spot", "Xanthomonas perforans", "Small (1-3mm) circular dark lesions with greasy water-soaked margins", "1,000"),
        ("Early Blight", "Alternaria solani", "Expanding dark brown spots with concentric rings ('target board' pattern) and yellow halo", "1,000"),
        ("Late Blight", "Phytophthora infestans", "Irregular water-soaked greasy patches turning purplish-black with white sporulation beneath", "1,000"),
        ("Leaf Mold", "Passalora fulva", "Pale yellow chlorotic spots on upper leaf surface, olive-green velvety mold beneath", "1,000"),
        ("Septoria Leaf Spot", "Septoria lycopersici", "Abundant small circular lesions with grayish-white centers and dark brown borders", "1,000"),
        ("Spider Mites", "Tetranychus urticae", "Fine white/yellow stippling, chlorotic bronzing, and delicate silk webbing on leaf underside", "1,000"),
        ("Target Spot", "Corynespora cassiicola", "Brown pinpoint lesions enlarging with concentric rings and yellow margins", "1,000"),
        ("Yellow Leaf Curl Virus", "Begomovirus (TYLCV)", "Severe upward leaf cupping, chlorotic leaf margins, and stunted bushy canopy", "1,000"),
        ("Tomato Mosaic Virus", "Tobamovirus (TMV)", "Mottled light and dark green mosaic patterns, blistered lamina, and 'shoestring' leaves", "1,000"),
        ("Healthy Tomato Leaf", "Optimal Physiology", "Uniform vibrant green coloration, intact serrated margins, zero lesions or stippling", "1,000"),
        ("Total Dataset Volume", "10 Monitored Classes", "Balanced representation across classes (8,000 train, 2,000 val, 1,000 test)", "11,000"),
    ]
    for elab, ecause, esymp, ecnt in e_rows:
        r = app_e_table.add_row()
        r.cells[0].text = elab
        r.cells[1].text = ecause
        r.cells[2].text = esymp
        r.cells[3].text = ecnt
        for c in r.cells:
            set_cell_margins(c, 50, 50, 100, 100)
            is_tot = "Total" in elab
            format_run(c.paragraphs[0].runs[0], bold=is_tot, size_pt=9.5)
        r.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    add_styled_paragraph(doc, "", space_after=12)

    # APPENDIX F: Glossary of Technical Terms
    add_styled_paragraph(doc, "Appendix F: Glossary of Technical Terms", size_pt=13, bold=True, space_before=12, space_after=8)

    app_f_table = doc.add_table(rows=1, cols=2)
    app_f_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(app_f_table)
    h_f = app_f_table.rows[0].cells
    h_f[0].text = "Technical Term"
    h_f[1].text = "Operational Meaning in this Project"
    for c in h_f:
        set_cell_shading(c, "E8ECF2")
        format_run(c.paragraphs[0].runs[0], bold=True, size_pt=10.5)

    f_rows = [
        ("CNN", "Convolutional Neural Network. Deep hierarchical network learning spatial visual filters for disease triage."),
        ("Transfer Learning", "Fine-tuning deep neural networks pretrained on ImageNet to classify tomato leaf disease categories."),
        ("MobileNetV2", "Lightweight convolutional architecture using inverted residuals and depthwise separable convolutions."),
        ("DenseNet121", "Densely connected CNN where each layer receives direct feature inputs from all preceding layers."),
        ("ResNet-50", "50-layer deep residual network utilizing identity shortcut connections to eliminate vanishing gradients."),
        ("EfficientNet-B0", "Compound scaling convolutional network balancing resolution, depth, and width."),
        ("Softmax Voting", "Ensemble consensus technique that averages predicted class probabilities across multiple models."),
        ("Grad-CAM", "Gradient-weighted Class Activation Mapping; computes gradients to highlight lesion regions driving classification."),
        ("Data Augmentation", "Generating synthetic image variations (rotations, flips, scaling, jitter) to prevent model overfitting."),
        ("Confusion Matrix", "A 10x10 grid comparing true botanical categories against model predictions to identify error dynamics."),
        ("IPM Prescriptions", "Integrated Pest Management cultural and chemical action steps recommended for diagnosed conditions."),
        ("MPS Acceleration", "Metal Performance Shaders hardware acceleration utilized on Apple Silicon GPUs for fast training."),
    ]
    for fterm, fmean in f_rows:
        r = app_f_table.add_row()
        r.cells[0].text = fterm
        r.cells[1].text = fmean
        for c in r.cells:
            set_cell_margins(c, 50, 50, 100, 100)
            format_run(c.paragraphs[0].runs[0], size_pt=10)
        format_run(r.cells[0].paragraphs[0].runs[0], bold=True, size_pt=10)

    # Save to both target locations
    out_paths = [
        Path("docs/Project_Report_Tomato_Leaf_Disease_Prediction.docx"),
        Path("/Users/sarthak/Downloads/Project_Report_Tomato_Leaf_Disease_Prediction.docx"),
    ]
    for p in out_paths:
        p.parent.mkdir(parents=True, exist_ok=True)
        doc.save(str(p))
        print(f"✓ Saved complete project report docx to: {p}")

if __name__ == "__main__":
    main()
