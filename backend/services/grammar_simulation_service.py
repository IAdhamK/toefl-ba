from __future__ import annotations

import re
import time
from collections import defaultdict
from copy import deepcopy
from typing import Any

from backend.database import now_iso
from backend.services.grammar_journey_service import get_grammar_journey, save_grammar_attempt
from backend.services.journey_service import get_default_user_id


SIMULATION_SESSIONS: dict[str, dict[str, Any]] = {}
SIMULATION_RESULTS: dict[str, dict[str, Any]] = {}
SIMULATION_HISTORY: dict[str, list[dict[str, Any]]] = defaultdict(list)

SIMULATION_MODES = {
    "short": {
        "id": "short",
        "title": "Short Grammar Simulation",
        "duration_minutes": 10,
        "question_count": 10,
        "description": "Quick mixed grammar review.",
    },
    "medium": {
        "id": "medium",
        "title": "Medium Grammar Simulation",
        "duration_minutes": 20,
        "question_count": 20,
        "description": "Mixed practice for Basic, Intermediate, Advanced, and correction patterns.",
    },
    "full": {
        "id": "full",
        "title": "Full Grammar Readiness Simulation",
        "duration_minutes": 40,
        "question_count": 40,
        "description": "Complete Grammar readiness test.",
    },
}


def q(
    qid: str,
    level: str,
    question_type: str,
    topic_id: str,
    instruction: str,
    sentence: str,
    question: str,
    options: list[str],
    correct: str,
    explanation: str,
    skill_area: str,
    trap: str = "",
    keywords: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "id": qid,
        "level": level,
        "question_type": question_type,
        "topic_id": topic_id,
        "instruction_id": instruction,
        "sentence": sentence,
        "question": question,
        "options": options,
        "correct_answer": correct,
        "explanation_id": explanation,
        "difficulty": level,
        "grammar_trap": trap,
        "ba_context_note": "Kalimat ini umum dalam konteks TOEFL + Business Analyst.",
        "skill_area": skill_area,
        "required_keywords": keywords or [],
    }


BASIC_QUESTIONS = [
    q("grammar_sim_subject_1", "basic", "identify_subject", "subject_verb", "Pilih subject.", "A business analyst must elicit requirements.", "Which part is the subject?", ["A business analyst", "must elicit", "requirements", "analyst must"], "A business analyst", "Subject adalah pelaku utama.", "subject_detection"),
    q("grammar_sim_verb_1", "basic", "identify_main_verb", "modal_verb", "Pilih main verb.", "The analyst should document the decision.", "Which one is the main verb?", ["The analyst", "should document", "decision", "the"], "should document", "Setelah modal should, document adalah verb utama.", "modal_verb"),
    q("grammar_sim_modal_1", "basic", "sentence_completion", "modal_verb", "Lengkapi kalimat.", "The system must ___ flexible for all users.", "Which word completes the sentence?", ["be", "is", "being", "to be"], "be", "Setelah must dan sebelum adjective, gunakan be.", "modal_verb"),
    q("grammar_sim_object_1", "basic", "identify_subject", "object_complement", "Pilih object.", "The analyst clarifies the scope.", "Which part is the object?", ["The analyst", "clarifies", "the scope", "analyst clarifies"], "the scope", "Object menerima aksi clarifies.", "object_complement"),
    q("grammar_sim_pattern_1", "basic", "choose_correct_sentence", "simple_sentence_pattern", "Pilih kalimat yang benar.", "Choose the correct sentence.", "Which sentence is correct?", ["The analyst clarifies the requirement.", "Clarifies the analyst requirement.", "The analyst the requirement clarifies.", "Requirement clarifies analyst the."], "The analyst clarifies the requirement.", "Pola dasar: Subject + Verb + Object.", "word_order"),
    q("grammar_sim_tense_1", "basic", "choose_correct_sentence", "simple_tense", "Pilih simple present yang benar.", "The system ___ reports every week.", "Which verb is correct?", ["generates", "generate", "generated", "generating"], "generates", "The system adalah singular, jadi generates.", "simple_tense"),
    q("grammar_sim_prep_1", "basic", "choose_correct_sentence", "prepositional_phrase", "Pilih preposition yang benar.", "The requirement must align ___ business strategy.", "Which preposition is correct?", ["with", "to", "for", "by"], "with", "Phrase yang umum adalah align with.", "prepositional_phrase"),
    q("grammar_sim_article_1", "basic", "choose_correct_sentence", "parts_of_speech", "Pilih article yang tepat.", "The analyst identified ___ issue.", "Which article is correct?", ["an", "a", "thee", "no article"], "an", "Issue diawali bunyi vokal, jadi an.", "parts_of_speech"),
    q("grammar_sim_modal_2", "basic", "choose_correct_sentence", "modal_verb", "Pilih pola modal yang benar.", "Choose the correct modal pattern.", "Which sentence is correct?", ["The analyst must clarify the scope.", "The analyst must clarifies the scope.", "The analyst must to clarify the scope.", "The analyst must clarified the scope."], "The analyst must clarify the scope.", "Modal diikuti base verb.", "modal_verb"),
    q("grammar_sim_subject_2", "basic", "identify_subject", "subject_verb", "Pilih subject.", "Requirements are unclear.", "Which part is the subject?", ["Requirements", "are", "unclear", "are unclear"], "Requirements", "Requirements adalah subject plural.", "subject_detection"),
]

