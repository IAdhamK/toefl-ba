from fastapi import APIRouter, HTTPException

from backend.services.reading_service import (
    generate_guided_reading_steps,
    generate_answer_review,
    generate_passage_map,
    get_reading_journey,
    get_reading_levels,
    get_reading_mistake_patterns,
    get_reading_recommendation,
    get_reading_review,
    get_reading_review_queue,
    get_reading_simulation_history,
    get_reading_simulation_result,
    get_reading_subskills,
    get_reading_trainer,
    save_reading_attempt,
    start_reading_simulation,
    submit_reading_simulation,
)
from backend.services.reading_progress_service import (
    get_reading_finish_status,
    get_reading_learning_path,
    get_reading_module_progress,
    get_reading_progress_summary,
    get_recommended_reading_section,
)


router = APIRouter(prefix="/api/reading", tags=["reading"])


@router.get("/journey")
def reading_journey(user_id: str | None = None) -> dict:
    return {"reading_journey": get_reading_journey(user_id)}


@router.get("/levels")
def reading_levels() -> dict:
    return get_reading_levels()


@router.get("/recommendation")
def reading_recommendation(user_id: str | None = None) -> dict:
    return {"recommendation": get_reading_recommendation(user_id)}


@router.get("/progress")
def reading_progress(user_id: str | None = None) -> dict:
    return get_reading_module_progress(user_id)


@router.get("/progress/summary")
def reading_progress_summary(user_id: str | None = None) -> dict:
    return {"summary": get_reading_progress_summary(user_id)}


@router.get("/progress/modules")
def reading_progress_modules(user_id: str | None = None) -> dict:
    return {"modules": get_reading_module_progress(user_id)["modules"]}


@router.get("/progress/path")
def reading_progress_path(user_id: str | None = None) -> dict:
    return get_reading_learning_path(user_id)


@router.get("/progress/recommended-section")
def reading_progress_recommended_section(user_id: str | None = None) -> dict:
    return {"recommended_section": get_recommended_reading_section(user_id)}


@router.get("/progress/finish-status")
def reading_progress_finish_status(user_id: str | None = None) -> dict:
    return {"finish_status": get_reading_finish_status(user_id)}


@router.get("/review")
def reading_review(user_id: str | None = None) -> dict:
    return get_reading_review(user_id)


@router.get("/mistake-patterns")
def reading_mistake_patterns(user_id: str | None = None) -> dict:
    return get_reading_mistake_patterns(user_id)


@router.get("/review-queue")
def reading_review_queue(user_id: str | None = None) -> dict:
    return get_reading_review_queue(user_id)


@router.post("/simulation/start")
def reading_simulation_start(payload: dict) -> dict:
    try:
        return start_reading_simulation(payload)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/simulation/submit")
def reading_simulation_submit(payload: dict) -> dict:
    try:
        return submit_reading_simulation(payload)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("/simulation/result/{session_id}")
def reading_simulation_result(session_id: str, user_id: str | None = None) -> dict:
    try:
        return get_reading_simulation_result(session_id, user_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/simulation/history")
def reading_simulation_history(user_id: str | None = None) -> dict:
    return get_reading_simulation_history(user_id)


@router.get("/subskills")
def reading_subskills(user_id: str | None = None) -> dict:
    return get_reading_subskills(user_id)


@router.get("/trainer/{sub_skill}")
def reading_trainer(sub_skill: str, user_id: str | None = None) -> dict:
    try:
        return get_reading_trainer(sub_skill, user_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/guided-steps")
def reading_guided_steps(payload: dict) -> dict:
    try:
        return generate_guided_reading_steps(payload)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/passage-map")
def reading_passage_map(payload: dict) -> dict:
    try:
        return generate_passage_map(payload)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/review-answer")
def reading_review_answer(payload: dict) -> dict:
    try:
        return {"answer_review": generate_answer_review(payload)}
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/attempt", status_code=201)
def reading_attempt(payload: dict) -> dict:
    try:
        return save_reading_attempt(payload)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
