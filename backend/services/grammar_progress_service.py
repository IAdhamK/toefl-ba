from __future__ import annotations

from collections import defaultdict
from typing import Any

from backend.database import decode_json, get_connection
from backend.services.grammar_error_service import get_error_categories
from backend.services.grammar_journey_service import get_grammar_journey
from backend.services.grammar_review_service import get_grammar_review
from backend.services.grammar_simulation_service import get_grammar_simulation_history
from backend.services.grammar_topic_service import get_grammar_topics
from backend.services.grammar_trainer_service import get_basic_trainer_topics, get_intermediate_trainer_topics
from backend.services.journey_service import get_default_user_id


DEFAULT_USER_ID = "default-user"

MODULE_ORDER = [
    "basic_trainer",
    "grammar_breakdown",
    "intermediate_trainer",
    "error_correction",
    "sentence_builder",
    "advanced_lab",
    "review",
    "simulation",
]

MODULE_DEFINITIONS = {
    "grammar_breakdown": {
        "module_id": "grammar_breakdown",
        "title": "Grammar Breakdown",
        "description": "Bedah kalimat untuk menemukan subject, main verb, phrase, clause, dan makna Bahasa Indonesia.",
        "target_score": 70,
        "section": "breakdown",
        "next_action": "Bedah 5 kalimat panjang agar terbiasa mencari inti kalimat.",
    },
    "basic_trainer": {
        "module_id": "basic_trainer",
        "title": "Basic Grammar Trainer",
        "description": "Latihan fondasi: parts of speech, subject, verb, object, modal, dan pola kalimat sederhana.",
        "target_score": 70,
        "section": "basic_trainer",
        "next_action": "Lanjutkan Basic Grammar Trainer dari topic yang belum selesai.",
    },
    "intermediate_trainer": {
        "module_id": "intermediate_trainer",
        "title": "Intermediate Grammar Trainer",
        "description": "Latihan kalimat panjang: gerund, relative clause, passive voice, connector, dan parallel structure.",
        "target_score": 70,
        "section": "intermediate_trainer",
        "next_action": "Latihan membedakan main verb dan phrase tambahan dalam kalimat panjang.",
    },
    "error_correction": {
        "module_id": "error_correction",
        "title": "Grammar Error Correction",
        "description": "Cari kesalahan grammar dan pilih corrected sentence yang benar.",
        "target_score": 70,
        "section": "error_correction",
        "next_action": "Ulangi error type yang masih sering salah.",
    },
    "sentence_builder": {
        "module_id": "sentence_builder",
        "title": "Grammar Sentence Builder",
        "description": "Susun kata, lengkapi kalimat, gabungkan kalimat, dan tulis ulang kalimat BA.",
        "target_score": 70,
        "section": "sentence_builder",
        "next_action": "Bangun kalimat sendiri dari pola grammar yang sudah dipelajari.",
    },
    "advanced_lab": {
        "module_id": "advanced_lab",
        "title": "Advanced Grammar Lab",
        "description": "Latihan grammar formal untuk TOEFL, akademik, dan Business Analyst writing.",
        "target_score": 70,
        "section": "advanced_lab",
        "next_action": "Latihan nominalization, hedging, connector akademik, dan formal BA writing.",
    },
    "review": {
        "module_id": "review",
        "title": "Grammar Review",
        "description": "Lihat kelemahan grammar, pola salah berulang, dan rekomendasi latihan ulang.",
        "target_score": 75,
        "section": "review",
        "next_action": "Buka Grammar Review untuk melihat area yang perlu diulang.",
    },
    "simulation": {
        "module_id": "simulation",
        "title": "Grammar Simulation",
        "description": "Uji kemampuan grammar melalui simulasi short, medium, atau full.",
        "target_score": 75,
        "section": "simulation",
        "next_action": "Kerjakan Full Grammar Simulation dan targetkan minimal 75%.",
    },
}

ACTIVITY_MODULE_MAP = {
    "deep_grammar_breakdown": "grammar_breakdown",
    "grammar_breakdown": "grammar_breakdown",
    "basic_grammar_trainer": "basic_trainer",
    "intermediate_grammar_trainer": "intermediate_trainer",
    "grammar_error_correction": "error_correction",
    "grammar_sentence_builder": "sentence_builder",
    "advanced_grammar_practice": "advanced_lab",
    "advanced_grammar_rewrite": "advanced_lab",
    "grammar_simulation": "simulation",
}


