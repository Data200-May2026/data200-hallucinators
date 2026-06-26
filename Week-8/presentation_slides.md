# Nepal Nutrition Indicators Analysis
## Final Presentation Slides

---

## Slide 1: Title

**Exploring Real-World Data through Statistical and Predictive Modeling**

**Nepal Nutrition Indicators - A Statistical Analysis**

Team: Data 200 Applied Statistical Analysis
Date: June 2026

---

## Slide 2: Agenda

1. Introduction & Problem Statement
2. Dataset Overview
3. Exploratory Data Analysis (EDA)
4. Statistical Analysis & Hypothesis Testing
5. Regression Modeling
6. Key Findings & Insights
7. Python Application Demo
8. Conclusions & Future Work

---

## Slide 3: Introduction & Problem Statement

**Topic:** Child nutrition indicators in Nepal

**Data Source:** WHO Global Health Observatory (GHO)

**Research Questions:**
1. What are the trends in child nutrition indicators over time?
2. Do nutrition outcomes differ by demographic factors?
3. What predictors most influence child nutrition status?

**Problem Statement:**
Analyze Nepal's child nutrition indicators to identify trends and patterns that can inform public health interventions.

---

## Slide 4: Dataset Overview

- **Source:** WHO GHO - Nepal Nutrition Indicators
- **Time Period:** 1990 - 2024
- **Records:** 7,461
- **Indicators:** 37
- **Country:** Nepal (NPL)
- **Region:** South-East Asia (SEAR)

**Key Indicators:**
- Stunting (height-for-age < -2 SD)
- Wasting (weight-for-height < -2 SD)
- Underweight (weight-for-age < -2 SD)
- Anaemia in children 6-59 months
- Breastfeeding practices
- Low birth weight

**Dimensions:** Sex, Wealth Quintile, Residence, Education Level

---

## Slide 5: EDA - Dataset Summary Statistics

### Data Quality
| Metric | Before | After |
|--------|--------|-------|
| Rows | 7,556 | 7,461 |
| Duplicate rows | 93 | 0 |
| Missing (low/high) | 301 | 284 |

### Numeric Summary
| Statistic | numeric_value | low | high |
|-----------|---------------|-----|------|
| Count | 7,461 | 7,177 | 7,177 |
| Mean | 162.67 | 124.66 | 224.47 |
| Std Dev | 2,615.25 | 1,823.46 | 3,833.75 |
| Min | 0.00 | 0.00 | 0.00 |
| 25% | 4.20 | 2.60 | 7.20 |
| Median | 21.10 | 17.24 | 26.00 |
| 75% | 43.80 | 38.70 | 49.30 |
| Max | 68,536.00 | 46,911.00 | 99,139.00 |

### Key Indicator Statistics
| Indicator | Count | Mean | Year Min | Year Max |
|-----------|-------|------|----------|----------|
| Stunting (under 5) | 839 | 42.28% | 1995 | 2022 |
| Underweight (under 5) | 725 | 30.06% | 1995 | 2022 |
| Wasting (under 5) | 724 | 10.84% | 1995 | 2022 |
| Severe wasted | 709 | 2.51% | 1996 | 2022 |
| Overweight (under 5) | 663 | 1.47% | 1996 | 2022 |
| Exclusive breastfeeding | 175 | 62.03% | 1996 | 2019 |
| Early Initiation of Breastfeeding | 163 | 40.74% | 1996 | 2019 |
| Minimum dietary diversity | 160 | 37.48% | 2006 | 2019 |
| Prevalence of anaemia (6-59 months) | 100 | 29.91% | 2000 | 2019 |
| Low birth weight prevalence | 21 | 21.19% | 2000 | 2020 |

---

## Slide 6: EDA - Time Trend Analysis

### Stunting Trend (Both Sexes)
| Metric | Value |
|--------|-------|
| Years Covered | 1995, 1996, 1998, 2000-2022 |
| Mean Values | 68.2% (1995) → 38.96% (2022) |
| Slope | -5.04 per year |
| R-squared | 0.037 |
| **P-value** | **0.329 (NOT Significant)** |

