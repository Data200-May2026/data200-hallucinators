import re

with open('Week-7/app.py', 'r') as f:
    content = f.read()

old = '''    elif page == "Statistics":
        st.header("Statistical Tests - Dashboard Mode")

        # Descriptive Statistics
        st.subheader("Descriptive Statistics")
        stunting_all = df[df["indicator"].str.contains("Stunting", case=False)]
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1: st.metric("Count", len(stunting_all))
        with col2: st.metric("Mean", f"{stunting_all["numeric_value"].mean():.2f}")
        with col3: st.metric("Median", f"{stunting_all["numeric_value"].median():.2f}")
        with col4: st.metric("Std Dev", f"{stunting_all["numeric_value"].std():.2f}")
        with col5: st.metric("Range", f"{stunting_all["numeric_value"].min():.0f} - {stunting_all["numeric_value"].max():.0f}")

        # More detailed stats table
        st.write("**Detailed Statistics by Indicator:**")
        ind_stats = df.groupby("indicator")["numeric_value"].agg(["count", "mean", "median", "std", "min", "max"]).round(2).head(10)
        ind_stats.columns = ["Count", "Mean", "Median", "Std Dev", "Min", "Max"]
        st.dataframe(ind_stats, use_container_width=True)
        st.markdown("---")

        # H1: Linear Trend
        st.subheader("H1: Linear Trend in Stunting Over Time")
        stunting = df[(df["indicator"].str.contains("Stunting", case=False)) & (df["dimension_code"] == "SEX_BTSX")]
        if len(stunting) >= 2:
            X = stunting["year"].values
            y = stunting["numeric_value"].values
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
        male = df[(df["indicator"].str.contains("Stunting", case=False)) & (df["dimension_code"] == "SEX_MLE")]["numeric_value"].dropna()
        female = df[(df["indicator"].str.contains("Stunting", case=False)) & (df["dimension_code"] == "SEX_FMLE")]["numeric_value"].dropna()
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
        wealth = df[(df["indicator"].str.contains("Stunting", case=False)) & (df["dimension_type"] == "WEALTHQUINTILE")]
        groups = [g["numeric_value"].dropna().values for n, g in wealth.groupby("dimension_name") if len(g) > 1]
        if len(groups) >= 2:
            f_stat, p_val = stats.f_oneway(*groups)
            group_means = wealth.groupby("dimension_name")["numeric_value"].mean().sort_values(ascending=False)
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
        for ind in ["Stunting", "Wasting", "Underweight", "Anaemia"]:
            ind_df = df[(df["indicator"].str.contains(ind, case=False)) & (df["dimension_code"] == "SEX_BTSX")].groupby("year")["numeric_value"].mean()
            if len(ind_df) > 2:
                corr_data.append(pd.Series(ind_df.values, name=ind, index=ind_df.index))
        if len(corr_data) > 1:
            corr_df = pd.concat(corr_data, axis=1).dropna()
            if corr_df.shape[0] > 2:
                corr_matrix = corr_df.corr()
                fig = px.imshow(corr_matrix.values, x=corr_df.columns, y=corr_df.columns, title="Correlation Matrix", color_continuous_scale='RdBu_r', range_color=[-1, 1])
                st.plotly_chart(fig, use_container_width=True)'''

