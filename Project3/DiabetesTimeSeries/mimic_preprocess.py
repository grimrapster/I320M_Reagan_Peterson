"""
mimic_preprocess.py

One-time preprocessing script. Reads raw MIMIC-IV hosp/ CSV files and outputs
three cleaned CSVs that match the Kaggle pipeline column structure exactly, so
the notebook requires zero changes downstream.

Run locally once, then upload the three output CSVs to Google Drive.

Usage:
    python mimic_preprocess.py

Output files (written to OUTPUT_DIR):
    mimic_lab_results.csv   — HbA1c measurements for T2D patients
    mimic_patients.csv      — Patient demographics + comorbidity flags
    mimic_outcomes.csv      — 30-day readmission per hospital admission
"""

from pathlib import Path
import pandas as pd
import numpy as np

# ── Configuration ──────────────────────────────────────────────────────────────
INPUT_DIR  = Path("data/Mimic")    # Directory containing the MIMIC-IV hosp/ .csv.gz files
OUTPUT_DIR = Path(".")             # Where to write the three output CSVs

HBAC1_ITEMID = 50852              # MIMIC-IV itemid for HbA1c (Hemoglobin A1c)
CHUNK_SIZE   = 500_000            # Rows per chunk when streaming labevents

# Comorbidity ICD code prefixes: output_column → (icd9_prefixes, icd10_prefixes)
# These mirror the dx_ columns in the Kaggle patients.csv
COMORBIDITIES = {
    "dx_hypertension":            (["401", "402", "403", "404", "405"], ["I10", "I11", "I12", "I13", "I14", "I15"]),
    "dx_hyperlipidemia":          (["272"],                              ["E78"]),
    "dx_obesity":                 (["2780"],                             ["E66"]),
    "dx_coronary_artery_disease": (["410", "411", "412", "413", "414"], ["I20", "I21", "I22", "I23", "I24", "I25"]),
    "dx_heart_failure":           (["428"],                              ["I50"]),
    "dx_chronic_kidney_disease":  (["585"],                              ["N18"]),
    "dx_depression":              (["2962", "2963", "311"],              ["F32", "F33"]),
    "dx_anxiety":                 (["3000"],                             ["F41"]),
}

# ── Step 1: Identify T2D patients from diagnoses ───────────────────────────────
print("=" * 60)
print("Step 1: Loading diagnoses_icd...")
print("=" * 60)

diag = pd.read_csv(
    INPUT_DIR / "diagnoses_icd.csv.gz",
    compression="gzip",
    dtype={"icd_code": str}
)
diag["icd_code"] = diag["icd_code"].str.strip()

# Type 2 diabetes:
#   ICD-9: 250.x0 and 250.x2 stored without decimal → 25000, 25002, 25010, ...
#          5-digit codes starting with 250 where last digit is 0 or 2
#   ICD-10: E11.x → any code starting with E11
icd9_t2d_mask = (
    (diag["icd_version"] == 9) &
    (diag["icd_code"].str.startswith("250")) &
    (diag["icd_code"].str.len() == 5) &
    (diag["icd_code"].str[-1].isin(["0", "2"]))
)
icd10_t2d_mask = (
    (diag["icd_version"] == 10) &
    (diag["icd_code"].str.startswith("E11"))
)

t2d_ids = set(diag.loc[icd9_t2d_mask | icd10_t2d_mask, "subject_id"])
print(f"T2D patients identified: {len(t2d_ids):,}")

# ── Step 2: Stream labevents, keep only HbA1c rows for T2D patients ────────────
print()
print("=" * 60)
print("Step 2: Streaming labevents (this will take several minutes)...")
print("=" * 60)

hba1c_chunks = []
rows_read = 0

for chunk in pd.read_csv(
    INPUT_DIR / "labevents.csv.gz",
    compression="gzip",
    chunksize=CHUNK_SIZE,
    usecols=["subject_id", "itemid", "charttime", "valuenum", "flag"],
    dtype={"flag": str},
    low_memory=False,
):
    filtered = chunk[
        (chunk["itemid"] == HBAC1_ITEMID) &
        (chunk["subject_id"].isin(t2d_ids)) &
        (chunk["valuenum"].notna()) &
        (chunk["valuenum"] > 0)
    ].copy()

    if len(filtered) > 0:
        hba1c_chunks.append(filtered)

    rows_read += len(chunk)
    print(f"  {rows_read:>12,} rows scanned | {sum(len(c) for c in hba1c_chunks):,} HbA1c records collected", end="\r")

print()

hba1c_raw = pd.concat(hba1c_chunks, ignore_index=True)
print(f"HbA1c records for T2D patients: {len(hba1c_raw):,}")
print(f"Unique T2D patients with HbA1c: {hba1c_raw['subject_id'].nunique():,}")

