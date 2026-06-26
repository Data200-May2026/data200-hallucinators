"""
Week 5: Statistical Analysis and Validation
============================================
Conducts descriptive and inferential statistical tests.
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import warnings
warnings.filterwarnings('ignore')

CLEANED_DATA_PATH = "data/processed/cleaned_nutrition_indicators_npl.csv"
OUTPUT_DIR = "outputs/statistics/"

def load_data():
    return pd.read_csv(CLEANED_DATA_PATH)

# ============================================================================
# HYPOTHESIS 1: Linear Regression for Trend Analysis
# ============================================================================
def test_stunting_trend(df):
    """Test for linear trend in stunting over time."""
    print("\n" + "="*60)
    print("HYPOTHESIS 1: LINEAR REGRESSION - STUNTING TREND")
    print("="*60)
    print("H0: No significant linear trend in stunting over time")
    print("H1: Significant linear trend in stunting over time\n")

    # Get stunting data (both sexes for overall trend)
    stunting = df[
        (df['indicator'].str.contains('Stunting', case=False)) &
        (df['dimension_code'] == 'SEX_BTSX')
    ].copy()

    if len(stunting) < 3:
        print("Insufficient data for trend analysis")
        return None

    X = stunting['year'].values
    y = stunting['numeric_value'].values

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(X, y)

    print(f"--- Linear Regression Results ---")
    print(f"Slope: {slope:.4f} (change per year)")
    print(f"Intercept: {intercept:.4f}")
    print(f"R-squared: {r_value**2:.4f}")
    print(f"P-value: {p_value:.6f}")
    print(f"Standard Error: {std_err:.4f}")

    # Using statsmodels for more details
    X_sm = sm.add_constant(X)
    model = sm.OLS(y, X_sm).fit()

    print(f"\n--- Full Model Summary ---")
    print(f"F-statistic: {model.fvalue:.4f}")
    print(f"Prob (F-statistic): {model.f_pvalue:.6f}")
    print(f"Adj. R-squared: {model.rsquared_adj:.4f}")

    alpha = 0.05
    if p_value < alpha:
        print(f"\n** CONCLUSION: REJECT H0 at α={alpha}")
        print(f"   There IS a statistically significant linear trend.")
        print(f"   Stunting {'decreases' if slope < 0 else 'increases'} by {abs(slope):.2f}% per year.")
    else:
        print(f"\n** CONCLUSION: FAIL TO REJECT H0 at α={alpha}")
        print(f"   No statistically significant linear trend detected.")

    return {'slope': slope, 'p_value': p_value, 'r_squared': r_value**2}

# ============================================================================
# HYPOTHESIS 2: T-Test for Sex Differences
# ============================================================================
def test_sex_differences(df):
    """Test for differences between male and female children."""
    print("\n" + "="*60)
    print("HYPOTHESIS 2: INDEPENDENT T-TEST - SEX DIFFERENCES")
    print("="*60)
    print("H0: No significant difference between male and female children")
    print("H1: Significant difference between male and female children\n")

    # Get stunting data by sex
    stunting = df[df['indicator'].str.contains('Stunting', case=False)]
    male_data = stunting[stunting['dimension_code'] == 'SEX_MLE']['numeric_value'].dropna()
    female_data = stunting[stunting['dimension_code'] == 'SEX_FMLE']['numeric_value'].dropna()

    if len(male_data) < 2 or len(female_data) < 2:
        print("Insufficient data for t-test")
        return None

    print(f"Male group: n={len(male_data)}, mean={male_data.mean():.2f}, std={male_data.std():.2f}")
    print(f"Female group: n={len(female_data)}, mean={female_data.mean():.2f}, std={female_data.std():.2f}")

    # Independent samples t-test (assuming unequal variances - Welch's t-test)
    t_stat, p_value = stats.ttest_ind(male_data, female_data, equal_var=False)

    print(f"\n--- Welch's T-Test Results ---")
    print(f"T-statistic: {t_stat:.4f}")
    print(f"P-value: {p_value:.6f}")

    # Effect size (Cohen's d)
    pooled_std = np.sqrt(((len(male_data)-1)*male_data.std()**2 +
                          (len(female_data)-1)*female_data.std()**2) /
                         (len(male_data) + len(female_data) - 2))
    cohens_d = (male_data.mean() - female_data.mean()) / pooled_std

    print(f"Cohen's d: {cohens_d:.4f}")

    # Interpret effect size
    if abs(cohens_d) < 0.2:
        effect = "negligible"
    elif abs(cohens_d) < 0.5:
        effect = "small"
    elif abs(cohens_d) < 0.8:
        effect = "medium"
    else:
        effect = "large"
    print(f"Effect size interpretation: {effect}")

    alpha = 0.05
    if p_value < alpha:
        print(f"\n** CONCLUSION: REJECT H0 at α={alpha}")
        print(f"   Significant difference between male and female children.")
    else:
        print(f"\n** CONCLUSION: FAIL TO REJECT H0 at α={alpha}")
        print(f"   No significant difference between sexes.")

    return {'t_stat': t_stat, 'p_value': p_value, 'cohens_d': cohens_d}

# ============================================================================
# HYPOTHESIS 3: ANOVA for Wealth Quintile Differences
# ============================================================================
def test_wealth_differences(df):
    """Test for differences across wealth quintiles using ANOVA."""
    print("\n" + "="*60)
    print("HYPOTHESIS 3: ONE-WAY ANOVA - WEALTH QUINTILE")
    print("="*60)
    print("H0: No significant difference across wealth quintiles")
    print("H1: Significant difference across wealth quintiles\n")

    # Get stunting data by wealth quintile
    stunting = df[
        (df['indicator'].str.contains('Stunting', case=False)) &
        (df['dimension_type'] == 'WEALTHQUINTILE')
    ]

    # Create groups for each quintile
    groups = []
    group_names = []

    for dim_name in stunting['dimension_name'].unique():
        group_data = stunting[stunting['dimension_name'] == dim_name]['numeric_value'].dropna()
        if len(group_data) > 0:
            groups.append(group_data.values)
            group_names.append(dim_name)

    if len(groups) < 2:
        print("Insufficient groups for ANOVA")
        return None

    print(f"Number of wealth groups: {len(groups)}")
    for name, group in zip(group_names, groups):
        print(f"  {name}: n={len(group)}, mean={np.mean(group):.2f}")

    # One-way ANOVA
    f_stat, p_value = stats.f_oneway(*groups)

    print(f"\n--- ANOVA Results ---")
    print(f"F-statistic: {f_stat:.4f}")
    print(f"P-value: {p_value:.6f}")

    # Calculate effect size (eta-squared)
    # SSB (between groups) / SST (total)
    all_data = np.concatenate(groups)
    grand_mean = np.mean(all_data)

    ss_between = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in groups)
    ss_total = sum((all_data - grand_mean)**2)
    eta_squared = ss_between / ss_total

    print(f"Eta-squared (η²): {eta_squared:.4f}")

    # Interpret effect size
    if eta_squared < 0.01:
        effect = "negligible"
    elif eta_squared < 0.06:
        effect = "small"
    elif eta_squared < 0.14:
        effect = "medium"
    else:
        effect = "large"
    print(f"Effect size interpretation: {effect}")

    # Tukey HSD post-hoc test
    print("\n--- Tukey HSD Post-Hoc Test ---")
    stunting_clean = stunting.dropna(subset=['numeric_value', 'dimension_name'])

    if stunting_clean['dimension_name'].nunique() >= 2:
        tukey = pairwise_tukeyhsd(
            stunting_clean['numeric_value'],
            stunting_clean['dimension_name'],
            alpha=0.05
        )
        print(tukey)

    alpha = 0.05
    if p_value < alpha:
        print(f"\n** CONCLUSION: REJECT H0 at α={alpha}")
        print(f"   Significant difference in stunting across wealth quintiles.")
    else:
        print(f"\n** CONCLUSION: FAIL TO REJECT H0 at α={alpha}")
        print(f"   No significant difference across wealth quintiles.")

    return {'f_stat': f_stat, 'p_value': p_value, 'eta_squared': eta_squared}

# ============================================================================
# HYPOTHESIS 4: Correlation Between Indicators
# ============================================================================
def test_indicator_correlations(df):
    """Test correlations between different nutrition indicators."""
    print("\n" + "="*60)
    print("HYPOTHESIS 4: CORRELATION ANALYSIS")
    print("="*60)
    print("H0: No correlation between indicators")
    print("H1: Significant correlation between indicators\n")

    # Create pivot table
    pivot_df = df.pivot_table(
        index=['year', 'dimension_name'],
        columns='indicator_code',
        values='numeric_value',
        aggfunc='mean'
    ).reset_index()

    # Select key indicators for correlation
    key_indicators = [
        'NUTRITION_ANT_HAZ_NE2',  # Stunting
        'NUTRITION_WH_2',        # Wasting
        'NUTRITION_WA_2',        # Underweight
        'NUTRITION_ANAEMIA_CHILDREN_PREV',  # Anaemia
    ]

    available_indicators = [col for col in key_indicators if col in pivot_df.columns]

    if len(available_indicators) < 2:
        print("Insufficient indicators for correlation analysis")
        return None

    print(f"Indicators available: {len(available_indicators)}")

    # Calculate correlation matrix
    corr_data = pivot_df[available_indicators].dropna()

    if len(corr_data) < 3:
        print("Insufficient data points for correlation")
        return None

    corr_matrix = corr_data.corr()

    print("\n--- Correlation Matrix ---")
    print(corr_matrix.round(3))

    # Test significance of each correlation
    print("\n--- Significant Correlations (p < 0.05) ---")
    n = len(corr_data)

    for i, ind1 in enumerate(available_indicators):
        for j, ind2 in enumerate(available_indicators):
            if i < j:  # Upper triangle only
                r = corr_matrix.loc[ind1, ind2]
                # T-test for correlation
                t_stat = r * np.sqrt((n - 2) / (1 - r**2))
                p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 2))

                if p_value < 0.05:
                    print(f"  {ind1[:20]} <-> {ind2[:20]}: r={r:.3f}, p={p_value:.4f}")

    return corr_matrix

# ============================================================================
# HYPOTHESIS 5: Multiple Regression
# ============================================================================
def test_multiple_regression(df):
    """Test multiple regression with year and wealth as predictors."""
    print("\n" + "="*60)
    print("HYPOTHESIS 5: MULTIPLE LINEAR REGRESSION")
    print("="*60)
    print("DV: Stunting prevalence")
    print("IVs: Year, Wealth quintile\n")

    # Get stunting data with wealth dimension
    stunting = df[
        (df['indicator'].str.contains('Stunting', case=False)) &
        (df['dimension_type'] == 'WEALTHQUINTILE')
    ].copy()

    if len(stunting) < 10:
        print("Insufficient data for regression")
        return None

    # Create dummy variables for wealth
    stunting['wealth_rank'] = stunting['dimension_name'].map({
        'Q1 (Poorest)': 1,
        'Q2': 2,
        'Q3': 3,
        'Q4': 4,
        'Q5 (Richest)': 5
    })

    # Drop missing values
    reg_data = stunting.dropna(subset=['numeric_value', 'year', 'wealth_rank'])

    if len(reg_data) < 10:
        print("Insufficient complete cases for regression")
        return None

    print(f"Data points for regression: {len(reg_data)}")

    # Fit model
    X = reg_data[['year', 'wealth_rank']]
    X = sm.add_constant(X)
    y = reg_data['numeric_value']

    model = sm.OLS(y, X).fit()

    print("\n--- Model Summary ---")
    print(f"R-squared: {model.rsquared:.4f}")
    print(f"Adj. R-squared: {model.rsquared_adj:.4f}")
    print(f"F-statistic: {model.fvalue:.4f}")
    print(f"Prob (F-statistic): {model.f_pvalue:.6f}")

    print("\n--- Coefficient Estimates ---")
    print(f"{'Variable':<15} {'Coef':>10} {'Std Err':>10} {'t-value':>10} {'P>|t|':>10}")
    print("-" * 55)

    for var in model.params.index:
        print(f"{var:<15} {model.params[var]:>10.4f} {model.bse[var]:>10.4f} "
              f"{model.tvalues[var]:>10.4f} {model.pvalues[var]:>10.4f}")

    # Check significance of each predictor
    print("\n--- Significant Predictors (p < 0.05) ---")
    for var in model.params.index:
        if model.pvalues[var] < 0.05 and var != 'const':
            direction = "increases" if model.params[var] > 0 else "decreases"
            print(f"  {var}: {direction} stunting by {abs(model.params[var]):.4f} per unit")

    return model

# ============================================================================
# SUMMARY OF ALL TESTS
# ============================================================================
def summary_of_tests(df):
    """Print summary of all hypothesis tests."""
    print("\n" + "="*60)
    print("SUMMARY OF HYPOTHESIS TESTS")
    print("="*60)

    results = []

    # Test 1: Stunting trend
    print("\n[1] Linear Trend in Stunting Over Time")
    result1 = test_stunting_trend(df)
    if result1:
        results.append(("H1: Linear Trend", result1['p_value'] < 0.05, result1['p_value']))

    # Test 2: Sex differences
    print("\n[2] Sex Differences in Stunting")
    result2 = test_sex_differences(df)
    if result2:
        results.append(("H2: Sex Differences", result2['p_value'] < 0.05, result2['p_value']))

    # Test 3: Wealth differences
    print("\n[3] Wealth Quintile Differences")
    result3 = test_wealth_differences(df)
    if result3:
        results.append(("H3: Wealth Differences", result3['p_value'] < 0.05, result3['p_value']))

    # Test 4: Correlations
    print("\n[4] Correlation Between Indicators")
    result4 = test_indicator_correlations(df)

    # Test 5: Multiple regression
    print("\n[5] Multiple Regression (Year + Wealth)")
    result5 = test_multiple_regression(df)

    print("\n" + "="*60)
    print("FINAL CONCLUSIONS")
    print("="*60)
    print("\nHypothesis Test Results:")
    print("-" * 50)
    print(f"{'Hypothesis':<40} {'Significant':<15} {'p-value':<10}")
    print("-" * 50)
    for name, sig, pval in results:
        status = "YES ***" if sig else "NO"
        print(f"{name:<40} {status:<15} {pval:.6f}")

    print("\n" + "="*60)

def main():
    """Run all statistical tests."""
    print("\n" + "="*60)
    print("WEEK 5: STATISTICAL ANALYSIS AND VALIDATION")
    print("="*60)

    df = load_data()
    summary_of_tests(df)

    print("\n" + "="*60)
    print("STATISTICAL ANALYSIS COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
