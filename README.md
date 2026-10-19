# Explainable-Tomato-Leaf-Disease-Detection-Using-AI-Ml

**Explainable Tomato Leaf Disease Detection Using AI/ML**  
Comprehensive computer-vision diagnostic and explainability suite developed by **Team Green tech**.

---

## Project Status: 100% Complete (Production Ready)

All four project milestones have been fully implemented, validated, and tested:

- [x] **Milestone 1 (25% - Baseline Foundation):** Reproducible Python dependency management, ImageFolder dataset discovery, stratified train/validation splitting, class-balanced transfer learning with EfficientNet-B0, and basic Streamlit interface.
- [x] **Milestone 2 (50% - Evaluation & Error Dynamics):** Multi-class metrics (Accuracy, Macro Precision, Recall, F1), publication-ready 10×10 Confusion Matrix generator, and error dynamics analysis.
- [x] **Milestone 3 (75% - Explainable AI & Multi-Model Benchmarking):** Full Gradient-weighted Class Activation Mapping (Grad-CAM) pipeline with multi-colormap support, blended overlays, high-attention focus masks, agronomic disease treatment prescriptions, and multi-architecture backbones (EfficientNet-B0, ResNet-18, ResNet-50, MobileNetV3-Large).
- [x] **Milestone 4 (100% - Packaging, CLI, & Deployment):** Standalone CLI inference tool, instant demo sample image library, comprehensive 22-test automated test suite, Docker containerization, and docker-compose deployment.

---

## Architecture Overview (High-Level In-Depth System Flowchart)

