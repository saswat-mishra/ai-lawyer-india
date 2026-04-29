"use client";
import { useState } from "react";
import { Citation, api } from "@/lib/api";
import { motion, AnimatePresence } from "framer-motion";

export function CitationPill({ citation }: { citation: Citation }) {
  const [open, setOpen] = useState(false);
  const [chunk, setChunk] = useState<any>(null);
  const [doc, setDoc] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const label = citation.type === "section"
    ? `${citation.act ?? ""} §${citation.section ?? ""}`.trim()
    : citation.case_name || citation.citation_str || citation.raw;

  async function load() {
    if (chunk) return;
    if (!citation.chunk_id) return;
    setLoading(true);
    try {
      const data = await api.source(citation.chunk_id);
      setChunk(data.chunk);
      setDoc(data.document);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <button
        type="button"
        className="cite-pill"
        aria-label={`Source: ${label}`}
        onClick={() => { setOpen(true); load(); }}
      >
        <span aria-hidden>§</span>
        <span>{label}</span>
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            className="fixed inset-0 z-40 bg-black/30 backdrop-blur-[2px]"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            onClick={() => setOpen(false)}
          >
            <motion.aside
              className="absolute right-0 top-0 h-full w-full sm:w-[480px] bg-bone-50 dark:bg-ink-900 border-l border-black/10 dark:border-white/10 p-6 overflow-y-auto"
              initial={{ x: 480 }} animate={{ x: 0 }} exit={{ x: 480 }}
              transition={{ type: "tween", duration: 0.2 }}
              onClick={e => e.stopPropagation()}
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="text-xs uppercase tracking-wider text-ink-900/50 dark:text-bone-50/50 mb-1">Source</div>
                  <h3 className="font-serif text-xl">{label}</h3>
                  {doc?.title && <div className="text-sm opacity-70 mt-1">{doc.title}</div>}
                </div>
                <button onClick={() => setOpen(false)} aria-label="Close" className="text-2xl leading-none opacity-70">×</button>
              </div>
              <div className="mt-5 prose prose-sm dark:prose-invert max-w-none">
                {loading && <div className="skeleton h-24 w-full" />}
                {chunk && (
                  <>
                    <div className="text-xs opacity-60 mb-2">{(chunk.hierarchy_path || []).join(" > ")}</div>
                    <p className="whitespace-pre-wrap">{chunk.text}</p>
                  </>
                )}
                {!loading && !chunk && (
                  <p className="text-sm opacity-70">
                    No source body available — citation could not be drilled into.
                  </p>
                )}
                {doc?.source_url && (
                  <a
                    className="inline-block mt-4 text-sm text-saffron-600 underline"
                    href={doc.source_url} target="_blank" rel="noreferrer"
                  >
                    View original source ↗
                  </a>
                )}
              </div>
            </motion.aside>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
