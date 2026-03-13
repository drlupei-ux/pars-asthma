import streamlit as st
import pytesseract
from PIL import Image
import pdfplumber
import re

st.set_page_config(page_title="PARS Asthma System", layout="wide")

st.title("PARS – Asthma Remission System")

# ======================
# 数据输入
# ======================

st.header("Patient Data Input")

uploaded_file = st.file_uploader(
    "Upload Pulmonary Function Report",
    type=["pdf","png","jpg","jpeg"]
)

text = ""

# ======================
# OCR读取
# ======================

if uploaded_file:

    if uploaded_file.type == "application/pdf":

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                t = page.extract_text()

                if t:
                    text += t

    else:

        image = Image.open(uploaded_file)

        st.image(image,width=300)

        text = pytesseract.image_to_string(image,lang="chi_sim+eng")

    st.text_area("OCR Result",text,height=200)

# ======================
# 解析函数
# ======================

def extract(pattern,text):

    m = re.search(pattern,text,re.IGNORECASE)

    if m:
        return float(m.group(1))

    return None


def parse(text):

    FEV1 = extract(r"FEV1[^0-9]*(\d+\.\d+)",text)

    MEF25 = extract(r"MEF25[^0-9]*(\d+\.?\d*)",text)

    MEF50 = extract(r"MEF50[^0-9]*(\d+\.?\d*)",text)

    MEF75 = extract(r"MEF75[^0-9]*(\d+\.?\d*)",text)

    FEF25 = extract(r"FEF25[^0-9]*(\d+\.?\d*)",text)

    FEF50 = extract(r"FEF50[^0-9]*(\d+\.?\d*)",text)

    FEF75 = extract(r"FEF75[^0-9]*(\d+\.?\d*)",text)

    PEF = extract(r"PEF[^0-9]*(\d+\.?\d*)",text)

    if MEF25 is None and FEF75:
        MEF25 = FEF75

    if MEF50 is None and FEF50:
        MEF50 = FEF50

    if MEF75 is None and FEF25:
        MEF75 = FEF25

    return FEV1,MEF25,MEF50,MEF75,PEF


# ======================
# 默认值
# ======================

FEV1 = 2.6
MEF25 = 30
MEF50 = 40
MEF75 = 50
PEF = 560
symptom = 1

# ======================
# OCR解析
# ======================

if text:

    p = parse(text)

    if p[0]:
        FEV1,MEF25,MEF50,MEF75,PEF = p

# ======================
# 手动输入备用
# ======================

st.subheader("Manual Adjustment")

c1,c2,c3 = st.columns(3)

with c1:

    FEV1 = st.number_input("FEV1",value=float(FEV1))

with c2:

    MEF25 = st.number_input("MEF25",value=float(MEF25))
    MEF50 = st.number_input("MEF50",value=float(MEF50))
    MEF75 = st.number_input("MEF75",value=float(MEF75))

with c3:

    PEF = st.number_input("PEF",value=float(PEF))

# ======================
# 指标计算
# ======================

RS = FEV1 * 30

SAI = (MEF25 + MEF50 + MEF75) / 3

PV = 0

# ======================
# Dashboard
# ======================

st.header("Clinical Dashboard")

c1,c2,c3 = st.columns(3)

with c1:

    st.metric("Remission Score",round(RS,1))

with c2:

    st.metric("Small Airway Index",round(SAI,1))

with c3:

    st.metric("PEF Variability %",round(PV,1))

# ======================
# Interpretation
# ======================

if RS >= 90:

    st.success("Asthma close to clinical remission")

elif RS >= 70:

    st.warning("Controlled Asthma")

else:

    st.error("Uncontrolled Asthma")

# ======================
# AI Doctor Report
# ======================

st.header("AI Doctor Report")

if RS >= 90:

    severity = "Mild asthma"
    trend = "Improving"
    interpretation = "Airway stable with high remission probability"

elif RS >= 70:

    severity = "Moderate asthma"
    trend = "Stable"
    interpretation = "Residual small airway dysfunction"

else:

    severity = "Severe asthma"
    trend = "Worsening"
    interpretation = "High risk of exacerbation"

st.write("Severity:",severity)
st.write("Trend:",trend)
st.write("Interpretation:",interpretation)

# ======================
# Medication
# ======================

st.header("Medication Adjustment")

st.write("Current therapy: Breztri")

if RS >= 90:

    st.success("""
Suggested step-down plan

Maintain therapy for 3 months  
Consider SMART therapy
""")

elif RS >= 70:

    st.warning("""
Maintain therapy

Optimize inhaler technique  
Control allergens
""")

else:

    st.error("""
Escalation needed

Specialist consultation  
Consider biologic therapy
""")
