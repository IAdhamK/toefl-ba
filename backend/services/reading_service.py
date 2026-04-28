from __future__ import annotations

from typing import Any

from backend.database import get_connection
from backend.services.journey_service import (
    get_default_user_id,
    get_or_create_skill_journey,
    save_learning_attempt,
    update_skill_mastery,
)


READING_SUBSKILLS = (
    "general_meaning",
    "main_idea",
    "detail_information",
    "vocabulary_context",
    "reference",
    "sentence_simplification",
    "inference",
    "author_purpose",
    "paragraph_function",
    "ba_case_analysis",
)

READING_PHASE1_SUBSKILLS = (
    "general_meaning",
    "main_idea",
    "detail_information",
    "vocabulary_context",
)

READING_TRAINER_SUBSKILLS = (
    "main_idea",
    "detail_information",
    "vocabulary_context",
    "inference",
    "sentence_simplification",
)

READING_LEVELS = [
    {"step": 1, "id": "understand_simple_meaning", "title": "Understand Simple Meaning", "min_score": 0},
    {"step": 2, "id": "find_main_idea", "title": "Find Main Idea", "min_score": 20},
    {"step": 3, "id": "find_supporting_details", "title": "Find Supporting Details", "min_score": 35},
    {"step": 4, "id": "vocabulary_in_context", "title": "Vocabulary in Context", "min_score": 50},
    {"step": 5, "id": "reference_and_pronoun", "title": "Reference and Pronoun", "min_score": 60},
    {"step": 6, "id": "complex_sentence_breakdown", "title": "Complex Sentence Breakdown", "min_score": 70},
    {"step": 7, "id": "inference", "title": "Inference", "min_score": 78},
    {"step": 8, "id": "author_purpose_and_logic", "title": "Author Purpose and Logic", "min_score": 84},
    {"step": 9, "id": "ba_case_reading", "title": "BA Case Reading", "min_score": 90},
    {"step": 10, "id": "toefl_reading_simulation", "title": "TOEFL Reading Simulation", "min_score": 95},
]

READING_ACTIONS = {
    "general_meaning": "Hari ini fokus memahami arti umum passage pendek sebelum melihat pilihan jawaban.",
    "main_idea": "Latihan main idea: pilih jawaban yang merangkum seluruh passage, bukan detail kecil.",
    "detail_information": "Latihan detail: cocokkan pertanyaan dengan kalimat bukti di passage.",
    "vocabulary_context": "Ulangi vocabulary in context: pahami arti kata dari kalimatnya, bukan hanya kamus.",
    "reference": "Latihan reference: cari pronoun seperti it, they, this, dan lihat noun sebelumnya.",
    "sentence_simplification": "Pecah satu kalimat panjang menjadi subject, verb utama, dan informasi tambahan.",
    "inference": "Latihan inference: cari makna tersirat dari bukti yang ada di passage.",
    "author_purpose": "Latihan purpose: tanyakan mengapa penulis menyebut informasi tertentu.",
    "paragraph_function": "Latihan fungsi paragraf: cari peran paragraf dalam alur bacaan.",
    "ba_case_analysis": "Latihan BA case reading: hubungkan masalah, stakeholder, requirement, dan business outcome.",
}

