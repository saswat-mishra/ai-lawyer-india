import "./globals.css";
import type { Metadata } from "next";
import { SessionProvider } from "@/lib/session";
import { Sidebar } from "@/components/sidebar";

export const metadata: Metadata = {
  title: "AI Lawyer India",
  description:
    "India-first AI lawyer. Citation-faithful, BNS-current, founder & practitioner ready.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <SessionProvider>
          <div className="flex min-h-screen">
            <Sidebar />
            <main className="flex-1 min-w-0">{children}</main>
          </div>
        </SessionProvider>
      </body>
    </html>
  );
}