INTERMEDIATE_QUESTIONS = [
    q("grammar_sim_main_verb_1", "intermediate", "identify_main_verb", "gerund_vs_main_verb", "Pilih main verb.", "The analyst working with stakeholders must clarify priorities.", "Which one is the main verb?", ["working", "must clarify", "stakeholders", "priorities"], "must clarify", "\"working\" menjelaskan analyst. Main verb adalah \"must clarify\".", "main_verb_detection", "User may think working is the main verb."),
    q("grammar_sim_modifier_1", "intermediate", "identify_modifier_phrase", "gerund_vs_main_verb", "Pilih modifier phrase.", "The analyst working with stakeholders must clarify priorities.", "Which phrase describes the analyst?", ["working with stakeholders", "must clarify", "priorities", "The analyst"], "working with stakeholders", "Phrase -ing menjelaskan analyst.", "modifier_phrase"),
    q("grammar_sim_reduced_1", "intermediate", "identify_modifier_phrase", "reduced_relative_clause", "Pilih reduced relative clause.", "The requirement created during the workshop must be reviewed.", "Which phrase modifies requirement?", ["created during the workshop", "must be reviewed", "The requirement", "during"], "created during the workshop", "Created during the workshop menjelaskan requirement.", "reduced_relative_clause"),
    q("grammar_sim_passive_1", "intermediate", "passive_voice", "passive_voice", "Pilih passive voice yang benar.", "The requirements are ___ by the analyst.", "Which word is correct?", ["documented", "document", "documenting", "documents"], "documented", "Passive voice memakai are + V3.", "passive_voice"),
    q("grammar_sim_parallel_1", "intermediate", "parallel_structure", "parallel_structure", "Pilih parallel structure.", "The analyst must document requirements and ___ alignment.", "Which word keeps the structure parallel?", ["ensure", "ensuring", "ensures", "to ensure"], "ensure", "Setelah must, dua verb sejajar: document dan ensure.", "parallel_structure"),
    q("grammar_sim_connector_1", "intermediate", "connector_logic", "connector_logic", "Pilih connector yang tepat.", "The data is inconsistent; ___, the report cannot be finalized.", "Which connector fits?", ["therefore", "although", "however", "meanwhile"], "therefore", "Therefore menunjukkan akibat.", "connector_logic"),
    q("grammar_sim_relative_1", "intermediate", "identify_modifier_phrase", "relative_clause", "Pilih relative clause.", "Stakeholders who use the system provide feedback.", "Which part is the relative clause?", ["who use the system", "provide feedback", "Stakeholders", "the system"], "who use the system", "Who use the system menjelaskan stakeholders.", "relative_clause"),
    q("grammar_sim_infinitive_1", "intermediate", "identify_modifier_phrase", "infinitive_phrase", "Pilih infinitive phrase.", "The team needs data to validate assumptions.", "Which phrase shows purpose?", ["to validate assumptions", "needs data", "The team", "assumptions"], "to validate assumptions", "to validate assumptions menjelaskan tujuan.", "infinitive_phrase"),
    q("grammar_sim_passive_2", "intermediate", "choose_correct_sentence", "passive_voice", "Pilih kalimat passive yang benar.", "Choose the correct passive sentence.", "Which sentence is correct?", ["The data is processed by the system.", "The data is process by the system.", "The data processed by is system.", "The data are process by system."], "The data is processed by the system.", "Passive voice: is + V3.", "passive_voice"),
    q("grammar_sim_connector_2", "intermediate", "connector_logic", "connector_logic", "Pilih kalimat connector yang benar.", "Choose the logical sentence.", "Which sentence is correct?", ["Although the workflow is useful, it is too complex.", "Although the workflow is useful, but it is too complex.", "Because the workflow is useful, but complex.", "Workflow although useful complex."], "Although the workflow is useful, it is too complex.", "Although tidak perlu but.", "connector_logic"),
    q("grammar_sim_parallel_2", "intermediate", "parallel_structure", "parallel_structure", "Pilih daftar verb sejajar.", "The solution should improve reporting, ___ errors, and support decisions.", "Which word is parallel?", ["reduce", "reducing", "reduced", "to reduce"], "reduce", "Improve, reduce, support adalah verb sejajar.", "parallel_structure"),
    q("grammar_sim_main_verb_2", "intermediate", "identify_main_verb", "gerund_vs_main_verb", "Pilih main verb.", "Operating in a complex environment, the analyst must align requirements.", "Which one is the main verb?", ["Operating", "must align", "environment", "requirements"], "must align", "Operating adalah phrase pembuka, bukan main verb.", "main_verb_detection"),
    q("grammar_sim_reference_1", "intermediate", "grammar_meaning", "relative_clause", "Pahami makna kalimat.", "The team validates requirements that affect reporting.", "What does that affect reporting describe?", ["requirements", "team", "validates", "reporting only"], "requirements", "That clause menjelaskan requirements.", "relative_clause"),
    q("grammar_sim_completion_1", "intermediate", "sentence_completion", "passive_voice", "Lengkapi kalimat.", "The decision was ___ after stakeholder review.", "Which word is correct?", ["validated", "validate", "validating", "validates"], "validated", "Was + V3 membentuk passive.", "passive_voice"),
]

