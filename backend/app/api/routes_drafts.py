"""Draft + notice generation routes. Workflow-driven."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, Response

from app.api.schemas import ArtifactOut, DraftRequest, NoticeRequest
from app.core.device import device_id_from_request, get_or_create_device_id
from app.db import store
from app.workflows import drafts as drafts_wf
from app.workflows import notices as notices_wf

router = APIRouter(prefix="/api", tags=["drafts"])


@router.post("/draft", response_model=ArtifactOut)
async def create_draft(req: DraftRequest, request: Request,
                        response: Response) -> ArtifactOut:
    device_id = get_or_create_device_id(request, response)
    body, citations = await drafts_wf.generate(req.workflow, req.inputs,
                                                  device_id=device_id)
    artifact = await store.insert_artifact(
        device_id=device_id,
        artifact_type=f"draft:{req.workflow}",
        title=drafts_wf.title_for(req.workflow, req.inputs),
        body_md=body,
        inputs=req.inputs,
        citations=citations,
    )
    return ArtifactOut(**artifact)


@router.post("/notice", response_model=ArtifactOut)
async def create_notice(req: NoticeRequest, request: Request,
                         response: Response) -> ArtifactOut:
    device_id = get_or_create_device_id(request, response)
    body, citations = await notices_wf.generate(req.workflow, req.inputs,
                                                    device_id=device_id)
    artifact = await store.insert_artifact(
        device_id=device_id,
        artifact_type=f"notice:{req.workflow}",
        title=notices_wf.title_for(req.workflow, req.inputs),
        body_md=body,
        inputs=req.inputs,
        citations=citations,
    )
    return ArtifactOut(**artifact)


@router.get("/artifacts", response_model=list[ArtifactOut])
async def list_artifacts(request: Request) -> list[ArtifactOut]:
    device_id = device_id_from_request(request)
    if not device_id:
        return []
    out = await store.list_artifacts(device_id)
    return [ArtifactOut(**a) for a in out]


@router.get("/artifacts/{artifact_id}", response_model=ArtifactOut)
async def get_artifact(artifact_id: str, request: Request) -> ArtifactOut:
    device_id = device_id_from_request(request)
    if not device_id:
        raise HTTPException(401, "no session")
    a = await store.get_artifact(artifact_id, device_id)
    if not a:
        raise HTTPException(404, "artifact not found")
    return ArtifactOut(**a)
