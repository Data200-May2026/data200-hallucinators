"""
Week 4: Statistical Model Selection and Hypothesis Development
=============================================================
Selects appropriate statistical techniques and develops hypotheses.
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

CLEANED_DATA_PATH = "data/processed/cleaned_nutrition_indicators_npl.csv"

def load_data():
    return pd.read_csv(CLEANED_DATA_PATH)

def identify_key_indicators(df):
    """Identify key indicators for modeling."""
    print("\n" + "="*60)
    print("KEY INDICATORS IDENTIFICATION")
    print("="*60)

    indicators = df.groupby('indicator').agg({
        'numeric_value': ['count', 'mean', 'std'],
        'year': ['min', 'max']
    }).round(2)
    indicators.columns = ['Count', 'Mean', 'Std', 'Year_Min', 'Year_Max']

    # Focus on indicators with sufficient data
    sufficient_data = indicators[indicators['Count'] >= 5].sort_values('Count', ascending=False)
    print("\nIndicators with sufficient data (n>=5):")
    print(sufficient_data.head(15))

    return sufficient_data

def develop_hypotheses(df):
    """Develop statistical hypotheses."""
    print("\n" + "="*60)
    print("HYPOTHESIS DEVELOPMENT")
    print("="*60)

    hypotheses = """
    ============================================================================
    RESEARCH HYPOTHESES FOR NEPAL NUTRITION ANALYSIS
    ============================================================================

    HYPOTHESIS 1: Stunting Prevalence Over Time
    --------------------------------------------
    H0: There is no significant linear trend in stunting prevalence over time
    H1: There is a significant linear trend in stunting prevalence over time

    Expected: Based on public health interventions, we expect stunting to
              DECREASE over time (negative slope)

    HYPOTHESIS 2: Sex Differences in Child Nutrition
    -------------------------------------------------
    H0: There is no significant difference in nutrition indicators between
        male and female children
    H1: There is a significant difference in nutrition indicators between
        male and female children

    Expected: May or may not find significant differences

    HYPOTHESIS 3: Wealth Quintile Disparities
    -----------------------------------------
    H0: There is no significant difference in nutrition indicators across
        wealth quintiles
    H1: There is a significant difference in nutrition indicators across
        wealth quintiles

    Expected: We expect nutrition outcomes to IMPROVE with higher wealth quintile
              (lower stunting/wasting in richer households)

    HYPOTHESIS 4: Education and Child Nutrition
    -------------------------------------------
    H0: There is no significant relationship between maternal education level
        and child nutrition indicators
    H1: There is a significant relationship between maternal education level
        and child nutrition indicators

    Expected: Higher maternal education associated with better nutrition outcomes

    HYPOTHESIS 5: Breastfeeding Practices
    -------------------------------------
    H0: Breastfeeding initiation rates have not improved significantly over time
    H1: Breastfeeding initiation rates have improved significantly over time

    Expected: With health education programs, we expect improvement over time

    ============================================================================
    """
    print(hypotheses)
    return hypotheses

def model_selection_rationale():
    """Document model selection rationale."""
    print("\n" + "="*60)
    print("MODEL SELECTION RATIONALE")
    print("="*60)

    rationale = """
    ============================================================================
    STATISTICAL MODEL SELECTION
    ============================================================================

    1. LINEAR REGRESSION
    -------------------
    Use Case: Trend analysis over time
    Variables: Year (independent) → Nutrition indicator (dependent)
    Justification:
    - Simple, interpretable
    - Identifies direction and magnitude of trends
    - Suitable for time-series data

    2. ONE-WAY ANOVA
    ----------------
    Use Case: Compare means across 3+ groups
    Variables: Group (wealth quintile, education level) → Nutrition indicator
    Justification:
    - Tests if group means differ significantly
    - Extensions: Two-way ANOVA for factorial designs

    3. INDEPENDENT T-TEST
    ---------------------
    Use Case: Compare means between 2 groups
    Variables: Group (male/female, urban/rural) → Nutrition indicator
    Justification:
    - Simple comparison of two group means
    - Reports effect size (Cohen's d)

    4. CORRELATION ANALYSIS
    -----------------------
    Use Case: Measure relationship strength between two continuous variables
    Variables: Indicator A ↔ Indicator B
    Justification:
    - Pearson correlation for linear relationships
    - Spearman for non-parametric/ordinal data

    5. MULTIPLE LINEAR REGRESSION
    -----------------------------
    Use Case: Predict nutrition outcome using multiple predictors
    Variables: Year + Wealth + Education → Nutrition indicator
    Justification:
    - Controls for confounders
    - Quantifies unique contribution of each predictor

    6. CHI-SQUARE TEST
    ------------------
    Use Case: Test association between categorical variables
    Variables: Dimension Type ↔ Indicator Category
    Justification:
    - Non-parametric test for categorical relationships

    ============================================================================
    """
    print(rationale)
    return rationale

def feature_selection(df):
    """Perform feature selection for modeling."""
    print("\n" + "="*60)
    print("FEATURE SELECTION ANALYSIS")
    print("="*60)

    # Create features for modeling
    print("\n--- Available Features ---")
    print("1. Year (continuous) - for trend analysis")
    print("2. Dimension Type (categorical) - SEX, WEALTHQUINTILE, etc.")
    print("3. Dimension Name (categorical) - specific groups within type")
    print("4. Indicator Code (categorical) - type of nutrition indicator")
    print("5. Region (categorical) - SEAR (South-East Asia)")

    # Check data availability for each dimension
    print("\n--- Data Availability by Dimension ---")
    for dim_type in df['dimension_type'].unique():
        subset = df[df['dimension_type'] == dim_type]
        print(f"  {dim_type}: {subset['dimension_name'].nunique()} unique values, {len(subset)} records")

    # Select features for regression
    print("\n--- Selected Features for Modeling ---")
    features = {
        'dependent': ['numeric_value (Nutrition Indicator Value)'],
        'independent': [
            'year (Trend analysis)',
            'dimension_name (Group comparisons)',
            'indicator_code (Indicator type)'
        ]
    }
    for category, items in features.items():
        print(f"\n{category.upper()}:")
        for item in items:
            print(f"  - {item}")

    return features

def data_preparation_for_models(df):
    """Prepare data for statistical modeling."""
    print("\n" + "="*60)
    print("DATA PREPARATION FOR MODELS")
    print("="*60)

    # Filter for specific analyses
    stunting = df[df['indicator'].str.contains('Stunting', case=False)].copy()

    print(f"\nStunting data: {len(stunting)} records")
    print(f"Year range: {stunting['year'].min()} - {stunting['year'].max()}")
    print(f"Dimensions available: {stunting['dimension_type'].unique()}")

    # Create dummy variables for categorical features
    print("\n--- Creating Dummy Variables ---")

    # Example: Sex dimension
    sex_dummies = pd.get_dummies(
        stunting[stunting['dimension_type'] == 'SEX']['dimension_name'],
        prefix='sex'
    )
    print(f"Sex dummies created: {list(sex_dummies.columns)}")

    # Example: Wealth dimension
    wealth_dummies = pd.get_dummies(
        stunting[stunting['dimension_type'] == 'WEALTHQUINTILE']['dimension_name'],
        prefix='wealth'
    )
    print(f"Wealth dummies created: {list(wealth_dummies.columns)}")

    return stunting

def main():
    """Run model selection and hypothesis development."""
    print("\n" + "="*60)
    print("WEEK 4: MODEL SELECTION & HYPOTHESIS DEVELOPMENT")
    print("="*60)

    df = load_data()

    key_indicators = identify_key_indicators(df)
    hypotheses = develop_hypotheses(df)
    rationale = model_selection_rationale()
    features = feature_selection(df)
    stunting = data_preparation_for_models(df)

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE - Ready for Week 5")
    print("="*60)

if __name__ == "__main__":
    main()
