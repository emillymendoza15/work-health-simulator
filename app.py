import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Adolescent Work & Health Simulator",
    layout="wide"
)

# Title and intro
st.title("Adolescent Work, Academic Performance, and Health")
st.subheader("An Exploratory Biomedical Research Simulation")

st.markdown("""
This interactive project explores how work hours during adolescence may be associated 
with academic engagement, cognitive load, stress, and long-term health trends.

**Disclaimer:**  
This is an exploratory, population-level model informed by published research.  
It does not make individual predictions or medical claims.
""")

# Sidebar inputs (placeholder for now)
st.sidebar.header("Input Parameters")

work_hours = st.sidebar.slider(
    "Weekly Work Hours",
    min_value=0,
    max_value=40,
    value=20,
    step=1
)

sleep_hours = st.sidebar.slider(
    "Average Sleep Per Night (hours)",
    min_value=5.0,
    max_value=9.0,
    value=7.5,
    step=0.5
)

academic_load = st.sidebar.selectbox(
    "Academic Load",
    ["Light", "Moderate", "Heavy"]
)

homework_hours = st.sidebar.slider(
    "Homework / Study Hours per Week",
    min_value=0,
    max_value=15,
    value=8,
    step=1
)

# Display inputs (temporary)
st.header("Current Scenario")
st.write(f"**Work Hours:** {work_hours} hrs/week")
st.write(f"**Sleep:** {sleep_hours} hrs/night")
st.write(f"**Academic Load:** {academic_load}")
st.write(f"**Homework Time:** {homework_hours} hrs/week")

