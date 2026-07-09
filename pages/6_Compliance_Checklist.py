"""
KSA Tax AI — Compliance Checklist Generator
pages/6_Compliance_Checklist.py · Phase 4 · Rule-based, personalized to business profile
"""

import streamlit as st

st.set_page_config(page_title="Compliance Checklist · KSA Tax AI", page_icon="✅", layout="centered")

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
    .check-item {
        background: #0f2027; border: 1px solid #1e3a4a; border-radius: 10px;
        padding: 0.8rem 1rem; margin-bottom: 0.5rem; font-size: 0.92rem;
    }
    .status-ok    { color: #00d4aa; font-weight: 700; }
    .status-todo  { color: #ffa040; font-weight: 700; }
    .status-na    { color: #5a7684; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-title">✅ Compliance <span class="hero-accent">Checklist</span></div>
<div class="hero-sub">Answer a few questions about your business and get a personalized
ZATCA VAT compliance checklist.</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
    ⚠️ This checklist is a general guide based on common ZATCA requirements. It doesn't cover
    every edge case (sector-specific rules, group registration, etc.) — confirm with a licensed
    tax professional or <a href="https://zatca.gov.sa" target="_blank">zatca.gov.sa</a>.
</div>
""", unsafe_allow_html=True)

st.markdown("#### Your business profile")

annual_revenue = st.number_input(
    "Annual taxable revenue (SAR)", min_value=0, step=10000, value=500000
)
is_registered = st.radio("Are you currently VAT registered?", ["Yes", "No"], horizontal=True)
is_resident = st.radio("Is your business Saudi-resident?", ["Yes", "No"], horizontal=True)
has_einvoicing = st.radio(
    "Do you have a Fatoora-compliant e-invoicing system in place?",
    ["Yes", "No", "Not sure"], horizontal=True,
)
filing_current = st.radio(
    "Are your VAT returns filed up to date (including nil returns)?",
    ["Yes", "No", "N/A — not registered"], horizontal=True,
)
issues_b2c = st.radio("Do you issue simplified (B2C) invoices?", ["Yes", "No"], horizontal=True)

if st.button("Generate checklist", type="primary"):
    items = []

    # Registration
    if not is_resident.startswith("Y"):
        items.append(("todo", "Non-resident businesses must register for VAT regardless of "
                               "turnover, and should appoint a local tax representative."))
    elif annual_revenue >= 375000:
        if is_registered.startswith("Y"):
            items.append(("ok", "VAT registration in place — required at your revenue level (≥ SAR 375,000)."))
        else:
            items.append(("todo", "Your revenue exceeds SAR 375,000 — mandatory VAT registration "
                                   "applies. Register within 30 days to avoid a ~SAR 10,000 late-registration penalty."))
    elif annual_revenue >= 187500:
        if is_registered.startswith("Y"):
            items.append(("ok", "Voluntarily registered — allows input VAT recovery."))
        else:
            items.append(("na", "Below the mandatory threshold (SAR 375,000). Voluntary "
                                 "registration is optional at your revenue level."))
    else:
        items.append(("na", "Below the voluntary threshold (SAR 187,500) — VAT registration "
                             "is not required or available yet."))

    # Filing
    if is_registered.startswith("Y"):
        return_freq = "monthly" if annual_revenue > 40_000_000 else "quarterly"
        if filing_current.startswith("Y"):
            items.append(("ok", f"VAT returns are up to date ({return_freq} filing frequency applies at your revenue)."))
        elif filing_current.startswith("No"):
            items.append(("todo", f"Catch up on outstanding VAT returns — {return_freq} filing "
                                   "applies at your revenue. Late filings can trigger fines of 5–25% of VAT due."))

    # E-invoicing Phase 1 & 2
    if is_registered.startswith("Y"):
        if has_einvoicing.startswith("Y"):
            items.append(("ok", "Fatoora Phase 1 (electronic generation) appears to be covered."))
        else:
            items.append(("todo", "Set up a Fatoora Phase 1-compliant e-invoicing system "
                                   "(structured e-invoices in XML or PDF/A-3)."))
        if annual_revenue >= 375000:
            items.append(("todo", "Confirm your Fatoora Phase 2 integration wave and deadline "
                                   "with ZATCA — as of Wave 24, all VAT-registered businesses "
                                   "above SAR 375,000 are in scope (deadline 30 June 2026)."))

    # B2C QR codes
    if issues_b2c.startswith("Y"):
        items.append(("todo", "Ensure all simplified (B2C) invoices carry a valid QR code."))

    st.divider()
    st.markdown("#### Your checklist")

    icon_map = {"ok": ("✅", "status-ok"), "todo": ("🟠", "status-todo"), "na": ("⚪", "status-na")}
    for status, text in items:
        icon, css = icon_map[status]
        st.markdown(
            f"<div class='check-item'>{icon} <span class='{css}'>"
            f"{'DONE' if status=='ok' else 'ACTION NEEDED' if status=='todo' else 'N/A'}</span>"
            f" — {text}</div>",
            unsafe_allow_html=True,
        )

    todo_count = sum(1 for s, _ in items if s == "todo")
    if todo_count == 0:
        st.success("No outstanding action items based on your answers. 🎉")
    else:
        st.warning(f"{todo_count} action item(s) need attention.")

    summary_text = "KSA VAT Compliance Checklist\n" + "=" * 30 + "\n\n" + "\n".join(
        f"[{'DONE' if s=='ok' else 'TODO' if s=='todo' else 'N/A'}] {t}" for s, t in items
    )
    st.download_button("📥 Download checklist as .txt", summary_text, file_name="vat_compliance_checklist.txt")
