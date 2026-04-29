"""Pluggable storage backend.

By default `app.db.store` is the in-memory implementation in `store.py`.
When AIL_FORCE_PG=1 or DATABASE_URL points at a non-localhost host,
we hot-swap `app.db.store` to be the asyncpg-backed Postgres implementation
in `pg_store.py`. Callers always use `from app.db import store`.
"""
from __future__ import annotations

import os
import sys


def _use_pg() -> bool:
    if os.environ.get("AIL_FORCE_MEMORY") == "1":
        return False
    if os.environ.get("AIL_FORCE_PG") == "1":
        return True
    dsn = os.environ.get("DATABASE_URL", "")
    if dsn and "localhost" not in dsn and "127.0.0.1" not in dsn:
        return True
    return False


if _use_pg():
    from app.db import pg_store
    sys.modules["app.db.store"] = pg_store
