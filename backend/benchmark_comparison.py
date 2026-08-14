"""
benchmark_comparison.py
-----------------------
Runs empirical comparison across spaCy models (en_core_web_sm, en_core_web_md, en_core_web_lg)
measuring package size, RSS peak memory usage, load time, inference runtime,
and PII detection metrics (Precision, Recall, F1 Score) per entity category.
"""

import sys
import os
import time
import json
import subprocess

MODELS = ["en_core_web_sm", "en_core_web_md", "en_core_web_lg"]

RUNNER_SCRIPT = """
import sys
import os
import time
import gc
import json
import re
import psutil
import spacy

from docx import Document
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from custom_recognizers import register_all_custom_recognizers
from redactor import filter_and_resolve_overlaps, SUPPORTED_ENTITIES
from evaluator import load_ground_truth, extract_docx_text

model_name = sys.argv[1]

def get_model_size_mb(m):
    nlp = spacy.load(m)
    import importlib.util
    spec = importlib.util.find_spec(m)
    if spec and spec.origin:
        pkg_dir = os.path.dirname(spec.origin)
        total_bytes = sum(os.path.getsize(os.path.join(root, f)) for root, dirs, files in os.walk(pkg_dir) for f in files)
        return total_bytes / (1024 * 1024)
    return 0.0

process = psutil.Process(os.getpid())
gc.collect()
mem_before = process.memory_info().rss / (1024 * 1024)

# Measure model load time
t0 = time.time()
config = {"nlp_engine_name": "spacy", "models": [{"lang_code": "en", "model_name": model_name}]}
provider = NlpEngineProvider(nlp_configuration=config)
nlp_engine = provider.create_engine()
analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
register_all_custom_recognizers(analyzer)
t1 = time.time()
load_time = t1 - t0
mem_after_load = process.memory_info().rss / (1024 * 1024)

# Measure inference runtime and peak memory
docx_path = os.path.join("uploads", "Red_Herring_Prospectus.docx")
gt_path = "sample_ground_truth.json"
gt_data = load_ground_truth(gt_path)
doc_text = extract_docx_text(docx_path)

t2 = time.time()
raw_results = analyzer.analyze(text=doc_text, language="en", entities=SUPPORTED_ENTITIES)
detected_results = filter_and_resolve_overlaps(raw_results, doc_text)
t3 = time.time()
inference_time = t3 - t2
peak_mem = process.memory_info().rss / (1024 * 1024)

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

all_categories = [
    "PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "COMPANY", "ADDRESS",
    "SSN", "CREDIT_CARD", "DATE_OF_BIRTH", "IP_ADDRESS"
]
metrics_per_type = {}
total_tp = 0
total_fp = 0
total_fn = 0

def norm_s(s):
    return re.sub(r"[\\s\\+\\.-]", "", s.lower())

for cat in all_categories:
    gt_set = set(gt_data.get(cat, []))
    det_set = detected_by_type.get(cat, set())
    tp = 0
    matched_gt = set()
    matched_det = set()
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
    p = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    r = tp / (tp + fn) if (tp + fn) > 0 else 1.0
    f1 = (2 * p * r) / (p + r) if (p + r) > 0 else 0.0
    metrics_per_type[cat] = {
        "TP": tp, "FP": fp, "FN": fn,
        "precision": round(p, 4),
        "recall": round(r, 4),
        "f1_score": round(f1, 4)
    }

ov_p = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
ov_r = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
ov_f1 = (2 * ov_p * ov_r) / (ov_p + ov_r) if (ov_p + ov_r) > 0 else 0.0

pkg_size = get_model_size_mb(model_name)

result_payload = {
    "model": model_name,
    "pkg_size_mb": round(pkg_size, 2),
    "mem_before_mb": round(mem_before, 2),
    "mem_after_load_mb": round(mem_after_load, 2),
    "peak_mem_mb": round(peak_mem, 2),
    "load_time_sec": round(load_time, 3),
    "inference_time_sec": round(inference_time, 3),
    "total_runtime_sec": round(load_time + inference_time, 3),
    "overall": {
        "precision": round(ov_p, 4),
        "recall": round(ov_r, 4),
        "f1_score": round(ov_f1, 4)
    },
    "per_type": metrics_per_type
}
print(json.dumps(result_payload))
"""

def run_benchmarks():
    results = []
    for model in MODELS:
        cmd = [sys.executable, "-c", RUNNER_SCRIPT, model]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode == 0:
            data = json.loads(proc.stdout.strip())
            results.append(data)
        else:
            print(f"Error benchmarking {model}:\n{proc.stderr}")
    return results

def format_prf(metrics_dict):
    p = metrics_dict["precision"] * 100
    r = metrics_dict["recall"] * 100
    f1 = metrics_dict["f1_score"] * 100
    return f"{p:.1f}% / {r:.1f}% / {f1:.1f}%"

def generate_table(results):
    lines = [
        "| Model | Package Size | Peak RSS RAM | Load Time | Total Runtime | Names (P/R/F1) | Companies (P/R/F1) | Addresses (P/R/F1) | Overall (P/R/F1) | Render 512MB Status |",
        "|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|"
    ]
    for r in results:
        m = r["model"]
        size = f"{r['pkg_size_mb']:.1f} MB"
        peak_mem = f"{r['peak_mem_mb']:.1f} MB"
        load_t = f"{r['load_time_sec']:.3f} s"
        total_t = f"{r['total_runtime_sec']:.3f} s"
        names = format_prf(r["per_type"]["PERSON"])
        comps = format_prf(r["per_type"]["COMPANY"])
        addrs = format_prf(r["per_type"]["ADDRESS"])
        ov = format_prf(r["overall"])
        status = "**PASSED** (< 450 MB)" if r["peak_mem_mb"] < 450 else "**FAILED (OOM > 512 MB)**"
        lines.append(
            f"| `{m}` | {size} | {peak_mem} | {load_t} | {total_t} | {names} | {comps} | {addrs} | {ov} | {status} |"
        )
    return "\n".join(lines)

if __name__ == "__main__":
    res = run_benchmarks()
    print("=== SPA CY MODEL COMPARISON BENCHMARK RESULTS ===")
    print(json.dumps(res, indent=2))
    print("\n=== MARKDOWN COMPARISON TABLE ===")
    print(generate_table(res))
