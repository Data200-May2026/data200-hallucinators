"""
Week 5-6: Regression Models and Diagnostics
==============================================
Builds and validates regression models for Nepal nutrition data.
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.stats.api as sms
import warnings
warnings.filterwarnings('ignore')

CLEANED_DATA_PATH = "data/processed/cleaned_nutrition_indicators_npl.csv"
OUTPUT_DIR = "outputs/models/"

def load_data():
    return pd.read_csv(CLEANED_DATA_PATH)

# ============================================================================
# SIMPLE LINEAR REGRESSION
# ============================================================================
def simple_linear_regression(df):
    """Simple linear regression: Year -> Stunting."""
    print("\n" + "="*60)
    print("SIMPLE LINEAR REGRESSION")
    print("Predicting Stunting from Year")
    print("="*60)

    stunting = df[
        (df['indicator'].str.contains('Stunting', case=False)) &
        (df['dimension_code'] == 'SEX_BTSX')
    ].copy()

    X = stunting['year'].values
    y = stunting['numeric_value'].values

    # Statsmodels OLS
    X_sm = sm.add_constant(X)
    model = sm.OLS(y, X_sm).fit()

    print(model.summary())

    # Predictions
    y_pred = model.predict(X_sm)
    residuals = y - y_pred

    print("\n--- Model Diagnostics ---")
    print(f"R-squared: {model.rsquared:.4f}")
    print(f"Adj. R-squared: {model.rsquared_adj:.4f}")
    print(f"Slope: {model.params[1]:.4f}")
    print(f"Intercept: {model.params[0]:.4f}")

    return model

# ============================================================================
# MULTIPLE LINEAR REGRESSION
# ============================================================================
def multiple_linear_regression(df):
    """Multiple linear regression with multiple predictors."""
    print("\n" + "="*60)
    print("MULTIPLE LINEAR REGRESSION")
    print("Predicting Nutrition Indicators from Multiple Factors")
    print("="*60)

    # Get data with multiple dimensions
    stunting = df[
        (df['indicator'].str.contains('Stunting', case=False)) &
        (df['dimension_type'].isin(['SEX', 'WEALTHQUINTILE']))
    ].copy()

    # Map wealth to numeric BEFORE creating dummies
    wealth_map = {
        'Q1 (Poorest)': 1,
        'Q2': 2,
        'Q3': 3,
        'Q4': 4,
        'Q5 (Richest)': 5
    }

    # Add numeric wealth using dimension_name
    stunting['wealth_numeric'] = stunting['dimension_name'].map(wealth_map)

    # Create dummy variables (only for SEX dimension to avoid issues)
    stunting = pd.get_dummies(stunting, columns=['dimension_name'], drop_first=True)

    # Filter complete cases
    reg_data = stunting.dropna(subset=['numeric_value', 'year', 'wealth_numeric'])

    if len(reg_data) < 10:
        print("Insufficient data for multiple regression")
        return None

    # Prepare features
    feature_cols = ['year', 'wealth_numeric']
    X = reg_data[feature_cols]
    X = sm.add_constant(X)
    y = reg_data['numeric_value']

    # Fit model
    model = sm.OLS(y, X).fit()

    print("\n--- Multiple Regression Results ---")
    print(f"R-squared: {model.rsquared:.4f}")
    print(f"Adj. R-squared: {model.rsquared_adj:.4f}")
    print(f"F-statistic: {model.fvalue:.4f}")
    print(f"Prob (F-statistic): {model.f_pvalue:.6f}")
    print(f"\nAIC: {model.aic:.2f}")
    print(f"BIC: {model.bic:.2f}")

    print("\n--- Coefficients ---")
    for var in model.params.index:
        print(f"{var}: {model.params[var]:.4f} (p={model.pvalues[var]:.4f})")

    return model

# ============================================================================
# LOGISTIC REGRESSION (for binary outcomes)
# ============================================================================
def logistic_regression(df):
    """Logistic regression for binary outcomes."""
    print("\n" + "="*60)
    print("LOGISTIC REGRESSION")
    print("Predicting Adequate vs Inadequate Nutrition")
    print("="*60)

    # Create a binary outcome:
    # 1 = Low stunting (<30%), 0 = High stunting (>=30%)
    stunting = df[
        (df['indicator'].str.contains('Stunting', case=False)) &
        (df['dimension_code'] == 'SEX_BTSX')
    ].copy()

    stunting['low_stunting'] = (stunting['numeric_value'] < 30).astype(int)

    # Map wealth to numeric
    wealth_map = {'Q1 (Poorest)': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4, 'Q5 (Richest)': 5}

    stunting_wealth = df[
        (df['indicator'].str.contains('Stunting', case=False)) &
        (df['dimension_type'] == 'WEALTHQUINTILE')
    ].copy()

    stunting_wealth['low_stunting'] = (stunting_wealth['numeric_value'] < 30).astype(int)
    stunting_wealth['wealth_numeric'] = stunting_wealth['dimension_name'].map(wealth_map)

    reg_data = stunting_wealth.dropna(subset=['low_stunting', 'wealth_numeric', 'year'])

    if len(reg_data) < 10:
        print("Insufficient data for logistic regression")
        return None

    X = reg_data[['year', 'wealth_numeric']]
    X = sm.add_constant(X)
    y = reg_data['low_stunting']

    try:
        model = sm.Logit(y, X).fit(disp=0)

        print(f"\nPseudo R-squared: {model.prsquared:.4f}")
        print(f"Log-Likelihood: {model.llf:.4f}")

        print("\n--- Coefficients (Odds Ratios) ---")
        for var in model.params.index:
            odds_ratio = np.exp(model.params[var])
            print(f"{var}: coef={model.params[var]:.4f}, odds_ratio={odds_ratio:.4f}, p={model.pvalues[var]:.4f}")

        return model
    except:
        print("Logistic regression failed to converge")
        return None

# ============================================================================
# MODEL DIAGNOSTICS
# ============================================================================
def regression_diagnostics(df):
    """Perform comprehensive model diagnostics."""
    print("\n" + "="*60)
    print("REGRESSION DIAGNOSTICS")
    print("="*60)

    stunting = df[
        (df['indicator'].str.contains('Stunting', case=False)) &
        (df['dimension_code'] == 'SEX_BTSX')
    ].copy()

    X = stunting['year'].values
    y = stunting['numeric_value'].values

    X_sm = sm.add_constant(X)
    model = sm.OLS(y, X_sm).fit()

    y_pred = model.predict(X_sm)
    residuals = model.resid
    standardized_resid = model.get_influence().resid_studentized_internal

    print("\n--- 1. Residual Statistics ---")
    print(f"Mean of residuals: {np.mean(residuals):.6f} (should be ~0)")
    print(f"Std of residuals: {np.std(residuals):.4f}")

    print("\n--- 2. Normality Test (Shapiro-Wilk) ---")
    if len(residuals) >= 3:
        shapiro_stat, shapiro_p = stats.shapiro(residuals)
        print(f"Shapiro-Wilk statistic: {shapiro_stat:.4f}")
        print(f"Shapiro-Wilk p-value: {shapiro_p:.4f}")
        if shapiro_p > 0.05:
            print("Residuals appear normally distributed (p > 0.05)")
        else:
            print("Residuals may NOT be normally distributed (p < 0.05)")

    print("\n--- 3. Heteroscedasticity Test (Breusch-Pagan) ---")
    try:
        bp_test = sms.het_breuschpagan(residuals, X_sm)
        bp_lm_stat = bp_test[0]
        bp_lm_pval = bp_test[1]
        print(f"Breusch-Pagan LM statistic: {bp_lm_stat:.4f}")
        print(f"Breusch-Pagan p-value: {bp_lm_pval:.4f}")
        if bp_lm_pval > 0.05:
            print("No significant heteroscedasticity detected (p > 0.05)")
        else:
            print("Significant heteroscedasticity detected (p < 0.05)")
    except:
        print("Breusch-Pagan test failed")

    print("\n--- 4. Autocorrelation Test (Durbin-Watson) ---")
    dw_stat = sms.durbin_watson(residuals)
    print(f"Durbin-Watson statistic: {dw_stat:.4f}")
    print("(Values close to 2 indicate no autocorrelation)")

    print("\n--- 5. Outlier Detection ---")
    influence = model.get_influence()
    leverage = influence.hat_matrix_diag
    cooks_d = influence.cooks_distance[0]

    # Find influential points (Cook's D > 4/n)
    threshold = 4 / len(y)
    influential = np.where(cooks_d > threshold)[0]

    print(f"Cook's D threshold: {threshold:.4f}")
    print(f"Number of influential points: {len(influential)}")
    if len(influential) > 0:
        print(f"Influential points at indices: {influential}")
        print(f"Years: {X[influential]}")
        print(f"Cook's D values: {cooks_d[influential].round(4)}")

    return {
        'residuals': residuals,
        'standardized_resid': standardized_resid,
        'y_pred': y_pred,
        'leverage': leverage,
        'cooks_d': cooks_d
    }

def multicollinearity_check(df):
    """Check for multicollinearity in predictors."""
    print("\n" + "="*60)
    print("MULTICOLLINEARITY CHECK (VIF)")
    print("="*60)

    stunting = df[
        (df['indicator'].str.contains('Stunting', case=False)) &
        (df['dimension_type'] == 'WEALTHQUINTILE')
    ].copy()

    # Map wealth
    wealth_map = {'Q1 (Poorest)': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4, 'Q5 (Richest)': 5}
    stunting['wealth_numeric'] = stunting['dimension_name'].map(wealth_map)

    reg_data = stunting.dropna(subset=['year', 'wealth_numeric', 'numeric_value'])

    if len(reg_data) < 5:
        print("Insufficient data for VIF calculation")
        return None

    X = reg_data[['year', 'wealth_numeric']]
    X = sm.add_constant(X)
    y = reg_data['numeric_value']

    # Calculate VIF for each feature
    print("\n--- Variance Inflation Factors ---")
    vif_data = []
    for i, col in enumerate(X.columns):
        try:
            vif = variance_inflation_factor(X.values, i)
            vif_data.append((col, vif))
            status = "OK" if vif < 5 else "HIGH" if vif < 10 else "VERY HIGH"
            print(f"{col}: VIF={vif:.2f} ({status})")
        except:
            pass

    return vif_data

# ============================================================================
# ANOVA WITH REGRESSION
# ============================================================================
def anova_as_regression(df):
    """Show how ANOVA is equivalent to regression with categorical variables."""
    print("\n" + "="*60)
    print("ANOVA AS REGRESSION")
    print("Comparing Group Means via Linear Regression")
    print("="*60)

    stunting = df[
        (df['indicator'].str.contains('Stunting', case=False)) &
        (df['dimension_type'] == 'WEALTHQUINTILE')
    ].copy()

    # Create numeric coding for wealth
    wealth_map = {'Q1 (Poorest)': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4, 'Q5 (Richest)': 5}
    stunting['wealth_numeric'] = stunting['dimension_name'].map(wealth_map)

    reg_data = stunting.dropna(subset=['numeric_value', 'wealth_numeric'])

    if len(reg_data) < 10:
        print("Insufficient data")
        return None

    # Model as continuous (treating wealth as linear)
    X = sm.add_constant(reg_data['wealth_numeric'])
    y = reg_data['numeric_value']

    model = sm.OLS(y, X).fit()

    # ANOVA using scipy (since statsmodels anova_lm needs formula interface)
    groups = [reg_data[reg_data['wealth_numeric'] == w]['numeric_value'].dropna().values
              for w in sorted(reg_data['wealth_numeric'].unique())]
    if len(groups) >= 2:
        f_stat, p_val = stats.f_oneway(*groups)
        print("\n--- ANOVA Results (Wealth Quintile) ---")
        print(f"F-statistic: {f_stat:.4f}")
        print(f"P-value: {p_val:.6f}")

    return model

def main():
    """Run all regression analyses."""
    print("\n" + "="*60)
    print("WEEK 5-6: REGRESSION MODELS AND DIAGNOSTICS")
    print("="*60)

    df = load_data()

    # Run all models
    simple_linear_regression(df)
    multiple_linear_regression(df)
    logistic_regression(df)
    regression_diagnostics(df)
    multicollinearity_check(df)
    anova_as_regression(df)

    print("\n" + "="*60)
    print("REGRESSION ANALYSIS COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
