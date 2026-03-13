import streamlit as st
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

# --------------------
# 指标计算
# --------------------

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

# --------------------
# 分级
# --------------------

def remission_grade(score):

    if score >= 90:
        return "Clinical Remission","green","Asthma fully controlled"

    elif score >= 70:
        return "Controlled Asthma","orange","Symptoms minimal but residual airway inflammation possible"

    else:
        return "Uncontrolled Asthma","red","Active disease requiring treatment optimization"


def airway_grade(index):

    if index >= 60:
        return "Normal Small Airway","green","Small airway flow preserved"

    elif index >= 40:
        return "Mild Small Airway Dysfunction","orange","Early small airway involvement"

    else:
        return "Significant Small Airway Disease","red","Marked small airway obstruction"


def pef_grade(var):

    if var < 10:
        return "Stable Airway","green","Low airway variability"

    elif var < 20:
        return "Moderate Variability","orange","Airway instability present"

    else:
        return "High Variability","red","High exacerbation risk"


rs_label, rs_color, rs_text = remission_grade(rs)
sai_label, sai_color, sai_text = airway_grade(sai)
pv_label, pv_color, pv_text = pef_grade(pv)

# --------------------
# Dashboard
# --------------------

st.header("Clinical Dashboard")

c1,c2,c3 = st.columns(3)

with c1:

    st.metric("Remission Score", round(rs,1))
    st.markdown(f":{rs_color}[{rs_label}]")
    st.write(rs_text)

with c2:

    st.metric("Small Airway Index", round(sai,1))
    st.markdown(f":{sai_color}[{sai_label}]")
    st.write(sai_text)

with c3:

    st.metric("PEF Variability %", round(pv,1))
    st.markdown(f":{pv_color}[{pv_label}]")
    st.write(pv_text)

# --------------------
# 综合判断
# --------------------

st.header("Overall Interpretation")

if rs >= 90 and pv < 10:

    st.success("Asthma in near clinical remission")

elif rs >= 70:

    st.warning("Partially controlled asthma with residual airway dysfunction")

else:

    st.error("Poor asthma control with elevated exacerbation risk")

# --------------------
# AI Doctor Report
# --------------------

st.header("AI Doctor Report")

if rs >= 90:

    severity = "Mild asthma / remission stage"
    plan = """
Continue current therapy.

Step-down consideration:

• Maintain current therapy for 3 months  
• Transition to SMART therapy  
• Monitor PEF weekly
"""

elif rs >= 70:

    severity = "Moderate asthma"

    plan = """
Maintain current therapy.

Recommended actions:

• optimize inhaler technique  
• allergen exposure control  
• reassess lung function in 4 weeks
"""

else:

    severity = "Poorly controlled asthma"

    plan = """
Escalation recommended.

Consider:

• short course systemic steroids  
• specialist consultation  
• biologic therapy assessment
"""

st.write("Severity:",severity)

st.write("Treatment suggestion:")

st.write(plan)

# --------------------
# 缓解概率
# --------------------

st.header("Remission Probability")

prob = min(100, rs - pv)

st.metric("Estimated probability", round(prob,1))
