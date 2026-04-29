/**
 * API client. All endpoints rely on the device-ID cookie. We use credentials:
 * "include" so the signed cookie travels.
 */
export type Persona = "citizen" | "founder" | "practitioner";

export type Citation = {
  type: string;
  raw: string;
  act?: string | null;
  section?: string | null;
  case_name?: string | null;
  citation_str?: string | null;
  chunk_id?: string | null;
};

export type ChatResponse = {
  conversation_id: string;
  answer_md: string;
  citations: Citation[];
  confidence: "high" | "medium" | "low" | "refused";
  refused: boolean;
  refusal_reason?: string | null;
  needs_clarification: boolean;
  clarifying_questions: Array<{
    slot: string;
    question: string;
    choices: string[];
    allow_free_text?: boolean;
  }>;
  trace?: any[];
};

export type Conversation = { id: string; title: string; workflow: string; updated_at: string };
export type Message = {
  id: string; role: string; content: string;
  meta: any; confidence: string | null; created_at: string;
};
export type CompanyDoc = {
  id: string; filename: string; mime_type: string; size_bytes: number;
  doc_type: string; status: string; link_url?: string | null; created_at: string;
};
export type Artifact = {
  id: string; artifact_type: string; title: string; body_md: string;
  citations: any[]; inputs: any; created_at: string;
};

const BASE = "/api";

async function json<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(BASE + path, {
    credentials: "include",
    headers: { "content-type": "application/json", ...(init?.headers || {}) },
    ...init,
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}: ${await res.text()}`);
  return res.json();
}

export const api = {
  health: () => json<{ ok: boolean; has_openai: boolean }>("/health"),

  session: () => json<{ device_id: string; persona: Persona; language_pref: string }>(
    "/session", { method: "POST" },
  ),
  setPersona: (persona: Persona) => json<{ persona: Persona }>(
    "/session/persona", { method: "PATCH", body: JSON.stringify({ persona }) },
  ),
  setLanguage: (language_pref: string) => json<{ language_pref: string }>(
    "/session/language", { method: "PATCH", body: JSON.stringify({ language_pref }) },
  ),

  chat: (query: string, conversation_id?: string, slots: any = {}) =>
    json<ChatResponse>("/chat", {
      method: "POST", body: JSON.stringify({ query, conversation_id, slots }),
    }),
  conversations: () => json<Conversation[]>("/chat/conversations"),
  messages: (id: string) => json<Message[]>(`/chat/conversations/${id}/messages`),

  companyDocs: () => json<CompanyDoc[]>("/company/docs"),
  uploadCompanyDoc: async (file: File, doc_type = "agreement"): Promise<CompanyDoc> => {
    const fd = new FormData();
    fd.append("file", file);
    fd.append("doc_type", doc_type);
    const res = await fetch(BASE + "/company/docs", {
      method: "POST", credentials: "include", body: fd,
    });
    if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
    return res.json();
  },
  addCompanyLink: (url: string, label = "") =>
    json<CompanyDoc>("/company/links", { method: "POST", body: JSON.stringify({ url, label }) }),
  deleteCompanyDoc: (id: string) => json(`/company/docs/${id}`, { method: "DELETE" }),

  draft: (workflow: string, inputs: any) =>
    json<Artifact>("/draft", { method: "POST", body: JSON.stringify({ workflow, inputs }) }),
  notice: (workflow: string, inputs: any) =>
    json<Artifact>("/notice", { method: "POST", body: JSON.stringify({ workflow, inputs }) }),
  artifacts: () => json<Artifact[]>("/artifacts"),
  getArtifact: (id: string) => json<Artifact>(`/artifacts/${id}`),

  source: (chunk_id: string) => json<{ chunk: any; document: any }>(`/sources/chunk/${chunk_id}`),
  successor: (act: string, section: string) =>
    json<{ found: boolean; new_act?: string; new_section?: string; notes?: string }>(
      `/sources/successor?act=${encodeURIComponent(act)}&section=${encodeURIComponent(section)}`,
    ),
};
