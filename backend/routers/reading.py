from fastapi import APIRouter, HTTPException

from backend.services.reading_service import (
    generate_guided_reading_steps,
    generate_passage_map,
    get_reading_journey,
    get_reading_levels,
    get_reading_recommendation,
    get_reading_subskills,
    get_reading_trainer,
    save_reading_attempt,
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


@router.post("/attempt", status_code=201)
def reading_attempt(payload: dict) -> dict:
    try:
        return save_reading_attempt(payload)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
