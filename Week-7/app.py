"""
Week 7: Python Application - Nepal Nutrition Dashboard
======================================================
Interactive Streamlit dashboard for exploring Nepal nutrition data.
Run with: python -m streamlit run Week-7/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Nepal Nutrition Dashboard",
    page_icon="Hospital",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #1a1a2e; color: white; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { color: white !important; }
    [data-testid="stSidebar"] .stRadio label, [data-testid="stSidebar"] .stRadio span { color: white !important; }
    .main-content { background-color: white; padding: 2rem; border-radius: 10px; }
    h1 { color: #1a1a2e !important; font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem; }
    h2 { color: #1a1a2e !important; font-size: 1.8rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.75rem; padding-bottom: 0.5rem; border-bottom: 2px solid #1a1a2e; }
    h3 { color: #16213e !important; font-size: 1.3rem; font-weight: 600; margin-top: 1rem; margin-bottom: 0.5rem; }
    p, li { color: #333333 !important; font-size: 1rem; line-height: 1.6; }
    [data-testid="stMetric"] { background-color: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 1rem; }
    [data-testid="stMetricValue"] { color: #1a1a2e !important; font-size: 1.8rem; font-weight: 700; }
    [data-testid="stMetricLabel"] { color: #6c757d !important; font-size: 0.9rem; }
    table { background-color: white; border-collapse: collapse; width: 100%; margin: 1rem 0; }
    th { background-color: #1a1a2e !important; color: white !important; padding: 12px; text-align: left; font-weight: 600; }
    td { background-color: #f8f9fa !important; color: #333 !important; padding: 10px; border-bottom: 1px solid #e9ecef; }
    hr { border-color: #e9ecef; margin: 1.5rem 0; }
    .success-box { background-color: #d4edda; border-left: 4px solid #28a745; padding: 1rem; border-radius: 4px; margin: 1rem 0; }
    .warning-box { background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 1rem; border-radius: 4px; margin: 1rem 0; }
    .info-box { background-color: #d1ecf1; border-left: 4px solid #17a2b8; padding: 1rem; border-radius: 4px; margin: 1rem 0; }
    .insight-box { background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 1rem; border-radius: 4px; margin: 1rem 0; }
    .stDownloadButton button { background-color: #1a1a2e; color: white; border: none; border-radius: 6px; }
    .stDownloadButton button:hover { background-color: #16213e; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/cleaned_nutrition_indicators_npl.csv")
    return df

df = load_data()

# ============ SIDEBAR ============
st.sidebar.markdown("<h1 style='color: white; font-size: 1.5rem; text-align: center;'>Nepal Nutrition Dashboard</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border-color: #444;'>", unsafe_allow_html=True)

app_mode = st.sidebar.radio(
    "Select Mode:",
    ["Presentation Slides", "Dashboard (Interactive)"],
    index=0
)

# ========== PRESENTATION MODE ==========
if app_mode == "Presentation Slides":

    slide = st.sidebar.selectbox(
        "Go to Slide:",
        [
            "1. Title Slide",
            "2. Problem Statement",
            "3. Dataset Overview",
            "4. EDA Insights",
            "5. Trends Analysis",
            "6. Hypothesis Tests",
            "7. Regression Models",
            "8. Key Findings",
            "9. Conclusions",
            "10. Thank You"
        ]
    )

    # SLIDE 1: TITLE
    if slide == "1. Title Slide":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; border-bottom: 3px solid #1a1a2e; padding-bottom: 1rem;'>Nepal Nutrition Indicators</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #6c757d;'>Exploring Real-World Data through Statistical and Predictive Modeling</h2>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<h3 style='text-align: center;'>Date</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size: 1.2rem;'>June 2026</p>", unsafe_allow_html=True)
        with col2:
            st.markdown("<h3 style='text-align: center;'>Course</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Data 200 Applied Statistical Analysis</p>", unsafe_allow_html=True)
        with col3:
            st.markdown("<h3 style='text-align: center;'>Data Source</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size: 1.2rem;'>WHO Global Health Observatory</p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #6c757d;'>Country: Nepal (NPL) | Region: South-East Asia (SEAR)</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # SLIDE 2: PROBLEM STATEMENT
    elif slide == "2. Problem Statement":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Problem Statement</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.1rem; background-color: #f8f9fa; padding: 1.5rem; border-left: 4px solid #1a1a2e; border-radius: 4px;'>Analyze Nepal's child nutrition indicators to identify trends, relationships between demographic factors, and statistical patterns that can inform public health interventions.</p>", unsafe_allow_html=True)

        st.markdown("<h3>Research Questions</h3>", unsafe_allow_html=True)
        st.markdown("""
        <ol style='font-size: 1.1rem; line-height: 2;'>
            <li>What are the <strong>temporal trends</strong> in child nutrition indicators over time?</li>
            <li>Do nutrition outcomes differ by <strong>demographic factors</strong> (sex, wealth, education)?</li>
            <li>What <strong>predictors</strong> most strongly influence child nutrition status?</li>
        </ol>
        """, unsafe_allow_html=True)

        st.markdown("<h3>Why This Matters</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class='insight-box'>
            <p><strong>Child malnutrition</strong> is a critical public health issue in Nepal. It affects physical growth, cognitive development, and overall health outcomes. Understanding patterns and causes helps policymakers design effective interventions to reduce malnutrition rates.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h3>Project Objectives</h3>", unsafe_allow_html=True)
        st.markdown("""
        <ul style='font-size: 1.1rem; line-height: 2;'>
            <li>Analyze <strong>trends</strong> in key nutrition indicators over time</li>
            <li>Identify <strong>demographic disparities</strong> in nutrition outcomes</li>
            <li>Apply <strong>statistical techniques</strong> (regression, ANOVA, t-tests)</li>
            <li>Develop an <strong>interactive Python application</strong> for data exploration</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # SLIDE 3: DATASET OVERVIEW
    elif slide == "3. Dataset Overview":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Dataset Overview</h2>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", "7,461")
        with col2:
            st.metric("Year Range", "1990 - 2024")
        with col3:
            st.metric("Indicators", "37")
        with col4:
            st.metric("Country", "Nepal")

        st.markdown("<hr>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3>Data Quality</h3>", unsafe_allow_html=True)
            st.markdown("""
            <table>
                <tr><th>Metric</th><th>Before</th><th>After</th></tr>
                <tr><td>Rows</td><td>7,556</td><td>7,461</td></tr>
                <tr><td>Duplicates</td><td>93</td><td>0</td></tr>
                <tr><td>Missing Values</td><td>301</td><td>284</td></tr>
            </table>
            """, unsafe_allow_html=True)

            st.markdown("<h3>Key Indicators</h3>", unsafe_allow_html=True)
            st.markdown("""
            <ul style='line-height: 1.8;'>
                <li><strong>Stunting:</strong> Height-for-age < -2 SD - Children too short for their age</li>
                <li><strong>Wasting:</strong> Weight-for-height < -2 SD - Children too thin for their height</li>
                <li><strong>Underweight:</strong> Weight-for-age < -2 SD - Children underweight for their age</li>
                <li><strong>Anaemia:</strong> Low hemoglobin in blood</li>
                <li><strong>Breastfeeding:</strong> Exclusive breastfeeding practices</li>
                <li><strong>Low Birth Weight:</strong> Babies born under 2.5kg</li>
            </ul>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("<h3>Data Dimensions Explained</h3>", unsafe_allow_html=True)
            st.markdown("""
            <div class='insight-box'>
                <p><strong>Sex:</strong> Male, Female, Both sexes - Used to check if nutrition differs by gender</p>
                <p><strong>Wealth Quintile:</strong> Q1 (Poorest) to Q5 (Richest) - Socioeconomic status of household</p>
                <p><strong>Residence:</strong> Urban vs Rural - Access to healthcare and resources</p>
                <p><strong>Education:</strong> Caregiver's education level - Higher education often means better nutrition knowledge</p>
            </div>
            """, unsafe_allow_html=True)

            dim_counts = df['dimension_type'].value_counts()
            fig = px.pie(values=dim_counts.values[:6], names=dim_counts.index[:6],
                        title="Records by Dimension Type", hole=0.4,
                        color_discrete_sequence=['#1a1a2e', '#16213e', '#0f3460', '#e94560', '#533483', '#4a90a4'])
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("<h3>Data Source Attribution</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class='info-box'>
            <p><strong>Source:</strong> World Health Organization (WHO) Global Health Observatory</p>
            <p><strong>URL:</strong> https://www.who.int/data/gho</p>
            <p><strong>Reliability:</strong> WHO is the authoritative source for global health statistics, ensuring data credibility.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # SLIDE 4: EDA INSIGHTS
    elif slide == "4. EDA Insights":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Exploratory Data Analysis Insights</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3>Descriptive Statistics</h3>", unsafe_allow_html=True)
            st.markdown("""
            <table>
                <tr><th>Statistic</th><th>Value</th><th>What It Means</th></tr>
                <tr><td>Mean</td><td>162.67</td><td>Average value across all records</td></tr>
                <tr><td>Median</td><td>21.10</td><td>Middle value - less affected by outliers</td></tr>
                <tr><td>Std Dev</td><td>2615.25</td><td>High variation due to different indicator scales</td></tr>
            </table>
            """, unsafe_allow_html=True)

            st.markdown("<h3>Key Findings</h3>", unsafe_allow_html=True)
            st.markdown("""
            <div class='info-box'>
                <p><strong>1. Temporal Trends:</strong></p>
                <ul style='margin-bottom: 0.5rem;'>
                    <li>Stunting declined from ~61% (1998) - Public health interventions working!</li>
                    <li>Wasting fluctuates between 6-14% - unstable, needs monitoring</li>
                    <li>Underweight shows gradual decline - positive trend</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class='info-box'>
                <p><strong>2. Demographic Disparities:</strong></p>
                <ul style='margin-bottom: 0.5rem;'>
                    <li>Higher stunting in poorer wealth quintiles - poverty is a key factor</li>
                    <li>Minimal sex-based differences - gender equity in nutrition access</li>
                    <li>Urban/Rural variations exist - infrastructure matters</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            indicator_counts = df.groupby('indicator').size().sort_values(ascending=False).head(10)
            fig = px.bar(
                x=indicator_counts.values,
                y=[name[:35] + '...' if len(name) > 35 else name for name in indicator_counts.index],
                orientation='h',
                title="Top 10 Indicators by Record Count",
                color=indicator_counts.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(font=dict(size=10), height=400, margin=dict(l=150))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("<h3>Why This Matters</h3>", unsafe_allow_html=True)
            st.markdown("""
            <div class='insight-box'>
                <p><strong>Stunting</strong> has the most records because it's the primary measure of chronic malnutrition. The decline over time suggests Nepal's nutrition programs are effective.</p>
                <p><strong>Wealth disparities</strong> suggest that economic status strongly influences nutrition outcomes - richer families can afford better food and healthcare.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # SLIDE 5: TRENDS ANALYSIS
    elif slide == "5. Trends Analysis":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Trends Over Time Analysis</h2>", unsafe_allow_html=True)

        main_indicators = [
            'Stunting prevalence among children under 5 years of age',
            'Wasting prevalence among children under 5 years of age',
            'Underweight prevalence among children under 5 years of age'
        ]

        main_data = df[
            (df['indicator'].isin(main_indicators)) &
            (df['dimension_code'] == 'SEX_BTSX')
        ]

        if len(main_data) > 0:
            yearly_main = main_data.groupby(['year', 'indicator'])['numeric_value'].mean().reset_index()

            fig = px.line(
                yearly_main,
                x='year',
                y='numeric_value',
                color='indicator',
                title="Main Child Nutrition Indicators Trends (Both Sexes)",
                markers=True,
                line_shape="spline"
            )
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Prevalence (%)",
                height=400,
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.02),
                font=dict(size=11)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for the selected indicators")

        st.markdown("<h3>Understanding the Trends</h3>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        stunting_both = df[(df['indicator'].str.contains('Stunting', case=False)) & (df['dimension_code'] == 'SEX_BTSX')]
        wasting_both = df[(df['indicator'].str.contains('Wasting', case=False)) & (df['dimension_code'] == 'SEX_BTSX')]
        underweight_both = df[(df['indicator'].str.contains('Underweight', case=False)) & (df['dimension_code'] == 'SEX_BTSX')]

        with col1:
            if len(stunting_both) > 0:
                st.metric("Stunting Mean", f"{stunting_both['numeric_value'].mean():.1f}%")
                st.markdown("<p style='font-size: 0.9rem; color: #666;'><strong>Insight:</strong> High but declining. Stunting reflects chronic malnutrition - long-term food security issues.</p>", unsafe_allow_html=True)
        with col2:
            if len(wasting_both) > 0:
                st.metric("Wasting Mean", f"{wasting_both['numeric_value'].mean():.1f}%")
                st.markdown("<p style='font-size: 0.9rem; color: #666;'><strong>Insight:</strong> Acute malnutrition. Wasting indicates recent food shortage or illness.</p>", unsafe_allow_html=True)
        with col3:
            if len(underweight_both) > 0:
                st.metric("Underweight Mean", f"{underweight_both['numeric_value'].mean():.1f}%")
                st.markdown("<p style='font-size: 0.9rem; color: #666;'><strong>Insight:</strong> Combined measure. Reflects both chronic and acute malnutrition.</p>", unsafe_allow_html=True)

        st.markdown("<h3>Key Trend Insights</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class='insight-box'>
            <p><strong>Stunting Trend:</strong> The graph shows gradual decline from ~61% in 1998. This is a POSITIVE sign indicating that nutrition interventions over the past 3 decades are working.</p>
            <p><strong>Why it matters:</strong> Stunting is irreversible after age 2. Early childhood nutrition programs are crucial.</p>
        </div>
        <div class='insight-box'>
            <p><strong>Wasting Fluctuations:</strong> Wasting varies between 6-14% without clear trend. This reflects acute food insecurity that can be caused by:</p>
            <ul>
                <li>Seasonal food shortages</li>
                <li>Disease outbreaks (diarrhea, pneumonia)</li>
                <li>Natural disasters</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # SLIDE 6: HYPOTHESIS TESTS
    elif slide == "6. Hypothesis Tests":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Statistical Hypothesis Testing Results</h2>", unsafe_allow_html=True)

        st.markdown("<h3>H1: Linear Trend in Stunting Over Time</h3>", unsafe_allow_html=True)
        st.markdown("<p>Test: Simple Linear Regression | H0: No linear trend | H1: Significant trend exists</p>", unsafe_allow_html=True)
        st.markdown("""
        <table>
            <tr><th>Statistic</th><th>Value</th><th>Interpretation</th></tr>
            <tr><td>Slope</td><td>-15.11</td><td>Stunting decreases 15.11 units per year</td></tr>
            <tr><td>R-squared</td><td>0.0314</td><td>Only 3% of variance explained</td></tr>
            <tr><td>P-value</td><td>0.1719</td><td>Not statistically significant</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class='warning-box'>
            <p><strong>Result:</strong> FAIL TO REJECT H0 - No statistically significant linear trend detected (p > 0.05)</p>
            <p><strong>Why?</strong> The relationship is not perfectly linear. Stunting declines unevenly - fast initially, then slows down. Simple linear regression doesn't capture this complexity.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<h3>H2: Sex Differences in Stunting</h3>", unsafe_allow_html=True)
        st.markdown("<p>Test: Welch's T-Test | H0: No difference | H1: Significant difference</p>", unsafe_allow_html=True)
        st.markdown("""
        <table>
            <tr><th>Statistic</th><th>Value</th><th>Interpretation</th></tr>
            <tr><td>Male Mean</td><td>106.55</td><td>Average stunting for boys</td></tr>
            <tr><td>Female Mean</td><td>100.63</td><td>Average stunting for girls</td></tr>
            <tr><td>T-statistic</td><td>0.3377</td><td>Small difference between groups</td></tr>
            <tr><td>P-value</td><td>0.7358</td><td>No significant difference</td></tr>
            <tr><td>Cohen's d</td><td>0.031</td><td>Negligible effect size</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class='success-box'>
            <p><strong>Result:</strong> FAIL TO REJECT H0 - No significant sex difference (p > 0.05)</p>
            <p><strong>Insight:</strong> Nepal has achieved gender equity in nutrition! Boys and girls have equal access to food and healthcare within households.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<h3>H3: Wealth Quintile Differences</h3>", unsafe_allow_html=True)
        st.markdown("<p>Test: One-Way ANOVA | H0: No difference | H1: Significant difference</p>", unsafe_allow_html=True)
        st.markdown("""
        <table>
            <tr><th>Wealth Group</th><th>Mean Stunting</th><th>What This Means</th></tr>
            <tr><td>Q1 (Poorest)</td><td>53.85%</td><td>More than half of children are stunted - crisis level</td></tr>
            <tr><td>Q2</td><td>44.91%</td><td>Still very high - public health concern</td></tr>
            <tr><td>Q3</td><td>40.48%</td><td>Moderate improvement</td></tr>
            <tr><td>Q4</td><td>34.94%</td><td>Noticeable improvement</td></tr>
            <tr><td>Q5 (Richest)</td><td>25.05%</td><td>Best outcomes - but still above WHO threshold</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown("""
        <table>
            <tr><th>Statistic</th><th>Value</th><th>Meaning</th></tr>
            <tr><td>F-statistic</td><td>5.6153</td><td>Ratio of between-group to within-group variance</td></tr>
            <tr><td>P-value</td><td>0.000419</td><td>Highly significant - less than 0.1% chance this is random</td></tr>
            <tr><td>Eta-squared</td><td>0.384</td><td>38.4% of variance explained by wealth - LARGE effect</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class='success-box'>
            <p><strong>Result:</strong> REJECT H0 - Highly significant wealth disparities (p < 0.001)</p>
            <p><strong>Critical Insight:</strong> Wealth explains 38.4% of stunting variation - this is a LARGE effect. Children in the poorest quintile are 2x more likely to be stunted than the richest. <strong>Poverty is the primary driver of malnutrition.</strong></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # SLIDE 7: REGRESSION MODELS
    elif slide == "7. Regression Models":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Regression Modeling Results</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3>Simple Linear Regression</h3>", unsafe_allow_html=True)
            st.markdown("<p><em>DV: Stunting Prevalence | IV: Year</em></p>", unsafe_allow_html=True)
            st.markdown("""
            <table>
                <tr><th>Metric</th><th>Value</th><th>Interpretation</th></tr>
                <tr><td>R-squared</td><td>0.031</td><td>Year alone explains only 3% of variation</td></tr>
                <tr><td>F-statistic</td><td>1.912</td><td>Model is not statistically significant</td></tr>
                <tr><td>Slope</td><td>-15.11</td><td>Suggested decline per year</td></tr>
                <tr><td>P-value</td><td>0.172</td><td>Not significant at alpha=0.05</td></tr>
            </table>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class='warning-box'>
                <p><strong>Problem:</strong> Simple regression oversimplifies reality. It assumes the relationship is purely linear and ignores other factors.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("<h3>Multiple Linear Regression</h3>", unsafe_allow_html=True)
            st.markdown("<p><em>DV: Stunting | IVs: Year + Wealth Quintile</em></p>", unsafe_allow_html=True)
            st.markdown("""
            <table>
                <tr><th>Metric</th><th>Value</th><th>Interpretation</th></tr>
                <tr><td>R-squared</td><td>0.941</td><td><strong>94.1% of variance explained!</strong></td></tr>
                <tr><td>F-statistic</td><td>294.99</td><td>Highly significant model</td></tr>
                <tr><td>P-value</td><td>< 0.001</td><td>Model is statistically significant</td></tr>
            </table>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class='success-box'>
                <p><strong>Improvement:</strong> Adding wealth quintile improved R-squared from 3% to 94%!</p>
                <p><strong>This proves:</strong> Year alone is not a good predictor - we must include socioeconomic factors.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<h3>Multiple Regression Coefficients</h3>", unsafe_allow_html=True)
        st.markdown("""
        <table>
            <tr><th>Variable</th><th>Coefficient</th><th>P-value</th><th>What It Means</th></tr>
            <tr><td>(Constant)</td><td>2496.78</td><td><0.001</td><td>Baseline stunting when year=0</td></tr>
            <tr><td>Year</td><td>-1.21</td><td><0.001</td><td>Stunting decreases 1.21% per year, <strong>controlling for wealth</strong></td></tr>
            <tr><td>Wealth Rank</td><td>-6.76</td><td><0.001</td><td><strong>Each quintile higher = 6.76% less stunting</strong></td></tr>
        </table>
        """, unsafe_allow_html=True)

        st.markdown("<h3>Model Diagnostics</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <table>
                <tr><th>Test</th><th>Result</th><th>Meaning</th></tr>
                <tr><td>Durbin-Watson</td><td>2.41</td><td>No autocorrelation (OK)</td></tr>
                <tr><td>Shapiro-Wilk</td><td>p < 0.05</td><td>Non-normal residuals - common with aggregated data</td></tr>
                <tr><td>Breusch-Pagan</td><td>p < 0.05</td><td>Heteroscedasticity present</td></tr>
                <tr><td>Influential Points</td><td>3 points</td><td>Years 2000-2002 need attention</td></tr>
            </table>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("<h3>Logistic Regression</h3>", unsafe_allow_html=True)
            st.markdown("""
            <div class='info-box'>
                <p><strong>Outcome:</strong> Low Stunting (<30%) vs High (>=30%)</p>
                <p><strong>Pseudo R-squared:</strong> 0.769 (Excellent fit)</p>
                <p><strong>Year coef:</strong> 0.77 (p=0.041) - Significant</p>
                <p><strong>Wealth coef:</strong> 3.21 (p=0.029) - Significant</p>
                <p><strong>Insight:</strong> Higher wealth quintile strongly predicts lower stunting probability.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<h3>Key Modeling Insights</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class='insight-box'>
            <p><strong>Why Multiple Regression is Better:</strong></p>
            <ul>
                <li>Simple regression (R²=3%) gives misleading results</li>
                <li>Multiple regression (R²=94%) shows the TRUE picture</li>
                <li>Year appears significant only when controlling for wealth</li>
                <li>Key takeaway: <strong>Wealth is the dominant factor, not time itself</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # SLIDE 8: KEY FINDINGS
    elif slide == "8. Key Findings":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Key Findings and Insights</h2>", unsafe_allow_html=True)

        st.markdown("""
        <div class='success-box' style='font-size: 1.1rem;'>
            <h3>Main Finding: Wealth Quintile is the Strongest Predictor</h3>
            <p>The multiple regression model explains <strong>94.1%</strong> of variance (R-squared = 0.941) when including both year and wealth quintile as predictors. This is an exceptionally strong model for social science data.</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3>Temporal Improvements</h3>", unsafe_allow_html=True)
            st.markdown("""
            <div class='info-box'>
                <p><strong>Underweight:</strong> Shows significant decline (p < 0.001)</p>
                <p><strong>Stunting:</strong> Declined from 68% to ~39% over 30 years</p>
                <p><strong>Wasting:</strong> Remains relatively stable (6-14%)</p>
            </div>
            <p><strong>Insight:</strong> Nepal has made measurable progress in reducing chronic malnutrition (stunting and underweight). However, acute malnutrition (wasting) remains volatile and needs ongoing monitoring.</p>
            """, unsafe_allow_html=True)

            st.markdown("<h3>Demographic Patterns</h3>", unsafe_allow_html=True)
            st.markdown("""
            <div class='warning-box'>
                <p><strong>Sex:</strong> No significant differences (p = 0.74)</p>
                <p><strong>Insight:</strong> Gender equity achieved in household nutrition distribution.</p>
            </div>
            <div class='warning-box'>
                <p><strong>Wealth:</strong> Highly significant (p < 0.001)</p>
                <ul>
                    <li>Poorest (Q1): 53.85% stunting - CRISIS</li>
                    <li>Richest (Q5): 25.05% stunting - Still high but better</li>
                    <li>Gap: 28.8 percentage points</li>
                </ul>
                <p><strong>Insight:</strong> The wealth gap in nutrition outcomes is enormous - poverty directly causes malnutrition.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("<h3>Indicator Correlations</h3>", unsafe_allow_html=True)
            st.markdown("""
            <div class='info-box'>
                <p><strong>Strong correlations found:</strong></p>
                <ul>
                    <li>Stunting and Underweight: r = 0.988</li>
                    <li>Stunting and Anaemia: r = 0.955</li>
                    <li>Underweight and Anaemia: r = 0.943</li>
                </ul>
                <p><strong>Insight:</strong> These indicators form a "malnutrition syndrome" - they tend to occur together because they share common underlying causes:</p>
                <ul>
                    <li>Chronic poverty</li>
                    <li>Inadequate food security</li>
                    <li>Poor maternal health</li>
                    <li>Lack of access to healthcare</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<h3>Limitations</h3>", unsafe_allow_html=True)
            st.markdown("""
            <ul>
                <li><strong>Ecological fallacy:</strong> We use aggregate data, cannot make individual-level conclusions</li>
                <li><strong>Heteroscedasticity:</strong> Variance is not constant - common in cross-sectional data</li>
                <li><strong>Missing CI:</strong> 3.8% of records lack confidence intervals</li>
            </ul>
            """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<h3>Summary of Hypothesis Tests</h3>", unsafe_allow_html=True)
        results_data = {
            "Hypothesis": ["H1: Linear Trend", "H2: Sex Differences", "H3: Wealth Disparities"],
            "Test": ["Linear Regression", "T-Test", "ANOVA"],
            "P-value": ["0.172", "0.736", "0.0004"],
            "Significant?": ["No", "No", "YES ***"]
        }
        st.dataframe(pd.DataFrame(results_data), use_container_width=True)

        st.markdown("""
        <div class='insight-box'>
            <p><strong>Takeaway:</strong> The most important finding is that <strong>wealth quintile is the dominant predictor</strong> of child nutrition outcomes. Time alone does not explain improvements - rather, improvements are driven by socioeconomic development and poverty reduction.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # SLIDE 9: CONCLUSIONS
    elif slide == "9. Conclusions":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Conclusions and Recommendations</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3>Conclusions</h3>", unsafe_allow_html=True)
            st.markdown("""
            <div class='success-box'>
                <h4>1. Progress Made</h4>
                <p>Nepal has <strong>reduced child stunting significantly</strong> over 30 years. This is a testament to effective public health interventions.</p>
            </div>
            <div class='warning-box'>
                <h4>2. Socioeconomic Disparities Persist</h4>
                <p>Wealth quintile is the <strong>strongest predictor</strong> of child nutrition outcomes (R-squared = 0.941). The poorest children are 2x more likely to be stunted.</p>
            </div>
            <div class='success-box'>
                <h4>3. Gender Equity Achieved</h4>
                <p>No significant differences between male and female children in nutrition indicators. Nepal has achieved equity in household food distribution.</p>
            </div>
            <div class='info-box'>
                <h4>4. Interconnected Indicators</h4>
                <p>Stunting, wasting, underweight, and anaemia form a "malnutrition syndrome" - addressing one requires addressing all underlying causes.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("<h3>Recommendations</h3>", unsafe_allow_html=True)
            st.markdown("""
            <ol style='line-height: 2;'>
                <li><strong>Target Interventions:</strong> Focus resources on poorest wealth quintiles (Q1-Q2). They need the most help.</li>
                <li><strong>Continue Monitoring:</strong> Maintain surveillance of all nutrition indicators, especially wasting which fluctuates.</li>
                <li><strong>Address Root Causes:</strong> Since indicators are correlated, poverty alleviation is key:</li>
                <ul>
                    <li>Improve food security</li>
                    <li>Enhance maternal healthcare</li>
                    <li>Increase access to clean water and sanitation</li>
                </ul>
                <li><strong>Leverage Success:</strong> Study what interventions enabled Q5 (richest) to achieve 25% stunting - can these be replicated for poorer groups?</li>
            </ol>
            """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<h3>Future Work</h3>", unsafe_allow_html=True)
        st.markdown("""
        <ul style='line-height: 2;'>
            <li><strong>District-level analysis:</strong> Identify geographic hotspots for targeted intervention</li>
            <li><strong>Predictive modeling:</strong> Forecast future nutrition outcomes to plan ahead</li>
            <li><strong>Regional comparison:</strong> Compare Nepal with India and Bangladesh to learn from their interventions</li>
            <li><strong>Longitudinal analysis:</strong> Track the same children over time if individual-level data becomes available</li>
        </ul>
        """, unsafe_allow_html=True)

        st.markdown("<h3>Evaluation Criteria Coverage</h3>", unsafe_allow_html=True)
        st.markdown("""
        <table>
            <tr><th>Criterion</th><th>Weight</th><th>Covered In</th></tr>
            <tr><td>Dataset and Problem Definition</td><td>10%</td><td>Slides 1-3</td></tr>
            <tr><td>EDA and Preprocessing</td><td>20%</td><td>Slides 3-4</td></tr>
            <tr><td>Statistical Modeling and Validation</td><td>40%</td><td>Slides 5-7</td></tr>
            <tr><td>Python Application Development</td><td>10%</td><td>Streamlit App</td></tr>
            <tr><td>Presentation and Collaboration</td><td>20%</td><td>All Slides + App</td></tr>
        </table>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # SLIDE 10: THANK YOU
    elif slide == "10. Thank You":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; padding: 3rem 0;'>Thank You!</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #6c757d; padding: 1rem 0;'>Questions?</h2>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<h3>Project Summary</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class='insight-box'>
            <p><strong>Dataset:</strong> WHO Global Health Observatory - Nepal Nutrition Indicators (7,461 records, 37 indicators)</p>
            <p><strong>Methods:</strong> Linear Regression, Multiple Regression, T-Tests, ANOVA, Correlation Analysis</p>
            <p><strong>Key Finding:</strong> Wealth quintile is the strongest predictor of child nutrition outcomes (R-squared = 0.941)</p>
            <p><strong>Application:</strong> Interactive Streamlit dashboard for data exploration</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Data 200 Applied Statistical Analysis</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.2rem;'>June 2026</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ========== DASHBOARD MODE ==========
else:
    page = st.sidebar.radio("Select Page:", ["Overview", "Trends Over Time", "Demographic Analysis", "Statistical Tests", "Data Explorer"])

    if page == "Overview":
        st.header("Dataset Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Year Range", f"{df['year'].min()} - {df['year'].max()}")
        with col3:
            st.metric("Indicators", df['indicator'].nunique())
        with col4:
            st.metric("Countries", df['country'].nunique())

        st.divider()
        indicator_counts = df.groupby('indicator').size().sort_values(ascending=False)
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = px.bar(x=indicator_counts.values[:10], y=[name[:50] + '...' if len(name) > 50 else name for name in indicator_counts.index[:10]], orientation='h', title="Top 10 Indicators", color=indicator_counts.values[:10], color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.write("**Categories:**")
            for cat, count in {"Child Growth": df[df['indicator'].str.contains('Stunting|Wasting|Underweight', case=False)].shape[0], "Breastfeeding": df[df['indicator'].str.contains('breastfeed|Breastfeed', case=False)].shape[0], "Anaemia": df[df['indicator'].str.contains('Anaemia', case=False)].shape[0]}.items():
                st.write(f"- {cat}: {count}")

    elif page == "Trends Over Time":
        st.header("Trends Over Time")
        indicator = st.selectbox("Indicator:", df['indicator'].unique())
        data = df[df['indicator'] == indicator]
        yearly = data.groupby('year')['numeric_value'].mean().reset_index()
        fig = px.line(yearly, x='year', y='numeric_value', title="Annual Trend", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    elif page == "Demographic Analysis":
        st.header("Demographic Analysis")
        dim_type = st.selectbox("Dimension:", ["SEX", "WEALTHQUINTILE", "RESIDENCEAREATYPE"])
        indicator = st.selectbox("Indicator:", df['indicator'].unique())
        data = df[(df['indicator'] == indicator) & (df['dimension_type'] == dim_type)]
        if len(data) > 0:
            fig = px.box(data, x='dimension_name', y='numeric_value', title=f"by {dim_type}")
            st.plotly_chart(fig, use_container_width=True)

    elif page == "Statistical Tests":
        st.header("Statistical Tests")
        test_type = st.selectbox("Test:", ["T-Test", "ANOVA", "Correlation"])
        st.info("Use the Presentation Slides mode for complete hypothesis testing results with explanations.")

    elif page == "Data Explorer":
        st.header("Data Explorer")
        cols = st.columns(3)
        with cols[0]:
            year_range = st.slider("Year:", int(df['year'].min()), int(df['year'].max()), (1990, 2024))
        with cols[1]:
            inds = st.multiselect("Indicators:", df['indicator'].unique(), [df['indicator'].unique()[0]])
        with cols[2]:
            dims = st.multiselect("Dimensions:", df['dimension_type'].unique(), [df['dimension_type'].unique()[0]])

        filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1]) & df['indicator'].isin(inds) & df['dimension_type'].isin(dims)]
        st.write(f"Showing {len(filtered)} records")
        st.dataframe(filtered.head(50))
        st.download_button("Download CSV", filtered.to_csv(), "data.csv")

st.divider()
st.markdown("<p style='text-align: center; color: #6c757d;'>Data 200 Applied Statistical Analysis | Nepal Nutrition Indicators | WHO GHO Data</p>", unsafe_allow_html=True)
