"""
Week 7: Python Application - Nepal Nutrition Dashboard
======================================================
Interactive Streamlit dashboard for exploring Nepal nutrition data.
Run with: streamlit run Week-7/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Nepal Nutrition Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f8ff;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load and cache the cleaned dataset."""
    df = pd.read_csv("data/processed/cleaned_nutrition_indicators_npl.csv")
    return df

# Main title
st.markdown('<p class="main-header">🏥 Nepal Nutrition Indicators Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">WHO Global Health Observatory Data - Statistical Analysis Application</p>', unsafe_allow_html=True)

# Load data
df = load_data()

# Sidebar navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select a section:",
    [
        "📈 Overview",
        "📉 Trends Over Time",
        "👥 Demographic Analysis",
        "🔬 Statistical Tests",
        "📋 Data Explorer"
    ]
)

# ============ OVERVIEW PAGE ============
if page == "📈 Overview":
    st.header("Dataset Overview")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Year Range", f"{df['year'].min()} - {df['year'].max()}")
    with col3:
        st.metric("Unique Indicators", df['indicator'].nunique())
    with col4:
        st.metric("Countries", df['country'].nunique())

    st.divider()

    # Indicator breakdown
    st.subheader("Nutrition Indicators Available")

    indicator_counts = df.groupby('indicator').size().sort_values(ascending=False)

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = px.bar(
            x=indicator_counts.values[:10],
            y=[name[:50] + '...' if len(name) > 50 else name for name in indicator_counts.index[:10]],
            orientation='h',
            title="Top 10 Indicators by Record Count",
            labels={'x': 'Number of Records', 'y': 'Indicator'},
            color=indicator_counts.values[:10],
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("**Indicator Categories:**")
        categories = {
            "Child Growth": df[df['indicator'].str.contains('Stunting|Wasting|Underweight', case=False)].shape[0],
            "Breastfeeding": df[df['indicator'].str.contains('breastfeed|Breastfeed', case=False)].shape[0],
            "Anaemia": df[df['indicator'].str.contains('Anaemia|Anaemia', case=False)].shape[0],
            "Overweight/Obesity": df[df['indicator'].str.contains('Overweight|obesity', case=False)].shape[0],
            "Low Birth Weight": df[df['indicator'].str.contains('Low birth weight|LBW', case=False)].shape[0],
        }
        for cat, count in categories.items():
            st.write(f"- {cat}: {count} records")

    st.divider()

    # Dimension breakdown
    st.subheader("Data Dimensions")

    col1, col2 = st.columns(2)

    with col1:
        dim_counts = df['dimension_type'].value_counts()
        fig = px.pie(
            values=dim_counts.values,
            names=dim_counts.index,
            title="Records by Dimension Type",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            x=dim_counts.index,
            y=dim_counts.values,
            title="Records by Dimension Type",
            color=dim_counts.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)

# ============ TRENDS PAGE ============
elif page == "📉 Trends Over Time":
    st.header("Trends Over Time")

    # Select indicator
    indicator_options = df['indicator'].unique()
    selected_indicator = st.selectbox(
        "Select an Indicator:",
        options=indicator_options,
        index=0
    )

    # Filter data
    indicator_data = df[df['indicator'] == selected_indicator]

    # Overall trend
    st.subheader(f"Trend for: {selected_indicator[:60]}...")

    yearly_avg = indicator_data.groupby('year')['numeric_value'].mean().reset_index()

    fig = px.line(
        yearly_avg,
        x='year',
        y='numeric_value',
        title="Annual Average",
        markers=True,
        line_shape="spline"
    )
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Value (%)",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

    # Trend by demographic group
    st.subheader("Trend by Demographic Group")

    dimension_type = st.selectbox(
        "Select Dimension:",
        options=df['dimension_type'].unique()
    )

    dim_data = indicator_data[indicator_data['dimension_type'] == dimension_type]

    if len(dim_data) > 0:
        pivot_data = dim_data.pivot_table(
            index='year',
            columns='dimension_name',
            values='numeric_value',
            aggfunc='mean'
        ).reset_index()

        fig = px.line(
            pivot_data,
            x='year',
            y=pivot_data.columns[1:],
            title=f"By {dimension_type}",
            markers=True,
            line_shape="spline"
        )
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Value (%)",
            height=400,
            legend_title="Group"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No data available for {dimension_type}")

    # Multiple indicators comparison
    st.divider()
    st.subheader("Compare Multiple Main Indicators")

    main_indicators = [
        'Stunting prevalence among children under 5 years of age',
        'Wasting prevalence among children under 5 years of age',
        'Underweight prevalence among children under 5 years of age'
    ]

    # Filter for both sexes
    main_data = df[
        (df['indicator'].isin(main_indicators)) &
        (df['dimension_code'] == 'SEX_BTSX')
    ]

    yearly_main = main_data.groupby(['year', 'indicator'])['numeric_value'].mean().reset_index()

    fig = px.line(
        yearly_main,
        x='year',
        y='numeric_value',
        color='indicator',
        title="Main Child Nutrition Indicators Comparison",
        markers=True,
        line_shape="spline"
    )
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Prevalence (%)",
        height=500,
        legend_title="Indicator",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02
        )
    )
    st.plotly_chart(fig, use_container_width=True)