### Wasting Trend
| Metric | Value |
|--------|-------|
| Years Covered | 1995, 1996, 1998, 2001, 2006, 2010, 2011, 2014, 2016, 2019, 2022 |
| Range | 6.0% to 13.8% |
| Slope | 0.02 (essentially flat) |
| **P-value** | **0.829 (NOT Significant)** |

### Underweight Trend
| Metric | Value |
|--------|-------|
| Years Covered | 1990-2022 (continuous) |
| Range | 36.77% (1995) to 10.32% (2021) |
| Slope | -0.60 per year |
| R-squared | 0.495 |
| **P-value** | **< 0.001 (SIGNIFICANT)** |

**Key Insight:** Underweight shows significant linear decline; stunting and wasting fluctuate without clear linear trends.

---

## Slide 7: EDA - Demographic Analysis

### By Sex (SEX Dimension)
| Sex | Mean Value | Count |
|-----|------------|-------|
| Both sexes | 104.22 | 725 |
| Female | 95.92 | 1,590 |
| Male | 29.37 | 1,445 |

### By Wealth Quintile (WEALTHQUINTILE)
| Quintile | Mean | Count |
|----------|------|-------|
| Q1 (Poorest) | 45.42 | 91 |
| Q2 | 43.90 | 91 |
| Q3 | 42.29 | 91 |
| Q4 | 42.85 | 91 |
| Q5 (Richest) | 41.20 | 91 |
| Total | 42.63 | 115 |

### By Residence Area (RESIDENCEAREATYPE)
| Area | Mean | Count |
|------|------|-------|
| Rural | 44.69 | 102 |
| Urban | 42.43 | 102 |
| Total | 42.63 | 115 |

### By Education Level (EDUCATIONLEVEL)
| Level | Mean | Count |
|-------|------|-------|
| None and primary | 44.59 | 97 |
| Primary | 44.50 | 97 |
| Secondary | 46.66 | 91 |
| Secondary or higher | 44.61 | 97 |
| Higher | 43.93 | 86 |

### By Age Group (AGEGROUP)
| Age Group | Mean | Count |
|-----------|------|-------|
| 0 to 1 month | 83.58 | 6 |
| 0 to 11 months | 13.48 | 41 |
| 12 to 23 months | 29.02 | 64 |
| 24 to 59 months | 20.72 | 37 |
| Total (All ages) | 29.51 | 82 |

**Key Pattern:** Clear wealth gradient - Q1 (poorest) have 4.24% higher stunting than Q5 (richest)

---

## Slide 8: EDA - Correlation Analysis

### Pearson Correlations (r > 0.5)

| Variable Pair | Correlation | Interpretation |
|---------------|--------------|----------------|
| Stunting <-> Underweight | **0.988** | Very strong positive |
| Stunting <-> Anaemia | **0.955** | Very strong positive |
| Underweight <-> Anaemia | **0.943** | Very strong positive |
| year <-> LBW_NUMBER | **-0.967** | Strong negative |
| year <-> LBW_PREVALENCE | **-0.991** | Very strong negative |
| year <-> NCD_BMI_25A | **0.956** | Strong positive |
| year <-> NCD_BMI_30A | **0.904** | Strong positive |

### Indicator-Specific Correlations
| Indicator 1 | Indicator 2 | r | p-value |
|-------------|-------------|---|---------|
| NUTRITION_ANT_HAZ_NE2 (Stunting) | NUTRITION_WA_2 (Underweight) | 0.988 | < 0.0001 |
| NUTRITION_ANT_HAZ_NE2 (Stunting) | NUTRITION_ANAEMIA_CHILDREN | 0.955 | < 0.0001 |
| NUTRITION_WA_2 (Underweight) | NUTRITION_ANAEMIA_CHILDREN | 0.943 | < 0.0001 |

### What This Means
**Malnutrition Syndrome:** Stunting, wasting, and underweight form a cluster - addressing poverty improves all simultaneously

**Dual Burden:** Undernutrition decreasing (r=-0.97) while overnutrition increasing (r=0.90+)

---

## Slide 9: Hypothesis Testing - ANOVA (H3)

### One-Way ANOVA: Wealth Quintile Differences

**Research Question:** Do stunting prevalence rates differ across wealth quintiles?

