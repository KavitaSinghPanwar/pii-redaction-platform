# Privora - PII Redaction Platform

## Overview

Privora is a web-based application that detects and anonymizes Personally Identifiable Information (PII) from DOCX documents.

The system automatically identifies sensitive information and replaces it with realistic fake values while preserving document structure.

---

## Features

- Name Redaction
- Email Redaction
- Phone Number Redaction
- Aadhaar Number Redaction
- Fake Data Replacement using Faker
- Entity Count Tracking
- DOCX Upload & Download
- FastAPI Backend
- Next.js Frontend

---

## Tech Stack

### Frontend
- Next.js
- React
- Tailwind CSS

### Backend
- FastAPI
- Python 3.10

### PII Detection
- Microsoft Presidio
- spaCy
- Custom Regex Recognizers

### Fake Data Generation
- Faker

### Document Processing
- python-docx

---

## Supported PII Types

| Entity | Example |
|----------|----------|
| PERSON | Kavita Singh Panwar |
| EMAIL_ADDRESS | kavita@gmail.com |
| PHONE_NUMBER | 9876543210 |
| AADHAAR | 1234 5678 9012 |

---

## Example

Input:

```
Name: Kavita Singh Panwar
Email: kavita@gmail.com
Phone: 9876543210
Aadhaar: 1234 5678 9012
```

Output:

```
Name: Jessica Jones
Email: thomasherrera@example.net
Phone: +91 7372732827
Aadhaar: XXXX XXXX XXXX
```

---

## Entity Tracking

Example backend output:

```
Detected Entities:
{
  "PERSON": 1,
  "EMAIL_ADDRESS": 1,
  "PHONE_NUMBER": 1,
  "AADHAAR": 1
}
```

---

## Installation

### Backend

```bash
cd backend

source venv/bin/activate

pip install -r requirements.txt

python -m uvicorn app:app --reload
```

Backend runs on:

```
http://127.0.0.1:8000
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```
http://localhost:3000
```

---

## Future Improvements

- PDF Support
- User Authentication
- Audit Logging
- Docker Deployment
- Cloud Deployment

---

## Author

Kavita Singh Panwar