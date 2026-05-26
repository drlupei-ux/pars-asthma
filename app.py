import streamlit as st
import pytesseract
from PIL import Image
import pdfplumber
import re

from modules.core.clinical_engine import run_pars_engine
from modules.ai.decision_engine import run_decision_engine

st.set_page_config(
    page_title="PARS 哮喘缓解评估系统",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d6a9f 100%);
        padding: 20px 28px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
    }
    .main-header h1 { color: white; font-size: 26px; margin: 0; }
    .main-header p  { color: #b8d4f0; margin: 6px 0 0 0; font-size: 13px; }

    .section-label {
        font-size: 13px;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }

    div[data-testid="metric-container"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px 18px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }

    .risk-box {
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin: 4px 0;
        font-size: 15px;
    }
    .risk-high     { background:#fef2f2; border-left:4px solid #dc2626; }
    .risk-moderate { background:#fffbeb; border-left:4px solid #d97706; }
    .risk-low      { background:#f0fdf4; border-left:4px solid #16a34a; }

    .summary-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 18px 22px;
        line-height: 1.7;
    }
</style>
""", unsafe_allow_html=True)

# ── 页头 ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🫁 PARS 哮喘缓解评估系统</h1>
    <p>肺功能分析 · 小气道评估 · PEF 变异监测 · AI 用药决策</p>
</div>
""", unsafe_allow_html=True)

# ── OCR 上传 ──────────────────────────────────────────────────────────────────
st.subheader("📋 上传肺功能报告")

uploaded_file = st.file_uploader(
    "支持 PDF / PNG / JPG 格式（可选）",
    type=["pdf", "png", "jpg", "jpeg"],
    label_visibility="collapsed"
)

text = ""

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t
    else:
        image = Image.open(uploaded_file)
        col_img, _ = st.columns([1, 3])
        with col_img:
            st.image(image, width=260, caption="已上传图像")
        text = pytesseract.image_to_string(image, lang="chi_sim+eng")

    with st.expander("查看 OCR 识别文本", expanded=False):
        st.text_area("", text, height=140, label_visibility="collapsed")

# ── 解析函数 ──────────────────────────────────────────────────────────────────
def _extract(pattern, text):
    m = re.search(pattern, text, re.IGNORECASE)
    return float(m.group(1)) if m else None


def _parse_report(text):
    fev1  = _extract(r"FEV1[^0-9]*(\d+\.\d+)", text)
    mef25 = _extract(r"MEF25[^0-9]*(\d+\.?\d*)", text)
    mef50 = _extract(r"MEF50[^0-9]*(\d+\.?\d*)", text)
    mef75 = _extract(r"MEF75[^0-9]*(\d+\.?\d*)", text)
    fef25 = _extract(r"FEF25[^0-9]*(\d+\.?\d*)", text)
    fef50 = _extract(r"FEF50[^0-9]*(\d+\.?\d*)", text)
    fef75 = _extract(r"FEF75[^0-9]*(\d+\.?\d*)", text)
    if mef25 is None and fef75:
        mef25 = fef75
    if mef50 is None and fef50:
        mef50 = fef50
    if mef75 is None and fef25:
        mef75 = fef25
    return fev1, mef25, mef50, mef75


# ── 默认值（可被 OCR 覆盖）────────────────────────────────────────────────────
_fev1  = 85.0
_mef25 = 45.0
_mef50 = 55.0
_mef75 = 65.0

if text:
    parsed = _parse_report(text)
    if parsed[0]: _fev1  = parsed[0]
    if parsed[1]: _mef25 = parsed[1]
    if parsed[2]: _mef50 = parsed[2]
    if parsed[3]: _mef75 = parsed[3]

# ── 数据录入 ──────────────────────────────────────────────────────────────────
st.subheader("✏️ 数据录入")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<p class="section-label">肺功能</p>', unsafe_allow_html=True)
    fev1_pct = st.number_input(
        "FEV₁占预计值 (%)",
        min_value=0.0, max_value=150.0,
        value=float(_fev1), step=0.5,
        help="第一秒用力呼气量占预计值百分比"
    )
    st.markdown('<p class="section-label" style="margin-top:12px">症状评分</p>', unsafe_allow_html=True)
    symptom_score = st.slider(
        "日间症状评分（0 = 无症状，10 = 严重）",
        min_value=0, max_value=10, value=2,
        help="根据过去 2 周日间症状频率评分"
    )

with col2:
    st.markdown('<p class="section-label">小气道指标（占预计值 %）</p>', unsafe_allow_html=True)
    mef25 = st.number_input(
        "MEF25%", min_value=0.0, max_value=200.0,
        value=float(_mef25), step=0.5,
        help="25% 肺活量位最大呼气流速"
    )
    mef50 = st.number_input(
        "MEF50%", min_value=0.0, max_value=200.0,
        value=float(_mef50), step=0.5,
        help="50% 肺活量位最大呼气流速"
    )
    mef75 = st.number_input(
        "MEF75%", min_value=0.0, max_value=200.0,
        value=float(_mef75), step=0.5,
        help="75% 肺活量位最大呼气流速"
    )

with col3:
    st.markdown('<p class="section-label">PEF 日间变异</p>', unsafe_allow_html=True)
    pef_am = st.number_input(
        "PEF 早晨 (L/min)",
        min_value=0.0, max_value=900.0,
        value=450.0, step=5.0,
        help="早晨起床后首次测量的峰值呼气流速"
    )
    pef_pm = st.number_input(
        "PEF 下午 (L/min)",
        min_value=0.0, max_value=900.0,
        value=430.0, step=5.0,
        help="下午 4–6 点测量的峰值呼气流速"
    )

st.divider()

# ── 临床引擎计算 ──────────────────────────────────────────────────────────────
engine_out = run_pars_engine({
    "fev1_percent":  fev1_pct,
    "symptom_score": symptom_score,
    "mef25":         mef25,
    "mef50":         mef50,
    "mef75":         mef75,
    "pef_am":        pef_am,
    "pef_pm":        pef_pm,
})

remission_score   = engine_out["remission_score"]
sad_score         = engine_out["small_airway_score"]
pef_variability   = engine_out["pef_variability"]
exacerbation_risk = engine_out["exacerbation_risk"]

decision_out    = run_decision_engine(remission_score, sad_score, pef_variability)
remission_prob  = decision_out["remission_probability"]
med_advice      = decision_out["medication_recommendation"]
ai_summary_text = decision_out["ai_summary"]

# ── 临床仪表盘 ────────────────────────────────────────────────────────────────
st.subheader("📊 临床仪表盘")

m1, m2, m3, m4 = st.columns(4)

with m1:
    label_rs = "临床缓解" if remission_score >= 90 else ("控制良好" if remission_score >= 70 else "未控制")
    st.metric("缓解评分", remission_score,
              delta=label_rs,
              delta_color="normal" if remission_score >= 70 else "inverse")

with m2:
    label_sad = "正常" if sad_score >= 80 else ("轻度受损" if sad_score >= 60 else "明显受损")
    st.metric("小气道评分", sad_score,
              delta=label_sad,
              delta_color="normal" if sad_score >= 60 else "inverse")

with m3:
    label_pef = "稳定" if pef_variability < 10 else ("轻度不稳定" if pef_variability < 20 else "不稳定")
    st.metric("PEF 变异率", f"{pef_variability}%",
              delta=label_pef,
              delta_color="normal" if pef_variability < 10 else "inverse")

with m4:
    label_prob = "高" if remission_prob >= 80 else ("中" if remission_prob >= 60 else "低")
    st.metric("缓解概率", f"{remission_prob}%", delta=f"概率 {label_prob}")

# 急性发作风险
st.markdown("**急性发作风险**")
if exacerbation_risk == "High":
    st.markdown(
        '<div class="risk-box risk-high">🔴 <strong>高风险</strong> — 需要立即升级治疗方案，建议转介专科</div>',
        unsafe_allow_html=True
    )
elif exacerbation_risk == "Moderate":
    st.markdown(
        '<div class="risk-box risk-moderate">🟡 <strong>中等风险</strong> — 密切随访，优化现有方案，4–6 周复诊</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div class="risk-box risk-low">🟢 <strong>低风险</strong> — 继续当前方案，3 个月定期复查</div>',
        unsafe_allow_html=True
    )

st.divider()

# ── AI 医生报告 + 用药建议 ────────────────────────────────────────────────────
col_ai, col_med = st.columns(2)

with col_ai:
    st.subheader("🤖 AI 医生分析")
    st.markdown(f'<div class="summary-box">{ai_summary_text}</div>', unsafe_allow_html=True)

    st.markdown("")

    if remission_score >= 90:
        data = [("疾病阶段", "✅ 临床缓解"), ("气道功能", "✅ 稳定"), ("发作趋势", "✅ 改善")]
    elif remission_score >= 70:
        data = [("疾病阶段", "⚠️ 控制中"), ("气道功能", "⚠️ 轻度受损"), ("发作趋势", "⚠️ 稳定")]
    else:
        data = [("疾病阶段", "❌ 未控制"), ("气道功能", "❌ 受损"), ("发作趋势", "❌ 恶化风险高")]

    tbl = "| 指标 | 状态 |\n|------|------|\n"
    for k, v in data:
        tbl += f"| {k} | {v} |\n"
    st.markdown(tbl)

with col_med:
    st.subheader("💊 用药调整建议")
    st.caption("当前用药：Breztri（布地格福吸入气雾剂）")

    if remission_score >= 90 and sad_score >= 60 and pef_variability < 10:
        st.success(f"""
**{med_advice}**

- ✅ 维持现有治疗至少 3 个月
- ✅ 可考虑转换 SMART 疗法
- ✅ 每 3 个月复查肺功能
""")
    elif remission_score >= 70:
        st.warning(f"""
**{med_advice}**

- ⚠️ 维持现有治疗方案
- ⚠️ 强化吸入技术培训
- ⚠️ 减少过敏原暴露
- ⚠️ 4–6 周后复诊评估
""")
    else:
        st.error(f"""
**{med_advice}**

- ❌ 升级治疗方案（增加剂量或加用 LABA/LAMA）
- ❌ 转介呼吸科专科医生
- ❌ 评估生物制剂适应证
- ❌ 复查吸入技术及依从性
""")
