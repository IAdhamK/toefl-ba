from __future__ import annotations

import time
from datetime import datetime, timedelta
from typing import Any

from backend.database import decode_json, encode_json, get_connection, now_iso


SKILL_TYPES = ("reading", "grammar", "vocabulary", "writing", "listening", "scenario")

NEXT_ACTIONS = {
    "reading": "Lanjutkan latihan mencari main idea dalam passage Business Analyst.",
    "grammar": "Latihan menemukan subject dan verb dalam kalimat panjang.",
    "vocabulary": "Ulangi 10 kata yang paling sering salah.",
    "writing": "Tulis paragraf pendek dengan struktur subject + verb yang jelas.",
    "listening": "Dengarkan short dialogue dan jawab pertanyaan detail.",
    "scenario": "Latihan menganalisis kebutuhan stakeholder dalam case BA.",
}

STAGE_NAMES = {
    "reading": "Main idea dan detail",
    "grammar": "Subject dan verb",
    "vocabulary": "Daily review",
    "writing": "Clear requirement writing",
    "listening": "Meeting comprehension",
    "scenario": "Stakeholder analysis",
}


def validate_skill_type(skill_type: str) -> str:
    normalized = (skill_type or "").strip().lower()
    if normalized not in SKILL_TYPES:
        raise ValueError(f"Invalid skill_type: {skill_type}")
    return normalized


def score_to_level(score: float) -> str:
    if score < 40:
        return "Beginner 1"
    if score < 60:
        return "Beginner 2"
    if score < 75:
        return "Intermediate 1"
    if score < 90:
        return "Intermediate 2"
    return "Advanced"


def score_to_status(score: float, completed_count: int) -> str:
    if completed_count == 0:
        return "not_started"
    if score >= 75:
        return "on_track"
    if score >= 50:
        return "needs_practice"
    return "needs_review"


def next_review_date(days: int = 1) -> str:
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S%z")


def row_dict(row) -> dict[str, Any] | None:
    return dict(row) if row else None


def public_learning_journey(row) -> dict[str, Any]:
    item = dict(row)
    item["overall_score"] = round(float(item.get("overall_score") or 0), 1)
    return item


def public_skill_journey(row) -> dict[str, Any]:
    item = dict(row)
    item["average_score"] = round(float(item.get("average_score") or 0), 1)
    return item


def get_default_user_id(user_id: str | None = None) -> str:
    if user_id:
        return user_id
    with get_connection() as conn:
        row = conn.execute("SELECT id FROM users ORDER BY created_at DESC LIMIT 1").fetchone()
    return row["id"] if row else "default-user"


def get_or_create_learning_journey(user_id: str) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    now = now_iso()
    journey_id = f"journey-{user_id}"
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM learning_journeys WHERE user_id = ?", (user_id,)).fetchone()
        if row:
            return public_learning_journey(row)
        conn.execute(
            """
            INSERT INTO learning_journeys (
                id, user_id, current_level, overall_score, total_exercises, learning_streak,
                weakest_skill, strongest_skill, next_recommended_module, last_activity_at, created_at, updated_at
            )
            VALUES (?, ?, 'Beginner 1', 0, 0, 0, 'grammar', 'reading', 'grammar', NULL, ?, ?)
            """,
            (journey_id, user_id, now, now),
        )
        row = conn.execute("SELECT * FROM learning_journeys WHERE user_id = ?", (user_id,)).fetchone()
    for skill_type in SKILL_TYPES:
        get_or_create_skill_journey(user_id, skill_type)
    return public_learning_journey(row)


