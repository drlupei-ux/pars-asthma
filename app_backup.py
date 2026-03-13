import streamlit as st
import pandas as pd
import pytesseract
import pdfplumber
from PIL import Image
import os
import re
from datetime import datetime

DATA_FILE="asthma_data.csv"

st.set_page_config(
    page_title="Asthma Remission System",
    layout="centered"
)

st.title("AI Asthma Remission System")

# 初始化数据库
if not os.path.exists(DATA_FILE):

    df=pd.DataFrame(columns=[
        "date",
        "PEF_AM",
        "PEF_PM",
        "FEV1",
        "MEF25",
        "MEF50",
        "MEF75",
        "symptom",
        "source"
    ])

    df.to_csv(DATA_FILE,index=False)

df=pd.read_csv(DATA_FILE)

# 侧边栏
page=st.sidebar.selectbox(
"Menu",
[
"Dashboard",
"Add Data",
"Upload Report",
"Records"
]
)

# =========================
# DASHBOARD
# =========================

if page=="Dashboard":

    st.header("Asthma Status")

    if len(df)>0:

        latest=df.iloc[-1]

        pef_am=latest["PEF_AM"]
        pef_pm=latest["PEF_PM"]

        if pef_am and pef_pm:

            variability=abs(pef_am-pef_pm)/((pef_am+pef_pm)/2)

        else:

            variability=0

        small_airway=(

            latest["MEF25"]+
            latest["MEF50"]+
            latest["MEF75"]

        )/3

        fev1=latest["FEV1"]

        symptom=latest["symptom"]

        # Remission Engine
        inflammation_score=(1-symptom/3)*25
        stability_score=(1-variability)*25
        small_airway_score=(small_airway/70)*25
        lung_function_score=(fev1/3)*25

        remission_score=(
            inflammation_score+
            stability_score+
            small_airway_score+
            lung_function_score
        )

        # 卡片
        col1,col2,col3=st.columns(3)

        col1.metric(
        "Remission Score",
        round(remission_score,1)
        )

        col2.metric(
        "PEF Variability",
        str(round(variability*100,1))+"%"
        )

        col3.metric(
        "Small Airway Index",
        round(small_airway,1)
        )

        # -----------------------
        # Interpretation
        # -----------------------

        st.subheader("Clinical Interpretation")

        if remission_score>85:

            st.success("Asthma near clinical remission")

        elif remission_score>70:

            st.info("Asthma well controlled")

        elif remission_score>50:

            st.warning("Partially controlled asthma")

        else:

            st.error("Uncontrolled asthma")

        # -----------------------
        # Trajectory
        # -----------------------

        st.subheader("Trajectory")

        if len(df)>=5:

            trend=df.tail(5)

            trend["SmallAirway"]=(
                trend["MEF25"]+
                trend["MEF50"]+
                trend["MEF75"]
            )/3

            if trend["SmallAirway"].is_monotonic_increasing:

                trajectory="Improving"

            elif trend["SmallAirway"].is_monotonic_decreasing:

                trajectory="Deteriorating"

            else:

                trajectory="Stable"

        else:

            trajectory="Insufficient data"

        st.write("Trajectory:",trajectory)

        # -----------------------
        # Medication Adjustment
        # -----------------------

        st.subheader("Medication Adjustment")

        advice=""

        if remission_score>85:

            advice="""
Maintain current therapy.

If stability persists for 3–6 months,
gradual therapy step-down may be considered.
"""

        elif remission_score>70:

            advice="""
Continue current Breztri therapy.

Monitor airway stability and symptoms.
"""

        elif remission_score>50:

            advice="""
Optimize anti-inflammatory control.

Check inhaler technique and adherence.
"""

        else:

            advice="""
Asthma not well controlled.

Evaluate adherence and consider specialist assessment.
"""

        if small_airway<50:

            advice+= """

Small airway dysfunction detected.
Consider therapies targeting distal airways.
"""

        st.info(advice)

        # -----------------------
        # Trend
        # -----------------------

        st.subheader("Recovery Trend")

        df["SmallAirway"]=(
            df["MEF25"]+
            df["MEF50"]+
            df["MEF75"]
        )/3

        st.line_chart(
        df[
        [
        "FEV1",
        "PEF_AM",
        "SmallAirway"
        ]
        ])

    else:

        st.info("No data yet")

# =========================
# ADD DATA
# =========================

if page=="Add Data":

    st.header("Manual Entry")

    pef_am=st.number_input("PEF AM",value=0)
    pef_pm=st.number_input("PEF PM",value=0)

    fev1=st.number_input("FEV1",value=0.0)

    mef25=st.number_input("MEF25",value=0.0)
    mef50=st.number_input("MEF50",value=0.0)
    mef75=st.number_input("MEF75",value=0.0)

    symptom=st.slider("Symptom Score",0,3)

    if st.button("Save Data"):

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

# =========================
# OCR UPLOAD
# =========================

if page=="Upload Report":

    st.header("Upload Medical Report")

    file=st.file_uploader(
    "Upload PDF or Image",
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

        def find(patterns):

            for p in patterns:

                m=re.search(p+r"\s*[:：]?\s*([\d\.]+)",text)

                if m:

                    return float(m.group(1))

            return None

        fev1=find(["FEV1"])
        mef25=find(["MEF25","FEF25"])
        mef50=find(["MEF50","FEF50"])
        mef75=find(["MEF75","FEF75"])

        st.write("Extracted Values")

        st.write("FEV1:",fev1)
        st.write("MEF25:",mef25)
        st.write("MEF50:",mef50)
        st.write("MEF75:",mef75)

# =========================
# RECORDS
# =========================

if page=="Records":

    st.header("Records")

    st.dataframe(df)
