# Data 200 Applied Statistical Analysis - Project
## "Exploring Real-World Data through Statistical and Predictive Modeling"

---

## 📊 Project Overview

**Topic:** Nepal Nutrition Indicators - Statistical Analysis of Child Health Metrics

**Dataset:** WHO Global Health Observatory (GHO) Nutrition Indicators for Nepal

**Problem Statement:** Analyze Nepal's child nutrition indicators (stunting, wasting, underweight, breastfeeding practices, anaemia prevalence) to identify trends, relationships between demographic factors, and statistical patterns that can inform public health interventions.

---

## 📁 Project Structure

```
data200-hallucinators/
├── data/
│   ├── raw/                  # Raw WHO nutrition data for Nepal
│   └── processed/            # Cleaned dataset (ready for analysis)
├── scripts/
│   ├── 01_inspect_data.py     # Initial data inspection
│   ├── 02_clean_data.py        # Data cleaning pipeline
│   └── 03_verify_cleaned_data.py  # Verification of cleaned data
├── outputs/
│   ├── visualizations/        # EDA plots and charts
│   ├── models/                # Saved statistical models
│   └── statistics/            # Test results and statistics
├── Week-1/                    # Group formation & topic finalization
├── Week-2/                    # Literature review & dataset selection
├── Week-3/                    # Exploratory Data Analysis
├── Week-4/                    # Statistical model selection & hypothesis
├── Week-5/                    # Statistical analysis & validation
├── Week-6/                    # Statistical modeling (continued)
├── Week-7/                    # Python application development
├── Week-8/                    # Peer evaluation & final presentation
├── Evaluation/               # Evaluation criteria documentation
│   ├── 01-Dataset-Problem-Definition/
│   ├── 02-EDA-Preprocessing/
│   ├── 03-Statistical-Modeling/
│   ├── 04-Application-Development/
│   └── 05-Presentation-Collaboration/
└── TeamInfo/                  # Team information & task division
```

---

## 📋 Dataset Description

**Source:** WHO Global Health Observatory (GHO) - Nepal Nutrition Indicators

**File:** `data/raw/nutrition_indicators_npl.csv`

### Columns:
| Column | Description |
|--------|-------------|
| `indicator_code` | WHO GHO indicator code |
| `indicator` | Full indicator name |
| `indicator_url` | WHO data portal URL |
| `year` | Year of measurement |
| `start_year` | Reporting period start |
| `end_year` | Reporting period end |
| `region_code` | WHO region code (SEAR = South-East Asia) |
| `region` | Region name |
| `country_code` | ISO country code (NPL = Nepal) |
| `country` | Country name |
| `dimension_type` | Category type (SEX, WEALTHQUINTILE, RESIDENCEAREA, etc.) |
| `dimension_code` | Specific dimension code |
| `dimension_name` | Human-readable dimension name |
| `numeric_value` | Numeric indicator value |
| `value` | String formatted value with CI |
| `low` | Lower confidence interval |
| `high` | Upper confidence interval |

### Key Indicators Analyzed:
1. **Stunting** - Prevalence of children under 5 with height-for-age < -2 SD
2. **Wasting** - Prevalence of children under 5 with weight-for-height < -2 SD
3. **Underweight** - Prevalence of children under 5 with weight-for-age < -2 SD
4. **Overweight** - Prevalence of children with BMI > +2 SD
5. **Anaemia** - Prevalence in children aged 6-59 months
6. **Breastfeeding** - Exclusive breastfeeding, early initiation, minimum acceptable diet
7. **Low Birth Weight** - LBW prevalence percentage
8. **Obesity** - Adult and child obesity prevalence

### Data Dimensions:
- **Sex:** Male, Female, Both sexes
- **Wealth Quintile:** Q1 (Poorest) to Q5 (Richest)
- **Residence Area:** Urban, Rural, Total
- **Education Level:** Primary, Secondary, Higher, Total
- **Age Groups:** Various child age groups

---

## 🔬 Statistical Methods Used

### Week 4-5: Hypothesis Testing & Statistical Analysis
- **Linear Regression:** Trend analysis of nutrition indicators over time
- **ANOVA:** Differences in nutrition indicators across demographic groups
- **Correlation Analysis:** Relationships between different nutrition indicators
- **T-tests:** Mean comparison between groups (male/female, urban/rural)

### Week 6: Statistical Modeling
- **Multiple Linear Regression:** Predicting stunting/wasting based on socioeconomic factors
- **Logistic Regression:** Probability of meeting minimum acceptable diet
- **Model Diagnostics:** R-squared, residual analysis, VIF for multicollinearity

---

## 📅 Weekly Progress

| Week | Topic | Status |
|------|-------|--------|
| Week 1 | Group Formation & Topic Finalization | ✅ Complete |
| Week 2 | Literature Review & Dataset Selection | ✅ Complete |
| Week 3 | Exploratory Data Analysis (EDA) | ✅ Complete |
| Week 4 | Statistical Model Selection & Hypothesis | ✅ Complete |
| Week 5 | Statistical Analysis & Validation | ✅ Complete |
| Week 6 | Statistical Modeling (Continued) | ✅ Complete |
| Week 7 | Python Application Development | ✅ Complete |
| Week 8 | Peer Evaluation & Final Presentation | 🔄 In Progress |

---

## 🚀 How to Run

### 1. Setup Environment
```bash
pip install -r requirements.txt
```

### 2. Run Data Cleaning
```bash
python scripts/02_clean_data.py
```

### 3. Run EDA Analysis
```bash
python Week-3/01_eda_analysis.py
```

### 4. Generate Visualizations
```bash
python Week-3/02_visualizations.py
```

### 5. Run Statistical Tests
```bash
python Week-5/01_statistical_tests.py
```

### 6. Build Statistical Models
```bash
python Week-5/02_regression_models.py
```

### 7. Launch Python Application
```bash
streamlit run Week-7/app.py
```

---

## 📊 Key Findings

*(To be filled after analysis)*

### Main Insights:
1. Stunting prevalence shows declining trend over 1998-2022
2. Wasting rates vary significantly by sex and wealth quintile
3. Breastfeeding initiation rates improve with maternal education
4. Anaemia prevalence correlates with low birth weight rates

---

## 👥 Team Members

| Name | Role | Tasks |
|------|------|-------|
| Member 1 | Data Analyst | EDA, Statistical Analysis |
| Member 2 | Model Developer | Regression, ANOVA, Hypothesis Testing |
| Member 3 | App Developer | Python Dashboard, Visualizations |

---

## 📚 Dependencies

```
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
seaborn>=0.12.0
scipy>=1.9.0
statsmodels>=0.13.0
sklearn>=1.2.0
streamlit>=1.20.0
plotly>=5.10.0
```

---

**Professor:** Data 200 Applied Statistical Analysis
**Institution:** (Your Institution Name)
**Date:** June 2026
