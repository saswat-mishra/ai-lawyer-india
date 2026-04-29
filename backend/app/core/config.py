"""Centralised settings. Source of truth for env-driven config."""
from __future__ import annotations

from enum import Enum
from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Persona(str, Enum):
    CITIZEN = "citizen"
    FOUNDER = "founder"
    PRACTITIONER = "practitioner"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- App ---
    app_env: Literal["development", "production", "test"] = "development"
    allowed_origins: str = "http://localhost:3000"

    # --- OpenAI ---
    openai_api_key: str = ""
    openai_model_default: str = "gpt-4o-mini"
    openai_model_heavy: str = "gpt-4o"
    openai_model_nano: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_embedding_dim: int = 1536

    # --- DB ---
    database_url: str = "postgresql://postgres:postgres@localhost:54322/postgres"
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_key: str = ""
    supabase_storage_bucket: str = "company-docs"

    # --- Session ---
    device_cookie_secret: str = "dev-secret-change-me"
    device_cookie_name: str = "ail_did"
    device_cookie_max_age_days: int = 365

    # --- Web search (optional) ---
    tavily_api_key: str = ""
    serpapi_api_key: str = ""

    # --- RAG knobs ---
    legal_topk: int = 50                # initial hybrid candidate count
    legal_final_k: int = 8              # final top-k after rerank
    company_topk: int = 20
    company_final_k: int = 4
    rrf_k: int = 60
    citizen_max_results: int = 6
    practitioner_max_results: int = 20
    refusal_floor: float = 0.22         # min retrieval support density (calibrated 2026-04-29)

    # --- Test flags ---
    run_openai_tests: bool = False
    run_live_tests: bool = False

    @property
    def has_openai(self) -> bool:
        return bool(self.openai_api_key.strip())

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
