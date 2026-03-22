"""
Healthy Life Expectancy Estimator — Streamlit UI (Japanese)
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go

try:
    from life_expectancy_app import generate_synthetic_dataset, train_model, predict_life_expectancy
except Exception as e:
    st.error(f"Import error: {e}")
    st.stop()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="健康寿命シミュレーター",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS with animations ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700;900&display=swap');
html, body, [class*="css"] {
    font-family: 'Noto Sans JP', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }

/* ── keyframes ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInScale {
    from { opacity: 0; transform: scale(0.9); }
    to   { opacity: 1; transform: scale(1); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%      { transform: translateY(-8px); }
}
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 20px rgba(79, 138, 139, 0.3); }
    50%      { box-shadow: 0 0 40px rgba(79, 138, 139, 0.6); }
}
@keyframes gradient-shift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes particle-float {
    0%   { transform: translateY(0) rotate(0deg); opacity: 0; }
    10%  { opacity: 1; }
    90%  { opacity: 1; }
    100% { transform: translateY(-100vh) rotate(720deg); opacity: 0; }
}

/* ── hero ── */
.hero {
    position: relative;
    background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #0a3d62);
    background-size: 400% 400%;
    animation: gradient-shift 8s ease infinite;
    border-radius: 24px;
    padding: 3.5rem 2.5rem;
    margin-bottom: 2.5rem;
    color: #fff;
    text-align: center;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(circle at 20% 80%, rgba(120, 200, 200, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(100, 180, 255, 0.1) 0%, transparent 50%);
    pointer-events: none;
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 900;
    margin: 0 0 0.5rem 0;
    letter-spacing: 2px;
    animation: fadeInUp 1s ease;
    position: relative;
}
.hero .subtitle {
    font-size: 1.1rem;
    opacity: 0.9;
    margin: 0;
    font-weight: 300;
    animation: fadeInUp 1s ease 0.2s both;
    position: relative;
}
.hero .particles {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    overflow: hidden;
}
.hero .particle {
    position: absolute;
    bottom: -10px;
    width: 6px;
    height: 6px;
    background: rgba(255,255,255,0.3);
    border-radius: 50%;
    animation: particle-float linear infinite;
}
.hero .particle:nth-child(1) { left: 10%; animation-duration: 8s; animation-delay: 0s; width: 4px; height: 4px; }
.hero .particle:nth-child(2) { left: 25%; animation-duration: 12s; animation-delay: 2s; width: 6px; height: 6px; }
.hero .particle:nth-child(3) { left: 40%; animation-duration: 10s; animation-delay: 4s; width: 3px; height: 3px; }
.hero .particle:nth-child(4) { left: 55%; animation-duration: 14s; animation-delay: 1s; width: 5px; height: 5px; }
.hero .particle:nth-child(5) { left: 70%; animation-duration: 9s; animation-delay: 3s; width: 4px; height: 4px; }
.hero .particle:nth-child(6) { left: 85%; animation-duration: 11s; animation-delay: 5s; width: 7px; height: 7px; }
.hero .particle:nth-child(7) { left: 50%; animation-duration: 13s; animation-delay: 6s; width: 3px; height: 3px; }
.hero .particle:nth-child(8) { left: 15%; animation-duration: 15s; animation-delay: 7s; width: 5px; height: 5px; }

/* ── metric cards ── */
.metric-row {
    display: flex;
    gap: 1.2rem;
    margin: 1.5rem 0 2.5rem 0;
    flex-wrap: wrap;
}
.metric-card {
    flex: 1;
    min-width: 160px;
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 1.8rem 1.2rem;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.04);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    animation: fadeInScale 0.8s ease both;
    position: relative;
    overflow: hidden;
}
.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    transition: left 0.6s;
}
.metric-card:hover::after { left: 100%; }
.metric-card:nth-child(1) { animation-delay: 0.1s; }
.metric-card:nth-child(2) { animation-delay: 0.2s; }
.metric-card:nth-child(3) { animation-delay: 0.3s; }
.metric-card:nth-child(4) { animation-delay: 0.4s; }
.metric-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}
.metric-card .emoji { font-size: 1.8rem; margin-bottom: 0.3rem; }
.metric-card .label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #718096;
    font-weight: 600;
}
.metric-card .value {
    font-size: 2.6rem;
    font-weight: 900;
    margin: 0.2rem 0 0.1rem 0;
    line-height: 1.1;
}
.metric-card .unit {
    font-size: 0.8rem;
    color: #a0aec0;
    font-weight: 400;
}

/* ── primary metric (life expectancy) glow ── */
.metric-card.primary {
    animation: fadeInScale 0.8s ease 0.1s both, pulse-glow 3s ease-in-out infinite;
    border: 2px solid rgba(79, 138, 139, 0.3);
}

/* ── sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a202c 0%, #2d3748 100%);
}
section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
section[data-testid="stSidebar"] .stMarkdown h2 {
    color: #fff !important;
    font-weight: 700;
}
section[data-testid="stSidebar"] .stMarkdown h4 {
    color: #90cdf4 !important;
    font-weight: 600;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.1) !important;
}

/* ── section headers ── */
.section-header {
    font-size: 1.2rem;
    font-weight: 700;
    color: #1a202c;
    border-left: 5px solid;
    border-image: linear-gradient(to bottom, #4F8A8B, #2c5364) 1;
    padding-left: 1rem;
    margin: 2.5rem 0 1.2rem 0;
    animation: fadeInUp 0.6s ease both;
}

/* ── disclaimer ── */
.disclaimer {
    background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
    border: 1px solid #fcd34d;
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    font-size: 0.82rem;
    color: #92400e;
    margin-top: 2.5rem;
    line-height: 1.7;
    animation: fadeInUp 0.8s ease both;
}

/* ── tip cards ── */
.tip-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.2rem;
    margin-top: 1.2rem;
}
.tip-card {
    background: linear-gradient(145deg, #ffffff, #f7fafc);
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 1.5rem;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    animation: fadeInUp 0.6s ease both;
    position: relative;
    overflow: hidden;
}
.tip-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #4F8A8B, #2c5364, #4F8A8B);
    background-size: 200% auto;
    animation: shimmer 3s linear infinite;
}
.tip-card:hover {
    transform: translateY(-5px) scale(1.01);
    box-shadow: 0 15px 35px rgba(0,0,0,0.08);
}
.tip-card .icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    animation: float 3s ease-in-out infinite;
}
.tip-card .title {
    font-weight: 700;
    font-size: 0.95rem;
    color: #1a202c;
}
.tip-card .desc {
    font-size: 0.82rem;
    color: #4a5568;
    margin-top: 0.4rem;
    line-height: 1.7;
}

/* ── life timeline ── */
.timeline {
    position: relative;
    padding: 1rem 0;
    margin: 1rem 0;
}
.timeline-bar {
    width: 100%;
    height: 28px;
    border-radius: 14px;
    position: relative;
    overflow: hidden;
}
.timeline-fill {
    height: 100%;
    border-radius: 14px;
    transition: width 1s ease;
    position: relative;
}
.timeline-fill::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    animation: shimmer 2s linear infinite;
    background-size: 200% 100%;
}
.timeline-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 0.5rem;
    font-size: 0.78rem;
    color: #718096;
}
.timeline-marker {
    position: absolute;
    top: -6px;
    width: 3px;
    height: 40px;
    background: #1a202c;
    border-radius: 2px;
    z-index: 2;
}
.timeline-marker-label {
    position: absolute;
    top: -24px;
    transform: translateX(-50%);
    font-size: 0.7rem;
    font-weight: 700;
    color: #1a202c;
    white-space: nowrap;
}

/* ── score ring ── */
.score-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Load / cache model ───────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    with st.spinner("AIモデルを学習中..."):
        df = generate_synthetic_dataset()
        model = train_model(df)
    return model


model = load_model()

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="particles">
        <div class="particle"></div><div class="particle"></div>
        <div class="particle"></div><div class="particle"></div>
        <div class="particle"></div><div class="particle"></div>
        <div class="particle"></div><div class="particle"></div>
    </div>
    <h1>🌿 健康寿命シミュレーター</h1>
    <p class="subtitle">あなたの生活習慣と健康データから、AIが寿命を推定します</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar inputs ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🩺 あなたの健康プロフィール")
    st.caption("下のパラメーターを調整して、あなたの現在の健康状態を入力してください。")

    st.markdown("---")
    st.markdown("#### 👤 基本情報")
    age = st.slider("年齢", 20, 80, 35, help="現在の年齢（歳）")
    gender = st.radio("性別", ["男性", "女性"], horizontal=True)

    st.markdown("---")
    st.markdown("#### 📊 身体データ")
    bmi = st.slider("BMI（体格指数）", 18.0, 40.0, 24.0, 0.1,
                     help="BMI = 体重(kg) ÷ 身長(m)²　｜正常値: 18.5〜24.9")
    blood_pressure = st.slider("最高血圧 (mmHg)", 90, 180, 120,
                                help="最適値: 120 mmHg 未満")
    cholesterol = st.slider("総コレステロール (mg/dL)", 150, 300, 200,
                             help="望ましい値: 200 mg/dL 未満")

    st.markdown("---")
    st.markdown("#### 🏃 生活習慣")
    smoking = st.toggle("喫煙している", value=False, help="現在タバコを吸っている")
    alcohol = st.toggle("頻繁に飲酒する", value=False, help="週に3回以上飲酒する")
    physical_activity = st.toggle("定期的に運動する", value=True,
                                   help="週150分以上の中程度の運動、または週75分以上の激しい運動")
    diet = st.toggle("バランスの良い食事", value=True,
                      help="野菜・果物・全粒穀物・良質なタンパク質を中心とした食事")

    st.markdown("---")
    st.markdown("#### 🏥 既往歴")
    chronic_condition = st.toggle("持病がある", value=False,
                                   help="糖尿病・心臓病・高血圧・喘息などの慢性疾患")

# ── Build feature dict ───────────────────────────────────────────────────────
user_features = {
    "age": age,
    "gender": 0 if gender == "男性" else 1,
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

def le_grade(le: float) -> str:
    if le >= 90:
        return "S"
    if le >= 85:
        return "A"
    if le >= 80:
        return "B"
    if le >= 75:
        return "C"
    if le >= 65:
        return "D"
    return "E"

def le_grade_color(grade: str) -> str:
    return {
        "S": "#805ad5", "A": "#38a169", "B": "#4F8A8B",
        "C": "#d69e2e", "D": "#dd6b20", "E": "#e53e3e",
    }.get(grade, "#718096")

color = le_color(predicted_le)
grade = le_grade(predicted_le)
grade_color = le_grade_color(grade)
health_score = min(remaining / max(90 - age, 1) * 100, 100)

# ── Metric cards ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="metric-row">
    <div class="metric-card primary">
        <div class="emoji">🕊️</div>
        <div class="label">推定寿命</div>
        <div class="value" style="color:{color}">{predicted_le:.1f}</div>
        <div class="unit">歳</div>
    </div>
    <div class="metric-card">
        <div class="emoji">⏳</div>
        <div class="label">残りの人生</div>
        <div class="value" style="color:{color}">{remaining:.1f}</div>
        <div class="unit">年</div>
    </div>
    <div class="metric-card">
        <div class="emoji">🎂</div>
        <div class="label">現在の年齢</div>
        <div class="value" style="color:#4a5568">{age}</div>
        <div class="unit">歳</div>
    </div>
    <div class="metric-card">
        <div class="emoji">🏆</div>
        <div class="label">健康グレード</div>
        <div class="value" style="color:{grade_color}">{grade}</div>
        <div class="unit">スコア {health_score:.0f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Life Timeline ────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🗓️ ライフタイムライン</div>', unsafe_allow_html=True)

life_pct = min(age / predicted_le * 100, 100)
current_pos = min(age / 105 * 100, 100)
predicted_pos = min(predicted_le / 105 * 100, 100)

past_color = "#4F8A8B"
future_color = "#c6f6d5" if predicted_le >= 80 else "#fefcbf" if predicted_le >= 70 else "#fed7d7"

st.markdown(f"""
<div class="timeline">
    <div class="timeline-bar" style="background: #edf2f7;">
        <div class="timeline-fill" style="width: {predicted_pos}%;
            background: linear-gradient(90deg, {past_color} 0%, {past_color} {life_pct}%, {future_color} {life_pct}%, {future_color} 100%);">
        </div>
        <div class="timeline-marker" style="left: {current_pos}%;">
            <div class="timeline-marker-label">📍 現在 {age}歳</div>
        </div>
    </div>
    <div class="timeline-labels">
        <span>0歳</span>
        <span>🎯 推定寿命 {predicted_le:.0f}歳</span>
        <span>105歳</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.caption(f"濃い部分 = 過去（{age}年間）　｜　薄い部分 = 推定される残りの人生（{remaining:.0f}年間）")

