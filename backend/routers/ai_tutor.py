from fastapi import APIRouter

from backend.schemas import ChatPayload, ContextualHelpPayload, TextPayload
from backend.services.ai_service import ai_service
from backend.services.grammar_service import grammar_breakdown, indonesian_help
from backend.services.grammar_journey_service import save_grammar_attempt
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


@router.post("/api/ai/contextual-help")
def contextual_help(payload: ContextualHelpPayload) -> dict:
    return ai_service.contextual_help(
        payload.text,
        payload.module,
        payload.context_type,
        payload.user_level,
        payload.extra_context,
    )


@router.post("/api/ai/grammar-breakdown")
@router.post("/api/grammar/breakdown")
def grammar(payload: dict) -> dict:
    sentence = payload.get("sentence", payload.get("text", ""))
    analysis = grammar_breakdown(sentence)
    update = save_grammar_attempt(
        {
            "user_id": payload.get("user_id") or payload.get("userId") or "default-user",
            "topic_id": analysis.get("recommended_topic_id", "subject_verb"),
            "activity_type": "deep_grammar_breakdown",
            "score": 100 if sentence.strip() else 0,
            "max_score": 100,
            "mistakes": [],
            "feedback": analysis.get("next_practice") or analysis.get("explanation", ""),
        }
    )
    journey_update = update.get("journey_update", {})
    return {
        "analysis": analysis,
        "journey_update": {
            "skill_type": "grammar",
            "average_score": journey_update.get("skill_journey", {}).get("average_score", 0),
            "next_action": journey_update.get("skill_journey", {}).get("next_action", ""),
            "overall_score": journey_update.get("journey", {}).get("overall_score", 0),
            "recommended_topic_id": analysis.get("recommended_topic_id", "subject_verb"),
        },
    }


@router.post("/api/ai/writing-feedback")
def writing_feedback(payload: dict) -> dict:
    return ai_service.writing_feedback(payload.get("text", ""))


@router.post("/api/ai/recommend-next-step")
@router.post("/api/ai-tutor/recommendation")
def recommend_next_step(payload: dict) -> dict:
    return recommendation(payload.get("progress", {}))