# ── Step 3: Format lab results to match Kaggle structure ──────────────────────
print()
print("=" * 60)
print("Step 3: Formatting lab results...")
print("=" * 60)

lab_results = hba1c_raw.rename(columns={
    "subject_id": "patient_id",
    "charttime":  "test_date",
    "valuenum":   "value",
})
lab_results["test_name"]   = "HbA1c"
lab_results["is_abnormal"] = (lab_results["flag"].str.lower().str.strip() == "abnormal").astype(int)
lab_results = lab_results[["patient_id", "test_name", "test_date", "value", "is_abnormal"]]

print(f"Rows: {len(lab_results):,}")
print(f"Date range: {lab_results['test_date'].min()} → {lab_results['test_date'].max()}")
print(f"HbA1c value range: {lab_results['value'].min():.1f} – {lab_results['value'].max():.1f}%")

# ── Step 4: Build patients table with comorbidity flags ───────────────────────
print()
print("=" * 60)
print("Step 4: Building patients table with comorbidity flags...")
print("=" * 60)

patients_raw = pd.read_csv(
    INPUT_DIR / "patients.csv.gz",
    compression="gzip",
    usecols=["subject_id"]
)
patients_out = (
    patients_raw[patients_raw["subject_id"].isin(t2d_ids)]
    .copy()
    .rename(columns={"subject_id": "patient_id"})
)
patients_out["dx_type2_diabetes"] = 1

# Build per-patient ICD code sets (vectorized, not apply)
diag_t2d = diag[diag["subject_id"].isin(t2d_ids)].copy()

icd9_per_patient  = (
    diag_t2d[diag_t2d["icd_version"] == 9]
    .groupby("subject_id")["icd_code"]
    .apply(set)
)
icd10_per_patient = (
    diag_t2d[diag_t2d["icd_version"] == 10]
    .groupby("subject_id")["icd_code"]
    .apply(set)
)

for col, (icd9_prefixes, icd10_prefixes) in COMORBIDITIES.items():
    icd9_prefixes_tuple  = tuple(icd9_prefixes)
    icd10_prefixes_tuple = tuple(icd10_prefixes)

    def has_comorbidity(pid, p9=icd9_prefixes_tuple, p10=icd10_prefixes_tuple):
        codes9  = icd9_per_patient.get(pid, set())
        codes10 = icd10_per_patient.get(pid, set())
        return int(
            any(c.startswith(p9)  for c in codes9) or
            any(c.startswith(p10) for c in codes10)
        )

    patients_out[col] = patients_out["patient_id"].map(has_comorbidity)
    print(f"  {col}: {patients_out[col].mean()*100:.1f}% prevalence")

# ── Step 5: Compute 30-day readmission ────────────────────────────────────────
print()
print("=" * 60)
print("Step 5: Computing 30-day readmission...")
print("=" * 60)

admissions = pd.read_csv(
    INPUT_DIR / "admissions.csv.gz",
    compression="gzip",
    usecols=["subject_id", "hadm_id", "admittime", "dischtime"],
    parse_dates=["admittime", "dischtime"]
)
admissions = (
    admissions[admissions["subject_id"].isin(t2d_ids)]
    .sort_values(["subject_id", "admittime"])
    .copy()
)

# Next admission time within each patient
admissions["next_admittime"] = admissions.groupby("subject_id")["admittime"].shift(-1)
admissions["readmitted_30d"] = (
    (admissions["next_admittime"] - admissions["dischtime"]).dt.days
    .between(0, 30, inclusive="both")
).astype(int)

outcomes = admissions[["subject_id", "hadm_id", "readmitted_30d"]].rename(
    columns={"subject_id": "patient_id"}
)

overall_rate = outcomes["readmitted_30d"].mean() * 100
print(f"Admissions: {len(outcomes):,}")
print(f"Overall 30-day readmission rate: {overall_rate:.1f}%")

# ── Step 6: Save output CSVs ──────────────────────────────────────────────────
print()
print("=" * 60)
print("Step 6: Saving output files...")
print("=" * 60)

lab_results.to_csv(OUTPUT_DIR / "mimic_lab_results.csv", index=False)
print(f"  mimic_lab_results.csv  — {len(lab_results):,} rows")

patients_out.to_csv(OUTPUT_DIR / "mimic_patients.csv", index=False)
print(f"  mimic_patients.csv     — {len(patients_out):,} rows")

outcomes.to_csv(OUTPUT_DIR / "mimic_outcomes.csv", index=False)
print(f"  mimic_outcomes.csv     — {len(outcomes):,} rows")

print()
print("Done. Upload the three CSV files to Google Drive.")
