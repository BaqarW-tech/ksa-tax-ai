"""
KSA Tax AI — ZATCA Document Search (RAG)
pages/5_ZATCA_Search.py · Phase 3 · Retrieval-augmented Q&A over a curated ZATCA knowledge base
"""

import json
import os
import numpy as np
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="ZATCA Document Search · KSA Tax AI", page_icon="📚", layout="centered")

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
    .source-chip {
        display: inline-block; background: #0f2027; border: 1px solid #1e3a4a;
        border-radius: 8px; padding: 0.6rem 0.9rem; margin-bottom: 0.5rem;
        font-size: 0.85rem; color: #8ba3b0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-title">📚 ZATCA <span class="hero-accent">Document Search</span></div>
<div class="hero-sub">Retrieval-augmented Q&A over a curated knowledge base of ZATCA VAT,
Fatoora e-invoicing, penalty, and Zakat/CIT summaries — grounded answers with sources shown.</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
    ⚠️ Answers are generated from a summarized internal knowledge base, not the live ZATCA
    portal, and are for informational purposes only — not legal or tax advice.
</div>
""", unsafe_allow_html=True)

# ── Gemini setup ─────────────────────────────────────────────────────────────
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not API_KEY:
    st.error(
        "No Gemini API key found. Add `GEMINI_API_KEY` to your Streamlit Cloud "
        "app secrets, or to a local `.streamlit/secrets.toml` file."
    )
    st.stop()

genai.configure(api_key=API_KEY)
EMBED_MODEL = "models/text-embedding-004"
GEN_MODEL = "gemini-2.0-flash"
TOP_K = 4

INDEX_PATH = os.path.join("knowledge_base", "embeddings.json")


@st.cache_resource
def load_index():
    if not os.path.exists(INDEX_PATH):
        return None
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)
    matrix = np.array([r["embedding"] for r in records], dtype=np.float32)
    # Pre-normalize for cosine similarity via dot product
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1
    matrix = matrix / norms
    return records, matrix


index = load_index()
if index is None:
    st.warning(
        "No knowledge base index found yet. Run `build_index.py` locally "
        "(see comments in that file) and commit `knowledge_base/embeddings.json` "
        "to your repo to enable this page."
    )
    st.stop()

records, matrix = index


def retrieve(query: str, k: int = TOP_K):
    result = genai.embed_content(
        model=EMBED_MODEL, content=query, task_type="retrieval_query"
    )
    q_vec = np.array(result["embedding"], dtype=np.float32)
    q_vec = q_vec / (np.linalg.norm(q_vec) or 1)
    scores = matrix @ q_vec
    top_idx = np.argsort(-scores)[:k]
    return [(records[i], float(scores[i])) for i in top_idx]


RAG_PROMPT_TEMPLATE = """You are a KSA VAT/ZATCA assistant. Answer the user's question using
ONLY the context passages below. If the context doesn't contain enough information to answer
confidently, say so explicitly rather than guessing.

Cite which source file(s) you drew from at the end of your answer, like: (Source: vat_registration.md).

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""


@st.cache_resource
def get_gen_model():
    return genai.GenerativeModel(model_name=GEN_MODEL)


gen_model = get_gen_model()

# ── Query UI ─────────────────────────────────────────────────────────────────
query = st.text_input(
    "Ask a question about KSA VAT, Fatoora, penalties, or Zakat/CIT",
    placeholder="e.g. What's the penalty for filing my VAT return late?",
)

if query:
    with st.spinner("Searching knowledge base…"):
        hits = retrieve(query)

    with st.spinner("Generating answer…"):
        context = "\n\n---\n\n".join(
            f"[{h['source']}]\n{h['text']}" for h, _ in hits
        )
        prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=query)
        try:
            response = gen_model.generate_content(prompt)
            answer = response.text
        except Exception as e:
            st.error(f"Something went wrong calling Gemini: {e}")
            st.stop()

    st.markdown("#### Answer")
    st.markdown(answer)

    st.markdown("#### Sources retrieved")
    for h, score in hits:
        st.markdown(
            f"<div class='source-chip'>📄 <strong>{h['source']}</strong> "
            f"· relevance {score:.2f}<br>{h['text'][:220]}…</div>",
            unsafe_allow_html=True,
        )
