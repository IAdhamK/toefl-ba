from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from backend.database import get_connection, init_db, load_json_data, now_iso
from backend.repository import set_state, upsert_lesson, upsert_vocabulary
from backend.services.journey_service import (
    SKILL_TYPES,
    backfill_user_journeys,
    save_learning_attempt,
)


def migrate() -> dict:
    init_db()
    data = load_json_data()
    if not data:
        return {"lessons": 0, "vocabulary": 0, "users": 0, "state": False}

    lessons = data.get("lessons", [])
    vocabulary = data.get("vocabulary", [])
    users = data.get("users", [])
    sessions = data.get("sessions", {})
    now = now_iso()

    for lesson in lessons:
        upsert_lesson(lesson)
    for item in vocabulary:
        upsert_vocabulary(item)

    with get_connection() as conn:
        for user in users:
            conn.execute(
                """
                INSERT OR IGNORE INTO users (id, name, email, target_score, weakness, level, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user.get("id"),
                    user.get("name", "Junior BA Learner"),
                    user.get("email"),
                    user.get("targetScore", 500),
                    user.get("weakness", "Grammar"),
                    user.get("level", "Foundation"),
                    now,
                ),
            )
        for token, user_id in sessions.items():
            conn.execute(
                "INSERT OR REPLACE INTO sessions (token, user_id, created_at) VALUES (?, ?, ?)",
                (token, user_id, now),
            )

    if data.get("state"):
        set_state(data["state"])
        backfill_progress_from_state(data["state"], users)

    journey_result = backfill_user_journeys()

    return {
        "lessons": len(lessons),
        "vocabulary": len(vocabulary),
        "users": len(users),
        "state": bool(data.get("state")),
        "journey_users": journey_result["users"],
    }


def backfill_progress_from_state(state: dict, users: list[dict]) -> None:
    progress = state.get("progress", {})
    if not progress:
        return
    user_id = (state.get("user") or {}).get("id") or (users[0].get("id") if users else "default-user")
    for label, score in progress.items():
        skill_type = label.lower()
        if skill_type not in SKILL_TYPES:
            continue
        with get_connection() as conn:
            existing = conn.execute(
                """
                SELECT COUNT(*) AS total FROM learning_attempts
                WHERE user_id = ? AND skill_type = ? AND activity_id = ?
                """,
                (user_id, skill_type, f"legacy-{skill_type}"),
            ).fetchone()
        if existing and existing["total"]:
            continue
        try:
            save_learning_attempt(
                user_id=user_id,
                skill_type=skill_type,
                activity_id=f"legacy-{skill_type}",
                activity_type="legacy_progress_import",
                score=float(score or 0),
                max_score=100,
                mistakes=[],
                feedback="Diimpor dari progress MVP lama.",
            )
        except Exception:
            continue


if __name__ == "__main__":
    result = migrate()
    print("Migrasi JSON ke SQLite selesai.")
    print(f"- Lessons: {result['lessons']}")
    print(f"- Vocabulary: {result['vocabulary']}")
    print(f"- Users: {result['users']}")
    print(f"- State frontend: {'ada' if result['state'] else 'kosong'}")
    print(f"- Journey users: {result['journey_users']}")
