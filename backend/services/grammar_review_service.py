from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from backend.database import decode_json, get_connection
from backend.services.grammar_journey_service import get_grammar_journey
from backend.services.grammar_topic_service import get_grammar_topic
from backend.services.journey_service import get_default_user_id


DEFAULT_USER_ID = "default-user"

MISTAKE_TOPIC_MAP = {
    "subject_verb_agreement": "subject_verb",
    "missing_be_after_modal": "modal_verb",
    "modal_verb_pattern": "modal_verb",
    "main_verb_detection": "gerund_vs_main_verb",
    "gerund_vs_main_verb": "gerund_vs_main_verb",
    "reduced_relative_clause": "reduced_relative_clause",
    "passive_voice": "passive_voice",
    "parallel_structure": "parallel_structure",
    "connector_logic": "connector_logic",
    "nominalization": "nominalization",
    "formal_ba_writing": "formal_ba_writing",
    "word_order": "simple_sentence_pattern",
    "sentence_builder": "simple_sentence_pattern",
    "unknown_grammar_issue": "subject_verb",
}

REVIEW_ENDPOINTS = {
    "subject_verb": ("/api/grammar/trainer/basic/subject_verb", "Basic Grammar Trainer", "basic"),
    "object_complement": ("/api/grammar/trainer/basic/object_complement", "Basic Grammar Trainer", "basic"),
    "modal_verb": ("/api/grammar/trainer/basic/modal_verb", "Basic Grammar Trainer", "basic"),
    "simple_sentence_pattern": ("/api/grammar/sentence-builder?level=basic", "Grammar Sentence Builder", "basic"),
    "gerund_vs_main_verb": ("/api/grammar/trainer/intermediate/gerund_vs_main_verb", "Intermediate Grammar Trainer", "intermediate"),
    "reduced_relative_clause": ("/api/grammar/trainer/intermediate/reduced_relative_clause", "Intermediate Grammar Trainer", "intermediate"),
    "passive_voice": ("/api/grammar/trainer/intermediate/passive_voice", "Intermediate Grammar Trainer", "intermediate"),
    "parallel_structure": ("/api/grammar/trainer/intermediate/parallel_structure", "Intermediate Grammar Trainer", "intermediate"),
    "connector_logic": ("/api/grammar/trainer/intermediate/connector_logic", "Intermediate Grammar Trainer", "intermediate"),
    "nominalization": ("/api/grammar/advanced/topics/nominalization", "Advanced Grammar Lab", "advanced"),
    "formal_ba_writing": ("/api/grammar/advanced/topics/formal_ba_writing", "Advanced Grammar Lab", "advanced"),
}

MISTAKE_EXPLANATIONS = {
    "subject_verb_agreement": "User sering salah mencocokkan subject tunggal/jamak dengan verb.",
    "missing_be_after_modal": "User sering lupa memakai be setelah modal sebelum adjective.",
    "modal_verb_pattern": "User perlu mengingat bahwa modal diikuti base verb.",
    "main_verb_detection": "User sering belum menemukan main verb di kalimat panjang.",
    "gerund_vs_main_verb": "User sering mengira kata -ing seperti working atau operating adalah verb utama.",
    "reduced_relative_clause": "User perlu membedakan phrase penjelas noun dan main clause.",
    "passive_voice": "User perlu menguatkan pola passive be + V3.",
    "parallel_structure": "User sering mencampur bentuk grammar dalam daftar aksi.",
    "connector_logic": "User perlu memilih connector sesuai hubungan ide.",
    "nominalization": "User perlu mengenali bentuk noun formal seperti implementation dan validation.",
    "formal_ba_writing": "User perlu membangun kalimat BA yang lebih formal dan spesifik.",
    "word_order": "User perlu memperkuat urutan kata Subject + Verb + Object.",
    "sentence_builder": "User perlu latihan membangun kalimat dari bagian kecil.",
    "unknown_grammar_issue": "Kesalahan grammar belum cukup spesifik, perlu latihan fondasi.",
}


