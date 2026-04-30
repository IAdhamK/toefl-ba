from __future__ import annotations

from typing import Any

from backend.database import get_connection
from backend.services.grammar_topic_service import get_grammar_topic, get_grammar_topics, get_next_topic
from backend.services.journey_service import get_default_user_id, save_learning_attempt, update_skill_mastery


DEFAULT_USER_ID = "default-user"


def calculate_grammar_level(score: float, completed_topics: int) -> str:
    if completed_topics == 0:
        return "Basic 1 - Sentence Foundation"
    if score < 25:
        return "Basic 1 - Sentence Foundation"
    if score < 50:
        return "Basic 2 - Subject and Verb Control"
    if score < 70:
        return "Intermediate 1 - Phrase and Clause Awareness"
    if score < 85:
        return "Intermediate 2 - Complex Grammar Control"
    return "Advanced 1 - Professional Grammar Usage"


def get_grammar_journey(user_id: str | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    topic_mastery = get_grammar_topic_mastery(user_id)
    attempted_topics = [item for item in topic_mastery if item["completed_count"] > 0]
    completed_topics = len([item for item in topic_mastery if item["mastery_score"] >= 70])
    grammar_score = round(
        sum(float(item["mastery_score"] or 0) for item in attempted_topics) / len(attempted_topics),
        1,
    ) if attempted_topics else 0
    weakest = get_weakest_grammar_topic(user_id)
    strongest = get_strongest_grammar_topic(user_id)
    next_topic = get_next_recommended_grammar_topic(user_id)
    grammar_level = calculate_grammar_level(grammar_score, completed_topics)
    return {
        "user_id": user_id,
        "grammar_level": grammar_level,
        "grammar_score": grammar_score,
        "completed_topics": completed_topics,
        "total_topics": len(topic_mastery),
        "strongest_topic": strongest,
        "weakest_topic": weakest,
        "next_recommended_topic": next_topic,
        "topic_mastery": topic_mastery,
        "mentor_message": _mentor_message(grammar_score, attempted_topics, weakest),
        "next_action": _topic_next_action(next_topic),
    }


def save_grammar_attempt(payload: dict) -> dict[str, Any]:
    user_id = get_default_user_id(payload.get("user_id") or payload.get("userId") or DEFAULT_USER_ID)
    topic_id = (payload.get("topic_id") or "subject_verb").strip()
    topic = get_grammar_topic(topic_id) or get_grammar_topic("subject_verb")
    max_score = max(float(payload.get("max_score") or 100), 1)
    score = float(payload.get("score") or 0)
    accuracy = round((score / max_score) * 100, 1)
    is_completed = accuracy >= 70
    feedback = payload.get("feedback") or f"Latihan grammar untuk topic {topic['title']} selesai."
    mistakes = payload.get("mistakes") or []
    journey_update = save_learning_attempt(
        user_id=user_id,
        skill_type="grammar",
        activity_id=payload.get("activity_id") or topic["id"],
        activity_type=payload.get("activity_type") or "grammar_topic_attempt",
        score=score,
        max_score=max_score,
        mistakes=mistakes,
        feedback=feedback,
    )
    update_skill_mastery(
        user_id=user_id,
        skill_type="grammar",
        topic=topic["id"],
        is_correct=is_completed,
        score=accuracy,
    )
    return {
        "grammar_attempt": {
            "user_id": user_id,
            "topic_id": topic["id"],
            "score": score,
            "max_score": max_score,
            "accuracy": accuracy,
            "is_completed": is_completed,
        },
        "grammar_journey": get_grammar_journey(user_id),
        "journey_update": journey_update,
    }


def get_grammar_topic_mastery(user_id: str | None = None) -> list[dict[str, Any]]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM skill_mastery
            WHERE user_id = ? AND skill_type = 'grammar'
            """,
            (user_id,),
        ).fetchall()
    mastery_by_topic = {row["topic"]: dict(row) for row in rows}
    items = []
    for topic in get_grammar_topics():
        row = mastery_by_topic.get(topic["id"])
        mastery_score = round(float(row["mastery_score"] or 0), 1) if row else 0
        completed_count = int(row["attempt_count"] or 0) if row else 0
        items.append(
            {
                "topic_id": topic["id"],
                "title": topic["title"],
                "level": topic["level"],
                "mastery_score": mastery_score,
                "completed_count": completed_count,
                "status": _mastery_status(mastery_score),
                "last_score": mastery_score if completed_count else 0,
                "next_action": _topic_next_action(topic),
            }
        )
    return items


def get_weakest_grammar_topic(user_id: str | None = None) -> dict[str, Any]:
    mastery = get_grammar_topic_mastery(user_id)
    attempted = [item for item in mastery if item["completed_count"] > 0]
    if attempted:
        return min(attempted, key=lambda item: (item["mastery_score"], -item["completed_count"]))
    return _topic_mastery_shell(get_grammar_topic("subject_verb"))


def get_strongest_grammar_topic(user_id: str | None = None) -> dict[str, Any]:
    mastery = get_grammar_topic_mastery(user_id)
    attempted = [item for item in mastery if item["completed_count"] > 0]
    if attempted:
        return max(attempted, key=lambda item: (item["mastery_score"], item["completed_count"]))
    return _topic_mastery_shell(get_grammar_topic("subject_verb"))


def get_next_recommended_grammar_topic(user_id: str | None = None) -> dict[str, Any]:
    mastery = get_grammar_topic_mastery(user_id)
    for item in mastery:
        if item["status"] == "need_review":
            return _topic_with_mastery(item)
    for item in mastery:
        if item["status"] == "not_started":
            return _topic_with_mastery(item)
    weakest = get_weakest_grammar_topic(user_id)
    next_topic = get_next_topic(weakest.get("topic_id"))
    return _topic_mastery_shell(next_topic)


def build_grammar_recommendation(user_id: str | None = None) -> dict[str, Any]:
    journey = get_grammar_journey(user_id)
    topic = journey["next_recommended_topic"]
    reason = (
        "Topic ini direkomendasikan karena menjadi fondasi grammar berikutnya."
        if topic.get("status") == "not_started"
        else "Topic ini perlu diulang karena mastery score masih rendah."
    )
    return {
        "recommended_topic": topic,
        "reason": reason,
        "next_action": journey["next_action"],
        "mentor_message": journey["mentor_message"],
    }


def _mastery_status(mastery_score: float) -> str:
    if mastery_score >= 85:
        return "mastered"
    if mastery_score >= 70:
        return "in_progress"
    if mastery_score >= 1:
        return "need_review"
    return "not_started"


def _topic_next_action(topic: dict[str, Any] | None) -> str:
    if not topic:
        return "Mulai dari Subject and Verb. Cari siapa pelaku dan apa aksi utamanya."
    topic_id = topic.get("id") or topic.get("topic_id")
    if topic_id == "subject_verb":
        return "Latihan menemukan subject dan main verb dalam kalimat BA sederhana."
    if topic_id == "object_complement":
        return "Latihan membedakan object dan complement setelah verb."
    if topic_id == "modal_verb":
        return "Latihan memahami must, should, can, may, dan could dalam requirement."
    if topic_id == "gerund_vs_main_verb":
        return "Latihan membedakan kata -ing yang hanya modifier dan verb utama."
    if topic_id == "relative_clause":
        return "Latihan membaca clause yang menjelaskan noun seperti that, who, dan which."
    return f"Lanjutkan latihan {topic.get('title', 'grammar')} dengan contoh TOEFL dan Business Analyst."


def _mentor_message(score: float, attempted_topics: list[dict[str, Any]], weakest: dict[str, Any]) -> str:
    if not attempted_topics:
        return "Mulai dari Subject and Verb. Fokus utama: cari siapa pelaku dan apa aksi utamanya."
    if weakest.get("topic_id") == "subject_verb":
        return "Kamu perlu memperkuat kemampuan menemukan subject dan main verb sebelum masuk ke kalimat yang lebih panjang."
    if score > 70:
        return "Progress Grammar kamu sudah cukup baik. Lanjutkan ke phrase, clause, dan grammar trap."
    return "Ulangi topic yang mastery score-nya masih rendah sebelum masuk ke latihan yang lebih sulit."


def _topic_mastery_shell(topic: dict[str, Any] | None) -> dict[str, Any]:
    if not topic:
        return {}
    return {
        "topic_id": topic["id"],
        "title": topic["title"],
        "level": topic["level"],
        "mastery_score": 0,
        "completed_count": 0,
        "status": "not_started",
        "last_score": 0,
        "next_action": _topic_next_action(topic),
    }


def _topic_with_mastery(item: dict[str, Any]) -> dict[str, Any]:
    topic = get_grammar_topic(item["topic_id"]) or {}
    return {
        **item,
        "purpose": topic.get("purpose", ""),
        "example_sentence": topic.get("example_sentence", ""),
        "beginner_tip": topic.get("beginner_tip", ""),
    }
