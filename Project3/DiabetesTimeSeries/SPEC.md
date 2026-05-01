# Project 3 Specification: HbA1c Longitudinal Trend Clustering

**Author:** Reagan Peterson | Rian Kahlon
**Course:** I320M  
**Date:** 2026-04-30

---

## 1. Problem Statement

Diabetic patients do not all follow the same HbA1c trajectory over time. Some maintain stable glycemic control, others deteriorate gradually, and some improve after an initial period of poor control. Identifying these trajectory phenotypes from longitudinal HbA1c data can support personalized care planning and help predict readmission risk at a population level.

This project clusters diabetic patients by their multi-year HbA1c time series using Dynamic Time Warping (DTW) distance and k-medoids clustering, then validates the clinical coherence of the resulting clusters.

---

## 2. Data Sources

### 2.1 Synthetic Dataset (Kaggle)
- **Source:** `kagglehub.dataset_download("sergionefedov/patient-records-100k-patients-15-conditions")`
- **Purpose:** Initial pipeline development and exploratory analysis
- **Relevant tables:** `patients.csv`, `lab_results.csv`, `outcomes.csv`
- **Key columns:** `patient_id`, `test_name`, `test_date`, `value`, `is_abnormal`, `dx_type2_diabetes`, `readmitted_30d`
- **Limitation:** Synthetically generated; comorbidity flags and readmission labels may not reflect real clinical distributions

### 2.2 MIMIC-IV (Real Clinical Data)
- **Source:** PhysioNet MIMIC-IV hosp module, preprocessed via `mimic_preprocess.py`
- **Purpose:** Replication on real clinical data for cross-validation
- **Files used:** `diagnoses_icd.csv.gz`, `labevents.csv.gz`, `patients.csv.gz`, `admissions.csv.gz`
- **HbA1c item ID:** 50852 (Hemoglobin A1c, MIMIC-IV labevents)
- **T2D identification:** ICD-9 codes 250.x0/250.x2; ICD-10 codes E11.x
- **Preprocessed outputs:** `mimic_lab_results.csv`, `mimic_patients.csv`, `mimic_outcomes.csv`
- **Storage:** Google Drive (loaded via gdown in Colab)

---

## 3. Inclusion Criteria

Applied identically to both datasets:

| Criterion | Value | Rationale |
|-----------|-------|-----------|
| Minimum HbA1c measurements | 3 | Per project spec: "3 is probably your minimum threshold" |
| Minimum observation span | 365 days | Per project spec: "spanning at least 12 months"; one year captures a full cycle of routine diabetes management and aligns with clinical practice (HbA1c measured every 3–6 months) |
| Lab type | HbA1c only | Isolates the primary longitudinal biomarker for glycemic control |
| Diagnosis | Type 2 diabetes only | Identified via `dx_type2_diabetes` flag (Kaggle) or ICD codes (MIMIC) |

**No minimum HbA1c threshold was applied.** HbA1c below 6.5% in a T2D patient reflects successful treatment, not a data error — the 6.5% line is a diagnostic threshold, not a treatment threshold.

---

## 4. Data Pipeline

### 4.1 Preprocessing
1. Filter lab results to HbA1c only
2. Filter to T2D patient cohort
3. Sort chronologically within each patient
4. Apply inclusion criteria (≥3 measurements, ≥365-day span)

### 4.2 Time Series Representation
- **Interpolation:** Each patient's HbA1c series is linearly interpolated onto a uniform grid of `N_TIMEPOINTS = 10` evenly-spaced points
- **Time normalization:** Time axis mapped to [0, 1] relative to each patient's first and last measurement, so clustering captures trajectory *shape* independent of observation duration
- **Duplicate handling:** Multiple measurements on the same date are averaged before interpolation
- **Linear (not spline) interpolation:** Chosen because HbA1c data is sparse; higher-order interpolation would introduce artificial wiggles between real measurements

### 4.3 Z-Normalization
Each patient's series is z-normalized by their own mean and standard deviation:

```
X_znorm = (X_raw - patient_mean) / patient_std
```

This ensures clustering groups patients by trajectory *shape* rather than absolute HbA1c level. A patient stable at 9% and one stable at 7% have different clinical severity but the same trajectory pattern (flat). Patients with zero standard deviation (perfectly flat series) have their std replaced with 1.0 to avoid division by zero.

### 4.4 Distance Metric: Dynamic Time Warping
Euclidean distance is unsuitable for HbA1c trajectories because:
- Measurements are irregularly spaced in time
- Patients have different numbers of measurements
- A shifted but otherwise identical trajectory would appear very dissimilar under Euclidean distance