```mermaid
flowchart TD
    %% ==========================================
    %% TIER 1: DATA INGESTION & TRANSFORMS
    %% ==========================================
    subgraph Tier1["1. Data Discovery, Stratification & Augmentation Layer"]
        RawData["📁 Raw Dataset (data/raw/)<br/>10 Disease Categories"] --> SplitCheck{"Explicit train/val Split?"}
        SplitCheck -- "Yes" --> ExplicitSplit["Load datasets.ImageFolder<br/>(data/raw/train & val)"]
        SplitCheck -- "No" --> StratSplit["sklearn train_test_split<br/>Stratified 80/20 (Seed = 42)"]
        
        ExplicitSplit --> Transforms["Apply build_transforms() Pipeline"]
        StratSplit --> Transforms

        Transforms --> AugmentTrain["Train Transform:<br/>• Resize (224×224)<br/>• RandomHorizontalFlip(p=0.5)<br/>• RandomRotation(degrees=10°)<br/>• ToTensor() -> [3, 224, 224]<br/>• Normalize: μ=(0.485, 0.456, 0.406), σ=(0.229, 0.224, 0.225)"]
        Transforms --> AugmentVal["Val Transform:<br/>• Resize (224×224)<br/>• ToTensor() -> [3, 224, 224]<br/>• Normalize: μ, σ"]

        AugmentTrain --> TrainLoader["DataLoader (Train)<br/>batch_size=32, shuffle=True"]
        AugmentVal --> ValLoader["DataLoader (Val)<br/>batch_size=32, shuffle=False"]
    end

    %% ==========================================
    %% TIER 2: MODEL ARCHITECTURE & TRAINING
    %% ==========================================
    subgraph Tier2["2. Convolutional Backbone & Training Mechanics"]
        TrainLoader --> TrainLoop["Epoch Loop (run_epoch)"]
        
        ArchChoice["Backbone Selection (build_model):<br/>• EfficientNet-B0 (MBConv + Squeeze-and-Excitation)<br/>• ResNet-18 / ResNet-50 (Residual Skip Connections)<br/>• MobileNetV3-Large (Hardware-Aware NAS)"] --> InitModel["Replace Head:<br/>model.classifier[1] = nn.Linear(1280, 10)"]
        InitModel --> TrainLoop

        TrainLoop --> FwdTrain["Forward Pass: outputs = model(images)<br/>Batch Tensor: [32, 10]"]
        FwdTrain --> CalcLoss["CrossEntropyLoss(outputs, labels)"]
        CalcLoss --> Backprop["loss.backward() + AdamW.step()<br/>lr=1e-3, weight_decay=1e-4"]
        
        Backprop --> EvalVal["Validation Pass (torch.no_grad)<br/>Compute Loss & Top-1 Accuracy"]
        ValLoader --> EvalVal
        
        EvalVal --> CheckBest{"val_accuracy > best_accuracy?"}
        CheckBest -- "Yes" --> SaveCkpt[("💾 Save Checkpoint (models/best.pt)<br/>• model_state_dict<br/>• class_names (10 classes)<br/>• image_size=224<br/>• training_history")]
        CheckBest -- "No" --> NextEpoch["Log Metrics & Proceed Next Epoch"]
        SaveCkpt --> NextEpoch
    end

    %% ==========================================
    %% TIER 3: MODEL DESERIALIZATION BRIDGE
    %% ==========================================
    SaveCkpt ==>|"Serialized Weights Bridge"| CacheLoader["📦 Resource Caching (@st.cache_resource)<br/>torch.load(map_location='cpu') -> model.eval()"]

    %% ==========================================
    %% TIER 4: DUAL-PATH EXPLAINABLE INFERENCE
    %% ==========================================
    subgraph Tier3["3. Dual-Path Explainable Inference Engine"]
        UserInput["📸 Input Query Leaf:<br/>• Live Camera Upload (JPG/PNG)<br/>• Built-in Samples (data/samples/)"] --> InputTensor["Bilinear Resize (224×224)<br/>ToTensor() + Normalize<br/>unsqueeze(0) -> [1, 3, 224, 224]"]
        
        CacheLoader --> ModelReady["Inference Backbone Ready<br/>Registers Forward & Backward Hooks"]
        InputTensor --> ModelReady

        %% Path A: Classification
        ModelReady --> BranchA["Forward Pass (torch.no_grad)<br/>Logits: z ∈ ℝ¹⁰"]
        BranchA --> Softmax["Softmax: P(y=c|x) = e^zc / ∑ e^zj"]
        Softmax --> TopKRank["Top-K Ranking & Argmax<br/>• Predicted Disease Index<br/>• Confidence Score %<br/>• Distribution Bars"]

        %% Path B: Grad-CAM
        ModelReady --> BranchB["Forward Hook: Capture Activations<br/>A^k ∈ ℝ^{C × 7 × 7} (Last Conv Layer)"]
        BranchB --> GradBackprop["Backward Pass with Target Score Y^c<br/>Backward Hook: Capture Gradients ∂Y^c / ∂A^k"]
        GradBackprop --> GAP["Global Average Pooling (Weights α_k^c):<br/>α_k^c = (1/Z) ∑_i ∑_j (∂Y^c / ∂A_{i,j}^k)"]
        GAP --> WeightedReLU["Weighted Sum + ReLU:<br/>L_GradCAM = ReLU(∑_k α_k^c A^k)"]
        WeightedReLU --> Upsample["Bilinear Upsample (7×7 -> 224×224)<br/>Min-Max Normalize -> [0.0, 1.0]"]
        Upsample --> ColorMap["Apply Colormap (Jet, Turbo, Viridis)<br/>-> 3-Channel RGB Heatmap"]
        ColorMap --> BlendOverlay["Alpha Blending:<br/>I_blend = (1 - α)·I_orig + α·I_heatmap"]
        ColorMap --> FocusMask["Attention Thresholding (Heatmap ≥ 0.5)<br/>-> High-Activation Lesion Mask"]
    end

    %% ==========================================
    %% TIER 5: CLINICAL AGRONOMY & DELIVERY
    %% ==========================================
    subgraph Tier4["4. Agronomic Prescription & Multi-Channel Delivery"]
        TopKRank --> KnowledgeBase["📖 Agronomic Lookup (disease_info.py)"]
        KnowledgeBase --> BioProfile["Pathogen Taxonomy & Severity<br/>(Bacterium, Fungus, Oomycete, Virus, Pest)"]
        KnowledgeBase --> ActionPlan["🚨 Immediate Containment Triage<br/>• Rogue infected tissue<br/>• Cease overhead irrigation<br/>• Disinfect tools (70% alcohol)"]
        KnowledgeBase --> TreatmentPlan["🌿 Integrated Pest Management (IPM)<br/>• Certified Organic: Copper, Bacillus subtilis, Neem<br/>• Chemical: FRAC rotation (M05 chlorothalonil, 11 azoxystrobin)<br/>• Prevention: Drip irrigation, 3-yr rotation"]

        BlendOverlay --> VisualInspectionGrid["🖼️ 4-View Visual Explanation Grid<br/>1. Original Leaf Image<br/>2. Grad-CAM Heatmap Tile<br/>3. Superimposed Blend Overlay<br/>4. High-Attention Focus Area"]
        FocusMask --> VisualInspectionGrid

        BioProfile --> FinalDelivery["✅ Verified Actionable Diagnostic Report"]
        ActionPlan --> FinalDelivery
        TreatmentPlan --> FinalDelivery
        VisualInspectionGrid --> FinalDelivery
    end

    FinalDelivery --> StreamlitUI["🌐 Interactive Streamlit App (localhost:8501)"]
    FinalDelivery --> CLITool["💻 Standalone CLI (predict.py --explain)"]
    FinalDelivery --> DockerDeploy["🐳 Dockerized Microservice Container"]

    style SaveCkpt fill:#1b4d32,stroke:#2ecc71,stroke-width:2px,color:#fff
    style FinalDelivery fill:#103324,stroke:#27ae60,stroke-width:3px,color:#fff
    style StreamlitUI fill:#1d5c40,stroke:#85b79a,stroke-width:2px,color:#fff
    style CLITool fill:#1d5c40,stroke:#85b79a,stroke-width:2px,color:#fff
    style DockerDeploy fill:#1d5c40,stroke:#85b79a,stroke-width:2px,color:#fff
    style Tier1 fill:#f9fcf9,stroke:#d0e6d6,stroke-width:1px
    style Tier2 fill:#f4fbf5,stroke:#bce0c8,stroke-width:1px
    style Tier3 fill:#f0f9f3,stroke:#a6d8b6,stroke-width:1px
    style Tier4 fill:#eaf7ee,stroke:#89cca0,stroke-width:1px
```

