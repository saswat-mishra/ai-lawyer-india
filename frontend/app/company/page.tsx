"use client";
import { useEffect, useRef, useState } from "react";
import { Upload, FileText, Link2, Trash2, Building2, ShieldCheck } from "lucide-react";
import { api, CompanyDoc } from "@/lib/api";
import { motion } from "framer-motion";

export default function CompanyPage() {
  const [docs, setDocs] = useState<CompanyDoc[]>([]);
  const [busy, setBusy] = useState(false);
  const [linkUrl, setLinkUrl] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);

  async function refresh() { setDocs(await api.companyDocs()); }
  useEffect(() => { refresh(); }, []);

  async function onUpload(file: File) {
    setBusy(true);
    try {
      await api.uploadCompanyDoc(file, file.type.startsWith("image/") ? "image" : "agreement");
      await refresh();
    } catch (e: any) { alert(e.message); }
    finally { setBusy(false); }
  }

  async function onAddLink() {
    if (!linkUrl.trim()) return;
    setBusy(true);
    try {
      await api.addCompanyLink(linkUrl.trim());
      setLinkUrl("");
      await refresh();
    } catch (e: any) { alert(e.message); }
    finally { setBusy(false); }
  }

  async function onDelete(id: string) {
    if (!confirm("Delete this document and its embeddings?")) return;
    await api.deleteCompanyDoc(id);
    await refresh();
  }

  return (
    <div className="p-4 sm:p-8 max-w-4xl mx-auto">
      <div className="flex items-start gap-3">
        <Building2 className="text-saffron-500" size={26} />
        <div>
          <h1 className="font-serif text-3xl">Company Knowledge Base</h1>
          <p className="text-sm opacity-70 mt-1 max-w-prose">
            Upload your contracts, policies, brand assets, or links. They are scoped to this device only — never visible to other users, never used to train models. Vakeel will weave them into answers and drafts when relevant.
          </p>
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}
        className="mt-6 grid sm:grid-cols-2 gap-4"
      >
        <div
          onDragOver={e => e.preventDefault()}
          onDrop={e => { e.preventDefault(); const f = e.dataTransfer.files[0]; if (f) onUpload(f); }}
          className="rounded-xl border-2 border-dashed border-black/15 dark:border-white/15 p-6 flex flex-col items-center justify-center text-center hover:bg-black/[0.03] dark:hover:bg-white/[0.03] transition"
        >
          <Upload className="opacity-60" size={20} />
          <div className="text-sm mt-2">Drop a file or</div>
          <button
            disabled={busy}
            onClick={() => fileRef.current?.click()}
            className="mt-2 text-xs px-3 py-1.5 rounded-md bg-ink-900 text-bone-50 disabled:opacity-50"
          >
            Choose file
          </button>
          <input
            ref={fileRef}
            type="file"
            className="hidden"
            accept=".pdf,.docx,.txt,.md,.png,.jpg,.jpeg,.webp,.csv"
            onChange={e => { const f = e.target.files?.[0]; if (f) onUpload(f); }}
          />
          <div className="text-[11px] opacity-60 mt-3">PDF, DOCX, TXT, MD, CSV, PNG/JPG up to 50MB</div>
        </div>

        <div className="rounded-xl border border-black/10 dark:border-white/10 p-4">
          <div className="flex items-center gap-2 text-sm font-medium"><Link2 size={16}/> Add a link</div>
          <p className="text-xs opacity-60 mt-1">Public-page URL. We fetch and index its text.</p>
          <div className="flex gap-2 mt-3">
            <input
              type="url"
              placeholder="https://yourcompany.com/policies/data"
              className="flex-1 bg-transparent border border-black/10 dark:border-white/15 rounded-md px-2 py-1.5 text-sm"
              value={linkUrl}
              onChange={e => setLinkUrl(e.target.value)}
            />
            <button
              disabled={busy || !linkUrl.trim()}
              onClick={onAddLink}
              className="text-xs px-3 py-1.5 rounded-md bg-ink-900 text-bone-50 disabled:opacity-50"
            >
              Add
            </button>
          </div>
          <div className="mt-4 flex items-center gap-2 text-xs text-sage-600">
            <ShieldCheck size={14} /> Per-device, never shared, never used in training
          </div>
        </div>
      </motion.div>

      <div className="mt-8">
        <div className="text-xs uppercase tracking-wider opacity-60 mb-2">Indexed</div>
        {docs.length === 0 ? (
          <div className="text-sm opacity-60">Nothing here yet — drop a contract or paste a link to get started.</div>
        ) : (
          <ul className="space-y-2">
            {docs.map(d => (
              <li key={d.id} className="flex items-center gap-3 rounded-lg border border-black/10 dark:border-white/10 px-3 py-2 text-sm">
                <FileText size={14} className="opacity-60 shrink-0" />
                <span className="font-medium truncate">{d.filename}</span>
                <span className="text-xs opacity-50 shrink-0">· {d.doc_type}</span>
                <span className={"ml-auto text-xs px-1.5 rounded shrink-0 " +
                  (d.status === "ready" ? "bg-sage-500/15 text-sage-600"
                    : d.status === "failed" ? "bg-wine-500/15 text-wine-500"
                    : "bg-saffron-500/15 text-saffron-600")}>{d.status}</span>
                <button onClick={() => onDelete(d.id)} aria-label="Delete" className="opacity-60 hover:opacity-100">
                  <Trash2 size={14} />
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
