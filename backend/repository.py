from __future__ import annotations

import time
from typing import Any

from backend.database import decode_json, encode_json, get_connection, now_iso


def lesson_from_row(row) -> dict[str, Any] | None:
    if not row:
        return None
    return {
        "id": row["id"],
        "title": row["title"],
        "level": row["level"],
        "context": row["context"],
        "passage": row["passage"],
        "vocabulary": decode_json(row["vocabulary_json"], []),
        "grammar": row["grammar"],
        "questions": decode_json(row["questions_json"], []),
    }


def vocabulary_from_row(row) -> dict[str, Any] | None:
    if not row:
        return None
    return {
        "id": row["id"],
        "word": row["word"],
        "part": row["part"],
        "meaningId": row["meaning_id"],
        "meaningEn": row["meaning_en"],
        "example": row["example"],
        "answer": row["answer"],
    }


def list_lessons() -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM lessons ORDER BY created_at DESC").fetchall()
    return [lesson_from_row(row) for row in rows]


def get_lesson(lesson_id: str) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM lessons WHERE id = ?", (lesson_id,)).fetchone()
    return lesson_from_row(row)


def upsert_lesson(payload: dict[str, Any]) -> dict[str, Any]:
    lesson_id = payload.get("id") or f"lesson-{int(time.time() * 1000)}"
    now = now_iso()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO lessons (id, title, level, context, passage, vocabulary_json, grammar, questions_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                level = excluded.level,
                context = excluded.context,
                passage = excluded.passage,
                vocabulary_json = excluded.vocabulary_json,
                grammar = excluded.grammar,
                questions_json = excluded.questions_json,
                updated_at = excluded.updated_at
            """,
            (
                lesson_id,
                payload.get("title", "Untitled Lesson"),
                payload.get("level", "Foundation"),
                payload.get("context", ""),
                payload.get("passage", ""),
                encode_json(payload.get("vocabulary", [])),
                payload.get("grammar", ""),
                encode_json(payload.get("questions", [])),
                now,
                now,
            ),
        )
    return get_lesson(lesson_id)


def delete_lesson(lesson_id: str) -> bool:
    with get_connection() as conn:
        result = conn.execute("DELETE FROM lessons WHERE id = ?", (lesson_id,))
    return result.rowcount > 0


def list_vocabulary() -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM vocabulary ORDER BY created_at DESC").fetchall()
    return [vocabulary_from_row(row) for row in rows]


def get_vocabulary_item(item_id: str) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM vocabulary WHERE id = ?", (item_id,)).fetchone()
    return vocabulary_from_row(row)


def upsert_vocabulary(payload: dict[str, Any]) -> dict[str, Any]:
    item_id = payload.get("id") or f"vocab-{int(time.time() * 1000)}"
    now = now_iso()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO vocabulary (id, word, part, meaning_id, meaning_en, example, answer, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                word = excluded.word,
                part = excluded.part,
                meaning_id = excluded.meaning_id,
                meaning_en = excluded.meaning_en,
                example = excluded.example,
                answer = excluded.answer,
                updated_at = excluded.updated_at
            """,
            (
                item_id,
                payload.get("word", ""),
                payload.get("part", ""),
                payload.get("meaningId", payload.get("meaning_id", "")),
                payload.get("meaningEn", payload.get("meaning_en", "")),
                payload.get("example", ""),
                payload.get("answer", ""),
                now,
                now,
            ),
        )
    return get_vocabulary_item(item_id)


def delete_vocabulary(item_id: str) -> bool:
    with get_connection() as conn:
        result = conn.execute("DELETE FROM vocabulary WHERE id = ?", (item_id,))
    return result.rowcount > 0


def get_state() -> dict[str, Any]:
    with get_connection() as conn:
        row = conn.execute("SELECT value_json FROM app_state WHERE key = 'frontend'").fetchone()
    return decode_json(row["value_json"], {}) if row else {}


def set_state(state: dict[str, Any]) -> dict[str, Any]:
    now = now_iso()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO app_state (key, value_json, updated_at)
            VALUES ('frontend', ?, ?)
            ON CONFLICT(key) DO UPDATE SET value_json = excluded.value_json, updated_at = excluded.updated_at
            """,
            (encode_json(state), now),
        )
    return state


def list_admin_content() -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM admin_content ORDER BY created_at DESC").fetchall()
    return [
        {
            "id": row["id"],
            "type": row["content_type"],
            "title": row["title"],
            "payload": decode_json(row["payload_json"], {}),
        }
        for row in rows
    ]


def upsert_admin_content(payload: dict[str, Any], content_id: str | None = None) -> dict[str, Any]:
    item_id = content_id or payload.get("id") or f"content-{int(time.time() * 1000)}"
    now = now_iso()
    content_type = payload.get("type") or payload.get("contentType") or "lesson"
    title = payload.get("title") or payload.get("word") or "Untitled Content"
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO admin_content (id, content_type, title, payload_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                content_type = excluded.content_type,
                title = excluded.title,
                payload_json = excluded.payload_json,
                updated_at = excluded.updated_at
            """,
            (item_id, content_type, title, encode_json(payload), now, now),
        )
    return {"id": item_id, "type": content_type, "title": title, "payload": payload}


def delete_admin_content(content_id: str) -> bool:
    with get_connection() as conn:
        result = conn.execute("DELETE FROM admin_content WHERE id = ?", (content_id,))
    return result.rowcount > 0
