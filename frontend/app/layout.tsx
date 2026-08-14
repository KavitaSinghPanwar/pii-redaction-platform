import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Privora | Enterprise PII Redaction Platform",
  description: "Automated PII Detection and Realistic Synthetic Redaction Engine for Compliance and Security",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full antialiased dark">
      <body className="min-h-full flex flex-col bg-slate-950 text-slate-100 font-sans">{children}</body>
    </html>
  );
}
