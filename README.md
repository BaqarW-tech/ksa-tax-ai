# KSA Tax AI

A Streamlit application that helps freelancers, SMEs, and ecommerce businesses in Saudi Arabia understand and manage VAT compliance under ZATCA (Zakat, Tax and Customs Authority) regulations.

Live app: https://ksa-tax-ai-djrvpkcqeuvr2rmdgegws2.streamlit.app/
Repository: https://github.com/BaqarW-tech/ksa-tax-ai

## Overview

KSA Tax AI combines deterministic calculation tools with AI-assisted features to cover the practical VAT compliance workflow of a Saudi business: registration eligibility, invoice compliance, regulatory Q&A, and penalty exposure. Calculations and compliance rules are implemented as plain Python logic rather than delegated to a language model, so results are consistent and auditable. Language models are used only where judgment or natural-language understanding adds value: answering open-ended questions and extracting structured data from unstructured documents.

## Features

### VAT Calculator
Adds VAT to a net amount or extracts VAT from a gross amount at the standard 15 percent rate.

### Registration Checker
Determines whether VAT registration is mandatory, voluntary, or not applicable based on a business's annual taxable revenue, using ZATCA's SAR 375,000 mandatory and SAR 187,500 voluntary thresholds.

### AI Tax Q&A
A chat interface for questions about VAT, ZATCA regulations, and e-invoicing. Uses the Gemini API with a system prompt scoped to KSA tax topics.

### Invoice Analyzer
Accepts an invoice PDF, extracts text, and uses the Gemini API to pull structured fields (VAT registration number, invoice number, dates, amounts, VAT rate). Results are checked against a fixed set of ZATCA e-invoicing compliance rules implemented in code, not by the model.

### ZATCA Document Search
A retrieval-augmented question-answering feature. A curated set of markdown documents covering VAT registration, VAT rates and supply categories, Fatoora e-invoicing, penalties and filing deadlines, and Zakat versus corporate income tax are chunked and embedded using Gemini's text-embedding-004 model. User queries are embedded and matched against the corpus using cosine similarity, and the top-matching passages are passed to the model as context, with sources shown alongside each answer. The index is built once at runtime and cached for the life of the app instance, rather than requiring a separate offline build step.

### Compliance Checklist
Generates a personalized VAT compliance checklist from a short business profile (revenue, registration status, residency, e-invoicing readiness, filing status). Logic is rule-based.

### Penalty Estimator
Produces an estimated penalty range for late VAT registration, late VAT return filing, or e-invoicing non-compliance, based on ZATCA's published penalty framework. Figures are estimates only and the tool states this explicitly in the interface.

## Tech Stack

- Python
- Streamlit (multipage app)
- Google Gemini API (gemini-2.0-flash for generation, text-embedding-004 for embeddings)
- pdfplumber for PDF text extraction
- numpy for similarity search

## Project Structure

```
ksa-tax-ai/
├── app.py                          # Home page and navigation
├── pages/
│   ├── 1_VAT_Calculator.py
│   ├── 2_Registration_Checker.py
│   ├── 3_AI_Tax_QA.py
│   ├── 4_Invoice_Analyzer.py
│   ├── 5_ZATCA_Search.py
│   ├── 6_Compliance_Checklist.py
│   └── 7_Penalty_Estimator.py
├── knowledge_base/
│   ├── vat_registration.md
│   ├── vat_rates_categories.md
│   ├── fatoora_einvoicing.md
│   ├── penalties_deadlines.md
│   └── zakat_vs_cit.md
├── requirements.txt
└── README.md
```

## Setup

### Prerequisites
- Python 3.12 (pinned via `runtime.txt` for Streamlit Cloud compatibility)
- A Gemini API key from Google AI Studio

### Local installation

```
git clone https://github.com/BaqarW-tech/ksa-tax-ai.git
cd ksa-tax-ai
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` in the project root:

```
GEMINI_API_KEY = "your-key-here"
```

Run the app:

```
streamlit run app.py
```

### Deployment (Streamlit Community Cloud)

1. Connect the GitHub repository to Streamlit Community Cloud.
2. Set the main file to `app.py`.
3. Add `GEMINI_API_KEY` under App Settings → Secrets.
4. Deploy. The app redeploys automatically on every push to the main branch.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | Yes | API key for Gemini generation and embedding calls, used by the Q&A, Invoice Analyzer, and Document Search pages |

## Status

All four planned phases are implemented: core VAT calculation tools, AI-assisted Q&A and invoice extraction, retrieval-augmented search over ZATCA documentation, and a compliance checklist with penalty estimation.

## Disclaimer

This application is for informational purposes only and does not constitute legal or tax advice. VAT rules, thresholds, and penalties referenced in this project reflect ZATCA regulations as understood at the time of writing and may change. Users should confirm current requirements with a licensed KSA tax professional or at zatca.gov.sa before relying on any output from this application.

## License

MIT License 
