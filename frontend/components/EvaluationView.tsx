"use client";

import React, { useState } from "react";

interface EvalMetrics {
  precision: number;
  recall: number;
  f1_score: number;
  accuracy: number;
  ground_truth_count: number;
  detected_count: number;
}

export function EvaluationView() {
  const [loading, setLoading] = useState(false);
  const [reportData, setReportData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchEvaluation = async () => {
    setLoading(true);
    setError(null);
    const apiBase = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/$/, "");
    try {
      const res = await fetch(`${apiBase}/evaluate`);
      if (!res.ok) {
        throw new Error(`Evaluation failed with status ${res.status}`);
      }
      const data = await res.json();
      setReportData(data);
    } catch (err: any) {
      setError(err.message || "Failed to load evaluation benchmark report.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white border border-slate-200 rounded-lg p-5 mb-6 shadow-xs">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-4 mb-4">
        <div className="border-l-3 border-l-blue-600 pl-3">
          <h3 className="text-base font-bold text-slate-900">
            Quality Assurance & Ground Truth Benchmark
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Evaluated against ground truth labels from the Red Herring Prospectus.
          </p>
        </div>
        <button
          onClick={fetchEvaluation}
          disabled={loading}
          className="mt-3 sm:mt-0 py-2 px-3.5 rounded bg-slate-100 hover:bg-slate-200/80 text-slate-800 border border-slate-300 font-semibold text-xs transition-colors flex items-center space-x-1.5 disabled:opacity-50 cursor-pointer"
        >
          {loading ? (
            <span>Computing...</span>
          ) : (
            <>
              <svg className="w-3.5 h-3.5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <span>{reportData ? "Refresh Benchmark" : "Run Live Evaluation"}</span>
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded text-red-700 text-xs mb-4">
          {error}
        </div>
      )}

      {reportData && (
        <div>
          {/* Overall Key Performance Metrics */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
            <div className="p-3 rounded bg-slate-50/80 border border-slate-200 text-center">
              <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider font-semibold">Precision</span>
              <div className="text-xl font-black text-emerald-700 font-mono mt-0.5">
                {(reportData.overall.precision * 100).toFixed(1)}%
              </div>
            </div>
            <div className="p-3 rounded bg-slate-50/80 border border-slate-200 text-center">
              <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider font-semibold">Recall</span>
              <div className="text-xl font-black text-blue-700 font-mono mt-0.5">
                {(reportData.overall.recall * 100).toFixed(1)}%
              </div>
            </div>
            <div className="p-3 rounded bg-slate-50/80 border border-slate-200 text-center">
              <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider font-semibold">F1 Score</span>
              <div className="text-xl font-black text-indigo-700 font-mono mt-0.5">
                {(reportData.overall.f1_score * 100).toFixed(1)}%
              </div>
            </div>
            <div className="p-3 rounded bg-slate-50/80 border border-slate-200 text-center">
              <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider font-semibold">Accuracy</span>
              <div className="text-xl font-black text-amber-700 font-mono mt-0.5">
                {(reportData.overall.accuracy * 100).toFixed(1)}%
              </div>
            </div>
          </div>

          {/* Breakdown Table */}
          <div className="overflow-x-auto rounded border border-slate-200 bg-white">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] font-semibold border-b border-slate-200">
                <tr>
                  <th className="py-2.5 px-3">PII Category</th>
                  <th className="py-2.5 px-3 text-center">Ground Truth</th>
                  <th className="py-2.5 px-3 text-center">Detected</th>
                  <th className="py-2.5 px-3 text-right">Precision</th>
                  <th className="py-2.5 px-3 text-right">Recall</th>
                  <th className="py-2.5 px-3 text-right">F1 Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-800">
                {Object.entries(reportData.metrics_per_type).map(([cat, m]: [string, any]) => (
                  <tr key={cat} className="hover:bg-slate-50/60 transition-colors">
                    <td className="py-2 px-3 font-bold text-slate-900">{cat}</td>
                    <td className="py-2 px-3 text-center text-slate-600">{m.ground_truth_count}</td>
                    <td className="py-2 px-3 text-center text-slate-600">{m.detected_count}</td>
                    <td className="py-2 px-3 text-right text-emerald-700 font-bold">{(m.precision * 100).toFixed(1)}%</td>
                    <td className="py-2 px-3 text-right text-blue-700 font-bold">{(m.recall * 100).toFixed(1)}%</td>
                    <td className="py-2 px-3 text-right text-indigo-700 font-bold">{(m.f1_score * 100).toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
