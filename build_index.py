"""
build_index.py — Run this ONCE locally (not on Streamlit Cloud) whenever you add or
edit files in knowledge_base/. It chunks each document, embeds the chunks with Gemini's
embedding model, and writes the result to knowledge_base/embeddings.json.

Usage:
    export GEMINI_API_KEY="your-key-here"      # or set in .env
    pip install google-generativeai
    python build_index.py
"""

import json
import os
import re
import time
import google.generativeai as genai

KB_DIR = "knowledge_base"
OUTPUT_FILE = os.path.join(KB_DIR, "embeddings.json")
EMBED_MODEL = "models/text-embedding-004"
CHUNK_SIZE_WORDS = 150
CHUNK_OVERLAP_WORDS = 30


def chunk_text(text: str, size: int = CHUNK_SIZE_WORDS, overlap: int = CHUNK_OVERLAP_WORDS):
    """Split on markdown headings first, then further split long sections by word count."""
    sections = re.split(r"\n(?=#{1,3} )", text)
    chunks = []
    for section in sections:
        words = section.split()
        if not words:
            continue
        if len(words) <= size:
            chunks.append(section.strip())
            continue
        start = 0
        while start < len(words):
            end = start + size
            chunks.append(" ".join(words[start:end]))
            start = end - overlap
    return [c for c in chunks if c.strip()]


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("Set the GEMINI_API_KEY environment variable first.")
    genai.configure(api_key=api_key)

    records = []
    files = sorted(f for f in os.listdir(KB_DIR) if f.endswith(".md"))
    print(f"Found {len(files)} knowledge base files.")

    for fname in files:
        path = os.path.join(KB_DIR, fname)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = chunk_text(text)
        print(f"  {fname}: {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            result = genai.embed_content(
                model=EMBED_MODEL,
                content=chunk,
                task_type="retrieval_document",
            )
            records.append({
                "source": fname,
                "chunk_id": f"{fname}::{i}",
                "text": chunk,
                "embedding": result["embedding"],
            })
            time.sleep(0.2)  # gentle on free-tier rate limits

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f)

    print(f"\nWrote {len(records)} embedded chunks to {OUTPUT_FILE}")
    print("Commit this file to your repo — the app loads it at runtime and does NOT")
    print("re-embed the knowledge base, so no API cost at query time beyond the question itself.")


if __name__ == "__main__":
    main()
