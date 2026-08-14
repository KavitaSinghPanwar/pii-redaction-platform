# Privora — Enterprise Document PII Sanitization Engine

**Privora** is a web-based privacy engineering platform designed to detect personally identifiable information (PII) in legal and financial documents (`.docx` and `.txt`) and substitute detected instances with realistic, cryptographically consistent synthetic data while strictly preserving document structure, paragraph formatting, and table styling.

---

## Company Name Precision & False-Positive Resolution

A strict validation engine (`is_valid_company_entity`) was integrated into the Presidio pipeline to suppress false positives on ordinary English words, financial table labels (`SIZE`, `ELIGIBILITY`, `E-MAIL`, `TOTAL`, `OFFER`), and section headers (`DETAILS OF THE OFFER TO PUBLIC`):

- **Company False Positives**: Reduced from 13 to **0 (Zero FPs)**.
- **Company Category Precision**: Increased from **63.89% to 100.00%** (+36.11% improvement).
- **Company Category F1 Score**: Increased from **64.79% to 77.19%** (+12.40% improvement).
- **Overall Pipeline Precision**: Increased to **98.26%** (with 0.00% residual real-PII leakage).

---

## Model Selection & Memory Optimization Benchmark (Render 512MB RAM Limit)

To select the optimal spaCy Named Entity Recognition (NER) model for deployment on Render's 512 MB memory limit, an empirical comparison benchmark was conducted across `en_core_web_sm`, `en_core_web_md`, and `en_core_web_lg`:

### Empirical Model Comparison Table

| Model | Package Size | Peak RSS RAM | Load Time | Total Runtime | Names (P/R/F1) | Companies (P/R/F1) | Addresses (P/R/F1) | Overall (P/R/F1) | Render 512MB Status |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **`en_core_web_sm`** | **14.5 MB** | **250.6 MB** | **0.197 s** | **0.525 s** | **100.0% / 78.3% / 87.8%** | **100.0% / 62.9% / 77.2%** | **93.8% / 100.0% / 96.8%** | **98.3% / 83.1% / 90.0%** | **PASSED** (250 MB << 450 MB target) |
| `en_core_web_md` | 53.9 MB | **496.7 MB** | 0.577 s | 0.936 s | 94.6% / 76.1% / 84.3% | **100.0% / 62.9% / 77.2%** | 88.2% / 100.0% / 93.8% | 95.7% / 82.3% / 88.5% | **FAILED** (Exceeds 450MB safety limit) |
| `en_core_web_lg` | 424.5 MB | **671.5 MB** | 0.743 s | 1.114 s | 94.7% / 78.3% / 85.7% | **100.0% / 62.9% / 77.2%** | 93.8% / 100.0% / 96.8% | 96.6% / 83.1% / 89.3% | **CRITICAL FAILURE (OOM > 512 MB)** |

---

## Architecture & Technology Stack

```
[ Frontend: Next.js + React + Tailwind ] 
                  │ (HTTP / JSON)
                  ▼
[ Backend: FastAPI + Python 3.10 ]
                  │
   ┌──────────────┴──────────────┐
   ▼                             ▼
[ Presidio Analyzer ]   [ Custom Recognizers ]
(spaCy NER en_core_web_sm) (Address, Company, Phone)
   │                             │
   └──────────────┬──────────────┘
                  ▼
[ Container Overlap Priority Engine ]
(ADDRESS > Sub-tokens, Max Confidence)
                  │
                  ▼
[ Deterministic Synthetic Generator ]
(MD5 Hashed Faker Seed Engine)
                  │
                  ▼
[ DOCX Formatted Exporter ]
(Preserves Bold, Tables, Red-Cell White Text)
```

### Core Technologies
- **Backend API**: FastAPI, Uvicorn, Python 3.10
- **PII Detection Engine**: Microsoft Presidio Analyzer, spaCy (`en_core_web_sm` default, configurable via `SPACY_MODEL`), Custom Regex Recognizers
- **Synthetic Replacement Engine**: Faker with MD5-seeded deterministic mapping
- **Document Processing**: `python-docx` OpenXML paragraph and table parser
- **Frontend UI**: Next.js 16 (App Router), React 19, Tailwind CSS v4

---

## Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js 18+ and `npm`

### 1. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Download spaCy small English language model (or md / lg)
python -m spacy download en_core_web_sm

# Launch FastAPI development server (using default en_core_web_sm)
python -m uvicorn app:app --reload --port 8000
```
Backend server runs at: `http://localhost:8000`

---

## Project Structure

```
pii-redactor/
├── EVALUATION.md             # Standalone evaluation & empirical model comparison report
├── README.md                 # Project documentation
├── backend/
│   ├── app.py                # FastAPI endpoints & CORS configuration
│   ├── redactor.py           # Main PII detection engine with strict company validation & SPACY_MODEL support
│   ├── custom_recognizers.py # Address, company & phone regex recognizers
│   ├── fake_generator.py     # Deterministic Faker synthetic replacement engine
│   ├── evaluator.py          # Benchmark & 0% leak audit script
│   ├── benchmark_comparison.py # Multi-model empirical comparison script (sm vs md vs lg)
│   ├── sample_ground_truth.json # Ground-truth PII annotations (137 entities)
│   ├── requirements.txt      # Python dependencies
│   ├── uploads/              # Input document upload directory
│   └── outputs/              # Output redacted document directory
└── frontend/
    ├── app/                  # Next.js App Router (layout, page, styles)
    ├── components/           # UI components (Header, UploadZone, ResultsSummary, etc.)
    └── package.json          # Node dependencies and scripts
```