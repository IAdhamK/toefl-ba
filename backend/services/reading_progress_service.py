from __future__ import annotations

from typing import Any

from backend.database import decode_json, get_connection
from backend.repository import list_lessons
from backend.services.journey_service import get_default_user_id
from backend.services.reading_service import (
    get_reading_journey,
    get_reading_review,
    get_reading_simulation_history,
)


DEFAULT_USER_ID = "default-user"

MODULE_ORDER = [
    "overview",
    "guided",
    "practice",
    "trainer",
    "simulation",
]

MODULE_DEFINITIONS = {
    "overview": {
        "module_id": "overview",
        "title": "Reading Overview",
        "description": "Ringkasan level, score, skill kuat/lemah, dan langkah Reading berikutnya.",
        "target_score": 70,
        "section": "overview",
        "next_action": "Lihat ringkasan Reading Journey dan pilih langkah yang direkomendasikan.",
    },
    "guided": {
        "module_id": "guided",
        "title": "Guided Reading",
        "description": "Baca pelan-pelan: title, kalimat pertama, subject/verb, vocabulary, paragraph map, dan main idea.",
        "target_score": 70,
        "section": "guided",
        "next_action": "Selesaikan Guided Reading untuk passage aktif yang tersedia.",
    },
    "practice": {
        "module_id": "practice",
        "title": "Practice Questions",
        "description": "Kerjakan soal TOEFL-style dari passage aktif dan pelajari Answer Review.",
        "target_score": 70,
        "section": "practice",
        "next_action": "Kerjakan passage practice lalu baca bukti jawaban di Answer Review.",
    },
    "trainer": {
        "module_id": "trainer",
        "title": "Reading Trainer",
        "description": "Latihan sub-skill: main idea, detail, vocabulary context, inference, dan sentence breakdown.",
        "target_score": 70,
        "section": "trainer",
        "next_action": "Latih sub-skill yang masih paling lemah.",
    },
    "review": {
        "module_id": "review",
        "title": "Reading Review",
        "description": "Lihat weakness report, mistake pattern, review queue, dan rekomendasi latihan ulang.",
        "target_score": 75,
        "section": "review",
        "next_action": "Buka Reading Review untuk melihat pola salah dan latihan ulang.",
    },
    "simulation": {
        "module_id": "simulation",
        "title": "TOEFL Reading Simulation",
        "description": "Uji kemampuan Reading dengan timer short, medium, atau full practice.",
        "target_score": 75,
        "section": "simulation",
        "next_action": "Kerjakan Full Practice Simulation dan targetkan minimal 75%.",
    },
}

ACTIVITY_MODULE_MAP = {
    "guided_reading": "guided",
    "reading_quiz": "practice",
    "reading_journey_attempt": "practice",
    "reading_answer_review": "practice",
    "reading_subskill_trainer": "trainer",
    "reading_trainer": "trainer",
    "reading_simulation": "simulation",
}


