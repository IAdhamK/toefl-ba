from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

from backend.services.grammar_journey_service import save_grammar_attempt


SENTENCE_BUILDER_LEVELS: list[dict[str, Any]] = [
    {
        "id": "basic",
        "title": "Basic Sentence Builder",
        "description": "Latihan menyusun kalimat dasar dengan subject, modal, verb, object, dan be.",
        "modes": ["arrange_words", "complete_sentence", "fix_word_order"],
    },
    {
        "id": "intermediate",
        "title": "Intermediate Sentence Builder",
        "description": "Latihan menggabungkan kalimat, modifier phrase, passive voice, connector, dan word order.",
        "modes": ["combine_sentences", "arrange_words", "complete_sentence", "fix_word_order"],
    },
    {
        "id": "advanced_preview",
        "title": "Advanced Preview: Formal BA Writing",
        "description": "Preview kecil untuk mengubah kalimat informal menjadi kalimat Business Analyst yang lebih formal.",
        "modes": ["rewrite_formal_ba_sentence", "combine_sentences"],
    },
]


def _builder_item(
    item_id: str,
    level: str,
    mode: str,
    topic_id: str,
    title: str,
    instruction_id: str,
    prompt_text: str,
    input_parts: list[str],
    expected_answer: str,
    explanation_id: str,
    grammar_rule_id: str,
    beginner_tip: str,
    ba_context_note: str,
    difficulty: str,
    related_topic_id: str,
    acceptable_answers: list[str] | None = None,
    required_keywords: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "id": item_id,
        "level": level,
        "mode": mode,
        "topic_id": topic_id,
        "title": title,
        "instruction_id": instruction_id,
        "prompt_text": prompt_text,
        "input_parts": input_parts,
        "expected_answer": expected_answer,
        "acceptable_answers": acceptable_answers or [],
        "required_keywords": required_keywords or [],
        "explanation_id": explanation_id,
        "grammar_rule_id": grammar_rule_id,
        "beginner_tip": beginner_tip,
        "ba_context_note": ba_context_note,
        "difficulty": difficulty,
        "related_topic_id": related_topic_id,
    }