def get_or_create_skill_journey(user_id: str, skill_type: str) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    skill_type = validate_skill_type(skill_type)
    now = now_iso()
    item_id = f"skill-{user_id}-{skill_type}"
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM skill_journeys WHERE user_id = ? AND skill_type = ?",
            (user_id, skill_type),
        ).fetchone()
        if row:
            return public_skill_journey(row)
        conn.execute(
            """
            INSERT INTO skill_journeys (
                id, user_id, skill_type, current_stage, current_level, average_score,
                completed_count, total_time_spent, last_activity_at, next_action, status, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, 'Beginner 1', 0, 0, 0, NULL, ?, 'not_started', ?, ?)
            """,
            (item_id, user_id, skill_type, STAGE_NAMES[skill_type], NEXT_ACTIONS[skill_type], now, now),
        )
        row = conn.execute(
            "SELECT * FROM skill_journeys WHERE user_id = ? AND skill_type = ?",
            (user_id, skill_type),
        ).fetchone()
    return public_skill_journey(row)


def get_all_skill_journeys(user_id: str) -> list[dict[str, Any]]:
    user_id = get_default_user_id(user_id)
    get_or_create_learning_journey(user_id)
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM skill_journeys
            WHERE user_id = ?
            ORDER BY CASE skill_type
                WHEN 'reading' THEN 1
                WHEN 'grammar' THEN 2
                WHEN 'vocabulary' THEN 3
                WHEN 'writing' THEN 4
                WHEN 'listening' THEN 5
                WHEN 'scenario' THEN 6
                ELSE 99
            END
            """,
            (user_id,),
        ).fetchall()
    return [public_skill_journey(row) for row in rows]


def get_user_journey_summary(user_id: str) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    journey = get_or_create_learning_journey(user_id)
    skills = get_all_skill_journeys(user_id)
    recommendation = generate_next_recommendation(user_id)
    return {
        "user_id": user_id,
        "journey": journey,
        "skills": skills,
        "continue_learning": get_continue_learning_state(user_id),
        "daily_plan": get_daily_study_plan(user_id),
        "review_list": get_review_list(user_id),
        "recommendation": recommendation,
        "mentor_message": mentor_message(journey),
    }


def save_learning_attempt(
    user_id: str,
    skill_type: str,
    activity_id: str,
    activity_type: str,
    score: float,
    max_score: float,
    mistakes: list | None,
    feedback: str,
) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    skill_type = validate_skill_type(skill_type)
    max_score = max(float(max_score or 100), 1)
    score = float(score or 0)
    accuracy = round((score / max_score) * 100, 1)
    now = now_iso()
    attempt_id = f"journey-attempt-{int(time.time() * 1000)}"
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO learning_attempts (
                id, user_id, skill_type, activity_id, activity_type, score, max_score,
                accuracy, mistakes_json, feedback, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                attempt_id,
                user_id,
                skill_type,
                activity_id or f"{skill_type}-activity",
                activity_type or f"{skill_type}_practice",
                score,
                max_score,
                accuracy,
                encode_json(mistakes or []),
                feedback or "",
                now,
            ),
        )
    skill = update_skill_journey_after_attempt(user_id, skill_type, score, max_score)
    journey = update_overall_journey(user_id)
    recommendation = generate_next_recommendation(user_id)
    return {
        "attempt_id": attempt_id,
        "skill_type": skill_type,
        "score": score,
        "max_score": max_score,
        "accuracy": accuracy,
        "skill_journey": skill,
        "journey": journey,
        "recommendation": recommendation,
    }


def update_skill_journey_after_attempt(user_id: str, skill_type: str, score: float, max_score: float) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    skill_type = validate_skill_type(skill_type)
    get_or_create_skill_journey(user_id, skill_type)
    percent_score = round((float(score or 0) / max(float(max_score or 100), 1)) * 100, 1)
    now = now_iso()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT average_score, completed_count FROM skill_journeys WHERE user_id = ? AND skill_type = ?",
            (user_id, skill_type),
        ).fetchone()
        previous_average = float(row["average_score"] or 0)
        previous_count = int(row["completed_count"] or 0)
        completed_count = previous_count + 1
        average_score = round(((previous_average * previous_count) + percent_score) / completed_count, 1)
        conn.execute(
            """
            UPDATE skill_journeys
            SET average_score = ?, completed_count = ?, current_level = ?, current_stage = ?,
                last_activity_at = ?, next_action = ?, status = ?, updated_at = ?
            WHERE user_id = ? AND skill_type = ?
            """,
            (
                average_score,
                completed_count,
                score_to_level(average_score),
                STAGE_NAMES[skill_type],
                now,
                NEXT_ACTIONS[skill_type],
                score_to_status(average_score, completed_count),
                now,
                user_id,
                skill_type,
            ),
        )
        updated = conn.execute(
            "SELECT * FROM skill_journeys WHERE user_id = ? AND skill_type = ?",
            (user_id, skill_type),
        ).fetchone()
    return public_skill_journey(updated)


def update_overall_journey(user_id: str) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    get_or_create_learning_journey(user_id)
    skills = get_all_skill_journeys(user_id)
    scores = [float(skill["average_score"] or 0) for skill in skills]
    overall_score = round(sum(scores) / len(scores), 1) if scores else 0
    if skills and any(score > 0 for score in scores):
        strongest = max(skills, key=lambda item: item["average_score"])
        weakest = min(skills, key=lambda item: item["average_score"])
    else:
        strongest = {"skill_type": "reading"}
        weakest = {"skill_type": "grammar"}
    total_exercises = sum(int(skill["completed_count"] or 0) for skill in skills)
    now = now_iso()
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE learning_journeys
            SET current_level = ?, overall_score = ?, total_exercises = ?,
                learning_streak = CASE WHEN ? > 0 THEN MAX(learning_streak, 1) ELSE learning_streak END,
                weakest_skill = ?, strongest_skill = ?, next_recommended_module = ?,
                last_activity_at = ?, updated_at = ?
            WHERE user_id = ?
            """,
            (
                score_to_level(overall_score),
                overall_score,
                total_exercises,
                total_exercises,
                weakest["skill_type"],
                strongest["skill_type"],
                weakest["skill_type"],
                now if total_exercises else None,
                now,
                user_id,
            ),
        )
        row = conn.execute("SELECT * FROM learning_journeys WHERE user_id = ?", (user_id,)).fetchone()
    return public_learning_journey(row)


