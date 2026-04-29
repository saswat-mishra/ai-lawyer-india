"use client";
import { useEffect, useState } from "react";
import { api, Artifact } from "@/lib/api";
import { motion } from "framer-motion";

const DRAFTS = [
  { workflow: "rental_agreement", title: "Rental / Leave-and-Licence", fields: ["state","landlord_name","tenant_name","premises_address","monthly_rent_inr","deposit_inr","tenure_months","start_date"] },
  { workflow: "nda", title: "Mutual NDA", fields: ["disclosing_party","receiving_party","purpose","duration_months","governing_law_state"] },
  { workflow: "employment_letter", title: "Offer Letter", fields: ["company_name","candidate_name","role","ctc_inr","start_date","city","probation_months"] },
  { workflow: "founders_agreement", title: "Founders' Agreement", fields: ["founders","company_name","equity_split","vesting_schedule","ip_assignment","governing_law_state"] },
  { workflow: "vendor_msa", title: "Vendor MSA", fields: ["customer","vendor","scope","fees_terms","governing_law_state","indemnity_cap"] },
  { workflow: "consultancy_agreement", title: "Consultancy Agreement", fields: ["principal","consultant","scope","fees","duration_months"] },
];

const NOTICES = [
  { workflow: "s138_ni_act_notice", title: "Cheque Bounce (s.138 NI Act)", fields: ["payee_name","payee_address","drawer_name","drawer_address","cheque_number","cheque_date","cheque_amount_inr","bank_name","dishonour_date","underlying_debt"] },
  { workflow: "eviction_notice", title: "Eviction / Notice to Quit", fields: ["landlord_name","tenant_name","premises_address","ground","notice_period_days","state"] },
  { workflow: "consumer_complaint_notice", title: "Consumer Complaint", fields: ["complainant","opposite_party","service_or_goods","deficiency","amount_paid_inr","relief_sought"] },
  { workflow: "breach_of_contract_notice", title: "Breach of Contract", fields: ["claimant","respondent","contract_date","breach_description","cure_period_days","damages_claimed_inr"] },
  { workflow: "defamation_notice", title: "Defamation Notice", fields: ["claimant","respondent","alleged_statement","publication_date","harm_description","relief_sought"] },
];

export default function DraftsPage() {
  const [artifacts, setArtifacts] = useState<Artifact[]>([]);
  const [active, setActive] = useState<{ kind: "draft"|"notice"; spec: any } | null>(null);
  const [busy, setBusy] = useState(false);
  const [output, setOutput] = useState<Artifact | null>(null);

  useEffect(() => { api.artifacts().then(setArtifacts); }, []);

  async function generate(inputs: Record<string,string>) {
    if (!active) return;
    setBusy(true);
    try {
      const a = active.kind === "draft"
        ? await api.draft(active.spec.workflow, inputs)
        : await api.notice(active.spec.workflow, inputs);
      setOutput(a);
      setArtifacts(prev => [a, ...prev]);
    } catch (e: any) {
      alert(e.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="p-4 sm:p-8 max-w-6xl mx-auto">
      <h1 className="font-serif text-3xl mb-1">Drafts & Notices</h1>
      <p className="text-sm opacity-70 mb-6">India-specific workflows with citation-grounded output.</p>

      <div className="grid md:grid-cols-2 gap-4">
        <Section title="Drafts">
          {DRAFTS.map(d => (
            <Tile key={d.workflow} title={d.title} onClick={() => { setActive({ kind: "draft", spec: d }); setOutput(null); }} />
          ))}
        </Section>
        <Section title="Legal Notices">
          {NOTICES.map(n => (
            <Tile key={n.workflow} title={n.title} onClick={() => { setActive({ kind: "notice", spec: n }); setOutput(null); }} />
          ))}
        </Section>
      </div>

      {active && (
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          className="mt-8 grid lg:grid-cols-2 gap-4"
        >
          <Form spec={active.spec} onSubmit={generate} busy={busy} />
          <Preview output={output} />
        </motion.div>
      )}

      {artifacts.length > 0 && (
        <div className="mt-12">
          <div className="text-xs uppercase tracking-wider opacity-60 mb-2">Recent</div>
          <div className="grid sm:grid-cols-2 gap-2">
            {artifacts.slice(0,8).map(a => (
              <button
                key={a.id}
                onClick={() => setOutput(a)}
                className="text-left text-sm rounded-lg border border-black/10 dark:border-white/10 px-3 py-2 hover:bg-black/5 dark:hover:bg-white/5"
              >
                <div className="font-medium truncate">{a.title}</div>
                <div className="text-xs opacity-60">{a.artifact_type}</div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <div className="text-xs uppercase tracking-wider opacity-60 mb-2">{title}</div>
      <div className="grid sm:grid-cols-2 gap-2">{children}</div>
    </div>
  );
}

function Tile({ title, onClick }: { title: string; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="text-left rounded-xl border border-black/10 dark:border-white/10 px-4 py-3 hover:bg-black/5 dark:hover:bg-white/5 transition"
    >
      <div className="text-sm font-medium">{title}</div>
    </button>
  );
}

function Form({ spec, onSubmit, busy }: { spec: any; onSubmit: (i: any) => void; busy: boolean }) {
  const [vals, setVals] = useState<Record<string,string>>({});
  const ready = spec.fields.every((f: string) => (vals[f] ?? "").length > 0);
  return (
    <div className="rounded-xl border border-black/10 dark:border-white/10 p-4">
      <div className="font-medium mb-3">{spec.title}</div>
      <div className="grid sm:grid-cols-2 gap-3">
        {spec.fields.map((f: string) => (
          <label key={f} className="text-xs">
            <div className="opacity-70 mb-1">{prettify(f)}</div>
            <input
              className="w-full bg-transparent border border-black/10 dark:border-white/15 rounded-md px-2 py-1.5 text-sm"
              value={vals[f] ?? ""}
              onChange={e => setVals(v => ({ ...v, [f]: e.target.value }))}
            />
          </label>
        ))}
      </div>
      <button
        disabled={!ready || busy}
        onClick={() => onSubmit(vals)}
        className="mt-4 px-3 py-1.5 rounded-md bg-ink-900 text-bone-50 disabled:opacity-50 text-sm"
      >
        {busy ? "Generating..." : "Generate"}
      </button>
    </div>
  );
}

function Preview({ output }: { output: Artifact | null }) {
  return (
    <div className="rounded-xl border border-black/10 dark:border-white/10 p-4 min-h-[400px]">
      {!output ? (
        <div className="text-sm opacity-60">Output will appear here. Every clause will be cited to the controlling provision.</div>
      ) : (
        <>
          <div className="text-xs uppercase tracking-wider opacity-60 mb-2">{output.artifact_type}</div>
          <div className="font-serif text-xl mb-3">{output.title}</div>
          <pre className="whitespace-pre-wrap text-sm legal-prose font-serif">{output.body_md}</pre>
        </>
      )}
    </div>
  );
}

function prettify(s: string): string {
  return s.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
}
