LISTENING_SCENARIO = {
    "id": "listening-1",
    "title": "Stakeholder Interview: Reporting Delay",
    "transcript": "Stakeholder: The monthly report is always late. Analyst: What causes the delay? Stakeholder: Data from two departments arrives in different formats. Analyst: So the main issue is inconsistent input data before consolidation.",
    "question": "What is the main issue discussed in the meeting?",
    "answer": "Inconsistent input data before consolidation.",
    "keywords": ["inconsistent", "format", "data", "consolidation"],
    "audio": {
        "mode": "mock",
        "url": None,
        "durationSeconds": 42,
        "note": "Future TTS provider will generate audio from the transcript here.",
    },
}


def generate_listening_scenario() -> dict:
    # Future integration point: replace mock metadata with TTS-generated audio,
    # transcript timestamps, and optional STT answer capture.
    return LISTENING_SCENARIO


def evaluate_listening(answer: str) -> dict:
    lowered = answer.lower()
    matches = [keyword for keyword in LISTENING_SCENARIO["keywords"] if keyword in lowered]
    score = min(100, 35 + len(matches) * 20)
    return {
        "score": score,
        "isCorrect": score >= 75,
        "idealAnswer": LISTENING_SCENARIO["answer"],
        "explanation": "The stakeholder says the delay comes from department data arriving in different formats before consolidation.",
    }