READING_TRAINER_CONTENT = {
    "main_idea": {
        "passage": {
            "id": "trainer-main-idea-1",
            "title": "Requirements and Strategy",
            "text": (
                "A business analyst must connect stakeholder needs with business requirements and organizational "
                "strategy. This connection helps teams avoid building features that do not support the desired business outcome."
            ),
        },
        "question": {
            "id": "trainer-main-idea-q1",
            "sub_skill": "main_idea",
            "question_type": "main_idea",
            "text": "What is the main idea of the passage?",
            "options": [
                "Business analysts should write code before asking questions.",
                "Business analysts connect stakeholder needs, requirements, and strategy.",
                "Teams should ignore business outcomes during planning.",
                "Stakeholders only need technical documentation.",
            ],
            "answer": 1,
            "evidence_sentence": "A business analyst must connect stakeholder needs with business requirements and organizational strategy.",
            "explanation": "Opsi B paling merangkum seluruh passage, bukan hanya detail kecil.",
        },
    },
    "detail_information": {
        "passage": {
            "id": "trainer-detail-1",
            "title": "Approval Workflow Delay",
            "text": (
                "Before recommending automation, the analyst interviews the approval team and measures how long each approval step takes. "
                "The longest delay happens when managers wait for missing information from requesters."
            ),
        },
        "question": {
            "id": "trainer-detail-q1",
            "sub_skill": "detail_information",
            "question_type": "detail_information",
            "text": "Where does the longest delay happen?",
            "options": [
                "When managers wait for missing information.",
                "When developers write new code.",
                "When requesters approve their own requests.",
                "When automation is already complete.",
            ],
            "answer": 0,
            "evidence_sentence": "The longest delay happens when managers wait for missing information from requesters.",
            "explanation": "Jawaban ada langsung di kalimat kedua, jadi ini latihan mencari detail.",
        },
    },
    "vocabulary_context": {
        "passage": {
            "id": "trainer-vocab-1",
            "title": "Clarifying Vague Problems",
            "text": (
                "When a stakeholder gives a vague problem statement, the analyst clarifies the expected outcome before proposing a solution. "
                "This prevents the team from solving the wrong problem."
            ),
        },
        "question": {
            "id": "trainer-vocab-q1",
            "sub_skill": "vocabulary_context",
            "question_type": "vocabulary_context",
            "text": "The word 'clarifies' is closest in meaning to:",
            "options": ["makes clearer", "deletes", "delays", "approves"],
            "answer": 0,
            "evidence_sentence": "the analyst clarifies the expected outcome before proposing a solution",
            "explanation": "Dalam konteks ini, clarifies berarti membuat informasi yang samar menjadi lebih jelas.",
        },
    },
    "inference": {
        "passage": {
            "id": "trainer-inference-1",
            "title": "Duplicate Data Entry",
            "text": (
                "Two departments enter the same customer data into different systems. The analyst notices that reports often disagree "
                "because each system is updated at a different time."
            ),
        },
        "question": {
            "id": "trainer-inference-q1",
            "sub_skill": "inference",
            "question_type": "inference",
            "text": "What can be inferred from the passage?",
            "options": [
                "The organization may need a better shared data process.",
                "The departments never use customer data.",
                "Reports are always accurate.",
                "The analyst should stop collecting requirements.",
            ],
            "answer": 0,
            "evidence_sentence": "reports often disagree because each system is updated at a different time",
            "explanation": "Ini inference karena jawabannya tersirat dari masalah duplicate entry dan laporan yang tidak sama.",
        },
    },
    "sentence_simplification": {
        "passage": {
            "id": "trainer-sentence-1",
            "title": "Complex Requirement Sentence",
            "text": (
                "Although stakeholders requested a faster dashboard, the analyst first examined whether the existing data sources "
                "were accurate enough to support reliable decisions."
            ),
        },
        "question": {
            "id": "trainer-sentence-q1",
            "sub_skill": "sentence_simplification",
            "question_type": "sentence_simplification",
            "text": "Which sentence best simplifies the original sentence?",
            "options": [
                "The analyst checked data accuracy before improving the dashboard.",
                "Stakeholders stopped needing a dashboard.",
                "The analyst ignored the data sources.",
                "Reliable decisions were impossible for every user.",
            ],
            "answer": 0,
            "evidence_sentence": "the analyst first examined whether the existing data sources were accurate enough",
            "explanation": "Opsi A mempertahankan makna utama: cek akurasi data dulu sebelum mempercepat dashboard.",
        },
    },
}


