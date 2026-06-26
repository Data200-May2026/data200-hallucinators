"""
Week 3: Data Visualizations
============================
Generates comprehensive visualizations for EDA.
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

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def load_data():
    """Load the cleaned dataset."""
    return pd.read_csv(CLEANED_DATA_PATH)

def plot_year_range_distribution(df):
    """Plot distribution of records by year."""
    fig, ax = plt.subplots(figsize=(12, 5))

    year_counts = df.groupby('year').size()
    year_counts.plot(kind='bar', ax=ax, color='steelblue', alpha=0.8)

    ax.set_title('Distribution of Records by Year', fontsize=14, fontweight='bold')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Number of Records', fontsize=12)
    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}01_year_distribution.png', dpi=150)
    plt.close()
    print("Saved: 01_year_distribution.png")

def plot_indicator_counts(df):
    """Plot count of records per indicator."""
    fig, ax = plt.subplots(figsize=(12, 8))

    indicator_counts = df.groupby('indicator').size().sort_values(ascending=True)

    # Shorten indicator names for display
    short_names = [name[:60] + '...' if len(name) > 60 else name
                   for name in indicator_counts.index]

    indicator_counts.plot(kind='barh', ax=ax, color='coral', alpha=0.8)
    ax.set_title('Number of Records per Nutrition Indicator', fontsize=14, fontweight='bold')
    ax.set_xlabel('Count', fontsize=12)
    ax.set_ylabel('Indicator', fontsize=12)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}02_indicator_counts.png', dpi=150)
    plt.close()
    print("Saved: 02_indicator_counts.png")

def plot_stunting_trend(df):
    """Plot stunting prevalence trend over time."""
    fig, ax = plt.subplots(figsize=(12, 6))

    # Filter stunting data
    stunting = df[df['indicator'].str.contains('Stunting', case=False)]
    stunting_avg = stunting.groupby('year')['numeric_value'].mean()

    # Also get by sex if available
    stunting_male = stunting[stunting['dimension_code'] == 'SEX_MLE'].groupby('year')['numeric_value'].mean()
    stunting_female = stunting[stunting['dimension_code'] == 'SEX_FMLE'].groupby('year')['numeric_value'].mean()

    ax.plot(stunting_avg.index, stunting_avg.values, 'o-', label='Both Sexes',
            linewidth=2, markersize=8, color='darkblue')

    if len(stunting_male) > 0:
        ax.plot(stunting_male.index, stunting_male.values, 's--', label='Male',
                linewidth=2, markersize=6, color='steelblue', alpha=0.7)
    if len(stunting_female) > 0:
        ax.plot(stunting_female.index, stunting_female.values, '^--', label='Female',
                linewidth=2, markersize=6, color='coral', alpha=0.7)

    # Add trend line
    if len(stunting_avg) > 1:
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            stunting_avg.index, stunting_avg.values
        )
        trend_line = slope * stunting_avg.index + intercept
        ax.plot(stunting_avg.index, trend_line, ':', color='gray',
                linewidth=2, label=f'Trend (p={p_value:.3f})')

    ax.set_title('Stunting Prevalence Trend (1998-2022)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Prevalence (%)', fontsize=12)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}03_stunting_trend.png', dpi=150)
    plt.close()
    print("Saved: 03_stunting_trend.png")

def plot_wasting_trend(df):
    """Plot wasting prevalence trend over time."""
    fig, ax = plt.subplots(figsize=(12, 6))

    wasting = df[df['indicator'].str.contains('Wasting', case=False)]
    wasting_avg = wasting.groupby('year')['numeric_value'].mean()

    # By sex
    wasting_male = wasting[wasting['dimension_code'] == 'SEX_MLE'].groupby('year')['numeric_value'].mean()
    wasting_female = wasting[wasting['dimension_code'] == 'SEX_FMLE'].groupby('year')['numeric_value'].mean()

    ax.plot(wasting_avg.index, wasting_avg.values, 'o-', label='Both Sexes',
            linewidth=2, markersize=8, color='darkgreen')

    if len(wasting_male) > 0:
        ax.plot(wasting_male.index, wasting_male.values, 's--', label='Male',
                linewidth=2, markersize=6, color='steelblue', alpha=0.7)
    if len(wasting_female) > 0:
        ax.plot(wasting_female.index, wasting_female.values, '^--', label='Female',
                linewidth=2, markersize=6, color='coral', alpha=0.7)

    ax.set_title('Wasting Prevalence Trend (1995-2022)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Prevalence (%)', fontsize=12)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}04_wasting_trend.png', dpi=150)
    plt.close()
    print("Saved: 04_wasting_trend.png")

def plot_underweight_trend(df):
    """Plot underweight prevalence trend over time."""
    fig, ax = plt.subplots(figsize=(12, 6))

    underweight = df[df['indicator'].str.contains('Underweight', case=False)]
    underweight_avg = underweight.groupby('year')['numeric_value'].mean()

    ax.plot(underweight_avg.index, underweight_avg.values, 'o-',
            linewidth=2, markersize=8, color='darkorange')

    # Add trend line
    if len(underweight_avg) > 1:
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            underweight_avg.index, underweight_avg.values
        )
        trend_line = slope * underweight_avg.index + intercept
        ax.plot(underweight_avg.index, trend_line, ':', color='gray', linewidth=2)
        ax.text(0.05, 0.95, f'Trend: slope={slope:.2f}/year, p={p_value:.3f}',
                transform=ax.transAxes, fontsize=10, verticalalignment='top')

    ax.set_title('Underweight Prevalence Trend', fontsize=14, fontweight='bold')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Prevalence (%)', fontsize=12)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}05_underweight_trend.png', dpi=150)
    plt.close()
    print("Saved: 05_underweight_trend.png")

def plot_dimension_boxplot(df):
    """Plot boxplots by demographic dimensions."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # By Sex
    sex_data = df[df['dimension_type'] == 'SEX']
    if len(sex_data) > 0:
        ax1 = axes[0, 0]
        sex_order = ['Both sexes', 'Male', 'Female']
        sns.boxplot(data=sex_data, x='dimension_name', y='numeric_value', ax=ax1)
        ax1.set_title('Nutrition Indicators by Sex', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Sex', fontsize=10)
        ax1.set_ylabel('Value (%)', fontsize=10)
        ax1.tick_params(axis='x', rotation=15)

    # By Wealth Quintile
    wealth_data = df[df['dimension_type'] == 'WEALTHQUINTILE']
    if len(wealth_data) > 0:
        ax2 = axes[0, 1]
        sns.boxplot(data=wealth_data, x='dimension_name', y='numeric_value', ax=ax2)
        ax2.set_title('Nutrition Indicators by Wealth Quintile', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Wealth Quintile', fontsize=10)
        ax2.set_ylabel('Value (%)', fontsize=10)
        ax2.tick_params(axis='x', rotation=30)

    # By Residence Area
    residence_data = df[df['dimension_type'] == 'RESIDENCEAREATYPE']
    if len(residence_data) > 0:
        ax3 = axes[1, 0]
        sns.boxplot(data=residence_data, x='dimension_name', y='numeric_value', ax=ax3)
        ax3.set_title('Nutrition Indicators by Residence Area', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Area Type', fontsize=10)
        ax3.set_ylabel('Value (%)', fontsize=10)
        ax3.tick_params(axis='x', rotation=15)

    # By Education Level
    education_data = df[df['dimension_type'] == 'EDUCATIONLEVEL']
    if len(education_data) > 0:
        ax4 = axes[1, 1]
        sns.boxplot(data=education_data, x='dimension_name', y='numeric_value', ax=ax4)
        ax4.set_title('Nutrition Indicators by Education Level', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Education Level', fontsize=10)
        ax4.set_ylabel('Value (%)', fontsize=10)
        ax4.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}06_dimension_boxplots.png', dpi=150)
    plt.close()
    print("Saved: 06_dimension_boxplots.png")

def plot_heatmaps(df):
    """Plot heatmaps of nutrition indicators over time by dimension."""
    # Create pivot table for heatmap
    stunting = df[df['indicator'].str.contains('Stunting', case=False)]

    if len(stunting) > 0:
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        # By Sex over time
        stunting_sex = stunting[stunting['dimension_type'] == 'SEX']
        if len(stunting_sex) > 0:
            pivot_sex = stunting_sex.pivot_table(
                index='dimension_name',
                columns='year',
                values='numeric_value',
                aggfunc='mean'
            )
            ax1 = axes[0]
            sns.heatmap(pivot_sex, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax1)
            ax1.set_title('Stunting Prevalence by Sex Over Time', fontsize=12, fontweight='bold')

        # By Wealth Quintile over time
        stunting_wealth = stunting[stunting['dimension_type'] == 'WEALTHQUINTILE']
        if len(stunting_wealth) > 0:
            pivot_wealth = stunting_wealth.pivot_table(
                index='dimension_name',
                columns='year',
                values='numeric_value',
                aggfunc='mean'
            )
            ax2 = axes[1]
            sns.heatmap(pivot_wealth, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax2)
            ax2.set_title('Stunting Prevalence by Wealth Quintile Over Time', fontsize=12, fontweight='bold')

        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}07_stunting_heatmaps.png', dpi=150)
        plt.close()
        print("Saved: 07_stunting_heatmaps.png")

def plot_histograms(df):
    """Plot distribution histograms of numeric values."""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    main_indicators = [
        ('Stunting', 'Stunting'),
        ('Wasting', 'Wasting'),
        ('Underweight', 'Underweight'),
        ('Anaemia', 'Anaemia'),
        ('Overweight', 'Overweight'),
        ('Low birth weight', 'Low Birth Weight')
    ]

    for idx, (keyword, title) in enumerate(main_indicators):
        ax = axes[idx // 3, idx % 3]
        subset = df[df['indicator'].str.contains(keyword, case=False)]

        if len(subset) > 0:
            ax.hist(subset['numeric_value'].dropna(), bins=15,
                    edgecolor='black', alpha=0.7, color='steelblue')
            ax.axvline(subset['numeric_value'].mean(), color='red',
                      linestyle='--', label=f'Mean: {subset["numeric_value"].mean():.1f}')
            ax.set_title(f'{title} Distribution', fontsize=11, fontweight='bold')
            ax.set_xlabel('Value (%)', fontsize=9)
            ax.set_ylabel('Frequency', fontsize=9)
            ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}08_indicator_histograms.png', dpi=150)
    plt.close()
    print("Saved: 08_indicator_histograms.png")

def plot_correlation_matrix(df):
    """Plot correlation matrix of indicators."""
    # Pivot to get indicators as columns
    pivot_df = df.pivot_table(
        index=['year', 'dimension_name'],
        columns='indicator_code',
        values='numeric_value',
        aggfunc='mean'
    ).reset_index()

    numeric_cols = pivot_df.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) > 2:
        corr_matrix = pivot_df[numeric_cols].corr()

        # Shorten column names for display
        short_names = {col: col[:15] for col in corr_matrix.columns}
        corr_matrix_display = corr_matrix.rename(columns=short_names, index=short_names)

        fig, ax = plt.subplots(figsize=(14, 10))
        mask = np.triu(np.ones_like(corr_matrix_display, dtype=bool))
        sns.heatmap(corr_matrix_display, mask=mask, annot=True, fmt='.2f',
                    cmap='coolwarm', center=0, ax=ax, annot_kws={'fontsize': 7})
        ax.set_title('Correlation Matrix of Nutrition Indicators', fontsize=14, fontweight='bold')

        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}09_correlation_matrix.png', dpi=150)
        plt.close()
        print("Saved: 09_correlation_matrix.png")

