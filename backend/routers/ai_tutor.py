from fastapi import APIRouter

from backend.schemas import ChatPayload, TextPayload
from backend.services.ai_service import ai_service
from backend.services.grammar_service import grammar_breakdown, indonesian_help
from backend.services.progress_service import recommendation


router = APIRouter(tags=["ai"])


@router.post("/api/ai/chat")
@router.post("/api/ai-tutor/chat")
def ai_chat(payload: ChatPayload) -> dict:
    return {"reply": ai_service.chat(payload.message, payload.context)}


@router.post("/api/ai/explain-sentence")
@router.post("/api/help/indonesian")
def explain_sentence(payload: TextPayload) -> dict:
    return ai_service.explain_sentence(payload.text, payload.type)


@router.post("/api/ai/grammar-breakdown")
@router.post("/api/grammar/breakdown")
def grammar(payload: dict) -> dict:
    return {"analysis": grammar_breakdown(payload.get("sentence", payload.get("text", "")))}


@router.post("/api/ai/writing-feedback")
def writing_feedback(payload: dict) -> dict:
    return ai_service.writing_feedback(payload.get("text", ""))


@router.post("/api/ai/recommend-next-step")
@router.post("/api/ai-tutor/recommendation")
def recommend_next_step(payload: dict) -> dict:
    return recommendation(payload.get("progress", {}))
