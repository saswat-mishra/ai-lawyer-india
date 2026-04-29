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

function matchCitation(kind: string, body: string, citations: Citation[]): Citation | null {
  if (kind === "SECT") {
    const [act, sec] = body.split(":");
    return citations.find(c => c.type === "section" && c.act === act?.trim() && c.section === sec?.trim()) ?? null;
  }
  if (kind === "CASE") {
    return citations.find(c => c.type === "case" && (c.citation_str === body || c.case_name === body)) ?? null;
  }
  if (kind === "COMPANY") {
    return { type: "company", raw: body, chunk_id: null } as any;
  }
  return null;
}