def get_reading_module_progress(user_id: str | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    attempts = get_recent_reading_module_attempts(user_id, limit=500)
    journey = _safe_journey(user_id)
    review = _safe_review(user_id)
    history = _safe_simulation_history(user_id)
    modules = [_build_module_progress(module_id, attempts, journey, review, history) for module_id in MODULE_ORDER]
    recommended = _choose_recommended_module(modules, journey, review)
    modules = [_mark_recommended(module, recommended["module_id"]) for module in modules]
    summary = get_reading_progress_summary(user_id, modules=modules, journey=journey, recommended=recommended)
    finish_status = get_reading_finish_status(user_id, modules=modules, history=history)
    learning_path = get_reading_learning_path(user_id, modules=modules)["learning_path"]
    return {
        "summary": summary,
        "modules": modules,
        "learning_path": learning_path,
        "recommended_section": recommended,
        "finish_status": finish_status,
    }


def get_reading_progress_summary(
    user_id: str | None = None,
    modules: list[dict[str, Any]] | None = None,
    journey: dict[str, Any] | None = None,
    recommended: dict[str, Any] | None = None,
) -> dict[str, Any]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    modules = modules if modules is not None else get_reading_module_progress(user_id)["modules"]
    journey = journey or _safe_journey(user_id)
    recommended = recommended or _choose_recommended_module(modules, journey, _safe_review(user_id))
    completed_modules = len([module for module in modules if module["status"] == "completed"])
    overall_progress = round(sum(float(module.get("progress_percent") or 0) for module in modules) / len(modules), 1) if modules else 0
    return {
        "overall_progress_percent": overall_progress,
        "reading_level": journey.get("reading_level", "Understand Simple Meaning"),
        "reading_score": round(float(journey.get("reading_score") or 0), 1),
        "completed_modules": completed_modules,
        "total_modules": len(modules),
        "active_module": recommended.get("section", "guided"),
        "next_action": recommended.get("next_action", "Mulai dari Guided Reading."),
        "finish_target": "Full Reading Simulation minimal 75%",
    }


def get_reading_learning_path(user_id: str | None = None, modules: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    modules = modules if modules is not None else get_reading_module_progress(user_id)["modules"]
    return {"learning_path": [{"step": index, **module} for index, module in enumerate(modules, start=1)]}


def get_recommended_reading_section(user_id: str | None = None) -> dict[str, Any]:
    return get_reading_module_progress(user_id)["recommended_section"]


def get_reading_finish_status(
    user_id: str | None = None,
    modules: list[dict[str, Any]] | None = None,
    history: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    modules = modules if modules is not None else get_reading_module_progress(user_id)["modules"]
    history = history if history is not None else _safe_simulation_history(user_id)
    full_scores = [float(item.get("total_score") or item.get("accuracy") or 0) for item in history if item.get("mode") == "full"]
    full_score = max(full_scores) if full_scores else 0
    simulation = next((module for module in modules if module["module_id"] == "simulation"), {})
    if simulation.get("status") == "completed":
        full_score = max(full_score, float(simulation.get("best_score") or 0))
    is_finished = full_score >= 75
    return {
        "is_finished": is_finished,
        "finish_rule": "Full Reading Simulation minimal 75%",
        "full_simulation_score": round(full_score, 1),
        "message": (
            "Reading Lab selesai. Pertahankan skor full simulation minimal 75%."
            if is_finished
            else "Belum finish. Ikuti rekomendasi Reading berikutnya sampai siap full simulation minimal 75%."
        ),
    }


def get_recent_reading_module_attempts(user_id: str | None = None, limit: int = 200) -> list[dict[str, Any]]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, activity_id, activity_type, score, max_score, accuracy,
                   mistakes_json, feedback, created_at
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
    journey: dict[str, Any],
    review: dict[str, Any],
    history: list[dict[str, Any]],
) -> dict[str, Any]:
    if module_id == "overview":
        return _overview_module(attempts, journey)
    if module_id == "review":
        return _review_module(review, attempts, journey)
    if module_id == "simulation":
        return _simulation_module([item for item in attempts if item.get("module_id") == "simulation"], history)

    module_attempts = [item for item in attempts if item.get("module_id") == module_id]
    total_items = _module_total_items(module_id)
    completed_items = _completed_items_for_module(module_id, module_attempts, total_items)
    progress_percent = round((completed_items / max(total_items, 1)) * 100, 1)
    latest = module_attempts[0] if module_attempts else {}
    scores = [float(item.get("percent_score") or 0) for item in module_attempts]
    last_score = float(latest.get("percent_score") or 0) if latest else None
    status = calculate_module_status(progress_percent, len(module_attempts), last_score)
    if any(score < 50 for score in scores):
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
        next_action=_module_next_action(module_id, completed_items, total_items),
    )


def _overview_module(attempts: list[dict[str, Any]], journey: dict[str, Any]) -> dict[str, Any]:
    score = float(journey.get("reading_score") or 0)
    completed_passages = int(journey.get("completed_passages") or 0)
    progress = min(100, max(score, (completed_passages / 3) * 100 if completed_passages else 0))
    status = "completed" if score >= 70 and completed_passages > 0 else ("in_progress" if attempts else "not_started")
    return _module_payload(
        "overview",
        status=status,
        progress_percent=progress,
        completed_items=1 if attempts else 0,
        total_items=1,
        last_score=score if attempts else None,
        best_score=score if attempts else None,
        attempt_count=len(attempts),
        next_action=journey.get("next_recommended_action") or MODULE_DEFINITIONS["overview"]["next_action"],
    )


def _review_module(review: dict[str, Any], attempts: list[dict[str, Any]], journey: dict[str, Any]) -> dict[str, Any]:
    queue = review.get("review_items") or []
    patterns = review.get("mistake_patterns") or []
    active_queue = [item for item in queue if item.get("type") != "starter_review"]
    score = float(journey.get("reading_score") or 0)
    total_items = max(len(active_queue), 1)
    completed = _completed_review_items(active_queue, journey)
    review_mastery = _average_review_mastery(active_queue, journey)
    if not attempts:
        status = "not_started"
        progress = 0
        completed = 0
    elif active_queue and completed < total_items:
        status = "recommended" if completed == 0 else "in_progress"
        progress = round((completed / total_items) * 100, 1)
    elif not active_queue and not _active_review_patterns(patterns) and score >= 75:
        status = "completed"
        progress = 100
        completed = total_items
    elif completed >= total_items and score >= 75:
        status = "completed"
        progress = 100
    else:
        status = "recommended"
        progress = 60
    return _module_payload(
        "review",
        status=status,
        progress_percent=progress,
        completed_items=completed,
        total_items=total_items,
        last_score=review_mastery if attempts and active_queue else None,
        best_score=score if attempts else None,
        attempt_count=1 if attempts else 0,
        next_action=_review_next_action(status, completed, total_items, review),
    )


def _simulation_module(attempts: list[dict[str, Any]], history: list[dict[str, Any]]) -> dict[str, Any]:
    modes = {"short": 0.0, "medium": 0.0, "full": 0.0}
    for item in history:
        mode = item.get("mode")
        if mode in modes:
            modes[mode] = max(modes[mode], float(item.get("total_score") or item.get("accuracy") or 0))
    for attempt in attempts:
        mode = _infer_simulation_mode(attempt)
        modes[mode] = max(modes.get(mode, 0), float(attempt.get("percent_score") or 0))
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


def _completed_items_for_module(module_id: str, attempts: list[dict[str, Any]], total_items: int) -> int:
    if module_id == "guided":
        return min(len({item.get("activity_id") for item in attempts if float(item.get("percent_score") or 0) >= 70}), total_items)
    latest_by_item: dict[str, dict[str, Any]] = {}
    for attempt in reversed(attempts):
        latest_by_item[_module_item_key(module_id, attempt)] = attempt
    completed = [item for item in latest_by_item.values() if float(item.get("percent_score") or 0) >= 70]
    return min(len(completed), total_items)


def _completed_review_items(queue: list[dict[str, Any]], journey: dict[str, Any]) -> int:
    mastery = _subskill_mastery_lookup(journey)
    completed = 0
    for item in queue:
        candidates = [
            item.get("source_sub_skill"),
            item.get("target_sub_skill"),
            item.get("sub_skill"),
        ]
        scores = [mastery.get(str(candidate), 0) for candidate in candidates if candidate]
        if scores and max(scores) >= 70:
            completed += 1
    return completed


def _average_review_mastery(queue: list[dict[str, Any]], journey: dict[str, Any]) -> float:
    mastery = _subskill_mastery_lookup(journey)
    scores: list[float] = []
    for item in queue:
        candidates = [
            item.get("source_sub_skill"),
            item.get("target_sub_skill"),
            item.get("sub_skill"),
        ]
        candidate_scores = [mastery.get(str(candidate), 0) for candidate in candidates if candidate]
        if candidate_scores:
            scores.append(max(candidate_scores))
    return round(sum(scores) / len(scores), 1) if scores else 0


def _subskill_mastery_lookup(journey: dict[str, Any]) -> dict[str, float]:
    rows = journey.get("sub_skill_mastery") or []
    return {
        str(item.get("subskill") or item.get("sub_skill")): float(item.get("mastery_score") or 0)
        for item in rows
        if item.get("subskill") or item.get("sub_skill")
    }


def _active_review_patterns(patterns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        item
        for item in patterns
        if int(item.get("wrong_count") or 0) > 0
        or (int(item.get("attempt_count") or 0) > 0 and float(item.get("mastery_score") or 0) < 70)
    ]


def _review_next_action(status: str, completed: int, total_items: int, review: dict[str, Any]) -> str:
    if status == "completed":
        return "Reading Review selesai. Lanjutkan Simulation untuk memastikan hasil stabil."
    if total_items > 1:
        return (
            f"Selesaikan {total_items - completed} item Review Queue. "
            "Klik Latihan Ulang Skill Lemah, lalu tingkatkan mastery skill prioritas minimal 70%."
        )
    return review.get("recommended_practice") or review.get("mentor_message") or MODULE_DEFINITIONS["review"]["next_action"]


def _module_item_key(module_id: str, attempt: dict[str, Any]) -> str:
    activity_id = str(attempt.get("activity_id") or module_id)
    if module_id == "trainer":
        return activity_id.replace("trainer-", "")
    return activity_id


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
            if module["module_id"] in {"overview", "review"} and status == "not_started":
                continue
            if module["status"] == status:
                return _recommended_payload(module, _recommended_reason(module, review))
    fallback = next((module for module in modules if module["module_id"] == "simulation"), modules[0])
    return _recommended_payload(fallback, "Semua mode utama sudah berjalan. Uji kesiapan lewat Reading Simulation.")


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
        return f"Mulai dari {module['title']} agar alur Reading tetap terarah."
    if module["status"] == "in_progress":
        return f"Lanjutkan {module['title']} sampai progress mode ini selesai."
    return review.get("mentor_message") or "Ikuti rekomendasi Reading berikutnya."


def _module_total_items(module_id: str) -> int:
    if module_id == "guided":
        return min(max(_active_reading_passage_count(), 1), 3)
    if module_id == "practice":
        return 5
    if module_id == "trainer":
        return 5
    return 1


def _module_next_action(module_id: str, completed_items: int, total_items: int) -> str:
    if module_id == "guided":
        if completed_items >= total_items:
            return "Guided Reading selesai untuk semua passage aktif. Lanjutkan ke Practice Questions."
        if total_items < 3:
            return "Selesaikan Guided Reading untuk semua passage aktif."
        return "Selesaikan Guided Reading untuk 3 passage pendek."
    return MODULE_DEFINITIONS[module_id]["next_action"]


def _active_reading_passage_count() -> int:
    try:
        lessons = [lesson for lesson in list_lessons() if lesson]
        return len(lessons) or 1
    except Exception:
        return 2


def _safe_journey(user_id: str) -> dict[str, Any]:
    try:
        return get_reading_journey(user_id)
    except Exception:
        return {"reading_level": "Understand Simple Meaning", "reading_score": 0, "completed_passages": 0}


def _safe_review(user_id: str) -> dict[str, Any]:
    try:
        return get_reading_review(user_id)
    except Exception:
        return {"weakness_summary": {}, "mistake_patterns": [], "review_items": [], "mentor_message": ""}


def _safe_simulation_history(user_id: str) -> list[dict[str, Any]]:
    try:
        return get_reading_simulation_history(user_id).get("history", [])
    except Exception:
        return []


def _infer_simulation_mode(attempt: dict[str, Any]) -> str:
    feedback = str(attempt.get("feedback") or "")
    if feedback.startswith("SIMULATION_RESULT:"):
        parsed = decode_json(feedback.removeprefix("SIMULATION_RESULT:"), {})
        mode = parsed.get("mode") if isinstance(parsed, dict) else None
        if mode in {"short", "medium", "full"}:
            return mode
    activity_id = str(attempt.get("activity_id") or "")
    for mode in ("short", "medium", "full"):
        if mode in activity_id:
            return mode
    return "short"


def _percent(score: Any, max_score: Any) -> float:
    max_value = max(float(max_score or 100), 1)
    return round((float(score or 0) / max_value) * 100, 1)
