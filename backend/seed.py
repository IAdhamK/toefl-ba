from __future__ import annotations

from backend.database import get_connection, init_db, load_json_data, now_iso, table_count
from backend.repository import upsert_lesson, upsert_vocabulary
from backend.services.journey_service import backfill_user_journeys


DEFAULT_LESSONS = [
    {
        "id": "reading-1",
        "title": "Stakeholder Needs and Strategy Alignment",
        "level": "Foundation",
        "context": "Requirement elicitation",
        "passage": "A business analyst operating within a complex enterprise environment must not only elicit requirements but also ensure alignment between stakeholder needs and organizational strategy. When a stakeholder describes a problem vaguely, the analyst should clarify the expected outcome before proposing a solution.",
        "vocabulary": ["elicit", "alignment", "stakeholder", "vaguely", "outcome"],
        "grammar": "Reduced relative clause: operating within a complex enterprise environment.",
        "questions": [
            {
                "id": "r1q1",
                "text": "What is the main idea of the passage?",
                "options": [
                    "Business analysts should write code immediately.",
                    "Business analysts must connect requirements with stakeholder needs and strategy.",
                    "Stakeholders should avoid discussing vague problems.",
                    "Organizational strategy is unrelated to requirements.",
                ],
                "answer": 1,
                "explanation": "The passage emphasizes eliciting requirements and aligning them with needs and strategy.",
            }
        ],
    }
]


DEFAULT_VOCABULARY = [
    {
        "id": "v1",
        "word": "elicit",
        "part": "verb",
        "meaningId": "menggali atau memperoleh informasi",
        "meaningEn": "to draw out information",
        "example": "The analyst must elicit clear requirements from stakeholders.",
        "answer": "menggali",
    },
    {
        "id": "v2",
        "word": "validate",
        "part": "verb",
        "meaningId": "memastikan sesuatu benar atau sesuai kebutuhan",
        "meaningEn": "to confirm correctness or suitability",
        "example": "The team validates the requirement before development starts.",
        "answer": "memastikan",
    },
]


def seed_database() -> None:
    init_db()
    data = load_json_data()
    lessons = data.get("lessons") or DEFAULT_LESSONS
    vocabulary = data.get("vocabulary") or DEFAULT_VOCABULARY

    if table_count("lessons") == 0:
        for lesson in lessons:
            upsert_lesson(lesson)

    if table_count("vocabulary") == 0:
        for item in vocabulary:
            upsert_vocabulary(item)

    if table_count("prompts") == 0:
        seed_prompts()

    backfill_user_journeys()


def seed_prompts() -> None:
    prompts = {
        "toefl_reading_explanation": "Explain TOEFL reading in Indonesian for a beginner Business Analyst learner.",
        "grammar_breakdown": "Find subject, main verb, phrase, and explain the meaning simply.",
        "subject_verb_detection": "Show the subject and verb, then explain why other phrases are modifiers.",
        "vocabulary_explanation": "Explain word meaning, Indonesian translation, and one BA example.",
        "writing_feedback": "Give grammar, clarity, measurable requirement, and revised writing feedback.",
        "next_lesson_recommendation": "Recommend one small next step based on weakest skill.",
    }
    now = now_iso()
    with get_connection() as conn:
        for prompt_id, content in prompts.items():
            conn.execute(
                """
                INSERT INTO prompts (id, name, category, content, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (prompt_id, prompt_id.replace("_", " ").title(), "ai", content, now, now),
            )


if __name__ == "__main__":
    seed_database()
    print("Database siap: data/toefl_ba.sqlite3")
