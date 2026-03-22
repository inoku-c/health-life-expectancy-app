"""
Life Expectancy Estimator — Evidence-Based Model
=================================================

This module estimates life expectancy using risk coefficients derived from
peer-reviewed epidemiological research. It does NOT use synthetic data.

Data sources and references:
- Base life expectancy: WHO World Health Statistics 2023
  (Japan: M 81.5, F 87.6 / Global: M 70.8, F 75.9)
- Smoking: Doll et al., BMJ 2004 — ~10 years reduction for lifelong smokers
- BMI: Global BMI Mortality Collaboration, Lancet 2016
  — U-shaped curve, optimal BMI 22.5, each 5 kg/m² above → HR 1.29
- Physical activity: Wen et al., Lancet 2011
  — 15 min/day exercise → +3 years; meeting guidelines → +4.5 years
- Diet: Sofi et al., BMJ 2008 (Mediterranean diet meta-analysis)
  — healthy diet → ~4 years reduction in mortality-equivalent
- Alcohol: Wood et al., Lancet 2018
  — heavy drinking → ~2–5 years reduction
- Blood pressure: Lewington et al., Lancet 2002 (Prospective Studies)
  — each 20 mmHg above 115 → doubles CVD risk
- Cholesterol: Emerging Risk Factors Collaboration, Lancet 2009
  — each 1 mmol/L (~39 mg/dL) increase → HR 1.17 for vascular mortality
- Chronic conditions: GBD 2019 study, Lancet 2020
  — diabetes: −6 yrs, heart disease: −7 yrs, average chronic: −5 yrs

This is an educational tool. It is NOT a medical device.
"""


