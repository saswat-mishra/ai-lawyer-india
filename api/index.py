"""Vercel Python serverless entrypoint.

Vercel routes anything matching the rewrite pattern `/api/*` to this file.
We expose the FastAPI app directly; Vercel's Python runtime supports ASGI.
"""
import os
import sys

# Add the backend package to the import path.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

# Default to in-memory store for the cold-start path. For real deployment,
# set DATABASE_URL to your Supabase Postgres URL and pass AIL_FORCE_PG=1.
os.environ.setdefault("AIL_FORCE_MEMORY", "1")

from app.main import app  # noqa: E402

# Vercel calls `app(scope, receive, send)` — FastAPI is ASGI-compatible.
