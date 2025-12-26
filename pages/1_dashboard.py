import os

import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import scipy.stats as stats
import streamlit as st

st.title("Health & Lifestyle Dashboard")
st.markdown(
    """
    This dashboard provides an exploratory analysis of a health and lifestyle dataset.
    It helps users understand how factors such as age, BMI, smoking behavior,
    physical activity, and calorie intake relate to disease risk and to each other.
    """
)

csv_path = os.path.join("data", "cleaned", "clean_health.csv")
df = pd.read_csv(csv_path)
st.caption(
    "Use this slider to focus the analysis on a specific age group. "
    "All visualizations below update dynamically based on the selected age range."
)

age_range = st.slider("Age range", 18, 80, (25, 60))

df_filtered = df[
    (df["age"] >= age_range[0]) &
    (df["age"] <= age_range[1])
    ]




st.subheader("Dataset Overview")
st.caption(
    "This table summarizes the main numerical features of the dataset, "
    "showing average values, variability, and ranges for the selected age group."
)
# st.write(df_filtered.describe())

readable_names = {
    "id": "ID",
    "age": "Age",
    "gender": "Gender",
    "bmi": "Body Mass Index (BMI)",
    "daily_steps": "Daily Steps",
    "sleep_hours": "Sleep Duration",
    "water_intake_l": "Daily Water Intake",
    "calories_consumed": "Daily Calorie Intake (kcal)",
    "smoker": "Smoking Status",
    "alcohol": "Alcohol Consumption",
    "resting_hr": "Resting Heart Rate (bpm)",
    "systolic_bp": "Systolic Blood Pressure (mmHg)",
    "diastolic_bp": "Diastolic Blood Pressure (mmHg)",
    "cholesterol": "Cholesterol Level (mg/dL)",
    "family_history": "Family History of Disease",
    "disease_risk": "Disease Risk"
}
summary = df_filtered.describe()

summary = summary.rename(
    columns={col: readable_names[col] for col in summary.columns if col in readable_names}
)

st.write(summary)





st.subheader("Age Distribution (Boxplot)")
st.caption(
    "This boxplot shows the distribution of ages in the selected group. "
)
fig_age_box = px.box(df_filtered, y="age")
st.plotly_chart(fig_age_box)

fig_pie = px.pie(
    df_filtered.assign(
        disease_risk_label=df_filtered['disease_risk'].map({0: "No", 1: "Yes"})
    ),
    names='disease_risk_label',
)
st.subheader('Disease Risk Proportion')
st.caption(
    "This chart shows the proportion of individuals with and without disease risk "
    "within the selected age range."
)
st.plotly_chart(fig_pie)



# Category counts
risk_counts = df_filtered['disease_risk'].value_counts().reset_index()
risk_counts.columns = ['Risk', 'Count']
risk_counts['Risk'] = risk_counts['Risk'].map({0: "No", 1: "Yes"})

fig_risk = px.bar(
    risk_counts,
    x='Risk',
    y='Count',
    # title='Disease Risk Distribution',
    text='Count', color='Risk'
)
st.subheader('Disease Risk Distribution')
st.caption(
    "This bar chart displays the absolute number of individuals in each disease risk category, "
    "allowing an easy comparison between groups."
)
st.plotly_chart(fig_risk)


# smoker histogram
fig_smoker = px.histogram(
    df_filtered.assign(
        smoker_label=df_filtered['smoker'].map({0: "No", 1: "Yes"})
    ),
    x="smoker_label",
    # title="Smoker Distribution", color="smoker_label"
)
st.subheader('Smoker Distribution')
st.caption(
    "This chart compares the number of smokers and non-smokers."
)
st.plotly_chart(fig_smoker)



st.subheader("BMI Visual Analysis")

st.markdown(
    """
    This section explores Body Mass Index (BMI) using different visual perspectives.
    """
)

chart_type = st.radio(
    "Select chart to display:",
    ["Boxplot", "Histogram", "Scatter"]
)

if chart_type == "Boxplot":
    st.caption("Shows BMI spread and potential outliers.")
    st.plotly_chart(px.box(df_filtered, y='bmi'))
elif chart_type == "Histogram":
    st.caption("Shows how BMI values are distributed across the population.")
    st.plotly_chart(px.histogram(df_filtered, x='bmi'))
elif chart_type == "Scatter":
    st.caption("Shows the relationship between age and BMI.")
    st.plotly_chart(px.scatter(df_filtered, x='age', y='bmi'))


## heatmap
st.subheader("Correlation Heatmap")

st.markdown(
    """
    This heatmap visualizes the relationships between key numerical variables.
    It helps identify which factors tend to increase or decrease together and
    how strong those relationships are.
    """
)

st.caption(
    "Values close to 1 indicate a strong positive relationship, values close to -1 indicate "
    "a strong negative relationship, and values near 0 indicate little or no relationship."
)

# columns to include in correlation
corr_cols = ["age", "bmi", "daily_steps", "calories_consumed"]

corr = df[corr_cols].corr()

corr = corr.rename(
    index=readable_names,
    columns=readable_names
)

fig_heatmap = ff.create_annotated_heatmap(
    z=corr.values,
    x=list(corr.columns),
    y=list(corr.index),
)
st.plotly_chart(fig_heatmap)


##
st.header("Correlation & Statistical Significance")

st.markdown(
    """
    This section allows you to examine the relationship between two numerical variables.
    Correlation indicates how strongly two variables move together, while statistical significance
    helps determine whether the observed relationship is likely to be meaningful or due to chance.
    """
)

st.caption(
    "Correlation values range from -1 to 1. Values closer to these extremes indicate stronger relationships."
)

numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()


display_names = {
    col: readable_names.get(col, col) for col in numeric_cols
}

# reverse mapping: display -> original
reverse_names = {v: k for k, v in display_names.items()}

col1, col2 = st.columns(2)

var1_display = col1.selectbox(
    "Select first variable",
    options=list(display_names.values()),
    index=None
)

var2_display = col2.selectbox(
    "Select second variable",
    options=list(display_names.values()),
    index=None
)

if var1_display and var2_display:
    var1 = reverse_names[var1_display]
    var2 = reverse_names[var2_display]

    st.subheader("Correlation Result")

    if var1 == var2:
        st.metric("Correlation", "1.000")
        st.write("**p-value**: :green[0]")
    else:
        corr, p_value = stats.pearsonr(df[var1], df[var2])

        st.metric("Correlation", f"{corr:.3f}")
        st.write(f"**p-value**: :green[{p_value:.5f}]")

        if p_value < 0.05:
            st.write("Result is **statistically significant**")
        else:
            st.write("Result is **not statistically significant**")