"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);

  const uploadFile = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(
      "http://127.0.0.1:8000/redact",
      {
        method: "POST",
        body: formData,
      }
    );

    const blob = await response.blob();

    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "redacted.docx";
    a.click();
  };

  return (
    <main className="min-h-screen bg-slate-100 flex items-center justify-center">
      <div className="bg-white shadow-xl rounded-2xl p-10 w-[700px]">

        <h1 className="text-4xl font-bold mb-3">
          PII Redaction Platform
        </h1>

        <p className="text-gray-500 mb-8">
          Detect and anonymize sensitive information
          inside enterprise documents.
        </p>

        <input
          type="file"
          accept=".docx"
          onChange={(e) =>
            setFile(e.target.files?.[0] || null)
          }
          className="mb-5"
        />

        <button
          onClick={uploadFile}
          className="bg-black text-white px-6 py-3 rounded-lg"
        >
          Upload & Redact
        </button>
      </div>
    </main>
  );
}