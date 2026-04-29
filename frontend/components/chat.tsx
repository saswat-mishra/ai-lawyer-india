"use client";
import { useEffect, useRef, useState } from "react";
import { Send, Sparkles, Globe2 } from "lucide-react";
import { api, ChatResponse } from "@/lib/api";
import { useSession } from "@/lib/session";
import { StageLoader } from "./stage-loader";
import { ConfidenceBadge } from "./confidence-badge";
import { AnswerRenderer } from "./answer-renderer";
import { Clarifier } from "./clarifier";

type Turn =
  | { kind: "user"; text: string }
  | { kind: "assistant"; resp: ChatResponse }
  | { kind: "clarify"; questions: ChatResponse["clarifying_questions"]; pendingQuery: string; pendingSlots: any };

export function Chat() {
  const { ready, persona } = useSession();
  const [turns, setTurns] = useState<Turn[]>([]);
  const [convId, setConvId] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: 999999, behavior: "smooth" });
  }, [turns, busy]);

  async function send(query: string, slots: any = {}) {
    setBusy(true);
    setTurns(t => [...t, { kind: "user", text: query }]);
    try {
      const resp = await api.chat(query, convId ?? undefined, slots);
      setConvId(resp.conversation_id);
      if (resp.needs_clarification) {
        setTurns(t => [
          ...t,
          { kind: "clarify", questions: resp.clarifying_questions, pendingQuery: query, pendingSlots: slots },
        ]);
      } else {
        setTurns(t => [...t, { kind: "assistant", resp }]);
      }
    } catch (err: any) {
      setTurns(t => [
        ...t,
        { kind: "assistant", resp: errorResp(err) },
      ]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="flex flex-col h-screen">
      <Header persona={persona} />
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 sm:px-8 py-6 space-y-6 max-w-3xl w-full mx-auto">
        {turns.length === 0 && <Empty persona={persona} onAsk={(q) => send(q)} />}
        {turns.map((t, i) =>
          t.kind === "user" ? (
            <UserBubble key={i} text={t.text} />
          ) : t.kind === "assistant" ? (
            <AssistantBubble key={i} resp={t.resp} />
          ) : (
            <Clarifier
              key={i}
              questions={t.questions}
              onAnswer={(slots) => {
                setTurns(prev => prev.filter((_, idx) => idx !== i));
                send(t.pendingQuery, { ...t.pendingSlots, ...slots });
              }}
            />
          ),
        )}
        <StageLoader active={busy} />
      </div>
      <Composer
        disabled={!ready || busy}
        value={input}
        onChange={setInput}
        onSubmit={() => {
          const q = input.trim();
          if (!q) return;
          setInput("");
          send(q);
        }}
      />
    </div>
  );
}

function Header({ persona }: { persona: string }) {
  return (
    <header className="border-b border-black/10 dark:border-white/10 px-4 sm:px-8 py-4 flex items-center gap-3">
      <Sparkles size={18} className="text-saffron-500" />
      <div className="flex-1">
        <div className="text-sm font-medium">Ask anything about Indian law</div>
        <div className="text-xs text-ink-900/50 dark:text-bone-50/60">
          Mode: <span className="capitalize">{persona}</span> · Citation-faithful, BNS-current
        </div>
      </div>
      <span className="hidden sm:inline-flex items-center gap-1 text-xs text-ink-900/50 dark:text-bone-50/60">
        <Globe2 size={12} /> Hindi support coming
      </span>
    </header>
  );
}

function Composer({
  value, onChange, onSubmit, disabled,
}: { value: string; onChange: (v: string) => void; onSubmit: () => void; disabled: boolean }) {
  return (
    <div className="border-t border-black/10 dark:border-white/10 px-4 sm:px-8 py-4">
      <div className="max-w-3xl mx-auto flex gap-2 items-end">
        <textarea
          value={value}
          rows={1}
          onChange={e => onChange(e.target.value)}
          onKeyDown={e => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              if (!disabled) onSubmit();
            }
          }}
          placeholder="e.g., My landlord wants to evict me without notice — what are my rights?"
          className="flex-1 resize-none bg-transparent border border-black/10 dark:border-white/15 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-saffron-500/40 max-h-40"
        />
        <button
          disabled={disabled}
          onClick={onSubmit}
          className="h-9 px-3 rounded-lg bg-ink-900 text-bone-50 disabled:opacity-50 flex items-center gap-1 text-sm"
          aria-label="Send"
        >
          <Send size={14} /> Ask
        </button>
      </div>
      <div className="max-w-3xl mx-auto mt-2 text-[11px] text-ink-900/50 dark:text-bone-50/50">
        Vakeel.ai gives you legal information & document help. For courtroom representation or anything high-stakes, consult an enrolled advocate.
      </div>
    </div>
  );
}

