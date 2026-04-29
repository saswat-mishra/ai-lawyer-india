"use client";
import { useState } from "react";
import { Search } from "lucide-react";
import { api, ChatResponse } from "@/lib/api";
import { AnswerRenderer } from "@/components/answer-renderer";
import { ConfidenceBadge } from "@/components/confidence-badge";
import { StageLoader } from "@/components/stage-loader";

/**
 * Practitioner research workbench.
 * Three-pane: query / answer / sources rail.
 * Same engine as chat, but persona-tuned and source-detail focused.
 */
export default function ResearchPage() {
  const [q, setQ] = useState("");
  const [resp, setResp] = useState<ChatResponse | null>(null);
  const [busy, setBusy] = useState(false);

  async function ask() {
    if (!q.trim()) return;
    setBusy(true);
    try {
      const r = await api.chat(q);
      setResp(r);
    } finally { setBusy(false); }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[1fr_360px] min-h-screen">
      <div className="p-4 sm:p-8 max-w-4xl">
        <h1 className="font-serif text-3xl mb-1">Research</h1>
        <p className="text-sm opacity-70 mb-4">Practitioner workbench. Cite-bearing memos with source drill-down.</p>
        <div className="flex gap-2">
          <input
            value={q}
            onChange={e => setQ(e.target.value)}
            onKeyDown={e => e.key === "Enter" && ask()}
            placeholder='e.g., "anticipatory bail under BNSS — divergence from CrPC 438"'
            className="flex-1 bg-transparent border border-black/10 dark:border-white/15 rounded-lg px-3 py-2 text-sm"
          />
          <button
            disabled={busy} onClick={ask}
            className="px-3 py-2 rounded-lg bg-ink-900 text-bone-50 text-sm flex items-center gap-1"
          >
            <Search size={14} /> Run
          </button>
        </div>

        <div className="mt-6 space-y-4">
          <StageLoader active={busy} />
          {resp && (
            <div className="rounded-xl border border-black/10 dark:border-white/10 p-4">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs uppercase tracking-wider opacity-60">Memo</span>
                <span className="ml-auto"><ConfidenceBadge value={resp.confidence} /></span>
              </div>
              <AnswerRenderer content={resp.answer_md} citations={resp.citations} />
            </div>
          )}
        </div>
      </div>

      <aside className="border-l border-black/10 dark:border-white/10 p-4 sm:p-6">
        <div className="text-xs uppercase tracking-wider opacity-60 mb-3">Sources rail</div>
        {!resp || resp.citations.length === 0 ? (
          <p className="text-sm opacity-60">Sources used in the memo will be listed here. Click a citation in the memo body to drill in.</p>
        ) : (
          <ol className="space-y-3 text-sm">
            {resp.citations.map((c, i) => (
              <li key={i}>
                <span className="font-medium">{i + 1}. </span>
                {c.type === "section"
                  ? `${c.act} §${c.section}`
                  : c.case_name || c.citation_str}
              </li>
            ))}
          </ol>
        )}
      </aside>
    </div>
  );
}