def reading_score_to_level(score: float) -> dict[str, Any]:
    current = READING_LEVELS[0]
    for level in READING_LEVELS:
        if float(score or 0) >= level["min_score"]:
            current = level
    return current


def public_mastery(row) -> dict[str, Any]:
    item = dict(row)
    item["mastery_score"] = round(float(item.get("mastery_score") or 0), 1)
    return item


def get_reading_levels() -> dict[str, Any]:
    return {
        "levels": READING_LEVELS,
        "subskills": list(READING_SUBSKILLS),
        "phase_1_subskills": list(READING_PHASE1_SUBSKILLS),
        "trainer_subskills": list(READING_TRAINER_SUBSKILLS),
    }


def get_reading_journey(user_id: str | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    skill = get_or_create_skill_journey(user_id, "reading")
    subskills = get_reading_subskill_mastery(user_id)
    reading_score = round(float(skill.get("average_score") or 0), 1)
    completed_passages = get_completed_passages_count(user_id)
    last_passage_id = get_last_passage_id(user_id)
    weak_subskills = weakest_subskills(subskills)
    strong_subskills = strongest_subskills(subskills)
    level = reading_score_to_level(reading_score)
    next_action = next_reading_action(weak_subskills, reading_score, completed_passages)
    return {
        "user_id": user_id,
        "reading_level": level["title"],
        "reading_level_step": level["step"],
        "reading_score": reading_score,
        "completed_passages": completed_passages,
        "current_stage": skill.get("current_stage") or "Reading Foundation",
        "weak_subskills": weak_subskills,
        "strong_subskills": strong_subskills,
        "sub_skill_mastery": subskills,
        "last_passage_id": last_passage_id,
        "last_activity_at": skill.get("last_activity_at"),
        "next_recommended_action": next_action,
        "skill_journey": skill,
    }


def get_reading_recommendation(user_id: str | None = None) -> dict[str, Any]:
    journey = get_reading_journey(user_id)
    weakest = journey["weak_subskills"][0]["subskill"] if journey["weak_subskills"] else "general_meaning"
    return {
        "user_id": journey["user_id"],
        "target_subskill": weakest,
        "recommended_action": journey["next_recommended_action"],
        "reason": f"Sub-skill {label_subskill(weakest)} masih menjadi fokus Reading berikutnya.",
        "reading_level": journey["reading_level"],
    }


def get_reading_subskills(user_id: str | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    subskills = get_reading_subskill_mastery(user_id)
    weakest = weakest_subskills(subskills)
    next_subskill = next_trainable_subskill(weakest[0]["subskill"] if weakest else "main_idea")
    return {
        "user_id": user_id,
        "subskills": subskills,
        "trainer_subskills": list(READING_TRAINER_SUBSKILLS),
        "next_recommended_subskill": next_subskill,
        "next_recommended_action": READING_ACTIONS.get(next_subskill, READING_ACTIONS["main_idea"]),
    }


def get_reading_trainer(sub_skill: str, user_id: str | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    sub_skill = normalize_subskill(sub_skill)
    if sub_skill not in READING_TRAINER_CONTENT:
        raise ValueError(
            "Trainer tersedia untuk main_idea, detail_information, vocabulary_context, inference, dan sentence_simplification."
        )
    content = READING_TRAINER_CONTENT[sub_skill]
    mastery = next(
        (item for item in get_reading_subskill_mastery(user_id) if item["subskill"] == sub_skill),
        None,
    )
    return {
        "user_id": user_id,
        "sub_skill": sub_skill,
        "label": label_subskill(sub_skill),
        "mastery": mastery,
        "next_action": READING_ACTIONS.get(sub_skill, READING_ACTIONS["main_idea"]),
        "passage": content["passage"],
        "question": content["question"],
        "guidance": trainer_guidance(sub_skill),
    }


def save_reading_attempt(payload: dict[str, Any]) -> dict[str, Any]:
    user_id = get_default_user_id(payload.get("user_id") or payload.get("userId"))
    passage_id = payload.get("passage_id") or payload.get("lesson_id") or payload.get("activity_id") or "reading-passage"
    sub_skill = normalize_subskill(payload.get("sub_skill") or payload.get("subskill") or payload.get("question_type") or "")
    trainer_feedback = build_trainer_answer_feedback(payload, sub_skill)
    if trainer_feedback:
        score = float(trainer_feedback["score"])
        max_score = float(trainer_feedback["max_score"])
    else:
        score = float(payload.get("score", 0) or 0)
        max_score = float(payload.get("max_score", 100) or 100)
    subskill_scores = normalize_subskill_scores(payload.get("subskill_scores") or payload.get("subskills") or {})
    mistakes = payload.get("mistakes", [])
    feedback = payload.get("feedback") or (trainer_feedback or {}).get("message") or "Reading attempt tersimpan. Lanjutkan latihan sesuai rekomendasi."
    if sub_skill and sub_skill not in READING_SUBSKILLS:
        raise ValueError(f"Sub-skill Reading tidak dikenal: {sub_skill}")
    update = save_learning_attempt(
        user_id=user_id,
        skill_type="reading",
        activity_id=passage_id,
        activity_type=payload.get("activity_type", "reading_journey_attempt"),
        score=score,
        max_score=max_score,
        mistakes=mistakes,
        feedback=feedback,
    )
    percent = round((score / max(max_score, 1)) * 100, 1)
    if not subskill_scores:
        subskill_scores = {sub_skill: percent} if sub_skill else infer_phase1_subskill_scores(percent)
    for subskill, subskill_score in subskill_scores.items():
        if subskill in READING_SUBSKILLS:
            update_skill_mastery(
                user_id=user_id,
                skill_type="reading",
                topic=subskill,
                is_correct=float(subskill_score or 0) >= 70,
                score=float(subskill_score or 0),
            )
    next_subskill = get_reading_recommendation(user_id)["target_subskill"]
    return {
        "attempt": update,
        "reading_journey": get_reading_journey(user_id),
        "recommendation": get_reading_recommendation(user_id),
        "answer_feedback": trainer_feedback,
        "next_recommended_subskill": next_trainable_subskill(next_subskill),
    }


def update_reading_subskills_from_quiz(user_id: str, lesson: dict[str, Any], result: dict[str, Any]) -> None:
    questions = lesson.get("questions", [])
    details = {item.get("questionId"): item for item in result.get("details", [])}
    for question in questions:
        subskill = infer_question_subskill(question)
        detail = details.get(question.get("id"), {})
        is_correct = bool(detail.get("isCorrect"))
        update_skill_mastery(
            user_id=user_id,
            skill_type="reading",
            topic=subskill,
            is_correct=is_correct,
            score=100 if is_correct else 35,
        )


def infer_question_subskill(question: dict[str, Any]) -> str:
    explicit = normalize_subskill(question.get("sub_skill") or question.get("subskill") or question.get("question_type") or "")
    if explicit in READING_SUBSKILLS:
        return explicit
    text = (question.get("text") or "").lower()
    if "main idea" in text or "best title" in text or "mostly about" in text:
        return "main_idea"
    if "closest in meaning" in text or "word" in text or "means" in text:
        return "vocabulary_context"
    if "refer to" in text or "pronoun" in text or "the word it" in text or "the word they" in text:
        return "reference"
    if "simplifies" in text or "simplify" in text or "best expresses" in text:
        return "sentence_simplification"
    if "infer" in text or "inferred" in text or "imply" in text or "suggest" in text:
        return "inference"
    if "purpose" in text or "why does the author" in text:
        return "author_purpose"
    if "function" in text or "role of the paragraph" in text:
        return "paragraph_function"
    if any(keyword in text for keyword in ["stakeholder", "requirement", "business analyst", "ba case"]):
        return "ba_case_analysis"
    if any(keyword in text for keyword in ["why", "what should", "what can", "before", "after"]):
        return "detail_information"
    return "general_meaning"


def get_reading_subskill_mastery(user_id: str) -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM skill_mastery
            WHERE user_id = ? AND skill_type = 'reading'
            """,
            (user_id,),
        ).fetchall()
    by_topic = {row["topic"]: public_mastery(row) for row in rows}
    items = []
    for subskill in READING_SUBSKILLS:
        row = by_topic.get(subskill)
        items.append(
            {
                "subskill": subskill,
                "label": label_subskill(subskill),
                "mastery_score": row["mastery_score"] if row else 0,
                "attempt_count": int(row["attempt_count"] or 0) if row else 0,
                "correct_count": int(row["correct_count"] or 0) if row else 0,
                "wrong_count": int(row["wrong_count"] or 0) if row else 0,
                "last_practiced_at": row.get("last_practiced_at") if row else None,
                "trainer_available": subskill in READING_TRAINER_SUBSKILLS,
                "status": mastery_status(row["mastery_score"] if row else 0, int(row["attempt_count"] or 0) if row else 0),
            }
        )
    return items


def normalize_subskill(value: Any) -> str:
    aliases = {
        "detail": "detail_information",
        "vocabulary": "vocabulary_context",
        "sentence_breakdown": "sentence_simplification",
        "sentence": "sentence_simplification",
        "purpose": "author_purpose",
        "paragraph": "paragraph_function",
        "ba_case": "ba_case_analysis",
    }
    key = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    return aliases.get(key, key)


def next_trainable_subskill(subskill: str) -> str:
    subskill = normalize_subskill(subskill)
    if subskill in READING_TRAINER_SUBSKILLS:
        return subskill
    if subskill in ("general_meaning", "author_purpose", "paragraph_function", "ba_case_analysis", "reference"):
        return "main_idea" if subskill == "general_meaning" else "detail_information"
    return "main_idea"


def trainer_guidance(sub_skill: str) -> dict[str, str]:
    guidance = {
        "main_idea": {
            "goal": "Latih kemampuan menangkap ide utama passage.",
            "tip": "Pilih opsi yang merangkum seluruh bacaan, bukan detail kecil.",
        },
        "detail_information": {
            "goal": "Latih mencari informasi spesifik di passage.",
            "tip": "Cari kata kunci pertanyaan, lalu cocokkan dengan evidence sentence.",
        },
        "vocabulary_context": {
            "goal": "Latih menebak arti kata dari konteks kalimat.",
            "tip": "Jangan hanya menghafal kamus; lihat fungsi kata di kalimat.",
        },
        "inference": {
            "goal": "Latih memahami makna tersirat.",
            "tip": "Jawaban inference harus didukung bukti, walau tidak tertulis langsung.",
        },
        "sentence_simplification": {
            "goal": "Latih menyederhanakan kalimat panjang.",
            "tip": "Pertahankan makna utama: siapa melakukan apa dan informasi pentingnya.",
        },
    }
    return guidance.get(sub_skill, guidance["main_idea"])


def build_trainer_answer_feedback(payload: dict[str, Any], sub_skill: str) -> dict[str, Any] | None:
    if not sub_skill or sub_skill not in READING_TRAINER_CONTENT:
        return None
    question = READING_TRAINER_CONTENT[sub_skill]["question"]
    selected = payload.get("selected")
    if selected is None:
        selected = payload.get("selected_answer")
    if selected is None:
        selected = payload.get("answer")
    if selected is None:
        return None
    answer = int(payload.get("correct_answer", question["answer"]))
    selected_index = parse_selected_index(selected, question["options"])
    is_correct = selected_index == answer
    selected_text = question["options"][selected_index] if selected_index is not None and 0 <= selected_index < len(question["options"]) else str(selected)
    correct_text = question["options"][answer]
    return {
        "is_correct": is_correct,
        "score": 100 if is_correct else 0,
        "max_score": 100,
        "selected_index": selected_index,
        "selected_text": selected_text,
        "correct_index": answer,
        "correct_answer": correct_text,
        "evidence_sentence": question.get("evidence_sentence"),
        "explanation": question.get("explanation"),
        "message": (
            f"Benar. {question.get('explanation')}"
            if is_correct
            else f"Belum tepat. Jawaban yang lebih kuat: {correct_text}. {question.get('explanation')}"
        ),
    }


def parse_selected_index(selected: Any, options: list[str]) -> int | None:
    if isinstance(selected, int):
        return selected
    text = str(selected or "").strip()
    if text.isdigit():
        return int(text)
    letters = {"a": 0, "b": 1, "c": 2, "d": 3}
    if text.lower() in letters:
        return letters[text.lower()]
    lowered = text.lower()
    for index, option in enumerate(options):
        if option.lower() == lowered:
            return index
    return None


def get_completed_passages_count(user_id: str) -> int:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT COUNT(DISTINCT activity_id) AS total
            FROM learning_attempts
            WHERE user_id = ? AND skill_type = 'reading'
            """,
            (user_id,),
        ).fetchone()
    return int(row["total"] or 0) if row else 0


def get_last_passage_id(user_id: str) -> str | None:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT activity_id
            FROM learning_attempts
            WHERE user_id = ? AND skill_type = 'reading'
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (user_id,),
        ).fetchone()
    return row["activity_id"] if row else None


def normalize_subskill_scores(raw: Any) -> dict[str, float]:
    if isinstance(raw, dict):
        return {str(key): float(value or 0) for key, value in raw.items()}
    if isinstance(raw, list):
        result = {}
        for item in raw:
            if isinstance(item, dict):
                key = item.get("subskill") or item.get("topic")
                if key:
                    result[str(key)] = float(item.get("score", item.get("mastery_score", 0)) or 0)
        return result
    return {}


def infer_phase1_subskill_scores(score: float) -> dict[str, float]:
    return {
        "general_meaning": score,
        "main_idea": score,
        "detail_information": max(0, score - 5 if score < 80 else score),
        "vocabulary_context": max(0, score - 10 if score < 70 else score),
    }


def weakest_subskills(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(items, key=lambda item: (item["mastery_score"], item["attempt_count"]))[:2]


def strongest_subskills(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    attempted = [item for item in items if item["attempt_count"] > 0]
    return sorted(attempted or items, key=lambda item: item["mastery_score"], reverse=True)[:2]


def next_reading_action(weak_subskills: list[dict[str, Any]], score: float, completed_passages: int) -> str:
    if completed_passages == 0:
        return "Mulai dari satu passage pendek. Baca judul, kalimat pertama, lalu cari arti umum bacaan."
    target = weak_subskills[0]["subskill"] if weak_subskills else "main_idea"
    if score < 40:
        return READING_ACTIONS["general_meaning"]
    return READING_ACTIONS.get(target, READING_ACTIONS["main_idea"])


def mastery_status(score: float, attempt_count: int) -> str:
    if attempt_count == 0:
        return "not_started"
    if score >= 80:
        return "strong"
    if score >= 60:
        return "developing"
    return "needs_review"


def label_subskill(subskill: str) -> str:
    labels = {
        "general_meaning": "Arti umum",
        "main_idea": "Main idea",
        "detail_information": "Detail informasi",
        "vocabulary_context": "Vocabulary in context",
        "reference": "Reference/pronoun",
        "sentence_simplification": "Kalimat kompleks",
        "inference": "Inference",
        "author_purpose": "Author purpose",
        "paragraph_function": "Fungsi paragraf",
        "ba_case_analysis": "BA case reading",
    }
    return labels.get(subskill, subskill.replace("_", " ").title())
