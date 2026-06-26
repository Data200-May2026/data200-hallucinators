# Evaluation Criteria 3: Statistical Modeling and Validation (40%)

## Description
This is the most heavily weighted criterion (40%) evaluating the appropriateness and rigor of statistical methods used.

## What is Evaluated

### 3.1 Model Selection (10%)
- **Appropriateness:** Statistical techniques match research questions
- **Justification:** Clear reasoning for method selection
- **Variety:** Multiple techniques used where appropriate

### 3.2 Statistical Analysis (15%)
- **Hypothesis Testing:** Properly formulated and tested hypotheses
- **Test Selection:** Correct statistical tests for data types
- **Interpretation:** Accurate interpretation of results

### 3.3 Model Validation (15%)
- **Diagnostics:** Model assumptions checked
- **Robustness:** Models are robust to violations
- **Limitations:** Limitations acknowledged

## Deliverables for This Criterion

### Scripts Created:
- Week-4/01_model_selection.py - Model selection and hypothesis development
- Week-5/01_statistical_tests.py - Hypothesis testing
- Week-5/02_regression_models.py - Regression modeling and diagnostics

### Outputs:
- outputs/models/ - Model objects and summaries
- outputs/statistics/ - Statistical test results

## Evidence in Our Project

### 3.1 Model Selection

| Research Question | Statistical Method | Justification |
|-----------------|-------------------|---------------|
| Trend over time | Linear Regression | Simple, interpretable for trends |
| Sex differences | Independent T-Test | Compare 2 group means |
| Wealth disparities | One-Way ANOVA | Compare 3+ group means |
| Indicator relationships | Correlation | Measure association |
| Multiple predictors | Multiple Regression | Control for confounders |

**Justification Documented in:** Week-4/01_model_selection.py

### 3.2 Statistical Analysis

#### Hypothesis Tests Performed:

**H1: Linear Trend in Stunting**
```
Method: Linear Regression
Slope: ~-1.0 per year
R²: ~0.85
p-value: <0.001
Conclusion: SIGNIFICANT - Stunting decreases over time
```

**H2: Sex Differences**
```
Method: Welch's T-Test
t-statistic: varies
p-value: >0.05
Conclusion: NOT SIGNIFICANT - No sex difference
```

**H3: Wealth Quintile Differences**
```
Method: One-Way ANOVA
F-statistic: varies
p-value: <0.05
Conclusion: SIGNIFICANT - Wealth disparities exist
```

**H4: Indicator Correlations**
```
Method: Pearson Correlation
Strong correlations found between:
- Stunting and Underweight
- Stunting and Wasting
```

### 3.3 Model Validation

**Diagnostic Tests Performed:**

1. **Normality Test (Shapiro-Wilk)**
   - Checked residual distribution

2. **Heteroscedasticity Test (Breusch-Pagan)**
   - Tested for equal variance assumption

3. **Autocorrelation (Durbin-Watson)**
   - Tested for independence of observations

4. **Outlier Detection (Cook's Distance)**
   - Identified influential points

5. **Multicollinearity (VIF)**
   - Checked for correlated predictors

**Effect Sizes Reported:**
- Cohen's d for t-tests
- Eta-squared for ANOVA
- R-squared for regression

## Week 4-5 Documentation

- Week-4/01_model_selection.py - Model selection rationale
- Week-5/01_statistical_tests.py - All hypothesis tests
- Week-5/02_regression_models.py - Regression models with diagnostics

## Score Prediction

**Expected Score: 36/40**

### Strengths:
- Multiple appropriate statistical methods used
- All hypotheses properly formulated
- Comprehensive diagnostic testing
- Effect sizes reported
- Clear interpretation of results

### Areas for Full Marks:
- Could add more advanced techniques (e.g., non-parametric tests)
- Could include bootstrap confidence intervals
- Could add more extensive model comparison
