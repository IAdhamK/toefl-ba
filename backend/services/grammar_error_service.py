from __future__ import annotations

from copy import deepcopy
from typing import Any

from backend.services.grammar_journey_service import save_grammar_attempt


ERROR_CATEGORY_META: dict[str, dict[str, Any]] = {
    "subject_verb_agreement": {
        "level": "basic",
        "title": "Subject-Verb Agreement",
        "learning_objective": "Mencocokkan subject tunggal/jamak dengan verb yang tepat.",
        "explanation_id": "Subject jamak biasanya memakai verb tanpa -s atau memakai are/were.",
        "beginner_tip": "Cari subject dulu, lalu cek apakah subject-nya tunggal atau jamak.",
        "common_trap": "Pemula sering memakai is untuk subject jamak seperti requirements.",
        "ba_context": "Requirement dan stakeholders sering muncul sebagai subject jamak dalam dokumen BA.",
        "related_topic_id": "subject_verb",
    },
    "missing_be_after_modal": {
        "level": "basic",
        "title": "Missing 'be' after modal",
        "learning_objective": "Memakai pola modal + be + adjective dengan benar.",
        "explanation_id": "Jika setelah modal ada adjective, tambahkan be sebelum adjective.",
        "beginner_tip": "Ingat pola: must/should/can + be + adjective.",
        "common_trap": "Pemula sering langsung menaruh adjective setelah modal.",
        "ba_context": "Sering dipakai untuk requirement kualitas sistem.",
        "related_topic_id": "modal_verb",
    },
    "wrong_modal_pattern": {
        "level": "basic",
        "title": "Wrong Modal Pattern",
        "learning_objective": "Memakai verb dasar setelah modal.",
        "explanation_id": "Setelah modal seperti must/should/can, gunakan base verb.",
        "beginner_tip": "Jangan pakai -s, -ed, atau to setelah modal.",
        "common_trap": "Must clarifies, should documented, dan can to improve adalah pola yang salah.",
        "ba_context": "Modal banyak dipakai di recommendation dan requirement statement.",
        "related_topic_id": "modal_verb",
    },
    "article_error": {
        "level": "basic",
        "title": "Article Error",
        "learning_objective": "Memakai a/an/the dengan noun singular.",
        "explanation_id": "Noun singular yang bisa dihitung biasanya perlu article.",
        "beginner_tip": "Jika noun tunggal dapat dihitung, cek apakah perlu a/an/the.",
        "common_trap": "Pemula sering menghilangkan article sebelum kata seperti requirement atau issue.",
        "ba_context": "Article membuat requirement sentence terdengar lebih natural.",
        "related_topic_id": "parts_of_speech",
    },
    "preposition_error": {
        "level": "basic",
        "title": "Preposition Error",
        "learning_objective": "Memakai preposition yang tepat dalam konteks BA.",
        "explanation_id": "Beberapa verb/adjective punya pasangan preposition tetap, seperti align with.",
        "beginner_tip": "Hafalkan phrase BA yang sering muncul: align with, responsible for, impact on.",
        "common_trap": "Pemula sering menerjemahkan preposition dari Bahasa Indonesia secara langsung.",
        "ba_context": "Preposition penting untuk menjelaskan hubungan requirement, stakeholder, dan strategy.",
        "related_topic_id": "prepositional_phrase",
    },
    "missing_main_verb": {
        "level": "intermediate",
        "title": "Missing Main Verb",
        "learning_objective": "Memastikan kalimat panjang tetap punya main verb.",
        "explanation_id": "Phrase panjang tidak cukup; kalimat tetap membutuhkan main verb.",
        "beginner_tip": "Setelah subject panjang, cari finite verb utama.",
        "common_trap": "User mengira phrase -ing sudah cukup menjadi verb utama.",
        "ba_context": "Kalimat BA panjang sering punya phrase sebelum main verb.",
        "related_topic_id": "gerund_vs_main_verb",
    },
    "gerund_as_main_verb": {
        "level": "intermediate",
        "title": "Gerund as Main Verb",
        "learning_objective": "Membedakan -ing phrase dan main verb.",
        "explanation_id": "Kata -ing dapat menjelaskan noun, bukan menjadi main verb.",
        "beginner_tip": "Cari modal atau finite verb setelah subject utama.",
        "common_trap": "Working/reviewing terlihat seperti aksi, tetapi sering hanya modifier.",
        "ba_context": "Sering muncul dalam kalimat stakeholder/process analysis.",
        "related_topic_id": "gerund_vs_main_verb",
    },
    "passive_voice_error": {
        "level": "intermediate",
        "title": "Passive Voice Error",
        "learning_objective": "Memakai pola passive be + V3 dengan benar.",
        "explanation_id": "Passive voice membutuhkan be dan past participle.",
        "beginner_tip": "Cari pola is/are/was/were + V3.",
        "common_trap": "Pemula sering menulis is process, bukan is processed.",
        "ba_context": "Passive voice banyak dipakai dalam process documentation.",
        "related_topic_id": "passive_voice",
    },
    "parallel_structure_error": {
        "level": "intermediate",
        "title": "Parallel Structure Error",
        "learning_objective": "Membuat daftar aksi dengan bentuk grammar yang sejajar.",
        "explanation_id": "Item dalam daftar harus memakai bentuk yang konsisten.",
        "beginner_tip": "Jika item pertama verb dasar, item berikutnya juga verb dasar.",
        "common_trap": "Mencampur document dan ensuring dalam satu daftar.",
        "ba_context": "Parallel structure penting dalam requirement list dan recommendation.",
        "related_topic_id": "parallel_structure",
    },
    "double_connector": {
        "level": "intermediate",
        "title": "Double Connector",
        "learning_objective": "Menghindari dua connector yang tidak perlu dalam satu hubungan ide.",
        "explanation_id": "Although sudah menunjukkan kontras, jadi tidak perlu but.",
        "beginner_tip": "Pilih satu connector utama untuk satu hubungan logika.",
        "common_trap": "Although ... but ... sering terbawa dari struktur Bahasa Indonesia.",
        "ba_context": "Connector yang bersih membuat reasoning BA lebih profesional.",
        "related_topic_id": "connector_logic",
    },
    "wrong_connector": {
        "level": "intermediate",
        "title": "Wrong Connector",
        "learning_objective": "Memilih connector sesuai hubungan ide.",
        "explanation_id": "Because untuk sebab, although untuk kontras, therefore untuk akibat.",
        "beginner_tip": "Tentukan dulu hubungan ide: sebab, akibat, kontras, atau tambahan.",
        "common_trap": "Pemula sering memilih connector berdasarkan terjemahan kata, bukan logika kalimat.",
        "ba_context": "Connector logic penting untuk impact analysis dan recommendation.",
        "related_topic_id": "connector_logic",
    },
    "word_form_error": {
        "level": "intermediate",
        "title": "Word Form Error",
        "learning_objective": "Memilih bentuk kata yang benar: noun, verb, adjective, atau adverb.",
        "explanation_id": "Kalimat formal sering membutuhkan noun seperti efficiency, bukan adjective efficient.",
        "beginner_tip": "Lihat posisi kata dalam kalimat untuk menentukan word form.",
        "common_trap": "Efficient dan efficiency sering tertukar.",
        "ba_context": "Word form penting dalam report dan benefit statement.",
        "related_topic_id": "nominalization",
    },
}


