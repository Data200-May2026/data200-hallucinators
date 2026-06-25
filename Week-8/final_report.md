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

### Key EDA Findings:

1. **Temporal Trends:**
   - Stunting has declined from ~61% (1998)
   - Wasting fluctuates between 6-14%

2. **Demographic Disparities:**
   - Higher stunting rates in poorer wealth quintiles
   - Minimal sex-based differences

3. **Data Quality:**
   - Clean dataset suitable for analysis
   - Confidence intervals available for most records

### Visualizations Generated (12 total):
- Year distribution chart
- Indicator counts bar chart
- Stunting/wasting/underweight trend lines
- Box plots by dimension
- Heatmaps
- Correlation matrix
- Histograms
- Confidence interval plots

---

## 4. Statistical Analysis

### Hypotheses Tested:

| Hypothesis | Test | Statistic | P-value | Result |
|------------|------|-----------|---------|--------|
| Stunting trend over time | Linear Regression | F=-15.11 | 0.172 | NOT Significant |
| Sex differences | T-Test | t=0.34 | 0.736 | NOT Significant |
| Wealth disparities | ANOVA | F=5.62 | 0.0004 | SIGNIFICANT |

### Key Statistics:

**Linear Regression (Stunting ~ Year):**
- Slope: -15.11 per year
- R-squared: 0.0314
- P-value: 0.172

**T-Test (Male vs Female Stunting):**
- Male Mean: 106.55
- Female Mean: 100.63
- P-value: 0.736

**ANOVA (Wealth Quintile):**
- F-statistic: 5.62
- P-value: 0.0004 (HIGHLY SIGNIFICANT)

---

## 5. Regression Modeling

### Simple Linear Regression:
- DV: Stunting Prevalence
- IV: Year
- R-squared = 0.0314

### Multiple Linear Regression:
- DV: Stunting Prevalence
- IVs: Year, Wealth Quintile
- Controls for socioeconomic factors

### Model Diagnostics Performed:
- Shapiro-Wilk normality test
- Breusch-Pagan heteroscedasticity test
- Durbin-Watson autocorrelation test
- Cook's Distance outlier detection
- VIF multicollinearity check

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

1. Nepal has made some progress in reducing child stunting
2. Socioeconomic factors (wealth quintile) remain significant predictors
3. No significant sex-based disparities in nutrition outcomes
4. Statistical methods effectively reveal data patterns

### Recommendations:
- Continue nutrition interventions focusing on poorer populations
- Target resources toward vulnerable socioeconomic groups
- Enhance data collection for longitudinal analysis

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
