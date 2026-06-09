import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PhotoFlow AI",
  description: "攝影師多平台發文、自動備份與 AI 分析",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-Hant">
      <body className="min-h-screen bg-neutral-50 text-neutral-900 antialiased">
        {children}
      </body>
    </html>
  );
}
