# Nepal Nutrition Indicators Analysis
## Final Project Report

**Course:** Data 200 Applied Statistical Analysis
**Date:** June 2026
**Topic:** Exploring Real-World Data through Statistical and Predictive Modeling

---

## Executive Summary

This report presents a comprehensive statistical analysis of Nepal's child nutrition indicators using WHO Global Health Observatory data. The analysis covers **7,461 records** spanning **1990 - 2022**.

### Key Findings:
- Wealth quintile is a significant predictor of child nutrition outcomes (p < 0.001)
- No significant sex-based differences in nutrition indicators (p = 0.74)
- Stunting shows some decline over time but not statistically significant (p = 0.17)
- Strong correlations exist between stunting, wasting, and underweight

---

## 1. Introduction and Problem Statement

### Research Questions:
1. What are the temporal trends in child nutrition indicators?
2. Do nutrition outcomes differ by demographic factors?
3. What predictors most strongly influence child nutrition status?

### Objectives:
- Analyze trends in key nutrition indicators over time
- Identify demographic disparities in nutrition outcomes
- Apply appropriate statistical techniques
- Develop an interactive Python application

---

## 2. Dataset Description

| Attribute | Value |
|-----------|-------|
| Source | WHO Global Health Observatory |
| Country | Nepal (NPL) |
| Region | South-East Asia (SEAR) |
| Total Records | 7,461 |
| Unique Indicators | 37 |
| Time Period | 1990 - 2022 |

### Key Indicators:
- Stunting (height-for-age < -2 SD)
- Wasting (weight-for-height < -2 SD)
- Underweight (weight-for-age < -2 SD)
- Anaemia prevalence
- Breastfeeding practices
- Low birth weight

---

## 3. Exploratory Data Analysis

### Data Quality Summary

| Metric | Before Cleaning | After Cleaning |
|--------|----------------|----------------|
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

### Indicator Statistics

| Indicator | Count | Mean | Year Min | Year Max |
|-----------|-------|------|----------|----------|
| Stunting prevalence (under 5) | 839 | 42.28% | 1995 | 2022 |
| Underweight prevalence (under 5) | 725 | 30.06% | 1995 | 2022 |
| Wasting prevalence (under 5) | 724 | 10.84% | 1995 | 2022 |
| Severe wasted prevalence | 709 | 2.51% | 1996 | 2022 |
| Overweight prevalence (under 5) | 663 | 1.47% | 1996 | 2022 |
| Exclusive breastfeeding (6 months) | 175 | 62.03% | 1996 | 2019 |
| Early Initiation of Breastfeeding | 163 | 40.74% | 1996 | 2019 |
| Ever breastfed | 163 | 98.35% | 1996 | 2019 |
| Zero vegetable or fruit consumption | 160 | 41.78% | 2006 | 2019 |
| Minimum dietary diversity (6-23 months) | 160 | 37.48% | 2006 | 2019 |
| Continued breastfeeding (12-23 months) | 149 | 93.64% | 1996 | 2019 |
| Introduction of solid/semi-solid foods | 143 | 74.56% | 2001 | 2019 |
| Minimum Meal Frequency | 128 | 73.78% | 2011 | 2019 |
| Minimum Acceptable Diet | 128 | 31.71% | 2011 | 2019 |
| Prevalence of anaemia (6-59 months) | 100 | 29.91% | 2000 | 2019 |
| Low birth weight prevalence | 21 | 21.19% | 2000 | 2020 |

### Time Trend Analysis

**Stunting Trend:**
- Years: 1995, 1996, 1998, 2000-2022 (sparse early years)
- Mean values: 68.2% (1995) → 38.96% (2022)
- Slope: -5.04 per year
- R-squared: 0.037
- **P-value: 0.329 (NOT significant)**

**Wasting Trend:**
- Years: 1995, 1996, 1998, 2001, 2006, 2010, 2011, 2014, 2016, 2019, 2022
- Range: 6.0% to 13.8%
- Slope: 0.02 (essentially flat)
- **P-value: 0.829 (NOT significant)**

**Underweight Trend:**
- Years: 1990-2022 (continuous data)
- Range: 36.77% (1995) to 10.32% (2021)
- Slope: -0.60 per year
- R-squared: 0.495
- **P-value: < 0.001 (SIGNIFICANT)**

### Demographic Analysis

**By Sex (SEX Dimension):**
| Sex | Mean Value | Count |
|-----|------------|-------|
| Both sexes | 104.22 | 725 |
| Female | 95.92 | 1,590 |
| Male | 29.37 | 1,445 |