# ── Charts row ───────────────────────────────────────────────────────────────
col_gauge, col_radar = st.columns([1, 1], gap="large")

# ── Gauge chart ──────────────────────────────────────────────────────────────
with col_gauge:
    st.markdown('<div class="section-header">📈 寿命ゲージ</div>', unsafe_allow_html=True)

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=predicted_le,
        delta={"reference": 84.0, "suffix": "歳", "increasing": {"color": "#38a169"}, "decreasing": {"color": "#e53e3e"}},
        number={"suffix": " 歳", "font": {"size": 48, "color": color, "family": "Noto Sans JP"}},
        title={"text": "日本人平均寿命 84歳 との比較", "font": {"size": 13, "color": "#718096"}},
        gauge={
            "axis": {"range": [40, 105], "tickwidth": 1, "tickcolor": "#cbd5e0",
                     "tickvals": [40, 50, 60, 70, 80, 90, 100],
                     "ticktext": ["40", "50", "60", "70", "80", "90", "100"]},
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "#f7fafc",
            "borderwidth": 0,
            "steps": [
                {"range": [40, 65], "color": "#fed7d7"},
                {"range": [65, 75], "color": "#fefcbf"},
                {"range": [75, 85], "color": "#c6f6d5"},
                {"range": [85, 105], "color": "#9ae6b4"},
            ],
            "threshold": {
                "line": {"color": "#1a202c", "width": 3},
                "thickness": 0.8,
                "value": 84.0,
            },
        },
    ))
    fig_gauge.update_layout(
        height=340,
        margin=dict(t=60, b=20, l=40, r=40),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Noto Sans JP"},
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

# ── Radar chart ──────────────────────────────────────────────────────────────
with col_radar:
    st.markdown('<div class="section-header">🕸️ 健康バランス</div>', unsafe_allow_html=True)

    # Normalize each factor to 0–100 (100 = best)
    bmi_score = max(0, 100 - abs(bmi - 22) * 8)
    bp_score = max(0, 100 - abs(blood_pressure - 115) * 1.2)
    chol_score = max(0, 100 - abs(cholesterol - 190) * 0.8)
    exercise_score = 90 if physical_activity else 20
    diet_score = 90 if diet else 20
    smoking_score = 95 if not smoking else 10
    alcohol_score = 85 if not alcohol else 30
    condition_score = 90 if not chronic_condition else 25

    categories = ["BMI", "血圧", "コレステロール", "運動", "食事", "禁煙", "節酒", "持病なし"]
    scores = [bmi_score, bp_score, chol_score, exercise_score, diet_score,
              smoking_score, alcohol_score, condition_score]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(79, 138, 139, 0.2)",
        line=dict(color="#4F8A8B", width=2.5),
        marker=dict(size=8, color="#4F8A8B"),
        name="あなた",
    ))
    # Ideal overlay
    fig_radar.add_trace(go.Scatterpolar(
        r=[90]*8 + [90],
        theta=categories + [categories[0]],
        fill="none",
        line=dict(color="#c6f6d5", width=1.5, dash="dot"),
        marker=dict(size=0),
        name="理想値",
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False,
                            gridcolor="rgba(0,0,0,0.06)"),
            angularaxis=dict(gridcolor="rgba(0,0,0,0.06)",
                             tickfont=dict(size=12, family="Noto Sans JP")),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5,
                    font=dict(family="Noto Sans JP")),
        height=360,
        margin=dict(t=30, b=40, l=60, r=60),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Noto Sans JP"},
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# ── Factor impact breakdown ──────────────────────────────────────────────────
st.markdown('<div class="section-header">🔬 各要因のインパクト分析</div>', unsafe_allow_html=True)

