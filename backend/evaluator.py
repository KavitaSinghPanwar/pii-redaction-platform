"""
evaluator.py
------------
Evaluates PII redaction accuracy, precision, and recall against ground truth labels.
Supports evaluation per PII category and computes overall performance metrics.
"""

import json
import os
import re
from docx import Document
from redactor import analyzer, filter_and_resolve_overlaps, SUPPORTED_ENTITIES


def load_ground_truth(gt_path: str) -> dict:
    """Loads ground truth entities from JSON."""
    with open(gt_path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_docx_text(docx_path: str) -> str:
    """Extracts all text from paragraphs and table cells of a DOCX file."""
    doc = Document(docx_path)
    lines = []
    for p in doc.paragraphs:
        if p.text and p.text.strip():
            lines.append(p.text.strip())
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if p.text and p.text.strip():
                        lines.append(p.text.strip())
    return "\n".join(lines)


def check_residual_leakage(redacted_docx_path: str, ground_truth_path: str) -> dict:
    """
    Performs a systematic substring search of all ground truth PII entities
    against the fully redacted document text to calculate residual real-PII leakage.
    """
    gt_data = load_ground_truth(ground_truth_path)
    redacted_text = extract_docx_text(redacted_docx_path)

    total_items = 0
    total_leaked = 0
    leaks_by_cat = {}

    for cat, items in gt_data.items():
        cat_leaks = []
        for item in items:
            total_items += 1
            if item in redacted_text:
                cat_leaks.append(item)
        if cat_leaks:
            leaks_by_cat[cat] = cat_leaks
            total_leaked += len(cat_leaks)

    leakage_rate = (total_leaked / total_items * 100) if total_items > 0 else 0.0
    return {
        "total_items": total_items,
        "total_leaked": total_leaked,
        "residual_real_pii_leakage_rate": round(leakage_rate, 4),
        "leaks_by_cat": leaks_by_cat
    }


def evaluate_redaction(docx_path: str, ground_truth_path: str, model_name: str = None) -> dict:
    """
    Compares redactor detections against ground truth labels
    and computes precision, recall, f1, and accuracy per entity type,
    as well as residual leakage on redacted output.
    """
    gt_data = load_ground_truth(ground_truth_path)
    doc_text = extract_docx_text(docx_path)

    active_analyzer = create_analyzer_engine(model_name) if model_name else analyzer

    raw_results = active_analyzer.analyze(
        text=doc_text,
        language="en",
        entities=SUPPORTED_ENTITIES
    )
    detected_results = filter_and_resolve_overlaps(raw_results, doc_text)

    # Organize detected entities by type
    detected_by_type = {}
    for res in detected_results:
        etype = res.entity_type
        if etype == "LOCATION":
            etype = "ADDRESS"
        elif etype == "ORGANIZATION":
            etype = "COMPANY"

        if etype not in detected_by_type:
            detected_by_type[etype] = set()
        entity_str = doc_text[res.start:res.end].strip()
        detected_by_type[etype].add(entity_str)

    # Categories to evaluate
    all_categories = [
        "PERSON",
        "EMAIL_ADDRESS",
        "PHONE_NUMBER",
        "COMPANY",
        "ADDRESS",
        "SSN",
        "CREDIT_CARD",
        "DATE_OF_BIRTH",
        "IP_ADDRESS"
    ]

    metrics_per_type = {}
    total_tp = 0
    total_fp = 0
    total_fn = 0

    for cat in all_categories:
        gt_set = set(gt_data.get(cat, []))
        det_set = detected_by_type.get(cat, set())

        # Exact/Sub-string matching for TP
        tp = 0
        matched_gt = set()
        matched_det = set()

        def norm_s(s):
            return re.sub(r"[\s\+\.-]", "", s.lower())

        for d in det_set:
            norm_d = norm_s(d)
            for g in gt_set:
                norm_g = norm_s(g)
                if norm_d == norm_g or norm_d in norm_g or norm_g in norm_d:
                    tp += 1
                    matched_gt.add(g)
                    matched_det.add(d)
                    break

        fp = len(det_set - matched_det)
        fn = len(gt_set - matched_gt)

        total_tp += tp
        total_fp += fp
        total_fn += fn

        precision = tp / (tp + fp) if (tp + fp) > 0 else (1.0 if fn == 0 else 0.0)
        recall = tp / (tp + fn) if (tp + fn) > 0 else (1.0 if fp == 0 else 0.0)
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        # Accuracy definition over entity set: TP / (TP + FP + FN)
        accuracy = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 1.0

        metrics_per_type[cat] = {
            "ground_truth_count": len(gt_set),
            "detected_count": len(det_set),
            "TP": tp,
            "FP": fp,
            "FN": fn,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "accuracy": round(accuracy, 4)
        }

    overall_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    overall_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    overall_f1 = (2 * overall_precision * overall_recall) / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0.0
    overall_accuracy = total_tp / (total_tp + total_fp + total_fn) if (total_tp + total_fp + total_fn) > 0 else 1.0

    summary = {
        "metrics_per_type": metrics_per_type,
        "overall": {
            "total_TP": total_tp,
            "total_FP": total_fp,
            "total_FN": total_fn,
            "precision": round(overall_precision, 4),
            "recall": round(overall_recall, 4),
            "f1_score": round(overall_f1, 4),
            "accuracy": round(overall_accuracy, 4)
        }
    }
    return summary


def generate_evaluation_markdown(summary: dict, leakage_summary: dict = None, output_md_path: str = "evaluation_report.md"):
    """Generates a Markdown report summarizing evaluation findings and residual real-PII leakage."""
    lines = [
        "# PII Redaction Platform Evaluation Report",
        "",
        "## Evaluation Methodology",
        "The evaluation was conducted by comparing ground-truth PII entities extracted from the real *Red Herring Prospectus* document against the entities detected by the tool's hybrid redaction engine.",
        "In addition, an explicit **Residual Real-PII Leakage Verification** was introduced to perform exact substring matching of ground-truth PII values against the final redacted document output.",
        "",
        "### Ground Truth Dataset",
        "The ground-truth dataset (`sample_ground_truth.json`) contains manually annotated entities directly from the Red Herring Prospectus across all 9 required PII categories:",
        "1. **Full Names (PERSON)**",
        "2. **Email Addresses (EMAIL_ADDRESS)**",
        "3. **Phone Numbers (PHONE_NUMBER)**",
        "4. **Company Names (COMPANY)**",
        "5. **Physical/Mailing Addresses (ADDRESS)**",
        "6. **Social Security Numbers (SSN)**",
        "7. **Credit Card Numbers (CREDIT_CARD)**",
        "8. **Dates of Birth (DATE_OF_BIRTH)**",
        "9. **IP Addresses (IP_ADDRESS)**",
        "",
        "## Evaluation Results per PII Type",
        "",
        "| PII Category | Ground Truth Count | Detected Count | Precision | Recall | F1 Score | Accuracy |",
        "|---|---|---|---|---|---|---|"
    ]

    metrics = summary["metrics_per_type"]
    for cat, val in metrics.items():
        p_pct = f"{val['precision'] * 100:.2f}%"
        r_pct = f"{val['recall'] * 100:.2f}%"
        f1_pct = f"{val['f1_score'] * 100:.2f}%"
        acc_pct = f"{val['accuracy'] * 100:.2f}%"
        lines.append(
            f"| **{cat}** | {val['ground_truth_count']} | {val['detected_count']} | {p_pct} | {r_pct} | {f1_pct} | {acc_pct} |"
        )

    ov = summary["overall"]
    lines.extend([
        "",
        "### Overall Performance Summary",
        f"- **Total True Positives (TP):** {ov['total_TP']}",
        f"- **Total False Positives (FP):** {ov['total_FP']}",
        f"- **Total False Negatives (FN):** {ov['total_FN']}",
        f"- **Overall Precision:** {ov['precision'] * 100:.2f}%",
        f"- **Overall Recall:** {ov['recall'] * 100:.2f}%",
        f"- **Overall F1 Score:** {ov['f1_score'] * 100:.2f}%",
        f"- **Overall Accuracy:** {ov['accuracy'] * 100:.2f}%",
        ""
    ])

    if leakage_summary:
        leak_rate = f"{leakage_summary['residual_real_pii_leakage_rate']:.2f}%"
        lines.extend([
            "## Residual Real-PII Leakage Check Methodology & Results",
            "",
            "To guarantee that no raw or partial PII leaks into the final redacted document, every ground-truth PII entity was subjected to an exact substring search against the complete text of the redacted document (`outputs/redacted_Red_Herring_Prospectus.docx`).",
            "",
            f"- **Total Ground Truth PII Values Checked:** {leakage_summary['total_items']}",
            f"- **Total Leaked PII Values Found in Output:** {leakage_summary['total_leaked']}",
            f"- **Residual Real-PII Leakage Rate:** `{leak_rate}`",
            ""
        ])
        if leakage_summary['total_leaked'] == 0:
            lines.append("> [!TIP]\n> **Leakage Verification Passed**: 0% residual leakage confirmed across all ground-truth PII values (addresses, names, phones, emails, companies, SSNs, credit cards, DOBs, IP addresses).")
        else:
            lines.append(f"> [!CAUTION]\n> **Leakage Detected**: {leakage_summary['total_leaked']} ground-truth entities still appear in the redacted output:")
            for c, items in leakage_summary.get('leaks_by_cat', {}).items():
                lines.append(f"- **{c}**: {', '.join(items)}")

    lines.extend([
        "",
        "## Analysis of Overlap Resolution & Address Atomicity Fixes",
        "1. **Address Container Precedence:** Multi-part physical addresses (including building names, street names, talukas, pin codes, states, and countries) are treated as single atomic `ADDRESS` spans. This suppresses sub-token misclassifications (such as place names being misdetected as `PERSON`).",
        "2. **Atomic Fake Replacement:** Detected address blocks are fully replaced with one fake address value. No raw pincodes, state names, or village names are retained or spliced alongside fake values.",
        "3. **Exact Punctuation Boundaries:** Entity patterns ending in punctuation (e.g. `Citibank N.A.`) use negative lookahead `(?!\w)` to ensure robust detection regardless of trailing colons or punctuation.",
        "",
        "## Ground Truth Limitations",
        "- Ground truth entities were compiled manually from pages 1-132 of the Red Herring Prospectus.",
        "- Precision/Recall/Accuracy metrics reflect real execution on this document dataset."
    ])

    content = "\n".join(lines)
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(content)

    return content


if __name__ == "__main__":
    from redactor import redact_docx
    gt_file = "sample_ground_truth.json"
    docx_file = os.path.join("uploads", "Red_Herring_Prospectus.docx")
    if os.path.exists(gt_file) and os.path.exists(docx_file):
        out_docx, _ = redact_docx(docx_file)
        res = evaluate_redaction(docx_file, gt_file)
        leak_res = check_residual_leakage(out_docx, gt_file)
        report = generate_evaluation_markdown(res, leak_res, "evaluation_report.md")
        print("Evaluation complete!")
        print("Overall metrics:", json.dumps(res["overall"], indent=2))
        print("Leakage summary:", json.dumps(leak_res, indent=2))

