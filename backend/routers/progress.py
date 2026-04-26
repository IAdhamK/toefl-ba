from fastapi import APIRouter

from backend.database import encode_json, get_connection, now_iso
from backend.repository import get_state, set_state
from backend.schemas import ProgressAttempt
from backend.services.progress_service import progress_analytics
from backend.services.scoring_service import attempt_id


router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.get("/summary")
def progress_summary() -> dict:
    state = get_state()
    return {"progress": state.get("progress", {})}


@router.get("/analytics")
def progress_analytics_get() -> dict:
    return {"analytics": progress_analytics(get_state())}


@router.post("/analytics")
def progress_analytics_post(state: dict) -> dict:
    return {"analytics": progress_analytics(state)}


@router.post("/record")
def record_progress(progress: dict) -> dict:
    state = get_state()
    state["progress"] = progress
    set_state(state)
    return {"progress": progress}


@router.post("/attempt", status_code=201)
def create_attempt(payload: ProgressAttempt) -> dict:
    now = now_iso()
    item_id = attempt_id(payload.module)
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO attempts (id, user_id, module, score, payload_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (item_id, payload.userId, payload.module, payload.score, encode_json(payload.payload), now),
        )
        conn.execute(
            """
            INSERT INTO progress (user_id, skill, score, metadata_json, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (payload.userId, payload.module, payload.score, encode_json(payload.payload), now),
        )
    return {"attempt": {"id": item_id, "module": payload.module, "score": payload.score}}
