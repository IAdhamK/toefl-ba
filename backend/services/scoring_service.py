from __future__ import annotations

import time
from typing import Any


SCENARIO_QUESTIONS = [
    {
        "id": "s1",
        "title": "Ambiguous Requirement",
        "context": 'A stakeholder says, "The system should be more flexible."',
        "question": "What should the business analyst do first?",
        "options": [
            "Ask the developer to build the feature immediately.",
            "Clarify what flexible means through elicitation.",
            "Ignore the stakeholder because the statement is vague.",
            "Write the requirement exactly as spoken.",
        ],
        "answer": 1,
        "explanation": "A BA should clarify vague language before documenting or proposing a solution.",
    },
    {
        "id": "s2",
        "title": "Conflicting Stakeholder Priorities",
        "context": "The finance team wants strict approval controls, while sales wants a faster checkout process.",
        "question": "Which BA action best supports alignment?",
        "options": [
            "Choose the finance team's request because controls are safer.",
            "Choose the sales team's request because speed improves revenue.",
            "Facilitate a discussion about business goals, risks, and measurable trade-offs.",
            "Send both requests directly to developers.",
        ],
        "answer": 2,
        "explanation": "The BA should help stakeholders compare goals and trade-offs before solution decisions.",
    },
    {
        "id": "s3",
        "title": "Solution Before Problem",
        "context": 'A manager says, "We need a mobile app," but cannot explain the business problem.',
        "question": "What is the best first question?",
        "options": [
            "Which color should the mobile app use?",
            "What business outcome should this solution improve?",
            "Which developer is available this week?",
            "Can we skip user research?",
        ],
        "answer": 1,
        "explanation": "A BA should connect solution requests to business outcomes and user needs.",
    },
]


def score_reading(lesson: dict[str, Any], answers: dict[str, Any]) -> dict[str, Any]:
    questions = lesson.get("questions", [])
    if not questions:
        return {"score": 0, "correct": 0, "total": 0, "details": []}

    correct = 0
    details = []
    for question in questions:
        selected = answers.get(question["id"])
        if isinstance(selected, str) and selected.isdigit():
            selected = int(selected)
        is_correct = selected == question.get("answer")
        correct += 1 if is_correct else 0
        details.append(
            {
                "questionId": question["id"],
                "isCorrect": is_correct,
                "correctAnswer": question.get("answer"),
                "explanation": question.get("explanation", ""),
            }
        )
    return {
        "score": round((correct / len(questions)) * 100),
        "correct": correct,
        "total": len(questions),
        "details": details,
    }


def score_vocabulary(item: dict[str, Any], answer: str) -> dict[str, Any]:
    normalized = (answer or "").strip().lower()
    expected = [
        str(item.get("answer", "")).strip().lower(),
        str(item.get("meaningId", "")).strip().lower(),
        str(item.get("meaning_id", "")).strip().lower(),
    ]
    is_correct = normalized in expected
    return {
        "score": 100 if is_correct else 0,
        "isCorrect": is_correct,
        "correctAnswer": item.get("answer"),
        "explanation": "Makna sudah sesuai konteks BA." if is_correct else "Perhatikan contoh kalimat dan makna Indonesia.",
    }


def evaluate_writing(text: str) -> dict[str, Any]:
    lowered = text.lower()
    issues = []
    score = 82
    if "must flexible" in lowered:
        issues.append("Use 'must be flexible' because flexible is an adjective.")
        score -= 14
    if "all user" in lowered:
        issues.append("Use plural form: all users.")
        score -= 8
    if "faster" in lowered and not any(word in lowered for word in ["within", "seconds", "minutes", "by "]):
        issues.append("The requirement needs a measurable target for 'faster'.")
        score -= 7
    if not any(word in lowered for word in ["stakeholder", "requirement", "system", "report", "user"]):
        issues.append("Add clearer Business Analyst context.")
        score -= 6
    score = max(40, min(100, score))
    return {
        "score": score,
        "issues": issues or ["The writing is understandable. Improve precision with measurable acceptance criteria."],
        "revised": "The system must be flexible enough to generate reports faster for different user roles.",
        "recommendation": "Write one measurable acceptance criterion using a number, condition, or deadline.",
    }


def score_scenario(question_id: str, selected: int) -> dict[str, Any]:
    question = next((item for item in SCENARIO_QUESTIONS if item["id"] == question_id), None)
    if not question:
        return {"error": "Scenario question not found"}
    is_correct = selected == question["answer"]
    return {
        "score": 100 if is_correct else 0,
        "isCorrect": is_correct,
        "correctAnswer": question["answer"],
        "explanation": question["explanation"],
    }


def attempt_id(module: str) -> str:
    return f"{module.lower()}-{int(time.time() * 1000)}"
