# Week 3 Assignment: Breast Cancer Wisconsin Dataset Analysis

## I 320D: Data Science for Biomedical Informatics | Spring 2026

### 📋 Assignment Version C

---

## 🎯 This Week's Mantra

> **"Every Column Tells a Story"**

In this assignment, you'll apply the 10-Point Data Inspection to a real-world medical imaging dataset focused on breast cancer diagnosis. By the end, you'll understand not just *what* the data contains, but *why* each variable matters for clinical decision-making.

---

## Learning Objectives

By completing this assignment, you will be able to:

1. ✅ Apply the systematic 10-Point Inspection to a new healthcare dataset
2. ✅ Identify and classify feature types (continuous, discrete, categorical, ordinal)
3. ✅ Detect and document data quality issues (missing values, unexpected values)
4. ✅ Research and document clinical meaning for healthcare variables
5. ✅ Create meaningful data groupings based on clinical standards
6. ✅ Formulate answerable research questions about cancer diagnosis factors

---

## About the Dataset

**Dataset:** Wisconsin Diagnostic Breast Cancer (WDBC)  
**Source:** UCI Machine Learning Repository / Kaggle  
**File:** `data.csv`  
**Target Variable:** `diagnosis` (M = Malignant, B = Benign)

### Clinical Context

Breast cancer is the most common cancer among women worldwide, affecting about 2.3 million women annually according to the World Health Organization (WHO). This dataset contains features computed from digitized images of fine needle aspirate (FNA) of breast masses. The features describe characteristics of the cell nuclei present in the image.

Understanding these variables is crucial for:

- Computer-aided diagnosis (CAD) systems
- Early detection of malignant tumors
- Reducing unnecessary biopsies
- Supporting clinical decision-making in oncology

### Feature Categories

The dataset contains **30 numeric features** organized into three measurement types for each of **10 characteristics**:

| Suffix | Meaning | Description |
|--------|---------|-------------|
| `_mean` | Mean | Average value across all nuclei in the image |
| `_se` | Standard Error | Variation in measurements |
| `_worst` | Worst/Largest | Mean of the three largest values |

The **10 cell nuclei characteristics** measured are:
- **radius** - mean distance from center to points on the perimeter
- **texture** - standard deviation of gray-scale values
- **perimeter** - boundary length of the nucleus
- **area** - area of the nucleus
- **smoothness** - local variation in radius lengths
- **compactness** - (perimeter² / area) - 1.0
- **concavity** - severity of concave portions of the contour
- **concave points** - number of concave portions of the contour
- **symmetry** - symmetry of the nucleus
- **fractal dimension** - "coastline approximation" - 1

---

## Getting Started

First, load the dataset and import your libraries:

```python
# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load the dataset
df = pd.read_csv('Data/data.csv')

# Display first few rows to confirm it loaded
print(df.head())

```

---

## Part 1: The 10-Point Data Inspection (40 points)

Complete each inspection step and document your findings.

### Step 1: Shape (4 points)

**Your Code:**
```python
# Step 1
print('Print the "Data Shape":\nNumber of Rows, Number of Features:')
print(df.shape)
```

**Your Findings:**
- How many rows (observations/patients)? 569
- How many columns (features)? 33
- What does each row represent in clinical terms? Each row represents a cytological sample (a sample of cells) from an individual's breast cancer.

---

### Step 2: Column Names (4 points)

**Your Code:**
```python
# Step 2
print("List of columns:\n")
print(df.columns)
```
```python
# Extract and display only the base feature names (without _mean, _se, _worst)
raw_features = str(df.columns)
processed_features = raw_features.strip('Index')
processed_features = processed_features.replace('\n','')
processed_features = processed_features.replace(',','\n')
processed_features = processed_features.split('\n')
def ProcessText(features):
    max_runs = (len(processed_features)-1)
    x = 0
    for i in processed_features:
        processed_features[x] = i.strip("([ ])")
        processed_features[x] = processed_features[x].replace("_se","")
        processed_features[x] = processed_features[x].replace("_mean","")
        processed_features[x] = processed_features[x].replace("_worst","")
        if x == max_runs:
            return processed_features
        else:
            x += 1
features_processed = ProcessText(processed_features)
print(features_processed)
```