SENTENCE_BUILDER_ITEMS: list[dict[str, Any]] = [
    _builder_item(
        "arrange_basic_modal_1",
        "basic",
        "arrange_words",
        "modal_verb",
        "Arrange modal verb sentence",
        "Susun kata berikut menjadi kalimat yang benar.",
        "must / requirements / elicit / A business analyst",
        ["must", "requirements", "elicit", "A business analyst"],
        "A business analyst must elicit requirements.",
        "Pola yang benar adalah Subject + modal + verb + object.",
        "Subject + modal + base verb + object",
        "Cari subject dulu, lalu modal, lalu verb utama, lalu object.",
        "Kalimat ini sering muncul dalam konteks pekerjaan Business Analyst.",
        "basic",
        "modal_verb",
        ["A business analyst must elicit requirements"],
    ),
    _builder_item(
        "arrange_basic_report_1",
        "basic",
        "arrange_words",
        "simple_sentence_pattern",
        "Arrange report sentence",
        "Susun kata berikut menjadi kalimat yang benar.",
        "generates / The system / reports / automatically",
        ["generates", "The system", "reports", "automatically"],
        "The system generates reports automatically.",
        "Subject berada di awal, lalu verb, object, dan adverb.",
        "Subject + verb + object + adverb",
        "Mulai dari siapa/apa pelakunya: The system.",
        "Dipakai untuk menjelaskan fungsi sistem.",
        "basic",
        "simple_sentence_pattern",
    ),
    _builder_item(
        "arrange_basic_scope_1",
        "basic",
        "arrange_words",
        "subject_verb",
        "Arrange requirement sentence",
        "Susun kata berikut menjadi kalimat yang benar.",
        "clarifies / the scope / The analyst",
        ["clarifies", "the scope", "The analyst"],
        "The analyst clarifies the scope.",
        "Subject tunggal The analyst memakai verb clarifies.",
        "Subject + verb + object",
        "Cari subject, lalu aksi utama.",
        "Kalimat BA sering memakai clarify untuk scope atau requirement.",
        "basic",
        "subject_verb",
    ),
    _builder_item(
        "complete_basic_be_1",
        "basic",
        "complete_sentence",
        "modal_verb",
        "Complete modal + be",
        "Isi bagian kosong dengan kata yang tepat.",
        "The system must ___ flexible for all users.",
        ["The system must", "___", "flexible for all users"],
        "be",
        "Setelah modal must dan sebelum adjective flexible, gunakan be.",
        "modal + be + adjective",
        "Jika setelah modal ada adjective, tambahkan be.",
        "Requirement kualitas sistem sering memakai must be.",
        "basic",
        "modal_verb",
    ),
    _builder_item(
        "complete_basic_modal_1",
        "basic",
        "complete_sentence",
        "modal_verb",
        "Complete modal verb",
        "Isi bagian kosong dengan verb dasar yang tepat.",
        "The analyst should ___ the requirement.",
        ["The analyst should", "___", "the requirement"],
        "document",
        "Setelah should, gunakan base verb document.",
        "modal + base verb",
        "Jangan menambahkan -ed atau -s setelah modal.",
        "Kalimat ini cocok untuk rekomendasi tugas BA.",
        "basic",
        "modal_verb",
    ),
    _builder_item(
        "complete_basic_article_1",
        "basic",
        "complete_sentence",
        "parts_of_speech",
        "Complete article sentence",
        "Isi bagian kosong dengan article yang tepat.",
        "The analyst identified ___ issue in the workflow.",
        ["The analyst identified", "___", "issue in the workflow"],
        "an",
        "Issue diawali bunyi vokal dan singular countable noun, jadi gunakan an.",
        "article + singular countable noun",
        "Cek apakah noun tunggal dapat dihitung membutuhkan a/an.",
        "Article membuat report BA terdengar natural.",
        "basic",
        "parts_of_speech",
    ),
    _builder_item(
        "fix_order_basic_modal_1",
        "basic",
        "fix_word_order",
        "modal_verb",
        "Fix modal word order",
        "Perbaiki urutan kata supaya menjadi kalimat pernyataan.",
        "Must the system generate reports automatically.",
        ["Must", "the system", "generate", "reports", "automatically"],
        "The system must generate reports automatically.",
        "Untuk pernyataan, subject muncul sebelum modal.",
        "Subject + modal + base verb + object",
        "Jangan mulai dengan modal jika bukan pertanyaan.",
        "Dipakai untuk requirement statement.",
        "basic",
        "modal_verb",
    ),
    _builder_item(
        "fix_order_basic_scope_1",
        "basic",
        "fix_word_order",
        "simple_sentence_pattern",
        "Fix simple word order",
        "Perbaiki urutan kata.",
        "Clarifies the analyst the requirement.",
        ["Clarifies", "the analyst", "the requirement"],
        "The analyst clarifies the requirement.",
        "Kalimat pernyataan dimulai dari subject.",
        "Subject + verb + object",
        "Cari pelaku dulu sebelum verb.",
        "Kalimat BA harus jelas siapa melakukan apa.",
        "basic",
        "simple_sentence_pattern",
    ),
    _builder_item(
        "combine_intermediate_parallel_1",
        "intermediate",
        "combine_sentences",
        "parallel_structure",
        "Combine parallel actions",
        "Gabungkan dua kalimat menjadi satu kalimat yang lebih efisien.",
        "The analyst interviews users. The analyst documents requirements.",
        ["The analyst interviews users.", "The analyst documents requirements."],
        "The analyst interviews users and documents requirements.",
        "Dua aksi dengan subject sama bisa digabung memakai and.",
        "Subject + verb + object + and + verb + object",
        "Jangan ulangi subject jika aksi dilakukan oleh pelaku yang sama.",
        "Kalimat ringkas membantu requirement documentation.",
        "intermediate",
        "parallel_structure",
    ),
    _builder_item(
        "combine_intermediate_connector_1",
        "intermediate",
        "combine_sentences",
        "connector_logic",
        "Combine contrast sentence",
        "Gabungkan dua ide dengan connector yang tepat.",
        "The workflow is useful. It is too complex.",
        ["The workflow is useful.", "It is too complex."],
        "Although the workflow is useful, it is too complex.",
        "Although menunjukkan kontras antara useful dan too complex.",
        "Although + clause, main clause",
        "Gunakan satu connector untuk satu hubungan ide.",
        "Dipakai saat menjelaskan trade-off proses.",
        "intermediate",
        "connector_logic",
    ),
    _builder_item(
        "combine_intermediate_result_1",
        "intermediate",
        "combine_sentences",
        "connector_logic",
        "Combine cause-result sentence",
        "Gabungkan sebab dan akibat dengan connector yang tepat.",
        "The data is inconsistent. The report cannot be finalized.",
        ["The data is inconsistent.", "The report cannot be finalized."],
        "The data is inconsistent; therefore, the report cannot be finalized.",
        "Therefore menunjukkan akibat dari data yang tidak konsisten.",
        "Cause; therefore, result",
        "Tentukan dulu hubungan ide: sebab atau akibat.",
        "BA sering menjelaskan impact dari masalah data.",
        "intermediate",
        "connector_logic",
    ),
    _builder_item(
        "arrange_intermediate_modifier_1",
        "intermediate",
        "arrange_words",
        "gerund_vs_main_verb",
        "Arrange modifier phrase",
        "Susun kalimat dengan modifier phrase.",
        "must clarify priorities / working with stakeholders / The analyst",
        ["must clarify priorities", "working with stakeholders", "The analyst"],
        "The analyst working with stakeholders must clarify priorities.",
        "working with stakeholders menjelaskan analyst, bukan main verb.",
        "Subject + modifier phrase + modal + verb + object",
        "Jangan menganggap kata -ing sebagai main verb.",
        "Menjelaskan BA yang sedang bekerja dengan stakeholder.",
        "intermediate",
        "gerund_vs_main_verb",
    ),
    _builder_item(
        "arrange_intermediate_modifier_2",
        "intermediate",
        "arrange_words",
        "reduced_relative_clause",
        "Arrange reduced relative clause",
        "Susun kalimat dengan reduced relative clause.",
        "must be reviewed / created during the workshop / The requirement",
        ["must be reviewed", "created during the workshop", "The requirement"],
        "The requirement created during the workshop must be reviewed.",
        "created during the workshop menjelaskan requirement.",
        "Subject + reduced relative clause + modal passive",
        "Pisahkan noun utama dan phrase penjelasnya.",
        "Requirement hasil workshop perlu review.",
        "intermediate",
        "reduced_relative_clause",
    ),
    _builder_item(
        "complete_intermediate_passive_1",
        "intermediate",
        "complete_sentence",
        "passive_voice",
        "Complete passive voice",
        "Isi bagian kosong dengan bentuk passive yang tepat.",
        "The requirements are ___ by the analyst.",
        ["The requirements are", "___", "by the analyst"],
        "documented",
        "Passive voice membutuhkan be + V3.",
        "be + past participle",
        "Setelah are dalam passive, gunakan V3.",
        "Dipakai untuk process documentation.",
        "intermediate",
        "passive_voice",
    ),
    _builder_item(
        "complete_intermediate_passive_2",
        "intermediate",
        "complete_sentence",
        "passive_voice",
        "Complete expected passive",
        "Isi bagian kosong dengan kata yang tepat.",
        "The solution is expected to ___ traceability.",
        ["The solution is expected to", "___", "traceability"],
        "improve",
        "Expected to diikuti base verb improve.",
        "be expected to + base verb",
        "Setelah to dalam infinitive, gunakan verb dasar.",
        "Kalimat ini sering muncul dalam benefit statement.",
        "intermediate",
        "passive_voice",
    ),
    _builder_item(
        "fix_order_intermediate_connector_1",
        "intermediate",
        "fix_word_order",
        "connector_logic",
        "Fix connector order",
        "Perbaiki urutan kalimat dengan connector.",
        "It is too complex although the workflow is useful.",
        ["It is too complex", "although", "the workflow is useful"],
        "Although the workflow is useful, it is too complex.",
        "Although clause dapat diletakkan di awal untuk membuat kontras jelas.",
        "Although + clause, main clause",
        "Jika although di awal, pisahkan dengan koma.",
        "Membantu menjelaskan batasan proses.",
        "intermediate",
        "connector_logic",
    ),
    _builder_item(
        "fix_order_intermediate_connector_2",
        "intermediate",
        "fix_word_order",
        "connector_logic",
        "Fix result connector",
        "Perbaiki urutan sebab-akibat.",
        "Therefore the report cannot be finalized the data is inconsistent.",
        ["therefore", "the report cannot be finalized", "the data is inconsistent"],
        "The data is inconsistent; therefore, the report cannot be finalized.",
        "Sebab muncul dulu, lalu therefore untuk akibat.",
        "Cause; therefore, result",
        "Cari mana penyebab dan mana akibat.",
        "Dipakai untuk menjelaskan impact analysis.",
        "intermediate",
        "connector_logic",
    ),
    _builder_item(
        "rewrite_advanced_formal_1",
        "advanced_preview",
        "rewrite_formal_ba_sentence",
        "formal_ba_writing",
        "Rewrite formal BA sentence",
        "Tulis ulang kalimat informal menjadi kalimat BA yang lebih formal.",
        "The system helps users make reports faster.",
        ["The system helps users make reports faster."],
        "The system helps users generate reports more efficiently.",
        "generate reports dan more efficiently terdengar lebih formal daripada make reports faster.",
        "formal verb + professional adverb",
        "Ganti kata umum dengan kata profesional yang tetap jelas.",
        "Cocok untuk benefit statement dalam dokumen BA.",
        "advanced_preview",
        "formal_ba_writing",
        required_keywords=["system", "users", "generate", "reports", "efficiently"],
    ),
    _builder_item(
        "rewrite_advanced_formal_2",
        "advanced_preview",
        "rewrite_formal_ba_sentence",
        "formal_ba_writing",
        "Rewrite stakeholder problem",
        "Tulis ulang menjadi kalimat problem statement yang formal.",
        "People wait too long for approvals.",
        ["People wait too long for approvals."],
        "Stakeholders experience delays in the approval workflow.",
        "Stakeholders dan approval workflow lebih spesifik untuk konteks BA.",
        "formal noun phrase + precise BA term",
        "Gunakan istilah BA yang spesifik.",
        "Cocok untuk problem statement.",
        "advanced_preview",
        "formal_ba_writing",
        required_keywords=["stakeholders", "delays", "approval", "workflow"],
    ),
    _builder_item(
        "rewrite_advanced_formal_3",
        "advanced_preview",
        "rewrite_formal_ba_sentence",
        "formal_ba_writing",
        "Rewrite data issue",
        "Tulis ulang menjadi kalimat formal.",
        "The data is messy.",
        ["The data is messy."],
        "The data is inconsistent and requires validation.",
        "Inconsistent dan requires validation lebih formal dan actionable.",
        "precise adjective + action requirement",
        "Jelaskan masalah dan tindakan yang dibutuhkan.",
        "Cocok untuk data quality issue.",
        "advanced_preview",
        "formal_ba_writing",
        required_keywords=["data", "inconsistent", "requires", "validation"],
    ),
    _builder_item(
        "rewrite_advanced_formal_4",
        "advanced_preview",
        "rewrite_formal_ba_sentence",
        "formal_ba_writing",
        "Rewrite vague requirement",
        "Tulis ulang kalimat informal menjadi requirement statement.",
        "The feature should be easy to use.",
        ["The feature should be easy to use."],
        "The feature should be intuitive for end users.",
        "Intuitive for end users lebih formal dan jelas daripada easy to use.",
        "modal + be + professional adjective",
        "Gunakan adjective profesional yang tetap mudah dipahami.",
        "Cocok untuk usability requirement.",
        "advanced_preview",
        "formal_ba_writing",
        required_keywords=["feature", "intuitive", "end", "users"],
    ),
    _builder_item(
        "combine_advanced_formal_1",
        "advanced_preview",
        "combine_sentences",
        "nominalization",
        "Combine formal benefit sentence",
        "Gabungkan dua kalimat menjadi kalimat BA formal.",
        "The system records changes. The system improves traceability.",
        ["The system records changes.", "The system improves traceability."],
        "The implementation of the system improves traceability by recording changes.",
        "Nominalization implementation membuat kalimat lebih formal.",
        "nominalization + by + gerund phrase",
        "Gunakan by + -ing untuk menjelaskan cara.",
        "Cocok untuk benefit statement.",
        "advanced_preview",
        "nominalization",
        required_keywords=["implementation", "system", "improves", "traceability", "recording", "changes"],
    ),
    _builder_item(
        "combine_advanced_formal_2",
        "advanced_preview",
        "combine_sentences",
        "formal_ba_writing",
        "Combine formal recommendation",
        "Gabungkan dua kalimat menjadi recommendation formal.",
        "The workflow is slow. The team should automate approvals.",
        ["The workflow is slow.", "The team should automate approvals."],
        "Because the workflow is slow, the team should automate approvals.",
        "Because menjelaskan alasan rekomendasi.",
        "Because + reason, recommendation",
        "Tentukan alasan dulu, lalu rekomendasi.",
        "Cocok untuk recommendation section.",
        "advanced_preview",
        "formal_ba_writing",
        required_keywords=["workflow", "slow", "team", "should", "automate", "approvals"],
    ),
]


