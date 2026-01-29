# Week 3 Practice Problems: The 10-Point Inspection
## Wisconsin Breast Cancer Dataset

**Course:** I 320D: Data Science for Biomedical Informatics  
**Mantra:** "Every Column Tells a Story"

---

## Introduction

You have been provided with the **Wisconsin Breast Cancer Dataset**, a classic biomedical dataset used for cancer diagnosis classification. The dataset contains features computed from digitized images of fine needle aspirate (FNA) of breast masses. These features describe characteristics of cell nuclei present in the images.

Your current notebook runs the basic 10-point inspection commands, but it's missing the most important part: **interpretation and clinical context**. Your task is to add cells that demonstrate you understand what the data is telling you.

**Instructions:**
- Add new markdown and code cells AFTER each existing inspection step
- Answer all questions in markdown cells
- Remember: Running code is not enough — you must interpret the results!

---

## PART 1: Interpret the 10-Point Inspection

For each existing inspection in your notebook, add interpretation cells.

---

### Problem 1: Shape Interpretation

**Your notebook shows:** `(569, 33)`

**Add a markdown cell answering:**

1. How many patient samples (tumor biopsies) are in this dataset?
2. How many features are measured for each sample?
3. Look at the last column name (`Unnamed: 32`). What might this indicate about the original data file?
4. **Clinical Context:** Is 569 samples a large or small dataset for training a cancer diagnosis model? What are the implications?

---

### Problem 2: Column Names Analysis

**Your notebook shows:** 33 columns including `id`, `diagnosis`, and 30 measurement features

**Add a markdown cell answering:**

