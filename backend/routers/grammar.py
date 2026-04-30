from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from backend.services.grammar_error_service import (
    get_error_categories,
    get_error_category,
    get_error_correction_items,
    submit_error_correction,
)
from backend.services.grammar_advanced_service import (
    get_advanced_practice_items,
    get_advanced_rewrite_items,
    get_advanced_topic,
    get_advanced_topics,
    submit_advanced_practice,
    submit_advanced_rewrite,
)
from backend.services.grammar_sentence_builder_service import (
    get_sentence_builder_item,
    get_sentence_builder_items,
    get_sentence_builder_levels,
    submit_sentence_builder,
)
from backend.services.grammar_simulation_service import (
    get_grammar_simulation_history,
    get_grammar_simulation_result,
    get_simulation_modes,
    start_grammar_simulation,
    submit_grammar_simulation,
)
from backend.services.grammar_service import grammar_breakdown
from backend.services.grammar_journey_service import (
    build_grammar_recommendation,
    get_grammar_journey,
    get_grammar_topic_mastery,
    get_next_recommended_grammar_topic,
    get_strongest_grammar_topic,
    get_weakest_grammar_topic,
    save_grammar_attempt,
)
from backend.services.grammar_review_service import (
    get_grammar_mistake_patterns,
    get_grammar_recommended_practice,
    get_grammar_review,
    get_grammar_review_queue,
    get_grammar_weakness_summary,
)
from backend.services.grammar_topic_service import (
    get_grammar_levels,
    get_grammar_topic,
    get_grammar_topics,
    get_next_topic,
    get_topic_summary,
)
from backend.services.grammar_trainer_service import (
    get_basic_grammar_trainer,
    get_basic_trainer_topics,
    get_intermediate_grammar_trainer,
    get_intermediate_trainer_topics,
    submit_basic_grammar_trainer,
    submit_intermediate_grammar_trainer,
)


router = APIRouter(prefix="/api/grammar", tags=["grammar"])


@router.get("/levels")
def grammar_levels() -> dict:
    return {"levels": get_grammar_levels()}


@router.get("/topics")
def grammar_topics(level: str | None = Query(default=None)) -> dict:
    topics = get_grammar_topics(level)
    return {"topics": topics, "total": len(topics), "level": level}


