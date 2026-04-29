"""FastAPI app composition."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes_chat import router as chat_router
from app.api.routes_company import router as company_router
from app.api.routes_drafts import router as drafts_router
from app.api.routes_session import router as session_router
from app.api.routes_sources import router as sources_router
from app.core.config import get_settings
from app.ingest.legal_seed import seed_legal_corpus


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Idempotent seed on boot — gives the user a working corpus from minute one.
    try:
        await seed_legal_corpus()
    except Exception as e:
        # Don't crash on seed failures — just log.
        print(f"[seed] warning: {e}")
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="AI Lawyer India", version="0.1.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(ValueError)
    async def _value_error_handler(request: Request, exc: ValueError):
        # Workflow input validation raises ValueError; map to 422.
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    @app.get("/api/health")
    async def health():
        return {"ok": True, "has_openai": settings.has_openai, "env": settings.app_env}

    app.include_router(session_router)
    app.include_router(chat_router)
    app.include_router(company_router)
    app.include_router(drafts_router)
    app.include_router(sources_router)
    return app


app = create_app()
