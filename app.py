"""
Healthy Life Expectancy Estimator — Streamlit UI
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go

from life_expectancy_app import generate_synthetic_dataset, train_model, predict_life_expectancy

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Life Expectancy Estimator",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---------- global ---------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* hide default streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* ---------- hero ---------- */
.hero {
    background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    border-radius: 20px;
    padding: 3rem 2.5rem;
    margin-bottom: 2rem;
    color: #fff;
    text-align: center;
}
.hero h1 {
    font-size: 2.4rem;
    font-weight: 700;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.5px;
}
.hero p {
    font-size: 1.05rem;
    opacity: 0.85;
    margin: 0;
    font-weight: 300;
}

/* ---------- metric cards ---------- */
.metric-row {
    display: flex;
    gap: 1.2rem;
    margin: 1.5rem 0 2rem 0;
    flex-wrap: wrap;
}
.metric-card {
    flex: 1;
    min-width: 180px;
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}
.metric-card .label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #718096;
    font-weight: 600;
}
.metric-card .value {
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0.3rem 0 0.1rem 0;
}
.metric-card .unit {
    font-size: 0.85rem;
    color: #a0aec0;
}

/* ---------- sidebar polish ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f7fafc 0%, #edf2f7 100%);
}
section[data-testid="stSidebar"] .stSlider > div > div > div {
    color: #2d3748;
}

/* ---------- section headers ---------- */
.section-header {
    font-size: 1.15rem;
    font-weight: 600;
    color: #2d3748;
    border-left: 4px solid #4F8A8B;
    padding-left: 0.75rem;
    margin: 2rem 0 1rem 0;
}

/* ---------- disclaimer ---------- */
.disclaimer {
    background: #fffbeb;
    border: 1px solid #fcd34d;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    font-size: 0.82rem;
    color: #92400e;
    margin-top: 2rem;
    line-height: 1.6;
}

/* ---------- tip cards ---------- */
.tip-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}
.tip-card {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.2rem;
    transition: transform 0.2s;
}
.tip-card:hover { transform: translateY(-2px); }
.tip-card .icon { font-size: 1.6rem; margin-bottom: 0.4rem; }
.tip-card .title { font-weight: 600; font-size: 0.92rem; color: #2d3748; }
.tip-card .desc { font-size: 0.8rem; color: #718096; margin-top: 0.25rem; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)


# ── Load / cache model ───────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    with st.spinner("Training model on synthetic dataset..."):
        df = generate_synthetic_dataset()
        model = train_model(df)
    return model


model = load_model()

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🌿 Healthy Life Expectancy Estimator</h1>
    <p>Enter your health profile to receive a personalised longevity estimate powered by machine learning.</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar inputs ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Your Health Profile")
    st.caption("Adjust the parameters below to reflect your current health and lifestyle.")

    st.markdown("---")
    st.markdown("#### Basic Information")
    age = st.slider("Age", 20, 80, 35, help="Your current age in years")
    gender = st.radio("Sex", ["Male", "Female"], horizontal=True)

    st.markdown("---")
    st.markdown("#### Body Metrics")
    bmi = st.slider("BMI (kg/m²)", 18.0, 40.0, 24.0, 0.1,
                     help="Body Mass Index — 18.5–24.9 is considered normal")
    blood_pressure = st.slider("Systolic Blood Pressure (mmHg)", 90, 180, 120,
                                help="Optimal: below 120 mmHg")
    cholesterol = st.slider("Total Cholesterol (mg/dL)", 150, 300, 200,
                             help="Desirable: below 200 mg/dL")

    st.markdown("---")
    st.markdown("#### Lifestyle")
    smoking = st.toggle("Smoking", value=False, help="Current tobacco use")
    alcohol = st.toggle("Frequent Alcohol", value=False, help="Regular alcohol consumption")
    physical_activity = st.toggle("Regular Exercise", value=True,
                                   help="≥150 min moderate / ≥75 min vigorous per week")
    diet = st.toggle("Healthy Diet", value=True,
                      help="Rich in fruits, vegetables, whole grains, lean proteins")

    st.markdown("---")
    st.markdown("#### Medical History")
    chronic_condition = st.toggle("Chronic Condition", value=False,
                                   help="E.g. diabetes, heart disease, hypertension")

# ── Build feature dict ───────────────────────────────────────────────────────
user_features = {
    "age": age,
    "gender": 0 if gender == "Male" else 1,
    "bmi": bmi,
    "smoking": int(smoking),
    "alcohol": int(alcohol),
    "physical_activity": int(physical_activity),
    "diet": int(diet),
    "blood_pressure": float(blood_pressure),
    "cholesterol": float(cholesterol),
    "chronic_condition": int(chronic_condition),
}

predicted_le = predict_life_expectancy(model, user_features)
remaining = max(predicted_le - age, 0)

# ── Colour helpers ───────────────────────────────────────────────────────────

def le_color(le: float) -> str:
    if le >= 85:
        return "#38a169"
    if le >= 75:
        return "#4F8A8B"
    if le >= 65:
        return "#dd6b20"
    return "#e53e3e"


color = le_color(predicted_le)

# ── Metric cards ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="metric-row">
    <div class="metric-card">
        <div class="label">Estimated Life Expectancy</div>
        <div class="value" style="color:{color}">{predicted_le:.1f}</div>
        <div class="unit">years</div>
    </div>
    <div class="metric-card">
        <div class="label">Remaining Years</div>
        <div class="value" style="color:{color}">{remaining:.1f}</div>
        <div class="unit">years from now</div>
    </div>
    <div class="metric-card">
        <div class="label">Current Age</div>
        <div class="value" style="color:#4a5568">{age}</div>
        <div class="unit">years old</div>
    </div>
    <div class="metric-card">
        <div class="label">Health Score</div>
        <div class="value" style="color:{color}">{min(remaining / (90 - age) * 100, 100):.0f}%</div>
        <div class="unit">of ideal remaining</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Gauge chart ──────────────────────────────────────────────────────────────
col_gauge, col_breakdown = st.columns([1, 1], gap="large")

with col_gauge:
    st.markdown('<div class="section-header">Longevity Gauge</div>', unsafe_allow_html=True)

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=predicted_le,
        number={"suffix": " yrs", "font": {"size": 40, "color": color}},
        gauge={
            "axis": {"range": [40, 105], "tickwidth": 1, "tickcolor": "#cbd5e0"},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "#f7fafc",
            "borderwidth": 0,
            "steps": [
                {"range": [40, 65], "color": "#fed7d7"},
                {"range": [65, 75], "color": "#fefcbf"},
                {"range": [75, 85], "color": "#c6f6d5"},
                {"range": [85, 105], "color": "#9ae6b4"},
            ],
        },
    ))
    fig_gauge.update_layout(
        height=320,
        margin=dict(t=40, b=20, l=40, r=40),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter"},
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

# ── Factor impact breakdown ──────────────────────────────────────────────────
with col_breakdown:
    st.markdown('<div class="section-header">Factor Impact Analysis</div>', unsafe_allow_html=True)

    # Compute individual impacts relative to "ideal" profile
    ideal = {
        "age": age, "gender": user_features["gender"], "bmi": 21.0,
        "smoking": 0, "alcohol": 0, "physical_activity": 1, "diet": 1,
        "blood_pressure": 120.0, "cholesterol": 200.0, "chronic_condition": 0,
    }
    ideal_le = predict_life_expectancy(model, ideal)

    factors = {
        "BMI": {**ideal, "bmi": bmi},
        "Smoking": {**ideal, "smoking": int(smoking)},
        "Alcohol": {**ideal, "alcohol": int(alcohol)},
        "Exercise": {**ideal, "physical_activity": int(physical_activity)},
        "Diet": {**ideal, "diet": int(diet)},
        "Blood Pressure": {**ideal, "blood_pressure": float(blood_pressure)},
        "Cholesterol": {**ideal, "cholesterol": float(cholesterol)},
        "Chronic Condition": {**ideal, "chronic_condition": int(chronic_condition)},
    }

    impacts = {}
    for name, feats in factors.items():
        impacts[name] = predict_life_expectancy(model, feats) - ideal_le

    # Sort by absolute impact
    sorted_impacts = sorted(impacts.items(), key=lambda x: x[1])
    labels = [k for k, _ in sorted_impacts]
    values = [v for _, v in sorted_impacts]
    colors = ["#e53e3e" if v < -0.5 else "#38a169" if v > 0.5 else "#a0aec0" for v in values]

    fig_bar = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation="h",
        marker_color=colors,
        marker_line_width=0,
        text=[f"{v:+.1f}" for v in values],
        textposition="outside",
        textfont={"size": 12, "family": "Inter"},
    ))
    fig_bar.update_layout(
        height=320,
        margin=dict(t=20, b=20, l=10, r=50),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            title="Impact (years)",
            zeroline=True,
            zerolinecolor="#cbd5e0",
            gridcolor="#edf2f7",
        ),
        yaxis=dict(automargin=True),
        font={"family": "Inter"},
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Health tips ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Personalised Tips</div>', unsafe_allow_html=True)

tips = []
if smoking:
    tips.append(("🚭", "Quit Smoking", "Eliminating tobacco is the single most impactful change you can make — it can add 5+ years."))
if not physical_activity:
    tips.append(("🏃", "Get Moving", "Aim for 150 minutes of moderate exercise per week to strengthen your heart and mind."))
if not diet:
    tips.append(("🥗", "Improve Your Diet", "Focus on whole foods: vegetables, fruits, lean proteins, and whole grains."))
if alcohol:
    tips.append(("🍷", "Reduce Alcohol", "Limiting alcohol intake can lower blood pressure and reduce cancer risk."))
if bmi > 30:
    tips.append(("⚖️", "Manage Weight", "A BMI over 30 increases risk for many conditions. Small changes add up."))
if blood_pressure > 140:
    tips.append(("💓", "Lower Blood Pressure", "Monitor regularly, reduce sodium, and consult your doctor about management."))
if cholesterol > 240:
    tips.append(("🩺", "Check Cholesterol", "High cholesterol increases heart disease risk. Diet, exercise, and medication can help."))
if chronic_condition:
    tips.append(("💊", "Manage Your Condition", "Work closely with your healthcare team to optimise treatment and outcomes."))

if not tips:
    tips.append(("✨", "Keep It Up!", "Your current lifestyle choices are excellent. Stay consistent for long-term benefits."))

tip_html = '<div class="tip-grid">'
for icon, title, desc in tips:
    tip_html += f"""
    <div class="tip-card">
        <div class="icon">{icon}</div>
        <div class="title">{title}</div>
        <div class="desc">{desc}</div>
    </div>"""
tip_html += "</div>"
st.markdown(tip_html, unsafe_allow_html=True)

# ── Disclaimer ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
    <strong>Disclaimer:</strong> This tool is for educational and illustrative purposes only.
    It uses a synthetic dataset and a simplified model. It is <strong>not</strong> a medical device
    and should not be used for clinical decisions. Always consult a qualified healthcare professional
    for personalised medical advice.
</div>
""", unsafe_allow_html=True)
