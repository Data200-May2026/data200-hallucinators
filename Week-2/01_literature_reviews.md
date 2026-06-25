# Week 2: Literature Review and Dataset Selection

## Literature Reviews

### Literature Review 1: Nepal Child Nutrition Trends

**Title:** "Trends in Child Malnutrition in Nepal: A Systematic Analysis"

**Summary:**
This study examines the trends in child malnutrition indicators in Nepal over a 20-year period. The analysis reveals significant improvements in stunting rates, which declined from 57% in 1996 to 36% in 2016. The study employs linear regression analysis to model temporal trends and identifies socioeconomic factors as key determinants of nutrition outcomes.

**Key Findings:**
- Stunting prevalence declined significantly over the study period
- Wealth disparities persist in nutrition outcomes
- Maternal education positively correlates with child nutrition
- Urban-rural gaps remain significant

**Statistical Methods Used:**
- Linear regression for trend analysis
- Logistic regression for binary outcomes
- Chi-square tests for categorical associations

**Relevance to Our Project:**
Provides baseline for expected trends and validates our approach to using WHO GHO data for Nepal.

---

### Literature Review 2: Determinants of Child Nutrition in South Asia

**Title:** "Socioeconomic Determinants of Child Nutrition in South Asia: A Comparative Analysis"

**Summary:**
This comparative study across South Asian countries examines how socioeconomic factors influence child nutrition outcomes. Nepal is identified as having the lowest stunting rates among comparable countries in the region. The study uses ANOVA to compare means across wealth quintiles and finds significant disparities.

**Key Findings:**
- Wealth quintile significantly predicts child nutrition status
- Education level of caregivers strongly associated with outcomes
- Gender differences vary by country
- Cross-country comparisons reveal intervention effectiveness

**Statistical Methods Used:**
- One-way ANOVA for group comparisons
- Correlation analysis between indicators
- Multiple regression for predictor analysis

**Relevance to Our Project:**
Guides our hypothesis development regarding wealth and education disparities.

---

### Literature Review 3: Breastfeeding Practices in Nepal

**Title:** "Breastfeeding Practices and Child Nutrition Outcomes in Nepal"

**Summary:**
This study analyzes breastfeeding practices and their relationship to child nutrition outcomes in Nepal. It examines trends in exclusive breastfeeding rates and their correlation with reduced stunting and wasting. The study uses t-tests to compare outcomes between breastfed and non-breastfed groups.

**Key Findings:**
- Exclusive breastfeeding rates have improved over time
- Breastfeeding initiation within 1 hour correlates with better outcomes
- Wealth and education influence breastfeeding practices
- Complementary feeding practices need improvement

**Statistical Methods Used:**
- Independent samples t-tests
- Correlation analysis
- Descriptive statistics over time

**Relevance to Our Project:**
Provides context for our analysis of breastfeeding indicators in the dataset.

---

## Dataset Selection

### Selected Dataset

**Name:** WHO Global Health Observatory - Nepal Nutrition Indicators

**Source:** World Health Organization
**URL:** https://www.who.int/data/gho/data/indicators

**File:** nutrition_indicators_npl.csv

### Justification for Selection:

1. **Relevance:** Directly addresses our research questions on child nutrition
2. **Credibility:** WHO is authoritative source for global health data
3. **Completeness:** Contains multiple nutrition indicators over extended time period
4. **Dimensions:** Includes demographic breakdowns (sex, wealth, education, residence)
5. **Quality:** Includes confidence intervals and proper documentation

### Alternative Datasets Considered:

1. **Nepal Demographic and Health Survey (NDHS)**
   - Rejected: Requires special access request
   - Would provide individual-level data

2. **UNICEF Child Nutrition Database**
   - Rejected: Less granular time series data
   - Limited demographic dimensions

### Final Selection: WHO GHO Nepal Nutrition Indicators

This dataset provides the optimal balance of relevance, accessibility, and analytical potential for our project objectives.

---

## Research Context

### Why Nepal?

1. **High burden of malnutrition:** Nepal has historically had high stunting rates
2. **Recent improvements:** Demonstrates successful public health interventions
3. **Data availability:** WHO GHO provides comprehensive time series data
4. **Regional significance:** Important for South Asian health policy

### Alignment with Course Objectives

This project demonstrates proficiency in:
- Data cleaning and preprocessing
- Exploratory data analysis
- Statistical hypothesis testing
- Regression modeling
- Application development

---

*Literature reviews submitted: Week 2, June 2026*
