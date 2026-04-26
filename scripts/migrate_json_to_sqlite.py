from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from backend.database import get_connection, init_db, load_json_data, now_iso
from backend.repository import set_state, upsert_lesson, upsert_vocabulary


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

    return {
        "lessons": len(lessons),
        "vocabulary": len(vocabulary),
        "users": len(users),
        "state": bool(data.get("state")),
    }


if __name__ == "__main__":
    result = migrate()
    print("Migrasi JSON ke SQLite selesai.")
    print(f"- Lessons: {result['lessons']}")
    print(f"- Vocabulary: {result['vocabulary']}")
    print(f"- Users: {result['users']}")
    print(f"- State frontend: {'ada' if result['state'] else 'kosong'}")