def get_grammar_module_progress(user_id: str | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    attempts = get_recent_grammar_module_attempts(user_id, limit=500)
    review = _safe_review(user_id)
    journey = _safe_journey(user_id)
    history = _safe_simulation_history(user_id)
    modules = [_build_module_progress(module_id, attempts, review, journey, history) for module_id in MODULE_ORDER]
    recommended = _choose_recommended_module(modules, journey, review)
    modules = [_mark_recommended(module, recommended["module_id"]) for module in modules]
    summary = get_grammar_progress_summary(user_id, modules=modules, journey=journey, recommended=recommended)
    finish_status = get_grammar_finish_status(user_id, modules=modules, history=history)
    learning_path = get_grammar_learning_path(user_id, modules=modules).get("learning_path", [])
    return {
        "summary": summary,
        "modules": modules,
        "learning_path": learning_path,
        "recommended_section": recommended,
        "finish_status": finish_status,
    }


def get_grammar_progress_summary(
    user_id: str | None = None,
    modules: list[dict[str, Any]] | None = None,
    journey: dict[str, Any] | None = None,
    recommended: dict[str, Any] | None = None,
) -> dict[str, Any]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    modules = modules if modules is not None else get_grammar_module_progress(user_id)["modules"]
    journey = journey or _safe_journey(user_id)
    recommended = recommended or _choose_recommended_module(modules, journey, _safe_review(user_id))
    completed_modules = len([module for module in modules if module["status"] == "completed"])
    overall_progress = round(sum(float(module["progress_percent"] or 0) for module in modules) / len(modules), 1) if modules else 0
    return {
        "overall_progress_percent": overall_progress,
        "grammar_level": journey.get("grammar_level", "Basic 1 - Sentence Foundation"),
        "grammar_score": round(float(journey.get("grammar_score") or 0), 1),
        "completed_modules": completed_modules,
        "total_modules": len(modules),
        "active_module": recommended.get("section", "basic_trainer"),
        "next_action": recommended.get("next_action", "Mulai dari Basic Grammar Trainer."),
        "finish_target": "Full Grammar Simulation minimal 75%",
    }


def get_grammar_learning_path(user_id: str | None = None, modules: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    modules = modules if modules is not None else get_grammar_module_progress(user_id)["modules"]
    path = []
    for index, module in enumerate(modules, start=1):
        path.append(
            {
                "step": index,
                **module,
            }
        )
    return {"learning_path": path}


def get_recommended_grammar_section(user_id: str | None = None) -> dict[str, Any]:
    progress = get_grammar_module_progress(user_id)
    return progress["recommended_section"]


def get_grammar_finish_status(
    user_id: str | None = None,
    modules: list[dict[str, Any]] | None = None,
    history: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    modules = modules if modules is not None else get_grammar_module_progress(user_id)["modules"]
    history = history if history is not None else _safe_simulation_history(user_id)
    full_scores = [float(item.get("total_score") or 0) for item in history if item.get("mode") == "full"]
    full_score = max(full_scores) if full_scores else 0
    simulation = next((module for module in modules if module["module_id"] == "simulation"), {})
    full_score = max(full_score, float(simulation.get("best_score") or 0) if simulation.get("status") == "completed" else 0)
    is_finished = full_score >= 75
    return {
        "is_finished": is_finished,
        "finish_rule": "Full Grammar Simulation minimal 75%",
        "full_simulation_score": round(full_score, 1),
        "message": (
            "Grammar Lab selesai. Pertahankan skor full simulation minimal 75%."
            if is_finished
            else "Belum finish. Ikuti rekomendasi berikutnya sampai siap full simulation minimal 75%."
        ),
    }


def get_recent_grammar_module_attempts(user_id: str | None = None, limit: int = 200) -> list[dict[str, Any]]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, activity_id, activity_type, score, max_score, accuracy,
                   mistakes_json, feedback, created_at
            FROM learning_attempts
            WHERE user_id = ? AND skill_type = 'grammar'
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
    attempts = []
    for row in rows:
        item = dict(row)
        item["module_id"] = map_activity_type_to_module(item.get("activity_type"))
        item["mistakes"] = decode_json(item.get("mistakes_json"), [])
        item["percent_score"] = round(float(item.get("accuracy") or _percent(item.get("score"), item.get("max_score"))), 1)
        attempts.append(item)
    return attempts


def map_activity_type_to_module(activity_type: str) -> str:
    return ACTIVITY_MODULE_MAP.get((activity_type or "").strip(), "")


def calculate_module_status(progress_percent: float, attempt_count: int, last_score: float | None = None) -> str:
    if attempt_count <= 0:
        return "not_started"
    if last_score is not None and last_score < 50:
        return "need_review"
    if progress_percent >= 100:
        return "completed"
    return "in_progress"


def _build_module_progress(
    module_id: str,
    attempts: list[dict[str, Any]],
    review: dict[str, Any],
    journey: dict[str, Any],
    history: list[dict[str, Any]],
) -> dict[str, Any]:
    module_attempts = [attempt for attempt in attempts if attempt.get("module_id") == module_id]
    if module_id == "review":
        return _review_module(review, attempts, journey)
    if module_id == "simulation":
        return _simulation_module(module_attempts, history)
    total_items = _module_total_items(module_id)
    completed_items = _completed_items_for_module(module_id, module_attempts, total_items)
    progress_percent = round((completed_items / max(total_items, 1)) * 100, 1)
    latest = module_attempts[0] if module_attempts else {}
    scores = [float(attempt.get("percent_score") or 0) for attempt in module_attempts]
    last_score = float(latest.get("percent_score") or 0) if latest else None
    status = calculate_module_status(progress_percent, len(module_attempts), last_score)
    if any(float(score) < 50 for score in scores):
        status = "need_review"
    return _module_payload(
        module_id,
        status=status,
        progress_percent=progress_percent,
        completed_items=completed_items,
        total_items=total_items,
        last_score=last_score,
        best_score=max(scores) if scores else None,
        attempt_count=len(module_attempts),
    )


def _completed_items_for_module(module_id: str, attempts: list[dict[str, Any]], total_items: int) -> int:
    if module_id == "grammar_breakdown":
        return min(len(attempts), total_items)
    latest_by_item: dict[str, dict[str, Any]] = {}
    for attempt in reversed(attempts):
        key = _module_item_key(module_id, attempt)
        latest_by_item[key] = attempt
    completed = [
        item for item in latest_by_item.values()
        if float(item.get("percent_score") or 0) >= 70
    ]
    return min(len(completed), total_items)


def _module_item_key(module_id: str, attempt: dict[str, Any]) -> str:
    activity_id = str(attempt.get("activity_id") or module_id)
    if module_id == "sentence_builder":
        parts = activity_id.split("_")
        return parts[-1] if len(parts) > 1 and parts[-1] in {"arrange_words", "complete_sentence", "combine_sentences", "rewrite_formal_ba_sentence", "fix_word_order"} else activity_id
    return activity_id


def _review_module(review: dict[str, Any], attempts: list[dict[str, Any]], journey: dict[str, Any]) -> dict[str, Any]:
    has_attempts = bool(attempts)
    score = float(journey.get("grammar_score") or 0)
    queue = review.get("review_queue") or []
    patterns = review.get("mistake_patterns") or []
    if not has_attempts:
        status = "not_started"
        progress = 0
        completed = 0
    elif not queue and not patterns and score >= 75:
        status = "completed"
        progress = 100
        completed = 1
    else:
        status = "recommended"
        progress = 60
        completed = 1
    return _module_payload(
        "review",
        status=status,
        progress_percent=progress,
        completed_items=completed,
        total_items=1,
        last_score=score if has_attempts else None,
        best_score=score if has_attempts else None,
        attempt_count=1 if has_attempts else 0,
        next_action=review.get("mentor_message") or MODULE_DEFINITIONS["review"]["next_action"],
    )


def _simulation_module(attempts: list[dict[str, Any]], history: list[dict[str, Any]]) -> dict[str, Any]:
    modes = {"short": 0.0, "medium": 0.0, "full": 0.0}
    for item in history:
        mode = item.get("mode")
        if mode in modes:
            modes[mode] = max(modes[mode], float(item.get("total_score") or 0))
    for attempt in attempts:
        # Persisted attempts do not always include mode, so count them as short practice fallback.
        modes["short"] = max(modes["short"], float(attempt.get("percent_score") or 0))
    completed_items = len([mode for mode, score in modes.items() if score >= 70 and mode != "full"]) + (1 if modes["full"] >= 75 else 0)
    best_score = max(list(modes.values()) + [float(attempt.get("percent_score") or 0) for attempt in attempts] or [0])
    latest_score = float(attempts[0].get("percent_score") or 0) if attempts else (max(modes.values()) if any(modes.values()) else None)
    if not attempts and not any(modes.values()):
        status = "not_started"
    elif modes["full"] >= 75:
        status = "completed"
    elif modes["full"] > 0 and modes["full"] < 75:
        status = "need_review"
    else:
        status = "in_progress"
    return _module_payload(
        "simulation",
        status=status,
        progress_percent=round((completed_items / 3) * 100, 1),
        completed_items=completed_items,
        total_items=3,
        last_score=latest_score,
        best_score=best_score if best_score else None,
        attempt_count=len(attempts) + len(history),
    )


def _module_payload(
    module_id: str,
    status: str,
    progress_percent: float,
    completed_items: int,
    total_items: int,
    last_score: float | None,
    best_score: float | None,
    attempt_count: int,
    next_action: str | None = None,
) -> dict[str, Any]:
    base = MODULE_DEFINITIONS[module_id]
    return {
        **base,
        "status": status,
        "progress_percent": round(float(progress_percent or 0), 1),
        "completed_items": int(completed_items or 0),
        "total_items": int(total_items or 0),
        "last_score": round(float(last_score), 1) if last_score is not None else None,
        "best_score": round(float(best_score), 1) if best_score is not None else None,
        "attempt_count": int(attempt_count or 0),
        "next_action": next_action or base["next_action"],
        "recommended": False,
    }


def _mark_recommended(module: dict[str, Any], recommended_module_id: str) -> dict[str, Any]:
    if module["module_id"] != recommended_module_id:
        return module
    status = module["status"] if module["status"] == "completed" else "recommended"
    return {**module, "status": status, "recommended": True}


def _choose_recommended_module(modules: list[dict[str, Any]], journey: dict[str, Any], review: dict[str, Any]) -> dict[str, Any]:
    for status in ("need_review", "not_started", "in_progress"):
        for module in modules:
            if module["module_id"] == "review" and status == "not_started":
                continue
            if module["status"] == status:
                return _recommended_payload(module, _recommended_reason(module, review))
    fallback = next((module for module in modules if module["module_id"] == "simulation"), modules[0])
    return _recommended_payload(fallback, "Semua module utama sudah berjalan. Uji kesiapan melalui simulasi.")


def _recommended_payload(module: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "module_id": module["module_id"],
        "section": module["section"],
        "title": module["title"],
        "reason": reason,
        "next_action": module["next_action"],
    }


def _recommended_reason(module: dict[str, Any], review: dict[str, Any]) -> str:
    if module["status"] == "need_review":
        return f"{module['title']} perlu diulang karena ada skor di bawah target."
    if module["attempt_count"] == 0:
        return f"Mulai dari {module['title']} agar jalur Grammar tetap berurutan."
    if module["status"] == "in_progress":
        return f"Lanjutkan {module['title']} sampai progress module ini selesai."
    return review.get("mentor_message") or "Ikuti rekomendasi Grammar berikutnya."


def _module_total_items(module_id: str) -> int:
    if module_id == "grammar_breakdown":
        return 5
    if module_id == "basic_trainer":
        return max(len(get_basic_trainer_topics()), 7)
    if module_id == "intermediate_trainer":
        return max(len(get_intermediate_trainer_topics()), 7)
    if module_id == "error_correction":
        return max(len(get_error_categories()), 1)
    if module_id == "sentence_builder":
        return 5
    if module_id == "advanced_lab":
        advanced = [topic for topic in get_grammar_topics("advanced")]
        return max(len(advanced), 7)
    return 1


def _safe_review(user_id: str) -> dict[str, Any]:
    try:
        return get_grammar_review(user_id)
    except Exception:
        return {"weakness_summary": {}, "mistake_patterns": [], "review_queue": [], "mentor_message": ""}


def _safe_journey(user_id: str) -> dict[str, Any]:
    try:
        return get_grammar_journey(user_id)
    except Exception:
        return {"grammar_level": "Basic 1 - Sentence Foundation", "grammar_score": 0}


def _safe_simulation_history(user_id: str) -> list[dict[str, Any]]:
    try:
        return get_grammar_simulation_history(user_id).get("history", [])
    except Exception:
        return []


def _percent(score: Any, max_score: Any) -> float:
    max_value = max(float(max_score or 100), 1)
    return round((float(score or 0) / max_value) * 100, 1)
