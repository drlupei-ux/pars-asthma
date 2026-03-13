import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import pytesseract
from PIL import Image
import pdfplumber
import re

st.set_page_config(page_title="PARS Asthma System", layout="wide")

st.title("PARS – Asthma Remission System")

# =========================
# 数据输入方式
# =========================

st.header("Patient Data Input")

input_mode = st.radio(
    "Select Data Input Method",
    ["Manual Input","Upload PDF","Upload Image"]
)

# 默认值
FEV1 = None
MEF25 = None
MEF50 = None
MEF75 = None
PEF_AM = None
PEF_PM = None
symptom = 1


# =========================
# 手工录入
# =========================

if input_mode == "Manual Input":

    c1,c2,c3 = st.columns(3)

    with c1:

        FEV1 = st.number_input("FEV1 (L)",0.5,6.0,2.6,0.1)

        symptom = st.slider("Symptom Score",0,5,1)

    with c2:

        MEF25 = st.number_input("MEF25 (%)",0,100,30)

        MEF50 = st.number_input("MEF50 (%)",0,100,40)

        MEF75 = st.number_input("MEF75 (%)",0,100,50)

    with c3:

        PEF_AM = st.number_input("Morning PEF",100,800,580)

        PEF_PM = st.number_input("Evening PEF",100,800,560)


# =========================
# PDF导入
# =========================

if input_mode == "Upload PDF":

    pdf_file = st.file_uploader("Upload Pulmonary Function Report",type=["pdf"])

    if pdf_file:

        text=""

        with pdfplumber.open(pdf_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:

                    text += page_text

        st.text_area("Extracted Text",text,height=200)


# =========================
# 照片 OCR
# =========================

if input_mode == "Upload Image":

    image_file = st.file_uploader("Upload Report Photo",type=["jpg","jpeg","png"])

    if image_file:

        image = Image.open(image_file)

        st.image(image,width=300)

        text = pytesseract.image_to_string(image,lang="chi_sim+eng")

        st.text_area("OCR Result",text,height=200)


# =========================
# 中国肺功能报告解析
# =========================

def extract_value(pattern,text):

    match = re.search(pattern,text,re.IGNORECASE)

    if match:

        return float(match.group(1))

    return None


def parse_pft(text):

    FEV1 = extract_value(r"FEV1[^0-9]*(\d+\.\d+)",text)

    PEF = extract_value(r"PEF[^0-9]*(\d+\.?\d*)",text)

    MEF25 = extract_value(r"MEF25[^0-9]*(\d+\.?\d*)",text)

    MEF50 = extract_value(r"MEF50[^0-9]*(\d+\.?\d*)",text)

    MEF75 = extract_value(r"MEF75[^0-9]*(\d+\.?\d*)",text)

    FEF25 = extract_value(r"FEF25[^0-9]*(\d+\.?\d*)",text)

    FEF50 = extract_value(r"FEF50[^0-9]*(\d+\.?\d*)",text)

    FEF75 = extract_value(r"FEF75[^0-9]*(\d+\.?\d*)",text)

    MMEF = extract_value(r"MMEF[^0-9]*(\d+\.?\d*)",text)

    FEF2575 = extract_value(r"FEF25[-–]?75[^0-9]*(\d+\.?\d*)",text)

    if MEF25 is None and FEF75:
        MEF25 = FEF75

    if MEF50 is None and FEF50:
        MEF50 = FEF50

    if MEF75 is None and FEF25:
        MEF75 = FEF25

    return FEV1,MEF25,MEF50,MEF75,PEF


# OCR 或 PDF解析
if "text" in locals():

    FEV1,MEF25,MEF50,MEF75,PEF = parse_pft(text)

    st.write("Detected values")

    st.write("FEV1:",FEV1)
    st.write("MEF25:",MEF25)
    st.write("MEF50:",MEF50)
    st.write("MEF75:",MEF75)
    st.write("PEF:",PEF)

    PEF_AM = PEF
    PEF_PM = PEF


# =========================
# 指标计算
# =========================

def remission_score(fev1,symptom):

    score = fev1*30

    score -= symptom*10

    return max(0,min(100,score))


def small_airway_index(m25,m50,m75):

    return (m25+m50+m75)/3


def pef_variability(am,pm):

    return abs(am-pm)/((am+pm)/2)*100


if FEV1 and MEF25 and MEF50 and MEF75:

    RS = remission_score(FEV1,symptom)

    SAI = small_airway_index(MEF25,MEF50,MEF75)

    PV = pef_variability(PEF_AM,PEF_PM)


# =========================
# Dashboard
# =========================

    st.header("Clinical Dashboard")

    c1,c2,c3 = st.columns(3)

    with c1:

        st.metric("Remission Score",round(RS,1))

    with c2:

        st.metric("Small Airway Index",round(SAI,1))

    with c3:

        st.metric("PEF Variability %",round(PV,1))


# =========================
# 分级
# =========================

    if RS>=90:

        st.success("Clinical Remission")

    elif RS>=70:

        st.warning("Controlled Asthma")

    else:

        st.error("Uncontrolled Asthma")


# =========================
# AI Doctor Report
# =========================

    st.header("AI Doctor Report")

    st.write("Severity:",RS)

    st.write("Small airway:",SAI)

    st.write("Airway variability:",PV)


# =========================
# Medication Adjustment
# =========================

    st.header("Medication Adjustment")

    st.write("Current therapy: Breztri")

    if RS>=90:

        st.success("""
Step-down suggestion

maintain therapy 3 months
switch to SMART therapy
""")

    elif RS>=70:

        st.warning("""
Maintain therapy
optimize inhaler technique
""")

    else:

        st.error("""
Escalation needed
specialist review
""")


# =========================
# 趋势图
# =========================

    st.header("Disease Trend")

    trend = pd.DataFrame({

        "Day":[1,2,3,4,5],

        "Remission":[80,85,88,92,RS],

        "SmallAirway":[45,48,52,56,SAI],

        "PEFVar":[15,12,9,6,PV]

    })

    fig = px.line(trend,x="Day",y=["Remission","SmallAirway","PEFVar"])

    st.plotly_chart(fig,use_container_width=True)
