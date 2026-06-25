"""
Week 3: Exploratory Data Analysis (EDA)
======================================
Performs descriptive statistics and data exploration on cleaned Nepal nutrition data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configuration
CLEANED_DATA_PATH = "data/processed/cleaned_nutrition_indicators_npl.csv"
OUTPUT_DIR = "outputs/visualizations/"

def load_data():
    """Load the cleaned dataset."""
    df = pd.read_csv(CLEANED_DATA_PATH)
    return df

def basic_statistics(df):
    """Generate basic descriptive statistics."""
    print("\n" + "="*60)
    print("BASIC DESCRIPTIVE STATISTICS")
    print("="*60)

    print("\n--- Dataset Overview ---")
    print(f"Total Records: {len(df)}")
    print(f"Time Period: {df['year'].min()} - {df['year'].max()}")
    print(f"Number of Unique Indicators: {df['indicator'].nunique()}")
    print(f"Number of Unique Countries: {df['country'].nunique()}")

    print("\n--- Numeric Summary ---")
    numeric_cols = ['numeric_value', 'low', 'high']
    print(df[numeric_cols].describe())

    return df

def indicator_summary(df):
    """Summary by indicator type."""
    print("\n" + "="*60)
    print("INDICATOR SUMMARY")
    print("="*60)

    indicator_stats = df.groupby('indicator').agg({
        'numeric_value': ['count', 'mean', 'std', 'min', 'max'],
        'year': ['min', 'max']
    }).round(2)

    indicator_stats.columns = ['Count', 'Mean', 'Std', 'Min', 'Max', 'Year_Min', 'Year_Max']
    indicator_stats = indicator_stats.sort_values('Count', ascending=False)

    print("\n--- Indicator Statistics ---")
    print(indicator_stats)

    return indicator_stats

def time_trend_analysis(df):
    """Analyze trends over time."""
    print("\n" + "="*60)
    print("TIME TREND ANALYSIS")
    print("="*60)

    # Focus on main child nutrition indicators
    main_indicators = [
        'Stunting prevalence among children under 5 years of age',
        'Wasting prevalence among children under 5 years of age',
        'Underweight prevalence among children under 5 years of age'
    ]

    for indicator in main_indicators:
        subset = df[df['indicator'].str.contains(indicator.split()[0], case=False)]
        if len(subset) > 0:
            yearly_avg = subset.groupby('year')['numeric_value'].mean()
            print(f"\n--- {indicator[:50]}... ---")
            print(f"Years covered: {list(yearly_avg.index)}")
            print(f"Mean values: {yearly_avg.values.round(2)}")

            # Linear trend test
            if len(yearly_avg) > 1:
                slope, intercept, r_value, p_value, std_err = stats.linregress(
                    yearly_avg.index, yearly_avg.values
                )
                print(f"Trend: slope={slope:.4f}, p-value={p_value:.4f}, R²={r_value**2:.4f}")

def dimension_analysis(df):
    """Analyze by demographic dimensions."""
    print("\n" + "="*60)
    print("DIMENSION ANALYSIS (Demographic Breakdowns)")
    print("="*60)

    for dim_type in df['dimension_type'].unique():
        print(f"\n--- Dimension Type: {dim_type} ---")
        subset = df[df['dimension_type'] == dim_type]
        dim_summary = subset.groupby('dimension_name')['numeric_value'].agg(['mean', 'count']).round(2)
        dim_summary.columns = ['Mean Value', 'Count']
        print(dim_summary)

def sex_disparity_analysis(df):
    """Analyze differences between male and female children."""
    print("\n" + "="*60)
    print("SEX DISPARITY ANALYSIS")
    print("="*60)

    # Filter for indicators that have both male and female data
    male_data = df[(df['dimension_type'] == 'SEX') & (df['dimension_code'] == 'SEX_MLE')]
    female_data = df[(df['dimension_type'] == 'SEX') & (df['dimension_code'] == 'SEX_FMLE')]

    # Find common indicators
    common_indicators = set(male_data['indicator'].unique()) & set(female_data['indicator'].unique())

    print(f"\nIndicators with sex-disaggregated data: {len(common_indicators)}")

    for indicator in list(common_indicators)[:5]:  # Top 5
        m_vals = male_data[male_data['indicator'] == indicator]['numeric_value'].values
        f_vals = female_data[female_data['indicator'] == indicator]['numeric_value'].values

        if len(m_vals) > 0 and len(f_vals) > 0:
            m_mean = np.mean(m_vals)
            f_mean = np.mean(f_vals)
            diff = m_mean - f_mean

            # T-test
            if len(m_vals) > 1 and len(f_vals) > 1:
                t_stat, p_value = stats.ttest_ind(m_vals, f_vals)
                sig = "**" if p_value < 0.05 else ""
                print(f"\n{indicator[:50]}...")
                print(f"  Male mean: {m_mean:.2f}, Female mean: {f_mean:.2f}")
                print(f"  Difference: {diff:.2f}, T-test p={p_value:.4f} {sig}")

def wealth_quintile_analysis(df):
    """Analyze nutrition by wealth quintile."""
    print("\n" + "="*60)
    print("WEALTH QUINTILE ANALYSIS")
    print("="*60)

    wealth_data = df[df['dimension_type'] == 'WEALTHQUINTILE']

    if len(wealth_data) > 0:
        wealth_order = ['Q1 (Poorest)', 'Q2', 'Q3', 'Q4', 'Q5 (Richest)']

        print("\nMean numeric_value by Wealth Quintile:")
        wealth_summary = wealth_data.groupby('dimension_name')['numeric_value'].agg(['mean', 'count']).round(2)
        print(wealth_summary)

        # ANOVA test
        groups = [group['numeric_value'].values for name, group in wealth_data.groupby('dimension_name')]
        if all(len(g) > 1 for g in groups):
            f_stat, p_value = stats.f_oneway(*groups)
            print(f"\nANOVA Test: F={f_stat:.4f}, p-value={p_value:.4f}")

def correlation_analysis(df):
    """Analyze correlations between different indicators."""
    print("\n" + "="*60)
    print("CORRELATION ANALYSIS")
    print("="*60)

    # Pivot to get indicators as columns
    pivot_df = df.pivot_table(
        index=['year', 'dimension_name'],
        columns='indicator_code',
        values='numeric_value',
        aggfunc='mean'
    ).reset_index()

    # Select numeric columns for correlation
    numeric_cols = pivot_df.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) > 1:
        corr_matrix = pivot_df[numeric_cols].corr()

        # Find high correlations
        high_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > 0.5:
                    high_corr.append((
                        corr_matrix.columns[i],
                        corr_matrix.columns[j],
                        corr_matrix.iloc[i, j]
                    ))

        print(f"\nFound {len(high_corr)} indicator pairs with correlation > 0.5:")
        for code1, code2, corr in high_corr[:10]:
            print(f"  {code1[:20]} <-> {code2[:20]}: {corr:.3f}")

    return pivot_df

def missing_values_check(df):
    """Check for missing values and data quality."""
    print("\n" + "="*60)
    print("DATA QUALITY CHECK")
    print("="*60)

    print("\nMissing values per column:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({'Missing': missing, 'Percent': missing_pct})
    print(missing_df[missing_df['Missing'] > 0])

    print(f"\nTotal duplicate rows: {df.duplicated().sum()}")
    print(f"Year range: {df['year'].min()} - {df['year'].max()}")

def main():
    """Run complete EDA analysis."""
    print("\n" + "="*60)
    print("WEEK 3: EXPLORATORY DATA ANALYSIS")
    print("Nepal Nutrition Indicators Dataset")
    print("="*60)

    # Load data
    df = load_data()

    # Run all analyses
    basic_statistics(df)
    indicator_summary(df)
    time_trend_analysis(df)
    dimension_analysis(df)
    sex_disparity_analysis(df)
    wealth_quintile_analysis(df)
    correlation_analysis(df)
    missing_values_check(df)

    print("\n" + "="*60)
    print("EDA ANALYSIS COMPLETE")
    print("="*60)

    return df

if __name__ == "__main__":
    df = main()
