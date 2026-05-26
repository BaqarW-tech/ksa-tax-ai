"""
VAT Calculator — KSA Tax AI
Mobile-friendly: slider + text input instead of number_input
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from utils.vat_logic import calculate_vat_exclusive, calculate_vat_inclusive, format_sar

st.set_page_config(page_title="VAT Calculator | KSA Tax AI", page_icon="🧮", layout="centered")

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
        padding: 0.5rem 0;
        border-bottom: 1px solid #1e3a4a;
    }
    .result-row:last-child { border-bottom: none; }
    .result-label { color: #8ba3b0; }
    .result-value { color: #e8f4f8; font-weight: 600; }
    .result-total .result-value { color: #00d4aa; font-size: 1.15rem; }
    .result-vat   .result-value { color: #ffa040; }
</style>
""", unsafe_allow_html=True)

st.title("🧮 VAT Calculator")
st.caption("Saudi Arabia · 15% VAT · ZATCA")
st.divider()

# ── Mode toggle (works perfectly on mobile) ──────────────────────────────────
mode = st.selectbox("What is your amount?", ["Excluding VAT (add VAT on top)", "Including VAT (extract VAT)"])

# ── Slider for touch + text box for precision ─────────────────────────────────
st.markdown("**Amount (SAR)**")
slider_val = st.slider("", min_value=0, max_value=100_000, value=1_000, step=100, label_visibility="collapsed")
typed_val  = st.number_input("Or type exact amount:", min_value=0.0, value=float(slider_val), step=100.0, format="%.2f")

# Typed input wins if user changed it away from slider
amount = typed_val if typed_val != float(slider_val) else float(slider_val)

st.divider()

# ── Result ────────────────────────────────────────────────────────────────────
if amount > 0:
    if "Excluding" in mode:
        result  = calculate_vat_exclusive(amount)
        context = "VAT added on top of your net amount."
    else:
        result  = calculate_vat_inclusive(amount)
        context = "VAT extracted from your gross amount."

    st.markdown(f"""
    <div class="result-card">
        <div class="result-row">
            <span class="result-label">Net (excl. VAT)</span>
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
    <p style="color:#8ba3b0;font-size:0.82rem;margin-top:0.6rem;">ℹ️ {context}</p>
    """, unsafe_allow_html=True)

    with st.expander("📋 Copy-friendly breakdown"):
        st.code(
            f"Net Amount : {format_sar(result.subtotal)}\n"
            f"VAT (15%)  : {format_sar(result.vat_amount)}\n"
            f"Total      : {format_sar(result.total)}",
            language="text"
        )
else:
    st.info("Move the slider or type an amount to see the VAT breakdown.")

st.divider()
st.caption("⚠️ Informational only. Consult a KSA tax professional or [zatca.gov.sa](https://zatca.gov.sa).")
        