ideal = {
    "age": age, "gender": user_features["gender"], "bmi": 21.0,
    "smoking": 0, "alcohol": 0, "physical_activity": 1, "diet": 1,
    "blood_pressure": 120.0, "cholesterol": 200.0, "chronic_condition": 0,
}
ideal_le = predict_life_expectancy(model, ideal)

factors = {
    "BMI（体格指数）": {**ideal, "bmi": bmi},
    "喫煙": {**ideal, "smoking": int(smoking)},
    "飲酒": {**ideal, "alcohol": int(alcohol)},
    "運動習慣": {**ideal, "physical_activity": int(physical_activity)},
    "食生活": {**ideal, "diet": int(diet)},
    "血圧": {**ideal, "blood_pressure": float(blood_pressure)},
    "コレステロール": {**ideal, "cholesterol": float(cholesterol)},
    "持病": {**ideal, "chronic_condition": int(chronic_condition)},
}

impacts = {}
for name, feats in factors.items():
    impacts[name] = predict_life_expectancy(model, feats) - ideal_le

sorted_impacts = sorted(impacts.items(), key=lambda x: x[1])
labels = [k for k, _ in sorted_impacts]
values = [v for _, v in sorted_impacts]
bar_colors = ["#e53e3e" if v < -0.5 else "#38a169" if v > 0.5 else "#a0aec0" for v in values]

