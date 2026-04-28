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
        extra_context = extra_context or {}
        if self.api_key and self.provider in {"openai", "openrouter", "compatible"}:
            prompt = (
                "You are Bantuan ID for TOEFL Analyst AI. Return strict JSON with these fields: "
                "direct_meaning_id, context_explanation, key_vocabulary, learner_action, beginner_tip, context_specific_fields. "
                "Do not give generic explanations. Explain the exact clicked text in beginner Indonesian. "
                "Use module, context_type, and extra_context. For multiple-choice options, compare with passage/question if available. "
                "For questions, explain what the question asks and how to answer. Do not over-explain irrelevant grammar."
                f"\n\nModule: {module}\nContext type: {context_type}\nText: {cleaned_text}"
            )
            reply = self._compatible_chat(prompt, extra_context)
            explanation = self._mock_contextual_explanation(cleaned_text, module, context_type, extra_context)
            explanation["beginner_explanation"] = reply
            return self._contextual_response(cleaned_text, module, context_type, explanation, "llm")

        explanation = self._mock_contextual_explanation(cleaned_text, module, context_type, extra_context)
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

    def _mock_contextual_explanation(self, text: str, module: str, context_type: str, extra_context: dict | None = None) -> dict:
        extra_context = extra_context or {}
        if context_type == "reading_question":
            return self._explain_reading_question(text, extra_context)
        if context_type == "reading_option":
            return self._explain_reading_option(text, extra_context)
        if context_type in {"reading_passage", "reading_paragraph"}:
            return self._explain_reading_paragraph(text, extra_context)
        if context_type.startswith("vocabulary"):
            return self._explain_vocabulary_item(text, extra_context)
        if context_type.startswith("grammar"):
            return self._explain_grammar_sentence(text, extra_context)
        if context_type.startswith("writing"):
            return self._explain_writing(text, context_type, extra_context)
        if context_type.startswith("listening"):
            return self._explain_listening(text, context_type, extra_context)
        if context_type in {"scenario_case", "scenario_stakeholder_statement"}:
            return self._explain_scenario_case(text, extra_context)
        if context_type == "scenario_option":
            return self._explain_scenario_option(text, extra_context)
        if context_type == "scenario_question":
            return self._explain_scenario_question(text, extra_context)
        return self._explain_general(text, module, context_type)

    def _explain_general(self, text: str, module: str, context_type: str) -> dict:
        words = self._important_vocabulary(text)
        structure = self._simple_structure(text)
        return {
            "direct_meaning_id": self._simple_meaning(text, module, context_type),
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

    def _explain_reading_question(self, text: str, extra_context: dict) -> dict:
        lowered = text.lower()
        if "main idea" in lowered:
            direct = "Pertanyaan ini menanyakan ide utama dari passage."
            intent = "Mencari gagasan umum yang merangkum seluruh isi bacaan."
            what = "Cari pesan besar passage, bukan detail kecil."
            how = "Baca judul, kalimat pertama, kalimat terakhir, lalu pilih opsi yang paling mencakup semuanya."
            trap = "Jangan memilih opsi yang hanya menyebut satu detail, atau opsi yang tidak didukung passage."
            keywords = ["main idea = ide utama", "passage = bacaan"]
        elif "closest in meaning" in lowered:
            direct = "Pertanyaan ini meminta arti kata yang paling dekat dengan kata dalam passage."
            intent = "Menguji vocabulary in context."
            what = "Cari arti kata berdasarkan kalimat tempat kata itu muncul."
            how = "Ganti kata target dengan tiap opsi, lalu pilih yang maknanya tetap cocok."
            trap = "Jangan pilih arti kamus kalau tidak cocok dengan konteks kalimat."
            keywords = ["closest in meaning = paling dekat artinya", "context = konteks"]
        else:
            direct = self._simple_meaning(text, "reading", "reading_question")
            intent = "Memahami apa yang diminta pertanyaan Reading."
            what = "Cari informasi yang diminta oleh kata tanya."
            how = "Cocokkan pertanyaan dengan bagian passage yang relevan."
            trap = "Jangan memilih opsi hanya karena katanya sama."
            keywords = [item["word"] for item in self._important_vocabulary(text)]
        return {
            "direct_meaning_id": direct,
            "simple_meaning_id": direct,
            "question_intent": intent,
            "what_to_find": what,
            "how_to_answer": how,
            "trap_to_avoid": trap,
            "key_words": keywords,
            "important_vocabulary": self._important_vocabulary(text),
            "beginner_explanation": "Fokus pada maksud pertanyaan dulu, baru lihat pilihan jawaban.",
            "tips": how,
        }

    def _explain_reading_option(self, text: str, extra_context: dict) -> dict:
        direct = self._direct_indonesian_meaning(text) or self._basic_contextual_translation(text)
        passage = (extra_context.get("passage_text") or "").lower()
        question = extra_context.get("question_text", "")
        correct_answer = (extra_context.get("correct_answer") or extra_context.get("correct_answer_text") or "").strip()
        exact_correct = correct_answer and text.strip().lower() == correct_answer.lower()
        lowered = text.lower()

        relation = "Perlu dicocokkan dengan passage karena konteks jawaban belum lengkap."
        hint = "Belum bisa dipastikan."
        why = "Bandingkan makna opsi ini dengan ide utama dan detail passage."

        if exact_correct:
            relation = "Sangat sesuai dengan passage."
            hint = "Opsi kuat/kemungkinan benar."
            why = "Opsi ini cocok dengan jawaban yang disimpan untuk latihan ini."
        elif "write code immediately" in lowered:
            relation = "Tidak didukung oleh passage jika passage membahas requirement elicitation dan alignment."
            hint = "Opsi lemah/kemungkinan salah."
            why = "Coding langsung bukan inti passage; passage menekankan menggali requirement dan menyelaraskan kebutuhan."
        elif "connect requirements" in lowered or ("requirements" in lowered and "stakeholder" in lowered and "strategy" in lowered):
            relation = "Sangat sesuai dengan passage karena mencakup requirements, stakeholder needs, dan strategy."
            hint = "Opsi kuat/kemungkinan benar untuk main idea."
            why = "Opsi ini merangkum inti passage tentang requirement dan alignment dengan strategy."
        elif "avoid discussing vague problems" in lowered:
            relation = "Kurang tepat karena passage mengatakan analyst harus clarify vague problems, bukan stakeholder harus menghindarinya."
            hint = "Opsi lemah/kemungkinan salah."
            why = "Fokus passage adalah klarifikasi oleh analyst, bukan menghindari pembahasan masalah."
        elif "unrelated to requirements" in lowered:
            relation = "Bertentangan dengan passage karena passage justru membahas alignment antara requirements dan organizational strategy."
            hint = "Opsi salah."
            why = "Kata unrelated berlawanan dengan isi passage yang menyatakan strategi dan requirement harus selaras."
        elif passage and any(word in lowered for word in ["requirements", "stakeholder", "strategy", "alignment"]):
            relation = "Ada kata yang berhubungan dengan passage, tetapi tetap perlu dicocokkan dengan maksud pertanyaan."
            hint = "Mungkin kuat, tergantung pertanyaannya."
            why = "Opsi memakai vocabulary yang sejalan dengan passage."

        return {
            "direct_meaning_id": direct,
            "simple_meaning_id": direct,
            "option_meaning": direct,
            "relation_to_context": relation,
            "likely_correctness_hint": hint,
            "why": why,
            "question_intent": self._question_intent_from_text(question),
            "key_words": [item["word"] for item in self._important_vocabulary(text)],
            "important_vocabulary": self._important_vocabulary(text),
            "beginner_explanation": relation,
            "tips": "Untuk opsi jawaban, pahami arti opsi lalu cek apakah didukung oleh passage.",
        }

    def _explain_reading_paragraph(self, text: str, extra_context: dict) -> dict:
        direct = self._direct_indonesian_meaning(text) or self._basic_contextual_translation(text)
        return {
            "direct_meaning_id": direct,
            "simple_meaning_id": direct,
            "main_message": "Passage menekankan peran Business Analyst dalam menggali requirement dan menyelaraskannya dengan kebutuhan stakeholder serta strategi organisasi.",
            "key_points": ["Business Analyst menggali requirement", "Stakeholder needs harus dipahami", "Requirement perlu selaras dengan strategy"],
            "grammar_focus": "Kalimat panjang bisa dipecah menjadi subject, modifier, main verb, dan object.",
            "important_vocabulary": self._important_vocabulary(text),
            "reading_tip": "Cari ide utama sebelum melihat pilihan jawaban.",
            "beginner_explanation": "Baca dulu maksud umum passage, lalu tandai kata seperti requirements, stakeholder, alignment, dan strategy.",
            "tips": "Main idea biasanya tidak terlalu sempit dan tidak bertentangan dengan passage.",
        }

    def _explain_vocabulary_item(self, text: str, extra_context: dict) -> dict:
        word = (extra_context.get("word") or text or "").split()[0].strip(".,:;!?\"'")
        example = extra_context.get("example") or text
        vocab_info = self._important_vocabulary(word)[0] if self._important_vocabulary(word) else {
            "word": word,
            "meaning_id": self._contextual_word_meaning(word, example),
            "one_word_meaning_id": self._one_word_meaning(word),
            "contextual_meaning_id": self._contextual_word_meaning(word, example),
        }
        direct = f"{word} berarti {vocab_info.get('meaning_id', 'makna sesuai konteks')}."
        return {
            "direct_meaning_id": direct,
            "simple_meaning_id": direct,
            "word": word,
            "word_class": self._guess_word_class(word),
            "word_one_word_meaning_id": vocab_info.get("one_word_meaning_id", self._one_word_meaning(word)),
            "word_meaning_id": vocab_info.get("meaning_id", ""),
            "word_contextual_meaning_id": vocab_info.get("contextual_meaning_id", self._contextual_word_meaning(word, example)),
            "ba_context": self._ba_context_for_word(word),
            "example_sentence": extra_context.get("example") or f"A BA elicits requirements from stakeholders.",
            "memory_tip": self._memory_tip(word),
            "important_vocabulary": [vocab_info],
            "beginner_explanation": self._contextual_word_meaning(word, example),
            "tips": self._memory_tip(word),
        }

    def _explain_grammar_sentence(self, text: str, extra_context: dict) -> dict:
        structure = self._simple_structure(text)
        lowered = text.lower()
        modifier = "operating within a complex enterprise environment" if "operating within" in lowered else ""
        main_verb = "must elicit dan must ensure" if "not only" in lowered and "but also" in lowered else structure.get("verb", "")
        direct = self._direct_indonesian_meaning(text) or self._basic_contextual_translation(text)
        return {
            "direct_meaning_id": direct,
            "simple_meaning_id": direct,
            "subject": structure.get("subject", ""),
            "main_verb": main_verb,
            "verb": main_verb,
            "modifier": modifier,
            "object_or_complement": structure.get("object_or_complement", ""),
            "grammar_pattern": "not only ... but also ..." if "not only" in lowered else structure.get("grammar_pattern", ""),
            "beginner_warning": "Jangan mengira operating sebagai main verb; operating hanya menerangkan business analyst." if "operating" in lowered else "Cari verb utama setelah subject.",
            "simplified_sentence": self._simplified_sentence(text),
            "important_vocabulary": self._important_vocabulary(text),
            "beginner_explanation": "Bedah kalimat panjang dari subject utama dulu, lalu cari verb utama.",
            "tips": "Abaikan sementara phrase panjang agar subject dan verb utama lebih mudah terlihat.",
        }

    def _explain_writing(self, text: str, context_type: str, extra_context: dict) -> dict:
        direct = self._direct_indonesian_meaning(text) or self._basic_contextual_translation(text)
        return {
            "direct_meaning_id": direct,
            "simple_meaning_id": direct,
            "clarity_feedback": "Kalimat writing harus jelas siapa melakukan apa, untuk siapa, dan dalam kondisi apa.",
            "grammar_issue": "Cek penggunaan be setelah must jika memakai adjective, misalnya must be flexible.",
            "improved_sentence": self._better_sentence(text),
            "why_better": "Versi perbaikan lebih natural dan lebih spesifik untuk requirement.",
            "writing_tip": "Gunakan pola: The system must + verb + object + condition.",
            "important_vocabulary": self._important_vocabulary(text),
            "beginner_explanation": "Fokus pada clarity dan measurable requirement.",
            "tips": "Tambahkan ukuran keberhasilan agar requirement tidak terlalu umum.",
        }

    def _explain_listening(self, text: str, context_type: str, extra_context: dict) -> dict:
        direct = self._direct_indonesian_meaning(text) or self._basic_contextual_translation(text)
        keywords = [item["word"] for item in self._important_vocabulary(text)] or ["purpose", "problem", "detail"]
        return {
            "direct_meaning_id": direct,
            "simple_meaning_id": direct,
            "listening_focus": "Cari tujuan pembicaraan, masalah utama, atau detail yang ditanyakan.",
            "keywords_to_hear": keywords,
            "speaker_intent": "Tentukan apakah pembicara sedang melaporkan masalah, meminta klarifikasi, atau menyarankan tindakan.",
            "answer_strategy": "Dengarkan kata yang diulang atau kontras seperti but, however, because.",
            "important_vocabulary": self._important_vocabulary(text),
            "beginner_explanation": "Untuk listening, tidak perlu menangkap semua kata; fokus pada kata kunci.",
            "tips": "Jawab berdasarkan maksud pembicara, bukan satu kata yang terdengar familiar.",
        }

    def _explain_scenario_case(self, text: str, extra_context: dict) -> dict:
        direct = self._direct_indonesian_meaning(text) or self._basic_contextual_translation(text)
        problem = "approval workflow lambat" if "approval workflow" in text.lower() or "delays" in text.lower() else "masalah bisnis perlu diklarifikasi"
        return {
            "direct_meaning_id": direct,
            "simple_meaning_id": direct,
            "ba_context": "Ini adalah problem statement awal dalam pekerjaan Business Analyst.",
            "business_problem": problem,
            "stakeholder_need": "Stakeholder membutuhkan proses yang lebih jelas, cepat, atau tidak menghambat pekerjaan.",
            "suggested_ba_action": "Klarifikasi titik bottleneck, aktor yang terlibat, durasi delay, dan dampaknya sebelum memilih solusi.",
            "answer_strategy": "Pilih tindakan BA yang memperjelas masalah, bukan langsung membuat solusi.",
            "important_vocabulary": self._important_vocabulary(text),
            "beginner_explanation": "Dalam scenario BA, cari masalah bisnis dan kebutuhan stakeholder terlebih dulu.",
            "tips": "Jangan langsung loncat ke solusi; pahami akar masalah.",
        }

    def _explain_scenario_option(self, text: str, extra_context: dict) -> dict:
        direct = self._direct_indonesian_meaning(text) or self._basic_contextual_translation(text)
        lowered = text.lower()
        if any(word in lowered for word in ["clarify", "facilitate", "business goals", "trade-offs", "outcome"]):
            hint = "Opsi ini cenderung kuat karena sesuai cara kerja BA: klarifikasi, fasilitasi, atau hubungkan dengan business outcome."
            action = "Cek apakah opsi ini membantu memahami kebutuhan sebelum solusi."
        else:
            hint = "Opsi ini perlu hati-hati; mungkin terlalu cepat memilih solusi atau terlalu sempit."
            action = "Bandingkan dengan prinsip BA: clarify, elicit, validate, align."
        return {
            "direct_meaning_id": direct,
            "simple_meaning_id": direct,
            "option_meaning": direct,
            "relation_to_context": hint,
            "likely_correctness_hint": hint,
            "why": action,
            "ba_context": "Opsi scenario harus dinilai dari apakah ia membantu BA memahami masalah dan stakeholder need.",
            "answer_strategy": "Prioritaskan opsi yang mengklarifikasi masalah dan menyelaraskan stakeholder.",
            "important_vocabulary": self._important_vocabulary(text),
            "beginner_explanation": hint,
            "tips": action,
        }

    def _explain_scenario_question(self, text: str, extra_context: dict) -> dict:
        direct = self._direct_indonesian_meaning(text) or self._basic_contextual_translation(text)
        return {
            "direct_meaning_id": direct,
            "simple_meaning_id": direct,
            "question_intent": "Pertanyaan ini meminta tindakan BA paling tepat.",
            "what_to_find": "Cari opsi yang paling membantu memahami masalah, stakeholder, atau business outcome.",
            "how_to_answer": "Pilih langkah analisis sebelum solusi teknis.",
            "trap_to_avoid": "Hindari opsi yang langsung memilih solusi tanpa klarifikasi.",
            "important_vocabulary": self._important_vocabulary(text),
            "beginner_explanation": "Scenario BA menilai cara berpikir, bukan hanya arti kata.",
            "tips": "Ingat urutan aman BA: clarify, elicit, validate, align.",
        }

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
            "code": "kode program",
            "immediately": "segera",
            "avoid": "menghindari",
            "vague": "samar atau tidak jelas",
            "unrelated": "tidak berhubungan",
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
            "code": "kode",
            "immediately": "segera",
            "avoid": "menghindari",
            "vague": "samar",
            "unrelated": "tidak-terkait",
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

    def _question_intent_from_text(self, question: str) -> str:
        lowered = (question or "").lower()
        if "main idea" in lowered:
            return "Pertanyaan meminta ide utama passage."
        if "closest in meaning" in lowered:
            return "Pertanyaan meminta arti vocabulary berdasarkan konteks."
        if "best" in lowered or "which" in lowered:
            return "Pertanyaan meminta pilihan yang paling tepat."
        return "Pertanyaan meminta informasi yang harus dicocokkan dengan konteks."

    def _ba_context_for_word(self, word: str) -> str:
        lowered = (word or "").lower()
        if lowered in {"elicit", "elicits"}:
            return "Dalam BA, elicit berarti menggali kebutuhan stakeholder lewat interview, workshop, observasi, atau pertanyaan klarifikasi."
        if lowered in {"requirement", "requirements"}:
            return "Dalam BA, requirement adalah kebutuhan bisnis atau sistem yang harus jelas dan dapat diuji."
        if lowered in {"stakeholder", "stakeholders"}:
            return "Dalam BA, stakeholder adalah pihak yang punya kebutuhan, memberi keputusan, atau terdampak solusi."
        if lowered in {"workflow"}:
            return "Dalam BA, workflow adalah alur kerja yang dianalisis untuk mencari hambatan atau perbaikan."
        return "Dalam BA, arti kata perlu dihubungkan dengan proses, stakeholder, requirement, risiko, atau business outcome."

    def _memory_tip(self, word: str) -> str:
        lowered = (word or "").lower()
        if lowered in {"elicit", "elicits"}:
            return "Ingat elicit sebagai menggali kebutuhan, bukan sekadar bertanya biasa."
        if lowered in {"maintain"}:
            return "Ingat maintain sebagai menjaga sesuatu tetap berjalan baik."
        if lowered in {"requirement", "requirements"}:
            return "Ingat requirement sebagai kebutuhan yang harus ditulis jelas."
        return f"Ingat {word} lewat satu contoh kalimat BA, bukan hanya hafalan kamus."

    def _simplified_sentence(self, text: str) -> str:
        lowered = (text or "").lower()
        if "business analyst" in lowered and "elicit" in lowered:
            return "A business analyst must elicit requirements and ensure alignment."
        if "approval workflow" in lowered:
            return "The approval workflow causes delays."
        return text

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
            "what is the main idea of the passage": "Pertanyaan ini menanyakan ide utama dari passage.",
            "business analysts should write code immediately": "Business Analyst sebaiknya langsung menulis kode.",
            "business analysts must connect requirements with stakeholder needs and strategy": "Business Analyst harus menghubungkan requirements dengan kebutuhan stakeholder dan strategy.",
            "stakeholders should avoid discussing vague problems": "Stakeholder sebaiknya menghindari membahas masalah yang masih samar.",
            "organizational strategy is unrelated to requirements": "Strategi organisasi tidak berhubungan dengan requirements.",
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
            "business analysts": "Business Analyst",
            "solution": "solusi",
            "improve": "memperbaiki",
            "main idea": "ide utama",
            "passage": "passage",
            "stakeholder": "stakeholder",
            "stakeholder needs": "kebutuhan stakeholder",
            "strategy": "strategi",
            "organizational strategy": "strategi organisasi",
            "approval workflow": "alur persetujuan",
            "causes delays": "menyebabkan keterlambatan",
            "requirements": "kebutuhan",
            "write code immediately": "langsung menulis kode",
            "unrelated": "tidak berhubungan",
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
