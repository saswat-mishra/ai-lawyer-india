"use client";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Citation } from "@/lib/api";
import { CitationPill } from "./citation-pill";

/**
 * Renders the assistant Markdown body and detects "[SECT:Act:Number]" /
 * "[CASE:short_citation]" tags emitted by the synthesis prompt; replaces them
 * with citation pills that drill down on click.
 */
export function AnswerRenderer({
  content,
  citations,
}: {
  content: string;
  citations: Citation[];
}) {
  const tagged = renderTagged(content, citations);
  return (
    <div className="legal-prose text-[15px]">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          // Replace inline-citation placeholders with pills.
          p: ({ children }) => <p>{withPills(children, citations)}</p>,
          li: ({ children }) => <li>{withPills(children, citations)}</li>,
        }}
      >
        {tagged}
      </ReactMarkdown>
    </div>
  );
}

const TAG_RE = /\[(SECT|CASE|COMPANY):([^\]]+)\]/g;

function renderTagged(content: string, _citations: Citation[]) {
  // Convert tags into a non-markdown placeholder Markdown can pass through —
  // we keep them as-is and parse in `withPills` since react-markdown delivers
  // them in the children stream.
  return content;
}

function withPills(node: React.ReactNode, citations: Citation[]): React.ReactNode {
  if (typeof node === "string") {
    const parts: React.ReactNode[] = [];
    let last = 0;
    for (const m of node.matchAll(TAG_RE)) {
      const idx = m.index ?? 0;
      if (idx > last) parts.push(node.slice(last, idx));
      const [, kind, body] = m;
      const cite = matchCitation(kind, body, citations);
      if (cite) {
        parts.push(<CitationPill key={`${idx}-${m[0]}`} citation={cite} />);
      } else {
        parts.push(<span className="cite-pill opacity-60">[unverified]</span>);
      }
      last = idx + m[0].length;
    }
    if (last < node.length) parts.push(node.slice(last));
    return parts;
  }
  if (Array.isArray(node)) return node.map((n, i) => <span key={i}>{withPills(n, citations)}</span>);
  return node;
}

// Lookup table for common act-name variations the model emits inline.
const ACT_ALIASES: Record<string, string> = {
  "Bharatiya Nyaya Sanhita": "BNS",
  "Bharatiya Nagarik Suraksha Sanhita": "BNSS",
  "Bharatiya Sakshya Adhiniyam": "BSA",
  "Indian Penal Code": "IPC",
  "Code of Criminal Procedure": "CrPC",
  "Indian Contract Act": "Contract Act",
  "Transfer of Property Act": "TP Act",
  "Negotiable Instruments Act": "NI Act",
  "Consumer Protection Act, 2019": "CPA 2019",
  "Consumer Protection Act": "CPA 2019",
};

function normaliseAct(s: string | null | undefined): string {
  if (!s) return "";
  const trimmed = s.trim();
  for (const [long, short] of Object.entries(ACT_ALIASES)) {
    if (trimmed.toLowerCase().includes(long.toLowerCase())) return short;
  }
  return trimmed;
}

function matchCitation(kind: string, body: string, citations: Citation[]): Citation | null {
  if (kind === "SECT") {
    const parts = body.split(":");
    const act = normaliseAct(parts[0]);
    const sec = (parts[1] ?? "").trim();
    return citations.find(c =>
      c.type === "section" &&
      normaliseAct(c.act ?? "") === act &&
      (c.section ?? "").trim() === sec,
    ) ?? null;
  }
  if (kind === "CASE") {
    const target = body.trim();
    return citations.find(c =>
      c.type === "case" && (
        c.citation_str === target ||
        c.case_name === target ||
        (c.citation_str ?? "").includes(target) ||
        (c.case_name ?? "").includes(target)
      ),
    ) ?? null;
  }
  if (kind === "COMPANY") {
    return { type: "company", raw: body, chunk_id: null } as any;
  }
  return null;
}
