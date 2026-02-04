import streamlit as st
import numpy as np
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Adolescent Work & Health Simulator",
    layout="wide"
)

# -----------------------------
# Title & Introduction
# -----------------------------
st.title("Adolescent Work, Academic Performance, and Health")
st.subheader("An Exploratory Biomedical Research Simulation")

st.markdown("""
This interactive project explores how **work hours during adolescence** may be associated with  
**academic engagement, cognitive load, stress exposure, and long-term health trends**.

**Disclaimer:**  
This is a self-directed, exploratory model informed by published research.  
It presents *population-level associations*, not individual predictions or medical advice.
""")

st.markdown("---")

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("Input Parameters")

# Preset Scenarios
preset = st.sidebar.selectbox(
    "Preset Scenarios",
    [
        "Custom",
        "Moderate Work + Good Sleep",
        "High Work + Low Sleep",
        "Low Work + Heavy Academics"
    ]
)

# Default values
work_hours = 20
sleep_hours = 7.5
academic_load_label = "Moderate"
homework_hours = 8

# Apply presets
if preset == "Moderate Work + Good Sleep":
    work_hours = 15
    sleep_hours = 8
    academic_load_label = "Moderate"
    homework_hours = 9

elif preset == "High Work + Low Sleep":
    work_hours = 30
    sleep_hours = 6
    academic_load_label = "Heavy"
    homework_hours = 5

elif preset == "Low Work + Heavy Academics":
    work_hours = 5
    sleep_hours = 7
    academic_load_label = "Heavy"
    homework_hours = 12

# Sliders
work_hours = st.sidebar.slider("Weekly Work Hours", 0, 40, work_hours)
sleep_hours = st.sidebar.slider("Average Sleep Per Night (hours)", 5.0, 9.0, sleep_hours, 0.5)
academic_load_label = st.sidebar.selectbox("Academic Load", ["Light", "Moderate", "Heavy"],
                                           index=["Light","Moderate","Heavy"].index(academic_load_label))
homework_hours = st.sidebar.slider("Homework / Study Hours per Week", 0, 15, homework_hours)

st.sidebar.markdown("---")
run_simulation = st.sidebar.button("Run Simulation")

# -----------------------------
# Convert Academic Load
# -----------------------------
academic_load_map = {"Light": 0.3, "Moderate": 0.6, "Heavy": 1.0}
academic_load = academic_load_map[academic_load_label]

# -----------------------------
# Model Logic
# -----------------------------
def run_model(work_hours, sleep_hours, academic_load, homework_hours):
    W_norm = work_hours / 40
    H_norm = homework_hours / 15
    sleep_deficit = max(0, (8 - sleep_hours) / 3)

    AEI_raw = (0.5 * H_norm) - (0.4 * W_norm) - (0.3 * sleep_deficit)
    AEI = np.clip((AEI_raw + 0.5) * 100, 0, 100)

    CLS_raw = (0.5 * academic_load) + (0.3 * sleep_deficit) + (0.2 * W_norm)
    CLS = "Low" if CLS_raw < 0.4 else "Moderate" if CLS_raw < 0.7 else "High"

    SRI_raw = (0.4 * sleep_deficit) + (0.35 * W_norm) + (0.25 * academic_load)
    SRI = "Low" if SRI_raw < 0.4 else "Moderate" if SRI_raw < 0.7 else "Elevated"

    LHR_raw = (0.5 * sleep_deficit) + (0.4 * W_norm) + (0.1 * academic_load)
    LHR = "Minimal" if LHR_raw < 0.4 else "Increasing" if LHR_raw < 0.7 else "Elevated"

    return AEI, CLS, SRI, LHR

# -----------------------------
# Results
# -----------------------------
if run_simulation:
    st.header("Simulation Results")

    AEI, CLS, SRI, LHR = run_model(work_hours, sleep_hours, academic_load, homework_hours)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Academic Engagement Index", f"{int(AEI)} / 100")
    col2.metric("Cognitive Load", CLS)
    col3.metric("Stress Risk", SRI)
    col4.metric("Health Risk Trend", LHR)

    # -----------------------------
    # Line Chart: Work Hours vs Engagement
    # -----------------------------
    st.markdown("---")
    st.subheader("Work Hours vs Academic Engagement")

    hours = np.arange(0, 41)
    engagement_curve = []

    for h in hours:
        aei, _, _, _ = run_model(h, sleep_hours, academic_load, homework_hours)
        engagement_curve.append(aei)

    df = pd.DataFrame({
        "Weekly Work Hours": hours,
        "Academic Engagement Index": engagement_curve
    })

    st.line_chart(df.set_index("Weekly Work Hours"))

    # -----------------------------
    # Interpretation
    # -----------------------------
    st.markdown("""
    **Interpretation:**  
    The curve illustrates diminishing academic engagement as work hours increase,
    particularly when sleep and academic demands remain constant. This reflects
    patterns observed in adolescent education and health research.
    """)

# -----------------------------
# Why UW–Madison Button
# -----------------------------
st.markdown("---")
if st.button("Why UW–Madison?"):
    st.subheader("Why This Project and UW–Madison")

    st.markdown("""
    This project was created to reflect how I approach learning when given the opportunity
    to engage deeply with research. Rather than presenting interest alone, I wanted to
    demonstrate **analytical thinking, research awareness, and problem-solving**.

    UW–Madison’s emphasis on undergraduate research, data-informed inquiry, and biomedical
    sciences aligns strongly with how I learn best by exploring complex systems and understanding
    tradeoffs. With access to UW–Madison’s academic resources and research environment,
    I am confident I would continue developing projects like this at a deeper and more rigorous level.
    """)

# -----------------------------
# References
# -----------------------------
st.markdown("---")
st.subheader("References")

st.markdown("""
- National Academies of Sciences. *Protecting Youth at Work*  
- Grant et al. (2021). Wisconsin Center for Education Research  
- Adolescent Employment and Health Outcomes. *NIH (PMC)*
""")