fig_bar = go.Figure(go.Bar(
    x=values,
    y=labels,
    orientation="h",
    marker_color=bar_colors,
    marker_line_width=0,
    text=[f"{v:+.1f}年" for v in values],
    textposition="outside",
    textfont={"size": 13, "family": "Noto Sans JP"},
))
fig_bar.update_layout(
    height=380,
    margin=dict(t=10, b=30, l=10, r=60),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(
        title=dict(text="寿命への影響（年）", font=dict(family="Noto Sans JP")),
        zeroline=True,
        zerolinecolor="#cbd5e0",
        zerolinewidth=2,
        gridcolor="#edf2f7",
    ),
    yaxis=dict(automargin=True, tickfont=dict(family="Noto Sans JP", size=13)),
    font={"family": "Noto Sans JP"},
)
st.plotly_chart(fig_bar, use_container_width=True)

# ── Age comparison chart ─────────────────────────────────────────────────────
st.markdown('<div class="section-header">👥 年代別シミュレーション</div>', unsafe_allow_html=True)
st.caption("現在の生活習慣を維持した場合、各年齢での推定寿命はこうなります。")

ages_range = list(range(20, 81, 5))
le_by_age = []
for a in ages_range:
    feats = {**user_features, "age": a}
    le_by_age.append(predict_life_expectancy(model, feats))

