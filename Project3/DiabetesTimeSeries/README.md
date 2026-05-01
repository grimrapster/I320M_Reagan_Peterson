# Project 3: HbA1c Longitudinal Trend Clustering

**Course:** I320M  
**Author:** Reagan Peterson, Rian Kahlon

## Overview

This project clusters diabetic patients by their multi-year HbA1c time series to identify trajectory phenotypes (e.g., Improving, Deteriorating, Stable). Clustering uses Dynamic Time Warping (DTW) distance and k-medoids, validated against comorbidity profiles and 30-day readmission rates.

The pipeline runs on two datasets:
- **Kaggle synthetic dataset** — used for initial development
- **MIMIC-IV** — real clinical data from Beth Israel Deaconess Medical Center, used for replication and comparison

---

## Repository Structure

```
DiabetesTimeSeries/
├── Project3.ipynb          # Main analysis notebook
├── mimic_preprocess.py     # One-time preprocessing script for MIMIC-IV raw files
├── SPEC.md                 # Full project specification document
(Data is stored privately for compliance with MIMIC-IV)
```
---

## Setup

### Dependencies

Install required packages:

```bash
pip install kagglehub tslearn pandas numpy matplotlib scikit-learn-extra kmedoids seaborn
```
---
## Notebook Structure

| Cells | Section |
|-------|---------|
| 1–3 | Imports and Kaggle data download |
| 4–6 | Data wrangling and inclusion criteria |
| 7–8 | Data exploration and validation |
| 9–10 | Time series interpolation and matrix construction |
| 11–13 | Interpolation check and spaghetti preview |
| 14–18 | DTW distance matrix and k-medoids cluster selection (k=3–6) |
| 19–20 | Spaghetti plots per cluster (k=4) |
| 21–29 | Clinical validation: mean HbA1c, comorbidities, 30-day readmission |
| 30–31 | MIMIC-IV data import |
| 32–39 | MIMIC data wrangling and inclusion criteria |
| 40–42 | MIMIC interpolation and visualization |
| 43–47 | MIMIC DTW matrix and cluster selection |
| 48–49 | MIMIC spaghetti plots (k=3) |
| 50–57 | MIMIC clinical validation |

---

## Key Design Decisions

- **DTW over Euclidean distance:** HbA1c measurements are irregularly spaced and variable in count; DTW allows elastic alignment of trajectory shapes
- **Z-normalization per patient:** Clustering captures trajectory shape, not absolute HbA1c level
- **k=4 for Kaggle, k=3 for MIMIC:** Chosen by balancing silhouette score with clinical interpretability; MIMIC's 21% silhouette drop at k=4 was too large to justify the added complexity
- **365-day minimum span:** Per project specification; ensures at least one full year of diabetes management is captured
- **N_TIMEPOINTS=10:** Matches average measurement density in both datasets; consistent across both pipelines to ensure valid comparison

---

## Limitations

- 30-day readmission is all-cause; at an academic medical center, many admissions are unrelated to diabetes
- Comorbidity prevalence in MIMIC is inflated by comprehensive inpatient ICD coding
- MIMIC cohort skews toward actively-managed patients due to inclusion criteria
- Comorbidity set selected for Kaggle comparability, not clinical comprehensiveness

See `SPEC.md` for full details.
