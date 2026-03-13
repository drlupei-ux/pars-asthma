import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="PARS Asthma System", layout="wide")

st.title("PARS – Asthma Remission System")

# 示例数据
data = {
    "PEF_AM":580,
    "PEF_PM":560,
    "FEV1":2.6,
    "MEF25":30,
    "MEF50":40,
    "MEF75":50,
    "symptom":1
}

# ----------------------
# 指标计算
# ----------------------

def remission_score(fev1, symptom):
    score = fev1 * 30
    score -= symptom * 10
    return max(0, min(100, score))

def small_airway_index(mef25, mef50, mef75):
    return (mef25 + mef50 + mef75)/3

def pef_variability(am, pm):
    return abs(am-pm)/((am+pm)/2)*100


rs = remission_score(data["FEV1"], data["symptom"])
sai = small_airway_index(data["MEF25"], data["MEF50"], data["MEF75"])
pv = pef_variability(data["PEF_AM"], data["PEF_PM"])


# ----------------------
# 指标分级函数
# ----------------------

def remission_level(score):

    if score >= 90:
        return "Clinical Remission", "green"

    elif score >= 70:
        return "Controlled Asthma", "orange"

    else:
        return "Uncontrolled Asthma", "red"



def airway_level(index):

    if index >= 60:
        return "Normal small airway", "green"

    elif index >= 40:
        return "Mild small airway dysfunction", "orange"

    else:
        return "Significant small airway disease", "red"



def pef_level(var):

    if var < 10:
        return "Stable airway", "green"

    elif var < 20:
        return "Moderate variability", "orange"

    else:
        return "High airway variability", "red"


rs_level, rs_color = remission_level(rs)
sai_level, sai_color = airway_level(sai)
pv_level, pv_color = pef_level(pv)

# ----------------------
# Dashboard
# ----------------------

st.header("Dashboard")

c1,c2,c3 = st.columns(3)

with c1:

    st.metric("Remission Score",round(rs,1))
    st.markdown(f":{rs_color}[{rs_level}]")
    st.caption("综合症状+肺功能评估整体缓解程度")

with c2:

    st.metric("Small Airway Index",round(sai,1))
    st.markdown(f":{sai_color}[{sai_level}]")
    st.caption("MEF25/50/75平均值评估小气道")

with c3:

    st.metric("PEF Variability %",round(pv,1))
    st.markdown(f":{pv_color}[{pv_level}]")
    st.caption("日峰流速变异率反映气道稳定性")


# ----------------------
# Interpretation
# ----------------------

st.header("Interpretation")

if rs >= 90 and pv < 10:

    st.success("Asthma close to clinical remission")

elif rs >= 70:

    st.warning("Asthma partially controlled")

else:

    st.error("Poor asthma control detected")


# ----------------------
# AI Doctor Report
# ----------------------

st.header("AI Doctor Report")

if rs >= 90 and pv < 10:

    severity = "Mild asthma / near remission"
    trend = "Improving"
    interpretation = "Airway stability good with low variability."

elif rs >= 70:

    severity = "Moderate asthma"
    trend = "Stable but residual airway dysfunction"
    interpretation = "Small airway abnormality persists."

else:

    severity = "Poorly controlled asthma"
    trend = "Risk of exacerbation"
    interpretation = "High airway variability detected."

st.write(f"Severity: {severity}")
st.write(f"Trend: {trend}")
st.write(f"Interpretation: {interpretation}")


# ----------------------
# Medication Adjustment
# ----------------------

st.header("Medication Adjustment")

st.write("Current therapy: Budesonide/Glycopyrrolate/Formoterol (Breztri)")


if rs >= 90 and pv < 10:

    st.success("""

Suggested step-down plan:

• Maintain Breztri for 3 months  
• Step down to Budesonide/Formoterol SMART therapy  
• Monitor PEF weekly  
• Repeat lung function in 3 months

""")

elif rs >= 70:

    st.warning("""

Maintain current therapy.

Suggested actions:

• optimize inhaler technique  
• check allergen exposure  
• repeat lung function in 4 weeks

""")

else:

    st.error("""

Escalation needed.

Consider:

• short course oral corticosteroid  
• specialist review  
• biologic therapy evaluation

""")


# ----------------------
# Remission Probability
# ----------------------

st.header("Remission Probability")

prob = min(100, rs - pv)

st.metric("Probability %",round(prob,1))