ADVANCED_QUESTIONS = [
    q("grammar_sim_nominal_1", "advanced", "nominalization", "nominalization", "Pilih nominalization.", "The implementation of the system improves traceability.", "Which word is nominalization?", ["implementation", "system", "improves", "traceability"], "implementation", "Implementation berasal dari implement.", "nominalization"),
    q("grammar_sim_hedging_1", "advanced", "grammar_meaning", "hedging_language", "Pilih hedging phrase.", "The delay may indicate a bottleneck.", "Which phrase shows caution?", ["may indicate", "delay", "bottleneck", "The"], "may indicate", "May indicate tidak terlalu absolut.", "hedging_language"),
    q("grammar_sim_inversion_1", "advanced", "grammar_meaning", "inversion", "Pahami inversion.", "Only after the requirements are validated can the team proceed.", "What must happen first?", ["requirements are validated", "the team proceeds immediately", "development starts first", "training ends"], "requirements are validated", "Only after menunjukkan prasyarat.", "inversion"),
    q("grammar_sim_conditional_1", "advanced", "grammar_meaning", "conditional_sentence", "Pilih condition.", "If the workflow is not simplified, users may continue to experience delays.", "Which part is the condition?", ["If the workflow is not simplified", "users may continue", "experience delays", "may continue"], "If the workflow is not simplified", "If clause adalah kondisi.", "conditional_sentence"),
    q("grammar_sim_academic_1", "advanced", "connector_logic", "academic_connectors", "Pilih makna connector.", "Consequently, the organization can reduce ambiguity.", "What does consequently show?", ["result", "contrast", "example", "time"], "result", "Consequently menunjukkan akibat.", "academic_connectors"),
    q("grammar_sim_formal_1", "advanced", "formal_ba_writing", "formal_ba_writing", "Pilih kalimat formal.", "Choose the formal BA sentence.", "Which sentence is best?", ["The system enables users to generate reports more efficiently.", "The system makes reports fast.", "People do reports quick.", "Reports become nice."], "The system enables users to generate reports more efficiently.", "Enables users to generate reports more efficiently lebih formal.", "formal_ba_writing"),
    q("grammar_sim_nominal_2", "advanced", "grammar_meaning", "nominalization", "Pilih versi sederhana.", "The validation of requirements reduces ambiguity.", "Which simpler version matches?", ["Validating requirements reduces ambiguity.", "Requirements create ambiguity.", "Validation is not needed.", "Ambiguity validates requirements."], "Validating requirements reduces ambiguity.", "Validation of requirements berarti validating requirements.", "nominalization"),
    q("grammar_sim_hedging_2", "advanced", "grammar_meaning", "hedging_language", "Pilih klaim hati-hati.", "Choose the cautious sentence.", "Which sentence is cautious?", ["The solution may address several issues.", "The solution fixes everything.", "The solution always works.", "The solution proves success."], "The solution may address several issues.", "May address lebih hati-hati.", "hedging_language"),
]

