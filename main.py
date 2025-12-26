import json

import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="Health & Lifestyle Dashboard",
    layout="wide"
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with open("assets/main_hero.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

with open("Assistant_Bot.json") as nm:
    animation = json.load(nm)

st_lottie(animation, height=150)














