"""Vercel Python serverless entrypoint.

Vercel routes anything matching the rewrite pattern `/api/*` to this file.
We expose the FastAPI app directly; Vercel's Python runtime supports ASGI.

The deploy script reorganises the tree so the deploy root looks like:
    /package.json (Next.js)
    /api/index.py  <- this file
    /backend/app/...
    /requirements.txt
so we add ./backend to sys.path.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
# In the deploy layout, backend/ is the sibling of api/.
sys.path.insert(0, os.path.join(_HERE, "..", "backend"))

# Default to in-memory store for the cold-start path. For real deployment,
# set DATABASE_URL to your Supabase Postgres URL and pass AIL_FORCE_PG=1.
os.environ.setdefault("AIL_FORCE_MEMORY", "1")

from app.main import app  # noqa: E402

# Vercel calls `app(scope, receive, send)` — FastAPI is ASGI-compatible.
