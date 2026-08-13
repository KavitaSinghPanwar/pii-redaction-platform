from docx import Document
from presidio_analyzer import AnalyzerEngine
from fake_generator import get_fake_value

analyzer = AnalyzerEngine()

def redact_text(text):

    results = analyzer.analyze(
        text=text,
        language="en"
    )

    results = sorted(
        results,
        key=lambda x: x.start,
        reverse=True
    )

    for result in results:

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

    return text


def redact_docx(path):

    doc = Document(path)

    for paragraph in doc.paragraphs:
        paragraph.text = redact_text(paragraph.text)

    output_path = (
        "outputs/redacted_"
        + path.split("/")[-1]
    )

    doc.save(output_path)

    return output_path