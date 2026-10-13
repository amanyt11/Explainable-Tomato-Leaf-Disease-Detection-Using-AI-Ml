# Explainable-Tomato-Leaf-Disease-Detection-Using-AI-Ml

## Project title

**Explainable Tomato Leaf Disease Detection Using AI/ML**

Baseline implementation for **Team Green tech**'s project proposal:
**Explainable Tomato Leaf Disease Detection Using AI/ML**.

## Current progress: 25% complete

This milestone establishes the first end-to-end foundation:

- reproducible Python dependency and configuration setup;
- ImageFolder dataset discovery and train/validation splitting;
- class-balanced baseline model using transfer learning with EfficientNet-B0;
- training command that saves the best validation checkpoint;
- Streamlit prediction interface with confidence scores and a clear checkpoint state.

The explainability layer, dataset-specific evaluation, and deployment hardening remain
future milestones. No model accuracy is claimed until the project dataset is supplied
and the training command has been run.

## Project layout

```text
.
├── app.py
├── requirements.txt
├── data/
│   └── raw/                 # ImageFolder data goes here (not committed)
├── models/                  # Generated checkpoints (not committed)
├── src/tomato_leaf_detection/
│   ├── config.py
│   ├── data.py
│   ├── model.py
│   └── train.py
└── tests/
    └── test_project.py
```

## Dataset format

Place images in class subdirectories. Both a single directory and a pre-split
dataset are supported:

```text
data/raw/
├── train/
│   ├── healthy/
│   └── tomato_late_blight/
└── val/
    ├── healthy/
    └── tomato_late_blight/
```

Any number of class names is supported. Keep the validation split reproducible by
using the same seed.

For a single unsplit directory, put the class folders directly under `data/raw/`;
the training command will create a stratified split automatically.

## Setup and usage

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Train the baseline:

```bash
python -m src.tomato_leaf_detection.train \
  --data-dir data/raw \
  --output models/best.pt \
  --epochs 5
```

Run the interface:

```bash
streamlit run app.py
```

The app accepts a trained checkpoint path through the sidebar. Until a checkpoint
exists, it still validates uploaded images and explains the next required step
instead of returning a misleading prediction.

## Planned next milestones

1. **50%:** train on the selected tomato leaf dataset and add reproducible metrics,
   confusion matrix, and error analysis.
2. **75%:** add Grad-CAM visual explanations and compare model architectures.
3. **100%:** test the complete application, document limitations, and package
   deployment.
