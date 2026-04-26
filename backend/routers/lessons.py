from fastapi import APIRouter, HTTPException

from backend.repository import delete_lesson, get_lesson, list_lessons, upsert_lesson
from backend.schemas import LessonPayload


router = APIRouter(prefix="/api/lessons", tags=["lessons"])


@router.get("")
def get_lessons() -> dict:
    return {"lessons": list_lessons()}


@router.get("/{lesson_id}")
def get_lesson_by_id(lesson_id: str) -> dict:
    lesson = get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return {"lesson": lesson}


@router.post("", status_code=201)
def create_lesson(payload: LessonPayload) -> dict:
    return {"lesson": upsert_lesson(payload.dict())}


@router.put("/{lesson_id}")
def update_lesson(lesson_id: str, payload: LessonPayload) -> dict:
    data = payload.dict()
    data["id"] = lesson_id
    return {"lesson": upsert_lesson(data)}


@router.delete("/{lesson_id}")
def remove_lesson(lesson_id: str) -> dict:
    if not delete_lesson(lesson_id):
        raise HTTPException(status_code=404, detail="Lesson not found")
    return {"ok": True}
