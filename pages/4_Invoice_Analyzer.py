"""
KSA Tax AI — Invoice PDF Analyzer
pages/4_Invoice_Analyzer.py · Phase 2 · Gemini-powered invoice extraction & ZATCA checks
"""

import json
import streamlit as st
import google.generativeai as genai
import pdfplumber

st.set_page_config(page_title="Invoice Analyzer · KSA Tax AI", page_icon="🧾", layout="centered")

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
    .check-pass { color: #00d4aa; font-weight: 600; }
    .check-fail { color: #ff6b6b; font-weight: 600; }
    .check-unknown { color: #8ba3b0; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-title">🧾 Invoice <span class="hero-accent">Analyzer</span></div>
<div class="hero-sub">Upload a KSA invoice (PDF) to extract key fields and run a quick
ZATCA e-invoicing compliance check.</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
    ⚠️ This is an automated, AI-assisted check for common ZATCA e-invoicing fields.
    It is not a substitute for a formal compliance audit or professional review.
</div>
""", unsafe_allow_html=True)

# ── Gemini setup ─────────────────────────────────────────────────────────────
API_KEY = st.secrets.get("GEMINI_API_KEY", "")

if not API_KEY:
    st.error(
        "No Gemini API key found. Add `GEMINI_API_KEY` to your Streamlit Cloud "
        "app secrets (Settings → Secrets), or to a local `.streamlit/secrets.toml` file."
    )
    st.stop()

genai.configure(api_key=API_KEY)

EXTRACTION_PROMPT = """You are analyzing the text extracted from a Saudi Arabian (KSA) invoice PDF.

Extract the following fields as strict JSON (use null if a field is not found — do not guess):

{
  "seller_name": string or null,
  "seller_vat_number": string or null,       // 15-digit ZATCA VAT registration number
  "buyer_name": string or null,
  "invoice_number": string or null,
  "invoice_date": string or null,
  "subtotal": number or null,
  "vat_rate_percent": number or null,
  "vat_amount": number or null,
  "total_amount": number or null,
  "has_qr_code_mentioned": boolean,          // true if text references a QR code/Fatoora
  "currency": string or null
}

Respond with ONLY the JSON object, no markdown fences, no commentary.

INVOICE TEXT:
---
{invoice_text}
---
"""

@st.cache_resource
def get_model():
    return genai.GenerativeModel(model_name="gemini-2.0-flash")

model = get_model()


def extract_pdf_text(file) -> str:
    text_parts = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def run_compliance_checks(data: dict) -> list:
    checks = []

    vat_num = data.get("seller_vat_number")
    checks.append({
        "label": "Seller VAT registration number present (15 digits)",
        "status": "pass" if vat_num and len(str(vat_num).replace(" ", "")) == 15
                   else ("fail" if vat_num else "unknown"),
    })

    checks.append({
        "label": "Invoice number present",
        "status": "pass" if data.get("invoice_number") else "unknown",
    })

    checks.append({
        "label": "Invoice date present",
        "status": "pass" if data.get("invoice_date") else "unknown",
    })

    vat_rate = data.get("vat_rate_percent")
    checks.append({
        "label": "Standard VAT rate applied (15%)",
        "status": "pass" if vat_rate == 15 else ("fail" if vat_rate is not None else "unknown"),
    })

    subtotal, vat_amt, total = data.get("subtotal"), data.get("vat_amount"), data.get("total_amount")
    math_ok = None
    if subtotal is not None and vat_amt is not None and total is not None:
        math_ok = abs((subtotal + vat_amt) - total) < 0.05
    checks.append({
        "label": "Totals reconcile (subtotal + VAT = total)",
        "status": "pass" if math_ok else ("fail" if math_ok is False else "unknown"),
    })

    checks.append({
        "label": "QR code / Fatoora reference detected",
        "status": "pass" if data.get("has_qr_code_mentioned") else "fail",
    })

    return checks


# ── Upload ────────────────────────────────────────────────────────────────────
uploaded = st.file_uploader("Upload invoice PDF", type=["pdf"])

if uploaded:
    with st.spinner("Extracting text from PDF…"):
        try:
            raw_text = extract_pdf_text(uploaded)
        except Exception as e:
            st.error(f"Couldn't read this PDF: {e}")
            st.stop()

    if not raw_text.strip():
        st.warning(
            "No selectable text found in this PDF — it may be a scanned image. "
            "OCR support is planned for a future update."
        )
        st.stop()

    with st.spinner("Analyzing with Gemini…"):
        try:
            prompt = EXTRACTION_PROMPT.replace("{invoice_text}", raw_text[:15000])
            response = model.generate_content(prompt)
            cleaned = response.text.strip().strip("```json").strip("```").strip()
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            st.error("Gemini's response wasn't valid JSON. Try a different invoice or re-run.")
            with st.expander("Raw model output"):
                st.code(response.text)
            st.stop()
        except Exception as e:
            st.error(f"Something went wrong calling Gemini: {e}")
            st.stop()

    st.divider()
    st.markdown("#### Extracted Fields")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Amount", f"{data.get('total_amount', '—')} {data.get('currency') or ''}")
        st.write(f"**Seller:** {data.get('seller_name') or '—'}")
        st.write(f"**Buyer:** {data.get('buyer_name') or '—'}")
        st.write(f"**Invoice #:** {data.get('invoice_number') or '—'}")
    with col2:
        st.metric("VAT Amount", f"{data.get('vat_amount', '—')}")
        st.write(f"**VAT #:** {data.get('seller_vat_number') or '—'}")
        st.write(f"**Date:** {data.get('invoice_date') or '—'}")
        st.write(f"**VAT Rate:** {data.get('vat_rate_percent', '—')}%")

    st.divider()
    st.markdown("#### ZATCA Compliance Check")
    icon_map = {"pass": "✅", "fail": "❌", "unknown": "❔"}
    css_map = {"pass": "check-pass", "fail": "check-fail", "unknown": "check-unknown"}
    for check in run_compliance_checks(data):
        icon = icon_map[check["status"]]
        css = css_map[check["status"]]
        st.markdown(f"{icon} <span class='{css}'>{check['label']}</span>", unsafe_allow_html=True)

    with st.expander("Raw extracted JSON"):
        st.json(data)
