"""
redactor.py
-----------
Main redaction module that reads source text/DOCX documents,
detects PII across 9 categories using Presidio + custom recognizers,
and replaces detected instances with consistent realistic fakes.
"""

from docx import Document
from presidio_analyzer import AnalyzerEngine
from custom_recognizers import register_all_custom_recognizers
from fake_generator import get_fake_value
import os

# Initialize Analyzer Engine and register custom recognizers
analyzer = AnalyzerEngine()
register_all_custom_recognizers(analyzer)

# All supported entities for the assignment
SUPPORTED_ENTITIES = [
    "PERSON",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "COMPANY",
    "ORGANIZATION",
    "ADDRESS",
    "LOCATION",
    "SSN",
    "CREDIT_CARD",
    "DATE_OF_BIRTH",
    "IP_ADDRESS",
    "AADHAAR"
]

IGNORE_WORDS = {
    "Name", "Email", "Phone", "Aadhaar", "Address", "Company", "SSN", "DOB",
    "IP", "Website", "Tel", "Fax", "Date", "Section", "Table", "Page", "Type",
    "Particulars", "General", "Term", "Description", "Offer", "Fresh Issue",
    "Total", "Issuer", "Public", "Equity", "Shares", "Board", "Auditors"
}


import re
from presidio_analyzer import RecognizerResult

LABEL_PREFIX_REGEX = re.compile(
    r"^(?:(?:Registered Office|Corporate Office|Registered and Corporate Office|Address)|[A-Za-z0-9&\s.-]+(?:Limited|LLP|Inc\.?|Corporation|Pvt\.?\s*Ltd\.?))\s*:\s*",
    re.IGNORECASE
)


def filter_and_resolve_overlaps(results, text):
    """
    Filters out noise/labels and resolves overlapping entity spans,
    enforcing container priority (ADDRESS containers override sub-tokens)
    and giving precedence to higher confidence and longer spans.
    """
    filtered = []
    for res in results:
        # If match is an ADDRESS starting with a label prefix (e.g. Registered Office:),
        # adjust start offset so the label prefix remains unredacted.
        if res.entity_type in ("ADDRESS", "LOCATION"):
            matched_str = text[res.start:res.end]
            m = LABEL_PREFIX_REGEX.match(matched_str)
            if m:
                new_start = res.start + m.end()
                if new_start < res.end:
                    res = RecognizerResult(
                        entity_type=res.entity_type,
                        start=new_start,
                        end=res.end,
                        score=res.score
                    )

        original = text[res.start:res.end].strip()
        if original in IGNORE_WORDS:
            continue
        if len(original) < 2:
            continue
        # Avoid single-word PERSON detections if low score
        if res.entity_type == "PERSON" and len(original.split()) < 2 and res.score < 0.90:
            continue
        filtered.append(res)

    # Sort key order:
    # 1. ADDRESS / LOCATION entities get container precedence (type_priority = 10) over sub-tokens (5)
    # 2. Score descending
    # 3. Span length descending
    def sort_key(r):
        type_priority = 10 if r.entity_type in ("ADDRESS", "LOCATION") else 5
        return (type_priority, r.score, r.end - r.start)

    sorted_res = sorted(filtered, key=sort_key, reverse=True)

    kept = []
    for r in sorted_res:
        overlap = False
        for k in kept:
            # Overlap check: spans overlap if not completely disjoint
            if not (r.end <= k.start or r.start >= k.end):
                overlap = True
                break
        if not overlap:
            kept.append(r)

    # Return sorted by start position ascending for orderly processing
    return sorted(kept, key=lambda r: r.start)


def redact_text(text: str):
    """
    Analyzes text for PII entities, replaces them with realistic fakes,
    and returns (redacted_text, entity_counts).
    """
    if not text or not text.strip():
        return text, {}

    results = analyzer.analyze(
        text=text,
        language="en",
        entities=SUPPORTED_ENTITIES
    )

    filtered_results = filter_and_resolve_overlaps(results, text)

    entity_counts = {}
    for res in filtered_results:
        entity_type = res.entity_type
        # Normalize entity names
        if entity_type == "LOCATION":
            entity_type = "ADDRESS"
        elif entity_type == "ORGANIZATION":
            entity_type = "COMPANY"

        entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1

    # Replace from end of text to start to keep character offsets valid
    sorted_for_replacement = sorted(
        filtered_results,
        key=lambda x: x.start,
        reverse=True
    )

    redacted_text = text
    for res in sorted_for_replacement:
        original = text[res.start:res.end]

        entity_type = res.entity_type
        if entity_type == "LOCATION":
            entity_type = "ADDRESS"
        elif entity_type == "ORGANIZATION":
            entity_type = "COMPANY"

        replacement = get_fake_value(entity_type, original)
        redacted_text = (
            redacted_text[:res.start]
            + replacement
            + redacted_text[res.end:]
        )

    return redacted_text, entity_counts


def redact_docx(path: str, output_dir: str = "outputs"):
    """
    Reads a .docx file, detects PII in paragraphs and tables,
    replaces PII with fakes, saves redacted document, and returns (output_path, total_entity_counts).
    """
    doc = Document(path)
    total_entity_counts = {}

    # 1. Process document paragraphs
    for paragraph in doc.paragraphs:
        if paragraph.text and paragraph.text.strip():
            redacted, counts = redact_text(paragraph.text)
            paragraph.text = redacted
            for k, v in counts.items():
                total_entity_counts[k] = total_entity_counts.get(k, 0) + v

    # 2. Process table cells
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    if paragraph.text and paragraph.text.strip():
                        redacted, counts = redact_text(paragraph.text)
                        paragraph.text = redacted
                        for k, v in counts.items():
                            total_entity_counts[k] = total_entity_counts.get(k, 0) + v

    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(path)
    output_path = os.path.join(output_dir, "redacted_" + filename)
    doc.save(output_path)

    return output_path, total_entity_counts