@router.get("/topics/{topic_id}")
def grammar_topic(topic_id: str) -> dict:
    topic = get_grammar_topic(topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Grammar topic tidak ditemukan.")
    return {"topic": topic}


@router.get("/topic-summary")
def grammar_topic_summary() -> dict:
    return {"summary": get_topic_summary()}


@router.get("/next-topic")
def grammar_next_topic(current_topic_id: str | None = Query(default=None)) -> dict:
    return {"next_topic": get_next_topic(current_topic_id)}


@router.get("/journey")
def grammar_journey(user_id: str | None = Query(default=None)) -> dict:
    return {"grammar_journey": get_grammar_journey(user_id)}


@router.post("/attempt", status_code=201)
def grammar_attempt(payload: dict) -> dict:
    return save_grammar_attempt(payload)


@router.get("/mastery")
def grammar_mastery(user_id: str | None = Query(default=None)) -> dict:
    return {
        "topic_mastery": get_grammar_topic_mastery(user_id),
        "weakest_topic": get_weakest_grammar_topic(user_id),
        "strongest_topic": get_strongest_grammar_topic(user_id),
        "next_recommended_topic": get_next_recommended_grammar_topic(user_id),
    }


@router.get("/recommendation")
def grammar_recommendation(user_id: str | None = Query(default=None)) -> dict:
    return {"recommendation": build_grammar_recommendation(user_id)}


@router.get("/review")
def grammar_review(user_id: str | None = Query(default=None)) -> dict:
    return get_grammar_review(user_id)


@router.get("/mistake-patterns")
def grammar_mistake_patterns(user_id: str | None = Query(default=None)) -> dict:
    return get_grammar_mistake_patterns(user_id)


@router.get("/review-queue")
def grammar_review_queue(user_id: str | None = Query(default=None)) -> dict:
    return get_grammar_review_queue(user_id)


@router.get("/weakness-summary")
def grammar_weakness_summary(user_id: str | None = Query(default=None)) -> dict:
    return {"weakness_summary": get_grammar_weakness_summary(user_id)}


@router.get("/recommended-practice")
def grammar_recommended_practice(user_id: str | None = Query(default=None)) -> dict:
    weakness = get_grammar_weakness_summary(user_id)
    patterns = get_grammar_mistake_patterns(user_id)["patterns"]
    return {
        "recommended_practice": get_grammar_recommended_practice(user_id),
        "mentor_message": get_grammar_review(user_id).get("mentor_message")
        or "Lanjutkan latihan grammar yang direkomendasikan.",
        "weakness_summary": weakness,
        "primary_pattern": patterns[0] if patterns else {},
    }


@router.get("/trainer/basic")
def grammar_basic_trainer_topics() -> dict:
    return {"topics": get_basic_trainer_topics()}


@router.get("/trainer/basic/{topic_id}")
def grammar_basic_trainer(topic_id: str) -> dict:
    trainer = get_basic_grammar_trainer(topic_id)
    if trainer is None:
        raise HTTPException(status_code=404, detail="Basic grammar trainer topic tidak ditemukan.")
    return {"trainer": trainer}


@router.post("/trainer/basic/submit")
def grammar_basic_trainer_submit(payload: dict) -> dict:
    return submit_basic_grammar_trainer(payload)


@router.get("/trainer/intermediate")
def grammar_intermediate_trainer_topics() -> dict:
    return {"topics": get_intermediate_trainer_topics()}


@router.get("/trainer/intermediate/{topic_id}")
def grammar_intermediate_trainer(topic_id: str) -> dict:
    trainer = get_intermediate_grammar_trainer(topic_id)
    if trainer is None:
        raise HTTPException(status_code=404, detail="Intermediate grammar trainer topic tidak ditemukan.")
    return {"trainer": trainer}


@router.post("/trainer/intermediate/submit")
def grammar_intermediate_trainer_submit(payload: dict) -> dict:
    return submit_intermediate_grammar_trainer(payload)


@router.get("/error-correction/categories")
def grammar_error_categories() -> dict:
    return {"categories": get_error_categories()}


@router.get("/error-correction")
def grammar_error_correction_items(error_type: str | None = Query(default=None), level: str | None = Query(default=None)) -> dict:
    items = get_error_correction_items(error_type=error_type, level=level)
    return {"items": items, "total": len(items), "filters": {"error_type": error_type, "level": level}}


@router.get("/error-correction/{error_type}")
def grammar_error_correction_category(error_type: str) -> dict:
    category = get_error_category(error_type)
    if category is None:
        raise HTTPException(status_code=404, detail="Grammar error category tidak ditemukan.")
    return {"category": category, "items": get_error_correction_items(error_type=error_type)}


@router.post("/error-correction/submit")
def grammar_error_correction_submit(payload: dict) -> dict:
    return submit_error_correction(payload)


@router.get("/sentence-builder/levels")
def grammar_sentence_builder_levels() -> dict:
    return {"levels": get_sentence_builder_levels()}


@router.get("/sentence-builder")
def grammar_sentence_builder_items(level: str | None = Query(default=None), mode: str | None = Query(default=None)) -> dict:
    items = get_sentence_builder_items(level=level, mode=mode)
    return {"items": items, "total": len(items), "filters": {"level": level, "mode": mode}}


@router.get("/sentence-builder/{item_id}")
def grammar_sentence_builder_item(item_id: str) -> dict:
    item = get_sentence_builder_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Grammar sentence builder item tidak ditemukan.")
    return {"item": item}


@router.post("/sentence-builder/submit")
def grammar_sentence_builder_submit(payload: dict) -> dict:
    return submit_sentence_builder(payload)


@router.get("/advanced/topics")
def grammar_advanced_topics() -> dict:
    return {"topics": get_advanced_topics()}


@router.get("/advanced/topics/{topic_id}")
def grammar_advanced_topic(topic_id: str) -> dict:
    topic = get_advanced_topic(topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Advanced grammar topic tidak ditemukan.")
    return {"topic": topic}


@router.get("/advanced/practice")
def grammar_advanced_practice(topic_id: str | None = Query(default=None)) -> dict:
    items = get_advanced_practice_items(topic_id)
    return {"items": items, "total": len(items), "topic_id": topic_id}


@router.get("/advanced/rewrite")
def grammar_advanced_rewrite(topic_id: str | None = Query(default=None)) -> dict:
    items = get_advanced_rewrite_items(topic_id)
    return {"items": items, "total": len(items), "topic_id": topic_id}


@router.post("/advanced/practice/submit")
def grammar_advanced_practice_submit(payload: dict) -> dict:
    return submit_advanced_practice(payload)


@router.post("/advanced/rewrite/submit")
def grammar_advanced_rewrite_submit(payload: dict) -> dict:
    return submit_advanced_rewrite(payload)


@router.get("/simulation/modes")
def grammar_simulation_modes() -> dict:
    return {"modes": get_simulation_modes()}


@router.post("/simulation/start")
def grammar_simulation_start(payload: dict) -> dict:
    return start_grammar_simulation(payload)


@router.post("/simulation/submit")
def grammar_simulation_submit(payload: dict) -> dict:
    return submit_grammar_simulation(payload)


@router.get("/simulation/result/{session_id}")
def grammar_simulation_result(session_id: str, user_id: str | None = Query(default=None)) -> dict:
    return get_grammar_simulation_result(session_id, user_id)


@router.get("/simulation/history")
def grammar_simulation_history(user_id: str | None = Query(default=None)) -> dict:
    return get_grammar_simulation_history(user_id)


@router.post("/breakdown/deep")
def grammar_deep_breakdown(payload: dict) -> dict:
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
    return {"analysis": analysis, "grammar_journey": update.get("grammar_journey"), "journey_update": update.get("journey_update")}
