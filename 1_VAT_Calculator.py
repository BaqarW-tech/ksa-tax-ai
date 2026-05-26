"""
VAT Calculator — KSA Tax AI
Page: pages/1_VAT_Calculator.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from utils.vat_logic import (
    calculate_vat_exclusive,
    calculate_vat_inclusive,
    format_sar,
    KSA_VAT_RATE,
)

st.set_page_config(page_title="VAT Calculator | KSA Tax AI", page_icon="🧮", layout="centered")

# ── Styles ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .result-card {
        background: #0f2027;
        border: 1px solid #1e3a4a;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-top: 1rem;
    }
    .result-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #1e3a4a;
        font-size: 1rem;
    }
    .result-row:last-child { border-bottom: none; }
    .result-label { color: #8ba3b0; }
    .result-value { color: #e8f4f8; font-weight: 600; }
    .result-total .result-value { color: #00d4aa; font-size: 1.2rem; }
    .result-vat .result-value  { color: #ffa040; }
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
st.title("🧮 VAT Calculator")
st.markdown('<span class="info-pill">Saudi Arabia · Standard Rate 15% · ZATCA</span>', unsafe_allow_html=True)
st.caption("Calculate VAT for any transaction — add VAT to a net amount, or extract it from a gross price.")

st.divider()

# ── Inputs ───────────────────────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    amount = st.number_input(
        "Enter Amount (SAR)",
        min_value=0.0,
        value=1000.0,
        step=100.0,
        format="%.2f",
        help="Enter the transaction amount in Saudi Riyals."
    )

with col2:
    mode = st.radio(
        "Amount is:",
        options=["Excluding VAT", "Including VAT"],
        help="Excluding: VAT will be added on top.\nIncluding: VAT will be extracted from this amount.",
    )

# ── Calculate ─────────────────────────────────────────────────────────────────
if amount > 0:
    if mode == "Excluding VAT":
        result = calculate_vat_exclusive(amount)
        context = "VAT added on top of your net amount."
    else:
        result = calculate_vat_inclusive(amount)
        context = "VAT extracted from your gross amount."

    # ── Result Card ───────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="result-card">
        <div class="result-row">
            <span class="result-label">Net Amount (excl. VAT)</span>
            <span class="result-value">{format_sar(result.subtotal)}</span>
        </div>
        <div class="result-row result-vat">
            <span class="result-label">VAT ({result.rate_pct})</span>
            <span class="result-value">{format_sar(result.vat_amount)}</span>
        </div>
        <div class="result-row result-total">
            <span class="result-label">Total (incl. VAT)</span>
            <span class="result-value">{format_sar(result.total)}</span>
        </div>
    </div>
    <p style="color:#8ba3b0; font-size:0.82rem; margin-top:0.6rem;">ℹ️ {context}</p>
    """, unsafe_allow_html=True)

    # ── Copy-friendly breakdown ───────────────────────────────────────────────
    with st.expander("📋 Copy-friendly breakdown"):
        st.code(
            f"Net Amount : {format_sar(result.subtotal)}\n"
            f"VAT (15%)  : {format_sar(result.vat_amount)}\n"
            f"Total      : {format_sar(result.total)}",
            language="text"
        )
else:
    st.info("Enter an amount above to see the VAT breakdown.")

# ── Footer note ───────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "⚠️ This tool is for informational purposes only. "
    "For binding tax advice consult a licensed KSA tax professional or visit [zatca.gov.sa](https://zatca.gov.sa)."
)
