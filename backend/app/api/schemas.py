"""Request/response schemas. All API I/O passes through these."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class SessionResponse(BaseModel):
    device_id: str
    persona: Literal["citizen", "founder", "practitioner"]
    language_pref: str


class PersonaUpdateRequest(BaseModel):
    persona: Literal["citizen", "founder", "practitioner"]


class LanguageUpdateRequest(BaseModel):
    language_pref: str


class ChatRequest(BaseModel):
    conversation_id: str | None = None
    query: str = Field(..., min_length=1, max_length=8000)
    slots: dict[str, Any] = Field(default_factory=dict)


class CitationOut(BaseModel):
    type: str
    raw: str
    act: str | None = None
    section: str | None = None
    case_name: str | None = None
    citation_str: str | None = None
    chunk_id: str | None = None


class ChatResponse(BaseModel):
    conversation_id: str
    answer_md: str
    citations: list[CitationOut]
    confidence: str
    refused: bool
    refusal_reason: str | None = None
    needs_clarification: bool = False
    clarifying_questions: list[dict[str, Any]] = Field(default_factory=list)
    trace: list[dict[str, Any]] = Field(default_factory=list)


class ConversationOut(BaseModel):
    id: str
    title: str
    workflow: str
    updated_at: str


class MessageOut(BaseModel):
    id: str
    role: str
    content: str
    meta: dict[str, Any]
    confidence: str | None
    created_at: str


class CompanyDocOut(BaseModel):
    id: str
    filename: str
    mime_type: str
    size_bytes: int
    doc_type: str
    status: str
    link_url: str | None = None
    created_at: str


class CompanyLinkRequest(BaseModel):
    url: str
    label: str = ""


class DraftRequest(BaseModel):
    workflow: Literal[
        "rental_agreement", "nda", "employment_letter", "founders_agreement",
        "vendor_msa", "consultancy_agreement", "partnership_deed", "will",
    ]
    inputs: dict[str, Any]


class NoticeRequest(BaseModel):
    workflow: Literal[
        "s138_ni_act_notice", "eviction_notice", "consumer_complaint_notice",
        "breach_of_contract_notice", "defamation_notice",
    ]
    inputs: dict[str, Any]


class ArtifactOut(BaseModel):
    id: str
    artifact_type: str
    title: str
    body_md: str
    citations: list[dict[str, Any]]
    inputs: dict[str, Any]
    created_at: str