1. What is the **target variable** (what we're trying to predict)?
2. The measurement columns follow a pattern: `[feature]_mean`, `[feature]_se`, `[feature]_worst`. What do you think these suffixes represent?
   - `_mean`: ?
   - `_se`: ? (Hint: SE stands for "Standard Error")
   - `_worst`: ?
3. List the 10 base features being measured (without the suffixes). What do these features describe about cell nuclei?
4. Which column should NOT be used for prediction and why?

**Add a code cell to:**
```python
# Extract and display only the base feature names (without _mean, _se, _worst)
# YOUR CODE HERE
```

---

### Problem 3: Data Types Deep Dive

**Your notebook shows:** 1 object column, 1 int64 column, 31 float64 columns

**Add a markdown cell answering:**

1. Which column is stored as `object` (text)? What values does it contain?
2. Why is `id` stored as `int64` while all measurements are `float64`?
3. The column `Unnamed: 32` is `float64` but has 0 unique values and all NaN. What should we do with it?
4. Should `diagnosis` be converted to a numeric type for machine learning? If so, what encoding would you use?

**Add a code cell to:**
```python
# Check the unique values in the 'diagnosis' column
# YOUR CODE HERE
```

---

### Problem 4: First Look (Head) Clinical Interpretation

**Your notebook shows:** First 5 rows of data

**Add a markdown cell answering:**

1. In the first 5 rows, what is the diagnosis for each patient? (M = Malignant, B = Benign)
2. Look at `radius_mean` values. What is the range in these 5 samples? 
3. Do malignant tumors (M) appear to have larger or smaller radius values in these samples?
4. **Warning:** Why shouldn't we draw conclusions from just 5 samples?

---

### Problem 5: Last Look (Tail) Pattern Detection

**Your notebook shows:** Last 5 rows of data

**Add a code cell to display the last 10 rows:**
```python
# Display last 10 rows instead of 5
# YOUR CODE HERE
```

**Add a markdown cell answering:**

1. What is the diagnosis distribution in the last 10 rows?
2. Does the data appear to be sorted by any particular column? How can you tell?
3. Is there any indication of data quality issues at the end of the file?

---

### Problem 6: Memory Usage Calculation

**Your notebook is MISSING this step!**

**Add a code cell:**
```python
# Calculate memory usage in megabytes
print("Memory Usage Analysis:")
print(f"Total memory: {df.memory_usage(deep=True).sum() / 1e6:.2f} MB")
print(f"\nMemory by column:")
print(df.memory_usage(deep=True).sort_values(ascending=False).head(10))
```

**Add a markdown cell answering:**

1. How many megabytes does this dataset use?
2. Which column uses the most memory? Why?
3. Would this dataset cause memory problems on a typical laptop?
4. If you had a similar dataset with 1 million patients, how much memory would it need?

---

### Problem 7: Missing Values Investigation

**Your notebook is MISSING this step!**

**Add a code cell:**
```python
# Check for missing values
print("Missing Values per Column:")
print(df.isnull().sum())
print(f"\nTotal missing values: {df.isnull().sum().sum()}")
print(f"\nPercentage missing by column:")
print((df.isnull().sum() / len(df) * 100).round(2))
```

**Add a markdown cell answering:**

1. Which column has ALL missing values? 
2. What should you do with this column?
3. Are there any missing values in the actual measurement columns?
4. **Clinical Importance:** Why is it significant that measurement data has no missing values?

**Add a code cell to remove the problematic column:**
```python
# Remove the Unnamed: 32 column and verify
# YOUR CODE HERE
# Then re-check df.shape to confirm
```

---

### Problem 8: Duplicate Detection

**Your notebook shows:** `df.duplicated()` output but doesn't summarize it

**Add a code cell:**
```python
# Count duplicates properly
print(f"Number of duplicate rows: {df.duplicated().sum()}")
print(f"Number of duplicate IDs: {df['id'].duplicated().sum()}")

# If duplicates exist, display them
if df.duplicated().sum() > 0:
    print("\nDuplicate rows:")
    print(df[df.duplicated(keep=False)])
```

**Add a markdown cell answering:**

1. Are there any duplicate rows in the dataset?
2. Is each patient `id` unique?
3. Why would duplicate patient records be a serious problem in a cancer diagnosis dataset?

---

### Problem 9: Statistical Summary Deep Dive

**Your notebook shows:** `df.describe()` output

**Add a markdown cell answering:**

**For `radius_mean`:**
1. What is the average tumor radius? (mean)
2. What is the range (min to max)?
3. What do the 25th and 75th percentiles tell us?

**For `area_mean`:**
1. The mean is 654.89 but the median (50%) is 551.10. What does this difference indicate about the distribution?
2. The max is 2501.0 while the 75th percentile is 782.7. What does this suggest?

**For `concavity_mean`:**
1. The minimum is 0.0. What does a concavity of 0 mean clinically?
2. How might concavity differ between benign and malignant tumors?

**Critical Observation:**
1. Look at the `Unnamed: 32` column in describe(). What do all the NaN values confirm?

---

### Problem 10: Unique Values & Cardinality

**Your notebook shows:** `df.nunique()` output

**Add a markdown cell answering:**

1. `id` has 569 unique values. What does this confirm?
2. `diagnosis` has 2 unique values. What are they?
3. `Unnamed: 32` has 0 unique values. Why is this possible?
4. Which measurement feature has the HIGHEST cardinality? Which has the LOWEST?
5. Why do continuous measurements have high cardinality while categorical variables have low cardinality?

---

## PART 2: Data Validation

Add these validation checks to ensure data quality.

---

### Problem 11: Validate the Target Variable

**Add a code cell:**
```python
# Check diagnosis distribution
print("Diagnosis Distribution:")
print(df['diagnosis'].value_counts())
print(f"\nPercentage:")
print(df['diagnosis'].value_counts(normalize=True) * 100)
```

**Add a markdown cell answering:**

1. How many tumors are Malignant (M)? How many are Benign (B)?
2. What percentage of tumors are malignant?
3. Is this dataset balanced or imbalanced? 
4. **Clinical Context:** In the general population, what percentage of breast biopsies are typically malignant? Does this dataset reflect that?

---

### Problem 12: Validate Measurement Ranges

**Add a code cell:**
```python
# Check for impossible values in key measurements
print("=== Radius Validation ===")
print(f"Negative radius values: {(df['radius_mean'] < 0).sum()}")
print(f"Zero radius values: {(df['radius_mean'] == 0).sum()}")
print(f"Range: {df['radius_mean'].min():.2f} to {df['radius_mean'].max():.2f}")

print("\n=== Area Validation ===")
print(f"Negative area values: {(df['area_mean'] < 0).sum()}")
print(f"Zero area values: {(df['area_mean'] == 0).sum()}")

print("\n=== Smoothness Validation (should be 0-1 range) ===")
print(f"Values > 1: {(df['smoothness_mean'] > 1).sum()}")
print(f"Values < 0: {(df['smoothness_mean'] < 0).sum()}")
print(f"Range: {df['smoothness_mean'].min():.4f} to {df['smoothness_mean'].max():.4f}")
```

**Add a markdown cell answering:**

1. Are there any physically impossible values (negative radius, negative area)?
2. Is the smoothness measurement within a reasonable range?
3. What would you do if you found negative radius values?

---

### Problem 13: Check for Outliers

**Add a code cell:**
```python
# Identify potential outliers using IQR method for area_mean
Q1 = df['area_mean'].quantile(0.25)
Q3 = df['area_mean'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df['area_mean'] < lower_bound) | (df['area_mean'] > upper_bound)]
print(f"Number of outliers in area_mean: {len(outliers)}")
print(f"Lower bound: {lower_bound:.2f}, Upper bound: {upper_bound:.2f}")
print(f"\nOutlier diagnoses:")
print(outliers['diagnosis'].value_counts())
```

**Add a markdown cell answering:**

1. How many statistical outliers exist in `area_mean`?
2. Are the outliers mostly Malignant or Benign tumors?
3. **Clinical Insight:** Should these outliers be removed? Why or why not?

---

## PART 3: Feature Type Classification

---

### Problem 14: Create a Data Dictionary

**Add a code cell to create a data dictionary:**
```python
# Create a summary data dictionary
import pandas as pd

# After removing Unnamed: 32, categorize the remaining columns
data_dict = {
    'Column': ['id', 'diagnosis', 'radius_mean', '... (continue for all)'],
    'Description': ['Unique patient identifier', 'Tumor classification', 'Mean radius of cell nuclei', '...'],
    'Feature_Type': ['Identifier', 'Categorical (Binary)', 'Continuous', '...'],
    'Role': ['Drop', 'Target', 'Predictor', '...'],
    'Notes': ['Do not use in model', 'M=Malignant, B=Benign', 'Measured in ?', '...']
}

# YOUR CODE: Complete the data dictionary for at least 10 columns
```

**Add a markdown cell with a complete table for at least these columns:**

| Column | Description | Feature Type | Role | Notes |
|--------|-------------|--------------|------|-------|
| id | | | | |
| diagnosis | | | | |
| radius_mean | | | | |
| texture_mean | | | | |
| perimeter_mean | | | | |
| area_mean | | | | |
| smoothness_mean | | | | |
| compactness_mean | | | | |
| concavity_mean | | | | |
| concave points_mean | | | | |

---

## PART 4: Clinical Groupings

---

### Problem 15: Compare Malignant vs Benign

**Add a code cell:**
```python
# Compare mean values between Malignant and Benign tumors
comparison = df.groupby('diagnosis')[['radius_mean', 'texture_mean', 'perimeter_mean', 
                                       'area_mean', 'smoothness_mean', 'concavity_mean']].mean()
print("Mean values by diagnosis:")
print(comparison.round(3))

print("\n\nRatio (Malignant / Benign):")
print((comparison.loc['M'] / comparison.loc['B']).round(2))
```

**Add a markdown cell answering:**

1. Which features show the BIGGEST difference between M and B?
2. For `concavity_mean`, malignant tumors average about how many times higher than benign?
3. Which feature shows the SMALLEST difference?
4. **Clinical Interpretation:** Why might malignant tumors have higher concavity?

---

### Problem 16: Create Size Categories

**Add a code cell:**
```python
# Create tumor size categories based on area_mean
# Using clinical-inspired thresholds
def categorize_size(area):
    if area < 400:
        return 'Small'
    elif area < 700:
        return 'Medium'
    elif area < 1000:
        return 'Large'
    else:
        return 'Very Large'

df['size_category'] = df['area_mean'].apply(categorize_size)

# Analyze diagnosis by size category
print("Diagnosis by Tumor Size:")
print(pd.crosstab(df['size_category'], df['diagnosis']))
print("\n")
print("Percentage Malignant by Size:")
print(pd.crosstab(df['size_category'], df['diagnosis'], normalize='index').round(3) * 100)
```

**Add a markdown cell answering:**

1. What percentage of "Small" tumors are malignant?
2. What percentage of "Very Large" tumors are malignant?
3. Does tumor size appear to be a strong predictor of malignancy?
4. **Caution:** Can we conclude that large tumors CAUSE malignancy?

---

## PART 5: Research Questions

---

### Problem 17: Questions Your Data CAN Answer

**Write THREE questions this dataset can answer, then pick one to explore:**

Example questions:
- "Is there a correlation between tumor radius and area?"
- "Do malignant tumors have higher symmetry variance than benign tumors?"
- "Which single feature best distinguishes malignant from benign tumors?"

**Add a code cell exploring ONE of your questions:**
```python
# YOUR CODE HERE - explore one question with code and visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Example: correlation between radius and area
# YOUR CODE HERE
```

---

### Problem 18: Questions Your Data CANNOT Answer

**Write TWO questions this dataset CANNOT answer and explain why:**

Consider limitations like:
- Missing information (patient demographics, treatment history)
- Temporal constraints (no follow-up data)
- Causation vs. correlation
- Sample selection

---

## PART 6: Clean Up & Summary

---

### Problem 19: Create a Clean Dataset

**Add a code cell:**
```python
# Create a clean version of the dataset
df_clean = df.drop(columns=['Unnamed: 32', 'id']).copy()

# Encode diagnosis as numeric
df_clean['diagnosis_numeric'] = df_clean['diagnosis'].map({'M': 1, 'B': 0})

print(f"Clean dataset shape: {df_clean.shape}")
print(f"\nColumn types:")
print(df_clean.dtypes.value_counts())
print(f"\nReady for machine learning: {df_clean.isnull().sum().sum() == 0}")
```

---

### Problem 20: Executive Summary

**Add a final markdown cell with an executive summary:**

Write a 5-7 sentence summary covering:
1. What is this dataset about?
2. How many samples and features?
3. What data quality issues did you find and fix?
4. What is the target variable and its distribution?
5. What features appear most predictive?
6. What are the limitations of this dataset?

---

## Submission Checklist

Before submitting, verify your notebook contains:

- [ ] Interpretation cells after EACH of the original 10 inspection steps
- [ ] Memory usage calculation (Problem 6) — this was missing!
- [ ] Missing values analysis (Problem 7) — this was missing!
- [ ] `Unnamed: 32` column removed with explanation
- [ ] Diagnosis distribution analysis
- [ ] Validation checks for impossible values
- [ ] Outlier analysis with clinical interpretation
- [ ] Data dictionary for at least 10 columns
- [ ] Malignant vs. Benign comparison
- [ ] At least one clinical grouping created
- [ ] 3 answerable + 2 unanswerable questions
- [ ] Clean dataset ready for modeling
- [ ] Executive summary

---

## Rubric Preview

| Component | Points | Criteria |
|-----------|--------|----------|
| 10-Point Interpretation (1-10) | 35 | Complete interpretation for each step |
| Missing Steps Added (6-7) | 10 | Memory usage + missing values analysis |
| Data Validation (11-13) | 15 | Validates ranges, identifies outliers |
| Data Dictionary (14) | 10 | Accurate feature types and descriptions |
| Clinical Analysis (15-16) | 15 | M vs B comparison + meaningful groupings |
| Research Questions (17-18) | 10 | Distinguishes answerable/unanswerable |
| Clean Dataset & Summary (19-20) | 5 | Ready for ML + clear summary |

---

**Remember:** "Every Column Tells a Story" 

In this dataset, each column describes a characteristic of cell nuclei that pathologists use to diagnose cancer. Your job is to understand what these measurements mean and how they relate to diagnosis!