def _item(
    item_id: str,
    error_type: str,
    incorrect: str,
    correct: str,
    explanation: str,
    rule: str,
    options: list[str] | None = None,
) -> dict[str, Any]:
    category = ERROR_CATEGORY_META[error_type]
    options = options or [
        incorrect,
        correct,
        correct.replace(" be ", " is "),
        correct.replace(" the ", " "),
    ]
    return {
        "id": item_id,
        "error_type": error_type,
        "level": category["level"],
        "instruction_id": "Pilih perbaikan kalimat yang paling tepat.",
        "incorrect_sentence": incorrect,
        "question": "Which sentence is correct?",
        "options": list(dict.fromkeys(options)),
        "correct_answer": correct,
        "corrected_sentence": correct,
        "explanation_id": explanation,
        "hint_id": category["beginner_tip"],
        "grammar_rule_id": rule,
        "common_trap": category["common_trap"],
        "difficulty": category["level"],
        "related_topic_id": category["related_topic_id"],
        "ba_context_note": category["ba_context"],
    }


CORRECTION_ITEMS: list[dict[str, Any]] = [
    _item(
        "subject_verb_agreement_1",
        "subject_verb_agreement",
        "The requirements is unclear.",
        "The requirements are unclear.",
        "Requirements adalah plural, jadi gunakan are.",
        "Plural subject + are/base verb",
    ),
    _item(
        "subject_verb_agreement_2",
        "subject_verb_agreement",
        "Stakeholders provides feedback every week.",
        "Stakeholders provide feedback every week.",
        "Stakeholders adalah plural, jadi verb tidak memakai -s.",
        "Plural subject + base verb",
    ),
    _item(
        "missing_be_after_modal_1",
        "missing_be_after_modal",
        "The system must flexible for all users.",
        "The system must be flexible for all users.",
        "Setelah modal 'must', gunakan base verb. Karena 'flexible' adalah adjective, perlu 'be'.",
        "Subject + modal + be + adjective",
        ["The system must flexible for all users.", "The system must be flexible for all users.", "The system must is flexible for all users.", "The system must being flexible for all users."],
    ),
    _item(
        "missing_be_after_modal_2",
        "missing_be_after_modal",
        "The report should accurate before submission.",
        "The report should be accurate before submission.",
        "Setelah should dan sebelum adjective accurate, gunakan be.",
        "Subject + modal + be + adjective",
    ),
    _item(
        "wrong_modal_pattern_1",
        "wrong_modal_pattern",
        "The analyst must clarifies the scope.",
        "The analyst must clarify the scope.",
        "Setelah must, gunakan verb dasar clarify.",
        "Modal + base verb",
    ),
    _item(
        "wrong_modal_pattern_2",
        "wrong_modal_pattern",
        "The team should documented the decision.",
        "The team should document the decision.",
        "Setelah should, gunakan verb dasar document.",
        "Modal + base verb",
    ),
    _item(
        "article_error_1",
        "article_error",
        "The analyst identified issue in the workflow.",
        "The analyst identified an issue in the workflow.",
        "Issue adalah singular countable noun, jadi perlu article.",
        "Article + singular countable noun",
    ),
    _item(
        "preposition_error_1",
        "preposition_error",
        "The requirement must align to business strategy.",
        "The requirement must align with business strategy.",
        "Phrase yang umum adalah align with, bukan align to.",
        "align with + noun",
    ),
    _item(
        "missing_main_verb_1",
        "missing_main_verb",
        "The analyst working with stakeholders the requirement.",
        "The analyst working with stakeholders documents the requirement.",
        "Phrase working with stakeholders hanya modifier; kalimat masih perlu main verb documents.",
        "Subject + modifier + main verb + object",
    ),
    _item(
        "missing_main_verb_2",
        "missing_main_verb",
        "The process reviewed by the team every month.",
        "The process is reviewed by the team every month.",
        "Passive voice butuh be sebelum V3 reviewed.",
        "Subject + be + V3",
    ),
    _item(
        "gerund_as_main_verb_1",
        "gerund_as_main_verb",
        "The analyst working with stakeholders clarify the requirement.",
        "The analyst working with stakeholders clarifies the requirement.",
        "Working hanya menjelaskan analyst; main verb untuk subject tunggal adalah clarifies.",
        "Subject + modifier + finite verb",
    ),
    _item(
        "gerund_as_main_verb_2",
        "gerund_as_main_verb",
        "The team reviewing the process improve the workflow.",
        "The team reviewing the process improves the workflow.",
        "Reviewing the process hanya modifier; main verb untuk the team adalah improves.",
        "Subject + modifier + finite verb",
    ),
    _item(
        "passive_voice_error_1",
        "passive_voice_error",
        "The data is process by the system.",
        "The data is processed by the system.",
        "Passive voice membutuhkan past participle: processed.",
        "be + past participle",
    ),
    _item(
        "passive_voice_error_2",
        "passive_voice_error",
        "The requirements are document by the analyst.",
        "The requirements are documented by the analyst.",
        "Passive voice memakai are + documented.",
        "be + past participle",
    ),
    _item(
        "parallel_structure_error_1",
        "parallel_structure_error",
        "The analyst must document requirements and ensuring alignment.",
        "The analyst must document requirements and ensure alignment.",
        "Setelah must, dua aksi harus sejajar: document dan ensure.",
        "Parallel base verbs after modal",
    ),
    _item(
        "parallel_structure_error_2",
        "parallel_structure_error",
        "The solution should improve reporting, reducing errors, and support decisions.",
        "The solution should improve reporting, reduce errors, and support decisions.",
        "Tiga aksi harus sejajar: improve, reduce, support.",
        "Parallel verb list",
    ),
    _item(
        "double_connector_1",
        "double_connector",
        "Although the workflow is useful, but it is too complex.",
        "Although the workflow is useful, it is too complex.",
        "Although sudah menunjukkan kontras, jadi tidak perlu but.",
        "Although + clause, main clause",
    ),
    _item(
        "double_connector_2",
        "double_connector",
        "Because the requirement is unclear, so the team delays development.",
        "Because the requirement is unclear, the team delays development.",
        "Because sudah menunjukkan sebab, jadi tidak perlu so.",
        "Because + clause, main clause",
    ),
    _item(
        "wrong_connector_1",
        "wrong_connector",
        "The process is slow because the team still recommends automation cautiously.",
        "Although the process is slow, the team still recommends automation cautiously.",
        "Hubungannya kontras, jadi gunakan although.",
        "Although for contrast",
    ),
    _item(
        "wrong_connector_2",
        "wrong_connector",
        "The data is inconsistent although the report cannot be finalized.",
        "The data is inconsistent; therefore, the report cannot be finalized.",
        "Hubungannya sebab-akibat, jadi gunakan therefore.",
        "Therefore for result",
    ),
    _item(
        "word_form_error_1",
        "word_form_error",
        "The implementation will improve efficient.",
        "The implementation will improve efficiency.",
        "Setelah improve dibutuhkan noun sebagai object: efficiency.",
        "Verb + noun object",
    ),
    _item(
        "word_form_error_2",
        "word_form_error",
        "The analysis supports accurate of the report.",
        "The analysis supports the accuracy of the report.",
        "Setelah supports dibutuhkan noun phrase: the accuracy.",
        "Verb + noun phrase",
    ),
]