**Your Findings:**
- List all column names:
['id', 'diagnosis', 'radius_mean', 'texture_mean', 'perimeter_mean',
       'area_mean', 'smoothness_mean', 'compactness_mean', 'concavity_mean',
       'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
       'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
       'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se',
       'fractal_dimension_se', 'radius_worst', 'texture_worst',
       'perimeter_worst', 'area_worst', 'smoothness_worst',
       'compactness_worst', 'concavity_worst', 'concave points_worst',
       'symmetry_worst', 'fractal_dimension_worst', 'Unnamed: 32']

- Do you notice any pattern in the column naming convention?
```
The naming pattern is suffix-based:

The columns that end with _mean are showing the average (mean) of the feature value across the sample.

The columns that end with _se are showing the "standard error" of the feature or the variability/spread of that feature's measurements.

The columns that end with _worst are showing the largest/most severe value of the feature.
```
- Which columns might need further research to understand?
```
Some columns that may need further research are compactness, concavity, concave points, and fractal_dimension. These values come from specific nuclear geometry computations rather than direct measurements.
```

---

### Step 3: Data Types (4 points)

**Your Code:**
```python
# Step 3
print("Features:                 Data Type:\n")
print(df.dtypes)
```

**Your Findings:**
- Which columns are numeric (int64 or float64)?
   - All of the columns are numeric except for `diagnosis` and the final column which is unnamed (`id` is int64 while the remaining columns are float64)  

- Which columns are categorical (object/string)?
   - The `diagnosis` column is an "object" type  

- Are there any data types that seem incorrect?
   - The final column is unnamed and has no values in any of the rows. However, this column is still counted as float64 and all of the values are NaN. We will take care of this column later on.
---

### Step 4: First Look (4 points)

**Your Code:**
```python
# Step 4
print("First Few Rows:\n")
print(df.head())
```

**Your Findings:**
- What do the actual values look like?  
   - Most of the values are floating point numbers and a significant amount of them are **<1**
- Do you notice anything unusual or unexpected?
   - Only the previously mentioned unnamed column with no values.

- What are the possible values for the `diagnosis` column?
   - **"M"** for malignant or **"B"** for benign.

---

### Step 5: Last Look (4 points)

**Your Code:**
```python
# Step 5
print("Last Few Rows:\n")
print(df.tail())
```

**Your Findings:**
- This data ends clearly
- The last rows **do** seem consistent with the first rows.

---

### Step 6: Memory Usage (4 points)

**Your Code:**
```python
# Step 6
print("Features:                 MemoryUsage:\n")
print(df.memory_usage(deep=True))
print("\nTotal usage (bytes):")
print(df.memory_usage(deep=True).sum())
```

**Your Findings:**
- How much memory does the dataset use?
   - 174.246 KB
- Is this a "small" or "large" dataset by data science standards?
   - This is a small dataset as large ones can be multiple gigabytes.

---

### Step 7: Missing Values (4 points)

**Your Code:**
```python
# Step 7
print("Features:                Null Data:\n")
print(df.isnull().sum())
```

**Your Findings:**
- Which columns have missing values (according to `.isnull()`)?
   - Only the final (blank) column
- What percentage of each column is missing?
   - 0% for all of the expected columns

- ⚠️ **IMPORTANT:** Do you notice any columns that appear to be entirely empty or have suspicious patterns?
   - Unnamed: 32

---

### Step 8: Duplicates (4 points)

**Your Code:**
```python
# Step 8
print("Identify Duplicate Rows:\n")
feature_check = "id"
x = df.duplicated(subset=[feature_check])
if df.duplicated().any():
    print(f"❌ There are some duplicated rows in the dataset.")
else:
    print(f"✅ The dataset has no duplicated rows.")
if x.any():
    print(f"❌ There are some duplicated values in the `{feature_check}` column.")
else:
    print(f"✅ The `{feature_check}` column has no duplicated values.")
```

**Your Findings:**
- Are there any duplicate rows? The dataset has no duplicated rows.
- Are all patient IDs unique? Yes. The `id` column has no duplicated values.

---

### Step 9: Basic Statistics (4 points)

**Your Code:**
```python
# Step 9
print("Overview / Summary of Data:\n")
print(df.describe())
```

**Your Findings:**
- What is the radius_mean range in the dataset? 6.981000 to 28.110000
- What is the range of area_mean values? 143.500000 to 2501.000000
- What is the range of concavity_mean values? 0.000000 to 0.426800
- Do any min/max values seem impossible or clinically unlikely? No, none of the data seems clinically unlikely.

