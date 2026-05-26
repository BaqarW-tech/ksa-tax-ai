# 🇸🇦 KSA Tax AI — Phase 1 MVP

A Saudi VAT compliance assistant for freelancers, SMEs, and ecommerce businesses.  
Built with **Python · Streamlit · ZATCA regulations**.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://baqarw-tech.streamlit.app)

---

## Features (Phase 1)

| Tool | Description |
|------|-------------|
| 🧮 VAT Calculator | Add VAT to a net amount or extract it from a gross price |
| 📋 Registration Checker | Check if your revenue triggers mandatory/voluntary VAT registration |

---

## Architecture

```
ksa-tax-ai/
├── app.py                    # Home page
├── requirements.txt
├── pages/
│   ├── 1_VAT_Calculator.py   # VAT calculation page
│   └── 2_Registration_Checker.py
├── utils/
│   └── vat_logic.py          # Pure business logic (no Streamlit)
└── tests/
    └── test_vat_logic.py     # Unit tests (pytest)
```

**Design principle:** all calculation logic lives in `utils/vat_logic.py` — pure functions, no UI dependency, fully testable.

---

## KSA VAT Reference

| Parameter | Value |
|-----------|-------|
| Standard VAT rate | 15% |
| Mandatory registration threshold | SAR 375,000 / year |
| Voluntary registration threshold | SAR 187,500 / year |
| Authority | ZATCA ([zatca.gov.sa](https://zatca.gov.sa)) |

---

## Local Setup

```bash
git clone https://github.com/BaqarW-tech/ksa-tax-ai
cd ksa-tax-ai
pip install -r requirements.txt
streamlit run app.py
```

---

## Roadmap

- [x] Phase 1: VAT Calculator + Registration Checker
- [ ] Phase 2: Claude API — Tax Q&A + Invoice PDF Analyzer
- [ ] Phase 3: RAG over ZATCA documentation (ChromaDB + sentence-transformers)
- [ ] Phase 4: Compliance Checklist Generator + Penalty Estimator

---

## Disclaimer

This application is for **informational purposes only** and does not constitute legal or tax advice.  
Always consult a licensed KSA tax professional or visit [zatca.gov.sa](https://zatca.gov.sa).

---

*Part of a Vision 2030–aligned AI portfolio. Built by [@BaqarW-tech](https://github.com/BaqarW-tech).*