def update_skill_mastery(user_id: str, skill_type: str, topic: str, is_correct: bool, score: float) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    skill_type = validate_skill_type(skill_type)
    topic = topic or STAGE_NAMES[skill_type]
    now = now_iso()
    item_id = f"mastery-{user_id}-{skill_type}-{slug(topic)}"
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM skill_mastery WHERE user_id = ? AND skill_type = ? AND topic = ?",
            (user_id, skill_type, topic),
        ).fetchone()
        if row:
            attempt_count = int(row["attempt_count"] or 0) + 1
            correct_count = int(row["correct_count"] or 0) + (1 if is_correct else 0)
            wrong_count = int(row["wrong_count"] or 0) + (0 if is_correct else 1)
            previous = float(row["mastery_score"] or 0)
            mastery_score = round(((previous * (attempt_count - 1)) + float(score or 0)) / attempt_count, 1)
            conn.execute(
                """
                UPDATE skill_mastery
                SET mastery_score = ?, attempt_count = ?, correct_count = ?, wrong_count = ?,
                    last_practiced_at = ?, next_review_at = ?, updated_at = ?
                WHERE id = ?
                """,
                (mastery_score, attempt_count, correct_count, wrong_count, now, next_review_date(1 if not is_correct else 3), now, row["id"]),
            )
        else:
            conn.execute(
                """
                INSERT INTO skill_mastery (
                    id, user_id, skill_type, topic, mastery_score, attempt_count, correct_count,
                    wrong_count, last_practiced_at, next_review_at, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item_id,
                    user_id,
                    skill_type,
                    topic,
                    float(score or 0),
                    1 if is_correct else 0,
                    0 if is_correct else 1,
                    now,
                    next_review_date(1 if not is_correct else 3),
                    now,
                    now,
                ),
            )
        updated = conn.execute("SELECT * FROM skill_mastery WHERE id = ?", (item_id if not row else row["id"],)).fetchone()
    return dict(updated)


def update_vocabulary_memory(user_id: str, word: str, meaning: str, context: str, is_correct: bool) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    word = (word or "").strip()
    if not word:
        return {}
    now = now_iso()
    item_id = f"vocab-memory-{user_id}-{slug(word)}"
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM vocabulary_memory WHERE user_id = ? AND word = ?", (user_id, word)).fetchone()
        if row:
            review_count = int(row["review_count"] or 0) + 1
            wrong_count = int(row["wrong_count"] or 0) + (0 if is_correct else 1)
            previous = float(row["mastery_score"] or 0)
            target = 100 if is_correct else 35
            mastery_score = round((previous * (review_count - 1) + target) / review_count, 1)
            status = "mastered" if mastery_score >= 80 and wrong_count <= 1 else "needs_review" if not is_correct else "learning"
            conn.execute(
                """
                UPDATE vocabulary_memory
                SET meaning = ?, context = ?, mastery_score = ?, review_count = ?, wrong_count = ?,
                    last_reviewed_at = ?, next_review_at = ?, status = ?, updated_at = ?
                WHERE id = ?
                """,
                (meaning, context, mastery_score, review_count, wrong_count, now, next_review_date(1 if not is_correct else 3), status, now, row["id"]),
            )
            item_id = row["id"]
        else:
            conn.execute(
                """
                INSERT INTO vocabulary_memory (
                    id, user_id, word, meaning, context, mastery_score, review_count, wrong_count,
                    last_reviewed_at, next_review_at, status, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item_id,
                    user_id,
                    word,
                    meaning,
                    context,
                    100 if is_correct else 35,
                    0 if is_correct else 1,
                    now,
                    next_review_date(1 if not is_correct else 3),
                    "learning" if is_correct else "needs_review",
                    now,
                    now,
                ),
            )
        updated = conn.execute("SELECT * FROM vocabulary_memory WHERE id = ?", (item_id,)).fetchone()
    return dict(updated)


