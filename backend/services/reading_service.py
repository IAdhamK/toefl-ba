from __future__ import annotations

import time
from typing import Any

from backend.database import decode_json, encode_json, get_connection, now_iso
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

READING_SIMULATION_MODES = {
    "short": {"label": "Short simulation", "passage_count": 1, "question_count": 5, "duration_minutes": 10},
    "medium": {"label": "Medium simulation", "passage_count": 2, "question_count": 10, "duration_minutes": 20},
    "full": {"label": "Full practice simulation", "passage_count": 3, "question_count": 15, "duration_minutes": 30},
}

READING_SIMULATION_BANK = [
    {
        "id": "sim-passage-1",
        "title": "Stakeholder Alignment",
        "text": (
            "A business analyst must connect stakeholder needs with business requirements and organizational strategy. "
            "When a problem is described vaguely, the analyst clarifies the expected outcome before proposing a solution. "
            "This work helps teams avoid building features that do not support the business goal."
        ),
        "questions": [
            {
                "id": "sim-p1-q1",
                "text": "What is the main idea of the passage?",
                "options": [
                    "Business analysts should write code immediately.",
                    "Business analysts connect stakeholder needs, requirements, and strategy.",
                    "Stakeholders should avoid all discussions.",
                    "Strategy is unrelated to requirements.",
                ],
                "answer": 1,
                "sub_skill": "main_idea",
                "explanation": "The passage focuses on connecting needs, requirements, and strategy.",
            },
            {
                "id": "sim-p1-q2",
                "text": "The word 'clarifies' is closest in meaning to:",
                "options": ["makes clearer", "deletes", "delays", "approves"],
                "answer": 0,
                "sub_skill": "vocabulary_context",
                "explanation": "Clarifies means making unclear information easier to understand.",
            },
            {
                "id": "sim-p1-q3",
                "text": "What should the analyst clarify before proposing a solution?",
                "options": ["The expected outcome.", "The code style.", "The office schedule.", "The final contract."],
                "answer": 0,
                "sub_skill": "detail_information",
                "explanation": "The passage says the analyst clarifies the expected outcome.",
            },
            {
                "id": "sim-p1-q4",
                "text": "What can be inferred about vague problems?",
                "options": [
                    "They should be clarified before solution design.",
                    "They are always ready for development.",
                    "They should be ignored.",
                    "They are unrelated to stakeholders.",
                ],
                "answer": 0,
                "sub_skill": "inference",
                "explanation": "The passage implies unclear problems need clarification first.",
            },
            {
                "id": "sim-p1-q5",
                "text": "Which sentence best simplifies the first sentence?",
                "options": [
                    "A BA links stakeholder needs, requirements, and strategy.",
                    "A BA avoids business strategy.",
                    "Stakeholders write all requirements alone.",
                    "Requirements replace stakeholder needs.",
                ],
                "answer": 0,
                "sub_skill": "sentence_simplification",
                "explanation": "The simplified sentence keeps the same core meaning.",
            },
        ],
    },
    {
        "id": "sim-passage-2",
        "title": "Process Improvement Before Automation",
        "text": (
            "Before recommending automation, a business analyst evaluates the current process to identify delays, duplicate work, "
            "and unclear responsibilities. This analysis helps the organization decide whether technology is the right solution "
            "or whether the process itself must be redesigned."
        ),
        "questions": [
            {
                "id": "sim-p2-q1",
                "text": "Why does the analyst evaluate the current process?",
                "options": [
                    "To identify delays and unclear responsibilities.",
                    "To replace all employees.",
                    "To avoid speaking with stakeholders.",
                    "To approve every request automatically.",
                ],
                "answer": 0,
                "sub_skill": "detail_information",
                "explanation": "The first sentence states the analyst identifies delays, duplicate work, and unclear responsibilities.",
            },
            {
                "id": "sim-p2-q2",
                "text": "What is the main idea of the passage?",
                "options": [
                    "Automation should always be implemented first.",
                    "A process should be evaluated before choosing automation.",
                    "Technology removes the need for analysis.",
                    "Duplicate work is always useful.",
                ],
                "answer": 1,
                "sub_skill": "main_idea",
                "explanation": "The passage explains why process evaluation comes before automation decisions.",
            },
            {
                "id": "sim-p2-q3",
                "text": "The word 'redesigned' is closest in meaning to:",
                "options": ["designed again", "ignored", "approved", "measured"],
                "answer": 0,
                "sub_skill": "vocabulary_context",
                "explanation": "Redesigned means designed again or changed in structure.",
            },
            {
                "id": "sim-p2-q4",
                "text": "What can be inferred from the passage?",
                "options": [
                    "Technology is not always the best first answer.",
                    "Automation always solves unclear responsibilities.",
                    "The analyst should skip process review.",
                    "Duplicate work cannot be detected.",
                ],
                "answer": 0,
                "sub_skill": "inference",
                "explanation": "The passage implies analysis may show process redesign is better than technology.",
            },
            {
                "id": "sim-p2-q5",
                "text": "What does 'This analysis' refer to?",
                "options": [
                    "Evaluating the current process.",
                    "Writing code.",
                    "Approving a contract.",
                    "Replacing the team.",
                ],
                "answer": 0,
                "sub_skill": "reference",
                "explanation": "This analysis refers to evaluating the current process.",
            },
        ],
    },
    {
        "id": "sim-passage-3",
        "title": "Reliable Reporting",
        "text": (
            "Two departments enter customer data into separate systems, so weekly reports often show different totals. "
            "The analyst traces the discrepancy to timing differences and proposes a shared data validation step. "
            "The goal is to make decisions based on consistent information."
        ),
        "questions": [
            {
                "id": "sim-p3-q1",
                "text": "What problem is described in the passage?",
                "options": [
                    "Reports show different totals.",
                    "Customers refuse to share data.",
                    "The analyst removes validation.",
                    "Both systems are already identical.",
                ],
                "answer": 0,
                "sub_skill": "detail_information",
                "explanation": "The passage says weekly reports often show different totals.",
            },
            {
                "id": "sim-p3-q2",
                "text": "What is the purpose of the shared validation step?",
                "options": [
                    "To support decisions with consistent information.",
                    "To make reports less reliable.",
                    "To stop departments from using data.",
                    "To create duplicate work.",
                ],
                "answer": 0,
                "sub_skill": "author_purpose",
                "explanation": "The final sentence explains the goal of consistent decision-making information.",
            },
            {
                "id": "sim-p3-q3",
                "text": "The word 'discrepancy' is closest in meaning to:",
                "options": ["difference", "approval", "strategy", "outcome"],
                "answer": 0,
                "sub_skill": "vocabulary_context",
                "explanation": "Discrepancy means a difference between two things that should match.",
            },
            {
                "id": "sim-p3-q4",
                "text": "What can be inferred about the reports?",
                "options": [
                    "They may be unreliable without validation.",
                    "They are always correct.",
                    "They do not use customer data.",
                    "They should never be reviewed.",
                ],
                "answer": 0,
                "sub_skill": "inference",
                "explanation": "Different totals imply the reports need validation before decision-making.",
            },
            {
                "id": "sim-p3-q5",
                "text": "What is the function of the last sentence?",
                "options": [
                    "It explains the business goal of the proposed step.",
                    "It introduces an unrelated topic.",
                    "It rejects consistent information.",
                    "It lists every stakeholder.",
                ],
                "answer": 0,
                "sub_skill": "paragraph_function",
                "explanation": "The last sentence explains why the validation step matters.",
            },
        ],
    },
]


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