---

### Step 10: Unique Counts (4 points)

**Your Code:**
```python
# Step 10
print("Number of Unique Values:")
print("Features:                 Unique Values:\n")
print(df.nunique())
```

**Your Findings:**
- Which columns have very few unique values (likely categorical)? Only the diagnosis column.

- Which columns have many unique values (likely continuous)? All of the other columns have many unique values. `fractal_dimension_se` has the most with 545.

- Does the number of unique IDs match the number of rows? Yes there are 569 unique values and 569 rows.

---

## Part 2: Data Dictionary (20 points)

Complete the following data dictionary for the **key columns**. For each column, you must:
1. **Research** the clinical meaning
2. **Identify** the feature type (Continuous, Discrete, Categorical-Nominal, Categorical-Ordinal, Binary, Identifier)
3. **Document** the valid values/range you observe
4. **Note** any issues or questions

| Column | Description | Feature Type | Valid Values/Range | Notes/Issues |
|--------|-------------|--------------|-------------------|--------------|
| `id` |Unique identifier| int64 |>0 (5-8 digits)|Unique per sample|
| `diagnosis` |Benign `B` or malignant `M`|Object|`M`, `B`|212 `M`, 357 `B`|
| `radius_mean` |Average distance from the center of the cell to its perimeter|float64|Non-negative numbers|Smaller are often benign in this dataset|
| `texture_mean` |standard deviation of gray-scale values within the nucleus|float64|Non-negative numbers|How "rough" the nucleus appears|
| `perimeter_mean` |Average length of the cell's perimeter|float64|Non-negative numbers| |
| `area_mean` |Average area if the nucleus|float64|Non-negative numbers|Larger area = bigger cells|
| `smoothness_mean` |Local variation in nuclear contour|float64|Non-negative numbers|Irregularity|
| `compactness_mean` |Measure of how "compact" or dense the nucleus shape is|float64|Non-negative numbers|perimeter² / area − 1.0|
| `concavity_mean` |Severity of inward indentations/concavities|float64|Non-negative numbers|Depth of dents|
| `concave points_mean` |Number of of inward indentations/concavities|float64|Non-negative numbers|Count of depths|
| `symmetry_mean` |How symmetric the nuclear contours are|float64|Non-negative numbers|1.0 = Perfect symmetry (>1.0: Possible if implementation allows (e.g., asymmetric distortion metrics))|
| `fractal_dimension_mean` |Measures the roughness/complexity of the nuclear boundary using fractal scaling principles|float64|Non-negative numbers|Theoretical minimum is ~0|

### Clinical Research Questions for Version C

Answer these questions based on your research (you may need to use Google):

**1. What is cell morphology in the context of cancer diagnosis? Why is the shape of cell nuclei an important indicator of malignancy?**

Your answer: Morphology is the cells external structure, shape, size, and generally how it looks.
---

**2. Explain what "concavity" and "concave points" measure. Why might cancer cells have more irregular, concave boundaries?**

Your answer: Concavity and concave points measure the amount and severity of indentations in the nucleus. Cancer cells develop more irregular concave boundaries based on a number of factors including dysregulated growth mechanics and genomic instability.

---

**3. What is pleomorphism in cancer cells? How does it relate to the variation measurements (standard error) in this dataset?**

Your answer: Pleomorphism is the variation in cell size and shape within a tumor sample. The variation measurements directly quantify pleomorphism.

---

**4. How do pathologists traditionally examine FNA samples? What advantages does computational analysis provide over manual examination?**

Your answer: Pathologists traditionally examine FNA samples using microscopes. Benefits of computational analysis include speed and accuracy when compared to human eyes.

---

## Part 3: Data Validation (15 points)

### 3.1 Diagnosis Distribution Validation (5 points)

Write code to check:
- How many patients have malignant (M) tumors?
- How many patients have benign (B) tumors?
- What is the percentage of each?

**Your Code:**
```python
dx_counts = df['diagnosis'].value_counts().tolist()
dx_m_count = dx_counts[1]
dx_b_count = dx_counts[0]
dx_count_all = dx_b_count + dx_m_count
print(f"Malignant (M): {dx_m_count} ({(dx_m_count/dx_count_all):.2%}) \nBenign    (B): {dx_b_count} ({(dx_b_count/dx_count_all):.2%})")

```

**Your Findings:**

