from __future__ import annotations

import json
import os
import re
import hashlib
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

    def contextual_help(
        self,
        text: str,
        module: str = "general",
        context_type: str = "general",
        user_level: str = "beginner",
        extra_context: dict | None = None,
    ) -> dict:
        cleaned_text = (text or "").strip()
        if self.api_key and self.provider in {"openai", "openrouter", "compatible"}:
            prompt = (
                "Explain the selected English content for an Indonesian beginner. "
                "Return practical help for TOEFL and Business Analyst learning. "
                "Use simple Indonesian and include meaning, sentence structure, key vocabulary, context, and tips."
                f"\n\nModule: {module}\nContext type: {context_type}\nText: {cleaned_text}"
            )
            reply = self._compatible_chat(prompt, extra_context or {})
            explanation = self._mock_contextual_explanation(cleaned_text, module, context_type)
            explanation["beginner_explanation"] = reply
            return self._contextual_response(cleaned_text, module, context_type, explanation, "llm")

        explanation = self._mock_contextual_explanation(cleaned_text, module, context_type)
        return self._contextual_response(cleaned_text, module, context_type, explanation, "mock")

    def _mock_chat(self, message: str) -> str:
        text = message.lower()
        if "operating" in text or "verb" in text:
            return "Dalam kalimat BA, operating biasanya bukan main verb jika ia menerangkan noun sebelumnya. Main verb membawa aksi utama, misalnya must elicit atau must ensure."
        if "requirement" in text:
            return "Requirement yang baik harus jelas, dapat diuji, dan tidak ambigu. Jika stakeholder berkata flexible, BA perlu bertanya kondisi, aktor, dan ukuran keberhasilannya."
        if "rekomendasi" in text or "latihan" in text:
            return "Latihan hari ini: pilih satu passage BA, cari main idea, lalu bedah satu kalimat panjang menjadi subject, main verb, dan phrase."
        return "Mulai dari subject dan main verb dulu. Setelah itu baru baca phrase tambahan, clause, dan konteks BA seperti stakeholder, requirement, atau business goal."

    def _contextual_response(self, text: str, module: str, context_type: str, explanation: dict, source: str) -> dict:
        digest = hashlib.sha1(f"{module}:{context_type}:{text}".encode("utf-8")).hexdigest()[:10]
        explanation_id = f"help-{digest}"
        return {
            "text": text,
            "module": module,
            "context_type": context_type,
            "explanation_id": explanation_id,
            "explanation": explanation,
            "source": source,
        }

    def _mock_contextual_explanation(self, text: str, module: str, context_type: str) -> dict:
        words = self._important_vocabulary(text)
        structure = self._simple_structure(text)
        base = {
            "simple_meaning_id": self._simple_meaning(text, module, context_type),
            "sentence_structure": structure["sentence_structure"],
            "subject": structure["subject"],
            "verb": structure["verb"],
            "object_or_complement": structure["object_or_complement"],
            "grammar_pattern": structure["grammar_pattern"],
            "important_vocabulary": words,
            "beginner_explanation": self._beginner_context(text, module, context_type),
            "tips": self._context_tip(module, context_type),
        }

        if module == "vocabulary" or context_type.startswith("vocabulary"):
            first_word = text.split()[0].strip(".,:;!?\"'") if text else "word"
            vocab_info = words[0] if words else {
                "word": first_word,
                "meaning_id": "makna perlu dilihat dari konteks",
                "one_word_meaning_id": "konteks",
                "contextual_meaning_id": "arti kata ini berubah sesuai contoh kalimat",
            }
            base.update(
                {
                    "word_meaning_id": vocab_info["meaning_id"],
                    "word_one_word_meaning_id": vocab_info.get("one_word_meaning_id", self._one_word_meaning(first_word)),
                    "word_contextual_meaning_id": vocab_info.get("contextual_meaning_id", self._contextual_word_meaning(first_word, text)),
                    "word_class": self._guess_word_class(first_word),
                    "pronunciation_hint": f"Baca pelan: {first_word.lower()}",
                    "memory_tip": f"Ingat {first_word} lewat contoh kerja Business Analyst, bukan hanya hafalan kamus.",
                    "example_sentence": f"The analyst needs to understand the word '{first_word}' in context.",
                    "ba_toefl_context": "Dalam TOEFL, kata ini sering diuji lewat makna sesuai kalimat. Dalam BA, pahami hubungannya dengan requirement, stakeholder, proses, atau keputusan.",
                }
            )

        if module == "writing" or context_type.startswith("writing"):
            base.update(
                {
                    "writing_meaning": "Kalimat ini mencoba menyampaikan kebutuhan atau ide kerja secara profesional.",
                    "grammar_issue": "Cek apakah subject dan verb sudah jelas, lalu pastikan requirement tidak terlalu umum.",
                    "better_sentence": self._better_sentence(text),
                    "improvement_reason": "Versi yang lebih baik biasanya lebih jelas, lebih terukur, dan lebih natural dalam bahasa Inggris bisnis.",
                }
            )

        if module == "listening" or context_type.startswith("listening"):
            base.update(
                {
                    "listening_keywords": [item["word"] for item in words[:4]] or ["main purpose", "problem", "detail"],
                    "speaker_intent": "Cari maksud pembicara: apakah menjelaskan masalah, meminta klarifikasi, atau memberi rekomendasi.",
                    "listening_tip": "Saat mendengar, tangkap kata kunci dan hubungan sebab-akibat. Tidak perlu memahami semua kata dulu.",
                }
            )

        if module == "scenario" or context_type.startswith("scenario"):
            base.update(
                {
                    "ba_context": "Ini adalah konteks kerja Business Analyst: memahami masalah, stakeholder, kebutuhan, dan langkah analisis.",
                    "business_problem": "Cari proses yang bermasalah, risiko, keterlambatan, data tidak konsisten, atau kebutuhan yang belum jelas.",
                    "stakeholders": "Stakeholder bisa berupa user, manager, product owner, customer, atau tim operasional.",
                    "answer_hint": "Pilih jawaban yang mengarah ke clarify, elicit, validate, atau align sebelum langsung membuat solusi.",
                }
            )

        return base

    def _important_vocabulary(self, text: str) -> list[dict[str, str]]:
        glossary = {
            "elicit": "menggali atau mendapatkan informasi",
            "elicits": "menggali atau mendapatkan informasi",
            "requirement": "kebutuhan sistem atau bisnis",
            "requirements": "kebutuhan sistem atau bisnis",
            "stakeholder": "pihak yang berkepentingan",
            "stakeholders": "pihak yang berkepentingan",
            "align": "menyelaraskan",
            "alignment": "keselarasan",
            "strategy": "strategi atau arah bisnis",
            "maintain": "menjaga atau merawat agar tetap berjalan",
            "approval": "persetujuan",
            "workflow": "alur kerja",
            "delay": "keterlambatan",
            "delays": "keterlambatan",
            "analyst": "orang yang menganalisis kebutuhan dan masalah",
            "clarify": "memperjelas",
            "validate": "memastikan kebenaran atau kesesuaian",
            "prioritize": "menentukan mana yang paling penting dulu",
            "assess": "menilai",
            "purpose": "tujuan",
            "conversation": "percakapan",
        }
        tokens = re.findall(r"[A-Za-z']+", text.lower())
        found = []
        seen = set()
        for token in tokens:
            if token in glossary and token not in seen:
                found.append(
                    {
                        "word": token,
                        "meaning_id": glossary[token],
                        "one_word_meaning_id": self._one_word_meaning(token),
                        "contextual_meaning_id": self._contextual_word_meaning(token, text),
                    }
                )
                seen.add(token)
        if not found and text:
            candidate = tokens[0] if tokens else text[:24]
            found.append(
                {
                    "word": candidate,
                    "meaning_id": "makna perlu dipahami dari konteks kalimat",
                    "one_word_meaning_id": self._one_word_meaning(candidate),
                    "contextual_meaning_id": self._contextual_word_meaning(candidate, text),
                }
            )
        return found[:6]

    def _one_word_meaning(self, word: str) -> str:
        one_word_map = {
            "elicit": "menggali",
            "elicits": "menggali",
            "requirement": "kebutuhan",
            "requirements": "kebutuhan",
            "stakeholder": "pemangku-kepentingan",
            "stakeholders": "pemangku-kepentingan",
            "align": "menyelaraskan",
            "alignment": "keselarasan",
            "strategy": "strategi",
            "maintain": "menjaga",
            "approval": "persetujuan",
            "workflow": "alur",
            "delay": "tertunda",
            "delays": "keterlambatan",
            "analyst": "analis",
            "clarify": "memperjelas",
            "validate": "memvalidasi",
            "prioritize": "memprioritaskan",
            "assess": "menilai",
            "purpose": "tujuan",
            "conversation": "percakapan",
        }
        return one_word_map.get((word or "").lower(), "konteks")

    def _contextual_word_meaning(self, word: str, text: str) -> str:
        lowered_word = (word or "").lower()
        lowered_text = (text or "").lower()
        if lowered_word in {"elicit", "elicits"} and "requirements" in lowered_text:
            return "Dalam kalimat ini, elicit berarti menggali requirement dari stakeholder lewat pertanyaan atau diskusi."
        if lowered_word in {"requirement", "requirements"}:
            return "Dalam konteks BA, requirement berarti kebutuhan bisnis atau sistem yang harus dipahami dan didokumentasikan."
        if lowered_word in {"stakeholder", "stakeholders"}:
            return "Dalam konteks BA, stakeholder adalah pihak yang memberi kebutuhan, terkena dampak, atau mengambil keputusan."
        if lowered_word in {"maintain"}:
            return "Dalam contoh kalimat tertentu, maintain bisa berarti menjaga proses, sistem, atau kualitas agar tetap berjalan baik."
        if lowered_word in {"approval"}:
            return "Dalam konteks workflow, approval berarti tahap persetujuan sebelum proses bisa lanjut."
        if lowered_word in {"workflow"}:
            return "Dalam konteks bisnis, workflow berarti rangkaian langkah kerja dari awal sampai selesai."
        if lowered_word in {"delay", "delays"}:
            return "Dalam kalimat ini, delay/delays menunjukkan proses menjadi lambat atau terlambat."
        if lowered_word in {"purpose"} and "conversation" in lowered_text:
            return "Dalam pertanyaan listening, purpose berarti tujuan utama percakapan."
        return "Dalam contoh kalimat ini, arti kata perlu disesuaikan dengan topik, subject, verb, dan tujuan kalimat."

    def _simple_structure(self, text: str) -> dict[str, str]:
        lowered = text.lower()
        if self._is_question_text(text):
            return self._question_structure(text)
        if self._is_short_option(text):
            return {
                "sentence_structure": "Pilihan jawaban pendek. Fokus pada arti pilihan ini, bukan bedah grammar panjang.",
                "subject": "",
                "verb": "",
                "object_or_complement": "",
                "grammar_pattern": "Answer option / phrase",
            }
        if "business analyst" in lowered:
            subject = "A business analyst / the analyst"
        elif "stakeholder" in lowered:
            subject = "The stakeholder"
        elif "system" in lowered:
            subject = "The system"
        else:
            words = text.split()
            subject = " ".join(words[:3]) if words else "Belum terdeteksi"

        verb = "must" if " must " in f" {lowered} " else "reports" if "reports" in lowered else "causes" if "causes" in lowered else "lihat kata kerja utama"
        if "elicit" in lowered:
            verb = "elicit / elicits"
        if "align" in lowered:
            verb = "align"
        if "maintain" in lowered:
            verb = "maintain"

        return {
            "sentence_structure": "Cari pelaku (subject), aksi utama (verb), lalu informasi tambahan.",
            "subject": subject,
            "verb": verb,
            "object_or_complement": self._object_hint(text),
            "grammar_pattern": "Subject + Verb + Object/Complement",
        }

    def _object_hint(self, text: str) -> str:
        lowered = text.lower()
        if "requirements" in lowered:
            return "requirements / stakeholder needs"
        if "workflow" in lowered:
            return "approval workflow / delays"
        if "conversation" in lowered:
            return "the main purpose of the conversation"
        if len(text.split()) > 6:
            return "bagian setelah verb berisi detail utama"
        return "belum jelas dari teks pendek ini"

    def _simple_meaning(self, text: str, module: str, context_type: str) -> str:
        direct_meaning = self._direct_indonesian_meaning(text)
        if direct_meaning:
            return direct_meaning
        lowered = text.lower()
        if "business analyst" in lowered and "requirements" in lowered:
            return "Seorang Business Analyst menggali kebutuhan dan menghubungkannya dengan tujuan bisnis atau stakeholder."
        if "approval workflow" in lowered:
            return "Stakeholder mengatakan alur persetujuan saat ini menyebabkan keterlambatan."
        if "main purpose" in lowered:
            return "Pertanyaan ini menanyakan tujuan utama percakapan."
        if module == "vocabulary":
            return f"Kata atau frasa '{text}' perlu dipahami dari konteks kalimat, bukan diterjemahkan satu per satu."
        return self._basic_contextual_translation(text)

    def _beginner_context(self, text: str, module: str, context_type: str) -> str:
        module_notes = {
            "reading": "Untuk Reading, cari ide utama dan kata kunci yang mirip maknanya dengan pilihan jawaban.",
            "grammar": "Untuk Grammar, jangan panik melihat kalimat panjang. Pecah dulu menjadi subject, verb, dan informasi tambahan.",
            "vocabulary": "Untuk Vocabulary, lihat contoh kalimat agar arti kata tidak tertukar.",
            "tutor": "Gunakan Bantuan ID untuk membedah contoh Inggris dari tutor tanpa keluar dari percakapan.",
            "writing": "Untuk Writing, cek apakah kalimat sudah jelas, natural, dan terukur.",
            "listening": "Untuk Listening, fokus pada kata kunci yang menjawab tujuan, masalah, atau detail.",
            "scenario": "Untuk Scenario BA, hubungkan arti kalimat dengan masalah bisnis dan kebutuhan stakeholder.",
        }
        return module_notes.get(module, "Baca pelan-pelan, cari kata penting, lalu pahami maksud kalimat secara utuh.")

    def _context_tip(self, module: str, context_type: str) -> str:
        if context_type.endswith("_option"):
            return "Pahami arti pilihan ini dulu, lalu cocokkan dengan pertanyaan. Jangan pilih hanya karena ada kata yang sama."
        if context_type.endswith("_question"):
            return "Cari kata tanya seperti what atau which. Itu menunjukkan hal apa yang harus dijawab."
        return {
            "reading": "Baca kalimat pertama dan terakhir untuk menemukan arah ide.",
            "grammar": "Tandai subject dan verb utama sebelum menerjemahkan seluruh kalimat.",
            "vocabulary": "Buat satu contoh sendiri agar kata lebih mudah diingat.",
            "writing": "Tulis ulang dengan pola Subject + Verb + Object + Condition.",
            "listening": "Dengarkan kata yang berulang karena biasanya itu inti masalah.",
            "scenario": "Dalam BA, langkah aman biasanya klarifikasi dulu sebelum solusi.",
        }.get(module, "Pahami konteks sebelum menerjemahkan kata per kata.")

    def _is_question_text(self, text: str) -> bool:
        lowered = (text or "").strip().lower()
        return lowered.endswith("?") or lowered.startswith(("what ", "which ", "why ", "how ", "when ", "where ", "who ", "can "))

    def _is_short_option(self, text: str) -> bool:
        words = (text or "").split()
        return 0 < len(words) <= 10

    def _question_structure(self, text: str) -> dict[str, str]:
        lowered = text.lower()
        if "business outcome" in lowered and "solution" in lowered:
            return {
                "sentence_structure": "What + business outcome + should + subject + verb",
                "subject": "this solution",
                "verb": "should improve",
                "object_or_complement": "business outcome",
                "grammar_pattern": "Question asking expected business result",
            }
        if "ba action" in lowered and "alignment" in lowered:
            return {
                "sentence_structure": "Which + noun phrase + best supports + object",
                "subject": "BA action",
                "verb": "supports",
                "object_or_complement": "alignment",
                "grammar_pattern": "Question asking best action",
            }
        if "main purpose" in lowered and "conversation" in lowered:
            return {
                "sentence_structure": "What + is + subject/complement",
                "subject": "main purpose of the conversation",
                "verb": "is",
                "object_or_complement": "the answer should explain the purpose",
                "grammar_pattern": "Question asking purpose",
            }
        return {
            "sentence_structure": "Kalimat ini adalah pertanyaan. Fokus pada apa yang diminta, bukan hanya subject/verb.",
            "subject": "",
            "verb": "",
            "object_or_complement": "",
            "grammar_pattern": "Question",
        }

    def _direct_indonesian_meaning(self, text: str) -> str:
        key = re.sub(r"\s+", " ", (text or "").strip().lower().strip(".?"))
        meanings = {
            "what business outcome should this solution improve": "Pertanyaan ini berarti: hasil bisnis apa yang harus diperbaiki oleh solusi ini?",
            "which ba action best supports alignment": "Pertanyaan ini berarti: tindakan Business Analyst mana yang paling membantu menyelaraskan tujuan atau kebutuhan stakeholder?",
            "what is the best first question": "Pertanyaan ini berarti: pertanyaan pertama apa yang paling tepat untuk diajukan?",
            "what is the main purpose of the conversation": "Pertanyaan ini berarti: apa tujuan utama dari percakapan tersebut?",
            "ask the developer to build the feature immediately": "Pilihan ini berarti: langsung meminta developer membuat fitur saat itu juga.",
            "clarify what flexible means through elicitation": "Pilihan ini berarti: memperjelas arti kata flexible dengan menggali kebutuhan dari stakeholder.",
            "ignore the stakeholder because the statement is vague": "Pilihan ini berarti: mengabaikan stakeholder karena pernyataannya masih tidak jelas.",
            "write the requirement exactly as spoken": "Pilihan ini berarti: menulis requirement persis seperti ucapan stakeholder tanpa memperjelasnya.",
            "which color should the mobile app use": "Pilihan ini berarti: menanyakan warna apa yang harus dipakai aplikasi mobile.",
            "which developer is available this week": "Pilihan ini berarti: menanyakan developer mana yang tersedia minggu ini.",
            "can we skip user research": "Pilihan ini berarti: menanyakan apakah riset user bisa dilewati.",
            "the stakeholder reports that the current approval workflow causes delays": "Kalimat ini berarti: stakeholder melaporkan bahwa alur persetujuan saat ini menyebabkan keterlambatan.",
            "the finance team wants strict approval controls, while sales wants a faster checkout process": "Kalimat ini berarti: tim finance ingin kontrol approval yang ketat, sedangkan tim sales ingin proses checkout yang lebih cepat.",
            "a manager says, \"we need a mobile app,\" but cannot explain the business problem": "Kalimat ini berarti: seorang manager meminta mobile app, tetapi belum bisa menjelaskan masalah bisnis yang ingin diselesaikan.",
        }
        return meanings.get(key, "")

    def _basic_contextual_translation(self, text: str) -> str:
        cleaned = (text or "").strip()
        if not cleaned:
            return "Teks kosong, belum ada yang bisa dijelaskan."
        replacements = {
            "business outcome": "hasil bisnis",
            "solution": "solusi",
            "improve": "memperbaiki",
            "stakeholder": "stakeholder",
            "approval workflow": "alur persetujuan",
            "causes delays": "menyebabkan keterlambatan",
            "requirements": "kebutuhan",
            "main purpose": "tujuan utama",
            "conversation": "percakapan",
        }
        translated = cleaned
        for source, target in replacements.items():
            translated = re.sub(source, target, translated, flags=re.IGNORECASE)
        return f"Maksud teks ini: {translated}"

    def _guess_word_class(self, word: str) -> str:
        lowered = word.lower()
        if lowered.endswith("tion") or lowered.endswith("ment") or lowered in {"workflow", "stakeholder", "requirement"}:
            return "noun"
        if lowered.endswith("ly"):
            return "adverb"
        if lowered in {"elicit", "maintain", "align", "validate", "prioritize", "assess"}:
            return "verb"
        return "lihat konteks kalimat"

    def _better_sentence(self, text: str) -> str:
        lowered = text.lower()
        if "must flexible" in lowered:
            return "The system must be flexible enough to generate reports faster for different user roles."
        if text:
            return "Rewrite with a clear subject, verb, object, and measurable condition."
        return "The system must generate accurate reports within two minutes for each user role."

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
