"use client";

import React from "react";

interface ResultsSummaryProps {
  entityCounts: Record<string, number>;
  totalDetected: number;
}

const CATEGORY_CONFIG: Record<
  string,
  { label: string; description: string; iconStyles: string; countStyles: string; iconSvg: React.ReactNode }
> = {
  PERSON: {
    label: "Full Names",
    description: "Promoters, executives, contacts",
    iconStyles: "bg-indigo-50 border-indigo-100 text-indigo-600",
    countStyles: "text-indigo-600",
    iconSvg: (
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
      </svg>
    )
  },
  EMAIL_ADDRESS: {
    label: "Email Addresses",
    description: "Corporate & personal emails",
    iconStyles: "bg-emerald-50 border-emerald-100 text-emerald-600",
    countStyles: "text-emerald-600",
    iconSvg: (
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
      </svg>
    )
  },
  PHONE_NUMBER: {
    label: "Phone Numbers",
    description: "Indian & intl phone numbers",
    iconStyles: "bg-purple-50 border-purple-100 text-purple-600",
    countStyles: "text-purple-600",
    iconSvg: (
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
      </svg>
    )
  },
  COMPANY: {
    label: "Company Names",
    description: "Corporate entities, banks, trusts",
    iconStyles: "bg-amber-50 border-amber-100 text-amber-600",
    countStyles: "text-amber-600",
    iconSvg: (
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5m0 0h5m0 0v-5a2 2 0 012-2h2a2 2 0 012 2v5" />
      </svg>
    )
  },
  ADDRESS: {
    label: "Physical Addresses",
    description: "Registered offices, locations",
    iconStyles: "bg-sky-50 border-sky-100 text-sky-600",
    countStyles: "text-sky-600",
    iconSvg: (
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    )
  },
  SSN: {
    label: "Social Security Numbers",
    description: "US SSN and National IDs",
    iconStyles: "bg-rose-50 border-rose-100 text-rose-600",
    countStyles: "text-rose-600",
    iconSvg: (
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 012-2h2a2 2 0 012 2v1m-4 0h4" />
      </svg>
    )
  },
  CREDIT_CARD: {
    label: "Credit Card Numbers",
    description: "Financial & card numbers",
    iconStyles: "bg-pink-50 border-pink-100 text-pink-600",
    countStyles: "text-pink-600",
    iconSvg: (
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
      </svg>
    )
  },
  DATE_OF_BIRTH: {
    label: "Dates of Birth",
    description: "DOBs & birth dates",
    iconStyles: "bg-teal-50 border-teal-100 text-teal-600",
    countStyles: "text-teal-600",
    iconSvg: (
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
    )
  },
  IP_ADDRESS: {
    label: "IP Addresses",
    description: "Network & server IP addresses",
    iconStyles: "bg-blue-50 border-blue-100 text-blue-600",
    countStyles: "text-blue-600",
    iconSvg: (
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
      </svg>
    )
  }
};

export function ResultsSummary({ entityCounts, totalDetected }: ResultsSummaryProps) {
  return (
    <div className="bg-white border border-slate-200 rounded-lg p-5 mb-6 shadow-xs">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-4 mb-4">
        <div className="border-l-3 border-l-blue-600 pl-3">
          <h3 className="text-base font-bold text-slate-900">
            Detected PII Breakdown
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Overview of detected entities replaced with realistic synthetic values.
          </p>
        </div>
        <div className="mt-3 sm:mt-0 flex items-center space-x-3 bg-slate-50/80 px-3.5 py-2 rounded border border-slate-200">
          <div className="text-2xl font-black text-blue-700 font-mono">
            {totalDetected}
          </div>
          <div className="text-xs text-slate-600 font-medium leading-tight">
            Total Entities <br />
            <span className="text-[11px] text-slate-500 font-normal">Anonymized</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {Object.entries(CATEGORY_CONFIG).map(([key, config]) => {
          const count = entityCounts[key] || 0;
          const isZero = count === 0;
          return (
            <div
              key={key}
              className={`p-3.5 rounded border transition-all ${
                isZero
                  ? "border-slate-200/60 bg-slate-50/50 opacity-55"
                  : "border-slate-200 bg-white shadow-xs hover:border-slate-300"
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center space-x-2">
                  <div className={`p-1.5 rounded border ${isZero ? "bg-slate-100 border-slate-200 text-slate-400" : config.iconStyles}`}>
                    {config.iconSvg}
                  </div>
                  <span className={`text-xs font-semibold ${isZero ? "text-slate-500 font-normal" : "text-slate-900"}`}>
                    {config.label}
                  </span>
                </div>
                <span className={`text-base font-bold font-mono ${isZero ? "text-slate-400 font-normal" : config.countStyles}`}>
                  {count}
                </span>
              </div>
              <p className={`text-[11px] ${isZero ? "text-slate-400" : "text-slate-500"}`}>
                {config.description}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