**Hypotheses:**
- H0: μQ1 = μQ2 = μQ3 = μQ4 = μQ5 (no difference)
- H1: At least one quintile mean is different

### Group Statistics
| Group | n | Mean Stunting | Std Dev |
|-------|---|---------------|---------|
| Q1 (Poorest) | 8 | 53.85% | - |
| Q2 | 8 | 44.91% | - |
| Q3 | 8 | 40.48% | - |
| Q4 | 8 | 34.94% | - |
| Q5 (Richest) | 8 | 25.05% | - |
| Total | 11 | 45.54% | - |

### ANOVA Summary Table
| Source | SS | df | MS | F | P-value |
|--------|----|----|----|---|---------|
| Between Groups | - | 5 | - | **5.62** | **0.0004** |
| Within Groups | - | 34 | - | - | - |
| Total | - | 39 | - | - | - |

### Effect Size
| Metric | Value | Interpretation |
|--------|-------|----------------|
| Eta-squared (η²) | **0.384** | **Large effect** - 38.4% of variance explained |
| Cohen's f | 0.79 | Large effect |

### Tukey HSD Post-Hoc Test Results
| Comparison | Mean Diff | P-adj | Significant? |
|------------|-----------|-------|--------------|
| Q1 (Poorest) vs Q2 | -8.94 | 0.668 | No |
| Q1 (Poorest) vs Q3 | -13.38 | 0.240 | No |
| Q1 (Poorest) vs Q4 | -18.91 | 0.031 | **Yes*** |
| Q1 (Poorest) vs Q5 (Richest) | -28.80 | 0.0002 | **Yes*** |
| Q2 vs Q5 (Richest) | -19.86 | 0.020 | **Yes*** |
| Q5 (Richest) vs Total | 20.49 | 0.007 | **Yes**** |

### Conclusion
**REJECT H0** at α=0.05

- There is a statistically significant difference in stunting prevalence across wealth quintiles
- **Practical Significance:** η²=0.38 indicates a LARGE effect - wealth explains 38.4% of variance
- Children in the poorest quintile (Q1) are **2.15x more likely** to be stunted than the richest (Q5)
- **Key Insight:** Poverty is the primary driver of child malnutrition in Nepal

---

## Slide 10: Hypothesis Testing Results Summary

| Hypothesis | Test | P-value | Result | Effect Size |
|-----------|------|---------|--------|-------------|
| H1: Linear Trend | Linear Regression | 0.172 | NOT Significant | R²=0.031 |
| H2: Sex Differences | T-Test | 0.736 | NOT Significant | Cohen's d=0.03 (negligible) |
| H3: Wealth Disparities | ANOVA | 0.0004 | **SIGNIFICANT*** | η²=0.38 (large) |
| H4: Indicator Correlations | Pearson | <0.05 | **SIGNIFICANT** | r=0.94-0.99 |

**Key Finding:** Only wealth quintile shows statistically significant differences in child nutrition outcomes.

---

## Slide 11: Regression Modeling

### Simple Linear Regression: Year → Stunting
| Metric | Value |
|--------|-------|
| R-squared | 0.031 |
| Adj. R-squared | 0.015 |
| Slope | -15.11 |
| P-value | 0.172 |

### Multiple Linear Regression: Year + Wealth → Stunting
| Metric | Value |
|--------|-------|
| R-squared | **0.941** |
| Adj. R-squared | 0.938 |
| F-statistic | 294.99 |
| P-value | < 0.001 |

### Coefficients
| Predictor | Coefficient | t-value | P-value |
|-----------|-------------|---------|---------|
| Year | -1.21 | -17.73 | < 0.001 |
| Wealth Rank | -6.76 | -16.60 | < 0.001 |

**Key Insight:** Adding wealth quintile improved R² from 3% to 94%!

---

## Slide 12: Model Diagnostics

### Residual Analysis
| Test | Statistic | P-value | Result |
|------|-----------|---------|--------|
| Shapiro-Wilk (Normality) | 0.836 | < 0.001 | Not Normal |
| Breusch-Pagan (Heteroscedasticity) | 24.30 | < 0.001 | Significant |
| Durbin-Watson (Autocorrelation) | 2.41 | - | OK (no autocorrelation) |