function UserBubble({ text }: { text: string }) {
  return (
    <div className="flex justify-end animate-fade-up">
      <div className="bg-ink-900 text-bone-50 dark:bg-bone-50 dark:text-ink-900 px-4 py-2.5 rounded-2xl rounded-tr-md max-w-[85%] text-sm whitespace-pre-wrap">
        {text}
      </div>
    </div>
  );
}

function AssistantBubble({ resp }: { resp: ChatResponse }) {
  return (
    <div className="animate-fade-up">
      <div className="rounded-2xl rounded-tl-md border border-black/10 dark:border-white/10 bg-bone-50 dark:bg-ink-900 px-4 py-4">
        <div className="flex items-center gap-2 mb-3">
          <Sparkles size={14} className="text-saffron-500" />
          <span className="text-xs uppercase tracking-wider text-ink-900/50 dark:text-bone-50/60">Vakeel.ai</span>
          <span className="ml-auto"><ConfidenceBadge value={resp.confidence} /></span>
        </div>
        <AnswerRenderer content={resp.answer_md} citations={resp.citations} />
        {resp.citations.length > 0 && (
          <details className="mt-4 text-xs text-ink-900/60 dark:text-bone-50/60">
            <summary className="cursor-pointer">{resp.citations.length} sources used</summary>
            <ul className="mt-2 space-y-1">
              {resp.citations.map((c, i) => (
                <li key={i} className="opacity-90">
                  {c.type === "section" ? `${c.act} §${c.section}` : c.case_name || c.citation_str}
                </li>
              ))}
            </ul>
          </details>
        )}
      </div>
    </div>
  );
}

function Empty({ persona, onAsk }: { persona: string; onAsk: (q: string) => void }) {
  const PROMPTS: Record<string, string[]> = {
    citizen: [
      "My landlord wants to evict me from my Mumbai flat without 30 days notice — what are my rights?",
      "Someone defamed me on Twitter. What can I do under Indian law?",
      "Can I file an FIR online for cheque bounce? What's the process?",
    ],
    founder: [
      "Draft a one-page NDA for a manufacturing partner discussion.",
      "What does the DPDP Act require for our user-data flows?",
      "Termination clauses I should add to a vendor MSA?",
    ],
    practitioner: [
      "Section 138 NI Act limitation: latest position in 2024–25 case law.",
      "Anticipatory bail under BNSS — how does it differ from CrPC §438?",
      "Strategy for a property dispute in Bombay HC: opposing party claims adverse possession.",
    ],
  };
  return (
    <div className="text-center max-w-xl mx-auto py-10">
      <div className="font-serif text-3xl">Vakeel for India.</div>
      <div className="mt-2 text-sm text-ink-900/60 dark:text-bone-50/60">
        Cite-faithful answers grounded in Indian law. BNS / BNSS / BSA aware. Drill into every source.
      </div>
      <div className="mt-6 grid sm:grid-cols-1 gap-2 text-left">
        {(PROMPTS[persona] ?? PROMPTS.citizen).map(p => (
          <button
            key={p}
            onClick={() => onAsk(p)}
            className="text-sm rounded-xl border border-black/10 dark:border-white/10 px-4 py-3 hover:bg-black/5 dark:hover:bg-white/5"
          >
            {p}
          </button>
        ))}
      </div>
    </div>
  );
}

function errorResp(err: any): ChatResponse {
  return {
    conversation_id: "",
    answer_md: `Something went wrong. ${String(err?.message || err)}`,
    citations: [],
    confidence: "low",
    refused: false,
    refusal_reason: null,
    needs_clarification: false,
    clarifying_questions: [],
  };
}