---

## Project Layout

```text
.
├── app.py                                # Full-featured Streamlit Diagnostic & Explainability App
├── Dockerfile                            # Production container image definition
├── docker-compose.yml                    # Multi-container orchestration config
├── requirements.txt                      # Pinned Python package dependencies
├── models/
│   └── best.pt                           # Trained EfficientNet-B0 checkpoint (10 classes)
├── data/
│   ├── raw/                              # ImageFolder dataset directory
│   └── samples/                          # Built-in diagnostic sample leaf images
├── results/                              # Output folder for exported Grad-CAM heatmaps
├── src/tomato_leaf_detection/
│   ├── __init__.py                       # Package exports and version metadata (v1.0.0)
│   ├── config.py                         # TrainingConfig settings and default paths
│   ├── data.py                           # Dataset loaders, augmentations, and stratified splitting
│   ├── disease_info.py                   # Agronomic knowledge base & treatments for 10 diseases
│   ├── evaluate.py                       # Confusion matrix, classification metrics, and error analysis
│   ├── explainability.py                 # Grad-CAM engine, colormap blending, and focus masking
│   ├── model.py                          # Multi-architecture builder and latency benchmarking
│   ├── predict.py                        # Standalone CLI prediction & Grad-CAM export tool
│   └── train.py                          # Multi-architecture model training script
└── tests/
    └── test_project.py                   # 22 automated unit and integration tests
```

---

## Monitored Tomato Leaf Conditions

The classifier diagnoses the following 10 conditions from the standard PlantVillage pathology taxonomy:

1. **Bacterial Spot** (*Xanthomonas vesicatoria*)
2. **Early Blight** (*Alternaria solani*)
3. **Late Blight** (*Phytophthora infestans*)
4. **Leaf Mold** (*Passalora fulva*)
5. **Septoria Leaf Spot** (*Septoria lycopersici*)
6. **Two-Spotted Spider Mites** (*Tetranychus urticae*)
7. **Target Spot** (*Corynespora cassiicola*)
8. **Tomato Yellow Leaf Curl Virus** (TYLCV)
9. **Tomato Mosaic Virus** (ToMV)
10. **Healthy Foliage** (*Solanum lycopersicum*)