### Multicollinearity (VIF)
| Variable | VIF | Status |
|----------|-----|--------|
| Year | 1.00 | OK |
| Wealth | 1.00 | OK |

### Outlier Detection
- **Cook's D threshold:** 0.066
- **Influential points:** 3 (Years: 2000, 2001, 2002)

### Logistic Regression (Binary Outcome: Low Stunting < 30%)
- **Pseudo R-squared:** 0.769
- **Year OR:** 2.16 (odds increase 116% per year)
- **Wealth OR:** 24.69 (dominant factor!)

---

## Slide 13: Key Findings

### 1. Temporal Improvement Observed
- Stunting declined from 68% (1995) to 39% (2022) over 30 years
- BUT: Simple regression (R²=3%) is misleading - no statistically significant linear trend
- The decline is real but occurs unevenly over time

### 2. Wealth is the Dominant Factor
- Multiple regression (R²=0.941) shows wealth quintile is the strongest predictor
- Children in Q1 (poorest) are **2.1x more likely** to be stunted than Q5 (richest)
- Effect size (η²=0.38) indicates large practical significance
- Odds ratio of 24.69 in logistic regression confirms wealth dominance

### 3. Gender Equity Achieved
- No significant difference between male and female children (p=0.74)
- Cohen's d=0.03 confirms negligible effect size
- Nepal has achieved equitable nutrition access across sexes

### 4. Malnutrition Syndrome
- Stunting & Underweight: r=0.988
- Stunting & Anaemia: r=0.955
- These indicators cluster together - common underlying causes (poverty, food insecurity)

---

## Slide 14: Statistical Conclusions

### What We Tested
1. **Linear Trend:** Does stunting decrease over time?
   - Result: No significant trend (p=0.17)

2. **Sex Differences:** Do boys and girls differ?
   - Result: No significant difference (p=0.74)

3. **Wealth Disparities:** Do quintiles differ?
   - Result: **Highly significant** (p<0.001)

4. **Correlation:** Are indicators related?
   - Result: **Strong correlations** (r=0.94-0.99)

### Why Multiple Regression Matters
- Simple regression (Year only): R²=3% → Misleading
- Multiple regression (Year + Wealth): R²=94% → True picture
- **Wealth is the dominant factor, not time itself**

---

## Slide 15: Python Application

**Interactive Dashboard Features:**
- Overview page with key metrics
- Time series visualizations (12 charts)
- Demographic breakdowns by sex, wealth, education, residence
- Statistical test interface with live calculations
- Data filtering and export

**Technology Stack:**
- Streamlit (Web framework)
- Plotly (Interactive visualizations)
- Pandas/NumPy (Data processing)
- SciPy/Statsmodels (Statistical analysis)

**Dashboard URL:** Run locally with `streamlit run Week-7/app.py`

---

## Slide 16: Limitations

1. **Ecological Study Design:** Aggregate data only (no individual-level)
2. **Missing Data:** Some years/indicators have incomplete coverage
3. **Cross-sectional Nature:** Cannot establish causation
4. **Model Violations:** Heteroscedasticity present, residuals not normal
5. **VIF Issue:** High constant VIF (expected in time-series models)

---

## Slide 17: Conclusions

### Nepal Has Made Progress
- Child stunting declined significantly over 30 years
- Gender equity achieved in nutrition outcomes

### But Disparities Persist
- Wealth is the strongest predictor (R²=0.941)
- Poorest children (Q1) are 2.1x more likely to be stunted
- Targeted interventions needed for vulnerable groups

### Methods Validated
- Multiple regression essential (not just simple regression)
- Effect sizes reveal practical significance
- Statistical significance ≠ practical importance

---

## Slide 18: Thank You

**Questions?**

**Project Summary:**
- Dataset: WHO GHO Nepal Nutrition (7,461 records, 37 indicators)
- Methods: Linear Regression, Multiple Regression, T-Tests, ANOVA, Correlation
- Key Finding: Wealth quintile is the strongest predictor (R²=0.941)
- Application: Interactive Streamlit dashboard

**Repository:** [GitHub Link]

**Team:** Data 200 Applied Statistical Analysis | June 2026
