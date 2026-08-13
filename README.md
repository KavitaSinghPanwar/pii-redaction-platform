# Aegis Redact — Enterprise Document PII Sanitization Engine

**Aegis Redact** is a web-based privacy engineering platform designed to detect personally identifiable information (PII) in legal and financial documents (`.docx` and `.txt`) and substitute detected instances with realistic, cryptographically consistent synthetic data while strictly preserving document structure, paragraph formatting, and table styling.

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
- **PII Detection Engine**: Microsoft Presidio Analyzer, spaCy (`en_core_web_sm`), Custom Regular Expression Pattern Recognizers
- **Synthetic Replacement Engine**: Faker with MD5-seeded deterministic mapping
- **Document Processing**: `python-docx` OpenXML paragraph and table parser
- **Frontend UI**: Next.js 16 (App Router), React 19, Tailwind CSS v4

---

## Key Features

1. **Comprehensive 9-Category PII Detection**:
   - Full Names (`PERSON`)
   - Email Addresses (`EMAIL_ADDRESS`)
   - Phone Numbers (`PHONE_NUMBER`)
   - Physical/Mailing Addresses (`ADDRESS`)
   - Company & Organization Names (`COMPANY`)
   - Social Security Numbers (`SSN`)
   - Credit Card Numbers (`CREDIT_CARD`)
   - Dates of Birth (`DATE_OF_BIRTH`)
   - IP Addresses (`IP_ADDRESS`)

2. **Atomic Address & Overlap Resolution**:
   - Container-priority resolution engine (`ADDRESS` > sub-tokens) ensures physical address blocks are atomized as single spans, suppressing sub-token misclassifications.

3. **Deterministic Synthetic Replacement**:
   - Cryptographically seeds synthetic values via MD5 hashes of original entity strings, guaranteeing consistent replacements across repeated occurrences.

4. **Document Formatting & Table Style Preservation**:
   - Preserves paragraph alignment, font bolding, and table cell structures. Automatically sets text color to **WHITE** on red/dark-red shaded header rows and section banners.

5. **Quality Assurance & Ground-Truth Benchmarking**:
   - Integrated evaluation suite (`evaluator.py`) measuring Precision, Recall, F1 Score, and Accuracy against manually labeled prospectus ground truth. Includes automated 0% residual real-PII substring leakage audits.

---

## Performance Benchmark Summary

Evaluated against 137 ground-truth PII entities from the *Red Herring Prospectus*:

| Metric | Result |
|---|:---:|
| **Overall Precision** | **94.87%** |
| **Overall Recall** | **80.43%** |
| **Overall F1 Score** | **87.06%** |
| **Overall Accuracy** | **77.08%** |
| **Residual Real-PII Leakage Rate** | **0.00%** (0 / 137 leaked) |

*For complete evaluation methodology, explicit scope decisions, and category breakdown, see [`EVALUATION.md`](EVALUATION.md).*

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

# Download spaCy small English language model
python -m spacy download en_core_web_sm

# Launch FastAPI development server
python -m uvicorn app:app --reload --port 8000
```
Backend server runs at: `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend

# Install Node dependencies
npm install

# Launch Next.js development server
npm run dev
```
Frontend application runs at: `http://localhost:3000`

---

## API Endpoints

- `GET /`: Health check and operational status.
- `POST /redact-full`: Accepts `.docx` or `.txt` upload; returns JSON summary, per-category entity counts, diff verification snippets, and download links.
- `POST /redact`: Legacy endpoint streaming redacted document output directly.
- `GET /download/{filename}`: Downloads processed redacted `.docx` / `.txt` files.
- `GET /evaluate`: Triggers live ground-truth evaluation benchmark and returns metric report.

---

## Project Structure

```
pii-redactor/
├── EVALUATION.md             # Standalone evaluation & benchmark report
├── README.md                 # Project documentation
├── backend/
│   ├── app.py                # FastAPI endpoints & CORS configuration
│   ├── redactor.py           # Main PII detection & overlap priority engine
│   ├── custom_recognizers.py # Address, company & phone regex recognizers
│   ├── fake_generator.py     # Deterministic Faker synthetic replacement engine
│   ├── evaluator.py          # Precision/Recall benchmark & 0% leak audit script
│   ├── sample_ground_truth.json # Ground-truth PII annotations (137 entities)
│   ├── requirements.txt      # Python dependencies
│   ├── uploads/              # Input document upload directory
│   └── outputs/              # Output redacted document directory
└── frontend/
    ├── app/                  # Next.js App Router (layout, page, styles)
    ├── components/           # UI components (Header, UploadZone, ResultsSummary, etc.)
    └── package.json          # Node dependencies and scripts
```