**By Wealth Quintile (WEALTHQUINTILE):**
| Quintile | Mean | Count |
|----------|------|-------|
| Q1 (Poorest) | 45.42 | 91 |
| Q2 | 43.90 | 91 |
| Q3 | 42.29 | 91 |
| Q4 | 42.85 | 91 |
| Q5 (Richest) | 41.20 | 91 |

**By Residence Area (RESIDENCEAREATYPE):**
| Area | Mean | Count |
|------|------|-------|
| Rural | 44.69 | 102 |
| Urban | 42.43 | 102 |

**By Education Level (EDUCATIONLEVEL):**
| Level | Mean | Count |
|-------|------|-------|
| None and primary | 44.59 | 97 |
| Primary | 44.50 | 97 |
| Secondary education | 46.66 | 91 |
| Higher education | 43.93 | 86 |

### Correlation Analysis

**Strong Correlations (r > 0.5):**
| Variable Pair | r | Interpretation |
|-------------|-----|----------------|
| Stunting <-> Underweight | 0.988 | Very strong positive |
| Stunting <-> Anaemia | 0.955 | Very strong positive |
| Underweight <-> Anaemia | 0.943 | Very strong positive |
| year <-> LBW_PREVALENCE | -0.991 | Very strong negative |
| year <-> NCD_BMI_25A | 0.956 | Strong positive |
| year <-> NCD_BMI_30A | 0.904 | Strong positive |

### Visualizations Generated (12 total):
1. Year distribution chart
2. Indicator counts bar chart
3. Stunting trend line
4. Wasting trend line
5. Underweight trend line
6. Box plots by dimension (sex, wealth, residence, education)
7. Heatmaps (sex and wealth over time)
8. Histograms of indicators
9. Correlation matrix
10. Scatter plots (sex vs wealth)
11. Confidence interval plots
12. Combined trends chart

---

## 4. Statistical Analysis

### Hypotheses Tested:

| Hypothesis | Test | Statistic | P-value | Effect Size | Result |
|------------|------|-----------|---------|--------------|--------|
| H1: Stunting trend over time | Linear Regression | F=-15.11, R²=0.031 | 0.172 | - | NOT Significant |
| H2: Sex differences | T-Test | t=0.34 | 0.736 | Cohen's d=0.03 (negligible) | NOT Significant |
| H3: Wealth disparities | ANOVA | F=5.62 | 0.0004 | η²=0.38 (large) | **SIGNIFICANT** |
| H4: Indicator correlations | Pearson | r=0.94-0.99 | <0.001 | - | **SIGNIFICANT** |

### Detailed Hypothesis Results:

**H1: Linear Trend in Stunting Over Time**
- Test: Simple Linear Regression
- Slope: -15.11 per year
- R-squared: 0.0314 (only 3.1% variance explained)
- F-statistic: 1.91, P-value: 0.172
- Conclusion: FAIL TO REJECT H0 - No statistically significant linear trend

**H2: Sex Differences in Stunting**
- Test: Welch's T-Test (unequal variances)
- Male Mean: 106.55 (n=242), std=200.38
- Female Mean: 100.63 (n=242), std=185.57
- T-statistic: 0.34, P-value: 0.736
- Cohen's d: 0.03 (negligible effect)
- Conclusion: FAIL TO REJECT H0 - No significant sex difference

**H3: Wealth Quintile Differences**
- Test: One-Way ANOVA with Tukey HSD post-hoc
- F-statistic: 5.62, P-value: 0.000419
- Eta-squared (η²): 0.3842 (large effect size)
- Group Means: Q1=53.85%, Q2=44.91%, Q3=40.48%, Q4=34.94%, Q5=25.05%
- Tukey HSD significant pairs: Q1-Q4, Q1-Q5, Q2-Q5, Q5-Total
- Conclusion: REJECT H0 - Highly significant wealth disparities

---

## 5. Regression Modeling

### Simple Linear Regression: Year → Stunting
| Metric | Value |
|--------|-------|
| R-squared | 0.031 |
| Adj. R-squared | 0.015 |
| Slope | -15.11 |
| Intercept | 30,938 |
| F-statistic | 1.91 |
| P-value | 0.172 |

**Problem:** Only explains 3% of variance - misleading results!

### Multiple Linear Regression: Year + Wealth → Stunting
| Metric | Value |
|--------|-------|
| R-squared | **0.941** |
| Adj. R-squared | 0.938 |
| F-statistic | 294.99 |
| P-value | < 0.001 |

**Coefficients:**
| Predictor | Coefficient | Std Error | t-value | P-value |
|-----------|-------------|-----------|---------|---------|
| Constant | 2496.78 | 137.41 | 18.17 | < 0.001 |
| Year | -1.21 | 0.07 | -17.73 | < 0.001 |
| Wealth Rank | -6.76 | 0.41 | -16.60 | < 0.001 |

