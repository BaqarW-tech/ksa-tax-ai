"""
VAT Registration Checker — KSA Tax AI
Mobile-friendly version
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from utils.vat_logic import (
    check_registration_status, RegistrationStatus, format_sar,
    MANDATORY_THRESHOLD, VOLUNTARY_THRESHOLD,
)

st.set_page_config(page_title="Registration Checker | KSA Tax AI", page_icon="📋", layout="centered")

STATUS_COLORS = {
    RegistrationStatus.MANDATORY:    ("#ff4b4b", "#2d1010", "🚨"),
    RegistrationStatus.VOLUNTARY:    ("#ffa040", "#2d1f0a", "⚡"),
    RegistrationStatus.NOT_REQUIRED: ("#00d4aa", "#0a2d26", "✅"),
}

st.markdown("""
<style>
    .status-card { border-radius: 12px; padding: 1.5rem 2rem; margin-top: 1rem; }
    .status-title { font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem; }
    .status-body  { font-size: 0.95rem; line-height: 1.6; margin-bottom: 1rem; color: #c8dde6; }
    .status-action { border-radius: 8px; padding: 0.75rem 1rem; font-size: 0.9rem; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

st.title("📋 Registration Checker")
st.caption("Saudi Arabia · ZATCA VAT Thresholds")
st.divider()

# ── Slider (touch-friendly) ───────────────────────────────────────────────────
st.markdown("**Annual Taxable Revenue (SAR)**")
revenue = st.slider("", min_value=0, max_value=1_000_000, value=300_000, step=5_000, label_visibility="collapsed")
typed   = st.number_input("Or type exact amount:", min_value=0.0, value=float(revenue), step=10_000.0, format="%.0f")
annual_revenue = typed if typed != float(revenue) else float(revenue)

st.caption(f"Selected: **{format_sar(annual_revenue)}** / year")
st.divider()

# ── Result ────────────────────────────────────────────────────────────────────
result = check_registration_status(annual_revenue)
color, bg, icon = STATUS_COLORS[result.status]

st.markdown(f"""
<div class="status-card" style="background:{bg}; border:1px solid {color}44;">
    <div class="status-title" style="color:{color};">{icon} {result.label}</div>
    <div class="status-body">{result.explanation}</div>
    <div class="status-action" style="background:{color}22; color:{color}; border:1px solid {color}44;">
        👉 {result.action}
    </div>
</div>
""", unsafe_allow_html=True)

# ── Metrics ───────────────────────────────────────────────────────────────────
st.markdown("#### Threshold comparison")
col1, col2, col3 = st.columns(3)
col1.metric("Your Revenue",         format_sar(annual_revenue))
col2.metric("Voluntary Threshold",  format_sar(VOLUNTARY_THRESHOLD))
col3.metric("Mandatory Threshold",  format_sar(MANDATORY_THRESHOLD))

# ── Reference ─────────────────────────────────────────────────────────────────
with st.expander("📖 ZATCA threshold reference"):
    st.markdown("""
| Status | Annual Supplies | Obligation |
|--------|----------------|------------|
| 🚨 Mandatory | ≥ SAR 375,000 | Must register |
| ⚡ Voluntary | SAR 187,500 – 374,999 | May register |
| ✅ Not Required | < SAR 187,500 | No action needed |

*Source: ZATCA VAT Implementing Regulations*
    """)

st.divider()
st.caption("⚠️ Informational only. Consult a KSA tax professional or [zatca.gov.sa](https://zatca.gov.sa).")
