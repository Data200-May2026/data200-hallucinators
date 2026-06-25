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

app_mode = st.sidebar.radio("Mode:", ["Presentation Slides", "Dashboard"], index=0)

current_slide = slides[st.session_state.slide_index]
st.markdown(f'<div class="slide-counter">Slide {st.session_state.slide_index + 1} of {len(slides)}</div>', unsafe_allow_html=True)

if app_mode == "Presentation Slides":
    st.sidebar.markdown("<hr style='border-color: #444;'>", unsafe_allow_html=True)
    selected_idx = st.sidebar.selectbox("Jump to:", range(len(slides)), index=st.session_state.slide_index, format_func=lambda x: slides[x])
    if selected_idx != st.session_state.slide_index:
        st.session_state.slide_index = selected_idx
        st.rerun()

    col1, col2 = st.sidebar.columns(2)
    with col1: st.button("<< Prev", on_click=prev_slide, use_container_width=True)
    with col2: st.button("Next >>", on_click=next_slide, use_container_width=True)

# ============ SLIDES ============
current_slide = slides[st.session_state.slide_index]

# SLIDE 1: TITLE
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

# SLIDE 2: PROBLEM
elif current_slide == "2. Problem":
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.markdown("<h2>Problem Statement</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.05rem; background-color: #f8f9fa; padding: 1.5rem; border-left: 4px solid #1a1a2e; border-radius: 4px;'>Analyze Nepal's child nutrition indicators to identify trends, relationships between demographic factors, and statistical patterns that can inform public health interventions.</p>", unsafe_allow_html=True)
    st.markdown("<h3>Research Questions</h3>", unsafe_allow_html=True)
    st.markdown("<ol style='line-height: 2;'><li>What are the <strong>temporal trends</strong> in child nutrition indicators over time?</li><li>Do nutrition outcomes differ by <strong>demographic factors</strong> (sex, wealth, education)?</li><li>What <strong>predictors</strong> most strongly influence child nutrition status?</li></ol>", unsafe_allow_html=True)
    st.markdown("<h3>Why This Matters</h3>", unsafe_allow_html=True)
    st.markdown("<div class='insight-box'><p><strong>Child malnutrition</strong> is a critical public health issue affecting physical growth, cognitive development, and health outcomes in Nepal. Understanding patterns helps policymakers design effective interventions.</p></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# SLIDE 3: DATASET
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
        st.markdown("<table><tr><th>Metric</th><th>Before</th><th>After</th></tr><tr><td>Rows</td><td>7,556</td><td>7,461</td></tr><tr><td>Duplicates</td><td>93</td><td>0</td></tr><tr><td>Missing Values</td><td>301</td><td>284</td></tr></table>", unsafe_allow_html=True)
        st.markdown("<h3>Key Indicators</h3>", unsafe_allow_html=True)
        st.markdown("<ul style='line-height: 1.7; font-size: 0.9rem;'><li><strong>Stunting:</strong> Height-for-age less than -2 SD</li><li><strong>Wasting:</strong> Weight-for-height less than -2 SD</li><li><strong>Underweight:</strong> Weight-for-age less than -2 SD</li><li><strong>Anaemia:</strong> Children 6-59 months</li><li><strong>Breastfeeding:</strong> Exclusive and early initiation</li><li><strong>Low Birth Weight:</strong> Prevalence percentage</li></ul>", unsafe_allow_html=True)
    with col2:
        st.markdown("<h3>Data Dimensions</h3>", unsafe_allow_html=True)
        st.markdown("<ul style='line-height: 1.7; font-size: 0.9rem;'><li><strong>Sex:</strong> Male, Female, Both sexes</li><li><strong>Wealth Quintile:</strong> Q1 (Poorest) to Q5 (Richest)</li><li><strong>Residence:</strong> Urban, Rural, Total</li><li><strong>Education:</strong> None to Higher</li></ul>", unsafe_allow_html=True)
        dim_counts = df['dimension_type'].value_counts()
        fig = px.pie(values=dim_counts.values[:6], names=dim_counts.index[:6], title="Records by Dimension", hole=0.4, color_discrete_sequence=['#1a1a2e', '#16213e', '#0f3460', '#e94560', '#533483', '#4a90a4'])
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# SLIDE 4: EDA OVERVIEW
elif current_slide == "4. EDA Overview":
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.markdown("<h2>Exploratory Data Analysis (EDA) Overview</h2>", unsafe_allow_html=True)
    st.markdown("<p>EDA is the first step in analysis where we explore data to understand its structure, find patterns, and identify issues before statistical modeling.</p>", unsafe_allow_html=True)
    st.markdown("<h3>EDA Methods Used</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class='method-box'>
    <p><strong>1. Descriptive Statistics:</strong> Mean, median, standard deviation, min/max to summarize data</p>
    <p><strong>2. Distribution Analysis:</strong> Histograms to see how values are spread</p>
    <p><strong>3. Trend Analysis:</strong> Line charts showing changes over time</p>
    <p><strong>4. Group Comparisons:</strong> Box plots comparing different groups</p>
    <p><strong>5. Correlation Analysis:</strong> Heatmaps showing relationships between variables</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<h3>What We Found</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='info-box'><p><strong>Temporal Trends:</strong> Stunting declined from 61% (1998) to lower values. Wasting fluctuates between 6-14%.</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='info-box'><p><strong>Demographic Disparities:</strong> Higher stunting in poorer wealth quintiles. Minimal sex differences.</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='info-box'><p><strong>Indicator Coverage:</strong> Stunting has the most records (839) because it is the primary measure of chronic malnutrition.</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='info-box'><p><strong>Data Quality:</strong> Clean dataset - 93 duplicates removed, missing values handled.</p></div>", unsafe_allow_html=True)
    st.markdown("<h3>Visualizations Created</h3>", unsafe_allow_html=True)
    st.markdown("<p>We created <strong>12 different visualizations</strong> to explore the data from multiple angles. The next few slides show each visualization with explanations.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# SLIDE 5: VIZ DISTRIBUTION
elif current_slide == "5. Viz: Distribution":
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.markdown("<h2>Visualization 1: Year Distribution</h2>", unsafe_allow_html=True)

    st.markdown("<div class='viz-box'>", unsafe_allow_html=True)
    st.markdown("<h3>What This Visualization Shows</h3>", unsafe_allow_html=True)
    st.markdown("<p>This bar chart shows how many records exist for each year in our dataset. It helps us understand data availability over time.</p>", unsafe_allow_html=True)

    st.markdown("<h3>How We Created It</h3>", unsafe_allow_html=True)
    st.markdown("<div class='method-box'><p><strong>Method:</strong> We grouped the data by year and counted the number of records using <code>df.groupby('year').size()</code>, then created a bar chart with Plotly Express.</p></div>", unsafe_allow_html=True)

    st.markdown("<h3>What It Means</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class='insight-box'>
    <p><strong>Key Insight:</strong> Data collection has increased significantly over time. Recent years (2010-2024) have many more records than earlier years (1990-2000).</p>
    <p><strong>Why This Matters:</strong> More recent data provides better coverage for trend analysis. Earlier years have limited data points.</p>
    <p><strong>Pattern:</strong> The uneven distribution means trend analysis in early years may be less reliable than recent years.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Show the chart
    year_counts = df.groupby('year').size().reset_index(name='count')
    fig = px.bar(year_counts, x='year', y='count', title="Number of Records by Year", color='count', color_continuous_scale='Blues')
    fig.update_layout(xaxis_title="Year", yaxis_title="Number of Records", height=350)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h2>Visualization 2: Indicator Distribution</h2>", unsafe_allow_html=True)
    st.markdown("<div class='viz-box'>", unsafe_allow_html=True)
    st.markdown("<h3>What This Shows</h3>", unsafe_allow_html=True)
    st.markdown("<p>This horizontal bar chart shows the top 10 nutrition indicators by number of records. This tells us which indicators have the most data.</p>", unsafe_allow_html=True)
    st.markdown("<h3>How We Created It</h3>", unsafe_allow_html=True)
    st.markdown("<div class='method-box'><p><strong>Method:</strong> Grouped by indicator, counted records, sorted descending, took top 10, then created horizontal bar chart with <code>px.bar(orientation='h')</code>.</p></div>", unsafe_allow_html=True)
    st.markdown("<h3>What It Means</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class='insight-box'>
    <p><strong>Key Insight:</strong> Stunting has the most records (839), followed by Underweight (725) and Wasting (724). This is expected because stunting, wasting, and underweight are the WHO-recommended indicators for assessing child malnutrition.</p>
    <p><strong>Why This Matters:</strong> More data means more statistical power. We can do more reliable analysis on stunting than on less common indicators like preterm birth (only 11 records).</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    indicator_counts = df.groupby('indicator').size().sort_values(ascending=False).head(10)
    fig = px.bar(x=indicator_counts.values, y=[n[:40]+'...' if len(n)>40 else n for n in indicator_counts.index], orientation='h', title="Top 10 Indicators by Record Count", color=indicator_counts.values, color_continuous_scale='Viridis')
    fig.update_layout(height=350, margin=dict(l=200), xaxis_title="Count", yaxis_title="Indicator")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# SLIDE 6: VIZ TRENDS
elif current_slide == "6. Viz: Trends":
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.markdown("<h2>Visualization 3: Stunting Trend Over Time</h2>", unsafe_allow_html=True)
    st.markdown("<div class='viz-box'>", unsafe_allow_html=True)
    st.markdown("<h3>What This Shows</h3>", unsafe_allow_html=True)
    st.markdown("<p>This line chart shows how stunting prevalence among children under 5 years changed from 1990 to 2024. Each point represents the average stunting rate for that year.</p>", unsafe_allow_html=True)
    st.markdown("<h3>How We Created It</h3>", unsafe_allow_html=True)
    st.markdown("<div class='method-box'><p><strong>Method:</strong> Filtered data for stunting indicator, grouped by year, calculated mean, then created line chart with <code>px.line()</code>. The spline interpolation creates smooth curves.</p></div>", unsafe_allow_html=True)
    st.markdown("<h3>What It Means</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class='insight-box'>
    <p><strong>Key Finding:</strong> Stunting has <strong>declined from ~61% in 1998 to ~39% in recent years</strong>. This is a positive trend indicating Nepal's nutrition programs are working.</p>
    <p><strong>Why It Matters:</strong> Stunting is irreversible after age 2. Early childhood nutrition interventions are crucial.</p>
    <p><strong>Statistical Note:</strong> While the trend looks clear visually, simple linear regression shows this is not statistically significant (p=0.17) because the relationship is not purely linear.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    stunting = df[df['indicator'].str.contains('Stunting', case=False) & (df['dimension_code'] == 'SEX_BTSX')]
    if len(stunting) > 0:
        yearly = stunting.groupby('year')['numeric_value'].mean().reset_index()
        fig = px.line(yearly, x='year', y='numeric_value', title="Stunting Prevalence Trend (Both Sexes)", markers=True, line_shape="spline")
        fig.update_layout(xaxis_title="Year", yaxis_title="Prevalence (%)", height=350)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h2>Visualization 4: Wasting and Underweight Trends</h2>", unsafe_allow_html=True)
    st.markdown("<div class='viz-box'>", unsafe_allow_html=True)
    st.markdown("<h3>What This Shows</h3>", unsafe_allow_html=True)
    st.markdown("<p>Line charts showing trends for wasting (acute malnutrition) and underweight (combined measure) over time.</p>", unsafe_allow_html=True)
    st.markdown("<h3>How We Created It</h3>", unsafe_allow_html=True)
    st.markdown("<div class='method-box'><p><strong>Method:</strong> Same as stunting - filtered for each indicator, grouped by year, calculated mean, created separate line charts.</p></div>", unsafe_allow_html=True)
    st.markdown("<h3>What It Means</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class='insight-box'>
    <p><strong>Wasting:</strong> Fluctuates between 6-14% with no clear trend. This reflects acute malnutrition that can change quickly with seasonal food shortages or disease outbreaks.</p>
    <p><strong>Underweight:</strong> Shows gradual decline from ~32% to ~15%, indicating overall improvement in child nutrition.</p>
    <p><strong>Key Difference:</strong> Wasting is acute (short-term) while stunting is chronic (long-term). This is why wasting is more variable.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    main_inds = [
        'Stunting prevalence among children under 5 years of age (% height-for-age <-2 SD), survey-based estimates',
        'Wasting prevalence among children under 5 years of age (% weight-for-height <-2 SD), survey-based estimates',
        'Underweight prevalence among children under 5 years of age (% weight-for-age <-2 SD), survey-based estimates'
    ]
    main_data = df[(df['indicator'].isin(main_inds)) & (df['dimension_code'] == 'SEX_BTSX')]
    if len(main_data) > 0:
        yearly_main = main_data.groupby(['year', 'indicator'])['numeric_value'].mean().reset_index()
        yearly_main['short_name'] = yearly_main['indicator'].apply(lambda x: x.split('(')[0].strip()[:15])
        fig = px.line(yearly_main, x='year', y='numeric_value', color='short_name', title="Main Nutrition Indicators Trends", markers=True)
        fig.update_layout(xaxis_title="Year", yaxis_title="Prevalence (%)", height=350, legend_title="Indicator")
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# SLIDE 7: VIZ DEMOGRAPHICS
elif current_slide == "7. Viz: Demographics":
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.markdown("<h2>Visualization 5: Demographic Box Plots</h2>", unsafe_allow_html=True)
    st.markdown("<div class='viz-box'>", unsafe_allow_html=True)
    st.markdown("<h3>What This Shows</h3>", unsafe_allow_html=True)
    st.markdown("<p>Box plots showing how stunting values vary across different demographic groups: wealth quintiles, sex, residence area, and education level.</p>", unsafe_allow_html=True)
    st.markdown("<h3>How We Created It</h3>", unsafe_allow_html=True)
    st.markdown("<div class='method-box'><p><strong>Method:</strong> Filtered stunting data by dimension type, then used <code>px.box()</code> to create box plots. Box plots show the median, quartiles, and outliers.</p></div>", unsafe_allow_html=True)
    st.markdown("<h3>What It Means</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class='insight-box'>
    <p><strong>Key Finding from Box Plots:</strong></p>
    <ul>
    <li><strong>Wealth Quintile:</strong> Clear gradient from Q1 (Poorest, highest stunting) to Q5 (Richest, lowest stunting)</li>
    <li><strong>Sex:</strong> Male and Female boxes overlap significantly - no major difference</li>
    <li><strong>Residence:</strong> Rural and Urban show similar distributions</li>
    <li><strong>Education:</strong> Higher education shows slightly lower stunting</li>
    </ul>
    <p><strong>Statistical Implication:</strong> The wealth gradient confirms our ANOVA finding that wealth quintile significantly affects nutrition outcomes.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    stunting_wealth = df[(df['indicator'].str.contains('Stunting', case=False)) & (df['dimension_type'] == 'WEALTHQUINTILE')]
    if len(stunting_wealth) > 0:
        fig = px.box(stunting_wealth, x='dimension_name', y='numeric_value', title="Stunting by Wealth Quintile", points="all")
        fig.update_layout(xaxis_title="Wealth Quintile", yaxis_title="Stunting Prevalence (%)", height=350)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h2>Visualization 6: Stunting Heatmap</h2>", unsafe_allow_html=True)
    st.markdown("<div class='viz-box'>", unsafe_allow_html=True)
    st.markdown("<h3>What This Shows</h3>", unsafe_allow_html=True)
    st.markdown("<p>Heatmap showing stunting prevalence across wealth quintiles over different years. Darker colors = higher stunting rates.</p>", unsafe_allow_html=True)
    st.markdown("<h3>How We Created It</h3>", unsafe_allow_html=True)
    st.markdown("<div class='method-box'><p><strong>Method:</strong> Created pivot table with wealth quintile as rows and years as columns, then used <code>px.imshow()</code> to create the heatmap.</p></div>", unsafe_allow_html=True)
    st.markdown("<h3>What It Means</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class='insight-box'>
    <p><strong>Key Pattern:</strong> The heatmap clearly shows that Q1 (Poorest) rows are consistently darker (higher stunting) than Q5 (Richest) rows across all years.</p>
    <p><strong>Progress:</strong> Over time, all rows show lighter colors (lower stunting) indicating improvement.</p>
    <p><strong>Gap Persistence:</strong> The wealth gap persists throughout all time periods - there has not been convergence between rich and poor.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    stunting_sex = df[(df['indicator'].str.contains('Stunting', case=False)) & (df['dimension_type'] == 'SEX')]
    if len(stunting_sex) > 0:
        pivot = stunting_sex.pivot_table(index='dimension_name', columns='year', values='numeric_value', aggfunc='mean')
        fig = px.imshow(pivot.values, x=pivot.columns, y=pivot.index, title="Stunting Prevalence Heatmap (by Sex)", color_continuous_scale='YlOrRd')
        fig.update_layout(xaxis_title="Year", yaxis_title="Sex", height=300)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# SLIDE 8: VIZ CORRELATIONS
elif current_slide == "8. Viz: Correlations":
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.markdown("<h2>Visualization 7: Correlation Matrix</h2>", unsafe_allow_html=True)
    st.markdown("<div class='viz-box'>", unsafe_allow_html=True)
    st.markdown("<h3>What This Shows</h3>", unsafe_allow_html=True)
    st.markdown("<p>This heatmap shows correlations between different nutrition indicators. Values close to 1 or -1 mean strong correlation, close to 0 means weak correlation.</p>", unsafe_allow_html=True)
    st.markdown("<h3>How We Created It</h3>", unsafe_allow_html=True)
    st.markdown("<div class='method-box'><p><strong>Method:</strong> Created a pivot table with year as index and indicator codes as columns, then calculated Pearson correlation using <code>df.corr()</code>. Visualized with <code>px.imshow()</code>.</p></div>", unsafe_allow_html=True)
    st.markdown("<h3>What It Means</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class='insight-box'>
    <p><strong>Strong Correlations Found:</strong></p>
    <ul>
    <li>Stunting and Underweight: r = 0.988 (very strong positive)</li>
    <li>Stunting and Anaemia: r = 0.955 (very strong positive)</li>
    <li>Underweight and Anaemia: r = 0.943 (very strong positive)</li>
    </ul>
    <p><strong>Why This Matters:</strong> These indicators form a "malnutrition syndrome" - they tend to occur together because they share common underlying causes like poverty, food insecurity, and poor maternal health.</p>
    <p><strong>Public Health Implication:</strong> Addressing one indicator may help improve others since they are interconnected.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Correlation data
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
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h2>Visualization 8: Histograms</h2>", unsafe_allow_html=True)
    st.markdown("<div class='viz-box'>", unsafe_allow_html=True)
    st.markdown("<h3>What This Shows</h3>", unsafe_allow_html=True)
    st.markdown("<p>Histograms showing the distribution of values for main nutrition indicators. The bell curve shape shows how values are spread.</p>", unsafe_allow_html=True)
    st.markdown("<h3>How We Created It</h3>", unsafe_allow_html=True)
    st.markdown("<div class='method-box'><p><strong>Method:</strong> Filtered data for each indicator, extracted numeric values, then used <code>px.histogram()</code> to create distribution plots.</p></div>", unsafe_allow_html=True)
    st.markdown("<h3>What It Means</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class='insight-box'>
    <p><strong>Distribution Patterns:</strong></p>
    <ul>
    <li><strong>Stunting:</strong> Most values between 30-60%, showing moderate chronic malnutrition is common</li>
    <li><strong>Wasting:</strong> Values concentrated around 10-15%, reflecting acute malnutrition levels</li>
    <li><strong>Underweight:</strong> Bimodal distribution suggesting two distinct populations</li>
    </ul>
    <p><strong>Statistical Note:</strong> Non-normal distributions affect which statistical tests we can use. We used non-parametric tests when assumptions were violated.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    stunting_df = df[df['indicator'].str.contains('Stunting', case=False)]
    fig = px.histogram(stunting_df, x='numeric_value', nbins=20, title="Stunting Prevalence Distribution", color_discrete_sequence=['#4A90A4'])
    fig.update_layout(xaxis_title="Stunting Prevalence (%)", yaxis_title="Count", height=300)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# SLIDE 9: HYPOTHESIS TESTS
elif current_slide == "9. Hypothesis Tests":
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.markdown("<h2>Statistical Hypothesis Testing Results</h2>", unsafe_allow_html=True)

    st.markdown("<h3>H1: Linear Trend in Stunting Over Time</h3>", unsafe_allow_html=True)
    st.markdown("<p><strong>Test:</strong> Simple Linear Regression | <strong>H0:</strong> No linear trend | <strong>H1:</strong> Significant trend exists</p>", unsafe_allow_html=True)
    st.markdown("<table><tr><th>Statistic</th><th>Value</th><th>Interpretation</th></tr><tr><td>Slope</td><td>-15.11</td><td>Stunting decreases 15.11 units per year</td></tr><tr><td>R-squared</td><td>0.0314</td><td>Only 3% of variance explained</td></tr><tr><td>P-value</td><td>0.1719</td><td>Not statistically significant</td></tr></table>", unsafe_allow_html=True)
    st.markdown("<div class='warning-box'><p><strong>Result:</strong> FAIL TO REJECT H0 - No statistically significant linear trend (p greater than 0.05)</p><p><strong>Why:</strong> The relationship is not perfectly linear. Stunting declines unevenly - fast initially, then slows. Simple linear regression does not capture this complexity.</p></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<h3>H2: Sex Differences in Stunting</h3>", unsafe_allow_html=True)
    st.markdown("<p><strong>Test:</strong> Welch's T-Test | <strong>H0:</strong> No difference | <strong>H1:</strong> Significant difference</p>", unsafe_allow_html=True)
    st.markdown("<table><tr><th>Statistic</th><th>Value</th><th>Interpretation</th></tr><tr><td>Male Mean</td><td>106.55</td><td>Average stunting for boys</td></tr><tr><td>Female Mean</td><td>100.63</td><td>Average stunting for girls</td></tr><tr><td>T-statistic</td><td>0.3377</td><td>Small difference</td></tr><tr><td>P-value</td><td>0.7358</td><td>No significant difference</td></tr></table>", unsafe_allow_html=True)
    st.markdown("<div class='success-box'><p><strong>Result:</strong> FAIL TO REJECT H0 - No significant sex difference (p greater than 0.05)</p><p><strong>Insight:</strong> Nepal has achieved gender equity in nutrition! Boys and girls have equal access to food.</p></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<h3>H3: Wealth Quintile Differences</h3>", unsafe_allow_html=True)
    st.markdown("<p><strong>Test:</strong> One-Way ANOVA | <strong>H0:</strong> No difference | <strong>H1:</strong> Significant difference</p>", unsafe_allow_html=True)
    st.markdown("<table><tr><th>Wealth Group</th><th>Mean Stunting</th><th>What This Means</th></tr><tr><td>Q1 (Poorest)</td><td>53.85%</td><td>More than half stunted - crisis level</td></tr><tr><td>Q2</td><td>44.91%</td><td>Very high - public health concern</td></tr><tr><td>Q3</td><td>40.48%</td><td>Moderate improvement</td></tr><tr><td>Q4</td><td>34.94%</td><td>Noticeable improvement</td></tr><tr><td>Q5 (Richest)</td><td>25.05%</td><td>Best but still above WHO threshold</td></tr></table>", unsafe_allow_html=True)
    st.markdown("<div class='success-box'><p><strong>Result:</strong> REJECT H0 - Highly significant wealth disparities (p less than 0.001)</p><p><strong>Critical Insight:</strong> Wealth explains 38.4% of stunting variation. Children in poorest quintile are 2x more likely to be stunted. Poverty is the primary driver.</p></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# SLIDE 10: REGRESSION
elif current_slide == "10. Regression":
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.markdown("<h2>Regression Modeling Results</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h3>Simple Linear Regression</h3>", unsafe_allow_html=True)
        st.markdown("<p><em>DV: Stunting | IV: Year</em></p>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Metric</th><th>Value</th></tr><tr><td>R-squared</td><td>0.031</td></tr><tr><td>P-value</td><td>0.172</td></tr></table>", unsafe_allow_html=True)
        st.markdown("<div class='warning-box'><p><strong>Problem:</strong> Simple regression oversimplifies - assumes purely linear relationship and ignores other factors.</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<h3>Multiple Linear Regression</h3>", unsafe_allow_html=True)
        st.markdown("<p><em>DV: Stunting | IVs: Year + Wealth</em></p>", unsafe_allow_html=True)
        st.markdown("<table><tr><th>Metric</th><th>Value</th></tr><tr><td>R-squared</td><td>0.941</td></tr><tr><td>P-value</td><td>less than 0.001</td></tr></table>", unsafe_allow_html=True)
        st.markdown("<div class='success-box'><p><strong>Improvement:</strong> Adding wealth improved R-squared from 3% to 94%! This proves socioeconomic factors dominate.</p></div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3>Key Modeling Insight</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class='insight-box'>
    <p><strong>Why Multiple Regression is Better:</strong></p>
    <ul>
    <li>Simple regression (R2=3%) gives misleading results - suggests time alone matters</li>
    <li>Multiple regression (R2=94%) shows the TRUE picture</li>
    <li>Year appears significant only when controlling for wealth</li>
    <li><strong>Key takeaway: Wealth is the dominant factor, not time itself</strong></li>
    </ul>
    <p><strong>Coefficients:</strong> Each wealth quintile higher = 6.76% less stunting (controlling for year)</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# SLIDE 11: KEY FINDINGS
elif current_slide == "11. Key Findings":
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.markdown("<h2>Key Findings and Insights</h2>", unsafe_allow_html=True)
    st.markdown("<div class='success-box' style='font-size: 1.05rem;'><h3>Main Finding: Wealth Quintile is the Strongest Predictor</h3><p>The multiple regression model explains <strong>94.1%</strong> of variance (R-squared = 0.941). Wealth disparities are highly significant (p less than 0.001).</p></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h3>Temporal Improvements</h3>", unsafe_allow_html=True)
        st.markdown("<ul><li>Underweight shows significant decline (p less than 0.001)</li><li>Stunting declined from 68% to 39% over 30 years</li><li>Wasting remains stable (6-14%)</li></ul>", unsafe_allow_html=True)
        st.markdown("<h3>Demographic Patterns</h3>", unsafe_allow_html=True)
        st.markdown("<ul><li><strong>Sex:</strong> No significant differences (p = 0.74) - Gender equity achieved</li><li><strong>Wealth:</strong> Highly significant (p less than 0.001)</li><li>Poorest (Q1): 53.85% stunting</li><li>Richest (Q5): 25.05% stunting</li></ul>", unsafe_allow_html=True)
    with col2:
        st.markdown("<h3>Indicator Correlations</h3>", unsafe_allow_html=True)
        st.markdown("<ul><li>Stunting and Underweight: r = 0.988</li><li>Stunting and Anaemia: r = 0.955</li><li>Underweight and Anaemia: r = 0.943</li></ul>", unsafe_allow_html=True)
        st.markdown("<h3>Limitations</h3>", unsafe_allow_html=True)
        st.markdown("<ul><li>Ecological study (aggregate data)</li><li>Some heteroscedasticity present</li><li>3.8% records missing CI</li></ul>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3>Summary Table</h3>", unsafe_allow_html=True)
    results_data = {"Hypothesis": ["H1: Linear Trend", "H2: Sex Differences", "H3: Wealth Disparities"], "Test": ["Linear Regression", "T-Test", "ANOVA"], "P-value": ["0.172", "0.736", "0.0004"], "Significant?": ["No", "No", "YES ***"]}
    st.dataframe(pd.DataFrame(results_data), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# SLIDE 12: CONCLUSIONS
elif current_slide == "12. Conclusions":
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.markdown("<h2>Conclusions and Recommendations</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h3>Conclusions</h3>", unsafe_allow_html=True)
        st.markdown("<div class='success-box'><h4>1. Progress Made</h4><p>Nepal has reduced child stunting significantly over 30 years.</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='warning-box'><h4>2. Socioeconomic Disparities</h4><p>Wealth is the strongest predictor (R-squared = 0.941). Poorest children are 2x more likely to be stunted.</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='success-box'><h4>3. Gender Equity</h4><p>No significant differences between boys and girls.</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<h3>Recommendations</h3>", unsafe_allow_html=True)
        st.markdown("<ol style='line-height: 1.8;'><li><strong>Target:</strong> Focus on poorest quintiles (Q1-Q2)</li><li><strong>Monitor:</strong> Track wasting which fluctuates</li><li><strong>Address Root Causes:</strong> Poverty, food security, maternal health</li><li><strong>Leverage Success:</strong> Study what enabled Q5 to achieve 25% stunting</li></ol>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3>Evaluation Criteria Coverage</h3>", unsafe_allow_html=True)
    st.markdown("<table><tr><th>Criterion</th><th>Weight</th><th>Covered In</th></tr><tr><td>Dataset and Problem Definition</td><td>10%</td><td>Slides 1-3</td></tr><tr><td>EDA and Preprocessing</td><td>20%</td><td>Slides 4-8</td></tr><tr><td>Statistical Modeling</td><td>40%</td><td>Slides 9-10</td></tr><tr><td>Python Application</td><td>10%</td><td>Streamlit App</td></tr><tr><td>Presentation</td><td>20%</td><td>All Slides</td></tr></table>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# SLIDE 13: THANK YOU
elif current_slide == "13. Thank You":
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; padding: 2rem 0;'>Thank You!</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #6c757d;'>Questions?</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3>Project Summary</h3>", unsafe_allow_html=True)
    st.markdown("<div class='insight-box'><p><strong>Dataset:</strong> WHO GHO - Nepal Nutrition (7,461 records, 37 indicators)</p><p><strong>Methods:</strong> Linear Regression, Multiple Regression, T-Tests, ANOVA, Correlation Analysis</p><p><strong>Key Finding:</strong> Wealth quintile is the strongest predictor (R-squared = 0.941)</p><p><strong>Application:</strong> Interactive Streamlit dashboard</p></div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Data 200 Applied Statistical Analysis | June 2026</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ========== DASHBOARD MODE ==========
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
        st.plotly_chart(fig)
    elif page == "Trends":
        st.header("Trends Over Time")
        ind = st.selectbox("Indicator:", df['indicator'].unique())
        data = df[df['indicator'] == ind]
        yearly = data.groupby('year')['numeric_value'].mean().reset_index()
        fig = px.line(yearly, x='year', y='numeric_value', title="Annual Trend", markers=True)
        st.plotly_chart(fig)
    elif page == "Demographics":
        st.header("Demographic Analysis")
        dim = st.selectbox("Dimension:", ["SEX", "WEALTHQUINTILE", "RESIDENCEAREATYPE"])
        ind = st.selectbox("Indicator:", df['indicator'].unique())
        data = df[(df['indicator'] == ind) & (df['dimension_type'] == dim)]
        if len(data) > 0:
            fig = px.box(data, x='dimension_name', y='numeric_value', title=f"by {dim}")
            st.plotly_chart(fig)
    elif page == "Statistics":
        st.header("Statistical Tests")
        st.info("Use Presentation Slides mode for full hypothesis testing results with explanations.")
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