DTW allows elastic alignment of sequences, comparing trajectory shapes even when measurements don't occur at the same relative time points. The pairwise DTW distance matrix is computed using `tslearn.metrics.cdist_dtw`.

---

## 5. Clustering

### 5.1 Algorithm
- **Method:** K-medoids with FasterPAM algorithm (`kmedoids.fasterpam`)
- **Input:** Precomputed DTW distance matrix
- **Reproducibility:** `random_state=42`
- K-medoids was chosen over k-means because it operates on the precomputed distance matrix directly and produces actual patient exemplars (medoids) that can be clinically interpreted

### 5.2 Cluster Selection
K evaluated over range 3–6. Selection criteria:
- **Silhouette score** (higher = better): measures how well-separated clusters are
- **Davies-Bouldin index** (lower = better): measures average cluster compactness vs separation
- **Clinical interpretability:** statistical criteria are balanced against whether the resulting clusters are clinically meaningful and distinguishable

| Dataset | Chosen k | Rationale |
|---------|----------|-----------|
| Kaggle | 4 | Silhouette drop from k=3 to k=4 is only 6%; gains clinically meaningful distinction between trajectory subgroups |
| MIMIC | 3 | Silhouette drop from k=3 to k=4 is 21%; k=4 clusters were nearly identical in shape; real clinical data supports fewer distinct trajectory types |

### 5.3 Cluster Labels
Labels are assigned by visual inspection of spaghetti plots after clustering. This mirrors methodology in the clinical literature where trajectory phenotypes are labeled by expert review of cluster means. Labels are tied to `random_state=42` and would need re-verification if the seed or data changed.

**Kaggle clusters (k=4):**
- Worsened - Recovering
- Improved - Deteriorating
- Improving
- Deteriorating

**MIMIC clusters (k=3):**
- Improving
- Deteriorating
- Stable

---

## 6. Validation

### 6.1 Statistical
- Silhouette score and Davies-Bouldin index computed for k=3–6
- Results plotted side by side for visual comparison

### 6.2 Clinical Face Validity
- **Mean HbA1c per cluster:** bar chart with standard deviation error bars and clinical threshold lines (6.5% diagnostic, 8.0% poor control)
- **Comorbidity prevalence:** heatmap of 8 comorbidities across clusters (selected to match Kaggle dataset columns for direct comparison)
- **30-day readmission rate:** per-cluster admission counts and readmission percentages

### 6.3 Comorbidities Assessed
Hypertension, hyperlipidemia, obesity, coronary artery disease, heart failure, chronic kidney disease, depression, anxiety.

*Note: This set was selected to match the Kaggle dataset's available `dx_` columns, enabling direct comparison between datasets. It was not derived from a clinical literature review.*

---

## 7. Known Limitations

1. **All-cause readmission:** The 30-day readmission flag covers all hospital admissions regardless of reason. At an academic medical center (MIMIC/BIDMC), patients are frequently admitted for conditions unrelated to diabetes, inflating and obscuring diabetes-specific readmission risk. A future improvement would filter to diabetes-related primary diagnoses only.

2. **Comorbidity ascertainment in MIMIC:** ICD codes are captured from inpatient encounters, where coders document all known conditions comprehensively. This inflates comorbidity prevalence (e.g., 89–91% hypertension) compared to a general T2D population and reduces the discriminating power of comorbidity comparisons across clusters.

3. **MIMIC population bias:** Patients meeting the ≥3 measurements, ≥365-day span criteria at an academic medical center skew toward engaged, actively-managed patients. This selection effect may underrepresent poorly-controlled or disengaged patients.

4. **Comorbidity selection:** The eight comorbidities assessed were chosen for comparability with the Kaggle dataset, not based on clinical evidence. Microvascular complications specific to T2D (neuropathy, retinopathy) are absent.

5. **Linear interpolation:** For patients with measurements clustered at the start and end of their observation window, interpolated midpoints may not reflect true mid-period HbA1c values.

6. **N_TIMEPOINTS sensitivity:** The sensitivity of clustering results to the choice of N_TIMEPOINTS=10 was not formally tested.

---

## 8. Clinical Interpretation

### What each cluster represents and its intervention implication:

**Improving:** Patients with initially elevated HbA1c trending downward. Likely responding to treatment intensification. Intervention: maintain current management, monitor for sustained control.

**Deteriorating:** Patients with initially controlled HbA1c trending upward. May indicate treatment failure, medication non-adherence, or disease progression. Intervention: medication review, adherence support, specialist referral.

**Stable:** Patients with relatively flat trajectories. Sub-divide clinically by absolute HbA1c level — stable well-controlled patients need monitoring; stable poorly-controlled patients need treatment escalation despite trajectory stability.

---