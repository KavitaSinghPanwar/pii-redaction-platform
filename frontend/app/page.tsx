"use client";

import React, { useState } from "react";
import { Header } from "@/components/Header";
import { UploadZone } from "@/components/UploadZone";
import { ProcessingState } from "@/components/ProcessingState";
import { ResultsSummary } from "@/components/ResultsSummary";
import { DocumentPreview } from "@/components/DocumentPreview";
import { EvaluationView } from "@/components/EvaluationView";

type ViewState = "idle" | "processing" | "results" | "error";

const API_BASE_URL = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/$/, "");

export default function Home() {
  const [state, setState] = useState<ViewState>("idle");
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<{
    filename: string;
    output_filename: string;
    total_detected: number;
    entity_counts: Record<string, number>;
    sample_diffs: Array<{ category: string; original: string; redacted: string }>;
  } | null>(null);

  const handleFileProcess = async (file: File) => {
    setState("processing");
    setErrorMsg(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_BASE_URL}/redact-full`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        let detail = "Processing failed on server.";
        try {
          const errJson = await res.json();
          detail = errJson.detail || detail;
        } catch (_) {}
        throw new Error(detail);
      }

      const data = await res.json();
      setAnalysisResult(data);
      setState("results");
    } catch (err: any) {
      setErrorMsg(
        err.message || `Failed to communicate with backend server. Ensure backend is accessible at ${API_BASE_URL}.`
      );
      setState("error");
    }
  };

  const handleDownload = () => {
    if (!analysisResult) return;
    const downloadUrl = `${API_BASE_URL}/download/${analysisResult.output_filename}`;
    const a = document.createElement("a");
    a.href = downloadUrl;
    a.download = analysisResult.output_filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const handleReset = () => {
    setState("idle");
    setAnalysisResult(null);
    setErrorMsg(null);
  };

  return (
    <div className="min-h-screen bg-[#f8f8f6] text-slate-900 flex flex-col font-sans selection:bg-slate-200">
      <Header />

      <main className="flex-1 max-w-5xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Title Section - Product Header style */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight mb-1.5">
            Legal & Financial Document PII Redactor
          </h1>
          <p className="text-sm text-slate-600 max-w-3xl leading-relaxed">
            Detect 9 categories of sensitive PII (Names, Emails, Phones, Companies, Addresses, SSNs, Credit Cards, DOBs, IPs) and replace each span with a consistent, realistic synthetic value.
          </p>
        </div>

        {/* State 1: Idle Upload */}
        {state === "idle" && (
          <UploadZone onFileSelected={handleFileProcess} />
        )}

        {/* State 2: Processing */}
        {state === "processing" && (
          <ProcessingState />
        )}

        {/* State 3: Error */}
        {state === "error" && (
          <div className="bg-white border border-red-200 rounded-lg p-6 max-w-xl mx-auto shadow-sm">
            <div className="flex items-start space-x-3 mb-4">
              <div className="w-8 h-8 rounded bg-red-50 text-red-600 flex items-center justify-center shrink-0">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h3 className="text-sm font-semibold text-slate-900">Processing Error</h3>
                <p className="text-xs text-red-700 mt-1 font-mono bg-red-50 p-2.5 rounded border border-red-100">
                  {errorMsg}
                </p>
              </div>
            </div>
            <div className="text-right pt-2 border-t border-slate-100">
              <button
                onClick={handleReset}
                className="py-1.5 px-4 rounded bg-slate-900 hover:bg-slate-800 text-white text-xs font-medium transition-colors"
              >
                Try Again
              </button>
            </div>
          </div>
        )}

        {/* State 4: Results */}
        {state === "results" && analysisResult && (
          <div>
            <div className="flex items-center justify-between mb-4 bg-white border border-slate-200/80 px-4 py-2.5 rounded-lg shadow-xs">
              <div className="flex items-center space-x-2 text-xs text-slate-600">
                <span className="font-medium text-slate-500">Processed file:</span>
                <span className="font-mono text-slate-900 font-semibold bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
                  {analysisResult.filename}
                </span>
              </div>
              <button
                onClick={handleReset}
                className="text-xs text-slate-600 hover:text-slate-900 flex items-center space-x-1.5 font-medium transition-colors"
              >
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <span>Upload Another File</span>
              </button>
            </div>

            <ResultsSummary
              entityCounts={analysisResult.entity_counts}
              totalDetected={analysisResult.total_detected}
            />

            <DocumentPreview
              sampleDiffs={analysisResult.sample_diffs}
              outputFilename={analysisResult.output_filename}
              onDownload={handleDownload}
            />
          </div>
        )}

        {/* Bottom QA Evaluation Benchmark View */}
        <div className="mt-8">
          <EvaluationView />
        </div>
      </main>

      <footer className="border-t border-slate-200/80 bg-white py-4 text-center text-xs text-slate-500">
        <p>Privora Engine • Enterprise PII Anonymization Platform • Hybrid Presidio + spaCy NER Architecture</p>
      </footer>
    </div>
  );
}