**Interpretation:**
- Each year, stunting decreases by 1.21% (controlling for wealth)
- Each wealth quintile higher, stunting decreases by 6.76% (controlling for year)

### Logistic Regression (Binary: Low Stunting < 30%)
- Pseudo R-squared: 0.769
- Year coefficient: 0.771 (OR=2.16, p=0.041)
- Wealth coefficient: 3.206 (OR=24.69, p=0.029)
- **Key Insight:** Wealth has 24x greater effect than year!

### Model Diagnostics:

**1. Residual Statistics:**
- Mean of residuals: ~0 (acceptable)
- Std of residuals: 648.47

**2. Normality Test (Shapiro-Wilk):**
- Statistic: 0.836, P-value: < 0.001
- Residuals may NOT be normally distributed

**3. Heteroscedasticity Test (Breusch-Pagan):**
- LM statistic: 24.30, P-value: < 0.001
- Significant heteroscedasticity detected

**4. Autocorrelation (Durbin-Watson):**
- Statistic: 2.41 (close to 2 = no autocorrelation)

**5. Multicollinearity (VIF):**
| Variable | VIF | Status |
|----------|-----|--------|
| Year | 1.00 | OK |
| Wealth | 1.00 | OK |
| Constant | 56956 | Very High (expected in time-series) |

**6. Outlier Detection (Cook's D):**
- Threshold: 0.066
- Influential points: 3 (Years: 2000, 2001, 2002)
- Cook's D values: 0.073, 0.111, 0.090

---

## 6. Python Application

An interactive Streamlit dashboard was developed featuring:
- Dataset overview with key metrics
- Time series visualizations
- Demographic breakdowns
- Statistical testing interface
- Data filtering and export

**Run:** `streamlit run Week-7/app.py`

---

## 7. Conclusions

### Key Findings:

1. **Temporal Improvement Observed:**
   - Stunting declined from ~68% to ~39% over 30 years
   - BUT: Simple linear regression (R²=3%) misleading - no statistically significant trend (p=0.17)
   - The improvement is real but occurs unevenly over time

2. **Wealth is the Dominant Factor:**
   - Multiple regression (R²=0.941) shows wealth quintile is the strongest predictor
   - Children in Q1 (poorest) are **2.1x more likely** to be stunted than Q5 (richest)
   - Effect size (η²=0.38) indicates large practical significance
   - Odds ratio of 24.69 in logistic regression confirms wealth dominance

3. **Gender Equity Achieved:**
   - No significant difference between male and female children (p=0.74)
   - Cohen's d=0.03 confirms negligible effect size
   - Nepal has achieved equitable nutrition access across sexes

4. **Inter-Indicator Correlations:**
   - Stunting & Underweight: r=0.988
   - Stunting & Anaemia: r=0.955
   - These form a "malnutrition syndrome" with common underlying causes

### Limitations:

1. Ecological study design (aggregate data only)
2. Some heteroscedasticity and non-normality in residuals
3. Cross-sectional nature limits causal inference
4. Missing data in some years/indicator combinations

### Recommendations:

1. **Target Interventions:** Focus resources on poorest quintiles (Q1-Q2)
2. **Address Root Causes:** Poverty, food security, maternal health
3. **Monitor Wasting:** Fluctuates without clear trend - requires ongoing surveillance
4. **Continue Progress:** Maintain successful nutrition programs
5. **Collect Individual Data:** Enable more sophisticated causal analysis

### Why Multiple Regression Matters:

| Model | R² | Interpretation |
|-------|-----|---------------|
| Simple (Year only) | 0.031 | Misleading - suggests no significant trend |
| Multiple (Year + Wealth) | 0.941 | True picture - reveals wealth as key factor |

**Lesson Learned:** Always consider multiple predictors; simple models can be misleading.

---

## 8. References

1. WHO Global Health Observatory: https://www.who.int/data/gho
2. Nepal Demographic and Health Surveys
3. Python libraries: pandas, scipy, statsmodels, streamlit

---

## Project Structure

```
data200-hallucinators/
├── data/
│   ├── raw/              # Original data
│   └── processed/        # Cleaned data
├── scripts/              # Data cleaning scripts
├── Week-1/               # Topic finalization
├── Week-2/               # Literature review
├── Week-3/               # EDA scripts
├── Week-4/               # Model selection
├── Week-5/               # Statistical tests
├── Week-6/               # Model refinement
├── Week-7/               # Python application
├── Week-8/               # Final presentation
├── Evaluation/           # Criteria documentation
├── outputs/              # Generated outputs
│   └── visualizations/   # 12 visualization files
└── TeamInfo/             # Team information
```

---

*Report generated: June 2026*
