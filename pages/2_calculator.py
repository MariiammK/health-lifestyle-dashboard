import os

import pandas as pd
import streamlit as st

st.title("BMI Calculator")

csv_path = os.path.join("data", "cleaned", "clean_health.csv")
df = pd.read_csv(csv_path)
avg_bmi = df["bmi"].mean()

with st.form("bmi_form"):
    height = st.number_input("Height (cm)", min_value=0.0, step=0.1)
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
    submitted = st.form_submit_button("Calculate BMI")

if submitted:
    if height > 0 and weight > 0:
        bmi = weight / ((height / 100) ** 2)

        st.metric("Your BMI", f"{bmi:.2f}")

        if bmi < 18.5:
            st.warning("Underweight")
        elif bmi < 25:
            st.success("Normal weight")
        elif bmi < 30:
            st.warning("Overweight")
        else:
            st.error("Obesity")

        st.progress(min(bmi / 40, 1.0))
        st.metric("Average BMI in dataset", f"{avg_bmi:.1f}")
    else:
        st.error("Please enter height and weight.")