def estimate_life_expectancy(user_features: dict) -> dict:
    """Estimate life expectancy using evidence-based risk coefficients.

    Parameters
    ----------
    user_features : dict
        Keys: age, gender (0=male, 1=female), bmi, smoking (0/1),
        alcohol (0/1), physical_activity (0/1), diet (0/1),
        blood_pressure (systolic mmHg), cholesterol (mg/dL),
        chronic_condition (0/1).

    Returns
    -------
    dict with keys:
        - life_expectancy: float (estimated age at death)
        - remaining_years: float
        - factor_impacts: dict mapping factor name → years impact
        - references: list of source citations
    """
    age = user_features["age"]
    gender = user_features["gender"]  # 0 = male, 1 = female
    bmi = user_features["bmi"]
    smoking = user_features["smoking"]
    alcohol = user_features["alcohol"]
    physical_activity = user_features["physical_activity"]
    diet = user_features["diet"]
    bp = user_features["blood_pressure"]
    chol = user_features["cholesterol"]
    chronic = user_features["chronic_condition"]

    # ── Base life expectancy (WHO 2023, Japan) ──
    # Male: 81.5 years, Female: 87.6 years
    base_le = 81.5 if gender == 0 else 87.6

    factor_impacts = {}

    # ── Smoking (Doll et al., BMJ 2004) ──
    # Lifelong smokers lose ~10 years on average
    # Assuming current smoker: −8 years (some may quit later)
    smoking_impact = -8.0 if smoking else 0.0
    factor_impacts["喫煙"] = smoking_impact

    # ── BMI (Global BMI Mortality Collaboration, Lancet 2016) ──
    # Optimal BMI: 22.5. U-shaped mortality curve.
    # Each 5 kg/m² above 25 → ~30% higher mortality → approx −2.5 yrs per 5 units
    # Below 18.5 (underweight) also increases risk
    optimal_bmi = 22.5
    if bmi < 18.5:
        bmi_impact = -(18.5 - bmi) * 0.8  # underweight penalty
    elif bmi <= 25.0:
        bmi_impact = -abs(bmi - optimal_bmi) * 0.15  # minimal impact in normal range
    else:
        bmi_impact = -(bmi - 25.0) * 0.5  # overweight/obese penalty
    bmi_impact = max(bmi_impact, -12.0)  # cap at −12 years
    factor_impacts["BMI"] = round(bmi_impact, 2)

    # ── Physical activity (Wen et al., Lancet 2011) ──
    # Meeting WHO guidelines (150 min/wk moderate): +4.5 years vs sedentary
    # Not meeting: −2.0 years relative to baseline
    if physical_activity:
        activity_impact = 4.5
    else:
        activity_impact = -2.0
    factor_impacts["運動習慣"] = activity_impact

    # ── Diet (Sofi et al., BMJ 2008; EAT-Lancet 2019) ──
    # Healthy diet adherence: +3.5 years
    # Unhealthy diet: −2.0 years
    if diet:
        diet_impact = 3.5
    else:
        diet_impact = -2.0
    factor_impacts["食生活"] = diet_impact

    # ── Alcohol (Wood et al., Lancet 2018) ──
    # Heavy/frequent drinking: −3.0 years
    alcohol_impact = -3.0 if alcohol else 0.0
    factor_impacts["飲酒"] = alcohol_impact

    # ── Blood pressure (Lewington et al., Lancet 2002) ──
    # Optimal: 115 mmHg. Each 20 mmHg above doubles CVD risk.
    # Approximate life-years impact:
    if bp <= 120:
        bp_impact = 0.0
    elif bp <= 140:
        bp_impact = -(bp - 120) * 0.08  # stage 1: up to −1.6 yrs
    elif bp <= 160:
        bp_impact = -1.6 - (bp - 140) * 0.15  # stage 2: up to −4.6 yrs
    else:
        bp_impact = -4.6 - (bp - 160) * 0.2  # crisis: severe
    bp_impact = max(bp_impact, -10.0)
    factor_impacts["血圧"] = round(bp_impact, 2)

    # ── Cholesterol (Emerging Risk Factors Collaboration, Lancet 2009) ──
    # Optimal: ~200 mg/dL. Each 39 mg/dL above → HR 1.17
    # Approximate: each 39 mg/dL above 200 → −1.2 years
    if chol <= 200:
        chol_impact = 0.0
    else:
        chol_impact = -((chol - 200) / 39.0) * 1.2
    chol_impact = max(chol_impact, -8.0)
    factor_impacts["コレステロール"] = round(chol_impact, 2)

    # ── Chronic condition (GBD 2019, Lancet 2020) ──
    # Average chronic condition: −5 years
    chronic_impact = -5.0 if chronic else 0.0
    factor_impacts["持病"] = chronic_impact

    # ── Calculate total ──
    total_impact = sum(factor_impacts.values())
    life_expectancy = base_le + total_impact

    # Ensure minimum remaining life of 1 year
    life_expectancy = max(life_expectancy, age + 1.0)

    remaining = life_expectancy - age

    references = [
        "WHO World Health Statistics 2023 — 基準平均寿命（日本: 男性81.5歳, 女性87.6歳）",
        "Doll R, et al. BMJ 2004;328:1519 — 喫煙による寿命短縮（約10年）",
        "Global BMI Mortality Collaboration. Lancet 2016;388:776 — BMIと死亡率のU字型曲線",
        "Wen CP, et al. Lancet 2011;378:1244 — 運動による寿命延長（+3〜4.5年）",
        "Sofi F, et al. BMJ 2008;337:a1344 — 健康的食事による死亡率低下",
        "Wood AM, et al. Lancet 2018;391:1513 — 飲酒量と死亡リスク",
        "Lewington S, et al. Lancet 2002;360:1903 — 血圧と心血管疾患リスク",
        "Emerging Risk Factors Collaboration. Lancet 2009;374:1160 — コレステロールと血管死亡率",
        "GBD 2019 Study. Lancet 2020;396:1204 — 慢性疾患の平均寿命への影響",
    ]

    return {
        "life_expectancy": round(life_expectancy, 1),
        "remaining_years": round(remaining, 1),
        "factor_impacts": factor_impacts,
        "base_le": base_le,
        "total_impact": round(total_impact, 1),
        "references": references,
    }
