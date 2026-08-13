# PII Redaction Platform

## Overview

A web-based application for detecting and anonymizing Personally Identifiable Information (PII) from DOCX documents.

## Features

- Name Redaction
- Email Redaction
- Phone Number Redaction
- Aadhaar Number Redaction
- Fake Data Replacement
- Entity Count Tracking
- DOCX Upload & Download

## Tech Stack

### Frontend
- Next.js
- React
- Tailwind CSS

### Backend
- FastAPI
- Python 3.10

### NLP & PII Detection
- Microsoft Presidio
- spaCy
- Regex-based Custom Recognizers

### Data Generation
- Faker

### Document Processing
- python-docx

## Approach

The system processes DOCX files using python-docx, detects PII using Microsoft Presidio and custom regex recognizers, generates realistic replacement values using Faker, and produces a downloadable redacted document.

## Future Improvements

- PDF Support
- Authentication
- Audit Logging
- Docker Deployment
- Cloud Hosting
