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
<span class="badge">All Phases Live</span>
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
    {
        "icon": "💬",
        "title": "AI Tax Q&A",
        "desc": "Ask a Gemini-powered assistant about VAT, ZATCA rules, and e-invoicing requirements in plain language.",
        "page": "AI_Tax_QA",
    },
    {
        "icon": "🧾",
        "title": "Invoice Analyzer",
        "desc": "Upload an invoice PDF to extract key fields and run a quick ZATCA e-invoicing compliance check.",
        "page": "Invoice_Analyzer",
    },
    {
        "icon": "📚",
        "title": "ZATCA Document Search",
        "desc": "Retrieval-augmented Q&A grounded in a curated ZATCA knowledge base, with sources shown for every answer.",
        "page": "ZATCA_Search",
    },
    {
        "icon": "✅",
        "title": "Compliance Checklist",
        "desc": "Answer a few questions about your business and get a personalized ZATCA VAT compliance checklist.",
        "page": "Compliance_Checklist",
    },
    {
        "icon": "⚠️",
        "title": "Penalty Estimator",
        "desc": "Estimate potential ZATCA penalty exposure for late registration, late filing, or e-invoicing violations.",
        "page": "Penalty_Estimator",
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
with st.expander("🗺️ Feature Roadmap"):
    st.markdown("""
    | Phase | Feature | Status |
    |-------|---------|--------|
    | 1 | VAT Calculator | ✅ Live |
    | 1 | Registration Checker | ✅ Live |
    | 2 | AI Tax Q&A (Gemini API) | ✅ Live |
    | 2 | Invoice PDF Analyzer | ✅ Live |
    | 3 | RAG over ZATCA documents | ✅ Live |
    | 4 | Compliance Checklist Generator | ✅ Live |
    | 4 | VAT Penalty Estimator | ✅ Live |
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
st.caption("Built with Python · Streamlit · Gemini AI · ZATCA regulations · Phases 1–4 complete")
