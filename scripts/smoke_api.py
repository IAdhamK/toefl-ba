from urllib import request
import json


BASE_URL = "http://127.0.0.1:8001/api"


def call(path, payload=None):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = request.Request(f"{BASE_URL}{path}", data=data, headers=headers)
    with request.urlopen(req, timeout=5) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def assert_ok(name, condition):
    if not condition:
        raise AssertionError(f"{name} failed")
    print(f"ok - {name}")


def main():
    print("Smoke test TOEFL Analyst AI API")
    print(f"Target: {BASE_URL}")

    status, health = call("/health")
    assert_ok("health check FastAPI", status == 200 and health["ok"])

    status, lessons = call("/lessons")
    assert_ok("lessons", status == 200 and len(lessons["lessons"]) > 0)

    status, progress = call("/progress/summary")
    assert_ok("progress summary", status == 200 and "progress" in progress)

    status, journey = call("/journey/summary")
    assert_ok("journey summary", status == 200 and "journey" in journey)

    status, skills = call("/journey/skills")
    assert_ok("skill journeys", status == 200 and len(skills["skills"]) == 6)

    status, attempt = call(
        "/journey/attempt",
        {
            "user_id": "default-user",
            "skill_type": "reading",
            "activity_id": "smoke-reading",
            "activity_type": "smoke_test",
            "score": 8,
            "max_score": 10,
            "mistakes": [],
            "feedback": "Good progress.",
        },
    )
    assert_ok("save journey attempt", status == 201 and "journey_update" in attempt)

    status, continue_learning = call("/journey/continue")
    assert_ok("continue learning", status == 200 and "recommended_module" in continue_learning)

    status, daily_plan = call("/journey/daily-plan")
    assert_ok("daily plan", status == 200 and len(daily_plan["plan"]) == 3)

    status, review_list = call("/journey/review-list")
    assert_ok("review list", status == 200 and "weak_vocabulary" in review_list)

    status, adaptive = call("/journey/adaptive-practice")
    assert_ok("adaptive practice", status == 200 and "tasks" in adaptive and len(adaptive["tasks"]) == 3)

    status, mentor = call("/journey/mentor-summary")
    assert_ok("adaptive mentor summary", status == 200 and "message" in mentor)

    status, adaptive_done = call(
        "/journey/adaptive-practice/complete",
        {
            "user_id": "default-user",
            "skill_type": "grammar",
            "score": 75,
            "max_score": 100,
            "notes": "Smoke adaptive practice complete.",
        },
    )
    assert_ok("complete adaptive practice", status == 200 and "journey_update" in adaptive_done)

    status, daily_vocab = call("/vocabulary/daily")
    assert_ok("daily vocabulary", status == 200 and len(daily_vocab["items"]) == 25)

    lesson = lessons["lessons"][0]
    answers = {question["id"]: question["answer"] for question in lesson["questions"]}
    status, reading = call("/reading/submit-answer", {"lessonId": lesson["id"], "answers": answers})
    assert_ok("reading scoring", status == 200 and reading["score"] == 100 and "reading_journey_update" in reading)

    status, reading_journey = call("/reading/journey")
    assert_ok(
        "reading journey",
        status == 200
        and "reading_journey" in reading_journey
        and "reading_level" in reading_journey["reading_journey"]
        and "sub_skill_mastery" in reading_journey["reading_journey"],
    )

    status, reading_levels = call("/reading/levels")
    assert_ok("reading levels", status == 200 and len(reading_levels["levels"]) == 10)

    status, reading_recommendation = call("/reading/recommendation")
    assert_ok("reading recommendation", status == 200 and "recommended_action" in reading_recommendation["recommendation"])

    status, reading_attempt = call(
        "/reading/attempt",
        {
            "user_id": "default-user",
            "passage_id": "smoke-reading-phase-1",
            "score": 82,
            "max_score": 100,
            "subskill_scores": {
                "general_meaning": 90,
                "main_idea": 80,
                "detail_information": 75,
                "vocabulary_context": 70,
            },
            "feedback": "Smoke Reading Journey attempt.",
        },
    )
    assert_ok("save reading attempt", status == 201 and "reading_journey" in reading_attempt)

    status, reading_subskills = call("/reading/subskills")
    assert_ok(
        "reading subskills",
        status == 200
        and len(reading_subskills["subskills"]) == 10
        and "next_recommended_subskill" in reading_subskills,
    )

    status, reading_trainer = call("/reading/trainer/main_idea")
    assert_ok(
        "reading trainer main idea",
        status == 200
        and reading_trainer["sub_skill"] == "main_idea"
        and "question" in reading_trainer
        and reading_trainer["question"]["sub_skill"] == "main_idea",
    )

    status, reading_main_idea_attempt = call(
        "/reading/attempt",
        {
            "user_id": "default-user",
            "passage_id": "trainer-main-idea-1",
            "activity_type": "reading_subskill_trainer",
            "sub_skill": "main_idea",
            "selected": 1,
        },
    )
    assert_ok(
        "reading attempt main idea subskill",
        status == 201
        and reading_main_idea_attempt["answer_feedback"]["is_correct"]
        and "answer_review" in reading_main_idea_attempt
        and "distractor_analysis" in reading_main_idea_attempt
        and reading_main_idea_attempt["next_recommended_subskill"],
    )

    status, reading_vocab_attempt = call(
        "/reading/attempt",
        {
            "user_id": "default-user",
            "passage_id": "trainer-vocab-1",
            "activity_type": "reading_subskill_trainer",
            "sub_skill": "vocabulary_context",
            "selected": 0,
        },
    )
    assert_ok(
        "reading attempt vocabulary context subskill",
        status == 201
        and reading_vocab_attempt["answer_feedback"]["is_correct"]
        and reading_vocab_attempt["reading_journey"]["sub_skill_mastery"],
    )

    guided_payload = {
        "lesson_id": lesson["id"],
        "title": lesson["title"],
        "passage": lesson["passage"],
        "vocabulary": lesson.get("vocabulary", []),
        "question_text": lesson["questions"][0]["text"],
    }
    status, guided_steps = call("/reading/guided-steps", guided_payload)
    assert_ok(
        "reading guided steps",
        status == 200
        and guided_steps["total_steps"] == 7
        and guided_steps["steps"][0]["id"] == "title"
        and guided_steps["steps"][2]["subject"],
    )

    status, passage_map = call("/reading/passage-map", guided_payload)
    assert_ok(
        "reading passage map",
        status == 200
        and len(passage_map["paragraphs"]) >= 1
        and "simple_meaning" in passage_map["paragraphs"][0]
        and "beginner_tip" in passage_map["paragraphs"][0],
    )

    review_payload = {
        "passage": lesson["passage"],
        "question": lesson["questions"][0],
        "selected": 0,
        "correct_answer": lesson["questions"][0]["answer"],
        "explanation": lesson["questions"][0]["explanation"],
    }
    status, answer_review = call("/reading/review-answer", review_payload)
    review = answer_review.get("answer_review", {})
    assert_ok(
        "reading answer review",
        status == 200
        and not review["is_correct"]
        and "evidence_sentence" in review
        and len(review["distractor_analysis"]) == len(lesson["questions"][0]["options"])
        and "next_practice_recommendation" in review,
    )

    status, reading_review = call("/reading/review")
    assert_ok(
        "reading review",
        status == 200
        and "weakness_summary" in reading_review
        and "mistake_patterns" in reading_review
        and "review_items" in reading_review
        and "mentor_message" in reading_review,
    )

    status, mistake_patterns = call("/reading/mistake-patterns")
    assert_ok(
        "reading mistake patterns",
        status == 200
        and "patterns" in mistake_patterns
        and "repeated_wrong_question_types" in mistake_patterns,
    )

    status, review_queue = call("/reading/review-queue")
    assert_ok(
        "reading review queue",
        status == 200
        and "review_items" in review_queue
        and len(review_queue["review_items"]) >= 1,
    )

    status, simulation = call("/reading/simulation/start", {"mode": "short", "user_id": "default-user"})
    assert_ok(
        "reading simulation start",
        status == 200
        and simulation["mode"] == "short"
        and simulation["duration_minutes"] == 10
        and simulation["question_count"] == 5,
    )

    simulation_answers = {}
    for passage in simulation["passages"]:
        for question in passage["questions"]:
            simulation_answers[question["id"]] = question["answer"]
    status, simulation_result = call(
        "/reading/simulation/submit",
        {
            "user_id": "default-user",
            "session_id": simulation["session_id"],
            "mode": simulation["mode"],
            "session": simulation,
            "answers": simulation_answers,
            "time_spent_seconds": 120,
        },
    )
    assert_ok(
        "reading simulation submit",
        status == 200
        and simulation_result["total_score"] == 100
        and "sub_skill_breakdown" in simulation_result
        and "answer_review_summary" in simulation_result,
    )

    status, simulation_history = call("/reading/simulation/history?user_id=default-user")
    assert_ok(
        "reading simulation history",
        status == 200
        and "history" in simulation_history
        and any(item["session_id"] == simulation["session_id"] for item in simulation_history["history"]),
    )

    first_vocab = daily_vocab["items"][0]
    status, vocab_score = call("/scoring/vocabulary", {"itemId": first_vocab["id"], "answer": first_vocab["answer"]})
    assert_ok("vocabulary scoring", status == 200 and vocab_score["isCorrect"])

    status, grammar = call(
        "/grammar/breakdown",
        {"sentence": "A business analyst operating within a complex enterprise environment must elicit requirements."},
    )
    grammar_analysis = grammar.get("analysis", {})
    old_fields = {"subject", "mainVerb", "phrase", "pattern", "translation", "explanation"}
    deep_fields = {
        "sentence_level",
        "sentence_type",
        "main_subject",
        "main_verb",
        "grammar_patterns",
        "simple_meaning_id",
        "next_practice",
        "recommended_topic_id",
    }
    assert_ok(
        "grammar breakdown",
        status == 200
        and "analysis" in grammar
        and old_fields.issubset(grammar_analysis.keys())
        and deep_fields.issubset(grammar_analysis.keys()),
    )

    status, grammar_sample_1 = call(
        "/grammar/breakdown",
        {"sentence": "A business analyst must elicit requirements from stakeholders."},
    )
    sample_1 = grammar_sample_1.get("analysis", {})
    assert_ok(
        "deep grammar sample modal",
        status == 200
        and old_fields.issubset(sample_1.keys())
        and deep_fields.issubset(sample_1.keys())
        and "modal verb" in sample_1.get("grammar_patterns", []),
    )

    complex_sentence = (
        "A business analyst operating within a complex enterprise environment must not only elicit requirements "
        "but also ensure alignment between stakeholder needs and organizational strategy."
    )
    status, grammar_sample_2 = call("/grammar/breakdown", {"sentence": complex_sentence})
    sample_2 = grammar_sample_2.get("analysis", {})
    assert_ok(
        "deep grammar sample complex",
        status == 200
        and sample_2.get("sentence_level") in ("intermediate", "advanced")
        and ("modal verb" in sample_2.get("grammar_patterns", []) or "parallel structure" in sample_2.get("grammar_patterns", []))
        and ("operating" in sample_2.get("common_trap", "").lower() or "main verb" in sample_2.get("common_trap", "").lower())
        and sample_2.get("recommended_topic_id") in ("gerund_vs_main_verb", "reduced_relative_clause", "parallel_structure"),
    )

    advanced_sentence = (
        "The implementation of an integrated requirement management system is expected to improve traceability, "
        "reduce ambiguity, and support strategic alignment."
    )
    status, grammar_sample_3 = call("/grammar/breakdown", {"sentence": advanced_sentence})
    sample_3 = grammar_sample_3.get("analysis", {})
    assert_ok(
        "deep grammar sample advanced",
        status == 200
        and any(pattern in sample_3.get("grammar_patterns", []) for pattern in ("nominalization", "passive voice", "parallel structure"))
        and sample_3.get("recommended_topic_id") in ("nominalization", "passive_voice", "parallel_structure")
        and sample_3.get("ba_context_meaning"),
    )

    status, grammar_deep = call("/grammar/breakdown/deep", {"sentence": complex_sentence})
    assert_ok(
        "grammar deep endpoint",
        status == 200
        and "analysis" in grammar_deep
        and grammar_deep["analysis"].get("recommended_topic_id") in ("gerund_vs_main_verb", "reduced_relative_clause", "parallel_structure"),
    )

    status, grammar_levels = call("/grammar/levels")
    level_ids = {level["id"] for level in grammar_levels.get("levels", [])}
    assert_ok(
        "grammar levels",
        status == 200 and {"basic", "intermediate", "advanced"}.issubset(level_ids),
    )

    status, grammar_topics = call("/grammar/topics")
    assert_ok(
        "grammar topics",
        status == 200 and grammar_topics["total"] >= 21 and len(grammar_topics["topics"]) >= 21,
    )

    status, grammar_basic_topics = call("/grammar/topics?level=basic")
    basic_topic_ids = {topic["id"] for topic in grammar_basic_topics.get("topics", [])}
    assert_ok(
        "grammar basic topics",
        status == 200
        and grammar_basic_topics["level"] == "basic"
        and "subject_verb" in basic_topic_ids,
    )

    status, subject_verb_topic = call("/grammar/topics/subject_verb")
    subject_verb = subject_verb_topic.get("topic", {})
    assert_ok(
        "grammar subject verb topic",
        status == 200
        and subject_verb.get("title")
        and subject_verb.get("explanation_id")
        and subject_verb.get("example_sentence")
        and subject_verb.get("beginner_tip"),
    )

    status, grammar_topic_summary = call("/grammar/topic-summary")
    summary = grammar_topic_summary.get("summary", {})
    assert_ok(
        "grammar topic summary",
        status == 200
        and summary.get("total_topics", 0) >= 21
        and summary.get("levels", {}).get("basic") >= 7,
    )

    status, grammar_next_topic = call("/grammar/next-topic")
    assert_ok(
        "grammar next topic",
        status == 200
        and grammar_next_topic.get("next_topic", {}).get("id")
        and grammar_next_topic.get("next_topic", {}).get("title"),
    )

    status, grammar_journey = call("/grammar/journey")
    grammar_journey_data = grammar_journey.get("grammar_journey", {})
    assert_ok(
        "grammar journey",
        status == 200
        and "grammar_level" in grammar_journey_data
        and "topic_mastery" in grammar_journey_data
        and isinstance(grammar_journey_data["topic_mastery"], list)
        and "next_recommended_topic" in grammar_journey_data,
    )

    status, grammar_attempt = call(
        "/grammar/attempt",
        {
            "user_id": "default-user",
            "topic_id": "subject_verb",
            "activity_type": "grammar_topic_attempt",
            "score": 80,
            "max_score": 100,
            "mistakes": [],
            "feedback": "User can identify subject and main verb.",
        },
    )
    assert_ok(
        "save grammar attempt",
        status == 201
        and "grammar_attempt" in grammar_attempt
        and "grammar_journey" in grammar_attempt
        and grammar_attempt["grammar_attempt"]["topic_id"] == "subject_verb"
        and grammar_attempt["grammar_attempt"]["accuracy"] == 80,
    )

    status, grammar_mastery = call("/grammar/mastery")
    assert_ok(
        "grammar mastery",
        status == 200
        and isinstance(grammar_mastery.get("topic_mastery"), list)
        and "weakest_topic" in grammar_mastery
        and "strongest_topic" in grammar_mastery
        and "next_recommended_topic" in grammar_mastery,
    )

    status, grammar_recommendation = call("/grammar/recommendation")
    recommendation = grammar_recommendation.get("recommendation", {})
    assert_ok(
        "grammar recommendation",
        status == 200
        and "recommended_topic" in recommendation
        and "next_action" in recommendation
        and "mentor_message" in recommendation,
    )

    status, grammar_basic_trainer_topics = call("/grammar/trainer/basic")
    basic_trainer_topic_ids = {topic["topic_id"] for topic in grammar_basic_trainer_topics.get("topics", [])}
    assert_ok(
        "grammar basic trainer topics",
        status == 200
        and "subject_verb" in basic_trainer_topic_ids,
    )

    status, subject_verb_trainer = call("/grammar/trainer/basic/subject_verb")
    trainer = subject_verb_trainer.get("trainer", {})
    assert_ok(
        "grammar basic trainer subject verb",
        status == 200
        and trainer.get("topic_id") == "subject_verb"
        and len(trainer.get("examples", [])) > 0
        and len(trainer.get("guided_items", [])) > 0
        and len(trainer.get("quiz_items", [])) > 0,
    )

    trainer_answers = {item["id"]: item["correct_answer"] for item in trainer["quiz_items"]}
    status, trainer_submit = call(
        "/grammar/trainer/basic/submit",
        {
            "user_id": "default-user",
            "topic_id": "subject_verb",
            "answers": trainer_answers,
        },
    )
    assert_ok(
        "grammar basic trainer submit",
        status == 200
        and "result" in trainer_submit
        and trainer_submit["result"]["score"] >= 70
        and "recommendation" in trainer_submit
        and "grammar_journey" in trainer_submit,
    )

    status, grammar_intermediate_topics = call("/grammar/trainer/intermediate")
    intermediate_topic_ids = {topic["topic_id"] for topic in grammar_intermediate_topics.get("topics", [])}
    assert_ok(
        "grammar intermediate trainer topics",
        status == 200
        and "gerund_vs_main_verb" in intermediate_topic_ids,
    )

    status, gerund_trainer_response = call("/grammar/trainer/intermediate/gerund_vs_main_verb")
    gerund_trainer = gerund_trainer_response.get("trainer", {})
    assert_ok(
        "grammar intermediate trainer gerund",
        status == 200
        and gerund_trainer.get("topic_id") == "gerund_vs_main_verb"
        and len(gerund_trainer.get("examples", [])) > 0
        and len(gerund_trainer.get("guided_items", [])) > 0
        and len(gerund_trainer.get("quiz_items", [])) > 0
        and len(gerund_trainer.get("trap_items", [])) > 0,
    )

    status, reduced_trainer_response = call("/grammar/trainer/intermediate/reduced_relative_clause")
    reduced_trainer = reduced_trainer_response.get("trainer", {})
    assert_ok(
        "grammar intermediate trainer reduced relative",
        status == 200
        and reduced_trainer.get("topic_id") == "reduced_relative_clause"
        and reduced_trainer.get("common_trap"),
    )

    intermediate_answers = {
        item["id"]: item["correct_answer"]
        for item in gerund_trainer.get("quiz_items", []) + gerund_trainer.get("trap_items", [])
    }
    status, intermediate_submit = call(
        "/grammar/trainer/intermediate/submit",
        {
            "user_id": "default-user",
            "topic_id": "gerund_vs_main_verb",
            "answers": intermediate_answers,
        },
    )
    assert_ok(
        "grammar intermediate trainer submit",
        status == 200
        and "result" in intermediate_submit
        and intermediate_submit["result"]["level"] == "intermediate"
        and intermediate_submit["result"]["score"] >= 70
        and "recommendation" in intermediate_submit
        and "grammar_journey" in intermediate_submit,
    )

    status, error_categories = call("/grammar/error-correction/categories")
    error_types = {category["error_type"] for category in error_categories.get("categories", [])}
    assert_ok(
        "grammar error correction categories",
        status == 200 and "missing_be_after_modal" in error_types,
    )

    status, error_items = call("/grammar/error-correction")
    assert_ok(
        "grammar error correction items",
        status == 200 and error_items.get("total", 0) > 0 and len(error_items.get("items", [])) > 0,
    )

    status, basic_error_items = call("/grammar/error-correction?level=basic")
    assert_ok(
        "grammar error correction basic filter",
        status == 200
        and len(basic_error_items.get("items", [])) > 0
        and all(item["level"] == "basic" for item in basic_error_items["items"]),
    )

    status, missing_be_response = call("/grammar/error-correction/missing_be_after_modal")
    missing_be_items = missing_be_response.get("items", [])
    assert_ok(
        "grammar error correction missing be",
        status == 200
        and missing_be_response.get("category", {}).get("error_type") == "missing_be_after_modal"
        and len(missing_be_items) >= 1,
    )

    status, passive_error_response = call("/grammar/error-correction/passive_voice_error")
    assert_ok(
        "grammar error correction passive voice",
        status == 200
        and passive_error_response.get("category", {}).get("error_type") == "passive_voice_error"
        and len(passive_error_response.get("items", [])) >= 1,
    )

    error_answers = {item["id"]: item["correct_answer"] for item in missing_be_items}
    status, error_submit = call(
        "/grammar/error-correction/submit",
        {
            "user_id": "default-user",
            "error_type": "missing_be_after_modal",
            "answers": error_answers,
        },
    )
    error_details = error_submit.get("result", {}).get("details", [])
    assert_ok(
        "grammar error correction submit",
        status == 200
        and "result" in error_submit
        and error_submit["result"]["score"] >= 70
        and "recommendation" in error_submit
        and len(error_details) > 0
        and all("corrected_sentence" in item for item in error_details),
    )

    status, builder_levels = call("/grammar/sentence-builder/levels")
    builder_level_ids = {level["id"] for level in builder_levels.get("levels", [])}
    assert_ok(
        "grammar sentence builder levels",
        status == 200 and {"basic", "intermediate", "advanced_preview"}.issubset(builder_level_ids),
    )

    status, builder_items = call("/grammar/sentence-builder")
    assert_ok(
        "grammar sentence builder items",
        status == 200 and builder_items.get("total", 0) > 0 and len(builder_items.get("items", [])) > 0,
    )

    status, basic_builder_items = call("/grammar/sentence-builder?level=basic")
    assert_ok(
        "grammar sentence builder basic filter",
        status == 200
        and len(basic_builder_items.get("items", [])) > 0
        and all(item["level"] == "basic" for item in basic_builder_items["items"]),
    )

    status, arrange_builder_items = call("/grammar/sentence-builder?mode=arrange_words")
    assert_ok(
        "grammar sentence builder arrange filter",
        status == 200
        and len(arrange_builder_items.get("items", [])) > 0
        and all(item["mode"] == "arrange_words" for item in arrange_builder_items["items"]),
    )

    status, builder_detail = call("/grammar/sentence-builder/arrange_basic_modal_1")
    builder_item = builder_detail.get("item", {})
    assert_ok(
        "grammar sentence builder detail",
        status == 200
        and builder_item.get("expected_answer") == "A business analyst must elicit requirements."
        and builder_item.get("explanation_id"),
    )

    status, builder_submit = call(
        "/grammar/sentence-builder/submit",
        {
            "user_id": "default-user",
            "level": "basic",
            "mode": "arrange_words",
            "answers": {
                "arrange_basic_modal_1": "A business analyst must elicit requirements.",
                "arrange_basic_report_1": "The system generates reports automatically.",
                "arrange_basic_scope_1": "The analyst clarifies the scope.",
            },
        },
    )
    builder_details = builder_submit.get("result", {}).get("details", [])
    assert_ok(
        "grammar sentence builder submit",
        status == 200
        and "result" in builder_submit
        and builder_submit["result"]["score"] >= 70
        and "recommendation" in builder_submit
        and len(builder_details) > 0
        and all("expected_answer" in item for item in builder_details),
    )

    status, advanced_topics = call("/grammar/advanced/topics")
    advanced_topic_ids = {topic["topic_id"] for topic in advanced_topics.get("topics", [])}
    assert_ok(
        "grammar advanced topics",
        status == 200 and "nominalization" in advanced_topic_ids,
    )

    status, nominalization_response = call("/grammar/advanced/topics/nominalization")
    nominalization_topic = nominalization_response.get("topic", {})
    assert_ok(
        "grammar advanced nominalization topic",
        status == 200
        and nominalization_topic.get("beginner_bridge")
        and len(nominalization_topic.get("examples", [])) >= 3
        and len(nominalization_topic.get("practice_items", [])) >= 4
        and len(nominalization_topic.get("rewrite_items", [])) >= 2,
    )

    status, formal_ba_response = call("/grammar/advanced/topics/formal_ba_writing")
    formal_ba_topic = formal_ba_response.get("topic", {})
    assert_ok(
        "grammar advanced formal BA topic",
        status == 200
        and formal_ba_topic.get("professional_usage")
        and len(formal_ba_topic.get("rewrite_items", [])) >= 4,
    )

    status, advanced_practice = call("/grammar/advanced/practice?topic_id=nominalization")
    practice_items = advanced_practice.get("items", [])
    assert_ok(
        "grammar advanced practice items",
        status == 200 and len(practice_items) > 0,
    )

    status, advanced_rewrite = call("/grammar/advanced/rewrite?topic_id=formal_ba_writing")
    rewrite_items = advanced_rewrite.get("items", [])
    assert_ok(
        "grammar advanced rewrite items",
        status == 200 and len(rewrite_items) > 0,
    )

    advanced_practice_answers = {item["id"]: item["correct_answer"] for item in practice_items}
    status, advanced_practice_submit = call(
        "/grammar/advanced/practice/submit",
        {
            "user_id": "default-user",
            "topic_id": "nominalization",
            "answers": advanced_practice_answers,
        },
    )
    assert_ok(
        "grammar advanced practice submit",
        status == 200
        and "result" in advanced_practice_submit
        and advanced_practice_submit["result"]["score"] >= 70
        and "recommendation" in advanced_practice_submit,
    )

    advanced_rewrite_answers = {item["id"]: item["expected_answer"] for item in rewrite_items}
    status, advanced_rewrite_submit = call(
        "/grammar/advanced/rewrite/submit",
        {
            "user_id": "default-user",
            "topic_id": "formal_ba_writing",
            "answers": advanced_rewrite_answers,
        },
    )
    rewrite_details = advanced_rewrite_submit.get("result", {}).get("details", [])
    assert_ok(
        "grammar advanced rewrite submit",
        status == 200
        and "result" in advanced_rewrite_submit
        and advanced_rewrite_submit["result"]["score"] >= 70
        and "recommendation" in advanced_rewrite_submit
        and len(rewrite_details) > 0
        and all("expected_answer" in item or "required_keywords" in item for item in rewrite_details),
    )

    status, grammar_review = call("/grammar/review")
    assert_ok(
        "grammar review",
        status == 200
        and "weakness_summary" in grammar_review
        and "mistake_patterns" in grammar_review
        and "review_queue" in grammar_review
        and "recommended_practice" in grammar_review,
    )

    status, grammar_patterns = call("/grammar/mistake-patterns")
    assert_ok(
        "grammar mistake patterns",
        status == 200
        and isinstance(grammar_patterns.get("patterns"), list)
        and "total" in grammar_patterns,
    )

    status, grammar_review_queue = call("/grammar/review-queue")
    assert_ok(
        "grammar review queue",
        status == 200
        and isinstance(grammar_review_queue.get("review_items"), list)
        and "next_review" in grammar_review_queue,
    )

    status, grammar_weakness = call("/grammar/weakness-summary")
    assert_ok(
        "grammar weakness summary",
        status == 200
        and "weakness_summary" in grammar_weakness
        and "primary_weakness" in grammar_weakness["weakness_summary"],
    )

    status, grammar_recommended_practice = call("/grammar/recommended-practice")
    assert_ok(
        "grammar recommended practice",
        status == 200
        and "recommended_practice" in grammar_recommended_practice
        and grammar_recommended_practice["recommended_practice"].get("target_endpoint"),
    )

    status, grammar_sim_modes = call("/grammar/simulation/modes")
    grammar_sim_mode_ids = {mode["id"] for mode in grammar_sim_modes.get("modes", [])}
    assert_ok(
        "grammar simulation modes",
        status == 200 and {"short", "medium", "full"}.issubset(grammar_sim_mode_ids),
    )

    status, grammar_sim_start = call(
        "/grammar/simulation/start",
        {"user_id": "default-user", "mode": "short"},
    )
    grammar_session = grammar_sim_start.get("session", {})
    assert_ok(
        "grammar simulation start",
        status == 200
        and grammar_session.get("session_id")
        and grammar_session.get("duration_minutes") == 10
        and len(grammar_session.get("questions", [])) == 10,
    )

    grammar_sim_answers = {question["id"]: question["correct_answer"] for question in grammar_session["questions"]}
    status, grammar_sim_submit = call(
        "/grammar/simulation/submit",
        {
            "user_id": "default-user",
            "session_id": grammar_session["session_id"],
            "mode": "short",
            "session": grammar_session,
            "answers": grammar_sim_answers,
            "time_spent_seconds": 420,
        },
    )
    grammar_sim_result = grammar_sim_submit.get("result", {})
    assert_ok(
        "grammar simulation submit",
        status == 200
        and "total_score" in grammar_sim_result
        and "level_breakdown" in grammar_sim_result
        and "subskill_breakdown" in grammar_sim_result
        and "answer_review_summary" in grammar_sim_result
        and "recommendation" in grammar_sim_result,
    )

    status, grammar_sim_result_lookup = call(f"/grammar/simulation/result/{grammar_session['session_id']}")
    assert_ok(
        "grammar simulation result lookup",
        status == 200
        and grammar_sim_result_lookup.get("result", {}).get("session_id") == grammar_session["session_id"],
    )

    status, grammar_sim_history = call("/grammar/simulation/history?user_id=default-user")
    assert_ok(
        "grammar simulation history",
        status == 200 and isinstance(grammar_sim_history.get("history"), list),
    )

    status, writing = call("/writing/evaluate", {"text": "The system must flexible for all user and make report faster."})
    assert_ok("writing evaluate", status == 200 and writing["score"] < 82)

    status, listening = call("/listening/submit-answer", {"answer": "The issue is inconsistent data formats before consolidation."})
    assert_ok("listening scoring", status == 200 and listening["isCorrect"])

    status, scenario = call("/scenario/submit-answer", {"questionId": "s1", "selected": 1})
    assert_ok("scenario scoring", status == 200 and scenario["isCorrect"])

    status, tutor = call("/ai-tutor/recommendation", {"progress": {"Reading": 80, "Grammar": 20}})
    assert_ok("tutor recommendation", status == 200 and tutor["weakness"] == "Grammar")

    status, ai_chat = call("/ai/chat", {"message": "Explain requirement for beginner"})
    assert_ok("ai mock chat", status == 200 and "reply" in ai_chat)

    status, analytics = call(
        "/progress/analytics",
        {"progress": {"Reading": 80, "Grammar": 20}, "completedExercises": 2, "activity": [{"module": "Reading"}]},
    )
    assert_ok("progress analytics", status == 200 and analytics["analytics"]["weakestSkill"] == "Grammar")

    status, help_result = call(
        "/help/indonesian",
        {"text": "A business analyst must elicit requirements from stakeholders.", "type": "simple"},
    )
    assert_ok("indonesian help", status == 200 and "simpleMeaning" in help_result)

    contextual_samples = [
        (
            "bantuan id reading context",
            {
                "text": "A business analyst elicits requirements from stakeholders.",
                "module": "reading",
                "context_type": "reading_paragraph",
            },
        ),
        (
            "bantuan id grammar context",
            {
                "text": "Operating within a complex enterprise environment, the analyst must align stakeholder needs with strategy.",
                "module": "grammar",
                "context_type": "grammar_sentence",
            },
        ),
        (
            "bantuan id vocabulary context",
            {
                "text": "maintain",
                "module": "vocabulary",
                "context_type": "vocabulary_word",
            },
        ),
        (
            "bantuan id listening context",
            {
                "text": "What is the main purpose of the conversation?",
                "module": "listening",
                "context_type": "listening_question",
            },
        ),
        (
            "bantuan id scenario context",
            {
                "text": "The stakeholder reports that the current approval workflow causes delays.",
                "module": "scenario",
                "context_type": "scenario_case",
            },
        ),
    ]
    for name, payload in contextual_samples:
        status, contextual = call("/ai/contextual-help", payload)
        explanation = contextual.get("explanation", {})
        assert_ok(name, status == 200 and contextual["module"] == payload["module"] and "simple_meaning_id" in explanation)

    status, vocab_context = call(
        "/ai/contextual-help",
        {
            "text": "The analyst must maintain the approval workflow.",
            "module": "vocabulary",
            "context_type": "vocabulary_example",
        },
    )
    vocab_explanation = vocab_context.get("explanation", {})
    first_vocab = (vocab_explanation.get("important_vocabulary") or [{}])[0]
    assert_ok(
        "bantuan id word context meaning",
        status == 200
        and "one_word_meaning_id" in first_vocab
        and "contextual_meaning_id" in first_vocab
        and "word_contextual_meaning_id" in vocab_explanation,
    )

    status, question_context = call(
        "/ai/contextual-help",
        {
            "text": "What business outcome should this solution improve?",
            "module": "scenario",
            "context_type": "scenario_question",
        },
    )
    question_explanation = question_context.get("explanation", {})
    assert_ok(
        "bantuan id direct question meaning",
        status == 200
        and "hasil bisnis apa" in question_explanation.get("simple_meaning_id", "").lower()
    )

    reading_passage = (
        "A business analyst operating within a complex enterprise environment must not only elicit requirements "
        "but also ensure alignment between stakeholder needs and organizational strategy."
    )
    status, reading_question = call(
        "/ai/contextual-help",
        {
            "text": "What is the main idea of the passage?",
            "module": "reading",
            "context_type": "reading_question",
            "extra_context": {"passage_text": reading_passage},
        },
    )
    reading_question_explanation = reading_question.get("explanation", {})
    assert_ok(
        "bantuan id reading main idea question",
        status == 200
        and "ide utama" in reading_question_explanation.get("direct_meaning_id", "").lower()
        and "passage" in reading_question_explanation.get("direct_meaning_id", "").lower()
        and "detail" in reading_question_explanation.get("what_to_find", "").lower(),
    )

    option_context = {
        "passage_text": reading_passage,
        "question_text": "What is the main idea of the passage?",
        "correct_answer": "Business analysts must connect requirements with stakeholder needs and strategy.",
    }
    status, correct_option = call(
        "/ai/contextual-help",
        {
            "text": "Business analysts must connect requirements with stakeholder needs and strategy.",
            "module": "reading",
            "context_type": "reading_option",
            "extra_context": option_context,
        },
    )
    correct_option_explanation = correct_option.get("explanation", {})
    assert_ok(
        "bantuan id reading correct option",
        status == 200
        and "requirements" in correct_option_explanation.get("direct_meaning_id", "").lower()
        and "stakeholder" in correct_option_explanation.get("direct_meaning_id", "").lower()
        and "strategy" in correct_option_explanation.get("direct_meaning_id", "").lower()
        and ("sesuai" in correct_option_explanation.get("relation_to_context", "").lower() or "kuat" in correct_option_explanation.get("likely_correctness_hint", "").lower()),
    )

    status, wrong_option = call(
        "/ai/contextual-help",
        {
            "text": "Business analysts should write code immediately.",
            "module": "reading",
            "context_type": "reading_option",
            "extra_context": option_context,
        },
    )
    wrong_option_explanation = wrong_option.get("explanation", {})
    assert_ok(
        "bantuan id reading wrong option",
        status == 200
        and "kode" in wrong_option_explanation.get("direct_meaning_id", "").lower()
        and ("tidak didukung" in wrong_option_explanation.get("relation_to_context", "").lower() or "tidak sesuai" in wrong_option_explanation.get("relation_to_context", "").lower()),
    )

    status, contradictory_option = call(
        "/ai/contextual-help",
        {
            "text": "Organizational strategy is unrelated to requirements.",
            "module": "reading",
            "context_type": "reading_option",
            "extra_context": option_context,
        },
    )
    contradictory_explanation = contradictory_option.get("explanation", {})
    assert_ok(
        "bantuan id reading contradictory option",
        status == 200
        and ("bertentangan" in contradictory_explanation.get("relation_to_context", "").lower() or "tidak sesuai" in contradictory_explanation.get("relation_to_context", "").lower())
        and ("strategy" in contradictory_explanation.get("relation_to_context", "").lower() or "strategi" in contradictory_explanation.get("direct_meaning_id", "").lower())
        and "requirements" in contradictory_explanation.get("direct_meaning_id", "").lower(),
    )

    status, scenario_specific = call(
        "/ai/contextual-help",
        {
            "text": "The stakeholder reports that the current approval workflow causes delays.",
            "module": "scenario",
            "context_type": "scenario_case",
        },
    )
    scenario_explanation = scenario_specific.get("explanation", {})
    assert_ok(
        "bantuan id scenario specific meaning",
        status == 200
        and "alur persetujuan" in scenario_explanation.get("direct_meaning_id", "").lower()
        and "keterlambatan" in scenario_explanation.get("direct_meaning_id", "").lower()
        and "klarifikasi" in scenario_explanation.get("suggested_ba_action", "").lower(),
    )

    print("Selesai. API utama berjalan baik.")


if __name__ == "__main__":
    main()