def get_error_categories() -> list[dict[str, Any]]:
    return [
        {
            "error_type": error_type,
            "level": item["level"],
            "title": item["title"],
            "learning_objective": item["learning_objective"],
            "related_topic_id": item["related_topic_id"],
        }
        for error_type, item in ERROR_CATEGORY_META.items()
    ]


def get_error_category(error_type: str) -> dict[str, Any] | None:
    item = ERROR_CATEGORY_META.get(error_type)
    if not item:
        return None
    examples = [
        {
            "incorrect_sentence": correction["incorrect_sentence"],
            "corrected_sentence": correction["corrected_sentence"],
            "simple_meaning_id": "Makna kalimat tetap sama, tetapi struktur grammar dibuat benar.",
            "error_focus": correction["error_type"],
            "why_wrong_id": correction["explanation_id"],
            "correction_rule_id": correction["grammar_rule_id"],
            "ba_context_note": correction["ba_context_note"],
        }
        for correction in CORRECTION_ITEMS
        if correction["error_type"] == error_type
    ]
    return {"error_type": error_type, **deepcopy(item), "examples": deepcopy(examples)}


def get_error_correction_items(error_type: str | None = None, level: str | None = None) -> list[dict[str, Any]]:
    normalized_error = error_type.strip() if error_type else None
    normalized_level = level.strip().lower() if level else None
    items = [
        item
        for item in CORRECTION_ITEMS
        if (not normalized_error or item["error_type"] == normalized_error)
        and (not normalized_level or item["level"] == normalized_level)
    ]
    return deepcopy(items)


