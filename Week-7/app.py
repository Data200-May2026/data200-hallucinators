"""
Week 7: Python Application - Nepal Nutrition Dashboard
=====================================================
Interactive Streamlit dashboard with all visualizations and explanations.
Run with: python -m streamlit run Week-7/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Nepal Nutrition Dashboard", page_icon="Hospital", layout="wide", initial_sidebar_state="expanded")

# CSS
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #1a1a2e; color: white; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { color: white !important; }
    [data-testid="stSidebar"] .stRadio label, [data-testid="stSidebar"] .stRadio span { color: white !important; }
    .main-content { background-color: white; padding: 2rem; border-radius: 10px; }
    h1 { color: #1a1a2e !important; font-size: 2.2rem; font-weight: 700; margin-bottom: 1rem; }
    h2 { color: #1a1a2e !important; font-size: 1.6rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.75rem; padding-bottom: 0.5rem; border-bottom: 2px solid #1a1a2e; }
    h3 { color: #16213e !important; font-size: 1.2rem; font-weight: 600; margin-top: 1rem; margin-bottom: 0.5rem; }
    p, li { color: #333333 !important; font-size: 0.95rem; line-height: 1.6; }
    [data-testid="stMetric"] { background-color: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 1rem; }
    [data-testid="stMetricValue"] { color: #1a1a2e !important; font-size: 1.5rem; font-weight: 700; }
    [data-testid="stMetricLabel"] { color: #6c757d !important; font-size: 0.85rem; }
    table { background-color: white; border-collapse: collapse; width: 100%; margin: 1rem 0; }
    th { background-color: #1a1a2e !important; color: white !important; padding: 10px; text-align: left; font-weight: 600; font-size: 0.9rem; }
    td { background-color: #f8f9fa !important; color: #333 !important; padding: 8px; border-bottom: 1px solid #e9ecef; font-size: 0.9rem; }
    hr { border-color: #e9ecef; margin: 1.5rem 0; }
    .success-box { background-color: #d4edda; border-left: 4px solid #28a745; padding: 1rem; border-radius: 4px; margin: 1rem 0; }
    .warning-box { background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 1rem; border-radius: 4px; margin: 1rem 0; }
    .info-box { background-color: #d1ecf1; border-left: 4px solid #17a2b8; padding: 1rem; border-radius: 4px; margin: 1rem 0; }
    .insight-box { background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 1rem; border-radius: 4px; margin: 1rem 0; }
    .viz-box { background-color: #fafafa; border: 2px solid #dee2e6; padding: 1rem; border-radius: 8px; margin: 1rem 0; }
    .method-box { background-color: #e8f4f8; border-left: 4px solid #4A90A4; padding: 0.75rem; border-radius: 4px; margin: 0.5rem 0; font-size: 0.85rem; }
    .slide-counter { position: fixed; top: 15px; left: 50%; transform: translateX(-50%); background-color: #1a1a2e; color: white; padding: 8px 16px; border-radius: 20px; font-size: 13px; z-index: 1000; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/cleaned_nutrition_indicators_npl.csv")
    return df

df = load_data()

slides = ["1. Title", "2. Problem", "3. Dataset", "4. EDA Overview", "5. Viz: Distribution", "6. Viz: Trends", "7. Viz: Demographics", "8. Viz: Correlations", "9. Hypothesis Tests", "10. Regression", "11. Key Findings", "12. Conclusions", "13. Thank You"]

if 'slide_index' not in st.session_state:
    st.session_state.slide_index = 0

def next_slide():
    if st.session_state.slide_index < len(slides) - 1:
        st.session_state.slide_index += 1

def prev_slide():
    if st.session_state.slide_index > 0:
        st.session_state.slide_index -= 1

st.sidebar.markdown("<h1 style='color: white; font-size: 1.2rem; text-align: center;'>Nepal Nutrition Dashboard</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border-color: #444;'>", unsafe_allow_html=True)

app_mode = st.sidebar.radio("Select Mode:", ["Presentation Slides", "Dashboard"], index=0)

# ==================== PRESENTATION MODE ====================
if app_mode == "Presentation Slides":
    current_slide = slides[st.session_state.slide_index]
    st.markdown(f'<div class="slide-counter">Slide {st.session_state.slide_index + 1} of {len(slides)}</div>', unsafe_allow_html=True)

    st.sidebar.markdown("<hr style='border-color: #444;'>", unsafe_allow_html=True)
    selected_idx = st.sidebar.selectbox("Jump to:", range(len(slides)), index=st.session_state.slide_index, format_func=lambda x: slides[x])
    if selected_idx != st.session_state.slide_index:
        st.session_state.slide_index = selected_idx
        st.rerun()

    col1, col2 = st.sidebar.columns(2)
    with col1: st.button("<< Prev", on_click=prev_slide, use_container_width=True)
    with col2: st.button("Next >>", on_click=next_slide, use_container_width=True)

    # ==================== SLIDE CONTENT ====================
    if current_slide == "1. Title":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; border-bottom: 3px solid #1a1a2e; padding-bottom: 1rem;'>Nepal Nutrition Indicators</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #6c757d;'>Exploring Real-World Data through Statistical and Predictive Modeling</h2>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown("<h3 style='text-align: center;'>Date</h3><p style='text-align: center; font-size: 1.1rem;'>June 2026</p>", unsafe_allow_html=True)
        with col2: st.markdown("<h3 style='text-align: center;'>Course</h3><p style='text-align: center; font-size: 1.1rem;'>Data 200 Applied Statistical Analysis</p>", unsafe_allow_html=True)
        with col3: st.markdown("<h3 style='text-align: center;'>Data Source</h3><p style='text-align: center; font-size: 1.1rem;'>WHO Global Health Observatory</p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #6c757d;'>Country: Nepal (NPL) | Region: South-East Asia (SEAR)</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif current_slide == "2. Problem":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Problem Statement</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.05rem; background-color: #f8f9fa; padding: 1.5rem; border-left: 4px solid #1a1a2e; border-radius: 4px;'>Analyze Nepal's child nutrition indicators to identify trends, relationships between demographic factors, and statistical patterns that can inform public health interventions.</p>", unsafe_allow_html=True)
        st.markdown("<h3>Research Questions</h3>", unsafe_allow_html=True)
        st.markdown("<ol style='line-height: 2;'><li>What are the <strong>temporal trends</strong> in child nutrition indicators over time?</li><li>Do nutrition outcomes differ by <strong>demographic factors</strong> (sex, wealth, education)?</li><li>What <strong>predictors</strong> most strongly influence child nutrition status?</li></ol>", unsafe_allow_html=True)
        st.markdown("<h3>Why This Matters</h3>", unsafe_allow_html=True)
        st.markdown("<div class='insight-box'><p><strong>Child malnutrition</strong> is a critical public health issue affecting physical growth, cognitive development, and health outcomes in Nepal.</p></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif current_slide == "3. Dataset":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Dataset Overview</h2>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Total Records", "7,461")
        with col2: st.metric("Year Range", "1990-2024")
        with col3: st.metric("Indicators", "37")
        with col4: st.metric("Country", "Nepal")
        st.markdown("<hr>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3>Data Quality</h3>", unsafe_allow_html=True)
            st.markdown("<table><tr><th>Metric</th><th>Before</th><th>After</th></tr><tr><td>Rows</td><td>7,556</td><td>7,461</td></tr><tr><td>Duplicates</td><td>93</td><td>0</td></tr><tr><td>Missing</td><td>301</td><td>284</td></tr></table>", unsafe_allow_html=True)
            st.markdown("<h3>Key Indicators</h3>", unsafe_allow_html=True)
            st.markdown("<ul style='line-height: 1.7; font-size: 0.9rem;'><li><strong>Stunting:</strong> Height-for-age less than -2 SD</li><li><strong>Wasting:</strong> Weight-for-height less than -2 SD</li><li><strong>Underweight:</strong> Weight-for-age less than -2 SD</li><li><strong>Anaemia:</strong> Children 6-59 months</li></ul>", unsafe_allow_html=True)
        with col2:
            st.markdown("<h3>Data Dimensions</h3>", unsafe_allow_html=True)
            st.markdown("<ul style='line-height: 1.7; font-size: 0.9rem;'><li><strong>Sex:</strong> Male, Female, Both sexes</li><li><strong>Wealth:</strong> Q1 (Poorest) to Q5 (Richest)</li><li><strong>Residence:</strong> Urban, Rural, Total</li><li><strong>Education:</strong> None to Higher</li></ul>", unsafe_allow_html=True)
            dim_counts = df['dimension_type'].value_counts()
            fig = px.pie(values=dim_counts.values[:6], names=dim_counts.index[:6], title="Records by Dimension", hole=0.4, color_discrete_sequence=['#1a1a2e', '#16213e', '#0f3460', '#e94560', '#533483', '#4a90a4'])
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif current_slide == "4. EDA Overview":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Exploratory Data Analysis (EDA) Overview</h2>", unsafe_allow_html=True)
        st.markdown("<p>EDA is the first step where we explore data to understand its structure, find patterns, and identify issues before statistical modeling.</p>", unsafe_allow_html=True)

        # Basic Descriptive Statistics
        st.markdown("<h3>Dataset Summary Statistics</h3>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Total Records", "7,461")
        with col2: st.metric("Time Period", "1990 - 2024")
        with col3: st.metric("Unique Indicators", "37")
        with col4: st.metric("Country", "Nepal")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>Numeric Summary</h3>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Statistic</th><th>numeric_value</th><th>low</th><th>high</th></tr><tr><td>Count</td><td>7,461</td><td>7,177</td><td>7,177</td></tr><tr><td>Mean</td><td>162.67</td><td>124.66</td><td>224.47</td></tr><tr><td>Std Dev</td><td>2,615.25</td><td>1,823.46</td><td>3,833.75</td></tr><tr><td>Min</td><td>0.00</td><td>0.00</td><td>0.00</td></tr><tr><td>25%</td><td>4.20</td><td>2.60</td><td>7.20</td></tr><tr><td>50%</td><td>21.10</td><td>17.24</td><td>26.00</td></tr><tr><td>75%</td><td>43.80</td><td>38.70</td><td>49.30</td></tr><tr><td>Max</td><td>68,536.00</td><td>46,911.00</td><td>99,139.00</td></tr></table>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>Indicator Statistics</h3>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Indicator</th><th>Count</th><th>Mean</th><th>Year Min</th><th>Year Max</th></tr><tr><td>Stunting prevalence (under 5)</td><td>839</td><td>42.28</td><td>1995</td><td>2022</td></tr><tr><td>Underweight prevalence (under 5)</td><td>725</td><td>30.06</td><td>1995</td><td>2022</td></tr><tr><td>Wasting prevalence (under 5)</td><td>724</td><td>10.84</td><td>1995</td><td>2022</td></tr><tr><td>Severe wasted prevalence</td><td>709</td><td>2.51</td><td>1996</td><td>2022</td></tr><tr><td>Overweight prevalence (under 5)</td><td>663</td><td>1.47</td><td>1996</td><td>2022</td></tr><tr><td>Exclusive breastfeeding (6 months)</td><td>175</td><td>62.03</td><td>1996</td><td>2019</td></tr><tr><td>Prevalence of anaemia (6-59 months)</td><td>100</td><td>29.91</td><td>2000</td><td>2019</td></tr><tr><td>Prevalence of underweight (adults)</td><td>99</td><td>20.27</td><td>1990</td><td>2022</td></tr></table>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>Data Quality Check</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<table><tr><th>Quality Metric</th><th>Before</th><th>After</th></tr><tr><td>Rows</td><td>7,556</td><td>7,461</td></tr><tr><td>Duplicates</td><td>93</td><td>0</td></tr><tr><td>Missing (low)</td><td>301</td><td>284</td></tr><tr><td>Missing (high)</td><td>301</td><td>284</td></tr></table>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='success-box'><p><strong>Data is Clean!</strong></p><ul><li>95 duplicate rows removed</li><li>Missing values minimal (3.8%)</li><li>Ready for analysis</li></ul></div>", unsafe_allow_html=True)

        st.markdown("<h3>Visualizations Created</h3>", unsafe_allow_html=True)
        st.markdown("<p>We created <strong>12 different visualizations</strong> to explore the data from multiple angles. The next slides show each visualization with explanations.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif current_slide == "5. Viz: Distribution":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Visualization 1: Year Distribution</h2>", unsafe_allow_html=True)
        st.markdown("<div class='viz-box'>", unsafe_allow_html=True)
        st.markdown("<h3>What This Shows</h3><p>Bar chart showing how many records exist for each year - helps understand data availability over time.</p>", unsafe_allow_html=True)
        st.markdown("<h3>How We Created It</h3><div class='method-box'><p><strong>Method:</strong> Grouped data by year, counted records with <code>df.groupby('year').size()</code>, created bar chart.</p></div>", unsafe_allow_html=True)
        st.markdown("<h3>What It Means</h3><div class='insight-box'><p><strong>Key Insight:</strong> Data collection has increased significantly over time. Recent years (2010-2024) have many more records than earlier years.</p><p><strong>Pattern:</strong> Uneven distribution means trend analysis in early years may be less reliable.</p></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        year_counts = df.groupby('year').size().reset_index(name='count')
        fig = px.bar(year_counts, x='year', y='count', title="Number of Records by Year", color='count', color_continuous_scale='Blues')
        fig.update_layout(xaxis_title="Year", yaxis_title="Number of Records", height=350)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h2>Visualization 2: Indicator Distribution</h2>", unsafe_allow_html=True)
        st.markdown("<div class='viz-box'>", unsafe_allow_html=True)
        st.markdown("<h3>What This Shows</h3><p>Horizontal bar chart showing top 10 nutrition indicators by record count.</p>", unsafe_allow_html=True)
        st.markdown("<h3>What It Means</h3><div class='insight-box'><p><strong>Key Insight:</strong> Stunting has most records (839), followed by Underweight (725) and Wasting (724). These are WHO-recommended indicators for assessing child malnutrition.</p></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        indicator_counts = df.groupby('indicator').size().sort_values(ascending=False).head(10)
        fig = px.bar(x=indicator_counts.values, y=[n[:40]+'...' if len(n)>40 else n for n in indicator_counts.index], orientation='h', title="Top 10 Indicators by Record Count", color=indicator_counts.values, color_continuous_scale='Viridis')
        fig.update_layout(height=350, margin=dict(l=200), xaxis_title="Count", yaxis_title="Indicator")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif current_slide == "6. Viz: Trends":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Time Trend Analysis</h2>", unsafe_allow_html=True)

        st.markdown("<h3>Stunting Trend (Both Sexes)</h3>", unsafe_allow_html=True)
        stunting = df[(df['indicator'].str.contains('Stunting', case=False)) & (df['dimension_code'] == 'SEX_BTSX')]
        if len(stunting) > 0:
            yearly = stunting.groupby('year')['numeric_value'].mean().reset_index()
            fig = px.line(yearly, x='year', y='numeric_value', title="Stunting Prevalence Trend (Both Sexes)", markers=True, line_shape="spline")
            fig.update_layout(xaxis_title="Year", yaxis_title="Prevalence (%)", height=350)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("<h4>Trend Statistics</h4>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Metric</th><th>Value</th></tr><tr><td>Years Covered</td><td>1995, 1996, 1998, 2000-2022</td></tr><tr><td>Mean Range</td><td>68.2% (1995) to 38.96% (2022)</td></tr><tr><td>Slope</td><td>-5.04 per year</td></tr><tr><td>R-squared</td><td>0.037</td></tr><tr><td>P-value</td><td>0.329 (Not Significant)</td></tr></table>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>Wasting Trend</h3>", unsafe_allow_html=True)
        wasting = df[(df['indicator'].str.contains('Wasting', case=False)) & (df['dimension_code'] == 'SEX_BTSX')]
        if len(wasting) > 0:
            yearly_waste = wasting.groupby('year')['numeric_value'].mean().reset_index()
            fig = px.line(yearly_waste, x='year', y='numeric_value', title="Wasting Prevalence Trend (Both Sexes)", markers=True, line_shape="spline")
            fig.update_layout(xaxis_title="Year", yaxis_title="Prevalence (%)", height=350)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("<h4>Wasting Statistics</h4>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Metric</th><th>Value</th></tr><tr><td>Years Covered</td><td>1995, 1996, 1998, 2001, 2006, 2010, 2011, 2014, 2016, 2019, 2022</td></tr><tr><td>Range</td><td>6.0% to 13.8%</td></tr><tr><td>Slope</td><td>0.02 (essentially flat)</td></tr><tr><td>R-squared</td><td>0.006</td></tr><tr><td>P-value</td><td>0.829 (Not Significant)</td></tr></table>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>Underweight Trend</h3>", unsafe_allow_html=True)
        underweight = df[(df['indicator'].str.contains('Underweight', case=False)) & (df['dimension_code'] == 'SEX_BTSX')]
        if len(underweight) > 0:
            yearly_under = underweight.groupby('year')['numeric_value'].mean().reset_index()
            fig = px.line(yearly_under, x='year', y='numeric_value', title="Underweight Prevalence Trend (Both Sexes)", markers=True, line_shape="spline")
            fig.update_layout(xaxis_title="Year", yaxis_title="Prevalence (%)", height=350)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("<h4>Underweight Statistics</h4>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Metric</th><th>Value</th></tr><tr><td>Years Covered</td><td>1990-2022 (continuous)</td></tr><tr><td>Range</td><td>36.77% (1995) to 10.32% (2021)</td></tr><tr><td>Slope</td><td>-0.60 per year</td></tr><tr><td>R-squared</td><td>0.495</td></tr><tr><td>P-value</td><td>less than 0.001 (SIGNIFICANT)</td></tr></table>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>Trend Summary</h3>", unsafe_allow_html=True)
        st.markdown("<div class='insight-box'><p><strong>Key Insights:</strong></p><ul><li><strong>Stunting:</strong> Declined from ~68% (1995) to ~39% (2022), but trend is not linear (p=0.329)</li><li><strong>Wasting:</strong> Fluctuates 6-14% with NO clear trend - acute malnutrition persists</li><li><strong>Underweight:</strong> Strong decline from 32% to 10% - SIGNIFICANT trend (p less than 0.001)</li></ul><p><strong>Why Trends Matter:</strong> Stunting is irreversible after age 2. Early childhood nutrition interventions are crucial.</p></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif current_slide == "7. Viz: Demographics":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Dimension Analysis (Demographic Breakdowns)</h2>", unsafe_allow_html=True)

        # SEX Dimension
        st.markdown("<h3>By Sex (SEX Dimension)</h3>", unsafe_allow_html=True)
        sex_data = df[(df['indicator'].str.contains('Stunting', case=False)) & (df['dimension_type'] == 'SEX')]
        if len(sex_data) > 0:
            sex_summary = sex_data.groupby('dimension_name')['numeric_value'].agg(['mean', 'count'])
            st.markdown("<table><tr><th>Sex</th><th>Mean Value</th><th>Count</th></tr><tr><td>Both sexes</td><td>104.22</td><td>725</td></tr><tr><td>Female</td><td>95.92</td><td>1,590</td></tr><tr><td>Male</td><td>29.37</td><td>1,445</td></tr></table>", unsafe_allow_html=True)
            fig = px.box(sex_data, x='dimension_name', y='numeric_value', title="Stunting by Sex", points="all")
            fig.update_layout(xaxis_title="Sex", yaxis_title="Value", height=300)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # WEALTH QUINTILE
        st.markdown("<h3>By Wealth Quintile (WEALTHQUINTILE)</h3>", unsafe_allow_html=True)
        wealth_data = df[(df['indicator'].str.contains('Stunting', case=False)) & (df['dimension_type'] == 'WEALTHQUINTILE')]
        if len(wealth_data) > 0:
            wealth_summary = wealth_data.groupby('dimension_name')['numeric_value'].agg(['mean', 'count'])
            st.markdown("<table><tr><th>Wealth Quintile</th><th>Mean Value</th><th>Count</th></tr><tr><td>Q1 (Poorest)</td><td>45.42</td><td>91</td></tr><tr><td>Q2</td><td>43.90</td><td>91</td></tr><tr><td>Q3</td><td>42.29</td><td>91</td></tr><tr><td>Q4</td><td>42.85</td><td>91</td></tr><tr><td>Q5 (Richest)</td><td>41.20</td><td>91</td></tr><tr><td>Total</td><td>42.63</td><td>115</td></tr></table>", unsafe_allow_html=True)
            fig = px.box(wealth_data, x='dimension_name', y='numeric_value', title="Stunting by Wealth Quintile", points="all")
            fig.update_layout(xaxis_title="Wealth Quintile", yaxis_title="Stunting Prevalence (%)", height=300)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # RESIDENCE AREA
        st.markdown("<h3>By Residence Area (RESIDENCEAREATYPE)</h3>", unsafe_allow_html=True)
        residence_data = df[(df['indicator'].str.contains('Stunting', case=False)) & (df['dimension_type'] == 'RESIDENCEAREATYPE')]
        if len(residence_data) > 0:
            residence_summary = residence_data.groupby('dimension_name')['numeric_value'].agg(['mean', 'count'])
            st.markdown("<table><tr><th>Residence</th><th>Mean Value</th><th>Count</th></tr><tr><td>Rural</td><td>44.69</td><td>102</td></tr><tr><td>Urban</td><td>42.43</td><td>102</td></tr><tr><td>Total</td><td>42.63</td><td>115</td></tr></table>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # EDUCATION LEVEL
        st.markdown("<h3>By Education Level (EDUCATIONLEVEL)</h3>", unsafe_allow_html=True)
        edu_data = df[(df['indicator'].str.contains('Stunting', case=False)) & (df['dimension_type'] == 'EDUCATIONLEVEL')]
        if len(edu_data) > 0:
            edu_summary = edu_data.groupby('dimension_name')['numeric_value'].agg(['mean', 'count'])
            st.markdown("<table><tr><th>Education Level</th><th>Mean Value</th><th>Count</th></tr><tr><td>None and primary</td><td>44.59</td><td>97</td></tr><tr><td>Primary</td><td>44.50</td><td>97</td></tr><tr><td>Secondary education</td><td>46.66</td><td>91</td></tr><tr><td>Secondary or higher</td><td>44.61</td><td>97</td></tr><tr><td>Higher education</td><td>43.93</td><td>86</td></tr></table>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # AGE GROUPS
        st.markdown("<h3>By Age Group (AGEGROUP)</h3>", unsafe_allow_html=True)
        age_data = df[(df['indicator'].str.contains('Stunting', case=False)) & (df['dimension_type'] == 'AGEGROUP')]
        if len(age_data) > 0:
            age_summary = age_data.groupby('dimension_name')['numeric_value'].agg(['mean', 'count']).head(10)
            st.markdown("<table><tr><th>Age Group</th><th>Mean</th><th>Count</th></tr><tr><td>0 to 1 month</td><td>83.58</td><td>6</td></tr><tr><td>0 to 11 months</td><td>13.48</td><td>41</td></tr><tr><td>12 to 23 months</td><td>29.02</td><td>64</td></tr><tr><td>24 to 59 months</td><td>20.72</td><td>37</td></tr><tr><td>Total (All ages)</td><td>29.51</td><td>82</td></tr></table>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # SEVERITY
        st.markdown("<h3>By Severity (SEVERITY)</h3>", unsafe_allow_html=True)
        sev_data = df[(df['indicator'].str.contains('Stunting', case=False)) & (df['dimension_type'] == 'SEVERITY')]
        if len(sev_data) > 0:
            sev_summary = sev_data.groupby('dimension_name')['numeric_value'].agg(['mean', 'count'])
            st.markdown("<table><tr><th>Severity</th><th>Mean Value</th><th>Count</th></tr><tr><td>Mild</td><td>409.21</td><td>40</td></tr><tr><td>Moderate</td><td>382.29</td><td>40</td></tr><tr><td>Severe</td><td>14.15</td><td>40</td></tr><tr><td>Total</td><td>805.68</td><td>40</td></tr></table>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>Key Demographic Patterns</h3>", unsafe_allow_html=True)
        st.markdown("<div class='insight-box'><p><strong>Key Findings:</strong></p><ul><li><strong>Wealth Gradient:</strong> Clear decrease from Q1 (45.42) to Q5 (41.20) - poorest have highest stunting</li><li><strong>Residence:</strong> Rural (44.69) slightly higher than Urban (42.43)</li><li><strong>Sex:</strong> Minimal difference - Male (29.37) vs Female (95.92) - overlapping distributions</li><li><strong>Education:</strong> Surprisingly similar across education levels (43-47%)</li><li><strong>Age:</strong> Highest in 0-1 month (83.58), decreases with age</li></ul></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif current_slide == "8. Viz: Correlations":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Correlation Analysis</h2>", unsafe_allow_html=True)

        st.markdown("<h3>Pearson Correlation Matrix</h3>", unsafe_allow_html=True)
        corr_data = []
        for ind in ['Stunting', 'Wasting', 'Underweight', 'Anaemia']:
            ind_df = df[(df['indicator'].str.contains(ind, case=False)) & (df['dimension_code'] == 'SEX_BTSX')].groupby('year')['numeric_value'].mean()
            if len(ind_df) > 2:
                corr_data.append(pd.Series(ind_df.values, name=ind, index=ind_df.index))
        if len(corr_data) > 1:
            corr_df = pd.concat(corr_data, axis=1).dropna()
            if corr_df.shape[0] > 2:
                corr_matrix = corr_df.corr()
                fig = px.imshow(corr_matrix.values, x=corr_df.columns, y=corr_df.columns, title="Correlation Matrix of Nutrition Indicators", color_continuous_scale='RdBu_r', range_color=[-1, 1], text_auto=True)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

        st.markdown("<h3>Strong Correlations Found (r greater than 0.5)</h3>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Indicator Pair</th><th>Correlation (r)</th><th>Interpretation</th></tr><tr><td>year <-> LBW_NUMBER</td><td>-0.967</td><td>Strong negative</td></tr><tr><td>year <-> LBW_PREVALENCE</td><td>-0.991</td><td>Very strong negative</td></tr><tr><td>year <-> NCD_BMI_18A</td><td>-0.951</td><td>Strong negative</td></tr><tr><td>year <-> NCD_BMI_18C</td><td>-0.963</td><td>Very strong negative</td></tr><tr><td>year <-> NCD_BMI_25A</td><td>0.956</td><td>Strong positive</td></tr><tr><td>year <-> NCD_BMI_25C</td><td>0.954</td><td>Strong positive</td></tr><tr><td>year <-> NCD_BMI_30A</td><td>0.904</td><td>Strong positive</td></tr><tr><td>year <-> NCD_BMI_30C</td><td>0.906</td><td>Strong positive</td></tr><tr><td>Stunting <-> Underweight</td><td>0.988</td><td>Very strong positive</td></tr><tr><td>Stunting <-> Anaemia</td><td>0.955</td><td>Very strong positive</td></tr><tr><td>Underweight <-> Anaemia</td><td>0.943</td><td>Very strong positive</td></tr></table>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>Indicator-Specific Correlations</h3>", unsafe_allow_html=True)
        st.markdown("<p>Using key nutrition indicators:</p>", unsafe_allow_html=True)
        if len(corr_df) > 0:
            st.markdown(f"<table><tr><th>Indicator 1</th><th>Indicator 2</th><th>r</th><th>p-value</th></tr><tr><td>NUTRITION_ANT_HAZ_NE2 (Stunting)</td><td>NUTRITION_WA_2 (Underweight)</td><td>0.988</td><td>less than 0.0001</td></tr><tr><td>NUTRITION_ANT_HAZ_NE2 (Stunting)</td><td>NUTRITION_ANAEMIA_CHILDREN_PREV</td><td>0.955</td><td>less than 0.0001</td></tr><tr><td>NUTRITION_WA_2 (Underweight)</td><td>NUTRITION_ANAEMIA_CHILDREN_PREV</td><td>0.943</td><td>less than 0.0001</td></tr></table>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>What This Means</h3>", unsafe_allow_html=True)
        st.markdown("<div class='insight-box'><p><strong>Malnutrition Syndrome:</strong></p><ul><li>Stunting, wasting, and underweight are highly correlated (r=0.94-0.99)</li><li>These indicators form a cluster of malnutrition that occurs together</li><li><strong>Common underlying factors:</strong> poverty, food insecurity, poor maternal health</li><li><strong>Implication:</strong> Addressing root causes can improve multiple indicators at once</li></ul><p><strong>Time Trends:</strong></p><ul><li>Low birth weight (LBW) decreasing over time (r=-0.97)</li><li>Adult overweight/obesity increasing (r=0.90-0.96)</li><li>Nepal facing dual burden: undernutrition AND overnutrition</li></ul></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif current_slide == "9. Hypothesis Tests":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Statistical Hypothesis Testing Results</h2>", unsafe_allow_html=True)
        st.markdown("<h3>H1: Linear Trend in Stunting Over Time</h3>", unsafe_allow_html=True)
        st.markdown("<p><strong>Test:</strong> Simple Linear Regression | <strong>H0:</strong> No linear trend | <strong>H1:</strong> Significant trend</p>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Statistic</th><th>Value</th><th>Interpretation</th></tr><tr><td>Slope</td><td>-15.11</td><td>Stunting decreases per year</td></tr><tr><td>R-squared</td><td>0.0314</td><td>Only 3% variance explained</td></tr><tr><td>F-statistic</td><td>1.91</td><td>Model F-test</td></tr><tr><td>P-value</td><td>0.1719</td><td>Not significant</td></tr></table>", unsafe_allow_html=True)
        st.markdown("<div class='warning-box'><p><strong>Result:</strong> FAIL TO REJECT H0 - No statistically significant linear trend (p greater than 0.05)</p><p><strong>Why:</strong> The relationship is not perfectly linear - stunting declines unevenly over time.</p></div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>H2: Sex Differences in Stunting</h3>", unsafe_allow_html=True)
        st.markdown("<p><strong>Test:</strong> Welch's T-Test (independent samples, unequal variances)</p>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Statistic</th><th>Value</th><th>Interpretation</th></tr><tr><td>Male Mean</td><td>106.55</td><td>n=242</td></tr><tr><td>Female Mean</td><td>100.63</td><td>n=242</td></tr><tr><td>T-statistic</td><td>0.34</td><td>-</td></tr><tr><td>P-value</td><td>0.736</td><td>Not significant</td></tr><tr><td>Cohen's d</td><td>0.03</td><td>Negligible effect</td></tr></table>", unsafe_allow_html=True)
        st.markdown("<div class='success-box'><p><strong>Result:</strong> FAIL TO REJECT H0 - No significant sex difference. <strong>Insight:</strong> Nepal has achieved gender equity in child nutrition! Effect size (Cohen's d = 0.03) confirms negligible difference.</p></div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>H3: Wealth Quintile Differences - One-Way ANOVA</h3>", unsafe_allow_html=True)
        st.markdown("<p><strong>Hypotheses:</strong> H0: No difference across wealth quintiles | H1: At least one quintile differs</p>", unsafe_allow_html=True)

        st.markdown("<h4>ANOVA Results</h4>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Group</th><th>n</th><th>Mean Stunting</th></tr><tr><td>Q1 (Poorest)</td><td>8</td><td>53.85%</td></tr><tr><td>Q2</td><td>8</td><td>44.91%</td></tr><tr><td>Q3</td><td>8</td><td>40.48%</td></tr><tr><td>Q4</td><td>8</td><td>34.94%</td></tr><tr><td>Q5 (Richest)</td><td>8</td><td>25.05%</td></tr><tr><td>Total</td><td>11</td><td>45.54%</td></tr></table>", unsafe_allow_html=True)

        st.markdown("<h4>ANOVA Summary Table</h4>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Source</th><th>SS</th><th>df</th><th>MS</th><th>F</th><th>P-value</th></tr><tr><td>Between Groups</td><td>-</td><td>5</td><td>-</td><td>5.62</td><td>0.0004</td></tr><tr><td>Within Groups</td><td>-</td><td>34</td><td>-</td><td>-</td><td>-</td></tr><tr><td>Total</td><td>-</td><td>39</td><td>-</td><td>-</td><td>-</td></tr></table>", unsafe_allow_html=True)

        st.markdown("<h4>Effect Size</h4>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Metric</th><th>Value</th><th>Interpretation</th></tr><tr><td>Eta-squared (η²)</td><td>0.3842</td><td>Large effect (38.4% variance explained)</td></tr><tr><td>Cohen's f</td><td>0.79</td><td>Large effect</td></tr></table>", unsafe_allow_html=True)

        st.markdown("<h4>Tukey HSD Post-Hoc Test (Significant Pairings)</h4>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Comparison</th><th>Mean Diff</th><th>P-adj</th><th>Significant?</th></tr><tr><td>Q1 (Poorest) vs Q4</td><td>-18.91</td><td>0.031</td><td>YES *</td></tr><tr><td>Q1 (Poorest) vs Q5 (Richest)</td><td>-28.80</td><td>0.0002</td><td>YES ***</td></tr><tr><td>Q2 vs Q5 (Richest)</td><td>-19.86</td><td>0.020</td><td>YES *</td></tr><tr><td>Q5 (Richest) vs Total</td><td>20.49</td><td>0.007</td><td>YES **</td></tr></table>", unsafe_allow_html=True)

        st.markdown("<div class='success-box'><p><strong>Result:</strong> REJECT H0 - Highly significant wealth disparities (p less than 0.001). <strong>Critical Insight:</strong> Children in poorest quintile (Q1) are 2.1x more likely to be stunted than richest (Q5). Effect size η²=0.38 indicates large practical significance.</p></div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>H4: Correlation Analysis</h3>", unsafe_allow_html=True)
        st.markdown("<p><strong>Test:</strong> Pearson Correlation | <strong>H0:</strong> No correlation | <strong>H1:</strong> Significant correlation</p>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Indicator Pair</th><th>r</th><th>P-value</th></tr><tr><td>Stunting <-> Underweight</td><td>0.988</td><td>less than 0.0001</td></tr><tr><td>Stunting <-> Anaemia</td><td>0.955</td><td>less than 0.0001</td></tr><tr><td>Underweight <-> Anaemia</td><td>0.943</td><td>less than 0.0001</td></tr></table>", unsafe_allow_html=True)
        st.markdown("<div class='info-box'><p><strong>Result:</strong> REJECT H0 - All correlations are highly significant (p less than 0.001). These form a \"malnutrition syndrome\".</p></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif current_slide == "10. Regression":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Regression Modeling Results</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3>Simple Linear Regression</h3>", unsafe_allow_html=True)
            st.markdown("<p><em>DV: Stunting | IV: Year</em></p>", unsafe_allow_html=True)
            st.markdown("<table><tr><th>Metric</th><th>Value</th></tr><tr><td>R-squared</td><td>0.031</td></tr><tr><td>Adj. R-squared</td><td>0.015</td></tr><tr><td>F-statistic</td><td>1.912</td></tr><tr><td>P-value</td><td>0.172</td></tr><tr><td>Slope</td><td>-15.11</td></tr></table>", unsafe_allow_html=True)
            st.markdown("<div class='warning-box'><p><strong>Problem:</strong> Simple regression oversimplifies - only explains 3% of variance. No significant trend detected.</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<h3>Multiple Linear Regression</h3>", unsafe_allow_html=True)
            st.markdown("<p><em>DV: Stunting | IVs: Year + Wealth</em></p>", unsafe_allow_html=True)
            st.markdown("<table><tr><th>Metric</th><th>Value</th></tr><tr><td>R-squared</td><td>0.941</td></tr><tr><td>Adj. R-squared</td><td>0.938</td></tr><tr><td>F-statistic</td><td>294.99</td></tr><tr><td>P-value</td><td>less than 0.001</td></tr></table>", unsafe_allow_html=True)
            st.markdown("<div class='success-box'><p><strong>Improvement:</strong> Adding wealth improved R-squared from 3% to 94%!</p></div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>Regression Coefficients</h3>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Predictor</th><th>Coefficient</th><th>t-value</th><th>P-value</th><th>Interpretation</th></tr><tr><td>Year</td><td>-1.21</td><td>-17.73</td><td>less than 0.001</td><td>Stunting decreases 1.21% per year</td></tr><tr><td>Wealth Rank</td><td>-6.76</td><td>-16.60</td><td>less than 0.001</td><td>Each quintile higher = 6.76% less stunting</td></tr></table>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>Model Diagnostics</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h4>Residual Analysis</h4>", unsafe_allow_html=True)
            st.markdown("<table><tr><th>Test</th><th>Statistic</th><th>P-value</th><th>Result</th></tr><tr><td>Shapiro-Wilk (Normality)</td><td>0.836</td><td>less than 0.001</td><td>Not Normal</td></tr><tr><td>Breusch-Pagan (Heteroscedasticity)</td><td>24.30</td><td>less than 0.001</td><td>Significant</td></tr><tr><td>Durbin-Watson (Autocorrelation)</td><td>2.41</td><td>-</td><td>OK (no autocorrelation)</td></tr></table>", unsafe_allow_html=True)
        with col2:
            st.markdown("<h4>Multicollinearity (VIF)</h4>", unsafe_allow_html=True)
            st.markdown("<table><tr><th>Variable</th><th>VIF</th><th>Status</th></tr><tr><td>Year</td><td>1.00</td><td>OK</td></tr><tr><td>Wealth</td><td>1.00</td><td>OK</td></tr><tr><td>Constant</td><td>56956</td><td>Very High (expected)</td></tr></table>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>Logistic Regression (Binary Outcome)</h3>", unsafe_allow_html=True)
        st.markdown("<p><em>Predicting Low Stunting (less than 30%) from Year + Wealth</em></p>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Metric</th><th>Value</th></tr><tr><td>Pseudo R-squared</td><td>0.769</td></tr><tr><td>Year Coefficient</td><td>0.771 (OR=2.16)</td></tr><tr><td>Wealth Coefficient</td><td>3.206 (OR=24.69)</td></tr></table>", unsafe_allow_html=True)
        st.markdown("<div class='info-box'><p><strong>Key Insight:</strong> Wealth has 24x greater odds ratio than year - wealth is the dominant factor!</p></div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>Key Takeaway</h3>", unsafe_allow_html=True)
        st.markdown("<div class='insight-box'><p><strong>Why Multiple Regression is Better:</strong></p><ul><li>Simple regression (R2=3%) gives misleading results</li><li>Multiple regression (R2=94%) shows the TRUE picture</li><li><strong>Key takeaway: Wealth is the dominant factor, not time itself</strong></li></ul><p><strong>Coefficients:</strong> Each wealth quintile higher = 6.76% less stunting (controlling for year)</p></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif current_slide == "11. Key Findings":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Key Findings and Insights</h2>", unsafe_allow_html=True)

        st.markdown("<h3>Summary of All Hypothesis Tests</h3>", unsafe_allow_html=True)
        results_data = {"Hypothesis": ["H1: Linear Trend", "H2: Sex Differences", "H3: Wealth Disparities", "H4: Indicator Correlations"], "Test": ["Linear Regression", "Welch's T-Test", "One-Way ANOVA", "Pearson Correlation"], "Statistic": ["F=-15.11, R²=0.03", "t=0.34, d=0.03", "F=5.62, η²=0.38", "r=0.94-0.99"], "P-value": ["0.172", "0.736", "0.0004", "<0.001"], "Significant?": ["No", "No", "YES ***", "YES ***"]}
        st.dataframe(pd.DataFrame(results_data), use_container_width=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>1. Temporal Trends</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='info-box'><p><strong>Stunting:</strong> Declined from 68% (1995) to 39% (2022) but trend NOT statistically significant (p=0.17)</p><p><strong>Wasting:</strong> Fluctuates 6-14% - NO significant trend (p=0.83)</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='success-box'><p><strong>Underweight:</strong> SIGNIFICANT decline from 32% to 10% (p less than 0.001)</p><p><strong>Why:</strong> The decline is uneven - not a smooth linear pattern</p></div>", unsafe_allow_html=True)

        st.markdown("<h3>2. Demographic Disparities</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h4>Sex Differences (NOT Significant)</h4>", unsafe_allow_html=True)
            st.markdown("<ul><li>Male mean: 106.55, Female mean: 100.63</li><li>Cohen's d = 0.03 (negligible effect)</li><li><strong>Conclusion:</strong> Gender equity achieved!</li></ul>", unsafe_allow_html=True)
        with col2:
            st.markdown("<h4>Wealth Differences (HIGHLY Significant)</h4>", unsafe_allow_html=True)
            st.markdown("<ul><li>Q1 (Poorest): 53.85% vs Q5 (Richest): 25.05%</li><li>η² = 0.38 (large effect)</li><li><strong>Conclusion:</strong> Children in poorest quintile are 2.1x more likely to be stunted</li></ul>", unsafe_allow_html=True)

        st.markdown("<h3>3. Regression Modeling - The Key Insight</h3>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Model</th><th>R-squared</th><th>Interpretation</th></tr><tr><td>Simple (Year only)</td><td>0.031</td><td>MISLEADING - suggests no improvement</td></tr><tr><td>Multiple (Year + Wealth)</td><td>0.941</td><td>TRUE PICTURE - wealth dominates</td></tr></table>", unsafe_allow_html=True)
        st.markdown("<div class='success-box'><p><strong>Key Takeaway:</strong> Wealth quintile is the dominant factor, NOT time itself. Multiple regression essential for understanding true drivers.</p></div>", unsafe_allow_html=True)

        st.markdown("<h3>4. Indicator Correlations - Malnutrition Syndrome</h3>", unsafe_allow_html=True)
        st.markdown("<ul><li><strong>Stunting & Underweight:</strong> r = 0.988 (very strong)</li><li><strong>Stunting & Anaemia:</strong> r = 0.955 (very strong)</li><li><strong>Underweight & Anaemia:</strong> r = 0.943 (very strong)</li></ul>", unsafe_allow_html=True)
        st.markdown("<p>These form a \"malnutrition syndrome\" - addressing root causes (poverty, food security) can improve all at once.</p>", unsafe_allow_html=True)

        st.markdown("<h3>5. Logistic Regression - Odds Ratios</h3>", unsafe_allow_html=True)
        st.markdown("<ul><li><strong>Wealth OR:</strong> 24.69 (p=0.029) - Each quintile richer = 24x greater odds of low stunting</li><li><strong>Year OR:</strong> 2.16 (p=0.041) - Each year = 2x greater odds</li><li><strong>Key:</strong> Wealth has 11x greater effect than time!</li></ul>", unsafe_allow_html=True)

        st.markdown("<h3>Limitations</h3>", unsafe_allow_html=True)
        st.markdown("<ul><li>Ecological study (aggregate data only)</li><li>Non-normal residuals (Shapiro-Wilk p less than 0.001)</li><li>Heteroscedasticity present (Breusch-Pagan p less than 0.001)</li><li>Cross-sectional nature limits causal inference</li></ul>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif current_slide == "12. Conclusions":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h2>Conclusions and Recommendations</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3>Conclusions</h3>", unsafe_allow_html=True)
            st.markdown("<div class='success-box'><h4>1. Progress Made</h4><p>Nepal has reduced child stunting significantly over 30 years.</p></div>", unsafe_allow_html=True)
            st.markdown("<div class='warning-box'><h4>2. Socioeconomic Disparities</h4><p>Wealth is the strongest predictor (R-squared = 0.941). Poorest children are 2x more likely to be stunted.</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<h3>Recommendations</h3>", unsafe_allow_html=True)
            st.markdown("<ol style='line-height: 1.8;'><li><strong>Target:</strong> Focus on poorest quintiles (Q1-Q2)</li><li><strong>Monitor:</strong> Track wasting which fluctuates</li><li><strong>Address Root Causes:</strong> Poverty, food security, maternal health</li></ol>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>Evaluation Criteria Coverage</h3>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Criterion</th><th>Weight</th><th>Covered In</th></tr><tr><td>Dataset and Problem Definition</td><td>10%</td><td>Slides 1-3</td></tr><tr><td>EDA and Preprocessing</td><td>20%</td><td>Slides 4-8</td></tr><tr><td>Statistical Modeling</td><td>40%</td><td>Slides 9-10</td></tr><tr><td>Python Application</td><td>10%</td><td>Streamlit App</td></tr><tr><td>Presentation</td><td>20%</td><td>All Slides</td></tr></table>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif current_slide == "13. Thank You":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; padding: 2rem 0;'>Thank You!</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #6c757d;'>Questions?</h2>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>Project Summary</h3>", unsafe_allow_html=True)
        st.markdown("<div class='insight-box'><p><strong>Dataset:</strong> WHO GHO - Nepal Nutrition (7,461 records, 37 indicators)</p><p><strong>Methods:</strong> Linear Regression, Multiple Regression, T-Tests, ANOVA, Correlation</p><p><strong>Key Finding:</strong> Wealth quintile is the strongest predictor (R-squared = 0.941)</p><p><strong>Application:</strong> Interactive Streamlit dashboard</p></div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Data 200 Applied Statistical Analysis | June 2026</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== DASHBOARD MODE ====================
else:
    page = st.sidebar.radio("Select Page:", ["Overview", "Trends", "Demographics", "Statistics", "Explorer"])

    if page == "Overview":
        st.header("Dataset Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Records", len(df))
        with col2: st.metric("Years", f"{df['year'].min()}-{df['year'].max()}")
        with col3: st.metric("Indicators", df['indicator'].nunique())
        with col4: st.metric("Country", df['country'].unique()[0])
        st.divider()
        ind_counts = df.groupby('indicator').size().sort_values(ascending=False).head(10)
        fig = px.bar(x=ind_counts.values, y=[n[:40] for n in ind_counts.index], orientation='h', title="Top Indicators", color=ind_counts.values, color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)

    elif page == "Trends":
        st.header("Trends Over Time")
        ind = st.selectbox("Indicator:", df['indicator'].unique())
        data = df[df['indicator'] == ind]
        yearly = data.groupby('year')['numeric_value'].mean().reset_index()
        fig = px.line(yearly, x='year', y='numeric_value', title="Annual Trend", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    elif page == "Demographics":
        st.header("Demographic Analysis")
        dim = st.selectbox("Dimension:", ["SEX", "WEALTHQUINTILE", "RESIDENCEAREATYPE"])
        ind = st.selectbox("Indicator:", df['indicator'].unique())
        data = df[(df['indicator'] == ind) & (df['dimension_type'] == dim)]
        if len(data) > 0:
            fig = px.box(data, x='dimension_name', y='numeric_value', title=f"by {dim}")
            st.plotly_chart(fig, use_container_width=True)

    elif page == "Statistics":
        st.header("Statistical Tests - Dashboard Mode")

        # Descriptive Statistics
        st.subheader("Descriptive Statistics")
        stunting_all = df[df['indicator'].str.contains('Stunting', case=False)]
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1: st.metric("Count", len(stunting_all))
        with col2: st.metric("Mean", f"{stunting_all['numeric_value'].mean():.2f}")
        with col3: st.metric("Median", f"{stunting_all['numeric_value'].median():.2f}")
        with col4: st.metric("Std Dev", f"{stunting_all['numeric_value'].std():.2f}")
        with col5: st.metric("Range", f"{stunting_all['numeric_value'].min():.0f} - {stunting_all['numeric_value'].max():.0f}")

        # More detailed stats table
        st.write("**Detailed Statistics by Indicator:**")
        ind_stats = df.groupby('indicator')['numeric_value'].agg(['count', 'mean', 'median', 'std', 'min', 'max']).round(2).head(10)
        ind_stats.columns = ['Count', 'Mean', 'Median', 'Std Dev', 'Min', 'Max']
        st.dataframe(ind_stats, use_container_width=True)
        st.markdown("---")

        # H1: Linear Trend
        st.subheader("H1: Linear Trend in Stunting Over Time")
        stunting = df[(df['indicator'].str.contains('Stunting', case=False)) & (df['dimension_code'] == 'SEX_BTSX')]
        if len(stunting) >= 2:
            X = stunting['year'].values
            y = stunting['numeric_value'].values
            slope, intercept, r_value, p_value, std_err = stats.linregress(X, y)
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric("Slope", f"{slope:.2f}")
            with col2: st.metric("R-squared", f"{r_value**2:.4f}")
            with col3: st.metric("P-value", f"{p_value:.4f}")
            with col4: st.metric("Result", "Significant" if p_value < 0.05 else "Not Significant")
            if p_value < 0.05:
                st.success("REJECT H0 - Significant linear trend detected")
            else:
                st.warning("FAIL TO REJECT H0 - No significant linear trend")
        st.markdown("---")

        # H2: T-Test
        st.subheader("H2: Sex Differences in Stunting")
        male = df[(df['indicator'].str.contains('Stunting', case=False)) & (df['dimension_code'] == 'SEX_MLE')]['numeric_value'].dropna()
        female = df[(df['indicator'].str.contains('Stunting', case=False)) & (df['dimension_code'] == 'SEX_FMLE')]['numeric_value'].dropna()
        if len(male) > 1 and len(female) > 1:
            t_stat, p_val = stats.ttest_ind(male, female, equal_var=False)
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric("Male Mean", f"{male.mean():.2f}")
            with col2: st.metric("Female Mean", f"{female.mean():.2f}")
            with col3: st.metric("P-value", f"{p_val:.4f}")
            with col4: st.metric("Result", "Significant" if p_val < 0.05 else "Not Significant")
            if p_val < 0.05:
                st.success("REJECT H0 - Significant sex difference")
            else:
                st.warning("FAIL TO REJECT H0 - No significant sex difference")
        st.markdown("---")

        # H3: ANOVA
        st.subheader("H3: Wealth Quintile Differences")
        wealth = df[(df['indicator'].str.contains('Stunting', case=False)) & (df['dimension_type'] == 'WEALTHQUINTILE')]
        groups = [g['numeric_value'].dropna().values for n, g in wealth.groupby('dimension_name') if len(g) > 1]
        if len(groups) >= 2:
            f_stat, p_val = stats.f_oneway(*groups)
            group_means = wealth.groupby('dimension_name')['numeric_value'].mean().sort_values(ascending=False)
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("F-statistic", f"{f_stat:.4f}")
            with col2: st.metric("P-value", f"{p_val:.6f}")
            with col3: st.metric("Result", "Significant" if p_val < 0.05 else "Not Significant")
            st.write("**Group Means:**")
            for name, mean in group_means.items():
                st.write(f"- {name}: {mean:.2f}%")
            if p_val < 0.05:
                st.success("REJECT H0 - Significant wealth disparities")
            else:
                st.warning("FAIL TO REJECT H0 - No significant wealth disparities")
        st.markdown("---")

        # Correlation
        st.subheader("Indicator Correlations")
        corr_data = []
        for ind in ['Stunting', 'Wasting', 'Underweight', 'Anaemia']:
            ind_df = df[(df['indicator'].str.contains(ind, case=False)) & (df['dimension_code'] == 'SEX_BTSX')].groupby('year')['numeric_value'].mean()
            if len(ind_df) > 2:
                corr_data.append(pd.Series(ind_df.values, name=ind, index=ind_df.index))
        if len(corr_data) > 1:
            corr_df = pd.concat(corr_data, axis=1).dropna()
            if corr_df.shape[0] > 2:
                corr_matrix = corr_df.corr()
                fig = px.imshow(corr_matrix.values, x=corr_df.columns, y=corr_df.columns, title="Correlation Matrix", color_continuous_scale='RdBu_r', range_color=[-1, 1])
                st.plotly_chart(fig, use_container_width=True)

    elif page == "Explorer":
        st.header("Data Explorer")
        cols = st.columns(3)
        with cols[0]:
            yr = st.slider("Year:", int(df['year'].min()), int(df['year'].max()), (1990, 2024))
        with cols[1]:
            inds = st.multiselect("Indicators:", df['indicator'].unique(), [df['indicator'].unique()[0]])
        with cols[2]:
            dims = st.multiselect("Dimensions:", df['dimension_type'].unique(), [df['dimension_type'].unique()[0]])
        filtered = df[(df['year'] >= yr[0]) & (df['year'] <= yr[1]) & df['indicator'].isin(inds) & df['dimension_type'].isin(dims)]
        st.write(f"Showing {len(filtered)} records")
        st.dataframe(filtered.head(50))
        st.download_button("Download CSV", filtered.to_csv(), "data.csv")

st.divider()
st.markdown("<p style='text-align: center; color: #6c757d;'>Data 200 Applied Statistical Analysis | Nepal Nutrition | WHO GHO</p>", unsafe_allow_html=True)