ERROR_CORRECTION_QUESTIONS = [
    q("grammar_sim_error_1", "mixed", "error_correction", "modal_verb", "Pilih koreksi yang benar.", "The system must flexible for all users.", "Which sentence is correct?", ["The system must be flexible for all users.", "The system must flexible for all users.", "The system must is flexible for all users.", "The system must being flexible."], "The system must be flexible for all users.", "Modal + be + adjective.", "error_correction"),
    q("grammar_sim_error_2", "mixed", "error_correction", "passive_voice", "Pilih koreksi yang benar.", "The data is process by the system.", "Which sentence is correct?", ["The data is processed by the system.", "The data is process by the system.", "The data are process by system.", "The data processing by the system."], "The data is processed by the system.", "Passive voice: is + V3.", "error_correction"),
    q("grammar_sim_error_3", "mixed", "error_correction", "parallel_structure", "Pilih koreksi yang benar.", "The analyst must document requirements and ensuring alignment.", "Which sentence is correct?", ["The analyst must document requirements and ensure alignment.", "The analyst must documenting requirements and ensuring alignment.", "The analyst must document requirements and ensures alignment.", "The analyst document and ensuring alignment."], "The analyst must document requirements and ensure alignment.", "Document dan ensure sejajar setelah must.", "error_correction"),
    q("grammar_sim_error_4", "mixed", "error_correction", "connector_logic", "Pilih koreksi yang benar.", "Although the workflow is useful, but it is too complex.", "Which sentence is correct?", ["Although the workflow is useful, it is too complex.", "Although the workflow is useful, but it is too complex.", "The workflow although useful but complex.", "Although useful, but workflow complex."], "Although the workflow is useful, it is too complex.", "Although tidak perlu but.", "error_correction"),
]

BUILDER_QUESTIONS = [
    q("grammar_sim_builder_1", "mixed", "sentence_builder", "modal_verb", "Susun kalimat.", "must / requirements / elicit / A business analyst", "Write the correct sentence.", [], "A business analyst must elicit requirements.", "Subject + modal + verb + object.", "sentence_builder", keywords=["business", "analyst", "must", "elicit", "requirements"]),
    q("grammar_sim_builder_2", "mixed", "sentence_builder", "simple_sentence_pattern", "Perbaiki word order.", "Must the system generate reports automatically.", "Write the correct statement.", [], "The system must generate reports automatically.", "Subject muncul sebelum modal.", "sentence_builder", keywords=["system", "must", "generate", "reports", "automatically"]),
    q("grammar_sim_formal_write_1", "mixed", "formal_ba_writing", "formal_ba_writing", "Rewrite formal BA sentence.", "The system helps users make reports faster.", "Write a more formal sentence.", [], "The system enables users to generate reports more efficiently.", "Generate reports more efficiently lebih formal.", "formal_ba_writing", keywords=["system", "users", "generate", "reports", "efficiently"]),
    q("grammar_sim_builder_3", "mixed", "sentence_builder", "parallel_structure", "Gabungkan kalimat.", "The analyst interviews users. The analyst documents requirements.", "Write one combined sentence.", [], "The analyst interviews users and documents requirements.", "Dua aksi dengan subject sama bisa digabung.", "sentence_builder", keywords=["analyst", "interviews", "users", "documents", "requirements"]),
]


def get_simulation_modes() -> list[dict[str, Any]]:
    return list(SIMULATION_MODES.values())