def generate_next_recommendation(user_id: str) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    journey = get_or_create_learning_journey(user_id)
    target_skill = journey.get("weakest_skill") or "grammar"
    reason = f"Skill {target_skill} masih menjadi area yang paling perlu diperkuat."
    action = NEXT_ACTIONS.get(target_skill, NEXT_ACTIONS["grammar"])
    now = now_iso()
    recommendation_id = f"recommendation-{user_id}-{int(time.time() * 1000)}"
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO ai_recommendations (
                id, user_id, recommendation_type, source_skill, target_skill, reason,
                recommended_action, priority, status, created_at, updated_at
            )
            VALUES (?, ?, 'next_action', ?, ?, ?, ?, 1, 'active', ?, ?)
            """,
            (recommendation_id, user_id, target_skill, target_skill, reason, action, now, now),
        )
    return {
        "id": recommendation_id,
        "recommendation_type": "next_action",
        "source_skill": target_skill,
        "target_skill": target_skill,
        "reason": reason,
        "recommended_action": action,
        "priority": 1,
        "status": "active",
    }


def get_recent_recommendations(user_id: str, limit: int = 5) -> list[dict[str, Any]]:
    user_id = get_default_user_id(user_id)
    generate_next_recommendation(user_id)
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM ai_recommendations
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
    return [dict(row) for row in rows]


def get_daily_study_plan(user_id: str) -> list[dict[str, str]]:
    user_id = get_default_user_id(user_id)
    journey = get_or_create_learning_journey(user_id)
    weakest = journey.get("weakest_skill") or "grammar"
    plan = [
        {
            "skill_type": weakest,
            "title": f"Fokus {label_skill(weakest)}",
            "task": NEXT_ACTIONS.get(weakest, NEXT_ACTIONS["grammar"]),
            "duration": "10 menit",
        },
        {
            "skill_type": "vocabulary",
            "title": "Review Vocabulary",
            "task": "Review 10 kata yang paling sering salah atau belum dikuasai.",
            "duration": "10 menit",
        },
        {
            "skill_type": "listening",
            "title": "Short Dialogue",
            "task": "Baca transcript meeting pendek lalu jawab masalah utamanya.",
            "duration": "10 menit",
        },
    ]
    return plan


def get_continue_learning_state(user_id: str) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    journey = get_or_create_learning_journey(user_id)
    with get_connection() as conn:
        attempt = conn.execute(
            """
            SELECT * FROM learning_attempts
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (user_id,),
        ).fetchone()
    recommended = journey.get("next_recommended_module") or "grammar"
    return {
        "last_activity": dict(attempt) if attempt else None,
        "recommended_module": recommended,
        "next_action": NEXT_ACTIONS.get(recommended, NEXT_ACTIONS["grammar"]),
        "message": f"Lanjutkan dari {label_skill(recommended)}. {NEXT_ACTIONS.get(recommended, NEXT_ACTIONS['grammar'])}",
    }


