"use client";

import React, { useEffect, useState } from "react";

const STEPS = [
  "Uploading document to secure processing pipeline...",
  "Running Presidio & spaCy hybrid NER detection engine...",
  "Analyzing text spans for Names, Emails, Phones, Addresses, Companies, SSNs, Cards, DOBs, IPs...",
  "Generating deterministic, realistic synthetic replacements...",
  "Compiling redacted DOCX document structure..."
];

export function ProcessingState() {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 1200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full bg-white border border-slate-200 rounded-lg p-6 text-center shadow-xs">
      <div className="relative w-12 h-12 mx-auto mb-4 flex items-center justify-center">
        <div className="w-10 h-10 rounded-full border-2 border-slate-200 border-t-slate-900 animate-spin"></div>
        <div className="absolute text-slate-900 font-mono text-[10px] font-bold">
          {Math.min(100, (currentStep + 1) * 20)}%
        </div>
      </div>

      <h3 className="text-sm font-semibold text-slate-900 mb-1">
        Processing Document
      </h3>
      <p className="text-xs text-slate-600 font-mono mb-4 transition-all duration-300 min-h-[1.25rem]">
        {STEPS[currentStep]}
      </p>

      {/* Progress Bar */}
      <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden mb-4">
        <div
          className="bg-slate-900 h-full transition-all duration-500 ease-out"
          style={{ width: `${(currentStep + 1) * 20}%` }}
        ></div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px] text-slate-500 font-mono border-t border-slate-100 pt-3">
        <div className="flex items-center space-x-1.5 justify-center">
          <span className="w-1.5 h-1.5 rounded-full bg-slate-700"></span>
          <span>NER Engine: Active</span>
        </div>
        <div className="flex items-center space-x-1.5 justify-center">
          <span className="w-1.5 h-1.5 rounded-full bg-slate-700"></span>
          <span>Regex Engine: Active</span>
        </div>
        <div className="flex items-center space-x-1.5 justify-center">
          <span className="w-1.5 h-1.5 rounded-full bg-slate-700"></span>
          <span>Seed Faker: Active</span>
        </div>
        <div className="flex items-center space-x-1.5 justify-center">
          <span className="w-1.5 h-1.5 rounded-full bg-slate-700"></span>
          <span>Categories: 9/9</span>
        </div>
      </div>
    </div>
  );
}
