from docx import Document
from presidio_analyzer import (
    AnalyzerEngine,
    PatternRecognizer,
    Pattern
)
from fake_generator import get_fake_value

# Create analyzer
analyzer = AnalyzerEngine()

# Aadhaar recognizer
aadhaar_pattern = Pattern(
    name="aadhaar_pattern",
    regex=r"\b\d{4}\s\d{4}\s\d{4}\b",
    score=0.9
)

aadhaar_recognizer = PatternRecognizer(
    supported_entity="AADHAAR",
    patterns=[aadhaar_pattern]
)

analyzer.registry.add_recognizer(aadhaar_recognizer)


def redact_text(text):

    results = analyzer.analyze(
        text=text,
        language="en",
        entities=[
            "PERSON",
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "LOCATION",
            "AADHAAR"
        ]
    )

    IGNORE_WORDS = {
        "Name",
        "Email",
        "Phone",
        "Aadhaar"
    }

    filtered_results = []

    for result in results:

        original = text[result.start:result.end]

        if original.strip() in IGNORE_WORDS:
            continue

        if (
            result.entity_type == "PERSON"
            and len(original.split()) < 2
        ):
            continue

        filtered_results.append(result)

    entity_counts = {}

    for result in filtered_results:
        entity_type = result.entity_type

        entity_counts[entity_type] = (
            entity_counts.get(entity_type, 0) + 1
        )

    filtered_results = sorted(
        filtered_results,
        key=lambda x: x.start,
        reverse=True
    )

    for result in filtered_results:

        original = text[result.start:result.end]

        replacement = get_fake_value(
            result.entity_type,
            original
        )

        text = (
            text[:result.start]
            + replacement
            + text[result.end:]
        )

    return text, entity_counts


def redact_docx(path):

    doc = Document(path)

    final_counts = {}

    for paragraph in doc.paragraphs:

        redacted_text, counts = redact_text(
            paragraph.text
        )

        paragraph.text = redacted_text

        for key, value in counts.items():
            final_counts[key] = (
                final_counts.get(key, 0) + value
            )

    output_path = (
        "outputs/redacted_"
        + path.split("/")[-1]
    )

    doc.save(output_path)

    return output_path, final_counts