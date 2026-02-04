import streamlit as st
import numpy as np
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Adolescent Employment & Health Outcomes",
    layout="wide"
)

# -----------------------------
# Title & Introduction
# -----------------------------
st.title("Adolescent Employment, Academic Engagement, and Health Outcomes 🦡❤️")
st.subheader("An Exploratory Biomedical Research Simulation")

st.markdown("""
This interactive project explores how **employment during adolescence** may be associated with  
**academic engagement, cognitive load, stress exposure, and long-term health trends**.

**Disclaimer:**  
This is a self-directed, exploratory model informed by published research.  
It presents *population-level associations*, not individual predictions or medical advice.
""")

st.markdown("---")

# =====================================================
# SIDEBAR — STATE-SAFE INPUTS (BUG FIXED)
# =====================================================
st.sidebar.header("Input Parameters")

# Initialize session state
if "work_hours" not in st.session_state:
    st.session_state.work_hours = 20
    st.session_state.sleep_hours = 7.5
    st.session_state.academic_load = "Moderate"
    st.session_state.homework_hours = 8

# Preset selector
preset = st.sidebar.selectbox(
    "Preset Scenarios",
    [
        "Custom",
        "Moderate Work + Good Sleep",
        "High Work + Low Sleep",
        "Low Work + Heavy Academics"
    ]
)

# Apply presets
if preset == "Moderate Work + Good Sleep":
    st.session_state.work_hours = 15
    st.session_state.sleep_hours = 8.0
    st.session_state.academic_load = "Moderate"
    st.session_state.homework_hours = 9

elif preset == "High Work + Low Sleep":
    st.session_state.work_hours = 30
    st.session_state.sleep_hours = 6.0
    st.session_state.academic_load = "Heavy"
    st.session_state.homework_hours = 5

elif preset == "Low Work + Heavy Academics":
    st.session_state.work_hours = 5
    st.session_state.sleep_hours = 7.0
    st.session_state.academic_load = "Heavy"
    st.session_state.homework_hours = 12

# Sliders (read from session_state)
work_hours = st.sidebar.slider(
    "Weekly Work Hours",
    0, 40,
    st.session_state.work_hours
)

sleep_hours = st.sidebar.slider(
    "Average Sleep Per Night (hours)",
    5.0, 9.0,
    st.session_state.sleep_hours,
    0.5
)

academic_load_label = st.sidebar.selectbox(
    "Academic Load",
    ["Light", "Moderate", "Heavy"],
    index=["Light", "Moderate", "Heavy"].index(st.session_state.academic_load)
)

homework_hours = st.sidebar.slider(
    "Homework / Study Hours per Week",
    0, 15,
    st.session_state.homework_hours
)

st.sidebar.markdown("---")
run_simulation = st.sidebar.button("Run Simulation")
reset_simulation = st.sidebar.button("Restart Simulation")

# Restart logic
if reset_simulation:
    st.session_state.clear()
    st.experimental_rerun()

# -----------------------------
# Convert Academic Load
# -----------------------------
academic_load_map = {"Light": 0.3, "Moderate": 0.6, "Heavy": 1.0}
academic_load = academic_load_map[academic_load_label]

# -----------------------------
# MODEL LOGIC (NONLINEAR FIX)
# -----------------------------
def run_model(work_hours, sleep_hours, academic_load, homework_hours):
    W_norm = work_hours / 40
    H_norm = homework_hours / 15
    sleep_deficit = max(0, (8 - sleep_hours) / 3)

    # Nonlinear work threshold effect
    if work_hours <= 20:
        work_penalty = 0.2 * W_norm
    else:
        work_penalty = 0.2 * (20 / 40) + 0.6 * ((work_hours - 20) / 20)

    AEI_raw = (0.5 * H_norm) - work_penalty - (0.3 * sleep_deficit)
    AEI = np.clip((AEI_raw + 0.5) * 100, 0, 100)

    CLS_raw = (0.5 * academic_load) + (0.3 * sleep_deficit) + (0.2 * W_norm)
    CLS = "Low" if CLS_raw < 0.4 else "Moderate" if CLS_raw < 0.7 else "High"

    SRI_raw = (0.4 * sleep_deficit) + (0.35 * W_norm) + (0.25 * academic_load)
    SRI = "Low" if SRI_raw < 0.4 else "Moderate" if SRI_raw < 0.7 else "Elevated"

    LHR_raw = (0.5 * sleep_deficit) + (0.4 * W_norm) + (0.1 * academic_load)
    LHR = "Minimal" if LHR_raw < 0.4 else "Increasing" if LHR_raw < 0.7 else "Elevated"

    return AEI, CLS, SRI, LHR

# =====================================================
# RESULTS
# =====================================================
if run_simulation:
    st.header("Simulation Results")

    AEI, CLS, SRI, LHR = run_model(
        work_hours, sleep_hours, academic_load, homework_hours
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Academic Engagement Index", f"{int(AEI)} / 100")
    col2.metric("Cognitive Load", CLS)
    col3.metric("Stress Risk", SRI)
    col4.metric("Health Risk Trend", LHR)

    st.markdown("---")

    # Line chart
    st.subheader("Work Hours vs Academic Engagement")

    hours = np.arange(0, 41)
    engagement = [run_model(h, sleep_hours, academic_load, homework_hours)[0] for h in hours]

    df = pd.DataFrame({
        "Weekly Work Hours": hours,
        "Academic Engagement Index": engagement
    })

    st.line_chart(df.set_index("Weekly Work Hours"))

    st.markdown("""
    **Interpretation:**  
    The curve reflects a **threshold effect**, where moderate employment shows minimal impact,
    while higher-intensity work is associated with sharper declines in academic engagement.
    This pattern aligns with findings in adolescent education and health research.
    """)

# =====================================================
# WHY UW–MADISON
# =====================================================
st.markdown("---")
if st.button("Why UW–Madison?"):
    st.subheader("Why This Project and UW–Madison")

    st.markdown("""
    This project was created to demonstrate how I engage with academic material when given the
    opportunity to explore it deeply. Rather than presenting interest alone, I wanted to show
    **analytical thinking, research awareness, and interdisciplinary problem-solving**.

    UW–Madison’s emphasis on undergraduate research, biomedical sciences, and data-informed inquiry
    aligns strongly with how I learn best. With access to UW–Madison’s academic environment and
    research opportunities, I am confident I can continue developing work like this at a
    deeper and more rigorous level if given a chance to attend UW-Madison. - Emily Mendoza Dominguez
    """)

# =====================================================
# REFERENCES
# =====================================================
st.markdown("---")
st.subheader("References")

st.markdown("""
- National Academies of Sciences. *Protecting Youth at Work*  
- Grant et al. (2021). Wisconsin Center for Education Research  
- Adolescent Employment and Health Outcomes. *NIH (PMC)*
""")
