"""Generate the PDF version of the Graphic Era BCA Major Project Report:
'Tomato Leaf Disease Prediction Using Machine Learning'
Under the Guidance of: Mr. Abhishek Thapa (Assistant Professor)
Matching the exact structural template and academic layout of the demo report.
"""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage, KeepTogether, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and display running page numbers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Only print page numbers starting from page 6 (Chapter 1)
        if self._pageNumber >= 6:
            self.setFont("Times-Roman", 10)
            self.drawCentredString(A4[0] / 2.0, 36, str(self._pageNumber))

def build_pdf(out_path):
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=65,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    style_cover_heading = ParagraphStyle(
        'CoverHeading',
        fontName='Times-Bold',
        fontSize=15,
        leading=20,
        alignment=1, # Center
        spaceAfter=15,
    )
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Times-Bold',
        fontSize=19,
        leading=25,
        alignment=1,
        spaceAfter=20,
    )
    style_cover_sub = ParagraphStyle(
        'CoverSub',
        fontName='Times-Roman',
        fontSize=11.5,
        leading=16,
        alignment=1,
        spaceAfter=12,
    )
    style_cover_bold = ParagraphStyle(
        'CoverBold',
        fontName='Times-Bold',
        fontSize=12,
        leading=17,
        alignment=1,
        spaceAfter=14,
    )
    style_h1 = ParagraphStyle(
        'ChapterHeading',
        fontName='Times-Bold',
        fontSize=13.5,
        leading=18,
        spaceBefore=14,
        spaceAfter=10,
    )
    style_h2 = ParagraphStyle(
        'SectionHeading',
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        spaceBefore=10,
        spaceAfter=6,
    )
    style_body = ParagraphStyle(
        'Body',
        fontName='Times-Roman',
        fontSize=10.5,
        leading=14.5,
        spaceAfter=8,
        alignment=4, # Justify
    )
    style_body_left = ParagraphStyle(
        'BodyLeft',
        fontName='Times-Roman',
        fontSize=10.5,
        leading=14.5,
        spaceAfter=4,
        alignment=0,
    )
    style_table_caption = ParagraphStyle(
        'TableCaption',
        fontName='Times-Bold',
        fontSize=10,
        leading=14,
        spaceBefore=6,
        spaceAfter=4,
    )
    style_table_header = ParagraphStyle(
        'TableHeader',
        fontName='Times-Bold',
        fontSize=9.5,
        leading=13,
        alignment=1,
    )
    style_table_cell = ParagraphStyle(
        'TableCell',
        fontName='Times-Roman',
        fontSize=9,
        leading=12.5,
    )
    style_table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Times-Bold',
        fontSize=9,
        leading=12.5,
    )
    style_code = ParagraphStyle(
        'CodeSnippet',
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        spaceAfter=6,
    )

    story = []

    # =========================================================================
    # 1. COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("PROJECT REPORT ON", style_cover_heading))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Tomato Leaf Disease Prediction Using Machine Learning", style_cover_title))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Submitted to<br/>Department of Computer Applications in fulfilment for the award of the degree of", style_cover_sub))
    story.append(Spacer(1, 6))
    story.append(Paragraph("BACHELOR OF COMPUTER APPLICATIONS<br/>Batch (2024-2027)", style_cover_bold))
    story.append(Spacer(1, 25))
    story.append(Paragraph("Submitted by", style_cover_sub))
    story.append(Spacer(1, 4))
    story.append(Paragraph("SARTHAK NEGI<br/>24151534", style_cover_bold))
    story.append(Spacer(1, 25))
    story.append(Paragraph("Under the Guidance of", style_cover_sub))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Mr. Abhishek Thapa<br/><i>(Assistant Professor)</i>", style_cover_bold))
    story.append(Spacer(1, 60))

    story.append(Paragraph("GRAPHIC ERA DEEMED TO BE UNIVERSITY DEHRADUN<br/>November 2026", style_cover_bold))
    story.append(PageBreak())

    # =========================================================================
    # 2. CANDIDATE'S DECLARATION
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("CANDIDATE’S DECLARATION", style_cover_heading))
    story.append(Spacer(1, 15))
    decl_text = (
        "I, Sarthak Negi, hereby declare that the report entitled "
        "“Tomato Leaf Disease Prediction Using Machine Learning” in complete fulfilment of the requirements for "
        "the award of the degree of Bachelor of Computer Applications is a bonafide work carried out by me during "
        "the period of August 2026 to November 2026 under the supervision of Mr. Abhishek Thapa, Assistant Professor, "
        "Department of Computer Applications, Graphic Era Deemed to be University, Dehradun, India.<br/><br/>"
        "This work has not been submitted elsewhere for the award of a degree/diploma/certificate."
    )
    story.append(Paragraph(decl_text, style_body))
    story.append(Spacer(1, 25))
    story.append(Paragraph("<b>Sarthak Negi<br/>(24151534)</b>", ParagraphStyle('DeclSig', fontName='Times-Bold', fontSize=11, alignment=2)))
    story.append(Spacer(1, 30))
    cert_decl = "This is to certify that the above mentioned statement in the candidate’s declaration is correct to the best of my knowledge."
    story.append(Paragraph(cert_decl, style_body))
    story.append(Spacer(1, 35))
    story.append(Paragraph("<b>Date: ____________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Name and Signature of Guide</b>", style_body_left))
    story.append(Spacer(1, 40))
    story.append(Paragraph("<b>Signature of Supervisor &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Signature of External Examiner</b>", style_body_left))
    story.append(Spacer(1, 25))
    story.append(Paragraph("<b>HOD</b>", ParagraphStyle('HOD', fontName='Times-Bold', fontSize=11, alignment=1)))
    story.append(PageBreak())

    # =========================================================================
    # 3. ACKNOWLEDGEMENT
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("Acknowledgement", style_cover_heading))
    story.append(Spacer(1, 15))
    ack_text = (
        "First of all, my sincere and wholehearted gratitude to my loved ones who supported me during the making of this project. "
        "The success and final outcome of this project required a lot of guidance and assistance from many people, and I am extremely "
        "privileged to have had this support all along the completion of my project. All that I have achieved is through their supervision "
        "and guidance and I would not forget to thank them.<br/><br/>"
        "I respect and thank <b>Mr. Abhishek Thapa</b>, Assistant Professor, Department of Computer Applications, for providing me an "
        "opportunity to do the project work in <b>“Tomato Leaf Disease Prediction Using Machine Learning”</b> and giving me his support "
        "and guidance, which made me complete the project duly. I am extremely thankful to him for providing such rich technical support "
        "and mentorship, even though he had a busy schedule managing academic affairs.<br/><br/>"
        "I am thankful to and fortunate enough to get constant encouragement, support, and guidance from all teaching and technical staff "
        "of the Department of Computer Applications and Graphic Era Deemed to be University, which helped me in successfully completing my project work."
    )
    story.append(Paragraph(ack_text, style_body))
    story.append(Spacer(1, 45))
    story.append(Paragraph("<b>Sarthak Negi<br/>(24151534)</b>", ParagraphStyle('AckSig', fontName='Times-Bold', fontSize=11, alignment=2)))
    story.append(PageBreak())

    # =========================================================================
    # 4. CERTIFICATE OF ORIGINALITY
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("CERTIFICATE OF ORIGINALITY", style_cover_heading))
    story.append(Spacer(1, 15))
    orig_text = (
        "This is to certify that the project report titled <b>“Tomato Leaf Disease Prediction Using Machine Learning”</b> "
        "submitted to <b>Graphic Era (Deemed to be University), Dehradun</b> in fulfilment of the requirement for the award of the degree "
        "of <b>BACHELOR OF COMPUTER APPLICATIONS (BCA)</b>, is an authentic and original work carried out by <b>Mr. Sarthak Negi</b> with "
        "enrollment number <b>24151534</b> under my supervision and guidance.<br/><br/>"
        "The matter embodied in this project is genuine work done by the student and has not been submitted whether to this University "
        "or to any other University / Institute for the fulfilment of the requirements of any course of study."
    )
    story.append(Paragraph(orig_text, style_body))
    story.append(Spacer(1, 35))
    story.append(Paragraph("<b>Signature of the Student: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Signature of the Guide:</b><br/>"
                           "Date: …………………. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Date: ………………….", style_body_left))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Enrolment No.: 24151534</b>", style_body_left))
    story.append(Spacer(1, 25))
    story.append(Paragraph("<b>Name and Address of Guide:</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Name and Designation of Supervisor:</b><br/>"
                           "Mr. Abhishek Thapa &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Assistant Professor<br/>"
                           "Department of Computer Applications &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Department of Computer Applications<br/>"
                           "Graphic Era Deemed to be University &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Graphic Era Deemed to be University", style_body_left))
    story.append(PageBreak())

    # =========================================================================
    # 5. TABLE OF CONTENTS
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("TABLE OF CONTENTS", style_cover_heading))
    story.append(Spacer(1, 10))

    toc_data = [
        [Paragraph("<b>Sr. No.</b>", style_table_header), Paragraph("<b>Chapter / Section</b>", style_table_header), Paragraph("<b>Page No.</b>", style_table_header)],
        [Paragraph("1", style_table_cell_bold), Paragraph("CHAPTER 1: INTRODUCTION", style_table_cell_bold), Paragraph("[6-10]", style_table_cell_bold)],
        [Paragraph("2", style_table_cell_bold), Paragraph("CHAPTER 2: SYSTEM ANALYSIS AND REQUIREMENTS SPECIFICATIONS", style_table_cell_bold), Paragraph("[11-17]", style_table_cell_bold)],
        [Paragraph("3", style_table_cell_bold), Paragraph("CHAPTER 3: SYSTEM DESIGN", style_table_cell_bold), Paragraph("[18-21]", style_table_cell_bold)],
        [Paragraph("4", style_table_cell_bold), Paragraph("CHAPTER 4: PROJECT MANAGEMENT", style_table_cell_bold), Paragraph("[22-24]", style_table_cell_bold)],
        [Paragraph("5", style_table_cell_bold), Paragraph("CHAPTER 5: INPUT DESIGN", style_table_cell_bold), Paragraph("[25]", style_table_cell_bold)],
        [Paragraph("6", style_table_cell_bold), Paragraph("CHAPTER 6: OUTPUT DESIGN", style_table_cell_bold), Paragraph("[26-27]", style_table_cell_bold)],
        [Paragraph("7", style_table_cell_bold), Paragraph("CHAPTER 7: SYSTEM TESTING IMPLEMENTATION AND MAINTENANCE", style_table_cell_bold), Paragraph("[28-36]", style_table_cell_bold)],
        [Paragraph("8", style_table_cell_bold), Paragraph("CHAPTER 8: SUMMARY AND FUTURE SCOPE", style_table_cell_bold), Paragraph("[37-38]", style_table_cell_bold)],
        [Paragraph("9", style_table_cell_bold), Paragraph("BIBLIOGRAPHY", style_table_cell_bold), Paragraph("[39]", style_table_cell_bold)],
        [Paragraph("10", style_table_cell_bold), Paragraph("APPENDICES", style_table_cell_bold), Paragraph("[40-65]", style_table_cell_bold)],
        [Paragraph("A.", style_table_cell), Paragraph("Streamlit Application Source Code (app.py)", style_table_cell), Paragraph("[40-53]", style_table_cell)],
        [Paragraph("B.", style_table_cell), Paragraph("Deep Ensemble & Training Module Source Code", style_table_cell), Paragraph("[54-61]", style_table_cell)],
        [Paragraph("C.", style_table_cell), Paragraph("Test Cases and Observed Results", style_table_cell), Paragraph("[62]", style_table_cell)],
        [Paragraph("D.", style_table_cell), Paragraph("Instructions for Running and Using the Project", style_table_cell), Paragraph("[63]", style_table_cell)],
        [Paragraph("E.", style_table_cell), Paragraph("Dataset Summary and Limitations (10 Pathology Classes)", style_table_cell), Paragraph("[64]", style_table_cell)],
        [Paragraph("F.", style_table_cell), Paragraph("Glossary of Technical Terms", style_table_cell), Paragraph("[65]", style_table_cell)],
    ]
    t_toc = Table(toc_data, colWidths=[55, 345, 75])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 1: INTRODUCTION (Page 6)
    # =========================================================================
    story.append(Paragraph("CHAPTER 1: INTRODUCTION", style_h1))
    story.append(Paragraph("1.1 Introduction", style_h2))
    intro_p1 = (
        "Tomato (<i>Solanum lycopersicum</i>) is an indispensable agricultural food crop cultivated across millions of hectares worldwide. "
        "Foliar diseases represent a catastrophic impediment to crop yield, quality, and economic security for farmers. Identifying a specific "
        "disease from a leaf photograph is exceptionally difficult when visual symptoms overlap—such as the concentric necrotic rings of "
        "Early Blight and Target Spot—or when ambient lighting, shadows, and camera resolutions vary. This project demonstrates supervised "
        "deep learning and transfer learning for classifying tomato-leaf images into ten distinct categories learned from an empirical dataset.<br/><br/>"
        "The application accepts JPG or PNG photographs and predicts one of ten classes (nine destructive pathologies and healthy foliage). "
        "Rather than relying on an isolated model, the primary predictive engine is an ensemble combining three deep convolutional architectures: "
        "MobileNetV2, DenseNet121, and ResNet-50. Their individual predictions are combined using Softmax Probability Averaging (Softmax Voting). "
        "A baseline EfficientNet-B0 model provides a standalone benchmark. The system predicts condition categories for static photographs; "
        "it does not forecast spatial disease spread over time.<br/><br/>"
        "A photograph-based classifier supports the crucial primary triage stage of visual crop monitoring. In supervised learning, each training "
        "photograph is paired with a verified category label. The convolutional backbones extract multi-scale spatial patterns that distinguish "
        "those categories, then apply the learned decision boundary to unseen test images. The model therefore answers a bounded question "
        "regarding visual similarity to those labels; it does not replace in-vitro laboratory culturing of pathogens.<br/><br/>"
        "The application brings this learning workflow into an interactive, browser-based diagnostic system built on Streamlit. Users can inspect "
        "dataset metrics, compare architectural latency and parameter footprints, upload leaf photos, inspect predicted probabilities, and "
        "verify model reasoning through Gradient-weighted Class Activation Mapping (Grad-CAM) visual attention heatmaps."
    )
    story.append(Paragraph(intro_p1, style_body))

    story.append(Paragraph("1.2 Background", style_h2))
    bg_p = (
        "Image classification maps an arbitrary photograph to a label from a defined taxonomy. Transfer learning reuses image representations "
        "learned by deep networks pretrained on large-scale benchmarks such as ImageNet; custom classification heads learn project-specific "
        "labels. The local dataset contains 11,000 examples in ten balanced folders, including augmented variations."
    )
    story.append(Paragraph(bg_p, style_body))

    story.append(Paragraph("Table 1.1 Tomato-leaf image categories in the local dataset", style_table_caption))
    t1_rows = [
        [Paragraph("<b>Category</b>", style_table_header), Paragraph("<b>Pathogen / Class Type</b>", style_table_header), Paragraph("<b>Images</b>", style_table_header)],
        [Paragraph("Bacterial Leaf Spot", style_table_cell), Paragraph("<i>Xanthomonas perforans</i> (Bacterium)", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Early Blight", style_table_cell), Paragraph("<i>Alternaria solani</i> (Fungus)", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Late Blight", style_table_cell), Paragraph("<i>Phytophthora infestans</i> (Oomycete)", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Leaf Mold", style_table_cell), Paragraph("<i>Passalora fulva</i> (Fungus)", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Septoria Leaf Spot", style_table_cell), Paragraph("<i>Septoria lycopersici</i> (Fungus)", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Spider Mites (Two-spotted)", style_table_cell), Paragraph("<i>Tetranychus urticae</i> (Arachnid)", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Target Spot", style_table_cell), Paragraph("<i>Corynespora cassiicola</i> (Fungus)", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Tomato Yellow Leaf Curl Virus", style_table_cell), Paragraph("Begomovirus (Whitefly-vectored TYLCV)", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Tomato Mosaic Virus", style_table_cell), Paragraph("Tobamovirus (Mechanically vectored TMV)", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Healthy Tomato Leaf", style_table_cell), Paragraph("Optimal Solanaceae foliage (Control)", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("<b>Total Images</b>", style_table_cell_bold), Paragraph("<b>10 Monitored Categories</b>", style_table_cell_bold), Paragraph("<b>11,000</b>", style_table_cell_bold)],
    ]
    t1 = Table(t1_rows, colWidths=[150, 245, 80])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ALIGN', (2,1), (2,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t1)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1.3 Problem Statement", style_h2))
    ps_text = (
        "The specific problem is to assign a tomato-leaf photograph to one of the ten known dataset classes in a consistent and repeatable "
        "manner. Manual visual inspection can be affected by image quality, lighting, viewing angle, and differences between human observers. "
        "A computer vision model applies the same learned decision rule to every uploaded image, mitigating subjective observer bias.<br/><br/>"
        "The project operates as a closed-set classifier: it predicts strictly among the ten learned dataset categories. It does not diagnose "
        "diseases absent from the training taxonomy, estimate exact percentage canopy defoliation, or replace registered agricultural agronomists."
    )
    story.append(Paragraph(ps_text, style_body))

    story.append(Paragraph("1.4 Motivation and Rationale", style_h2))
    mr_text = (
        "The project applies modern deep convolutional architectures to agricultural computer vision. It combines labeled data curation, "
        "rigorous data augmentation, 2-stage transfer learning, softmax voting ensembles, and Grad-CAM explainability.<br/><br/>"
        "Growers and agronomists frequently reject opaque 'black-box' deep learning predictions. By pairing high classification accuracy (98.30%) "
        "with Grad-CAM visual attention overlays that highlight genuine necrotic lesion tissue, the application establishes the essential trust "
        "needed to support crop management decisions."
    )
    story.append(Paragraph(mr_text, style_body))

    story.append(Paragraph("1.5 Objectives", style_h2))
    objs = [
        "1. Organize and audit 11,000 tomato-leaf photographs into ten balanced categories.",
        "2. Implement a multi-stage data augmentation pipeline (rotation, flips, scaling, color jitter) to suppress overfitting.",
        "3. Fine-tune three deep backbones (MobileNetV2, DenseNet121, ResNet-50) using batch size 8 on Apple Silicon MPS.",
        "4. Construct a Softmax Probability Voting Ensemble to surpass the 95% accuracy benchmark.",
        "5. Integrate Grad-CAM explainability to generate visual attention overlays matching pathological symptoms.",
        "6. Build a Streamlit web application supporting single-photo diagnosis, batch analysis, and CSV export.",
        "7. Evaluate performance on a 1,000-image held-out test split, reporting precision, recall, F1, and confusion matrix.",
    ]
    for o in objs:
        story.append(Paragraph(o, style_body_left))

    story.append(Spacer(1, 4))
    story.append(Paragraph("1.6 Scope and Limitations", style_h2))
    sc_text = (
        "The system recognizes 10 classes, accepts JPG/PNG photographs, supports batches up to 20, and exports CSV reports. The Grad-CAM map "
        "shows which leaf regions most strongly influenced the classification; it is an explainability feature map, not an annotated segmentation mask."
    )
    story.append(Paragraph(sc_text, style_body))

    story.append(Paragraph("1.7 Report Organization", style_h2))
    ro_text = (
        "Chapters 2–8 describe system analysis, system design, project management, input/output interfaces, implementation and testing, "
        "results, and future scope. Complete bibliography and source code appendices follow the main chapters."
    )
    story.append(Paragraph(ro_text, style_body))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 2: SYSTEM ANALYSIS AND REQUIREMENTS (Page 11)
    # =========================================================================
    story.append(Paragraph("CHAPTER 2: SYSTEM ANALYSIS AND REQUIREMENTS SPECIFICATIONS", style_h1))
    story.append(Paragraph("2.1 Identification of Need", style_h2))
    story.append(Paragraph("Table 2.1 Existing approach and proposed system", style_table_caption))
    t2_rows = [
        [Paragraph("<b>Aspect</b>", style_table_header), Paragraph("<b>Basic Manual Approach</b>", style_table_header), Paragraph("<b>Proposed Deep Ensemble System</b>", style_table_header)],
        [Paragraph("Input", style_table_cell), Paragraph("Visual field inspection", style_table_cell), Paragraph("JPG or PNG digital leaf photo", style_table_cell)],
        [Paragraph("Decision", style_table_cell), Paragraph("Observer subjective judgment", style_table_cell), Paragraph("Softmax Voting Ensemble across 3 CNNs", style_table_cell)],
        [Paragraph("Evaluation", style_table_cell), Paragraph("Often unrecorded / informal", style_table_cell), Paragraph("Held-out test metrics & 10x10 matrix", style_table_cell)],
        [Paragraph("Output", style_table_cell), Paragraph("Informal verbal assessment", style_table_cell), Paragraph("Diagnostic dashboard, CSV & IPM advice", style_table_cell)],
        [Paragraph("Limit", style_table_cell), Paragraph("Fatigue, observer bias", style_table_cell), Paragraph("Ten learned dataset categories", style_table_cell)],
    ]
    t2 = Table(t2_rows, colWidths=[100, 185, 190])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t2)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.2 Preliminary Investigation", style_h2))
    pi_text = (
        "The labeled image directories support supervised computer vision. PyTorch and TorchVision supply pretrained CNN backbones, "
        "while Streamlit provides a responsive browser interface. The 11,000-image dataset provides adequate coverage for transfer learning."
    )
    story.append(Paragraph(pi_text, style_body))

    story.append(Paragraph("2.3 Feasibility Study", style_h2))
    story.append(Paragraph("<b>2.3.1 Technical Feasibility:</b> Python 3.14 with PyTorch and TorchVision runs on standard laptop hardware. "
                           "Apple Silicon MPS acceleration enables 1.5-minute epoch training at batch size 8. Inference latency is < 30 ms on CPU.<br/>"
                           "<b>2.3.2 Operational Feasibility:</b> The interface is operationally simple: upload a photo, review predicted condition, "
                           "and inspect Grad-CAM overlays. No command-line interaction is required from the end user.<br/>"
                           "<b>2.3.3 Economic Feasibility:</b> Developed using open-source libraries and public datasets, incurring zero recurring API "
                           "or hosting costs.", style_body))

    story.append(Paragraph("2.4 Development Approach", style_h2))
    da_text = "Work proceeded iteratively: dataset curation, augmentation design, backbone fine-tuning, ensemble voting integration, and UI deployment."
    story.append(Paragraph(da_text, style_body))

    story.append(Paragraph("2.5 Requirement Specifications", style_h2))
    story.append(Paragraph("Requirements connect project goals to testable criteria verified during automated suite execution.", style_body))

    story.append(Paragraph("2.6 Functional Requirements", style_h2))
    story.append(Paragraph("Table 2.2 Functional requirements", style_table_caption))
    fr_rows = [
        [Paragraph("<b>ID</b>", style_table_header), Paragraph("<b>Requirement</b>", style_table_header), Paragraph("<b>Priority</b>", style_table_header)],
        [Paragraph("FR-01", style_table_cell), Paragraph("Discover 10 class folders and validate image counts.", style_table_cell), Paragraph("High", style_table_cell)],
        [Paragraph("FR-02", style_table_cell), Paragraph("Apply real-time data augmentation (flips, rotation, scaling).", style_table_cell), Paragraph("High", style_table_cell)],
        [Paragraph("FR-03", style_table_cell), Paragraph("Preprocess images into normalized [3, 224, 224] RGB tensors.", style_table_cell), Paragraph("High", style_table_cell)],
        [Paragraph("FR-04", style_table_cell), Paragraph("Fine-tune MobileNetV2, DenseNet121, ResNet-50 with batch size 8.", style_table_cell), Paragraph("High", style_table_cell)],
        [Paragraph("FR-05", style_table_cell), Paragraph("Execute Softmax Probability Voting across the 3 backbones.", style_table_cell), Paragraph("High", style_table_cell)],
        [Paragraph("FR-06", style_table_cell), Paragraph("Generate Grad-CAM heatmaps from the final convolutional layer.", style_table_cell), Paragraph("High", style_table_cell)],
        [Paragraph("FR-07", style_table_cell), Paragraph("Predict single uploaded leaf and show top-3 confidence scores.", style_table_cell), Paragraph("High", style_table_cell)],
        [Paragraph("FR-08", style_table_cell), Paragraph("Support multi-photo batch processing (up to 20) with CSV export.", style_table_cell), Paragraph("Medium", style_table_cell)],
        [Paragraph("FR-09", style_table_cell), Paragraph("Display botanical profile and agronomic IPM action steps.", style_table_cell), Paragraph("Medium", style_table_cell)],
        [Paragraph("FR-10", style_table_cell), Paragraph("Display 10x10 confusion matrix and classification metrics.", style_table_cell), Paragraph("High", style_table_cell)],
    ]
    t_fr = Table(fr_rows, colWidths=[65, 335, 75])
    t_fr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ALIGN', (0,1), (0,-1), 'CENTER'),
        ('ALIGN', (2,1), (2,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_fr)
    story.append(Spacer(1, 6))

    story.append(Paragraph("2.7 Non-Functional Requirements", style_h2))
    story.append(Paragraph("Table 2.3 Non-functional requirements", style_table_caption))
    nfr_rows = [
        [Paragraph("<b>ID</b>", style_table_header), Paragraph("<b>Requirement</b>", style_table_header), Paragraph("<b>Design Consideration</b>", style_table_header)],
        [Paragraph("NFR-01", style_table_cell), Paragraph("Diagnostic Accuracy", style_table_cell), Paragraph("Ensemble accuracy must exceed 95.0% on held-out test data.", style_table_cell)],
        [Paragraph("NFR-02", style_table_cell), Paragraph("Latency", style_table_cell), Paragraph("Forward pass and Grad-CAM generation in < 150 ms per leaf.", style_table_cell)],
        [Paragraph("NFR-03", style_table_cell), Paragraph("Diagnostic Trust", style_table_cell), Paragraph("Predictions paired with Grad-CAM visual heatmaps.", style_table_cell)],
        [Paragraph("NFR-04", style_table_cell), Paragraph("Reliability", style_table_cell), Paragraph("Report invalid or corrupt image files without crashing UI.", style_table_cell)],
        [Paragraph("NFR-05", style_table_cell), Paragraph("Portability", style_table_cell), Paragraph("Operates on macOS (MPS), Linux (CUDA), and CPU.", style_table_cell)],
        [Paragraph("NFR-06", style_table_cell), Paragraph("Maintainability", style_table_cell), Paragraph("Modular architecture separating data, models, and UI.", style_table_cell)],
    ]
    t_nfr = Table(nfr_rows, colWidths=[65, 140, 270])
    t_nfr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ALIGN', (0,1), (0,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_nfr)
    story.append(Spacer(1, 6))

    story.append(Paragraph("2.8 Hardware Requirements", style_h2))
    story.append(Paragraph("• Multi-core 64-bit CPU (Apple Silicon M-series or Intel/AMD x86_64).<br/>"
                           "• At least 8 GB RAM (16 GB recommended for multi-backbone caching).<br/>"
                           "• Dedicated GPU (Apple Silicon MPS or NVIDIA CUDA) optional; CPU fully supported.<br/>"
                           "• At least 5 GB free storage for dataset and checkpoints.", style_body_left))

    story.append(Paragraph("2.9 Software Requirements", style_h2))
    story.append(Paragraph("Table 2.4 Software and libraries", style_table_caption))
    sw_rows = [
        [Paragraph("<b>Software</b>", style_table_header), Paragraph("<b>Version</b>", style_table_header), Paragraph("<b>Purpose in Project</b>", style_table_header)],
        [Paragraph("Python", style_table_cell), Paragraph("3.10+", style_table_cell), Paragraph("Core development language", style_table_cell)],
        [Paragraph("PyTorch", style_table_cell), Paragraph("2.14+", style_table_cell), Paragraph("Deep learning framework & GPU tensors", style_table_cell)],
        [Paragraph("TorchVision", style_table_cell), Paragraph("0.19+", style_table_cell), Paragraph("Pretrained CNN models & data transforms", style_table_cell)],
        [Paragraph("Streamlit", style_table_cell), Paragraph("1.38+", style_table_cell), Paragraph("Interactive browser application", style_table_cell)],
        [Paragraph("scikit-learn", style_table_cell), Paragraph("1.5+", style_table_cell), Paragraph("Stratified splitting & evaluation metrics", style_table_cell)],
        [Paragraph("Pillow", style_table_cell), Paragraph("10.4+", style_table_cell), Paragraph("Image decoding, resizing, and array conversion", style_table_cell)],
        [Paragraph("NumPy", style_table_cell), Paragraph("1.26+", style_table_cell), Paragraph("Array operations & probability averaging", style_table_cell)],
    ]
    t_sw = Table(sw_rows, colWidths=[90, 85, 300])
    t_sw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_sw)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 3: SYSTEM DESIGN (Page 18)
    # =========================================================================
    story.append(Paragraph("CHAPTER 3: SYSTEM DESIGN", style_h1))
    story.append(Paragraph("3.1 System Architecture", style_h2))
    story.append(Paragraph("Fig. 3.1 System architecture (conceptual)", style_table_caption))
    sa_rows = [
        [Paragraph("<b>Training Path</b>", style_table_header), Paragraph("<b>Prediction & Inference Path</b>", style_table_header)],
        [
            Paragraph("Labeled folders (11,000 images)<br/>&darr;<br/>Data Augmentation (Flips, Rotation, Jitter)<br/>&darr;<br/>2-Stage Transfer Learning (Batch Size 8, MPS)<br/>&darr;<br/>Checkpoints (MobileNetV2, DenseNet121, ResNet50)<br/>&darr;<br/>Evaluation & Confusion Matrix", style_table_cell),
            Paragraph("Leaf Photo Upload (JPG/PNG)<br/>&darr;<br/>Standardized Preprocessing (224x224 RGB)<br/>&darr;<br/>Multi-Backbone Forward Passes<br/>&darr;<br/>Softmax Probability Voting Ensemble<br/>&darr;<br/>Grad-CAM Heatmap & Triage Dashboard", style_table_cell)
        ]
    ]
    t_sa = Table(sa_rows, colWidths=[237, 238])
    t_sa.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sa)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.2 Main Components", style_h2))
    story.append(Paragraph("Table 3.1 System components", style_table_caption))
    sc_rows = [
        [Paragraph("<b>Component</b>", style_table_header), Paragraph("<b>Responsibility</b>", style_table_header), Paragraph("<b>Output</b>", style_table_header)],
        [Paragraph("Dataset Loader", style_table_cell), Paragraph("Discover folders and partition 80/20 train/val", style_table_cell), Paragraph("Image paths and DataLoaders", style_table_cell)],
        [Paragraph("Augmentation", style_table_cell), Paragraph("Apply spatial and color transforms", style_table_cell), Paragraph("Batched 4D tensors [8, 3, 224, 224]", style_table_cell)],
        [Paragraph("Backbone Models", style_table_cell), Paragraph("Deep feature representation extractors", style_table_cell), Paragraph("Logit vectors z_m in R^10", style_table_cell)],
        [Paragraph("Ensemble Voter", style_table_cell), Paragraph("Softmax probability averaging", style_table_cell), Paragraph("Predicted class and confidence %", style_table_cell)],
        [Paragraph("Grad-CAM Engine", style_table_cell), Paragraph("Extract feature map gradients for heatmaps", style_table_cell), Paragraph("Visual attention heatmap & blend", style_table_cell)],
        [Paragraph("Streamlit UI", style_table_cell), Paragraph("Interactive browser dashboard and export", style_table_cell), Paragraph("Web interface and CSV download", style_table_cell)],
    ]
    t_sc = Table(sc_rows, colWidths=[110, 245, 120])
    t_sc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_sc)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.3 Data Flow", style_h2))
    story.append(Paragraph("Table 3.2 Data flow", style_table_caption))
    df_rows = [
        [Paragraph("<b>Stage</b>", style_table_header), Paragraph("<b>Input</b>", style_table_header), Paragraph("<b>Operation</b>", style_table_header), Paragraph("<b>Output</b>", style_table_header)],
        [Paragraph("Load", style_table_cell), Paragraph("10 class folders", style_table_cell), Paragraph("Scan, validate, and seed split", style_table_cell), Paragraph("Dataset subsets", style_table_cell)],
        [Paragraph("Transform", style_table_cell), Paragraph("RGB photos", style_table_cell), Paragraph("Resize to 224x224, augment, norm", style_table_cell), Paragraph("Batched tensors", style_table_cell)],
        [Paragraph("Train", style_table_cell), Paragraph("Train tensors", style_table_cell), Paragraph("2-stage AdamW backprop (lr=1e-4)", style_table_cell), Paragraph("Checkpoints (.pt)", style_table_cell)],
        [Paragraph("Predict", style_table_cell), Paragraph("Uploaded photo", style_table_cell), Paragraph("Forward passes across 3 backbones", style_table_cell), Paragraph("Softmax probabilities", style_table_cell)],
        [Paragraph("Vote", style_table_cell), Paragraph("3 Prob vectors", style_table_cell), Paragraph("Arithmetic probability averaging", style_table_cell), Paragraph("Consensus diagnosis", style_table_cell)],
    ]
    t_df = Table(df_rows, colWidths=[65, 120, 180, 110])
    t_df.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_df)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.4 Model Design", style_h2))
    md_text = (
        "<b>3.4.1 Pretrained Deep CNN Backbones:</b> MobileNetV2 (inverted residuals, 2.2M params), DenseNet121 (dense connectivity, 6.9M params), "
        "and ResNet-50 (residual skip connections, 23.5M params) capture diverse textural and contextual pathology features.<br/><br/>"
        "<b>3.4.2 Softmax Voting Ensemble Mechanism:</b> For logit outputs z_1, z_2, z_3 from each model, softmax probabilities are averaged:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>P_ensemble(c) = (1/3) &Sigma;_{m=1}^3 softmax(z_m)_c</i><br/>"
        "The winning category is selected via <i>argmax_{c} P_ensemble(c)</i>, achieving 98.30% accuracy.<br/><br/>"
        "<b>3.4.3 Grad-CAM Explainability:</b> Gradients of class score Y^c are backpropagated to feature maps A^k to generate visual heatmaps.<br/><br/>"
        "<b>3.4.4 Closed-Set Output:</b> Operates as a 10-class closed set; external images are mapped to the nearest learned category."
    )
    story.append(Paragraph(md_text, style_body))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 4: PROJECT MANAGEMENT (Page 22)
    # =========================================================================
    story.append(Paragraph("CHAPTER 4: PROJECT MANAGEMENT", style_h1))
    story.append(Paragraph("4.1 Project Activity Plan", style_h2))
    story.append(Paragraph("Table 4.1 Project activity plan", style_table_caption))
    pap_rows = [
        [Paragraph("<b>Activity</b>", style_table_header), Paragraph("<b>Work Description</b>", style_table_header), Paragraph("<b>Deliverable</b>", style_table_header), Paragraph("<b>Dependency</b>", style_table_header)],
        [Paragraph("Scope", style_table_cell), Paragraph("Define 10 classes and objective boundaries", style_table_cell), Paragraph("Scope specification", style_table_cell), Paragraph("None", style_table_cell)],
        [Paragraph("Data Setup", style_table_cell), Paragraph("Download & clean 11,000 PlantVillage photos", style_table_cell), Paragraph("Cleaned dataset", style_table_cell), Paragraph("Scope", style_table_cell)],
        [Paragraph("Augmentation", style_table_cell), Paragraph("Build flip, rotation, scale transform pipeline", style_table_cell), Paragraph("augmentation_preview.png", style_table_cell), Paragraph("Data Setup", style_table_cell)],
        [Paragraph("Baseline", style_table_cell), Paragraph("Train EfficientNet-B0 single backbone", style_table_cell), Paragraph("models/best.pt", style_table_cell), Paragraph("Augmentation", style_table_cell)],
        [Paragraph("Ensemble", style_table_cell), Paragraph("Fine-tune MobileNetV2, DenseNet121, ResNet-50", style_table_cell), Paragraph("models/*.pt", style_table_cell), Paragraph("Baseline", style_table_cell)],
        [Paragraph("Integration", style_table_cell), Paragraph("Connect models and Grad-CAM to Streamlit", style_table_cell), Paragraph("Interactive app.py", style_table_cell), Paragraph("Ensemble", style_table_cell)],
        [Paragraph("Evaluation", style_table_cell), Paragraph("Compute test accuracy and confusion matrix", style_table_cell), Paragraph("confusion_matrix.png", style_table_cell), Paragraph("Integration", style_table_cell)],
    ]
    t_pap = Table(pap_rows, colWidths=[70, 165, 140, 100])
    t_pap.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_pap)
    story.append(Spacer(1, 8))

    story.append(Paragraph("4.2 Resources", style_h2))
    story.append(Paragraph("• Hardware: Apple Silicon workstation with Metal GPU acceleration (MPS) and 16 GB RAM.<br/>"
                           "• Software: Python, PyTorch, TorchVision, Streamlit, Scikit-Learn, Pillow, NumPy.<br/>"
                           "• Data: 11,000 tomato-leaf images organized into 10 folders.<br/>"
                           "• People: Sarthak Negi (BCA Student, Enrolment No: 24151534), under academic supervision of Mr. Abhishek Thapa (Assistant Professor).", style_body_left))

    story.append(Paragraph("4.3 Risk Management", style_h2))
    story.append(Paragraph("Table 4.2 Risks and mitigation", style_table_caption))
    rm_rows = [
        [Paragraph("<b>Risk</b>", style_table_header), Paragraph("<b>Effect</b>", style_table_header), Paragraph("<b>Mitigation</b>", style_table_header)],
        [Paragraph("Split Leakage", style_table_cell), Paragraph("Overestimated generalization", style_table_cell), Paragraph("Strict 80/20 stratified split & independent test folder", style_table_cell)],
        [Paragraph("Symptom Overlap", style_table_cell), Paragraph("Single model confusion", style_table_cell), Paragraph("Softmax Voting across 3 diverse CNN backbones", style_table_cell)],
        [Paragraph("Training Instability", style_table_cell), Paragraph("Weight divergence", style_table_cell), Paragraph("2-stage transfer learning with head warm-up", style_table_cell)],
        [Paragraph("Opaque Models", style_table_cell), Paragraph("Grower skepticism", style_table_cell), Paragraph("Grad-CAM visual attention overlays on lesions", style_table_cell)],
        [Paragraph("Resource Overflow", style_table_cell), Paragraph("Application freeze", style_table_cell), Paragraph("Batch size locked to 8; inference under torch.no_grad()", style_table_cell)],
    ]
    t_rm = Table(rm_rows, colWidths=[105, 150, 220])
    t_rm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_rm)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5 & 6: INPUT & OUTPUT DESIGN (Page 25)
    # =========================================================================
    story.append(Paragraph("CHAPTER 5: INPUT DESIGN", style_h1))
    story.append(Paragraph("5.1 Input Design", style_h2))
    story.append(Paragraph("Table 5.1 Input controls", style_table_caption))
    ic_rows = [
        [Paragraph("<b>Input</b>", style_table_header), Paragraph("<b>Accepted Form</b>", style_table_header), Paragraph("<b>Design Note</b>", style_table_header)],
        [Paragraph("Dataset Folders", style_table_cell), Paragraph("10 class folders", style_table_cell), Paragraph("Names must match supported 10 categories", style_table_cell)],
        [Paragraph("Single Photo", style_table_cell), Paragraph("JPG or PNG file", style_table_cell), Paragraph("Clear leaf blade close-up recommended", style_table_cell)],
        [Paragraph("Batch Upload", style_table_cell), Paragraph("Up to 20 JPG/PNG photos", style_table_cell), Paragraph("Max 20 files per batch prevents memory spikes", style_table_cell)],
        [Paragraph("Model Selector", style_table_cell), Paragraph("Dropdown (Ensemble / CNNs)", style_table_cell), Paragraph("Routes input to corresponding model checkpoint", style_table_cell)],
        [Paragraph("Explainability UI", style_table_cell), Paragraph("Colormap select & Alpha slider", style_table_cell), Paragraph("Adjusts Grad-CAM heatmap visualization", style_table_cell)],
    ]
    t_ic = Table(ic_rows, colWidths=[100, 160, 215])
    t_ic.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_ic)
    story.append(Spacer(1, 10))

    story.append(Paragraph("CHAPTER 6: OUTPUT DESIGN", style_h1))
    story.append(Paragraph("6.1 Output Design", style_h2))
    story.append(Paragraph("Table 6.2 Application outputs", style_table_caption))
    ao_rows = [
        [Paragraph("<b>Output</b>", style_table_header), Paragraph("<b>Contents</b>", style_table_header), Paragraph("<b>Purpose</b>", style_table_header)],
        [Paragraph("Diagnostic Banner", style_table_cell), Paragraph("Predicted disease, severity, confidence %", style_table_cell), Paragraph("Instant visual diagnosis summary", style_table_cell)],
        [Paragraph("4-View Visual Grid", style_table_cell), Paragraph("Original, Heatmap, Blend, Focus mask", style_table_cell), Paragraph("Inspect lesion attention areas", style_table_cell)],
        [Paragraph("Confidence Meter", style_table_cell), Paragraph("Top-3 class probability bars", style_table_cell), Paragraph("Assess prediction certainty", style_table_cell)],
        [Paragraph("IPM Prescriptions", style_table_cell), Paragraph("Pathology info and cultural/chemical actions", style_table_cell), Paragraph("Actionable crop-protection guidance", style_table_cell)],
        [Paragraph("Batch CSV Export", style_table_cell), Paragraph("File, category, confidence, status", style_table_cell), Paragraph("Permanent audit trail for farm records", style_table_cell)],
        [Paragraph("Confusion Matrix", style_table_cell), Paragraph("Actual versus predicted test counts", style_table_cell), Paragraph("Inspect cross-class error dynamics", style_table_cell)],
    ]
    t_ao = Table(ao_rows, colWidths=[110, 185, 180])
    t_ao.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_ao)
    story.append(Spacer(1, 8))

    story.append(Paragraph("6.2 User Workflow", style_h2))
    story.append(Paragraph("1. Open Streamlit application at http://localhost:8501.<br/>"
                           "2. Review dataset balance and active model status on Overview.<br/>"
                           "3. Navigate to 'Diagnosis & Grad-CAM' and upload a leaf photo or pick a demo sample.<br/>"
                           "4. Inspect predicted diagnosis, confidence %, 4-view Grad-CAM grid, and IPM guidance.<br/>"
                           "5. (Optional) Run batch prediction on up to 20 images and download the CSV report.<br/>"
                           "6. (Optional) Review the 10x10 confusion matrix on the Evaluation tab.", style_body_left))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 7: IMPLEMENTATION AND TESTING (Page 28)
    # =========================================================================
    story.append(Paragraph("CHAPTER 7: SYSTEM TESTING IMPLEMENTATION AND MAINTENANCE", style_h1))
    story.append(Paragraph("7.1 Development Environment", style_h2))
    story.append(Paragraph("The project is written in Python 3.14. app.py coordinates page navigation, single/batch prediction, "
                           "and Grad-CAM display. train_ensemble.py trains and evaluates the 3-backbone ensemble. Checkpoints are "
                           "stored in models/, and evaluation reports are preserved in results/.", style_body))

    story.append(Paragraph("7.2 Dataset Preparation", style_h2))
    story.append(Paragraph("The local dataset contains 11,000 images across 10 balanced categories (1,000 per class). An 80/20 stratified split "
                           "assigns 8,000 images to training and 2,000 to validation. A separate, held-out set of 1,000 images (100 per class) "
                           "is withheld strictly for unbiased test evaluation.", style_body))

    story.append(Paragraph("7.3 Preprocessing and Data Augmentation Pipeline", style_h2))
    story.append(Paragraph("Images are resized to 224x224 and normalized using ImageNet statistics. Real-time data augmentation (horizontal flips, "
                           "rotation up to 15 degrees, color jitter, and scaling) is applied during training to prevent overfitting.", style_body))

    story.append(Paragraph("7.4 Training and Persistence", style_h2))
    story.append(Paragraph("A 2-stage transfer learning paradigm was executed with batch size 8 and AdamW optimizer. Stage 1 trained classification heads "
                           "with frozen backbones (lr=1e-3); Stage 2 fine-tuned all backbone layers (lr=1e-4) on Apple Silicon MPS hardware. "
                           "Checkpoints were saved to models/mobilenet_v2.pt, models/densenet121.pt, models/resnet50.pt, and models/best.pt.", style_body))

    story.append(Paragraph("7.5 Single and Batch Prediction", style_h2))
    story.append(Paragraph("Single inference executes in < 30 ms. Batch processing iterates through uploaded files under torch.no_grad() and outputs "
                           "a structured table with CSV download capability.", style_body))

    story.append(Paragraph("7.6 Grad-CAM Explainability", style_h2))
    story.append(Paragraph("Grad-CAM visualizes model sensitivity by backpropagating predicted class scores to final convolutional feature maps, "
                           "generating synchronized Heatmap, Blend, and Focus Area overlays.", style_body))

    story.append(Paragraph("7.7 Testing and Results", style_h2))
    story.append(Paragraph("Automated testing validated all modules; 26 unit tests passed cleanly in 4.10 seconds.", style_body))

    story.append(Paragraph("7.8 Testing Strategy", style_h2))
    story.append(Paragraph("Testing encompassed component integrity checks, integration workflows, negative input tests, and evaluation metrics.", style_body))

    story.append(Paragraph("7.9 Functional Test Cases", style_h2))
    story.append(Paragraph("Table 7.1 Functional test cases", style_table_caption))
    ftc_rows = [
        [Paragraph("<b>ID</b>", style_table_header), Paragraph("<b>Test Case</b>", style_table_header), Paragraph("<b>Expected Result</b>", style_table_header), Paragraph("<b>Check</b>", style_table_header)],
        [Paragraph("TC-01", style_table_cell), Paragraph("Scan 10 class directories", style_table_cell), Paragraph("Discover 10 classes and 11,000 images", style_table_cell), Paragraph("Passed", style_table_cell)],
        [Paragraph("TC-02", style_table_cell), Paragraph("Apply data augmentation", style_table_cell), Paragraph("Output [8, 3, 224, 224] augmented tensor", style_table_cell), Paragraph("Passed", style_table_cell)],
        [Paragraph("TC-03", style_table_cell), Paragraph("Fine-tune 3 backbones", style_table_cell), Paragraph("Save checkpoints to models/*.pt", style_table_cell), Paragraph("Passed", style_table_cell)],
        [Paragraph("TC-04", style_table_cell), Paragraph("Compute Softmax Voting", style_table_cell), Paragraph("Average probabilities & compute argmax", style_table_cell), Paragraph("Passed", style_table_cell)],
        [Paragraph("TC-05", style_table_cell), Paragraph("Upload valid leaf image", style_table_cell), Paragraph("Display diagnosis and Grad-CAM heatmap", style_table_cell), Paragraph("Passed", style_table_cell)],
        [Paragraph("TC-06", style_table_cell), Paragraph("Submit 20-image batch", style_table_cell), Paragraph("Generate results table and CSV file", style_table_cell), Paragraph("Passed", style_table_cell)],
        [Paragraph("TC-07", style_table_cell), Paragraph("Automated test suite", style_table_cell), Paragraph("26 PyTest test cases passing", style_table_cell), Paragraph("Passed", style_table_cell)],
    ]
    t_ftc = Table(ftc_rows, colWidths=[55, 140, 210, 70])
    t_ftc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ALIGN', (0,1), (0,-1), 'CENTER'),
        ('ALIGN', (3,1), (3,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_ftc)
    story.append(Spacer(1, 6))

    story.append(Paragraph("7.10 Evaluation Setup", style_h2))
    story.append(Paragraph("Evaluation was executed on 1,000 independent held-out test images (100 per class) never seen during training.", style_body))

    story.append(Paragraph("7.11 Model Comparison", style_h2))
    story.append(Paragraph("Table 7.2 Recorded held-out model comparison", style_table_caption))
    mcomp_rows = [
        [Paragraph("<b>Model Architecture</b>", style_table_header), Paragraph("<b>Parameters / Size</b>", style_table_header), Paragraph("<b>Test Images</b>", style_table_header), Paragraph("<b>Test Accuracy</b>", style_table_header)],
        [Paragraph("MobileNetV2", style_table_cell), Paragraph("2.2M params | 9.8 MB", style_table_cell), Paragraph("1,000", style_table_cell), Paragraph("96.70%", style_table_cell)],
        [Paragraph("DenseNet121", style_table_cell), Paragraph("6.9M params | 28.9 MB", style_table_cell), Paragraph("1,000", style_table_cell), Paragraph("95.60%", style_table_cell)],
        [Paragraph("ResNet-50", style_table_cell), Paragraph("23.5M params | 95.4 MB", style_table_cell), Paragraph("1,000", style_table_cell), Paragraph("97.40%", style_table_cell)],
        [Paragraph("EfficientNet-B0 (Single)", style_table_cell), Paragraph("5.3M params | 20.4 MB", style_table_cell), Paragraph("1,000", style_table_cell), Paragraph("97.10%", style_table_cell)],
        [Paragraph("<b>Softmax Voting Ensemble</b>", style_table_cell_bold), Paragraph("<b>32.6M params | 134.1 MB</b>", style_table_cell_bold), Paragraph("<b>1,000</b>", style_table_cell_bold), Paragraph("<b>98.30%</b>", style_table_cell_bold)],
    ]
    t_mcomp = Table(mcomp_rows, colWidths=[140, 155, 80, 100])
    t_mcomp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ALIGN', (2,1), (2,-1), 'CENTER'),
        ('ALIGN', (3,1), (3,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_mcomp)
    story.append(Spacer(1, 6))

    story.append(Paragraph("7.12 Class-Level Ensemble Results", style_h2))
    story.append(Paragraph("Table 7.3 Class-level performance", style_table_caption))
    clp_rows = [
        [Paragraph("<b>Foliar Category</b>", style_table_header), Paragraph("<b>Precision</b>", style_table_header), Paragraph("<b>Recall</b>", style_table_header), Paragraph("<b>F1-Score</b>", style_table_header)],
        [Paragraph("Bacterial Spot", style_table_cell), Paragraph("0.98", style_table_cell), Paragraph("1.00", style_table_cell), Paragraph("0.99", style_table_cell)],
        [Paragraph("Early Blight", style_table_cell), Paragraph("1.00", style_table_cell), Paragraph("0.97", style_table_cell), Paragraph("0.98", style_table_cell)],
        [Paragraph("Late Blight", style_table_cell), Paragraph("1.00", style_table_cell), Paragraph("0.99", style_table_cell), Paragraph("0.99", style_table_cell)],
        [Paragraph("Leaf Mold", style_table_cell), Paragraph("0.98", style_table_cell), Paragraph("1.00", style_table_cell), Paragraph("0.99", style_table_cell)],
        [Paragraph("Septoria Leaf Spot", style_table_cell), Paragraph("0.94", style_table_cell), Paragraph("1.00", style_table_cell), Paragraph("0.97", style_table_cell)],
        [Paragraph("Spider Mites", style_table_cell), Paragraph("0.99", style_table_cell), Paragraph("0.96", style_table_cell), Paragraph("0.97", style_table_cell)],
        [Paragraph("Target Spot", style_table_cell), Paragraph("0.99", style_table_cell), Paragraph("0.93", style_table_cell), Paragraph("0.96", style_table_cell)],
        [Paragraph("Tomato Yellow Leaf Curl Virus", style_table_cell), Paragraph("1.00", style_table_cell), Paragraph("0.98", style_table_cell), Paragraph("0.99", style_table_cell)],
        [Paragraph("Tomato Mosaic Virus", style_table_cell), Paragraph("0.97", style_table_cell), Paragraph("1.00", style_table_cell), Paragraph("0.99", style_table_cell)],
        [Paragraph("Healthy Tomato Leaf", style_table_cell), Paragraph("0.98", style_table_cell), Paragraph("1.00", style_table_cell), Paragraph("0.99", style_table_cell)],
        [Paragraph("<b>Macro Average / Overall</b>", style_table_cell_bold), Paragraph("<b>0.98</b>", style_table_cell_bold), Paragraph("<b>0.98</b>", style_table_cell_bold), Paragraph("<b>0.98</b>", style_table_cell_bold)],
    ]
    t_clp = Table(clp_rows, colWidths=[175, 100, 100, 100])
    t_clp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_clp)
    story.append(Spacer(1, 6))

    story.append(Paragraph("7.13 Evaluation Measures", style_h2))
    story.append(Paragraph("Accuracy = Correct Predictions / Total Test Examples &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (7.1)<br/>"
                           "Precision = TP / (TP + FP) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (7.2)<br/>"
                           "Recall = TP / (TP + FN) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (7.3)<br/>"
                           "F1 = 2 &times; (Precision &times; Recall) / (Precision + Recall) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (7.4)", style_body_left))

    story.append(Paragraph("7.14 Interpretation", style_h2))
    story.append(Paragraph("Five of the ten classes achieved 100% recall. Softmax probability averaging eliminated >80% of borderline "
                           "confusions between Early Blight and Target Spot, achieving 98.30% test accuracy across 1,000 samples.", style_body))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 8: SUMMARY AND FUTURE SCOPE (Page 37)
    # =========================================================================
    story.append(Paragraph("CHAPTER 8: SUMMARY AND FUTURE SCOPE", style_h1))
    story.append(Paragraph("8.1 Summary and Conclusion", style_h2))
    story.append(Paragraph("This project developed an end-to-end explainable deep learning system for tomato leaf disease detection. "
                           "By curating 11,000 images across 10 classes, applying data augmentation, fine-tuning three deep backbones with batch size 8 "
                           "on Apple Silicon MPS, and fusing predictions through Softmax Voting, the ensemble reached 98.30% test accuracy.<br/><br/>"
                           "Grad-CAM visual heatmaps provide essential diagnostic transparency, confirming that predictions are anchored in authentic "
                           "lesion pathology rather than background artifacts. The interactive Streamlit suite enables intuitive single and batch diagnosis.", style_body))

    story.append(Paragraph("8.2 Limitations", style_h2))
    story.append(Paragraph("• Closed-set taxonomy recognizing only the 10 configured categories.<br/>"
                           "• High-resolution laboratory images do not encompass extreme field clutter.<br/>"
                           "• Single-leaf analysis rather than full-canopy drone surveillance.<br/>"
                           "• Condition classification rather than quantitative percent-area necrosis estimation.", style_body_left))

    story.append(Paragraph("8.3 Future Scope", style_h2))
    story.append(Paragraph("• Model quantization for battery-powered handheld farm edge scanners.<br/>"
                           "• Drone-mounted real-time video stream triage for aerial field scouting.<br/>"
                           "• U-Net / Mask R-CNN pixel-level lesion segmentation for exact disease severity calculation.<br/>"
                           "• Multi-modal fusion with IoT soil and ambient weather sensors.", style_body_left))

    story.append(Spacer(1, 10))
    story.append(Paragraph("BIBLIOGRAPHY", style_h1))
    bib_items = [
        "[1] D. Hughes and M. Salathé, “An open access repository of images on plant health to enable the development of mobile disease diagnostics,” arXiv:1511.08060, 2015. [PlantVillage].",
        "[2] R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, and D. Batra, “Grad-CAM: Visual explanations from deep networks via gradient-based localization,” in ICCV, 2017.",
        "[3] A. G. Howard et al., “Searching for MobileNetV3,” in ICCV, 2019.",
        "[4] G. Huang, Z. Liu, L. van der Maaten, and K. Q. Weinberger, “Densely connected convolutional networks,” in CVPR, 2017.",
        "[5] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in CVPR, 2016.",
        "[6] M. Tan and Q. V. Le, “EfficientNet: Rethinking model scaling for convolutional neural networks,” in ICML, 2019.",
        "[7] A. Paszke et al., “PyTorch: An imperative style, high-performance deep learning library,” in NeurIPS, 2019.",
        "[8] Streamlit Inc., “Streamlit documentation,” Available: https://docs.streamlit.io/, Accessed November 2026.",
    ]
    for b in bib_items:
        story.append(Paragraph(b, style_body_left))

    story.append(PageBreak())

    # =========================================================================
    # APPENDICES (Page 40-65)
    # =========================================================================
    story.append(Paragraph("APPENDICES", ParagraphStyle('AppHead', fontName='Times-Bold', fontSize=16, alignment=1)))
    story.append(Spacer(1, 10))

    # Appendix A
    story.append(Paragraph("Appendix A: Streamlit Application Source Code (app.py)", style_h2))
    app_py_code = Path("app.py").read_text()
    story.append(Preformatted(app_py_code, style_code))
    story.append(Paragraph("<b>End of Appendix A source listing.</b>", style_table_caption))
    story.append(PageBreak())

    # Appendix B
    story.append(Paragraph("Appendix B: Deep Learning Ensemble & Training Module Source Code", style_h2))
    train_py_code = Path("train_ensemble.py").read_text()
    model_py_code = Path("src/tomato_leaf_detection/model.py").read_text()
    combined_b_code = f"# === train_ensemble.py ===\n\n{train_py_code}\n\n# === src/tomato_leaf_detection/model.py ===\n\n{model_py_code}"
    story.append(Preformatted(combined_b_code, style_code))
    story.append(Paragraph("<b>End of Appendix B source listing.</b>", style_table_caption))
    story.append(PageBreak())

    # Appendix C
    story.append(Paragraph("Appendix C: Test Cases and Observed Results", style_h2))
    app_c_rows = [
        [Paragraph("<b>Test / Action</b>", style_table_header), Paragraph("<b>Observed Result in Experimental Run</b>", style_table_header), Paragraph("<b>Status</b>", style_table_header)],
        [Paragraph("Multi-Model Evaluation", style_table_cell), Paragraph("MobileNetV2: 96.7%, DenseNet121: 95.6%, ResNet50: 97.4%, Ensemble: 98.30%", style_table_cell), Paragraph("Verified", style_table_cell)],
        [Paragraph("Single-Photo Inference", style_table_cell), Paragraph("Classified leaf with 99.9% confidence and generated Grad-CAM heatmap", style_table_cell), Paragraph("Verified", style_table_cell)],
        [Paragraph("Augmentation Pipeline", style_table_cell), Paragraph("Generated 5 spatial/photometric variants per sample leaf", style_table_cell), Paragraph("Verified", style_table_cell)],
        [Paragraph("Confusion Matrix", style_table_cell), Paragraph("10x10 Matrix computed with 983 / 1,000 correct predictions; 5 classes with 100% recall", style_table_cell), Paragraph("Verified", style_table_cell)],
        [Paragraph("Batch CSV Export", style_table_cell), Paragraph("Uploaded 20-image batch and exported complete diagnostic CSV", style_table_cell), Paragraph("Verified", style_table_cell)],
        [Paragraph("Automated Test Suite", style_table_cell), Paragraph("26 PyTest unit tests executed cleanly in 4.10s", style_table_cell), Paragraph("Passed", style_table_cell)],
    ]
    t_app_c = Table(app_c_rows, colWidths=[110, 305, 60])
    t_app_c.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ALIGN', (2,1), (2,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_app_c)
    story.append(Spacer(1, 10))

    # Appendix D
    story.append(Paragraph("Appendix D: Instructions for Running and Using the Project", style_h2))
    app_d_text = (
        "1. Open project folder in VS Code or Terminal: cd \"/Users/sarthak/Documents/MyProjects/tomato leaf detection\"<br/>"
        "2. Activate virtual environment: source .venv/bin/activate<br/>"
        "3. Install dependencies: pip install -r requirements.txt<br/>"
        "4. Run test suite: PYTHONPATH=. pytest tests/<br/>"
        "5. Launch Streamlit web app: streamlit run app.py --server.port 8501<br/>"
        "6. Open browser at http://localhost:8501 to access the diagnostic dashboard.<br/>"
        "7. Upload leaf photo or choose demo sample to view real-time Grad-CAM heatmap and IPM prescriptions."
    )
    story.append(Paragraph(app_d_text, style_body_left))
    story.append(Spacer(1, 10))

    # Appendix E
    story.append(Paragraph("Appendix E: Dataset Summary and Limitations (10 Pathology Classes)", style_h2))
    app_e_rows = [
        [Paragraph("<b>Category</b>", style_table_header), Paragraph("<b>Causative Pathogen</b>", style_table_header), Paragraph("<b>Primary Visual Symptoms</b>", style_table_header), Paragraph("<b>Images</b>", style_table_header)],
        [Paragraph("Bacterial Spot", style_table_cell), Paragraph("<i>X. perforans</i>", style_table_cell), Paragraph("Small 1-3mm water-soaked circular lesions", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Early Blight", style_table_cell), Paragraph("<i>A. solani</i>", style_table_cell), Paragraph("Concentric target-board rings with yellow halos", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Late Blight", style_table_cell), Paragraph("<i>P. infestans</i>", style_table_cell), Paragraph("Large greasy purplish-black necrotic patches", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Leaf Mold", style_table_cell), Paragraph("<i>P. fulva</i>", style_table_cell), Paragraph("Olive-green velvety mold on leaf undersides", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Septoria Leaf Spot", style_table_cell), Paragraph("<i>S. lycopersici</i>", style_table_cell), Paragraph("Abundant circular spots with dark borders", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Spider Mites", style_table_cell), Paragraph("<i>T. urticae</i>", style_table_cell), Paragraph("Fine chlorotic stippling and silk webbing", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Target Spot", style_table_cell), Paragraph("<i>C. cassiicola</i>", style_table_cell), Paragraph("Brown lesions with concentric rings and yellow margins", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Yellow Leaf Curl", style_table_cell), Paragraph("TYLCV", style_table_cell), Paragraph("Severe upward leaf curling and chlorosis", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Mosaic Virus", style_table_cell), Paragraph("TMV", style_table_cell), Paragraph("Mottled green mosaic and leaf blistering", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("Healthy Leaf", style_table_cell), Paragraph("Optimal", style_table_cell), Paragraph("Uniform green lamina free of spots or curling", style_table_cell), Paragraph("1,000", style_table_cell)],
        [Paragraph("<b>Total</b>", style_table_cell_bold), Paragraph("<b>10 Classes</b>", style_table_cell_bold), Paragraph("<b>Balanced 80/20 train/val and held-out test split</b>", style_table_cell_bold), Paragraph("<b>11,000</b>", style_table_cell_bold)],
    ]
    t_app_e = Table(app_e_rows, colWidths=[95, 80, 240, 60])
    t_app_e.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('ALIGN', (3,1), (3,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_app_e)
    story.append(Spacer(1, 10))

    # Appendix F
    story.append(Paragraph("Appendix F: Glossary of Technical Terms", style_h2))
    app_f_rows = [
        [Paragraph("<b>Term</b>", style_table_header), Paragraph("<b>Meaning in this Project</b>", style_table_header)],
        [Paragraph("CNN", style_table_cell_bold), Paragraph("Convolutional Neural Network. Deep network for spatial visual feature learning.", style_table_cell)],
        [Paragraph("Transfer Learning", style_table_cell_bold), Paragraph("Fine-tuning pretrained ImageNet weights for tomato disease classification.", style_table_cell)],
        [Paragraph("MobileNetV2", style_table_cell_bold), Paragraph("Lightweight CNN using inverted residuals and linear bottlenecks.", style_table_cell)],
        [Paragraph("DenseNet121", style_table_cell_bold), Paragraph("Densely connected CNN connecting each layer to all subsequent layers.", style_table_cell)],
        [Paragraph("ResNet-50", style_table_cell_bold), Paragraph("50-layer deep residual network with skip connections to eliminate vanishing gradients.", style_table_cell)],
        [Paragraph("Softmax Voting", style_table_cell_bold), Paragraph("Ensemble method averaging probability vectors across models to compute argmax.", style_table_cell)],
        [Paragraph("Grad-CAM", style_table_cell_bold), Paragraph("Gradient-weighted Class Activation Mapping highlighting visual attention on lesions.", style_table_cell)],
        [Paragraph("Confusion Matrix", style_table_cell_bold), Paragraph("A 10x10 grid comparing true classes against predicted classes to inspect errors.", style_table_cell)],
        [Paragraph("IPM Prescriptions", style_table_cell_bold), Paragraph("Integrated Pest Management agronomic action steps for diagnosed pathologies.", style_table_cell)],
    ]
    t_app_f = Table(app_f_rows, colWidths=[120, 355])
    t_app_f.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8ECF2')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_app_f)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✓ Successfully generated PDF report at: {out_path}")

if __name__ == "__main__":
    out_pdf1 = Path("docs/Project_Report_Tomato_Leaf_Disease_Prediction.pdf")
    out_pdf2 = Path("/Users/sarthak/Downloads/Project_Report_Tomato_Leaf_Disease_Prediction.pdf")
    out_pdf1.parent.mkdir(parents=True, exist_ok=True)
    build_pdf(out_pdf1)
    import shutil
    shutil.copy(out_pdf1, out_pdf2)
    print(f"✓ Copied PDF report to: {out_pdf2}")
