import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PARS Asthma System", layout="wide")

st.title("PARS – Asthma Remission System")

# -----------------------
# 示例数据
# -----------------------

PEF_AM = 580
PEF_PM = 560
FEV1 = 2.6
MEF25 = 30
MEF50 = 40
MEF75 = 50
symptom = 1

# -----------------------
# 指标计算
# -----------------------

def remission_score(fev1, symptom):

    score = fev1 * 30
    score -= symptom * 10

    return max(0, min(100, score))


def small_airway_index(m25, m50, m75):

    return (m25 + m50 + m75) / 3


def pef_variability(am, pm):

    return abs(am - pm) / ((am + pm) / 2) * 100


RS = remission_score(FEV1, symptom)
SAI = small_airway_index(MEF25, MEF50, MEF75)
PV = pef_variability(PEF_AM, PEF_PM)

# -----------------------
# 分级
# -----------------------

def remission_grade(x):

    if x >= 90:
        return "Clinical Remission", "green", "哮喘临床缓解"

    elif x >= 70:
        return "Controlled", "orange", "哮喘基本控制"

    else:
        return "Uncontrolled", "red", "哮喘控制不佳"


def airway_grade(x):

    if x >= 60:
        return "Normal", "green", "小气道正常"

    elif x >= 40:
        return "Mild dysfunction", "orange", "轻度小气道异常"

    else:
        return "Significant disease", "red", "明显小气道病变"


def pef_grade(x):

    if x < 10:
        return "Stable airway", "green", "气道稳定"

    elif x < 20:
        return "Moderate variability", "orange", "气道波动"

    else:
        return "High variability", "red", "急性发作风险增加"


RS_label, RS_color, RS_mean = remission_grade(RS)
SAI_label, SAI_color, SAI_mean = airway_grade(SAI)
PV_label, PV_color, PV_mean = pef_grade(PV)

# -----------------------
# 指标卡片
# -----------------------

st.header("Clinical Dashboard")

c1, c2, c3 = st.columns(3)

with c1:

    st.metric("Remission Score", round(RS,1))
    st.markdown(f":{RS_color}[{RS_label}]")
    st.write(RS_mean)

with c2:

    st.metric("Small Airway Index", round(SAI,1))
    st.markdown(f":{SAI_color}[{SAI_label}]")
    st.write(SAI_mean)

with c3:

    st.metric("PEF Variability %", round(PV,1))
    st.markdown(f":{PV_color}[{PV_label}]")
    st.write(PV_mean)

# -----------------------
# 趋势图
# -----------------------

st.header("Disease Trend")

trend = pd.DataFrame({
    "Day":[1,2,3,4,5,6,7],
    "Remission":[82,85,87,90,92,94,96],
    "SmallAirway":[48,50,52,55,58,60,61],
    "PEFVar":[14,12,11,9,7,5,3]
})

fig = px.line(trend, x="Day", y=["Remission","SmallAirway","PEFVar"])

st.plotly_chart(fig, use_container_width=True)

# -----------------------
# 雷达图
# -----------------------

st.header("Airway Health Radar")

radar = pd.DataFrame(dict(
    r=[RS,SAI,100-PV,80,75],
    theta=[
        "Remission",
        "Small Airway",
        "Airway Stability",
        "Symptom Control",
        "Lung Function"
    ]
))

fig2 = px.line_polar(radar, r='r', theta='theta', line_close=True)

st.plotly_chart(fig2)

# -----------------------
# AI Doctor Report
# -----------------------

st.header("AI Doctor Report")

if RS >= 90 and PV < 10:

    st.success("Asthma near clinical remission")

elif RS >= 70:

    st.warning("Asthma partially controlled")

else:

    st.error("Poor asthma control")

st.write("Severity:", RS_label)
st.write("Small airway:", SAI_label)
st.write("Airway variability:", PV_label)

# -----------------------
# 用药建议
# -----------------------

st.header("Medication Adjustment")

st.write("Current therapy: Budesonide / Glycopyrrolate / Formoterol")

if RS >= 90:

    st.success("""
Step-down suggestion

• maintain therapy 3 months
• consider SMART therapy
• repeat lung function
""")

elif RS >= 70:

    st.warning("""
Maintain therapy

• optimize inhaler technique
• allergen control
""")

else:

    st.error("""
Escalation recommended

• specialist review
• consider biologic therapy
""")

# -----------------------
# 缓解概率
# -----------------------

st.header("Remission Probability")

prob = min(100, RS - PV)

st.metric("Probability %", round(prob,1))
