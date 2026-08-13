"use client";

import React from "react";

interface DiffItem {
  category: string;
  original: string;
  redacted: string;
}

interface DocumentPreviewProps {
  sampleDiffs: DiffItem[];
  outputFilename: string;
  onDownload: () => void;
}

export function DocumentPreview({
  sampleDiffs,
  outputFilename,
  onDownload,
}: DocumentPreviewProps) {
  return (
    <div className="bg-white border border-slate-200 rounded-lg p-5 mb-6 shadow-xs">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-4 mb-4">
        <div className="border-l-3 border-l-blue-600 pl-3">
          <h3 className="text-base font-bold text-slate-900">
            Replacement Preview & Verification
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Sample diff showing original detected spans replaced with consistent synthetic values.
          </p>
        </div>
        <button
          onClick={onDownload}
          className="mt-3 sm:mt-0 py-2.5 px-4.5 rounded bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs transition-colors flex items-center space-x-2 shadow-xs cursor-pointer"
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          <span>Download Redacted .DOCX</span>
        </button>
      </div>

      {sampleDiffs.length > 0 ? (
        <div className="overflow-x-auto rounded border border-slate-200 bg-white">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 font-mono text-[11px] font-semibold border-b border-slate-200">
              <tr>
                <th className="py-2.5 px-3">Category</th>
                <th className="py-2.5 px-3">Original PII (Detected)</th>
                <th className="py-2.5 px-3">Synthetic Replacement (Redacted)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-800">
              {sampleDiffs.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-50/60 transition-colors">
                  <td className="py-2 px-3 font-mono">
                    <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-700 border border-slate-200">
                      {item.category}
                    </span>
                  </td>
                  <td className="py-2 px-3 font-mono text-red-700 bg-red-50/40">
                    <span className="line-through opacity-90">{item.original}</span>
                  </td>
                  <td className="py-2 px-3 font-mono text-slate-900 bg-slate-50 font-semibold">
                    <span>{item.redacted}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="p-6 text-center text-slate-500 text-xs bg-slate-50 rounded border border-slate-200">
          No individual entity diff snippets available for display.
        </div>
      )}
    </div>
  );
}
