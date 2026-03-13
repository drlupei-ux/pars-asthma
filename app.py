import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="PARS Asthma System", layout="wide")

st.title("PARS – Asthma Remission System")

# ---------- 示例数据 ----------
data = {
    "PEF_AM":580,
    "PEF_PM":560,
    "FEV1":2.6,
    "MEF25":30,
    "MEF50":40,
    "MEF75":50,
    "symptom":1
}

# ---------- 计算指标 ----------

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

# ---------- Dashboard ----------
col1,col2,col3 = st.columns(3)

with col1:
    st.metric("Remission Score",round(rs,1))
    st.caption("综合症状+肺功能评估哮喘缓解程度")

with col2:
    st.metric("Small Airway Index",round(sai,1))
    st.caption("小气道功能指标（MEF25/50/75平均）")

with col3:
    st.metric("PEF Variability %",round(pv,1))
    st.caption("峰流速日变异率，反映气道稳定性")

# ---------- Interpretation ----------
st.header("Interpretation")

if rs > 90:
    st.success("Asthma close to clinical remission")
elif rs > 70:
    st.warning("Partially controlled asthma")
else:
    st.error("Poor asthma control")

# ---------- AI Doctor Report ----------

st.header("AI Doctor Report")

if rs > 90 and pv < 10:
    severity = "Mild asthma / near remission"
    trend = "Improving"
    interpretation = "Disease control stable with minimal variability."
else:
    severity = "Moderate asthma"
    trend = "Unstable"
    interpretation = "Airway variability detected."

st.write(f"Severity: {severity}")
st.write(f"Trend: {trend}")
st.write(f"Interpretation: {interpretation}")

# ---------- Medication Adjustment ----------

st.header("Medication Adjustment")

st.write("Current therapy: Budesonide/Glycopyrrolate/Formoterol (Breztri)")

if rs > 90 and pv < 10:
    st.success("""
Suggested step-down strategy:

1. Maintain current therapy for 3 months
2. Step down to Budesonide/Formoterol SMART therapy
3. Monitor PEF variability weekly
""")
else:
    st.warning("""
Maintain current therapy.

Consider:
- inhaler technique review
- allergen control
- repeat lung function in 4 weeks
""")

# ---------- Remission Probability ----------

st.header("Remission Probability")

prob = min(100, rs - pv)

st.metric("Probability %", round(prob,1))