---

## Installation & Setup

### Local Python Environment

```bash
# 1. Clone repository and navigate to workspace
cd "tomato leaf detection"

# 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Usage Guide

### 1. Launch the Interactive Web Application

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser. The application includes:
- **🔬 Leaf Health Diagnosis & Grad-CAM:** Upload leaf photos or select 1-click built-in demo samples. Inspect 4-view visualizations (Original, Heatmap, Superimposed Blend, High-Attention Focus Area) with selectable colormaps (`jet`, `turbo`, `viridis`, `plasma`, `magma`) and opacity blending.
- **⚡ Multi-Model Architecture Comparison:** Benchmark EfficientNet-B0, ResNet-18, ResNet-50, and MobileNetV3-Large on live latency and memory footprint.
- **📊 Model Evaluation & Confusion Matrix:** Interactive 10×10 Confusion Matrix and error pairing dynamics.
- **📖 Plant Pathology Guide & Reference:** Comprehensive agronomic disease encyclopedia with symptoms, immediate actions, organic remedies, and chemical controls.

### 2. Run CLI Diagnosis & Export Grad-CAM Heatmaps

Run automated predictions and save explainability visual overlays directly to disk:

```bash
python -m src.tomato_leaf_detection.predict \
  --image data/samples/early_blight_leaf.jpg \
  --explain \
  --output-dir results/
```

Outputs will be saved in `results/`:
- `[image]_gradcam_blend.png`
- `[image]_gradcam_heatmap.png`
- `[image]_focus.png`

To output machine-readable JSON for integration into farm management APIs:

```bash
python -m src.tomato_leaf_detection.predict \
  --image data/samples/healthy_leaf.jpg \
  --json
```

### 3. Train Models Across Backbones

Train any supported convolutional backbone on your dataset:

```bash
python -m src.tomato_leaf_detection.train \
  --data-dir data/raw \
  --architecture efficientnet_b0 \
  --output models/best.pt \
  --epochs 10 \
  --batch-size 32 \
  --device auto
```

Available architecture choices: `efficientnet_b0`, `resnet18`, `resnet50`, `mobilenet_v3_large`.

### 4. Run Automated Test Suite

Run the full pytest test suite (22 unit & integration tests):

```bash
PYTHONPATH=. pytest -v
```

---

## Docker Deployment

### Run with Docker Compose

```bash
docker-compose up --build
```

Access the application at `http://localhost:8501`.

### Build & Run Container Manually

```bash
docker build -t tomato-leaf-detection .
docker run -p 8501:8501 tomato-leaf-detection
```

---

## Model Benchmark Summary

| Architecture | Model Family | Total Parameters | Model Size (MB) | Avg Latency (CPU) | Validation Accuracy | Recommended Deployment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **EfficientNet-B0** | Compound Scaling CNN | 5.3M | 20.4 MB | ~14 ms | 65.9% (Baseline) | Cloud API, High Grad-CAM Fidelity |
| **ResNet-18** | Residual Network | 11.7M | 44.8 MB | ~11 ms | 63.4% | Fast Convergence, Robust Skip Connections |
| **ResNet-50** | Deep Residual Network | 25.6M | 97.8 MB | ~28 ms | 67.1% | Complex multi-symptom leaves |
| **MobileNetV3-Large** | Edge Hardware NAS | 5.4M | 21.6 MB | ~8.9 ms | 64.8% | Mobile, drones, field edge devices |

---

## Limitations & Best Practices

1. **Leaf Surface Clarity:** Photographs should be captured in uniform, well-diffused light with the leaf blade occupying 70%+ of the viewfinder.
2. **Co-Infections:** When multiple pathogens concurrently infect the same leaf, Grad-CAM highlights the dominant necrotic focus. Always cross-validate automated AI triage with physical field inspections.
3. **Preventive Chemistry:** Recommended treatments must be cross-checked with local agricultural extension guidelines and chemical registrations for your specific jurisdiction.

---

## Authors & Acknowledgments

- **Team Green tech**
- Plant pathology taxonomy based on standard Solanaceae diagnostic literature.
- Transfer learning weights courtesy of PyTorch TorchVision model zoo.
