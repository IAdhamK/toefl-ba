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

READING_VOCABULARY_MEANINGS = {
    "analyst": "orang yang menganalisis kebutuhan atau masalah",
    "business": "bisnis",
    "stakeholder": "pihak yang berkepentingan",
    "stakeholders": "pihak-pihak yang berkepentingan",
    "requirement": "kebutuhan sistem atau bisnis",
    "requirements": "kebutuhan sistem atau bisnis",
    "elicit": "menggali informasi",
    "elicits": "menggali informasi",
    "alignment": "keselarasan",
    "strategy": "strategi atau arah organisasi",
    "organizational": "berhubungan dengan organisasi",
    "vague": "samar atau belum jelas",
    "vaguely": "dengan cara yang samar",
    "clarify": "membuat lebih jelas",
    "clarifies": "membuat lebih jelas",
    "outcome": "hasil yang diharapkan",
    "process": "alur kerja",
    "automation": "otomatisasi",
    "evaluate": "menilai atau memeriksa",
    "delays": "keterlambatan",
    "duplicate": "ganda atau berulang",
    "responsibilities": "tanggung jawab",
    "redesigned": "dirancang ulang",
    "workflow": "alur kerja",
    "approval": "persetujuan",
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


def generate_guided_reading_steps(payload: dict[str, Any]) -> dict[str, Any]:
    title = str(payload.get("title") or payload.get("passage_title") or "Reading Passage").strip()
    passage = str(payload.get("passage") or payload.get("passage_text") or "").strip()
    if not passage:
        raise ValueError("Passage wajib diisi untuk Guided Reading.")
    lesson_id = payload.get("lesson_id") or payload.get("activity_id") or "guided-reading"
    first_sentence = split_sentences(passage)[0] if split_sentences(passage) else passage
    subject, verb = identify_subject_and_verb(first_sentence)
    vocabulary = extract_key_vocabulary(passage, payload.get("vocabulary") or [])
    passage_map = generate_passage_map({"title": title, "passage": passage, "vocabulary": payload.get("vocabulary") or []})
    main_idea = infer_main_idea(title, passage)
    steps = [
        {
            "step": 1,
            "id": "title",
            "title": "Pahami judul",
            "focus_text": title,
            "simple_explanation": f"Judul ini memberi sinyal bahwa bacaan membahas {title.lower()}.",
            "learner_action": "Sebelum membaca detail, tebak dulu topik besarnya dari judul.",
            "bantuan_context_type": "reading_passage",
        },
        {
            "step": 2,
            "id": "first_sentence",
            "title": "Baca kalimat pertama",
            "focus_text": first_sentence,
            "simple_explanation": simple_sentence_meaning(first_sentence),
            "learner_action": "Cari siapa pelakunya dan aksi utama yang dilakukan.",
            "bantuan_context_type": "reading_paragraph",
        },
        {
            "step": 3,
            "id": "subject_verb",
            "title": "Temukan subject dan main verb",
            "focus_text": first_sentence,
            "subject": subject,
            "main_verb": verb,
            "simple_explanation": f"Subject utamanya adalah '{subject}'. Aksi utamanya adalah '{verb}'.",
            "learner_action": "Jangan fokus dulu pada semua kata. Pegang subject dan verb utama dulu.",
            "bantuan_context_type": "grammar_sentence",
        },
        {
            "step": 4,
            "id": "vocabulary",
            "title": "Kenali vocabulary penting",
            "focus_text": ", ".join(item["word"] for item in vocabulary[:6]),
            "key_vocabulary": vocabulary[:8],
            "simple_explanation": "Kata-kata ini sering menentukan makna passage dan jawaban TOEFL.",
            "learner_action": "Pahami arti kata dari konteks kalimat, bukan hanya dari hafalan kamus.",
            "bantuan_context_type": "vocabulary_example",
        },
        {
            "step": 5,
            "id": "paragraph_map",
            "title": "Pahami tiap paragraf",
            "paragraph_map": passage_map["paragraphs"],
            "simple_explanation": "Setiap paragraf punya satu pesan utama. Baca per bagian, bukan sekaligus.",
            "learner_action": "Catat main point tiap paragraf sebelum melihat pertanyaan.",
            "bantuan_context_type": "reading_paragraph",
        },
        {
            "step": 6,
            "id": "main_idea",
            "title": "Temukan main idea",
            "focus_text": passage,
            "main_idea": main_idea,
            "simple_explanation": main_idea,
            "learner_action": "Pilih jawaban yang merangkum seluruh passage, bukan detail kecil.",
            "bantuan_context_type": "reading_question",
        },
        {
            "step": 7,
            "id": "answer_question",
            "title": "Siap jawab pertanyaan",
            "focus_text": payload.get("question_text") or "TOEFL-style question",
            "simple_explanation": "Sekarang kamu sudah punya bekal: topik, subject/verb, vocabulary, paragraf, dan main idea.",
            "learner_action": "Jawab pertanyaan dengan mencocokkan opsi dengan main idea dan evidence passage.",
            "bantuan_context_type": "reading_question",
        },
    ]
    return {
        "lesson_id": lesson_id,
        "title": title,
        "passage": passage,
        "steps": steps,
        "total_steps": len(steps),
        "support_activity": {
            "skill_type": "reading",
            "activity_type": "guided_reading",
            "feedback": "User menyelesaikan Guided Reading sebagai aktivitas pendukung. Aktivitas ini tidak menurunkan skor.",
        },
    }


def generate_passage_map(payload: dict[str, Any]) -> dict[str, Any]:
    title = str(payload.get("title") or payload.get("passage_title") or "Reading Passage").strip()
    passage = str(payload.get("passage") or payload.get("passage_text") or "").strip()
    if not passage:
        raise ValueError("Passage wajib diisi untuk passage map.")
    paragraphs = split_paragraphs(passage)
    mapped = []
    for index, paragraph in enumerate(paragraphs, start=1):
        vocab = extract_key_vocabulary(paragraph, payload.get("vocabulary") or [])
        mapped.append(
            {
                "paragraph_number": index,
                "text": paragraph,
                "simple_meaning": simple_paragraph_meaning(paragraph),
                "key_vocabulary": vocab[:6],
                "main_point": infer_paragraph_main_point(paragraph),
                "possible_reading_skill": infer_paragraph_skill(paragraph),
                "beginner_tip": paragraph_beginner_tip(paragraph),
            }
        )
    return {
        "title": title,
        "paragraphs": mapped,
        "main_idea": infer_main_idea(title, passage),
    }


def generate_answer_review(payload: dict[str, Any]) -> dict[str, Any]:
    passage = str(payload.get("passage") or payload.get("passage_text") or "").strip()
    question = normalize_review_question(payload)
    options = [str(option) for option in question.get("options", [])]
    if not options:
        raise ValueError("Options wajib diisi untuk Answer Review.")
    selected_index = parse_selected_index(
        payload.get("selected") if payload.get("selected") is not None else payload.get("selected_answer"),
        options,
    )
    correct_index = parse_correct_index(payload.get("correct_answer", question.get("answer")), options)
    if selected_index is None:
        raise ValueError("Selected answer tidak valid.")
    if correct_index is None:
        raise ValueError("Correct answer tidak valid.")
    selected_text = options[selected_index]
    correct_text = options[correct_index]
    is_correct = selected_index == correct_index
    sub_skill = normalize_subskill(payload.get("sub_skill") or payload.get("question_type") or infer_question_subskill(question))
    evidence_sentence = (
        payload.get("evidence_sentence")
        or question.get("evidence_sentence")
        or find_evidence_sentence(passage, question.get("text", ""), correct_text)
    )
    explanation = payload.get("explanation") or question.get("explanation") or answer_review_explanation(question, correct_text, evidence_sentence)
    distractors = build_distractor_analysis(options, correct_index, selected_index, passage, question.get("text", ""), evidence_sentence)
    selected_letter = option_letter(selected_index)
    correct_letter = option_letter(correct_index)
    why_wrong = ""
    if not is_correct:
        selected_analysis = distractors[selected_letter]
        why_wrong = f"Opsi {selected_letter} kurang tepat karena {selected_analysis['reason']}"
    return {
        "question_id": question.get("id") or payload.get("question_id") or payload.get("activity_id") or "reading-question",
        "question_text": question.get("text", ""),
        "selected_answer": {
            "label": selected_letter,
            "index": selected_index,
            "text": selected_text,
        },
        "correct_answer": {
            "label": correct_letter,
            "index": correct_index,
            "text": correct_text,
        },
        "is_correct": is_correct,
        "direct_explanation": (
            f"Jawaban Anda benar. Opsi {correct_letter} paling sesuai dengan bukti passage."
            if is_correct
            else f"Jawaban Anda belum tepat. Anda memilih opsi {selected_letter}, sedangkan jawaban yang lebih kuat adalah opsi {correct_letter}."
        ),
        "evidence_sentence": evidence_sentence,
        "why_correct_answer_is_correct": f"Opsi {correct_letter} benar karena {explanation}",
        "why_selected_answer_is_wrong": why_wrong,
        "distractor_analysis": distractors,
        "related_reading_sub_skill": sub_skill,
        "next_practice_recommendation": answer_review_next_practice(sub_skill, is_correct),
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
    answer_review = None
    if has_review_payload(payload):
        answer_review = generate_answer_review(payload)
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
        "answer_review": answer_review,
        "evidence_sentence": (answer_review or {}).get("evidence_sentence") or (trainer_feedback or {}).get("evidence_sentence"),
        "distractor_analysis": (answer_review or {}).get("distractor_analysis", {}),
        "next_recommendation": (answer_review or {}).get("next_practice_recommendation") or READING_ACTIONS.get(next_trainable_subskill(next_subskill)),
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


def parse_correct_index(correct: Any, options: list[str]) -> int | None:
    parsed = parse_selected_index(correct, options)
    if parsed is not None:
        return parsed
    if correct is None:
        return None
    lowered = str(correct).strip().lower()
    for index, option in enumerate(options):
        if option.lower() == lowered:
            return index
    return None


def has_review_payload(payload: dict[str, Any]) -> bool:
    has_selected = any(key in payload for key in ("selected", "selected_answer", "answer"))
    has_question = bool(payload.get("question") or payload.get("question_text") or payload.get("sub_skill"))
    return has_selected and has_question


def normalize_review_question(payload: dict[str, Any]) -> dict[str, Any]:
    question = dict(payload.get("question") or {})
    sub_skill = normalize_subskill(payload.get("sub_skill") or question.get("sub_skill") or question.get("question_type") or "")
    if sub_skill in READING_TRAINER_CONTENT and not question.get("options"):
        question = dict(READING_TRAINER_CONTENT[sub_skill]["question"])
    question["id"] = question.get("id") or payload.get("question_id") or payload.get("activity_id") or "reading-question"
    question["text"] = question.get("text") or payload.get("question_text") or ""
    question["options"] = question.get("options") or payload.get("options") or []
    question["answer"] = question.get("answer", payload.get("correct_answer"))
    question["explanation"] = question.get("explanation") or payload.get("explanation") or ""
    question["evidence_sentence"] = question.get("evidence_sentence") or payload.get("evidence_sentence") or ""
    question["sub_skill"] = sub_skill or infer_question_subskill(question)
    return question


def option_letter(index: int) -> str:
    return chr(65 + int(index))


def build_distractor_analysis(
    options: list[str],
    correct_index: int,
    selected_index: int,
    passage: str,
    question_text: str,
    evidence_sentence: str,
) -> dict[str, dict[str, str]]:
    analysis = {}
    for index, option in enumerate(options):
        letter = option_letter(index)
        is_correct = index == correct_index
        relation, reason = option_relation_and_reason(option, is_correct, passage, question_text, evidence_sentence)
        if not is_correct and index == selected_index:
            reason = f"Ini pilihan Anda, tetapi {reason}"
        analysis[letter] = {
            "meaning": translate_reading_option(option),
            "relation_to_passage": relation,
            "correct_or_wrong": "correct" if is_correct else "wrong",
            "reason": reason,
        }
    return analysis


def option_relation_and_reason(option: str, is_correct: bool, passage: str, question_text: str, evidence_sentence: str) -> tuple[str, str]:
    lowered = option.lower()
    if is_correct:
        return (
            "Sesuai dengan passage dan bukti yang ditemukan.",
            f"opsi ini paling cocok dengan evidence: {evidence_sentence or 'bagian utama passage'}."
        )
    if "write code" in lowered:
        return (
            "Tidak didukung oleh passage.",
            "passage membahas analisis requirement dan alignment, bukan langsung menulis kode."
        )
    if "avoid discussing vague problems" in lowered:
        return (
            "Kurang sesuai dengan passage.",
            "passage mengatakan analyst perlu mengklarifikasi masalah yang samar, bukan stakeholder harus menghindarinya."
        )
    if "unrelated" in lowered:
        return (
            "Bertentangan dengan passage.",
            "passage justru menyatakan requirement perlu selaras dengan strategy."
        )
    if "replace all employees" in lowered or "avoid speaking" in lowered or "ignore" in lowered:
        return (
            "Tidak didukung oleh passage.",
            "opsi ini terlalu ekstrem dan tidak muncul sebagai tujuan analyst."
        )
    if "technical documentation" in lowered:
        return (
            "Terlalu sempit.",
            "passage membahas kebutuhan, requirement, dan strategi, bukan hanya dokumentasi teknis."
        )
    overlap = vocabulary_overlap(option, passage)
    if overlap:
        return (
            "Memiliki beberapa kata yang terkait, tetapi bukan jawaban terbaik.",
            "ada kata yang mirip dengan passage, namun maknanya tidak paling menjawab pertanyaan."
        )
    return (
        "Tidak menjadi fokus passage.",
        "opsi ini tidak punya bukti kuat di passage."
    )


def translate_reading_option(option: str) -> str:
    lowered = option.lower().strip()
    known = {
        "business analysts should write code immediately.": "Business Analyst sebaiknya langsung menulis kode.",
        "business analysts should write code before asking questions.": "Business Analyst sebaiknya menulis kode sebelum bertanya.",
        "business analysts must connect requirements with stakeholder needs and strategy.": "Business Analyst harus menghubungkan requirement dengan kebutuhan stakeholder dan strategi.",
        "business analysts connect stakeholder needs, requirements, and strategy.": "Business Analyst menghubungkan kebutuhan stakeholder, requirement, dan strategi.",
        "stakeholders should avoid discussing vague problems.": "Stakeholder sebaiknya menghindari membahas masalah yang masih samar.",
        "organizational strategy is unrelated to requirements.": "Strategi organisasi tidak berhubungan dengan requirement.",
        "make clearer": "membuat lebih jelas",
        "remove": "menghapus",
        "delay": "menunda",
        "approve": "menyetujui",
        "clarify the expected outcome.": "memperjelas hasil yang diharapkan.",
        "ask the developer to build it.": "meminta developer langsung membuatnya.",
        "ignore the stakeholder.": "mengabaikan stakeholder.",
        "create a final contract.": "membuat kontrak final.",
        "when managers wait for missing information.": "ketika manager menunggu informasi yang masih kurang.",
        "the analyst checked data accuracy before improving the dashboard.": "Analyst memeriksa akurasi data sebelum memperbaiki dashboard.",
    }
    if lowered in known:
        return known[lowered]
    return f"Arti opsi: {option}"


def vocabulary_overlap(option: str, passage: str) -> bool:
    option_words = {word.strip(".,:;!?").lower() for word in option.split() if len(word.strip(".,:;!?")) > 4}
    passage_words = {word.strip(".,:;!?").lower() for word in passage.split() if len(word.strip(".,:;!?")) > 4}
    return bool(option_words & passage_words)


def find_evidence_sentence(passage: str, question_text: str, correct_answer: str) -> str:
    sentences = split_sentences(passage)
    if not sentences:
        return passage
    lower_correct = correct_answer.lower()
    if "requirements" in lower_correct and "stakeholder" in lower_correct and "strategy" in lower_correct:
        for sentence in sentences:
            lower = sentence.lower()
            if "requirements" in lower and "stakeholder" in lower and "strategy" in lower:
                return sentence
    if "clarify" in lower_correct or "clearer" in lower_correct or "outcome" in lower_correct:
        for sentence in sentences:
            if "clarify" in sentence.lower() or "outcome" in sentence.lower():
                return sentence
    target_words = {word.strip(".,:;!?").lower() for word in f"{question_text} {correct_answer}".split() if len(word.strip(".,:;!?")) > 4}
    ranked = sorted(
        sentences,
        key=lambda sentence: len(target_words & {word.strip(".,:;!?").lower() for word in sentence.split()}),
        reverse=True,
    )
    return ranked[0]


def answer_review_explanation(question: dict[str, Any], correct_text: str, evidence_sentence: str) -> str:
    if question.get("explanation"):
        return question["explanation"]
    text = (question.get("text") or "").lower()
    if "main idea" in text:
        return "jawaban benar merangkum isi passage secara umum, bukan hanya mengambil satu detail kecil."
    if "closest in meaning" in text:
        return "jawaban benar cocok dengan arti kata dalam konteks kalimat."
    return f"jawaban benar didukung oleh evidence sentence: {evidence_sentence or correct_text}."


def answer_review_next_practice(sub_skill: str, is_correct: bool) -> str:
    action = READING_ACTIONS.get(sub_skill, READING_ACTIONS["main_idea"])
    if is_correct:
        return f"Lanjutkan latihan {label_subskill(sub_skill)} dengan passage baru. {action}"
    return f"Ulangi sub-skill {label_subskill(sub_skill)}. {action}"


def split_paragraphs(passage: str) -> list[str]:
    chunks = [item.strip() for item in str(passage or "").split("\n") if item.strip()]
    return chunks or [str(passage or "").strip()]


def split_sentences(text: str) -> list[str]:
    normalized = str(text or "").replace("?", ".").replace("!", ".")
    sentences = [part.strip() for part in normalized.split(".") if part.strip()]
    return sentences


def identify_subject_and_verb(sentence: str) -> tuple[str, str]:
    words = str(sentence or "").split()
    lowered = [word.strip(",.").lower() for word in words]
    verb_candidates = [
        "must",
        "should",
        "can",
        "helps",
        "help",
        "evaluates",
        "evaluate",
        "connects",
        "connect",
        "elicits",
        "elicit",
        "clarifies",
        "clarify",
        "identifies",
        "identify",
        "determine",
        "determines",
        "describes",
        "proposing",
        "recommending",
    ]
    verb_index = next((index for index, word in enumerate(lowered) if word in verb_candidates), 1 if len(words) > 1 else 0)
    subject = " ".join(words[:verb_index]).strip(", ") or words[0] if words else "-"
    verb = words[verb_index].strip(",.") if words and verb_index < len(words) else "-"
    if verb.lower() == "must" and verb_index + 1 < len(words):
        verb = f"must {words[verb_index + 1].strip(',.')}"
    if subject.lower().startswith("when "):
        subject = "the analyst" if "analyst" in lowered else subject
    return subject, verb


def extract_key_vocabulary(text: str, provided: list[Any] | tuple[Any, ...]) -> list[dict[str, str]]:
    words = {str(word).strip(" ,.;:'\"()").lower() for word in str(text or "").split()}
    for word in provided or []:
        if word:
            words.add(str(word).strip().lower())
    items = []
    for word in sorted(words):
        if word in READING_VOCABULARY_MEANINGS:
            items.append(
                {
                    "word": word,
                    "meaning_id": READING_VOCABULARY_MEANINGS[word],
                    "context_tip": vocabulary_context_tip(word),
                }
            )
    return items


def vocabulary_context_tip(word: str) -> str:
    if word in {"requirement", "requirements"}:
        return "Dalam konteks BA, ini biasanya berarti kebutuhan bisnis atau sistem yang harus dipahami."
    if word in {"stakeholder", "stakeholders"}:
        return "Dalam konteks BA, ini adalah orang atau pihak yang punya kebutuhan, masalah, atau pengaruh."
    if word in {"elicit", "elicits"}:
        return "Dalam konteks BA, ini berarti menggali kebutuhan lewat pertanyaan, interview, atau workshop."
    if word in {"alignment"}:
        return "Kata ini sering berarti mencocokkan requirement dengan tujuan bisnis."
    return "Lihat kalimat sekitar kata ini untuk memahami arti yang paling tepat."


def simple_sentence_meaning(sentence: str) -> str:
    text = str(sentence or "")
    if "business analyst" in text.lower() and "requirements" in text.lower():
        return "Kalimat ini menjelaskan peran Business Analyst dalam memahami dan menghubungkan kebutuhan bisnis."
    if "process" in text.lower() and ("delay" in text.lower() or "delays" in text.lower()):
        return "Kalimat ini membahas pemeriksaan proses untuk menemukan penyebab keterlambatan."
    return f"Kalimat ini berarti: {text}"


def simple_paragraph_meaning(paragraph: str) -> str:
    lower = paragraph.lower()
    if "stakeholder" in lower and "strategy" in lower:
        return "Paragraf ini menjelaskan bahwa kebutuhan stakeholder harus dihubungkan dengan strategi organisasi."
    if "vague" in lower or "clarify" in lower:
        return "Paragraf ini menekankan pentingnya memperjelas masalah sebelum memberi solusi."
    if "automation" in lower or "process" in lower:
        return "Paragraf ini menjelaskan bahwa proses harus dievaluasi sebelum menentukan solusi teknologi."
    return f"Paragraf ini membahas: {paragraph[:140]}"


def infer_paragraph_main_point(paragraph: str) -> str:
    lower = paragraph.lower()
    if "not only elicit requirements" in lower or "alignment" in lower:
        return "Business Analyst perlu menggali requirement dan memastikan selaras dengan kebutuhan serta strategi."
    if "clarify" in lower or "vague" in lower:
        return "Masalah yang masih samar perlu diklarifikasi sebelum solusi dibuat."
    if "automation" in lower or "current process" in lower:
        return "Analyst mengevaluasi proses saat ini untuk mengetahui apakah automation benar-benar solusi yang tepat."
    return "Cari kalimat yang paling umum dan mencakup isi paragraf ini."


def infer_paragraph_skill(paragraph: str) -> str:
    lower = paragraph.lower()
    if "main idea" in lower or "must" in lower:
        return "main_idea"
    if "word" in lower or "means" in lower:
        return "vocabulary_context"
    if "because" in lower or "whether" in lower:
        return "inference"
    return "general_meaning"


def paragraph_beginner_tip(paragraph: str) -> str:
    lower = paragraph.lower()
    if "before" in lower:
        return "Perhatikan kata 'before' karena urutan tindakan sering menjadi jawaban detail."
    if "not only" in lower and "but also" in lower:
        return "Pola 'not only ... but also ...' berarti ada dua hal penting, bukan satu."
    if "whether" in lower:
        return "Kata 'whether' menunjukkan pilihan atau pengecekan apakah sesuatu benar."
    return "Baca perlahan: cari pelaku, aksi utama, lalu informasi tambahan."


def infer_main_idea(title: str, passage: str) -> str:
    lower = passage.lower()
    if "stakeholder" in lower and "strategy" in lower:
        return "Main idea: Business Analyst harus menghubungkan requirement, kebutuhan stakeholder, dan strategi organisasi."
    if "automation" in lower and "process" in lower:
        return "Main idea: Business Analyst perlu mengevaluasi proses sebelum merekomendasikan automation."
    if "approval" in lower and "delay" in lower:
        return "Main idea: Analyst perlu menemukan penyebab delay dalam approval workflow sebelum memilih solusi."
    return f"Main idea: bacaan ini membahas {title.lower()} dan informasi penting yang mendukung topik tersebut."


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
