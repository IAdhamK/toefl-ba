from fastapi import APIRouter, HTTPException, Query

from backend.services.journey_service import (
    SKILL_TYPES,
    complete_adaptive_practice,
    generate_next_recommendation,
    get_adaptive_mentor_summary,
    get_adaptive_practice,
    get_all_skill_journeys,
    get_continue_learning_state,
    get_daily_study_plan,
    get_default_user_id,
    get_or_create_skill_journey,
    get_recent_recommendations,
    get_review_list,
    get_user_journey_summary,
    reset_journey_data,
    save_learning_attempt,
    validate_skill_type,
)


router = APIRouter(prefix="/api/journey", tags=["journey"])


@router.get("/summary")
def journey_summary(user_id: str | None = None) -> dict:
    return get_user_journey_summary(get_default_user_id(user_id))


@router.get("/skills")
def journey_skills(user_id: str | None = None) -> dict:
    return {"skills": get_all_skill_journeys(get_default_user_id(user_id))}


@router.get("/skills/{skill_type}")
def journey_skill(skill_type: str, user_id: str | None = None) -> dict:
    try:
        normalized = validate_skill_type(skill_type)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"skill": get_or_create_skill_journey(get_default_user_id(user_id), normalized)}


@router.post("/attempt", status_code=201)
def journey_attempt(payload: dict) -> dict:
    try:
        update = save_learning_attempt(
            user_id=payload.get("user_id") or payload.get("userId") or get_default_user_id(None),
            skill_type=payload.get("skill_type", ""),
            activity_id=payload.get("activity_id", ""),
            activity_type=payload.get("activity_type", ""),
            score=payload.get("score", 0),
            max_score=payload.get("max_score", 100),
            mistakes=payload.get("mistakes", []),
            feedback=payload.get("feedback", ""),
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"journey_update": update}


@router.get("/continue")
def continue_learning(user_id: str | None = None) -> dict:
    return get_continue_learning_state(get_default_user_id(user_id))


@router.get("/recommendations")
def recommendations(user_id: str | None = None) -> dict:
    resolved_user_id = get_default_user_id(user_id)
    return {
        "current": generate_next_recommendation(resolved_user_id),
        "items": get_recent_recommendations(resolved_user_id),
    }


@router.get("/daily-plan")
def daily_plan(user_id: str | None = None) -> dict:
    return {"plan": get_daily_study_plan(get_default_user_id(user_id))}


@router.get("/review-list")
def review_list(user_id: str | None = None) -> dict:
    return get_review_list(get_default_user_id(user_id))


@router.get("/adaptive-practice")
def adaptive_practice(user_id: str | None = None, skill_type: str | None = None) -> dict:
    try:
        return get_adaptive_practice(get_default_user_id(user_id), skill_type)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("/mentor-summary")
def mentor_summary(user_id: str | None = None) -> dict:
    return get_adaptive_mentor_summary(get_default_user_id(user_id))


@router.post("/adaptive-practice/complete")
def adaptive_practice_complete(payload: dict) -> dict:
    try:
        return complete_adaptive_practice(
            user_id=payload.get("user_id") or payload.get("userId") or get_default_user_id(None),
            skill_type=payload.get("skill_type", ""),
            score=payload.get("score", 0),
            max_score=payload.get("max_score", 100),
            notes=payload.get("notes", ""),
            mistakes=payload.get("mistakes", []),
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/reset")
def reset_for_development(user_id: str | None = None, dev: bool = Query(default=False)) -> dict:
    # Dev-only helper. It is disabled unless the caller explicitly passes ?dev=true.
    if not dev:
        raise HTTPException(status_code=403, detail="Reset journey hanya tersedia dengan dev=true.")
    return reset_journey_data(get_default_user_id(user_id))
