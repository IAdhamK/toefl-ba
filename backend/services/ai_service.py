from __future__ import annotations

import json
import os
from urllib import request

from backend.services.grammar_service import grammar_breakdown, indonesian_help
from backend.services.progress_service import recommendation
from backend.services.scoring_service import evaluate_writing


PROMPT_TEMPLATES = {
    "toefl_reading_explanation": "Explain this TOEFL reading passage in beginner Indonesian with Business Analyst context.",
    "grammar_breakdown": "Break down subject, main verb, phrases, and meaning in simple Indonesian.",
    "subject_verb_detection": "Find the subject and finite verb. Explain why modifiers are not the main verb.",
    "vocabulary_explanation": "Explain the vocabulary in Indonesian, then give one Business Analyst example.",
    "writing_feedback": "Evaluate clarity, grammar, measurable requirement quality, and give a revised sentence.",
    "next_lesson_recommendation": "Recommend the next small learning step based on weakest skill and progress.",
}


class AIService:
    def __init__(self) -> None:
        self.provider = os.getenv("LLM_PROVIDER", "mock").lower()
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    def chat(self, message: str, context: dict | None = None) -> str:
        if self.api_key and self.provider in {"openai", "openrouter", "compatible"}:
            return self._compatible_chat(message, context or {})
        return self._mock_chat(message)

    def explain_sentence(self, text: str, help_type: str = "simple") -> dict:
        if self.api_key and self.provider in {"openai", "openrouter", "compatible"}:
            reply = self._compatible_chat(
                f"{PROMPT_TEMPLATES['toefl_reading_explanation']}\n\nText: {text}",
                {"help_type": help_type},
            )
            return {"simpleMeaning": reply, "keywords": [], "structure": "", "explanation": reply, "example": ""}
        return indonesian_help(text, help_type)

    def grammar_breakdown(self, sentence: str) -> dict:
        return grammar_breakdown(sentence)

    def writing_feedback(self, text: str) -> dict:
        if self.api_key and self.provider in {"openai", "openrouter", "compatible"}:
            reply = self._compatible_chat(f"{PROMPT_TEMPLATES['writing_feedback']}\n\nWriting: {text}", {})
            result = evaluate_writing(text)
            result["aiFeedback"] = reply
            return result
        return evaluate_writing(text)

    def recommend_next_step(self, progress: dict[str, int]) -> dict:
        return recommendation(progress)

    def _mock_chat(self, message: str) -> str:
        text = message.lower()
        if "operating" in text or "verb" in text:
            return "Dalam kalimat BA, operating biasanya bukan main verb jika ia menerangkan noun sebelumnya. Main verb membawa aksi utama, misalnya must elicit atau must ensure."
        if "requirement" in text:
            return "Requirement yang baik harus jelas, dapat diuji, dan tidak ambigu. Jika stakeholder berkata flexible, BA perlu bertanya kondisi, aktor, dan ukuran keberhasilannya."
        if "rekomendasi" in text or "latihan" in text:
            return "Latihan hari ini: pilih satu passage BA, cari main idea, lalu bedah satu kalimat panjang menjadi subject, main verb, dan phrase."
        return "Mulai dari subject dan main verb dulu. Setelah itu baru baca phrase tambahan, clause, dan konteks BA seperti stakeholder, requirement, atau business goal."

    def _compatible_chat(self, message: str, context: dict) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are TOEFL Analyst AI. Explain TOEFL and Business Analyst English in simple Indonesian for beginners.",
                },
                {"role": "user", "content": f"{message}\n\nContext: {json.dumps(context, ensure_ascii=False)}"},
            ],
            "temperature": 0.3,
        }
        req = request.Request(
            f"{self.base_url.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=20) as response:
                data = json.loads(response.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
        except Exception:
            return self._mock_chat(message)


ai_service = AIService()