def get_review_list(user_id: str) -> dict[str, list[dict[str, Any]]]:
    user_id = get_default_user_id(user_id)
    with get_connection() as conn:
        vocabulary_rows = conn.execute(
            """
            SELECT * FROM vocabulary_memory
            WHERE user_id = ? AND (status = 'needs_review' OR mastery_score < 70)
            ORDER BY wrong_count DESC, next_review_at ASC
            LIMIT 10
            """,
            (user_id,),
        ).fetchall()
        grammar_rows = conn.execute(
            """
            SELECT * FROM skill_mastery
            WHERE user_id = ? AND skill_type = 'grammar' AND mastery_score < 70
            ORDER BY wrong_count DESC, next_review_at ASC
            LIMIT 10
            """,
            (user_id,),
        ).fetchall()
        due_rows = conn.execute(
            """
            SELECT word AS item, 'vocabulary' AS source, next_review_at
            FROM vocabulary_memory
            WHERE user_id = ? AND next_review_at IS NOT NULL
            ORDER BY next_review_at ASC
            LIMIT 10
            """,
            (user_id,),
        ).fetchall()
    return {
        "weak_vocabulary": [dict(row) for row in vocabulary_rows],
        "weak_grammar_topics": [dict(row) for row in grammar_rows],
        "due_for_review": [dict(row) for row in due_rows],
    }


def reset_journey_data(user_id: str) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    with get_connection() as conn:
        for table in (
            "learning_journeys",
            "skill_journeys",
            "learning_attempts",
            "skill_mastery",
            "vocabulary_memory",
            "ai_recommendations",
        ):
            conn.execute(f"DELETE FROM {table} WHERE user_id = ?", (user_id,))
    return get_user_journey_summary(user_id)


def backfill_user_journeys() -> dict[str, int]:
    with get_connection() as conn:
        users = [row["id"] for row in conn.execute("SELECT id FROM users").fetchall()]
    if not users:
        users = ["default-user"]
    for user_id in users:
        get_or_create_learning_journey(user_id)
        update_overall_journey(user_id)
    return {"users": len(users), "skills": len(users) * len(SKILL_TYPES)}


def mentor_message(journey: dict[str, Any]) -> str:
    weakest = journey.get("weakest_skill") or "grammar"
    strongest = journey.get("strongest_skill") or "reading"
    if weakest == strongest:
        return f"Progress Anda sudah berjalan. Hari ini sebaiknya fokus ke {label_skill(weakest)} sebagai langkah awal yang paling ringan."
    return (
        f"Progress Anda sudah berjalan. Hari ini sebaiknya fokus ke {label_skill(weakest)} "
        f"karena skor rata-rata masih lebih rendah dibanding {label_skill(strongest)}."
    )


def label_skill(skill_type: str) -> str:
    labels = {
        "reading": "Reading",
        "grammar": "Grammar",
        "vocabulary": "Vocabulary",
        "writing": "Writing",
        "listening": "Listening",
        "scenario": "Scenario BA",
    }
    return labels.get(skill_type, skill_type.title())


def slug(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")[:80]
