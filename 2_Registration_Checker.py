"""
VAT Registration Checker — KSA Tax AI
Page: pages/2_Registration_Checker.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from utils.vat_logic import (
    check_registration_status,
    RegistrationStatus,
    format_sar,
    MANDATORY_THRESHOLD,
    VOLUNTARY_THRESHOLD,
)

st.set_page_config(page_title="Registration Checker | KSA Tax AI", page_icon="📋", layout="centered")

# ── Styles ───────────────────────────────────────────────────────────────────
STATUS_COLORS = {
    RegistrationStatus.MANDATORY:    ("#ff4b4b", "#2d1010", "🚨"),
    RegistrationStatus.VOLUNTARY:    ("#ffa040", "#2d1f0a", "⚡"),
    RegistrationStatus.NOT_REQUIRED: ("#00d4aa", "#0a2d26", "✅"),
}

st.markdown("""
<style>
    .status-card {
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-top: 1rem;
    }
    .status-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 0.5rem; }
    .status-explanation { font-size: 0.95rem; line-height: 1.6; margin-bottom: 1rem; }
    .status-action {
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 0.9rem;
        font-weight: 500;
    }
    .threshold-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
    .threshold-table th {
        background: #1e3a4a;
        color: #8ba3b0;
        padding: 0.5rem 0.75rem;
        text-align: left;
    }
    .threshold-table td {
        padding: 0.5rem 0.75rem;
        border-bottom: 1px solid #1e3a4a;
        color: #e8f4f8;
    }
    .info-pill {
        display: inline-block;
        background: #1e3a4a;
        color: #8ba3b0;
        border-radius: 20px;
        padding: 0.2rem 0.8rem;
        font-size: 0.8rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.title("📋 VAT Registration Checker")
st.markdown('<span class="info-pill">Saudi Arabia · ZATCA Thresholds · VAT Implementing Regulations</span>', unsafe_allow_html=True)
st.caption("Find out whether your business is required — or eligible — to register for VAT in KSA.")

st.divider()

# ── Input ─────────────────────────────────────────────────────────────────────
annual_revenue = st.number_input(
    "Annual Taxable Supplies / Revenue (SAR)",
    min_value=0.0,
    value=300_000.0,
    step=10_000.0,
    format="%.0f",
    help=(
        "Enter your total annual taxable supplies in SAR. "
        "This includes standard-rated and zero-rated supplies, but excludes exempt supplies."
    ),
)

st.caption(f"You entered: **{format_sar(annual_revenue)}** per year")

# ── Result ────────────────────────────────────────────────────────────────────
if annual_revenue >= 0:
    result = check_registration_status(annual_revenue)
    color, bg, icon = STATUS_COLORS[result.status]

    st.markdown(f"""
    <div class="status-card" style="background:{bg}; border: 1px solid {color}33;">
        <div class="status-title" style="color:{color};">{icon} {result.label}</div>
        <div class="status-explanation" style="color:#c8dde6;">{result.explanation}</div>
        <div class="status-action" style="background:{color}22; color:{color}; border: 1px solid {color}44;">
            👉 {result.action}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Revenue gauge ─────────────────────────────────────────────────────────
    st.markdown("#### Where you stand")
    progress_max = MANDATORY_THRESHOLD * 1.5
    pct = min(annual_revenue / progress_max, 1.0)
    mandatory_pct = MANDATORY_THRESHOLD / progress_max
    voluntary_pct = VOLUNTARY_THRESHOLD / progress_max

    st.progress(pct)
    col1, col2, col3 = st.columns(3)
    col1.metric("Your Revenue", format_sar(annual_revenue))
    col2.metric("Voluntary Threshold", format_sar(VOLUNTARY_THRESHOLD))
    col3.metric("Mandatory Threshold", format_sar(MANDATORY_THRESHOLD))

# ── Reference table ───────────────────────────────────────────────────────────
st.divider()
with st.expander("📖 ZATCA Registration Threshold Reference"):
    st.markdown("""
    <table class="threshold-table">
        <tr>
            <th>Scenario</th>
            <th>Annual Taxable Supplies</th>
            <th>Obligation</th>
        </tr>
        <tr>
            <td>🚨 Mandatory</td>
            <td>≥ SAR 375,000</td>
            <td>Must register for VAT</td>
        </tr>
        <tr>
            <td>⚡ Voluntary</td>
            <td>SAR 187,500 – SAR 374,999</td>
            <td>May register voluntarily</td>
        </tr>
        <tr>
            <td>✅ Not Required</td>
            <td>< SAR 187,500</td>
            <td>No registration needed</td>
        </tr>
    </table>
    <p style="color:#8ba3b0; font-size:0.82rem; margin-top:0.75rem;">
    Source: VAT Implementing Regulations, ZATCA. Thresholds apply to annual taxable supplies 
    (standard-rated + zero-rated). Exempt supplies are excluded from the calculation.
    </p>
    """, unsafe_allow_html=True)

st.divider()
st.caption(
    "⚠️ This tool is for informational purposes only. "
    "For binding advice consult a licensed KSA tax professional or visit [zatca.gov.sa](https://zatca.gov.sa)."
)