fig_age = go.Figure()
fig_age.add_trace(go.Scatter(
    x=ages_range, y=le_by_age,
    mode="lines+markers",
    line=dict(color="#4F8A8B", width=3, shape="spline"),
    marker=dict(size=8, color="#4F8A8B", line=dict(width=2, color="#fff")),
    fill="tozeroy",
    fillcolor="rgba(79, 138, 139, 0.08)",
    name="あなたの推定寿命",
))
# Highlight current age
fig_age.add_trace(go.Scatter(
    x=[age], y=[predicted_le],
    mode="markers+text",
    marker=dict(size=16, color="#e53e3e", symbol="star", line=dict(width=2, color="#fff")),
    text=[f"  現在 {predicted_le:.1f}歳"],
    textposition="top right",
    textfont=dict(size=13, color="#e53e3e", family="Noto Sans JP"),
    name="現在地",
))
# Average line
fig_age.add_hline(y=84, line_dash="dash", line_color="#a0aec0",
                   annotation_text="日本人平均寿命 84歳",
                   annotation_position="top left",
                   annotation=dict(font=dict(size=11, color="#718096", family="Noto Sans JP")))
fig_age.update_layout(
    height=350,
    margin=dict(t=30, b=40, l=50, r=30),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(title=dict(text="入力年齢（歳）", font=dict(family="Noto Sans JP")),
               gridcolor="#edf2f7",
               tickfont=dict(family="Noto Sans JP")),
    yaxis=dict(title=dict(text="推定寿命（歳）", font=dict(family="Noto Sans JP")),
               gridcolor="#edf2f7", range=[50, 105],
               tickfont=dict(family="Noto Sans JP")),
    font={"family": "Noto Sans JP"},
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font=dict(family="Noto Sans JP")),
)
st.plotly_chart(fig_age, use_container_width=True)