- Is this dataset balanced or imbalanced between the two classes?  
This dataset is weighted towards the Benign diagnosis with just under 2/3 of the cases.


- In the real world, what percentage of breast biopsies are malignant vs benign?  
According to the Breast Cancer Research Foundation, roughly 75% of biopsies performed in the U.S. are benign¹.

1.Brown J. What Is a Breast Biopsy? Breast Cancer Research Foundation. March 21, 2025. Accessed February 12, 2026. https://www.bcrf.org/about-breast-cancer/breast-biopsy/
---

### 3.2 Empty Column Validation (5 points)

Write code to examine all columns for any that might be completely empty or contain only null values.

**Your Code:**
```python
null_summary = df.isnull().sum()
empty_columns = null_summary[null_summary == len(df)].index.tolist()
print(empty_columns)
```

**Your Findings:**

- Did you find any columns that are entirely empty?  
There is one empty column in this dataset. This is due to trailing commas in the csv  file. The following code block will drop this before we begin the analysis.

- What should you do with such columns before analysis?  
This column is unintended so we will simply drop it.
- Why might an empty column exist in a dataset?  
This is due to trailing commas in the csv  file.
---

### 3.3 Feature Range Validation (5 points)

Write code to check if the "worst" measurements are always greater than or equal to the "mean" measurements for the same characteristic.

**Your Code:**
```python
col_map = {
    'radius': ('radius_mean', 'radius_worst'),
    'texture': ('texture_mean', 'texture_worst'),
    'perimeter': ('perimeter_mean', 'perimeter_worst'),
    'area': ('area_mean', 'area_worst'),
    'smoothness': ('smoothness_mean', 'smoothness_worst'),
    'compactness': ('compactness_mean', 'compactness_worst'),
    'concavity': ('concavity_mean', 'concavity_worst'),
    'concave points': ('concave points_mean', 'concave points_worst'),  # Space!
    'symmetry': ('symmetry_mean', 'symmetry_worst'),
    'fractal_dimension': ('fractal_dimension_mean', 'fractal_dimension_worst')
}

violations = 0
for feature, (mean_col, worst_col) in col_map.items():
    # Verify columns exist
    if mean_col in df.columns and worst_col in df.columns:
        viol = (df[worst_col] < df[mean_col]).sum()
        violations += viol
        # print(f"{worst_col} >= {mean_col}: {viol} violations")
    else:
        print(f"Missing: {mean_col} or {worst_col}")

print(f"\nTotal violations: {violations}")
```

**Your Findings:**

- Does `radius_worst` always >= `radius_mean`?  
`radius_worst` **is** always >= `radius_mean`

- Does this relationship hold for other features?  
**All** features that have a worst/mean column follow this rule.

- What would it mean if this relationship was violated?  
If this relationship was violated there would likely be an issue with the data.

---

## Part 4: Create Cell Irregularity Groups (10 points)

Create a new column called `irregularity_category` that categorizes tumors into clinically-meaningful groups based on `concavity_mean` (a key measure of cell shape irregularity).

### Version C: Morphological Irregularity Categories

Use these categories based on observed concavity values:

| Irregularity Category | Concavity Range | Clinical Rationale |
|-----------------------|-----------------|-------------------|
| Smooth | 0 - 0.03 | Minimal concavity, regular cell boundaries |
| Mild | 0.03 - 0.08 | Some irregularity, often seen in benign tumors |
| Moderate | 0.08 - 0.15 | Notable irregularity, warrants attention |
| Severe | 0.15 - 0.25 | High irregularity, suspicious for malignancy |
| Extreme | > 0.25 | Very irregular, strong indicator of malignancy |

### Your Code:

```python
# Create the irregularity_category column
# You can use a custom function with .apply() OR pd.cut()
# Remember: if using pd.cut(), you'll need to handle the upper bound
bins = [0, 0.035, 0.085, 0.155, 0.255, np.inf]
labels = ['Smooth:', 'Mild:', 'Moderate:', 'Severe:', 'Extreme:']
df['concavity_category'] = pd.cut(df['concavity_mean'], bins=bins, labels=labels, include_lowest=True)

```

### Verify your groupings worked:

```python
# Show counts per irregularity category
print(df['concavity_category'].value_counts().sort_index())
```

### Calculate malignancy rate by irregularity category:

