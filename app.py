import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Adolescent Employment & Health Outcomes",
    layout="wide"
)

# -------------------------------------------------
# Reset Function
# -------------------------------------------------
def reset_app():
    st.session_state.clear()
    st.experimental_rerun()

# -------------------------------------------------
# Title & Introduction
# -------------------------------------------------
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

# =================================================
# SIDEBAR — INPUTS WITH SAFE STATE MANAGEMENT
# =================================================
st.sidebar.header("Input Parameters")

# Default values
defaults = {
    "preset": "Custom",
    "work_hours": 20,
    "sleep_hours": 7.5,
    "academic_load": "Moderate",
    "homework_hours": 8
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Preset selector
preset = st.sidebar.selectbox(
    "Preset Scenarios",
    [
        "Custom",
        "Moderate Work + Good Sleep",
        "High Work + Low Sleep",
        "Low Work + Heavy Academics"
    ],
    index=[
        "Custom",
        "Moderate Work + Good Sleep",
        "High Work + Low Sleep",
        "Low Work + Heavy Academics"
    ].index(st.session_state.preset)
)

# Apply preset only when changed
if preset != st.session_state.preset:
    st.session_state.preset = preset

    if preset == "Moderate Work + Good Sleep":
        st.session_state.update({
            "work_hours": 15,
            "sleep_hours": 8.0,
            "academic_load": "Moderate",
            "homework_hours": 9
        })
    elif preset == "High Work + Low Sleep":
        st.session_state.update({
            "work_hours": 30,
            "sleep_hours": 6.0,
            "academic_load": "Heavy",
            "homework_hours": 5
        })
    elif preset == "Low Work + Heavy Academics":
        st.session_state.update({
            "work_hours": 5,
            "sleep_hours": 7.0,
            "academic_load": "Heavy",
            "homework_hours": 12
        })

# Sliders
work_hours = st.sidebar.slider(
    "Weekly Work Hours", 0, 40, st.session_state.work_hours
)
sleep_hours = st.sidebar.slider(
    "Average Sleep Per Night (hours)", 5.0, 9.0, st.session_state.sleep_hours, 0.5
)
academic_load_label = st.sidebar.selectbox(
    "Academic Load",
    ["Light", "Moderate", "Heavy"],
    index=["Light", "Moderate", "Heavy"].index(st.session_state.academic_load)
)
homework_hours = st.sidebar.slider(
    "Homework / Study Hours per Week", 0, 15, st.session_state.homework_hours
)

# Persist slider changes
st.session_state.work_hours = work_hours
st.session_state.sleep_hours = sleep_hours
st.session_state.academic_load = academic_load_label
st.session_state.homework_hours = homework_hours

st.sidebar.markdown("---")
run_simulation = st.sidebar.button("Run Simulation")
st.sidebar.button("Restart Simulation", on_click=reset_app)

# -------------------------------------------------
# Convert Academic Load
# -------------------------------------------------
academic_load_map = {"Light": 0.3, "Moderate": 0.6, "Heavy": 1.0}
academic_load = academic_load_map[academic_load_label]

# -------------------------------------------------
# MODEL LOGIC (NONLINEAR + RESPONSIVE)
# -------------------------------------------------
def run_model(work_hours, sleep_hours, academic_load, homework_hours):
    W_norm = work_hours / 40
    H_norm = homework_hours / 15
    sleep_deficit = max(0, (8 - sleep_hours) / 3)

    # Threshold effect at 20 hours/week
    if work_hours <= 20:
        work_penalty = 0.2 * W_norm
    else:
        work_penalty = 0.1 + 0.6 * ((work_hours - 20) / 20)

    AEI_raw = (0.5 * H_norm) - work_penalty - (0.3 * sleep_deficit)
    AEI = np.clip((AEI_raw + 0.5) * 100, 0, 100)

    CLS_raw = (0.5 * academic_load) + (0.3 * sleep_deficit) + (0.2 * W_norm)
    CLS = "Low" if CLS_raw < 0.4 else "Moderate" if CLS_raw < 0.7 else "High"

    SRI_raw = (0.4 * sleep_deficit) + (0.35 * W_norm) + (0.25 * academic_load)
    SRI = "Low" if SRI_raw < 0.4 else "Moderate" if SRI_raw < 0.7 else "Elevated"

    LHR_raw = (0.5 * sleep_deficit) + (0.4 * W_norm) + (0.1 * academic_load)
    LHR = "Minimal" if LHR_raw < 0.4 else "Increasing" if LHR_raw < 0.7 else "Elevated"

    return AEI, CLS, SRI, LHR

# =================================================
# RESULTS
# =================================================
if run_simulation:
    st.header("Simulation Results")

    AEI, CLS, SRI, LHR = run_model(
        work_hours, sleep_hours, academic_load, homework_hours
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Academic Engagement Index", f"{int(AEI)} / 100")
    c2.metric("Cognitive Load", CLS)
    c3.metric("Stress Risk", SRI)
    c4.metric("Health Risk Trend", LHR)

    st.markdown("---")

    # -----------------------------
    # RESPONSIVE CHART (FIXED)
    # -----------------------------
    st.subheader("Work Hours vs Academic Engagement")

    hours = np.arange(0, 41)
    engagement = []

    for h in hours:
        aei, _, _, _ = run_model(
            work_hours=h,
            sleep_hours=sleep_hours,
            academic_load=academic_load,
            homework_hours=homework_hours
        )
        engagement.append(aei)

    current_aei, _, _, _ = run_model(
        work_hours, sleep_hours, academic_load, homework_hours
    )

    fig, ax = plt.subplots()
    ax.plot(hours, engagement, label="Modeled Trend")
    ax.scatter(work_hours, current_aei, s=80, zorder=3, label="Current Scenario")
    ax.axvline(20, linestyle="--", alpha=0.6, label="~20 hr threshold")

    ax.set_xlabel("Weekly Work Hours")
    ax.set_ylabel("Academic Engagement Index")
    ax.set_title(
        "Work Hours vs Academic Engagement\n"
        "(Conditioned on Sleep, Academic Load, and Homework)"
    )
    ax.legend()

    st.pyplot(fig)

# =================================================
# WHY UW–MADISON
# =================================================
st.markdown("---")
if st.button("Why UW–Madison?"):
    st.subheader("Why This Project and UW–Madison")

    st.markdown("""
    This project was created to reflect how I approach learning when given the opportunity
    to explore complex questions. Rather than simply expressing interest, I wanted to
    demonstrate **analytical thinking, research awareness, and interdisciplinary problem-solving**.

 UW–Madison’s emphasis on undergraduate research, biomedical sciences, and data-informed inquiry
    aligns strongly with my interest. With access to UW–Madison’s academic environment and
    research opportunities, I am confident I can continue developing work like this at a
    deeper and more rigorous level if given a chance to attend and prove myself. - Emily Mendoza Dominguez

    """)

# =================================================
# REFERENCES
# =================================================
st.markdown("---")
st.subheader("References")

st.markdown("""
- National Academies of Sciences. *Protecting Youth at Work*  
- Grant et al. (2021). Wisconsin Center for Education Research  
- Adolescent Employment and Health Outcomes. *NIH (PMC)*
""")