# ── Health tips ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">💡 パーソナライズド・アドバイス</div>', unsafe_allow_html=True)

tips = []
if smoking:
    tips.append(("🚭", "禁煙のすすめ",
                 "禁煙は最も効果の大きい健康改善です。寿命を5年以上延ばす可能性があります。禁煙外来の利用も検討してみてください。"))
if not physical_activity:
    tips.append(("🏃", "運動を始めよう",
                 "週150分の中程度の有酸素運動（ウォーキング・水泳など）で、心臓・脳・メンタルヘルスが大幅に改善します。"))
if not diet:
    tips.append(("🥗", "食生活の改善",
                 "野菜・果物・魚・全粒穀物を中心にした食事を心がけましょう。まずは1日1食の置き換えから始めるのがおすすめです。"))
if alcohol:
    tips.append(("🍷", "飲酒量を減らす",
                 "過度な飲酒は血圧上昇やがんリスクの原因になります。休肝日を設けることから始めてみましょう。"))
if bmi > 30:
    tips.append(("⚖️", "体重管理",
                 "BMIが30を超えると様々な疾患リスクが高まります。急激なダイエットより、小さな生活習慣の改善を積み重ねましょう。"))
elif bmi < 18.5:
    tips.append(("⚖️", "体重を増やそう",
                 "BMIが低すぎると免疫力低下や骨粗しょう症のリスクがあります。バランスの良い食事で適正体重を目指しましょう。"))
if blood_pressure > 140:
    tips.append(("💓", "血圧を下げる",
                 "高血圧は「サイレントキラー」と呼ばれます。減塩・運動・ストレス管理を心がけ、定期的に測定しましょう。"))
if cholesterol > 240:
    tips.append(("🩺", "コレステロール管理",
                 "高コレステロールは動脈硬化のリスクを高めます。食事の見直しと定期健診を受けましょう。"))
if chronic_condition:
    tips.append(("💊", "持病の管理",
                 "かかりつけ医と連携し、服薬・生活習慣の管理を徹底することで、健康的な生活を維持できます。"))

if not tips:
    tips.append(("✨", "素晴らしい生活習慣です！",
                 "現在のライフスタイルは非常に理想的です。この習慣を継続して、長く健康な人生を楽しみましょう。"))

tip_html = '<div class="tip-grid">'
for i, (icon, title, desc) in enumerate(tips):
    tip_html += f"""
    <div class="tip-card" style="animation-delay: {i * 0.15}s;">
        <div class="icon">{icon}</div>
        <div class="title">{title}</div>
        <div class="desc">{desc}</div>
    </div>"""
tip_html += "</div>"
st.markdown(tip_html, unsafe_allow_html=True)

# ── Disclaimer ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
    <strong>⚠️ ご注意：</strong>このツールは教育・デモンストレーション目的で作成されています。
    合成データ（人工的に作成されたデータ）と簡易モデルを使用しており、
    <strong>医療機器ではありません</strong>。臨床的な判断には使用しないでください。
    健康に関するご相談は、必ず医療専門家にお問い合わせください。
</div>
""", unsafe_allow_html=True)
