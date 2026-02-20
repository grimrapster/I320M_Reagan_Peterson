# Project Specification: Breast Cancer Wisconsin Diagnostic Analysis

**Course:** I320M - Data Science for Biomedical Informatics
**Assignment:** Week 3 - Assignment Version C
**Semester:** Spring 2026

---

## 1. Purpose

Apply the 10-Point Data Inspection framework to the Wisconsin Diagnostic Breast Cancer (WDBC) dataset to systematically assess data quality, understand feature structure, and explore the relationship between cell morphology and cancer diagnosis.

---

## 2. Inputs

| Input | Description |
|-------|-------------|
| `Data/data.csv` | Wisconsin Diagnostic Breast Cancer dataset (569 rows, 33 columns) |
| Python libraries | `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy` |

---

## 3. Outputs

| Output | Description |
|--------|-------------|
| `Cell_Irregularity_Inspection.ipynb` | Main deliverable — completed analysis notebook |
| `10PointDataInspection.ipynb` | Supporting inspection notebook |
| Malignancy rate bar chart | Horizontal bar chart of malignancy % by concavity category |
| Cleaned DataFrame | Dataset with `Unnamed: 32` dropped, ready for further analysis |

---

## 4. Scope

### In Scope
- 10-Point Data Inspection with code and written interpretation for each step
- Data dictionary for 12 key columns with clinical research
- Three data validation checks (diagnosis distribution, empty columns, feature range)
- Morphological irregularity categorization using `concavity_mean`
- Malignancy rate analysis by irregularity category
- Five research questions (three answerable, one unanswerable, one groupby)

### Out of Scope
- Machine learning model training or prediction
- Analysis of `_se` or `_worst` feature groups (focus is on `_mean` features)
- Patient-level demographic data (not present in dataset)

---

## 5. Clarifying Questions & Decisions

These questions were identified and resolved before implementation to ensure an unambiguous analysis.

---

**Q1: Should `Unnamed: 32` be dropped before or after the 10-Point Inspection?**

Decision: **After.** The column is documented during the inspection (Steps 2, 3, 7, 9, 10) to demonstrate awareness of the issue. It is then dropped at the start of Part 3 (Data Validation, Step 3.2) before any grouping or analysis is performed.

---

**Q2: Should `id` be used or dropped during analysis?**

Decision: **Kept in the raw DataFrame but not used analytically.** `id` serves as a uniqueness check (Step 8) and is excluded from all feature comparisons and groupings. It would be dropped before any machine learning use.

---

**Q3: What bin boundaries define the five irregularity categories?**

Decision: The assignment specifies the following ranges based on `concavity_mean`:

| Category | Range |
|----------|-------|
| Smooth | 0 – 0.034 |
| Mild | 0.035 – 0.084 |
| Moderate | 0.085 – 0.154 |
| Severe | 0.155 – 0.254 |
 | Extreme | > 0.255 |

Implementation uses `pd.cut()` with `include_lowest=True` and `np.inf` as the upper bound for Extreme to capture all values above 0.25.

---

**Q4: Should bin edges be inclusive on the lower or upper bound?**

Decision: **Lower-bound inclusive** (`include_lowest=True` in `pd.cut()`). This ensures that a `concavity_mean` of exactly 0 is captured in the Smooth category rather than falling outside the bins.

---

**Q5: How should the malignancy rate by category be visualized?**

Decision: **Horizontal bar chart** using `matplotlib`. Each bar represents one irregularity category, the x-axis shows malignancy percentage (0–100%), and bars are color-coded from light (low risk) to dark red (high risk). Percentage labels are displayed to the right of each bar.

---

**Q6: What counts as a "meaningful" clarifying question for the research questions section?**

Decision: Research questions must be answerable using only the available columns in `data.csv`. Questions about causation, patient history, genetics, or follow-up outcomes are explicitly out of scope and used as examples of unanswerable questions.

---

**Q7: How should the diagnosis distribution be assessed for balance?**

Decision: Compare dataset proportions (37.26% M, 62.74% B) against real-world biopsy data. Per the Breast Cancer Research Foundation, ~75% of U.S. biopsies are benign — making this dataset slightly more weighted toward malignant cases than real-world prevalence, but not severely imbalanced.

---

## 6. Acceptance Criteria

The project is considered complete when:

- [✅] All 10 inspection steps contain both working code **and** written interpretation
- [✅] `Unnamed: 32` is identified, documented, and dropped before analysis
- [✅] Data dictionary covers all 12 required columns with correct feature types
- [✅] All 4 clinical research questions are answered
- [✅] Diagnosis distribution, empty column check, and feature range validation are complete
- [✅] `irregularity_category` column is created with the correct 5-level categorization
- [✅] Malignancy rate is calculated and visualized per category
- [✅] All 4 analysis questions in Part 4 are answered with interpretation
- [✅] 3 answerable research questions are written in specified topic areas
- [✅] 1 unanswerable question about genetic/family history is identified with explanation
- [✅] `concave points_mean` groupby by diagnosis is complete with interpretation

---

## 7. Known Constraints & Assumptions

- The dataset contains one artifact column (`Unnamed: 32`) caused by trailing commas in the CSV export — this is expected and not a data error
- `concavity_mean` minimum of 0.0 is valid (some tumors have no concave regions) and is not treated as missing data
- All measurement features are assumed to be non-negative by clinical definition; no negative values were found during validation
- The dataset is treated as a static snapshot — no temporal or longitudinal analysis is applicable
