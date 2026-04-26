from fastapi import APIRouter, HTTPException

from backend.repository import get_lesson
from backend.services.listening_service import evaluate_listening
from backend.services.scoring_service import evaluate_writing, score_reading, score_scenario, score_vocabulary
from backend.repository import get_vocabulary_item


router = APIRouter(tags=["scoring"])


@router.post("/api/scoring/reading")
@router.post("/api/reading/submit-answer")
def reading_score(payload: dict) -> dict:
    lesson = get_lesson(payload.get("lessonId", ""))
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return score_reading(lesson, payload.get("answers", {}))


@router.post("/api/scoring/vocabulary")
def vocabulary_score(payload: dict) -> dict:
    item = get_vocabulary_item(payload.get("itemId", ""))
    if not item:
        raise HTTPException(status_code=404, detail="Vocabulary item not found")
    return score_vocabulary(item, payload.get("answer", ""))


@router.post("/api/scoring/writing")
@router.post("/api/writing/evaluate")
def writing_score(payload: dict) -> dict:
    return evaluate_writing(payload.get("text", ""))


@router.post("/api/scoring/listening")
@router.post("/api/listening/submit-answer")
def listening_score(payload: dict) -> dict:
    return evaluate_listening(payload.get("answer", ""))


@router.post("/api/scoring/scenario")
@router.post("/api/scenario/submit-answer")
def scenario_score(payload: dict) -> dict:
    result = score_scenario(payload.get("questionId", ""), payload.get("selected"))
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
