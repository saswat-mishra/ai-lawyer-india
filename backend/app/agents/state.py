"""Agent state shared across nodes."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.core.config import Persona
from app.rag.retriever import RetrievedChunk
from app.verify.citations import Citation


@dataclass
class AgentState:
    device_id: str
    conversation_id: str | None
    persona: Persona = Persona.CITIZEN
    language_pref: str = "en"

    # Input.
    user_query: str = ""
    history: list[dict[str, Any]] = field(default_factory=list)

    # Classification + clarification.
    category: str = "general"
    slots: dict[str, Any] = field(default_factory=dict)
    clarifying_questions: list[dict[str, Any]] = field(default_factory=list)
    needs_clarification: bool = False

    # Retrieval.
    legal_results: list[RetrievedChunk] = field(default_factory=list)
    company_results: list[RetrievedChunk] = field(default_factory=list)
    support_density: float = 0.0

    # Synthesis output.
    answer_md: str = ""
    citations: list[Citation] = field(default_factory=list)
    confidence: str = "medium"
    refused: bool = False
    refusal_reason: str | None = None

    # Audit/trace.
    trace: list[dict[str, Any]] = field(default_factory=list)

    def log(self, step: str, **info: Any) -> None:
        self.trace.append({"step": step, **info})
