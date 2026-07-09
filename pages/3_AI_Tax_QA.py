"""
KSA Tax AI — AI Tax Q&A
pages/3_AI_Tax_QA.py · Phase 2 · Gemini-powered chat assistant
"""

import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Tax Q&A · KSA Tax AI", page_icon="💬", layout="centered")

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
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-title">💬 AI Tax <span class="hero-accent">Q&A</span></div>
<div class="hero-sub">Ask questions about Saudi VAT, ZATCA compliance, and e-invoicing.
Powered by Google Gemini.</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
    ⚠️ Answers are AI-generated and for informational purposes only — not legal or tax advice.
    Always confirm with a licensed KSA tax professional or <a href="https://zatca.gov.sa" target="_blank">zatca.gov.sa</a>.
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

SYSTEM_PROMPT = """You are a knowledgeable assistant specializing in Saudi Arabian VAT and
ZATCA (Zakat, Tax and Customs Authority) regulations. You help freelancers, SMEs, and
ecommerce businesses understand:
- VAT registration thresholds (mandatory: SAR 375,000/year, voluntary: SAR 187,500/year)
- The standard 15% VAT rate and zero-rated/exempt categories
- ZATCA e-invoicing (Fatoora) Phase 1 and Phase 2 requirements
- Filing deadlines, penalties, and Zakat basics for KSA businesses

Rules:
- Be concise, accurate, and practical. Use bullet points for multi-part answers.
- If a question requires case-specific legal judgment, say so and recommend consulting
  a licensed tax professional or zatca.gov.sa.
- Never state a specific answer with high confidence if you are not certain — flag uncertainty.
- Stay strictly on KSA tax/VAT/ZATCA topics. Politely redirect if asked something unrelated.
"""

@st.cache_resource
def get_model():
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=SYSTEM_PROMPT,
    )

model = get_model()

# ── Chat state ───────────────────────────────────────────────────────────────
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []
    st.session_state.qa_chat = model.start_chat(history=[])

# ── Suggested prompts ────────────────────────────────────────────────────────
if not st.session_state.qa_history:
    st.markdown("**Try asking:**")
    cols = st.columns(1)
    suggestions = [
        "Do I need to register for VAT if I earn SAR 200,000/year?",
        "What is ZATCA Phase 2 e-invoicing and who must comply?",
        "What happens if I file my VAT return late?",
    ]
    for s in suggestions:
        if st.button(s, key=s, use_container_width=True):
            st.session_state.pending_prompt = s
            st.rerun()

# ── Render history ───────────────────────────────────────────────────────────
for msg in st.session_state.qa_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Handle a suggested prompt click ─────────────────────────────────────────
prompt = st.chat_input("Ask about VAT, ZATCA, or e-invoicing…")
if "pending_prompt" in st.session_state:
    prompt = st.session_state.pop("pending_prompt")

if prompt:
    st.session_state.qa_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            response = st.session_state.qa_chat.send_message(prompt, stream=True)
            full_text = ""
            for chunk in response:
                if chunk.text:
                    full_text += chunk.text
                    placeholder.markdown(full_text + "▌")
            placeholder.markdown(full_text)
        except Exception as e:
            full_text = f"Sorry, something went wrong reaching Gemini: `{e}`"
            placeholder.error(full_text)

    st.session_state.qa_history.append({"role": "assistant", "content": full_text})

if st.session_state.qa_history:
    if st.button("🗑️ Clear conversation"):
        st.session_state.qa_history = []
        st.session_state.qa_chat = model.start_chat(history=[])
        st.rerun()