def get_sentence_builder_levels() -> list[dict[str, Any]]:
    return deepcopy(SENTENCE_BUILDER_LEVELS)


def get_sentence_builder_items(level: str | None = None, mode: str | None = None) -> list[dict[str, Any]]:
    normalized_level = level.strip().lower() if level else None
    normalized_mode = mode.strip().lower() if mode else None
    items = [
        item
        for item in SENTENCE_BUILDER_ITEMS
        if (not normalized_level or item["level"] == normalized_level)
        and (not normalized_mode or item["mode"] == normalized_mode)
    ]
    return deepcopy(items)


def get_sentence_builder_item(item_id: str) -> dict[str, Any] | None:
    for item in SENTENCE_BUILDER_ITEMS:
        if item["id"] == item_id:
            return deepcopy(item)
    return None


def submit_sentence_builder(payload: dict) -> dict[str, Any]:
    level = payload.get("level")
    mode = payload.get("mode")
    items = get_sentence_builder_items(level=level, mode=mode)
    if not items:
        items = get_sentence_builder_items()
    result = score_sentence_builder_answers(payload.get("answers") or {}, items)
    recommendation = get_sentence_builder_recommendation(result["score"], result["mistakes"])
    activity_id = f"{level}_{mode}" if level and mode else "mixed_sentence_builder"
    attempt_update = save_grammar_attempt(
        {
            "user_id": payload.get("user_id") or "default-user",
            "topic_id": recommendation["review_topic_id"],
            "activity_type": "grammar_sentence_builder",
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


def normalize_sentence_answer(answer: str) -> str:
    normalized = str(answer or "").strip().lower()
    normalized = re.sub(r"[.?!]+$", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized


def score_sentence_builder_answers(answers: dict, items: list[dict[str, Any]]) -> dict[str, Any]:
    details = []
    for item in items:
        if item["id"] not in answers:
            continue
        user_answer = str(answers.get(item["id"], ""))
        item_score = _score_one_answer(user_answer, item)
        is_correct = item_score >= 100
        details.append(
            {
                "item_id": item["id"],
                "is_correct": is_correct,
                "partial_score": item_score,
                "user_answer": user_answer,
                "expected_answer": item["expected_answer"],
                "explanation_id": item["explanation_id"],
                "grammar_rule_id": item["grammar_rule_id"],
                "related_topic_id": item["related_topic_id"],
                "mode": item["mode"],
                "level": item["level"],
            }
        )
    total = len(details)
    score = round(sum(item["partial_score"] for item in details) / total, 1) if total else 0
    correct = len([item for item in details if item["partial_score"] >= 70])
    mistakes = [item for item in details if item["partial_score"] < 70]
    return {
        "score": score,
        "max_score": 100,
        "correct_count": correct,
        "total_questions": total,
        "is_passed": score >= 70,
        "details": details,
        "mistakes": mistakes,
    }


def get_sentence_builder_recommendation(score: float, mistakes: list) -> dict[str, Any]:
    review_topic_id = mistakes[0]["related_topic_id"] if mistakes else "formal_ba_writing"
    if score >= 85:
        return {
            "next_action": "Lanjutkan ke level atau mode Sentence Builder berikutnya.",
            "review_topic_id": review_topic_id,
            "mentor_message": "Bagus. Kamu sudah mulai bisa membangun kalimat BA yang rapi dan jelas.",
        }
    if score >= 70:
        return {
            "next_action": "Ulangi satu item yang belum sempurna, lalu coba mode yang lebih sulit.",
            "review_topic_id": review_topic_id,
            "mentor_message": "Progress bagus. Sekarang perhatikan word order dan pilihan kata formal.",
        }
    return {
        "next_action": "Ulangi pola dasar: Subject + Verb + Object sebelum mencoba kalimat panjang.",
        "review_topic_id": review_topic_id,
        "mentor_message": "Tidak apa-apa. Bangun kalimat pelan-pelan dari subject, lalu verb, lalu object.",
    }


def _score_one_answer(user_answer: str, item: dict[str, Any]) -> float:
    normalized_user = normalize_sentence_answer(user_answer)
    expected_answers = [item["expected_answer"], *item.get("acceptable_answers", [])]
    normalized_expected = [normalize_sentence_answer(answer) for answer in expected_answers]
    if normalized_user in normalized_expected:
        return 100
    if item["mode"] == "rewrite_formal_ba_sentence" or item.get("required_keywords"):
        keywords = item.get("required_keywords", [])
        if not keywords:
            return 0
        matched = [keyword for keyword in keywords if keyword.lower() in normalized_user]
        return round((len(matched) / len(keywords)) * 100, 1)
    return 0