def plot_scatter_sex_vs_wealth(df):
    """Plot scatter of indicators by sex and wealth."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Stunting by Sex
    stunting = df[df['indicator'].str.contains('Stunting', case=False)]
    stunting_both = stunting[stunting['dimension_code'] == 'SEX_BTSX']

    if len(stunting_both) > 0:
        ax1 = axes[0]
        ax1.scatter(stunting_both['year'], stunting_both['numeric_value'],
                   s=100, alpha=0.7, c='steelblue', edgecolors='black')
        ax1.set_title('Stunting Prevalence Over Time (Both Sexes)', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Year', fontsize=11)
        ax1.set_ylabel('Prevalence (%)', fontsize=11)
        ax1.grid(True, alpha=0.3)

        # Add regression line
        if len(stunting_both) > 1:
            z = np.polyfit(stunting_both['year'], stunting_both['numeric_value'], 1)
            p = np.poly1d(z)
            ax1.plot(stunting_both['year'], p(stunting_both['year']),
                    '--', color='red', linewidth=2, label=f'Trend')
            ax1.legend()

    # Wasting by Sex
    wasting = df[df['indicator'].str.contains('Wasting', case=False)]
    wasting_both = wasting[wasting['dimension_code'] == 'SEX_BTSX']

    if len(wasting_both) > 0:
        ax2 = axes[1]
        ax2.scatter(wasting_both['year'], wasting_both['numeric_value'],
                   s=100, alpha=0.7, c='coral', edgecolors='black')
        ax2.set_title('Wasting Prevalence Over Time (Both Sexes)', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Year', fontsize=11)
        ax2.set_ylabel('Prevalence (%)', fontsize=11)
        ax2.grid(True, alpha=0.3)

        if len(wasting_both) > 1:
            z = np.polyfit(wasting_both['year'], wasting_both['numeric_value'], 1)
            p = np.poly1d(z)
            ax2.plot(wasting_both['year'], p(wasting_both['year']),
                    '--', color='red', linewidth=2, label=f'Trend')
            ax2.legend()

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}10_scatter_trends.png', dpi=150)
    plt.close()
    print("Saved: 10_scatter_trends.png")

def plot_confidence_intervals(df):
    """Plot indicators with confidence intervals."""
    fig, ax = plt.subplots(figsize=(14, 6))

    # Select key indicators with CI data
    key_indicators = df[df['indicator'].str.contains('Stunting|Wasting|Anaemia', case=False)]
    key_indicators = key_indicators.dropna(subset=['low', 'high'])

    if len(key_indicators) > 0:
        # Group by indicator and year
        summary = key_indicators.groupby(['indicator', 'year']).agg({
            'numeric_value': 'mean',
            'low': 'mean',
            'high': 'mean'
        }).reset_index()

        for indicator in summary['indicator'].unique()[:3]:
            ind_data = summary[summary['indicator'] == indicator].sort_values('year')
            if len(ind_data) > 0:
                short_name = indicator[:30] + '...' if len(indicator) > 30 else indicator
                ax.errorbar(ind_data['year'], ind_data['numeric_value'],
                           yerr=[ind_data['numeric_value'] - ind_data['low'],
                                 ind_data['high'] - ind_data['numeric_value']],
                           label=short_name, fmt='o-', linewidth=2, markersize=6,
                           capsize=4)

        ax.set_title('Nutrition Indicators with 95% Confidence Intervals', fontsize=14, fontweight='bold')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Prevalence (%)', fontsize=12)
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}11_confidence_intervals.png', dpi=150)
    plt.close()
    print("Saved: 11_confidence_intervals.png")

def plot_all_trends_combined(df):
    """Plot all main nutrition indicators on one chart."""
    fig, ax = plt.subplots(figsize=(14, 7))

    main_indicators = [
        ('Stunting', 'blue'),
        ('Wasting', 'green'),
        ('Underweight', 'orange'),
        ('Anaemia', 'red')
    ]

    for keyword, color in main_indicators:
        indicator_data = df[df['indicator'].str.contains(keyword, case=False)]
        if len(indicator_data) > 0:
            yearly_avg = indicator_data.groupby('year')['numeric_value'].mean()
            ax.plot(yearly_avg.index, yearly_avg.values, 'o-',
                   label=keyword, linewidth=2, markersize=6, color=color)

    ax.set_title('Main Child Nutrition Indicators Trend Over Time', fontsize=14, fontweight='bold')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Prevalence (%)', fontsize=12)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}12_combined_trends.png', dpi=150)
    plt.close()
    print("Saved: 12_combined_trends.png")

def main():
    """Generate all visualizations."""
    print("\n" + "="*60)
    print("GENERATING EDA VISUALIZATIONS")
    print("="*60)

    df = load_data()

    # Generate all plots
    plot_year_range_distribution(df)
    plot_indicator_counts(df)
    plot_stunting_trend(df)
    plot_wasting_trend(df)
    plot_underweight_trend(df)
    plot_dimension_boxplot(df)
    plot_heatmaps(df)
    plot_histograms(df)
    plot_correlation_matrix(df)
    plot_scatter_sex_vs_wealth(df)
    plot_confidence_intervals(df)
    plot_all_trends_combined(df)

    print("\n" + "="*60)
    print(f"ALL VISUALIZATIONS SAVED TO: {OUTPUT_DIR}")
    print("="*60)

if __name__ == "__main__":
    main()
