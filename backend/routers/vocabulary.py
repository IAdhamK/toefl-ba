import hashlib
import time

from fastapi import APIRouter, HTTPException

from backend.repository import delete_vocabulary, get_vocabulary_item, list_vocabulary, upsert_vocabulary
from backend.schemas import VocabularyPayload
from backend.services.scoring_service import score_vocabulary


router = APIRouter(prefix="/api/vocabulary", tags=["vocabulary"])


def seeded_daily_items(items: list[dict], seed_text: str, limit: int) -> list[dict]:
    decorated = []
    for item in items:
        source = f"{seed_text}-{item.get('id')}-{item.get('word')}".encode("utf-8")
        decorated.append((hashlib.sha256(source).hexdigest(), item))
    decorated.sort(key=lambda pair: pair[0])
    return [item for _, item in decorated[: min(limit, len(decorated))]]


@router.get("")
def get_vocabulary() -> dict:
    return {"vocabulary": list_vocabulary()}


@router.get("/daily")
def get_daily_vocabulary() -> dict:
    today = time.strftime("%Y-%m-%d")
    items = seeded_daily_items(list_vocabulary(), today, 25)
    return {
        "date": today,
        "target": 25,
        "items": items,
        "message": "Pengingat hari ini: selesaikan 25 kata vocabulary agar konsisten naik level.",
    }


@router.post("", status_code=201)
def create_vocabulary(payload: VocabularyPayload) -> dict:
    return {"item": upsert_vocabulary(payload.dict())}


@router.put("/{vocab_id}")
def update_vocabulary(vocab_id: str, payload: VocabularyPayload) -> dict:
    data = payload.dict()
    data["id"] = vocab_id
    return {"item": upsert_vocabulary(data)}


@router.delete("/{vocab_id}")
def remove_vocabulary(vocab_id: str) -> dict:
    if not delete_vocabulary(vocab_id):
        raise HTTPException(status_code=404, detail="Vocabulary item not found")
    return {"ok": True}


@router.post("/submit-answer")
def submit_vocabulary_answer(payload: dict) -> dict:
    item = get_vocabulary_item(payload.get("itemId", ""))
    if not item:
        raise HTTPException(status_code=404, detail="Vocabulary item not found")
    return score_vocabulary(item, payload.get("answer", ""))
