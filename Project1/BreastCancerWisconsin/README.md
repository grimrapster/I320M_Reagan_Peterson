# Project 1: Breast Cancer Wisconsin Diagnostic Analysis

## MAIN FILES  
```
Cell_Irregularity_Inspection.ipynb # Assignment Main Notebook
Breast_Assignment_VersionC.md      # Assignment prompt & Answers
SPEC.md                            # Project specification document
```

## Overview

This project applies the 10-Point Data Inspection framework to and analyzes the Wisconsin Diagnostic Breast Cancer (WDBC) dataset. The dataset contains features computed from digitized images of fine needle aspirate (FNA) of breast masses, describing characteristics of cell nuclei used to classify tumors as malignant or benign.

---

## Dataset

**Source:** [Kaggle - Breast Cancer Wisconsin (Diagnostic)](https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin-data) | UCI Machine Learning Repository
**File:** `Data/data.csv`
**Samples:** 569 patient biopsies
**Target Variable:** `diagnosis` (M = Malignant, B = Benign)


## Project Structure

```
BreastCancerWisconsin/
├── Data/                              # Raw dataset
├── 10PointDataInspection.ipynb        # Systematic data inspection & validation
├── Cell_Irregularity_Inspection.ipynb # Assignment Main Notebook
├── Breast_Assignment_VersionC.md      # Assignment prompt
├── Breast_Cancer_Presentation.pdf     # Assignment presentation
├── breast_cancer_10point_problems.md  # Practice problems
└── SPEC.md                            # Project specification document
```

### Notebooks

- **`Cell_Irregularity_Inspection.ipynb`** — Focuses on morphological irregularity categorization using `concavity_mean`. Tumors are grouped into five categories (Smooth, Mild, Moderate, Severe, Extreme) and analyzed for malignancy rate per group.

---

## Specification

The project specification document ([`SPEC.md`](SPEC.md)) defines the full scope of the analysis including inputs, outputs, clarifying questions and decisions, acceptance criteria, and known constraints.

---

## Key Findings

- **Diagnosis distribution:** 357 benign (62.7%), 212 malignant (37.3%)
- **Data quality:** One empty column (`Unnamed: 32`) identified and removed; no missing values in measurement columns
- **Most predictive features:** Tumor `size` and `area`
- **Irregularity analysis:** Higher irregularity is correlated with higher malignancy rates
- **Malignant vs. benign:** Malignant tumors show notably higher concavity, area, and perimeter on average