def get_grammar_review(user_id: str | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    weakness_summary = get_grammar_weakness_summary(user_id)
    patterns = get_grammar_mistake_patterns(user_id)["patterns"]
    queue = build_grammar_review_queue(
        [weakness_summary["primary_weakness"], weakness_summary.get("secondary_weakness")],
        patterns,
    )
    recommended = get_grammar_recommended_practice(user_id)
    recent = get_recent_grammar_attempts(user_id, limit=10)
    return {
        "weakness_summary": weakness_summary,
        "mistake_patterns": patterns,
        "review_queue": queue,
        "recommended_practice": recommended,
        "mentor_message": build_grammar_mentor_message(weakness_summary, patterns),
        "recent_attempts": recent,
    }


def get_grammar_mistake_patterns(user_id: str | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    attempts = get_recent_grammar_attempts(user_id, limit=50)
    classified = []
    for attempt in attempts:
        mistakes = attempt.get("mistakes", [])
        if mistakes:
            classified.extend(classify_grammar_mistake(mistake) for mistake in mistakes)
        elif float(attempt.get("accuracy") or 0) < 70:
            classified.append(classify_grammar_mistake(attempt))
    if not classified:
        classified = [classify_grammar_mistake({"related_topic_id": "subject_verb", "example": "Belum cukup data attempt."})]
    counter = Counter(item["mistake_type"] for item in classified)
    examples = {}
    topics = {}
    for item in classified:
        examples.setdefault(item["mistake_type"], item.get("example_mistake", ""))
        topics.setdefault(item["mistake_type"], item["topic_id"])
    patterns = []
    for index, (mistake_type, frequency) in enumerate(counter.most_common(), start=1):
        topic_id = topics.get(mistake_type) or MISTAKE_TOPIC_MAP.get(mistake_type, "subject_verb")
        topic = get_grammar_topic(topic_id) or {"title": _title_from_topic(topic_id)}
        endpoint, module, _difficulty = _endpoint_for_topic(topic_id)
        patterns.append(
            {
                "pattern_id": f"pattern_{mistake_type}",
                "topic_id": topic_id,
                "title": _pattern_title(mistake_type, topic.get("title", topic_id)),
                "mistake_type": mistake_type,
                "frequency": frequency,
                "severity": "high" if frequency >= 3 or index == 1 else "medium",
                "pattern_explanation_id": MISTAKE_EXPLANATIONS.get(mistake_type, MISTAKE_EXPLANATIONS["unknown_grammar_issue"]),
                "example_mistake": examples.get(mistake_type) or "Belum ada contoh spesifik.",
                "recommended_action": _recommended_action(topic_id),
                "recommended_endpoint": endpoint,
                "related_phase_module": module,
            }
        )
    return {
        "patterns": patterns,
        "total": len(patterns),
        "primary_pattern": patterns[0] if patterns else {},
        "mentor_message": build_grammar_mentor_message(get_grammar_weakness_summary(user_id), patterns),
    }


def get_grammar_review_queue(user_id: str | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    weakness = get_grammar_weakness_summary(user_id)
    patterns = get_grammar_mistake_patterns(user_id)["patterns"]
    queue = build_grammar_review_queue([weakness["primary_weakness"], weakness.get("secondary_weakness")], patterns)
    return {
        "review_items": queue,
        "total": len(queue),
        "next_review": queue[0] if queue else {},
        "mentor_message": build_grammar_mentor_message(weakness, patterns),
    }


def get_grammar_weakness_summary(user_id: str | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    journey = get_grammar_journey(user_id)
    mastery_rows = get_grammar_mastery_rows(user_id)
    attempted = [item for item in mastery_rows if int(item.get("attempt_count") or 0) > 0]
    weak_rows = sorted(attempted or mastery_rows, key=lambda item: (float(item.get("mastery_score") or 0), -int(item.get("wrong_count") or 0)))
    primary = _weakness_from_row(weak_rows[0] if weak_rows else None, "subject_verb")
    secondary = _weakness_from_row(weak_rows[1] if len(weak_rows) > 1 else None, "modal_verb")
    attempts = get_recent_grammar_attempts(user_id, limit=100)
    completed = len(attempts)
    average = journey.get("grammar_score", 0)
    if not completed:
        average = 0
    return {
        "primary_weakness": primary,
        "secondary_weakness": secondary,
        "average_grammar_score": average,
        "completed_grammar_attempts": completed,
        "review_priority": "high" if primary.get("mastery_score", 0) < 60 else "medium",
        "readiness_level": journey.get("grammar_level", "Basic 1 - Sentence Foundation"),
    }


def get_grammar_recommended_practice(user_id: str | None = None) -> dict[str, Any]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    patterns = get_grammar_mistake_patterns(user_id)["patterns"]
    weakness = get_grammar_weakness_summary(user_id)
    topic_id = patterns[0]["topic_id"] if patterns else weakness["primary_weakness"]["topic_id"]
    endpoint, module, difficulty = _endpoint_for_topic(topic_id)
    return {
        "recommended_topic_id": topic_id,
        "recommended_module": _module_key(module),
        "reason": f"Topik {topic_id} dipilih karena muncul sebagai weakness atau mistake pattern utama.",
        "next_action": _recommended_action(topic_id),
        "target_endpoint": endpoint,
        "estimated_minutes": _estimated_minutes(topic_id),
        "difficulty": difficulty,
    }


def get_recent_grammar_attempts(user_id: str | None = None, limit: int = 10) -> list[dict[str, Any]]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, skill_type, activity_id, activity_type, score, max_score, accuracy,
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
        item["mistakes"] = decode_json(item.get("mistakes_json"), [])
        attempts.append(item)
    return attempts


def get_grammar_mastery_rows(user_id: str | None = None) -> list[dict[str, Any]]:
    user_id = get_default_user_id(user_id or DEFAULT_USER_ID)
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT topic, mastery_score, attempt_count, correct_count, wrong_count,
                   last_practiced_at, next_review_at
            FROM skill_mastery
            WHERE user_id = ? AND skill_type = 'grammar'
            ORDER BY mastery_score ASC, wrong_count DESC
            """,
            (user_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def extract_mistake_tags(mistakes: list) -> list[str]:
    return [classify_grammar_mistake(mistake)["mistake_type"] for mistake in mistakes or []]


def classify_grammar_mistake(mistake: dict | str) -> dict[str, Any]:
    if isinstance(mistake, str):
        source = mistake.lower()
        raw = {"example": mistake}
    else:
        raw = mistake or {}
        source = " ".join(str(value).lower() for value in raw.values())
    explicit = (
        raw.get("error_type")
        or raw.get("mistake_type")
        or raw.get("related_topic_id")
        or raw.get("topic_id")
        or raw.get("recommended_review_topic")
    )
    mistake_type = _normalize_mistake_type(str(explicit or ""))
    if mistake_type == "unknown_grammar_issue":
        mistake_type = _classify_from_text(source)
    topic_id = raw.get("related_topic_id") or raw.get("topic_id") or MISTAKE_TOPIC_MAP.get(mistake_type, "subject_verb")
    return {
        "mistake_type": mistake_type,
        "topic_id": topic_id,
        "example_mistake": _example_from_mistake(raw),
    }


def build_grammar_review_queue(weak_topics: list, mistake_patterns: list) -> list[dict[str, Any]]:
    seen = set()
    queue = []
    for pattern in mistake_patterns:
        topic_id = pattern.get("topic_id")
        if topic_id and topic_id not in seen:
            seen.add(topic_id)
            queue.append(_review_item(topic_id, len(queue) + 1, pattern.get("pattern_explanation_id", ""), "mistake_pattern"))
    for weak in weak_topics:
        if not weak:
            continue
        topic_id = weak.get("topic_id")
        if topic_id and topic_id not in seen:
            seen.add(topic_id)
            queue.append(_review_item(topic_id, len(queue) + 1, weak.get("reason", ""), "weak_mastery"))
    if not queue:
        queue.append(_review_item("subject_verb", 1, "Belum cukup data. Mulai dari fondasi subject dan verb.", "fallback"))
    return queue[:5]


def build_grammar_mentor_message(weakness_summary: dict, mistake_patterns: list) -> str:
    primary = weakness_summary.get("primary_weakness", {})
    if weakness_summary.get("completed_grammar_attempts", 0) == 0:
        return "Belum cukup data review. Mulai dari Subject and Verb, lalu kerjakan beberapa latihan agar review menjadi lebih akurat."
    if mistake_patterns:
        return (
            f"Review utama kamu adalah {primary.get('title', 'Grammar foundation')}. "
            f"Pola salah yang paling terlihat: {mistake_patterns[0].get('title', 'grammar pattern')}. "
            "Ulangi latihan yang direkomendasikan sebelum lanjut ke topik lebih sulit."
        )
    return f"Fokus review saat ini: {primary.get('title', 'Subject and Verb')}. Latihan ulang pelan-pelan dan cek explanation setiap jawaban."


def _weakness_from_row(row: dict[str, Any] | None, fallback_topic_id: str) -> dict[str, Any]:
    topic_id = row.get("topic") if row else fallback_topic_id
    topic = get_grammar_topic(topic_id) or {"title": _title_from_topic(topic_id)}
    score = round(float(row.get("mastery_score") or 0), 1) if row else 0
    return {
        "topic_id": topic_id,
        "title": topic.get("title", _title_from_topic(topic_id)),
        "mastery_score": score,
        "reason": _weakness_reason(topic_id, score),
    }


def _review_item(topic_id: str, priority: int, reason: str, source: str) -> dict[str, Any]:
    topic = get_grammar_topic(topic_id) or {"title": _title_from_topic(topic_id)}
    endpoint, _module, _difficulty = _endpoint_for_topic(topic_id)
    return {
        "review_id": f"review_{topic_id}",
        "priority": priority,
        "topic_id": topic_id,
        "title": f"Review {topic.get('title', _title_from_topic(topic_id))}",
        "reason": reason or "Topik ini memiliki mastery score rendah atau muncul dalam mistake pattern.",
        "action_label": _action_label(topic_id),
        "target_endpoint": endpoint,
        "estimated_minutes": _estimated_minutes(topic_id),
        "source": source,
        "status": "pending",
    }


def _normalize_mistake_type(value: str) -> str:
    lowered = value.strip().lower()
    aliases = {
        "subject_verb": "subject_verb_agreement",
        "modal_verb": "modal_verb_pattern",
        "simple_sentence_pattern": "word_order",
        "gerund_vs_main_verb": "gerund_vs_main_verb",
        "passive_voice_error": "passive_voice",
        "advanced_grammar_rewrite": "formal_ba_writing",
        "grammar_sentence_builder": "sentence_builder",
    }
    if lowered in aliases:
        return aliases[lowered]
    if lowered in MISTAKE_TOPIC_MAP:
        return lowered
    return "unknown_grammar_issue"


def _classify_from_text(text: str) -> str:
    if "missing_be_after_modal" in text or "must be" in text or "should be" in text:
        return "missing_be_after_modal"
    if "modal" in text or "must clarify" in text or "should document" in text:
        return "modal_verb_pattern"
    if "working" in text or "operating" in text or "main verb" in text:
        return "gerund_vs_main_verb"
    if "passive" in text or "processed" in text or "documented" in text:
        return "passive_voice"
    if "parallel" in text or "ensure" in text or "and" in text:
        return "parallel_structure"
    if "although" in text or "therefore" in text or "connector" in text:
        return "connector_logic"
    if "implementation" in text or "validation" in text or "nominalization" in text:
        return "nominalization"
    if "formal" in text or "generate reports" in text or "efficiently" in text:
        return "formal_ba_writing"
    if "word_order" in text or "sentence_builder" in text:
        return "word_order"
    return "unknown_grammar_issue"


def _example_from_mistake(raw: dict[str, Any]) -> str:
    if isinstance(raw, str):
        return raw
    return (
        raw.get("example_mistake")
        or raw.get("user_answer")
        or raw.get("incorrect_sentence")
        or raw.get("item_id")
        or raw.get("question_id")
        or raw.get("activity_id")
        or "Belum ada contoh spesifik."
    )


def _endpoint_for_topic(topic_id: str) -> tuple[str, str, str]:
    return REVIEW_ENDPOINTS.get(topic_id, ("/api/grammar/trainer/basic/subject_verb", "Basic Grammar Trainer", "basic"))


def _module_key(module: str) -> str:
    return module.lower().replace(" grammar ", "_").replace(" ", "_")


def _estimated_minutes(topic_id: str) -> int:
    if topic_id in {"nominalization", "formal_ba_writing"}:
        return 15
    if topic_id in {"gerund_vs_main_verb", "reduced_relative_clause", "passive_voice", "parallel_structure", "connector_logic"}:
        return 12
    return 10


def _recommended_action(topic_id: str) -> str:
    actions = {
        "subject_verb": "Latihan ulang mencari subject dan main verb.",
        "modal_verb": "Latihan pola modal: must/should/can + base verb.",
        "gerund_vs_main_verb": "Ulangi Intermediate Trainer bagian Gerund vs Main Verb.",
        "passive_voice": "Latihan passive voice: be + V3.",
        "parallel_structure": "Latihan membuat daftar aksi yang sejajar.",
        "connector_logic": "Latihan memilih connector sesuai hubungan ide.",
        "nominalization": "Review Advanced Lab bagian Nominalization.",
        "formal_ba_writing": "Latihan rewrite kalimat menjadi formal BA writing.",
    }
    return actions.get(topic_id, "Ulangi latihan grammar yang direkomendasikan.")


def _action_label(topic_id: str) -> str:
    return _recommended_action(topic_id).replace("Ulangi ", "Latihan ulang ").replace("Review ", "Review ")


def _weakness_reason(topic_id: str, score: float) -> str:
    if score == 0:
        return "Belum cukup latihan pada topik ini."
    if score < 60:
        return f"Mastery score masih rendah ({score})."
    if score < 70:
        return f"Mastery score belum stabil ({score})."
    return f"Topik ini masih bisa diperkuat walau score sudah {score}."


def _pattern_title(mistake_type: str, topic_title: str) -> str:
    titles = {
        "gerund_vs_main_verb": "Confusing -ing phrase with main verb",
        "main_verb_detection": "Difficulty finding the main verb",
        "missing_be_after_modal": "Missing be after modal",
        "modal_verb_pattern": "Incorrect modal verb pattern",
        "passive_voice": "Passive voice pattern issue",
        "parallel_structure": "Parallel structure issue",
        "connector_logic": "Connector logic issue",
        "nominalization": "Nominalization recognition issue",
        "formal_ba_writing": "Formal BA writing issue",
        "word_order": "Word order issue",
        "sentence_builder": "Sentence builder issue",
    }
    return titles.get(mistake_type, f"{topic_title} review pattern")


def _title_from_topic(topic_id: str) -> str:
    return topic_id.replace("_", " ").title()