def start_grammar_simulation(payload: dict) -> dict[str, Any]:
    user_id = get_default_user_id(payload.get("user_id") or "default-user")
    mode = (payload.get("mode") or "short").strip().lower()
    config = SIMULATION_MODES.get(mode, SIMULATION_MODES["short"])
    session_id = f"grammar-sim-{int(time.time() * 1000)}"
    questions = build_simulation_questions(config["id"])
    session = {
        "session_id": session_id,
        "user_id": user_id,
        "mode": config["id"],
        "title": config["title"],
        "duration_minutes": config["duration_minutes"],
        "question_count": len(questions),
        "started_at": now_iso(),
        "instructions_id": "Jawab semua soal Grammar. Bantuan ID tidak ditampilkan saat simulasi.",
        "help_policy": {
            "bantuan_id_allowed": False,
            "show_explanation_during_test": False,
            "show_explanation_after_submit": True,
        },
        "questions": questions,
    }
    SIMULATION_SESSIONS[session_id] = session
    return {"session": deepcopy(session)}


def submit_grammar_simulation(payload: dict) -> dict[str, Any]:
    user_id = get_default_user_id(payload.get("user_id") or "default-user")
    session_id = payload.get("session_id")
    session = payload.get("session") or SIMULATION_SESSIONS.get(session_id)
    if not session:
        session = start_grammar_simulation({"user_id": user_id, "mode": payload.get("mode") or "short"})["session"]
        session_id = session["session_id"]
    result = score_simulation_answers(session, payload.get("answers") or {})
    result.update(
        {
            "session_id": session["session_id"],
            "user_id": user_id,
            "mode": session["mode"],
            "time_spent_seconds": int(payload.get("time_spent_seconds") or 0),
        }
    )
    recommendation = build_simulation_recommendation(result)
    result["recommended_next_practice"] = recommendation["next_action"]
    result["recommendation"] = recommendation
    mistakes = [item for item in result["answer_review_summary"] if not item["is_correct"]]
    attempt_update = save_grammar_attempt(
        {
            "user_id": user_id,
            "topic_id": recommendation["review_topic_id"],
            "activity_type": "grammar_simulation",
            "activity_id": session["session_id"],
            "score": result["total_score"],
            "max_score": 100,
            "mistakes": mistakes,
            "feedback": recommendation["next_action"],
        }
    )
    result["grammar_journey"] = attempt_update["grammar_journey"]
    SIMULATION_RESULTS[session["session_id"]] = result
    SIMULATION_HISTORY[user_id].insert(0, _history_item(result))
    return {"result": deepcopy(result)}


def get_grammar_simulation_result(session_id: str, user_id: str | None = None) -> dict[str, Any]:
    result = SIMULATION_RESULTS.get(session_id)
    if not result:
        return {"result": {}}
    if user_id and result.get("user_id") != user_id:
        return {"result": {}}
    return {"result": deepcopy(result)}


def get_grammar_simulation_history(user_id: str | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id or "default-user")
    return {"history": deepcopy(SIMULATION_HISTORY.get(user_id, []))}


def build_simulation_questions(mode: str) -> list[dict[str, Any]]:
    if mode == "medium":
        return deepcopy(BASIC_QUESTIONS[:6] + INTERMEDIATE_QUESTIONS[:8] + ADVANCED_QUESTIONS[:4] + ERROR_CORRECTION_QUESTIONS[:1] + BUILDER_QUESTIONS[:1])
    if mode == "full":
        return deepcopy(BASIC_QUESTIONS[:10] + INTERMEDIATE_QUESTIONS[:14] + ADVANCED_QUESTIONS[:8] + ERROR_CORRECTION_QUESTIONS[:4] + BUILDER_QUESTIONS[:4])
    return deepcopy(BASIC_QUESTIONS[:4] + INTERMEDIATE_QUESTIONS[:4] + ADVANCED_QUESTIONS[:2])


