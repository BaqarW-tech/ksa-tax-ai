"""
KSA Tax AI — Home
app.py · Entry point for Streamlit multipage app
"""

import streamlit as st

st.set_page_config(
    page_title="KSA Tax AI",
    page_icon="🇸🇦",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 0.5rem;
    }
    .hero-accent { color: #00d4aa; }
    .hero-sub {
        color: #8ba3b0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    .feature-card {
        background: #0f2027;
        border: 1px solid #1e3a4a;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 0.75rem;
        transition: border-color 0.2s;
    }
    .feature-card:hover { border-color: #00d4aa44; }
    .feature-icon { font-size: 1.5rem; margin-bottom: 0.4rem; }
    .feature-title { font-weight: 700; color: #e8f4f8; margin-bottom: 0.25rem; }
    .feature-desc  { color: #8ba3b0; font-size: 0.88rem; line-height: 1.5; }
    .badge {
        display: inline-block;
        background: #00d4aa22;
        color: #00d4aa;
        border: 1px solid #00d4aa44;
        border-radius: 20px;
        padding: 0.15rem 0.7rem;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
    }
    .disclaimer {
        background: #1a1a2e;
        border-left: 3px solid #ffa040;
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        color: #8ba3b0;
        font-size: 0.82rem;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-title">
    🇸🇦 KSA <span class="hero-accent">Tax AI</span>
</div>
<div class="hero-sub">
    A smart compliance assistant for Saudi VAT — built for freelancers,
    SMEs, and ecommerce businesses navigating ZATCA regulations.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<span class="badge">VAT 15%</span>
<span class="badge">ZATCA</span>
<span class="badge">KSA SME</span>
<span class="badge">Phase 1 MVP</span>
""", unsafe_allow_html=True)

st.divider()

# ── Features ──────────────────────────────────────────────────────────────────
st.markdown("#### Available Tools")

features = [
    {
        "icon": "🧮",
        "title": "VAT Calculator",
        "desc": "Add VAT to a net amount, or reverse-extract VAT from a gross price. Instant results with a copy-friendly breakdown.",
        "page": "VAT_Calculator",
    },
    {
        "icon": "📋",
        "title": "Registration Checker",
        "desc": "Enter your annual revenue to find out if VAT registration is mandatory, voluntary, or not required under ZATCA thresholds.",
        "page": "Registration_Checker",
    },
]

for f in features:
    st.markdown(f"""
    <div class="feature-card">
        <div class="feature-icon">{f["icon"]}</div>
        <div class="feature-title">{f["title"]}</div>
        <div class="feature-desc">{f["desc"]}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("*Use the sidebar to navigate between tools.*")

st.divider()

# ── Roadmap ───────────────────────────────────────────────────────────────────
with st.expander("🗺️ Upcoming Features (Phases 2–4)"):
    st.markdown("""
    | Phase | Feature | Status |
    |-------|---------|--------|
    | 2 | AI Tax Q&A (Claude API) | 🔜 Planned |
    | 2 | Invoice PDF Analyzer | 🔜 Planned |
    | 3 | RAG over ZATCA documents | 🔜 Planned |
    | 4 | Compliance Checklist Generator | 🔜 Planned |
    | 4 | VAT Penalty Estimator | 🔜 Planned |
    """)

# ── Disclaimer ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
    ⚠️ <strong>Disclaimer:</strong> This application is for informational purposes only and does not 
    constitute legal or tax advice. Always consult a licensed KSA tax professional or visit 
    <a href="https://zatca.gov.sa" target="_blank">zatca.gov.sa</a> for authoritative guidance.
</div>
""", unsafe_allow_html=True)

st.markdown("")
st.caption("Built with Python · Streamlit · ZATCA regulations · Phase 1 MVP") 
