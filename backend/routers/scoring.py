from fastapi import APIRouter, HTTPException

from backend.repository import get_lesson
from backend.services.listening_service import evaluate_listening
from backend.services.scoring_service import evaluate_writing, score_reading, score_scenario, score_vocabulary
from backend.repository import get_vocabulary_item
from backend.services.journey_service import save_learning_attempt, update_skill_mastery, update_vocabulary_memory
from backend.services.reading_service import generate_answer_review, get_reading_journey, update_reading_subskills_from_quiz


router = APIRouter(tags=["scoring"])


@router.post("/api/scoring/reading")
@router.post("/api/reading/submit-answer")
def reading_score(payload: dict) -> dict:
    lesson = get_lesson(payload.get("lessonId", ""))
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    result = score_reading(lesson, payload.get("answers", {}))
    mistakes = [item for item in result.get("details", []) if not item.get("isCorrect")]
    update = save_learning_attempt(
        payload.get("user_id") or payload.get("userId") or "default-user",
        "reading",
        payload.get("lessonId", lesson["id"]),
        "reading_quiz",
        result.get("score", 0),
        100,
        mistakes,
        "Reading selesai. Perhatikan main idea dan bukti jawaban di passage.",
    )
    update_skill_mastery(
        payload.get("user_id") or payload.get("userId") or "default-user",
        "reading",
        lesson.get("context") or "main idea",
        result.get("score", 0) >= 75,
        result.get("score", 0),
    )
    update_reading_subskills_from_quiz(
        payload.get("user_id") or payload.get("userId") or "default-user",
        lesson,
        result,
    )
    result["answer_reviews"] = build_reading_answer_reviews(lesson, payload.get("answers", {}))
    result["journey_update"] = compact_journey_update(update)
    result["reading_journey_update"] = get_reading_journey(payload.get("user_id") or payload.get("userId") or "default-user")
    return result


@router.post("/api/scoring/vocabulary")
def vocabulary_score(payload: dict) -> dict:
    item = get_vocabulary_item(payload.get("itemId", ""))
    if not item:
        raise HTTPException(status_code=404, detail="Vocabulary item not found")
    result = score_vocabulary(item, payload.get("answer", ""))
    update = save_learning_attempt(
        payload.get("user_id") or payload.get("userId") or "default-user",
        "vocabulary",
        item["id"],
        "vocabulary_drill",
        result.get("score", 0),
        100,
        [] if result.get("isCorrect") else [{"word": item.get("word"), "answer": payload.get("answer", "")}],
        result.get("explanation", ""),
    )
    update_vocabulary_memory(
        payload.get("user_id") or payload.get("userId") or "default-user",
        item.get("word", ""),
        item.get("meaningId", ""),
        item.get("example", ""),
        bool(result.get("isCorrect")),
    )
    result["journey_update"] = compact_journey_update(update)
    return result


@router.post("/api/scoring/writing")
@router.post("/api/writing/evaluate")
def writing_score(payload: dict) -> dict:
    result = evaluate_writing(payload.get("text", ""))
    update = save_learning_attempt(
        payload.get("user_id") or payload.get("userId") or "default-user",
        "writing",
        payload.get("activity_id", "writing-evaluate"),
        "writing_feedback",
        result.get("score", 0),
        100,
        result.get("issues", []),
        result.get("recommendation", ""),
    )
    update_skill_mastery(
        payload.get("user_id") or payload.get("userId") or "default-user",
        "writing",
        "requirement clarity",
        result.get("score", 0) >= 75,
        result.get("score", 0),
    )
    result["journey_update"] = compact_journey_update(update)
    return result


@router.post("/api/scoring/listening")
@router.post("/api/listening/submit-answer")
def listening_score(payload: dict) -> dict:
    result = evaluate_listening(payload.get("answer", ""))
    update = save_learning_attempt(
        payload.get("user_id") or payload.get("userId") or "default-user",
        "listening",
        payload.get("activity_id", "listening-default"),
        "listening_question",
        result.get("score", 0),
        100,
        [] if result.get("isCorrect") else [{"answer": payload.get("answer", "")}],
        result.get("explanation", ""),
    )
    result["journey_update"] = compact_journey_update(update)
    return result


@router.post("/api/scoring/scenario")
@router.post("/api/scenario/submit-answer")
def scenario_score(payload: dict) -> dict:
    result = score_scenario(payload.get("questionId", ""), payload.get("selected"))
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    update = save_learning_attempt(
        payload.get("user_id") or payload.get("userId") or "default-user",
        "scenario",
        payload.get("questionId", "scenario-question"),
        "scenario_ba_practice",
        result.get("score", 0),
        100,
        [] if result.get("isCorrect") else [{"selected": payload.get("selected"), "correctAnswer": result.get("correctAnswer")}],
        result.get("explanation", ""),
    )
    result["journey_update"] = compact_journey_update(update)
    return result


def compact_journey_update(update: dict) -> dict:
    skill = update.get("skill_journey", {})
    return {
        "skill_type": update.get("skill_type"),
        "average_score": skill.get("average_score", 0),
        "current_level": skill.get("current_level", "Beginner 1"),
        "next_action": skill.get("next_action", ""),
        "overall_score": update.get("journey", {}).get("overall_score", 0),
        "recommended_module": update.get("journey", {}).get("next_recommended_module", "grammar"),
    }


def build_reading_answer_reviews(lesson: dict, answers: dict) -> list[dict]:
    reviews = []
    for question in lesson.get("questions", []):
        selected = answers.get(question.get("id"))
        if selected is None:
            continue
        reviews.append(
            generate_answer_review(
                {
                    "passage": lesson.get("passage", ""),
                    "question": question,
                    "selected": selected,
                    "correct_answer": question.get("answer"),
                    "explanation": question.get("explanation", ""),
                    "sub_skill": question.get("sub_skill") or question.get("question_type"),
                }
            )
        )
    return reviews
