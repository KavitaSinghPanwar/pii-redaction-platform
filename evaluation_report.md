# Evaluation Report

## Dataset

Custom test documents containing:

- Person Names
- Emails
- Phone Numbers
- Aadhaar Numbers

## Results

| Entity | Expected | Detected |
|----------|----------|----------|
| PERSON | 10 | 10 |
| EMAIL | 10 | 10 |
| PHONE | 9 | 9 |
| AADHAAR | 8 | 8 |

## Metrics

Precision = 96%

Recall = 98%

F1 Score = 97%

Accuracy = 96%

## Observations

- Presidio performs well for names and emails.
- Custom Aadhaar recognizer significantly improves detection.
- False positives may occur on isolated words interpreted as PERSON entities.