def score_simulation_answers(session: dict, answers: dict) -> dict[str, Any]:
    details = []
    for question in session.get("questions", []):
        user_answer = answers.get(question["id"], "")
        points = _score_question(question, user_answer)
        is_correct = points >= 100
        details.append(
            {
                "question_id": question["id"],
                "is_correct": is_correct,
                "partial_score": points,
                "user_answer": user_answer,
                "correct_answer": question["correct_answer"],
                "explanation_id": question["explanation_id"],
                "topic_id": question["topic_id"],
                "skill_area": question["skill_area"],
                "level": question["level"],
            }
        )
    total = len(details) or 1
    total_score = round(sum(item["partial_score"] for item in details) / total, 1)
    correct_count = len([item for item in details if item["partial_score"] >= 70])
    return {
        "total_score": total_score,
        "max_score": 100,
        "correct_count": correct_count,
        "total_questions": len(details),
        "level_breakdown": calculate_level_breakdown(details),
        "subskill_breakdown": calculate_subskill_breakdown(details),
        "answer_review_summary": details,
    }


def calculate_subskill_breakdown(details: list[dict]) -> list[dict[str, Any]]:
    return _breakdown(details, "skill_area", "skill_area")


def calculate_level_breakdown(details: list[dict]) -> list[dict[str, Any]]:
    return _breakdown(details, "level", "level")


def build_simulation_recommendation(result: dict) -> dict[str, Any]:
    weak = min(result.get("subskill_breakdown") or [], key=lambda item: item["score"], default={"skill_area": "main_verb_detection"})
    skill_area = weak.get("skill_area", "main_verb_detection")
    mapping = {
        "main_verb_detection": ("gerund_vs_main_verb", "/api/grammar/trainer/intermediate/gerund_vs_main_verb", "Ulangi Gerund vs Main Verb untuk menemukan main verb."),
        "passive_voice": ("passive_voice", "/api/grammar/trainer/intermediate/passive_voice", "Ulangi passive voice: be + V3."),
        "modal_verb": ("modal_verb", "/api/grammar/trainer/basic/modal_verb", "Ulangi pola modal + base verb."),
        "formal_ba_writing": ("formal_ba_writing", "/api/grammar/advanced/topics/formal_ba_writing", "Latihan rewrite formal BA writing."),
        "error_correction": ("modal_verb", "/api/grammar/error-correction", "Ulangi Error Correction untuk pola grammar umum."),
        "sentence_builder": ("simple_sentence_pattern", "/api/grammar/sentence-builder", "Latihan Sentence Builder untuk word order."),
        "connector_logic": ("connector_logic", "/api/grammar/trainer/intermediate/connector_logic", "Ulangi connector logic."),
        "nominalization": ("nominalization", "/api/grammar/advanced/topics/nominalization", "Review nominalization."),
    }
    topic_id, endpoint, action = mapping.get(skill_area, ("subject_verb", "/api/grammar/trainer/basic/subject_verb", "Ulangi Subject and Verb foundation."))
    return {
        "weakest_skill_area": skill_area,
        "review_topic_id": topic_id,
        "target_endpoint": endpoint,
        "next_action": action,
        "mentor_message": f"Area terlemah simulasi: {skill_area}. {action}",
    }


def normalize_simulation_answer(answer: str) -> str:
    normalized = str(answer or "").strip().lower()
    normalized = re.sub(r"[.?!]+$", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized


def _score_question(question: dict, user_answer: str) -> float:
    if normalize_simulation_answer(user_answer) == normalize_simulation_answer(question["correct_answer"]):
        return 100
    keywords = question.get("required_keywords") or []
    if question["question_type"] in {"sentence_builder", "formal_ba_writing"} and keywords:
        normalized = normalize_simulation_answer(user_answer)
        matched = [keyword for keyword in keywords if keyword.lower() in normalized]
        return round((len(matched) / len(keywords)) * 100, 1)
    return 0


def _breakdown(details: list[dict], key: str, output_key: str) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for detail in details:
        grouped[detail.get(key, "unknown")].append(detail)
    items = []
    for name, rows in grouped.items():
        score = round(sum(row["partial_score"] for row in rows) / len(rows), 1)
        correct = len([row for row in rows if row["partial_score"] >= 70])
        items.append(
            {
                output_key: name,
                "score": score,
                "correct_count": correct,
                "total_questions": len(rows),
                "status": "on_track" if score >= 75 else "needs_practice",
            }
        )
    return items


def _history_item(result: dict) -> dict[str, Any]:
    return {
        "session_id": result["session_id"],
        "mode": result["mode"],
        "total_score": result["total_score"],
        "correct_count": result["correct_count"],
        "total_questions": result["total_questions"],
        "recommended_next_practice": result["recommended_next_practice"],
    }