```python
# Calculate the percentage of malignant diagnoses in each irregularity category
# Blank vars to store data
category_counts = {}
malignancy_data = []
malignancy_category_count = 0
benign_category_count = 0

# Loop through the categories to calculate counts and percentages
for category in df['concavity_category'].cat.categories:
    count = len(df[df['concavity_category'] == category])
    category_counts[category] = count
    malignant_in_category = len(df[(df['concavity_category'] == category) & (df['diagnosis'] == 'M')])
    benign_in_category = count - malignant_in_category 
    malignancy_category_count += malignant_in_category
    benign_category_count += benign_in_category
    malignancy_percent = (malignant_in_category/count)
    malignancy_percent_string = f"{malignancy_percent:0.2%}"
    benign_percent = (benign_in_category/count)
    benign_percent_string = f"{benign_percent:0.2%}"
    
    malignancy_data.append(malignancy_percent)
    print(f"{category}: {count} cases ({malignancy_percent_string} Malignant)")

# Print total cases and percentages
total_case_count = malignancy_category_count + benign_category_count
print(f"\nTotal malignant: {malignancy_category_count} ({(malignancy_category_count/total_case_count):.2%})")
print(f"Total benign: {benign_category_count} ({(benign_category_count/total_case_count):.2%})")
print("Total cases:", total_case_count)
```

### Analysis Questions:

**1. How many tumors are in each irregularity category?**

Your answer:
    Smooth:      172  
    Mild:        167  
    Moderate:    125  
    Severe:       83  
    Extreme:      22  
---

**2. What is the malignancy rate (percentage) for each irregularity category?**

Your answer:
    Smooth:    2.91%  
    Mild:     12.57%  
    Moderate: 68.80%  
    Severe:   97.59%  
    Extreme:  86.36%  
---

**3. At what level of concavity does malignancy rate sharply increase? Does cell shape irregularity appear to be a strong predictor of cancer?**

Your answer:
    Moderate.
---

**4. Why might severely irregular cell boundaries be associated with malignancy? (Think about how cancer cells grow and divide.)**

Your answer:
    As the cells grow they rapidly change and deform.
---

## Part 5: Research Questions (15 points)

### 5.1 Write Three Answerable Questions (9 points)

Write three questions that THIS dataset can answer. Remember: the data can show relationships and patterns, but cannot prove causation.

**Your questions must explore these specific areas:**

1. **A question about smoothness and diagnosis:**
How does the average smoothness (smoothness_mean) differ between benign (B) and malignant (M) tumors?

---

2. **A question comparing "concavity" vs "concave points":**
Do tumors with high concavity (concavity_mean) but few concave points (concave points_mean) show a different malignancy rate than tumors with many concave points but lower concavity?

---

3. **A question about fractal dimension combined with another feature:**
Among tumors with similar nuclear size (radius_mean), is a higher fractal_dimension_mean associated with a higher proportion of malignant cases?

---

### 5.2 Identify One Question the Data CANNOT Answer (3 points)

Write one question about **genetic factors or family history** that this dataset cannot answer, and explain why.

**Question:**
Are patients with a family history of breast cancer more likely to have malignant tumors than patients without such a family history?

**Why it cannot be answered with this data:**
This dataset only contains measurements derived from cell images. We do not know anything else about the affected patients.

---

### 5.3 Grouping Analysis (3 points)

Answer this question using a groupby analysis:

**"What is the average concave points_mean for each diagnosis category (M vs B)?"**

**Your Code:**
```python
result = df.groupby('diagnosis')['concave points_mean'].mean()
print(result)
```

**Your Interpretation:**

How many more concave points do malignant tumors have on average compared to benign tumors? What does this suggest about the diagnostic value of this feature?  
On average the malignant tumors have 0.062273 more concave points_mean. This is about 3x more, meaning this is a strong point to look at when comparing malignant vs benign cases from this dataset.

---

## Part 6: Target Variable Analysis (Bonus - 5 points)

The `diagnosis` column is our **target variable** - what we're trying to predict. Analyze its relationship with key features.

**Your Code:**
```python
# Show the distribution of diagnosis
# Calculate summary statistics for at least 3 key features, grouped by diagnosis
# 1. Show the distribution of diagnosis
print("Diagnosis distribution (counts):")
print(df["diagnosis"].value_counts())
print("\nDiagnosis distribution (proportions):")
print(df["diagnosis"].value_counts(normalize=True))

# 2. Calculate summary statistics for key features, grouped by diagnosis
key_features = ["radius_mean", "concavity_mean", "concave points_mean"]

group_summary = df.groupby("diagnosis")[key_features].describe()
print("\nSummary statistics for key features grouped by diagnosis:")
print(group_summary)

```

