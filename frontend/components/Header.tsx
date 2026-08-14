"use client";

import React from "react";

export function Header() {
  return (
    <header className="border-b border-slate-200/90 bg-white/95 backdrop-blur-sm sticky top-0 z-50 shadow-xs">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-7 h-7 rounded bg-blue-600 flex items-center justify-center text-white font-semibold text-xs shadow-xs">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-sm font-bold tracking-tight text-slate-900">
              Privora
            </span>
            <span className="text-xs text-slate-300">|</span>
            <span className="text-xs text-slate-500 font-medium">
              Document Sanitization Engine
            </span>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 text-xs text-slate-600 bg-slate-50 border border-slate-200 px-2.5 py-1 rounded">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-600"></span>
            <span className="font-mono text-[11px]">Deterministic Seed Engine</span>
          </div>
        </div>
      </div>
    </header>
  );
}