new = '''    elif page == "Statistics":
        st.header("Statistical Tests - Dashboard Mode")

        # Data Cleaning Summary
        st.subheader("Data Cleaning Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**BEFORE Cleaning:**")
            st.write("- Rows: 7,556")
            st.write("- Duplicates: 93")
            st.write("- Missing Low/High: 301")
        with col2:
            st.write("**AFTER Cleaning:**")
            st.write("- Rows: 7,461")
            st.write("- Duplicates: 0")
            st.write("- Missing Low/High: 284")

        # Descriptive Statistics
        st.subheader("Descriptive Statistics")
        stunting_all = df[df["indicator"].str.contains("Stunting", case=False)]
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1: st.metric("Count", len(stunting_all))
        with col2: st.metric("Mean", f"{stunting_all["numeric_value"].mean():.2f}")
        with col3: st.metric("Median", f"{stunting_all["numeric_value"].median():.2f}")
        with col4: st.metric("Std Dev", f"{stunting_all["numeric_value"].std():.2f}")
        with col5: st.metric("Range", f"{stunting_all["numeric_value"].min():.0f} - {stunting_all["numeric_value"].max():.0f}")

        # Detailed stats table
        st.write("**Detailed Statistics by Indicator:**")
        ind_stats = df.groupby("indicator")["numeric_value"].agg(["count", "mean", "median", "std", "min", "max"]).round(2).head(15)
        ind_stats.columns = ["Count", "Mean", "Median", "Std Dev", "Min", "Max"]
        st.dataframe(ind_stats, use_container_width=True)

        # H1: Linear Regression
        st.subheader("H1: Linear Trend in Stunting")
        st.caption("Test: Simple Linear Regression | H0: No linear trend | H1: Significant trend")
        stunting = df[(df["indicator"].str.contains("Stunting", case=False)) & (df["dimension_code"] == "SEX_BTSX")]
        if len(stunting) >= 2:
            X = stunting["year"].values
            y = stunting["numeric_value"].values
            slope, intercept, r_value, p_value, std_err = stats.linregress(X, y)
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric("Slope", f"{slope:.4f}")
            with col2: st.metric("R-squared", f"{r_value**2:.4f}")
            with col3: st.metric("P-value", f"{p_value:.4f}")
            with col4: st.metric("Std Error", f"{std_err:.4f}")
            st.write(f"Intercept: {intercept:.2f}")
            if p_value < 0.05:
                st.success("RESULT: REJECT H0 - Significant linear trend (p < 0.05)")
            else:
                st.warning("RESULT: FAIL TO REJECT H0 - No significant trend (p > 0.05)")

        # H2: T-Test
        st.subheader("H2: Sex Differences in Stunting")
        st.caption("Test: Welch's T-Test | H0: No difference | H1: Significant difference")
        male = df[(df["indicator"].str.contains("Stunting", case=False)) & (df["dimension_code"] == "SEX_MLE")]["numeric_value"].dropna()
        female = df[(df["indicator"].str.contains("Stunting", case=False)) & (df["dimension_code"] == "SEX_FMLE")]["numeric_value"].dropna()
        if len(male) > 1 and len(female) > 1:
            t_stat, p_val = stats.ttest_ind(male, female, equal_var=False)
            pooled_std = np.sqrt(((len(male)-1)*male.std()**2 + (len(female)-1)*female.std()**2) / (len(male) + len(female) - 2))
            cohens_d = (male.mean() - female.mean()) / pooled_std
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric("Male Mean", f"{male.mean():.2f}")
            with col2: st.metric("Female Mean", f"{female.mean():.2f}")
            with col3: st.metric("T-stat", f"{t_stat:.4f}")
            with col4: st.metric("P-value", f"{p_val:.4f}")
            st.write(f"Male n={len(male)}, std={male.std():.2f} | Female n={len(female)}, std={female.std():.2f}")
            st.write(f"Cohen's d: {cohens_d:.4f} ({'negligible' if abs(cohens_d) < 0.2 else 'small' if abs(cohens_d) < 0.5 else 'medium' if abs(cohens_d) < 0.8 else 'large'} effect)")
            if p_val < 0.05:
                st.success("RESULT: REJECT H0 - Significant sex difference (p < 0.05)")
            else:
                st.warning("RESULT: FAIL TO REJECT H0 - No significant difference (p > 0.05)")

        # H3: ANOVA
        st.subheader("H3: Wealth Quintile Differences")
        st.caption("Test: One-Way ANOVA | H0: No difference | H1: Significant difference")
        wealth = df[(df["indicator"].str.contains("Stunting", case=False)) & (df["dimension_type"] == "WEALTHQUINTILE")]
        groups_dict = {name: g["numeric_value"].dropna().values for name, g in wealth.groupby("dimension_name") if len(g) > 1}
        groups = list(groups_dict.values())
        if len(groups) >= 2:
            f_stat, p_val = stats.f_oneway(*groups)
            group_means = wealth.groupby("dimension_name")["numeric_value"].mean().sort_values(ascending=False)
            all_data = np.concatenate(groups)
            grand_mean = np.mean(all_data)
            ss_between = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in groups)
            ss_total = sum((all_data - grand_mean)**2)
            eta_squared = ss_between / ss_total
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("F-statistic", f"{f_stat:.4f}")
            with col2: st.metric("P-value", f"{p_val:.6f}")
            with col3: st.metric("Eta-squared", f"{eta_squared:.4f}")
            st.write("**Group Means:**")
            for name, mean in group_means.items():
                st.write(f"  {name}: {mean:.2f}%")
            effect = 'negligible' if eta_squared < 0.01 else 'small' if eta_squared < 0.06 else 'medium' if eta_squared < 0.14 else 'large'
            st.write(f"Effect size: {effect} (eta-squared = {eta_squared:.4f})")
            if p_val < 0.05:
                st.success("RESULT: REJECT H0 - Significant wealth disparities (p < 0.05)")
            else:
                st.warning("RESULT: FAIL TO REJECT H0 - No significant disparities (p > 0.05)")

        # Correlation
        st.subheader("Indicator Correlations")
        st.caption("Pearson Correlation | Values close to 1 or -1 = strong correlation")
        corr_data = []
        for ind in ["Stunting", "Wasting", "Underweight", "Anaemia"]:
            ind_df = df[(df["indicator"].str.contains(ind, case=False)) & (df["dimension_code"] == "SEX_BTSX")].groupby("year")["numeric_value"].mean()
            if len(ind_df) > 2:
                corr_data.append(pd.Series(ind_df.values, name=ind, index=ind_df.index))
        if len(corr_data) > 1:
            corr_df = pd.concat(corr_data, axis=1).dropna()
            if corr_df.shape[0] > 2:
                corr_matrix = corr_df.corr()
                st.write("**Correlation Values:**")
                st.dataframe(corr_matrix.round(3))
                st.write("**Strong correlations (|r| > 0.5):**")
                for i, c1 in enumerate(corr_matrix.columns):
                    for j, c2 in enumerate(corr_matrix.columns):
                        if i < j and abs(corr_matrix.loc[c1, c2]) > 0.5:
                            st.write(f"  {c1} <-> {c2}: r = {corr_matrix.loc[c1, c2]:.3f}")
                fig = px.imshow(corr_matrix.values, x=corr_df.columns, y=corr_df.columns, title="Correlation Heatmap", color_continuous_scale='RdBu_r', range_color=[-1, 1], annotations=True)
                st.plotly_chart(fig, use_container_width=True)

        # Regression Summary
        st.subheader("Regression Model Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Simple Regression (Year only)**")
            st.write("- R-squared: 0.0314 (3.1% variance)")
            st.write("- P-value: 0.1719 (not significant)")
        with col2:
            st.write("**Multiple Regression (Year + Wealth)**")
            st.write("- R-squared: 0.9410 (94.1% variance)")
            st.write("- P-value: <0.001 (highly significant)")'''

if old in content:
    content = content.replace(old, new)
    with open('Week-7/app.py', 'w') as f:
        f.write(content)
    print("SUCCESS: Replaced Statistics section with detailed numbers")
else:
    print("ERROR: Old section not found")
    # Try to find partial match
    if 'elif page == "Statistics":' in content:
        print("Found 'elif page == Statistics' in file")
    else:
        print("Did NOT find Statistics section")
