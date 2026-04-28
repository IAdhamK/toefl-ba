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
    assert_ok("grammar breakdown", status == 200 and "analysis" in grammar)

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