def get_reading_review(user_id: str | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    journey = get_reading_journey(user_id)
    subskills = journey["sub_skill_mastery"]
    attempts = get_reading_attempt_history(user_id)
    mistake_data = get_reading_mistake_patterns(user_id)
    queue_data = get_reading_review_queue(user_id)
    weak = weakest_subskills(subskills)
    recommended_sub_skill = next_trainable_subskill(weak[0]["subskill"] if weak else "main_idea")
    low_passages = low_score_passages(attempts)
    misunderstood_vocab = vocabulary_frequently_misunderstood(attempts, subskills)
    weakness_summary = {
        "primary_weakness": weak[0] if weak else None,
        "secondary_weakness": weak[1] if len(weak) > 1 else None,
        "low_score_passages": low_passages,
        "vocabulary_frequently_misunderstood": misunderstood_vocab,
        "bantuan_id_usage": bantuan_id_usage_summary(attempts),
    }
    return {
        "user_id": user_id,
        "weakness_summary": weakness_summary,
        "mistake_patterns": mistake_data["patterns"],
        "recommended_sub_skill": recommended_sub_skill,
        "recommended_practice": READING_ACTIONS.get(recommended_sub_skill, READING_ACTIONS["main_idea"]),
        "review_items": queue_data["review_items"],
        "mentor_message": reading_mentor_message(weakness_summary, recommended_sub_skill),
    }


def get_reading_mistake_patterns(user_id: str | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    attempts = get_reading_attempt_history(user_id)
    subskills = get_reading_subskill_mastery(user_id)
    patterns = []
    for item in sorted(subskills, key=lambda value: (value["wrong_count"], -value["attempt_count"]), reverse=True):
        if item["wrong_count"] > 0 or item["mastery_score"] < 60:
            patterns.append(
                {
                    "pattern": pattern_text_for_subskill(item["subskill"]),
                    "sub_skill": item["subskill"],
                    "label": item["label"],
                    "wrong_count": item["wrong_count"],
                    "attempt_count": item["attempt_count"],
                    "mastery_score": item["mastery_score"],
                    "recommendation": READING_ACTIONS.get(item["subskill"], READING_ACTIONS["main_idea"]),
                }
            )
    if not patterns:
        patterns.append(
            {
                "pattern": "Belum ada pola salah yang kuat. Mulai dari main idea agar fondasinya rapi.",
                "sub_skill": "main_idea",
                "label": label_subskill("main_idea"),
                "wrong_count": 0,
                "attempt_count": 0,
                "mastery_score": 0,
                "recommendation": READING_ACTIONS["main_idea"],
            }
        )
    return {
        "user_id": user_id,
        "patterns": patterns[:5],
        "repeated_wrong_question_types": patterns[:3],
        "low_score_passages": low_score_passages(attempts),
        "vocabulary_frequently_misunderstood": vocabulary_frequently_misunderstood(attempts, subskills),
        "bantuan_id_usage": bantuan_id_usage_summary(attempts),
    }


def get_reading_review_queue(user_id: str | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    attempts = get_reading_attempt_history(user_id)
    subskills = get_reading_subskill_mastery(user_id)
    weak = weakest_subskills(subskills)
    items = []
    for index, item in enumerate(weak[:3], start=1):
        target = next_trainable_subskill(item["subskill"])
        items.append(
            {
                "id": f"review-subskill-{item['subskill']}",
                "type": "weak_subskill",
                "title": f"Review {item['label']}",
                "sub_skill": target,
                "priority": index,
                "reason": f"Mastery {round(item['mastery_score'])}% dengan {item['wrong_count']} jawaban salah.",
                "action": READING_ACTIONS.get(target, READING_ACTIONS["main_idea"]),
            }
        )
    for passage in low_score_passages(attempts)[:3]:
        items.append(
            {
                "id": f"review-passage-{passage['activity_id']}",
                "type": "low_score_passage",
                "title": f"Ulangi passage {passage['activity_id']}",
                "sub_skill": "detail_information",
                "priority": 3,
                "reason": f"Skor terakhir {round(passage['accuracy'])}%.",
                "action": "Baca ulang evidence sentence dan cocokkan detail pertanyaan dengan passage.",
            }
        )
    for vocab in vocabulary_frequently_misunderstood(attempts, subskills)[:3]:
        items.append(
            {
                "id": f"review-vocab-{vocab['word']}",
                "type": "vocabulary_review",
                "title": f"Review vocabulary: {vocab['word']}",
                "sub_skill": "vocabulary_context",
                "priority": 2,
                "reason": vocab["reason"],
                "action": READING_ACTIONS["vocabulary_context"],
            }
        )
    if not items:
        items.append(
            {
                "id": "review-main-idea-start",
                "type": "starter_review",
                "title": "Mulai review Main Idea",
                "sub_skill": "main_idea",
                "priority": 1,
                "reason": "Belum ada data review yang cukup.",
                "action": READING_ACTIONS["main_idea"],
            }
        )
    return {"user_id": user_id, "review_items": items[:8]}


def start_reading_simulation(payload: dict[str, Any]) -> dict[str, Any]:
    mode = normalize_simulation_mode(payload.get("mode", "short"))
    config = READING_SIMULATION_MODES[mode]
    session_id = f"reading-sim-{mode}-{int(time.time() * 1000)}"
    passages = build_simulation_passages(mode)
    return {
        "session_id": session_id,
        "mode": mode,
        "label": config["label"],
        "duration_minutes": config["duration_minutes"],
        "duration_seconds": config["duration_minutes"] * 60,
        "started_at": now_iso(),
        "bantuan_id_policy": "Bantuan ID dibatasi dalam simulation mode. Gunakan hanya setelah selesai untuk review.",
        "passages": passages,
        "question_count": sum(len(passage["questions"]) for passage in passages),
    }


def submit_reading_simulation(payload: dict[str, Any]) -> dict[str, Any]:
    user_id = get_default_user_id(payload.get("user_id") or payload.get("userId"))
    session = payload.get("session") or {}
    mode = normalize_simulation_mode(payload.get("mode") or session.get("mode") or "short")
    session_id = payload.get("session_id") or session.get("session_id") or f"reading-sim-{mode}-{int(time.time() * 1000)}"
    passages = session.get("passages") or build_simulation_passages(mode)
    answers = payload.get("answers") or {}
    time_spent_seconds = int(payload.get("time_spent_seconds") or payload.get("timeSpentSeconds") or 0)
    flat_questions = []
    for passage in passages:
        for question in passage.get("questions", []):
            flat_questions.append((passage, question))
    correct = 0
    details = []
    subskill_totals: dict[str, dict[str, Any]] = {}
    mistakes = []
    answer_reviews = []
    for passage, question in flat_questions:
        qid = question["id"]
        selected = answers.get(qid)
        if isinstance(selected, str) and selected.isdigit():
            selected = int(selected)
        is_correct = selected == question.get("answer")
        correct += 1 if is_correct else 0
        sub_skill = normalize_subskill(question.get("sub_skill") or infer_question_subskill(question))
        bucket = subskill_totals.setdefault(sub_skill, {"sub_skill": sub_skill, "label": label_subskill(sub_skill), "correct": 0, "total": 0})
        bucket["total"] += 1
        bucket["correct"] += 1 if is_correct else 0
        if selected is not None:
            review = generate_answer_review(
                {
                    "passage": passage.get("text", ""),
                    "question": question,
                    "selected": selected,
                    "correct_answer": question.get("answer"),
                    "explanation": question.get("explanation", ""),
                    "sub_skill": sub_skill,
                }
            )
            answer_reviews.append(review)
        if not is_correct:
            mistakes.append({"question_id": qid, "selected": selected, "correct_answer": question.get("answer"), "sub_skill": sub_skill})
        details.append(
            {
                "question_id": qid,
                "passage_id": passage.get("id"),
                "selected": selected,
                "correct_answer": question.get("answer"),
                "is_correct": is_correct,
                "sub_skill": sub_skill,
            }
        )
    total = len(flat_questions) or 1
    accuracy = round((correct / total) * 100, 1)
    subskill_breakdown = []
    for item in subskill_totals.values():
        item["accuracy"] = round((item["correct"] / max(item["total"], 1)) * 100, 1)
        subskill_breakdown.append(item)
        update_skill_mastery(
            user_id=user_id,
            skill_type="reading",
            topic=item["sub_skill"],
            is_correct=item["accuracy"] >= 70,
            score=item["accuracy"],
        )
    strongest = max(subskill_breakdown, key=lambda item: item["accuracy"]) if subskill_breakdown else None
    weakest = min(subskill_breakdown, key=lambda item: item["accuracy"]) if subskill_breakdown else None
    recommended_subskill = next_trainable_subskill((weakest or {}).get("sub_skill", "main_idea"))
    result = {
        "session_id": session_id,
        "mode": mode,
        "total_score": round(accuracy),
        "accuracy": accuracy,
        "correct": correct,
        "total_questions": total,
        "time_spent_seconds": time_spent_seconds,
        "sub_skill_breakdown": subskill_breakdown,
        "strongest_sub_skill": strongest,
        "weakest_sub_skill": weakest,
        "recommended_next_practice": READING_ACTIONS.get(recommended_subskill, READING_ACTIONS["main_idea"]),
        "answer_review_summary": answer_reviews,
        "details": details,
        "submitted_at": now_iso(),
    }
    update = save_learning_attempt(
        user_id=user_id,
        skill_type="reading",
        activity_id=session_id,
        activity_type="reading_simulation",
        score=accuracy,
        max_score=100,
        mistakes=mistakes,
        feedback=f"SIMULATION_RESULT:{encode_json(result)}",
    )
    result["journey_update"] = update
    result["reading_journey"] = get_reading_journey(user_id)
    return result


def get_reading_simulation_result(session_id: str, user_id: str | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM learning_attempts
            WHERE user_id = ? AND skill_type = 'reading' AND activity_type = 'reading_simulation' AND activity_id = ?
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (user_id, session_id),
        ).fetchone()
    if not row:
        raise ValueError("Simulation result tidak ditemukan.")
    return parse_simulation_result_from_attempt(dict(row))


def get_reading_simulation_history(user_id: str | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id)
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM learning_attempts
            WHERE user_id = ? AND skill_type = 'reading' AND activity_type = 'reading_simulation'
            ORDER BY created_at DESC
            LIMIT 10
            """,
            (user_id,),
        ).fetchall()
    history = []
    for row in rows:
        result = parse_simulation_result_from_attempt(dict(row))
        history.append(
            {
                "session_id": result["session_id"],
                "mode": result["mode"],
                "total_score": result["total_score"],
                "accuracy": result["accuracy"],
                "time_spent_seconds": result.get("time_spent_seconds", 0),
                "submitted_at": result.get("submitted_at") or row["created_at"],
                "weakest_sub_skill": result.get("weakest_sub_skill"),
                "recommended_next_practice": result.get("recommended_next_practice"),
            }
        )
    return {"user_id": user_id, "history": history}


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


def get_reading_attempt_history(user_id: str, limit: int = 50) -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM learning_attempts
            WHERE user_id = ? AND skill_type = 'reading'
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
    attempts = []
    for row in rows:
        item = dict(row)
        item["score"] = float(item.get("score") or 0)
        item["max_score"] = float(item.get("max_score") or 100)
        item["accuracy"] = float(item.get("accuracy") or 0)
        item["mistakes"] = decode_json(item.get("mistakes_json"), [])
        attempts.append(item)
    return attempts


def low_score_passages(attempts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    items = []
    for attempt in attempts:
        activity_id = attempt.get("activity_id") or "reading-passage"
        if activity_id in seen:
            continue
        seen.add(activity_id)
        if float(attempt.get("accuracy") or 0) < 70 and attempt.get("activity_type") != "contextual_help":
            items.append(
                {
                    "activity_id": activity_id,
                    "activity_type": attempt.get("activity_type"),
                    "accuracy": round(float(attempt.get("accuracy") or 0), 1),
                    "created_at": attempt.get("created_at"),
                    "feedback": attempt.get("feedback") or "Skor passage masih perlu review.",
                }
            )
    return items


def vocabulary_frequently_misunderstood(attempts: list[dict[str, Any]], subskills: list[dict[str, Any]]) -> list[dict[str, str]]:
    words: dict[str, int] = {}
    for attempt in attempts:
        for mistake in attempt.get("mistakes", []) or []:
            text = " ".join(str(value) for value in mistake.values()) if isinstance(mistake, dict) else str(mistake)
            for word in READING_VOCABULARY_MEANINGS:
                if word in text.lower():
                    words[word] = words.get(word, 0) + 1
    vocab_mastery = next((item for item in subskills if item["subskill"] == "vocabulary_context"), None)
    if vocab_mastery and vocab_mastery["wrong_count"] > 0 and not words:
        words["clarify"] = vocab_mastery["wrong_count"]
    return [
        {
            "word": word,
            "meaning_id": READING_VOCABULARY_MEANINGS.get(word, "arti sesuai konteks"),
            "count": count,
            "reason": "Sering muncul pada kesalahan Reading atau sub-skill vocabulary context masih rendah.",
        }
        for word, count in sorted(words.items(), key=lambda item: item[1], reverse=True)[:5]
    ]


def bantuan_id_usage_summary(attempts: list[dict[str, Any]]) -> dict[str, Any]:
    help_attempts = [
        attempt for attempt in attempts
        if "contextual_help" in str(attempt.get("activity_type") or "")
        or "Bantuan ID" in str(attempt.get("feedback") or "")
    ]
    count = len(help_attempts)
    if count >= 8:
        level = "high"
        message = "Bantuan ID sering dipakai. Coba tebak arti kalimat dulu sebelum membuka bantuan."
    elif count >= 3:
        level = "medium"
        message = "Bantuan ID dipakai cukup sering. Itu baik untuk belajar, lalu coba jawab tanpa bantuan."
    else:
        level = "normal"
        message = "Penggunaan Bantuan ID masih wajar atau belum tercatat di backend."
    return {"count": count, "level": level, "message": message}


def pattern_text_for_subskill(subskill: str) -> str:
    patterns = {
        "general_meaning": "Masih perlu memperkuat arti umum passage sebelum masuk ke soal.",
        "main_idea": "Sering memilih detail kecil sebagai ide utama.",
        "detail_information": "Sering kehilangan evidence sentence untuk detail spesifik.",
        "vocabulary_context": "Sering memakai arti kamus tanpa mengecek konteks kalimat.",
        "reference": "Perlu latihan mencari noun yang dirujuk pronoun seperti it, they, this.",
        "sentence_simplification": "Perlu memisahkan subject, main verb, dan informasi tambahan dalam kalimat panjang.",
        "inference": "Perlu membedakan informasi tersirat dari asumsi yang tidak didukung passage.",
        "author_purpose": "Perlu memahami alasan penulis menyebut detail tertentu.",
        "paragraph_function": "Perlu memahami fungsi paragraf dalam struktur bacaan.",
        "ba_case_analysis": "Perlu menghubungkan masalah, stakeholder, requirement, dan business outcome.",
    }
    return patterns.get(subskill, "Pola salah belum spesifik. Lanjutkan review Reading.")


def reading_mentor_message(weakness_summary: dict[str, Any], recommended_sub_skill: str) -> str:
    weakness = weakness_summary.get("primary_weakness") or {}
    label = weakness.get("label") or label_subskill(recommended_sub_skill)
    low_count = len(weakness_summary.get("low_score_passages") or [])
    if low_count:
        return (
            f"Fokus Reading berikutnya adalah {label}. Ada {low_count} passage dengan skor rendah, "
            "jadi ulangi evidence sentence dulu sebelum mengerjakan soal baru."
        )
    return (
        f"Fokus Reading berikutnya adalah {label}. Kerjakan latihan pendek, lalu cek Answer Review untuk melihat pola salah."
    )


def normalize_simulation_mode(mode: Any) -> str:
    normalized = str(mode or "short").strip().lower()
    if normalized in {"full_practice", "full-practice"}:
        normalized = "full"
    if normalized not in READING_SIMULATION_MODES:
        raise ValueError("Mode simulation harus short, medium, atau full.")
    return normalized


def build_simulation_passages(mode: str) -> list[dict[str, Any]]:
    config = READING_SIMULATION_MODES[mode]
    passages = []
    for passage in READING_SIMULATION_BANK[: config["passage_count"]]:
        copied = {
            "id": passage["id"],
            "title": passage["title"],
            "text": passage["text"],
            "questions": [dict(question) for question in passage["questions"]],
        }
        passages.append(copied)
    return passages


def parse_simulation_result_from_attempt(attempt: dict[str, Any]) -> dict[str, Any]:
    feedback = str(attempt.get("feedback") or "")
    if feedback.startswith("SIMULATION_RESULT:"):
        parsed = decode_json(feedback.removeprefix("SIMULATION_RESULT:"), {})
        if parsed:
            return parsed
    return {
        "session_id": attempt.get("activity_id"),
        "mode": "unknown",
        "total_score": round(float(attempt.get("accuracy") or 0)),
        "accuracy": float(attempt.get("accuracy") or 0),
        "correct": 0,
        "total_questions": 0,
        "time_spent_seconds": 0,
        "sub_skill_breakdown": [],
        "strongest_sub_skill": None,
        "weakest_sub_skill": None,
        "recommended_next_practice": READING_ACTIONS["main_idea"],
        "answer_review_summary": [],
        "submitted_at": attempt.get("created_at"),
    }


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
