"""
KSA Tax AI — VAT Penalty Estimator
pages/7_Penalty_Estimator.py · Phase 4 · Rule-based estimate, no external API calls
"""

import streamlit as st

st.set_page_config(page_title="Penalty Estimator · KSA Tax AI", page_icon="⚠️", layout="centered")

# ── Styles (matches Home) ───────────────────────────────────────────────────
st.markdown("""
<style>
    .hero-title { font-size: 2.2rem; font-weight: 800; margin-bottom: 0.25rem; }
    .hero-accent { color: #00d4aa; }
    .hero-sub { color: #8ba3b0; font-size: 1rem; margin-bottom: 1.5rem; line-height: 1.5; }
    .disclaimer {
        background: #1a1a2e; border-left: 3px solid #ffa040; border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem; color: #8ba3b0; font-size: 0.82rem; line-height: 1.5;
        margin-bottom: 1rem;
    }
    .result-box {
        background: #0f2027; border: 1px solid #00d4aa44; border-radius: 12px;
        padding: 1.25rem 1.5rem; margin-top: 1rem;
    }
    .result-amount { font-size: 1.8rem; font-weight: 800; color: #00d4aa; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-title">⚠️ VAT Penalty <span class="hero-accent">Estimator</span></div>
<div class="hero-sub">Get a rough estimate of potential ZATCA penalty exposure. This is a
simplified model, not an official calculation.</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
    ⚠️ <strong>Estimate only.</strong> ZATCA determines actual penalties case-by-case, and this
    tool does not account for every mitigating or aggravating factor. Always verify with ZATCA
    or a licensed tax advisor before relying on any figure here.
</div>
""", unsafe_allow_html=True)

violation = st.selectbox(
    "Violation type",
    ["Late VAT registration", "Late VAT return filing", "E-invoicing (Fatoora) non-compliance"],
)

st.divider()

if violation == "Late VAT registration":
    st.markdown("Fixed penalty for registering after the 30-day deadline from crossing the mandatory threshold.")
    st.markdown("""
    <div class="result-box">
        <div>Estimated penalty</div>
        <div class="result-amount">SAR 10,000</div>
        <div style="color:#8ba3b0; font-size:0.85rem; margin-top:0.4rem;">
            Fixed amount per ZATCA's standard late-registration penalty. May be reduced
            through a first-time waiver request in some cases.
        </div>
    </div>
    """, unsafe_allow_html=True)

elif violation == "Late VAT return filing":
    vat_due = st.number_input("VAT due for the period (SAR)", min_value=0.0, step=100.0, value=10000.0)
    days_late = st.number_input("Days late", min_value=1, step=1, value=15)

    if days_late <= 30:
        rate = 0.05
        tier = "≤ 30 days late"
    elif days_late <= 90:
        rate = 0.10
        tier = "31–90 days late"
    elif days_late <= 180:
        rate = 0.15
        tier = "91–180 days late"
    elif days_late <= 365:
        rate = 0.20
        tier = "181–365 days late"
    else:
        rate = 0.25
        tier = "> 365 days late"

    estimated_penalty = vat_due * rate

    st.markdown(f"""
    <div class="result-box">
        <div>Estimated penalty ({tier}, ~{rate*100:.0f}% of VAT due)</div>
        <div class="result-amount">SAR {estimated_penalty:,.2f}</div>
        <div style="color:#8ba3b0; font-size:0.85rem; margin-top:0.4rem;">
            ZATCA's actual penalty for late filing scales from 5% to 25% of the VAT due
            depending on lateness — this tool uses a simplified linear tier model to
            approximate that range.
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    severity = st.radio("Nature of violation", ["First-time / minor", "Repeat / significant"], horizontal=True)
    low, high = (5000, 15000) if severity.startswith("First") else (15000, 50000)

    st.markdown(f"""
    <div class="result-box">
        <div>Estimated penalty range</div>
        <div class="result-amount">SAR {low:,} – {high:,}</div>
        <div style="color:#8ba3b0; font-size:0.85rem; margin-top:0.4rem;">
            E-invoicing violations (e.g. missing QR codes, non-compliant format, failure to
            integrate with Fatoora Phase 2 by your wave deadline) are penalized on a
            case-by-case basis within this general range, escalating for repeat offenses.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption(
    "For the current, authoritative penalty schedule, refer to ZATCA's published VAT "
    "Implementing Regulations at zatca.gov.sa."
)
