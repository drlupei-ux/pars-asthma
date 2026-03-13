import streamlit as st
import pandas as pd
import pytesseract
import pdfplumber
from PIL import Image
import re
import os
from datetime import datetime

DATA_FILE="asthma_data.csv"

st.set_page_config(
    page_title="PARS Asthma",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("PARS – Asthma Remission System")

# ---------------------------
# 数据初始化
# ---------------------------

if not os.path.exists(DATA_FILE):

    df=pd.DataFrame(columns=[
        "date","PEF_AM","PEF_PM",
        "FEV1","MEF25","MEF50","MEF75",
        "symptom","source"
    ])

    df.to_csv(DATA_FILE,index=False)

df=pd.read_csv(DATA_FILE)

# ---------------------------
# Dashboard
# ---------------------------

st.header("Dashboard")

if len(df)>0:

    latest=df.iloc[-1]

    pef_am=latest["PEF_AM"]
    pef_pm=latest["PEF_PM"]

    if pef_am>0 and pef_pm>0:
        variability=abs(pef_am-pef_pm)/((pef_am+pef_pm)/2)
    else:
        variability=0

    small_airway=(
        latest["MEF25"]+
        latest["MEF50"]+
        latest["MEF75"]
    )/3

    remission=(
        40*(1-latest["symptom"]/3)+
        30*(1-variability)+
        20*(small_airway/70)+
        10*(latest["FEV1"]/3)
    )

    col1,col2,col3=st.columns(3)

    col1.metric("Remission Score",round(remission,1))
    col2.metric("Small Airway Index",round(small_airway,1))
    col3.metric("PEF Variability %",round(variability*100,1))

# ---------------------------
# 指标含义
# ---------------------------

st.subheader("Interpretation")

if remission>85:
    st.success("Asthma close to clinical remission")

elif remission>70:
    st.info("Asthma well controlled")

elif remission>50:
    st.warning("Partially controlled asthma")

else:
    st.error("Uncontrolled asthma")

if small_airway<50:
    st.warning("Small airway dysfunction detected")

# ---------------------------
# Clinical Assessment
# ---------------------------

st.header("AI Doctor Report")

severity=""

if remission>80:
    severity="Mild asthma"

elif remission>60:
    severity="Moderate asthma"

else:
    severity="Poorly controlled asthma"

trend="stable"

if len(df)>4:

    trend_data=df.tail(5)

    if trend_data["MEF25"].is_monotonic_increasing:
        trend="improving"

    elif trend_data["MEF25"].is_monotonic_decreasing:
        trend="worsening"

report=f"""
Severity: {severity}

Trend: {trend}

Interpretation:
Persistent small airway dysfunction may reduce remission probability.
"""

st.write(report)

# ---------------------------
# Remission Probability
# ---------------------------

prob=(
0.35*(1-latest["symptom"]/3)+
0.30*(1-variability)+
0.20*(small_airway/70)+
0.15*(latest["FEV1"]/3)
)

probability=prob*100

st.header("Remission Probability")

st.metric("Probability %",round(probability,1))

# ---------------------------
# Medication Adjustment
# ---------------------------

st.header("Medication Adjustment")

if remission>85:

    st.success(
    "Maintain current Breztri therapy. "
    "If stable for 3–6 months consider step-down."
    )

elif remission>70:

    st.info(
    "Continue Breztri therapy. "
    "Monitor airway stability."
    )

elif remission>50:

    st.warning(
    "Optimize anti-inflammatory control. "
    "Evaluate inhaler technique."
    )

else:

    st.error(
    "Poor control. Consider therapy escalation "
    "and inflammatory phenotype evaluation."
    )

if small_airway<50:

    st.warning(
    "Small airway dysfunction present. "
    "Consider therapies targeting distal airways."
    )

# ---------------------------
# Trend
# ---------------------------

st.header("Recovery Trend")

if len(df)>0:

    df["SmallAirway"]=(
        df["MEF25"]+
        df["MEF50"]+
        df["MEF75"]
    )/3

    st.line_chart(df[["PEF_AM","FEV1","SmallAirway"]])

# ---------------------------
# Data Input
# ---------------------------

st.header("Add Data")

tab1,tab2=st.tabs(["Manual","Report Upload"])

# 手工输入

with tab1:

    pef_am=st.number_input("PEF AM",0)
    pef_pm=st.number_input("PEF PM",0)

    fev1=st.number_input("FEV1",0.0)

    mef25=st.number_input("MEF25",0.0)
    mef50=st.number_input("MEF50",0.0)
    mef75=st.number_input("MEF75",0.0)

    symptom=st.slider("Symptom",0,3)

    if st.button("Save"):

        new={

            "date":datetime.now(),
            "PEF_AM":pef_am,
            "PEF_PM":pef_pm,
            "FEV1":fev1,
            "MEF25":mef25,
            "MEF50":mef50,
            "MEF75":mef75,
            "symptom":symptom,
            "source":"manual"

        }

        df=pd.concat([df,pd.DataFrame([new])],ignore_index=True)

        df.to_csv(DATA_FILE,index=False)

        st.success("Saved")

# OCR

def find_value(patterns,text):

    for p in patterns:

        m=re.search(p+r"\s*[:：]?\s*([\d\.]+)",text)

        if m:

            return float(m.group(1))

    return None

with tab2:

    file=st.file_uploader(
        "Upload report",
        type=["pdf","png","jpg","jpeg"]
    )

    if file:

        text=""

        if file.type=="application/pdf":

            with pdfplumber.open(file) as pdf:

                for page in pdf.pages:

                    t=page.extract_text()

                    if t:
                        text+=t

        else:

            img=Image.open(file)

            text=pytesseract.image_to_string(
                img,
                lang="chi_sim+eng"
            )

        st.text_area("OCR Result",text)

        fev1=find_value(["FEV1"],text)

        mef25=find_value(["MEF25","FEF25"],text)
        mef50=find_value(["MEF50","FEF50"],text)
        mef75=find_value(["MEF75","FEF75"],text)

        st.write("Extracted")

        st.write("FEV1:",fev1)
        st.write("MEF25:",mef25)
        st.write("MEF50:",mef50)
        st.write("MEF75:",mef75)