def get_error_correction_item(item_id: str) -> dict[str, Any] | None:
    for item in CORRECTION_ITEMS:
        if item["id"] == item_id:
            return deepcopy(item)
    return None


def submit_error_correction(payload: dict) -> dict[str, Any]:
    error_type = payload.get("error_type")
    items = get_error_correction_items(error_type=error_type)
    if not items:
        items = get_error_correction_items()
    result = score_error_correction_answers(payload.get("answers") or {}, items)
    recommendation = get_error_correction_recommendation(result["score"], result["mistakes"])
    activity_id = error_type or "mixed_error_correction"
    attempt_update = save_grammar_attempt(
        {
            "user_id": payload.get("user_id") or "default-user",
            "topic_id": recommendation["review_topic_id"],
            "activity_type": "grammar_error_correction",
            "score": result["score"],
            "max_score": result["max_score"],
            "mistakes": result["mistakes"],
            "feedback": recommendation["mentor_message"],
            "activity_id": activity_id,
        }
    )
    return {
        "result": result,
        "recommendation": recommendation,
        "grammar_journey": attempt_update["grammar_journey"],
    }


def score_error_correction_answers(answers: dict, items: list[dict[str, Any]]) -> dict[str, Any]:
    details = []
    for item in items:
        if item["id"] not in answers:
            continue
        user_answer = answers.get(item["id"], "")
        is_correct = _normalize(user_answer) == _normalize(item["correct_answer"])
        details.append(
            {
                "item_id": item["id"],
                "is_correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": item["correct_answer"],
                "incorrect_sentence": item["incorrect_sentence"],
                "corrected_sentence": item["corrected_sentence"],
                "explanation_id": item["explanation_id"],
                "error_type": item["error_type"],
                "related_topic_id": item["related_topic_id"],
            }
        )
    total = len(details)
    correct = len([item for item in details if item["is_correct"]])
    score = round((correct / total) * 100, 1) if total else 0
    mistakes = [item for item in details if not item["is_correct"]]
    return {
        "score": score,
        "max_score": 100,
        "correct_count": correct,
        "total_questions": total,
        "is_passed": score >= 70,
        "details": details,
        "mistakes": mistakes,
    }


def get_error_correction_recommendation(score: float, mistakes: list) -> dict[str, Any]:
    if mistakes:
        first = mistakes[0]
        review_error_type = first["error_type"]
        review_topic_id = first["related_topic_id"]
    else:
        review_error_type = "mixed_error_correction"
        review_topic_id = "modal_verb"
    if score >= 70:
        return {
            "next_action": "Lanjutkan ke error type lain atau coba ulang dengan campuran soal.",
            "review_error_type": review_error_type,
            "review_topic_id": review_topic_id,
            "mentor_message": "Bagus. Kamu mulai bisa mengenali dan memperbaiki grammar error umum.",
        }
    return {
        "next_action": "Ulangi correction item yang salah dan baca pola grammar-nya pelan-pelan.",
        "review_error_type": review_error_type,
        "review_topic_id": review_topic_id,
        "mentor_message": "Tidak apa-apa. Fokus ke satu pola dulu: lihat kalimat salah, aturan, lalu kalimat benar.",
    }


def _normalize(value: Any) -> str:
    return str(value or "").strip().lower()