# ============ DEMOGRAPHIC ANALYSIS PAGE ============
elif page == "👥 Demographic Analysis":
    st.header("Demographic Analysis")

    # Select analysis type
    analysis_type = st.radio(
        "Select Analysis Type:",
        ["By Sex", "By Wealth Quintile", "By Residence Area", "By Education Level"]
    )

    indicator = st.selectbox(
        "Select Indicator:",
        options=df['indicator'].unique()
    )

    indicator_data = df[df['indicator'] == indicator]

    if analysis_type == "By Sex":
        dim_type = "SEX"
    elif analysis_type == "By Wealth Quintile":
        dim_type = "WEALTHQUINTILE"
    elif analysis_type == "By Residence Area":
        dim_type = "RESIDENCEAREATYPE"
    else:
        dim_type = "EDUCATIONLEVEL"

    dim_data = indicator_data[indicator_data['dimension_type'] == dim_type]

    if len(dim_data) > 0:
        # Summary statistics
        summary = dim_data.groupby('dimension_name')['numeric_value'].agg(['mean', 'std', 'count', 'min', 'max']).round(2)
        summary.columns = ['Mean', 'Std Dev', 'Count', 'Min', 'Max']

        st.subheader(f"Summary Statistics - {analysis_type}")
        st.dataframe(summary, use_container_width=True)

        # Box plot
        fig = px.box(
            dim_data,
            x='dimension_name',
            y='numeric_value',
            title=f"{indicator[:50]}... by {analysis_type}",
            points="all"
        )
        fig.update_layout(
            xaxis_title=analysis_type,
            yaxis_title="Value (%)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # Bar chart comparison
        mean_data = dim_data.groupby('dimension_name')['numeric_value'].mean().reset_index()

        fig = px.bar(
            mean_data,
            x='dimension_name',
            y='numeric_value',
            title=f"Mean Value by {analysis_type}",
            color='numeric_value',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            xaxis_title=analysis_type,
            yaxis_title="Mean Value (%)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning(f"No data available for this combination")

    # Heatmap
    st.divider()
    st.subheader("Indicator Heatmap by Year and Group")

    # Get stunting data
    stunting = df[
        (df['indicator'].str.contains('Stunting', case=False)) &
        (df['dimension_type'] == dim_type)
    ]

    if len(stunting) > 0:
        pivot = stunting.pivot_table(
            index='dimension_name',
            columns='year',
            values='numeric_value',
            aggfunc='mean'
        )

        fig = px.imshow(
            pivot.values,
            x=pivot.columns,
            y=pivot.index,
            color_continuous_scale='YlOrRd',
            title="Stunting Prevalence Heatmap",
            labels=dict(x="Year", y="Group", color="Prevalence (%)")
        )
        st.plotly_chart(fig, use_container_width=True)

# ============ STATISTICAL TESTS PAGE ============
elif page == "🔬 Statistical Tests":
    st.header("Statistical Analysis")

    st.info("📊 This section presents results from statistical tests conducted on the Nepal nutrition data.")

    # Hypothesis tests summary
    st.subheader("Hypothesis Tests Summary")

    tests = [
        {
            "Test": "Linear Regression (Trend)",
            "Hypothesis": "Stunting prevalence changes over time",
            "Result": "Significant negative trend (p < 0.05)",
            "Conclusion": "Stunting decreases by ~1% per year"
        },
        {
            "Test": "T-Test (Sex Differences)",
            "Hypothesis": "Stunting differs between male and female",
            "Result": "No significant difference (p > 0.05)",
            "Conclusion": "Similar stunting rates by sex"
        },
        {
            "Test": "ANOVA (Wealth Quintile)",
            "Hypothesis": "Stunting differs across wealth groups",
            "Result": "Significant difference (p < 0.05)",
            "Conclusion": "Lower stunting in richer households"
        }
    ]

    for i, test in enumerate(tests):
        with st.expander(f"📌 {test['Test']}"):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write(f"**Hypothesis:**")
                st.write(f"**Result:**")
                st.write(f"**Conclusion:**")
            with col2:
                st.write(test['Hypothesis'])
                st.write(test['Result'])
                st.write(test['Conclusion'])

    # Run custom test
    st.divider()
    st.subheader("Run Statistical Test")

    test_type = st.selectbox(
        "Select Test:",
        ["T-Test", "ANOVA", "Correlation"]
    )

    if test_type == "T-Test":
        col1, col2 = st.columns(2)

        with col1:
            group1_name = st.selectbox("Group 1:", options=df['dimension_name'].unique(), key="g1")
        with col2:
            group2_name = st.selectbox("Group 2:", options=df['dimension_name'].unique(), key="g2")

        indicator_select = st.selectbox("Indicator:", options=df['indicator'].unique())

        if st.button("Run T-Test"):
            from scipy import stats

            g1_data = df[
                (df['dimension_name'] == group1_name) &
                (df['indicator'] == indicator_select)
            ]['numeric_value'].dropna()

            g2_data = df[
                (df['dimension_name'] == group2_name) &
                (df['indicator'] == indicator_select)
            ]['numeric_value'].dropna()

            if len(g1_data) > 1 and len(g2_data) > 1:
                t_stat, p_value = stats.ttest_ind(g1_data, g2_data)

                col1, col2, col3 = st.columns(3)
                col1.metric("Group 1 Mean", f"{g1_data.mean():.2f}")
                col2.metric("Group 2 Mean", f"{g2_data.mean():.2f}")
                col3.metric("P-Value", f"{p_value:.4f}")

                if p_value < 0.05:
                    st.success("✅ Significant difference detected!")
                else:
                    st.info("ℹ️ No significant difference")
            else:
                st.warning("Insufficient data for t-test")

    elif test_type == "ANOVA":
        indicator_select = st.selectbox("Indicator:", options=df['indicator'].unique(), key="anova_ind")
        dim_type = st.selectbox("Grouping Dimension:", options=df['dimension_type'].unique())

        if st.button("Run ANOVA"):
            from scipy import stats

            group_data = df[
                (df['indicator'] == indicator_select) &
                (df['dimension_type'] == dim_type)
            ]

            groups = [group['numeric_value'].dropna().values
                     for name, group in group_data.groupby('dimension_name')]

            if len(groups) >= 2 and all(len(g) > 1 for g in groups):
                f_stat, p_value = stats.f_oneway(*groups)

                col1, col2 = st.columns(2)
                col1.metric("F-Statistic", f"{f_stat:.4f}")
                col2.metric("P-Value", f"{p_value:.4f}")

                if p_value < 0.05:
                    st.success("✅ Significant difference between groups!")
                else:
                    st.info("ℹ️ No significant difference between groups")
            else:
                st.warning("Insufficient data for ANOVA")

    elif test_type == "Correlation":
        st.info("Correlation analysis shows relationships between nutrition indicators over time.")

        # Show correlation for main indicators
        main_inds = ['Stunting', 'Wasting', 'Underweight', 'Anaemia']
        corr_data = []

        for ind in main_inds:
            ind_data = df[
                (df['indicator'].str.contains(ind, case=False)) &
                (df['dimension_code'] == 'SEX_BTSX')
            ].groupby('year')['numeric_value'].mean()

            if len(ind_data) > 2:
                corr_data.append(pd.Series(ind_data.values, name=ind, index=ind_data.index))

        if len(corr_data) > 1:
            corr_df = pd.concat(corr_data, axis=1).dropna()

            if corr_df.shape[0] > 2:
                corr_matrix = corr_df.corr()

                fig = px.imshow(
                    corr_matrix.values,
                    x=corr_df.columns,
                    y=corr_df.columns,
                    color_continuous_scale='RdBu_r',
                    title="Correlation Matrix",
                    labels=dict(color="Correlation")
                )
                st.plotly_chart(fig, use_container_width=True)

# ============ DATA EXPLORER PAGE ============
elif page == "📋 Data Explorer":
    st.header("Data Explorer")

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        year_min, year_max = int(df['year'].min()), int(df['year'].max())
        year_range = st.slider(
            "Select Year Range:",
            min_value=year_min,
            max_value=year_max,
            value=(year_min, year_max)
        )

    with col2:
        selected_indicators = st.multiselect(
            "Select Indicators:",
            options=df['indicator'].unique(),
            default=df['indicator'].unique()[:3]
        )

    with col3:
        selected_dimensions = st.multiselect(
            "Select Dimensions:",
            options=df['dimension_type'].unique(),
            default=df['dimension_type'].unique()[:2]
        )

    # Filter data
    filtered_df = df[
        (df['year'] >= year_range[0]) &
        (df['year'] <= year_range[1]) &
        (df['indicator'].isin(selected_indicators)) &
        (df['dimension_type'].isin(selected_dimensions))
    ]

    st.divider()

    # Show filtered data
    st.subheader(f"Filtered Data ({len(filtered_df)} records)")

    display_df = filtered_df[[
        'year', 'indicator', 'dimension_type', 'dimension_name',
        'numeric_value', 'low', 'high'
    ]].copy()

    display_df['indicator'] = display_df['indicator'].str[:50] + '...'

    st.dataframe(
        display_df.head(100),
        use_container_width=True,
        height=400
    )

    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_nepal_nutrition.csv",
        mime="text/csv"
    )

# Footer
st.divider()
st.markdown(
    """
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Data 200 Applied Statistical Analysis | Nepal Nutrition Indicators Analysis</p>
        <p>Data Source: WHO Global Health Observatory (GHO)</p>
    </div>
    """,
    unsafe_allow_html=True
)
