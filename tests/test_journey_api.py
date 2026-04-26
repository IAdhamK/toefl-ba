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


def test_journey_summary_shape():
    status, data = call("/journey/summary")
    assert status == 200
    assert "journey" in data
    assert len(data["skills"]) == 6


def test_journey_attempt_updates_progress():
    status, data = call(
        "/journey/attempt",
        {
            "user_id": "default-user",
            "skill_type": "grammar",
            "activity_id": "test-grammar",
            "activity_type": "unit_shape_check",
            "score": 7,
            "max_score": 10,
            "mistakes": ["subject verb"],
            "feedback": "Keep practicing.",
        },
    )
    assert status == 201
    assert data["journey_update"]["skill_type"] == "grammar"
