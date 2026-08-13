"use client";

import React, { useState, useRef } from "react";

interface UploadZoneProps {
  onFileSelected: (file: File) => void;
  disabled?: boolean;
}

export function UploadZone({ onFileSelected, disabled }: UploadZoneProps) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setSelectedFile(file);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
    }
  };

  const handleRemove = () => {
    setSelectedFile(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  const handleSubmit = () => {
    if (selectedFile) {
      onFileSelected(selectedFile);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + " bytes";
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB";
    else return (bytes / 1048576).toFixed(1) + " MB";
  };

  return (
    <div className="w-full">
      {!selectedFile ? (
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          className={`border border-dashed rounded-lg p-8 text-center cursor-pointer transition-all duration-150 ${
            dragActive
              ? "border-slate-900 bg-slate-100/80"
              : "border-slate-300 hover:border-slate-400 bg-white shadow-xs"
          } ${disabled ? "opacity-50 pointer-events-none" : ""}`}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".docx,.pdf,.txt"
            onChange={handleChange}
            className="hidden"
          />
          <div className="w-10 h-10 mx-auto mb-3 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-600">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <h3 className="text-sm font-semibold text-slate-900 mb-1">
            Drop document here, or <span className="text-slate-900 underline underline-offset-2 font-bold">select file</span>
          </h3>
          <p className="text-xs text-slate-500 mb-3">
            Supports DOCX, PDF, or TXT documents containing legal or financial records.
          </p>
          <div className="flex items-center justify-center space-x-2 text-[11px] text-slate-400 font-mono">
            <span>Max size: 25MB</span>
            <span>•</span>
            <span>Local & Secure Processing</span>
          </div>
        </div>
      ) : (
        <div className="bg-white border border-slate-200 rounded-lg p-5 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-700 font-bold text-xs uppercase font-mono">
                {selectedFile.name.split(".").pop()}
              </div>
              <div>
                <h4 className="text-xs font-semibold text-slate-900 truncate max-w-xs sm:max-w-md">
                  {selectedFile.name}
                </h4>
                <p className="text-[11px] text-slate-500 mt-0.5">
                  {formatFileSize(selectedFile.size)} • Ready for anonymization
                </p>
              </div>
            </div>
            <button
              onClick={handleRemove}
              disabled={disabled}
              className="text-slate-500 hover:text-red-600 p-1.5 rounded hover:bg-slate-100 transition-colors text-xs font-medium flex items-center space-x-1"
            >
              <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              <span>Remove</span>
            </button>
          </div>

          <button
            onClick={handleSubmit}
            disabled={disabled}
            className="w-full py-2.5 px-4 rounded bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs transition-colors flex items-center justify-center space-x-2 shadow-xs disabled:opacity-50 cursor-pointer"
          >
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <span>Start Redaction & Synthetic Replacement</span>
          </button>
        </div>
      )}
    </div>
  );
}