### Bonus Questions:

**1. What percentage of patients in this dataset have malignant tumors?**

Your answer:  
      37.26%
---

**2. Which feature shows the largest difference between malignant and benign tumors?**

Your answer:  
      radius_mean. This is because as the cancer cells progress the radius grows.
---

**3. Why does class imbalance matter for machine learning classification? (You may need to research this)**

Your answer:  
      Class imbalance matters because it can make a classifier look “good” overall while actually doing a poor job on the minority (often most important) class. This can lead to misleading results.
---

**4. If you were building a diagnostic model, which 3 features would you prioritize based on your analysis? Justify your choices.**

Your answer:
      I would pick radius_mean, symmetry_mean, and concavity_mean.
         Radius is the best predictor. I would then add symmetry because malignant cells are significantly less likely to be symmetrical. Finally I would add concavity mean because malignant cells are likely to have more intense concavity.
---

## Submission Checklist

Before submitting, verify you have completed:

- [ ] **Part 1:** All 10 inspection steps with code AND written findings
- [ ] **Part 2:** Complete data dictionary with 12 key columns filled in
- [ ] **Part 2:** Answered all 4 clinical research questions
- [ ] **Part 3:** All 3 validation checks with code and answers
- [ ] **Part 4:** Created `irregularity_category` column using **Morphological Irregularity Categories**
- [ ] **Part 4:** Calculated malignancy rate by irregularity category with interpretation
- [ ] **Part 5:** Three research questions (smoothness, concavity vs concave points, fractal dimension)
- [ ] **Part 5:** One unanswerable question about genetic factors/family history
- [ ] **Part 5:** concave points_mean by diagnosis groupby analysis
- [ ] **Bonus (Optional):** Target variable analysis

---

## Grading Rubric

| Component | Points | Requirements for Full Credit |
|-----------|--------|------------------------------|
| Part 1: 10-Point Inspection | 40 | All 10 steps complete with working code AND thoughtful written analysis |
| Part 2: Data Dictionary | 20 | All 12 columns documented with correct feature types and clinical research |
| Part 3: Data Validation | 15 | All validation checks complete with working code and insightful answers |
| Part 4: Irregularity Groups | 10 | Working code that creates correct groups AND meaningful interpretation |
| Part 5: Research Questions | 15 | Three good questions in specified areas, one clear limitation, groupby analysis complete |
| **Bonus:** Target Analysis | +5 | Thoughtful analysis with real-world connection |
| **Total** | 100 (+5 bonus) | |

---

## Hints (Read Before You Get Stuck!)

### ⚠️ Common Pitfalls:

1. **One column appears to be entirely empty** (all NaN values)
   - Check the last column carefully
   - This often happens with CSV exports that have trailing commas
   - You should drop this column before analysis

2. **The diagnosis column uses single letters** - "M" and "B"
   - Don't forget what these stand for when interpreting results
   - You may need to convert to 0/1 for some calculations

3. **Concavity has minimum value of 0** - some tumors have no concave regions
   - This is valid data, not an error
   - Make sure your bins capture the 0 values

4. **Continuous features** - most features in this dataset are continuous
   - Think carefully about appropriate grouping strategies

### 💡 Pro Tips:

- Use `value_counts()` liberally to understand categorical columns
- Use `value_counts(dropna=False)` to see if there are any null values
- When using `pd.cut()` with custom bins, use `include_lowest=True` and add a bin for values above your max (e.g., `float('inf')`)
- The `describe()` method works best with numeric columns
- For comparing groups, `groupby().mean()` is your friend

---

## Useful Resources

- **UCI ML Repository - Original Dataset:** https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)
- **Kaggle Dataset Page:** https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin-data
- **American Cancer Society - Breast Cancer:** https://www.cancer.org/cancer/breast-cancer.html
- **Cell Morphology in Cancer:** https://www.ncbi.nlm.nih.gov/books/NBK164700/
- **Pandas Documentation:** https://pandas.pydata.org/docs/

---

*Remember: "Every Column Tells a Story" - your job is to figure out what that story is!*

---

**Due Date:** [See Canvas]

**Submission:** Upload your completed Jupyter notebook (.ipynb) to Canvas
