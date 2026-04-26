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

    status, daily_vocab = call("/vocabulary/daily")
    assert_ok("daily vocabulary", status == 200 and len(daily_vocab["items"]) == 25)

    lesson = lessons["lessons"][0]
    answers = {question["id"]: question["answer"] for question in lesson["questions"]}
    status, reading = call("/reading/submit-answer", {"lessonId": lesson["id"], "answers": answers})
    assert_ok("reading scoring", status == 200 and reading["score"] == 100)

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

    print("Selesai. API utama berjalan baik.")


if __name__ == "__main__":
    main()
