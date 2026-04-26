from fastapi import APIRouter, HTTPException

from backend.repository import delete_admin_content, list_admin_content, upsert_admin_content


router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/content")
def get_content() -> dict:
    return {"content": list_admin_content()}


@router.post("/content", status_code=201)
def create_content(payload: dict) -> dict:
    return {"content": upsert_admin_content(payload)}


@router.put("/content/{content_id}")
def update_content(content_id: str, payload: dict) -> dict:
    return {"content": upsert_admin_content(payload, content_id)}


@router.delete("/content/{content_id}")
def remove_content(content_id: str) -> dict:
    if not delete_admin_content(content_id):
        raise HTTPException(status_code=404, detail="Content not found")
    return {"ok": True}
