from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import hashlib
import json
import time


ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
DATA_FILE = DATA_DIR / "app_data.json"


DEFAULT_DATA = {
    "users": [],
    "sessions": {},
    "lessons": [
        {
            "id": "reading-1",
            "title": "Stakeholder Needs and Strategy Alignment",
            "level": "Foundation",
            "context": "Requirement elicitation",
            "passage": "A business analyst operating within a complex enterprise environment must not only elicit requirements but also ensure alignment between stakeholder needs and organizational strategy. When a stakeholder describes a problem vaguely, the analyst should clarify the expected outcome before proposing a solution.",
            "vocabulary": ["elicit", "alignment", "stakeholder", "vaguely", "outcome"],
            "grammar": "Reduced relative clause: operating within a complex enterprise environment.",
            "questions": [
                {
                    "id": "r1q1",
                    "text": "What is the main idea of the passage?",
                    "options": [
                        "Business analysts should write code immediately.",
                        "Business analysts must connect requirements with stakeholder needs and strategy.",
                        "Stakeholders should avoid discussing vague problems.",
                        "Organizational strategy is unrelated to requirements.",
                    ],
                    "answer": 1,
                    "explanation": "The passage emphasizes eliciting requirements and aligning them with needs and strategy.",
                }
            ],
        },
        {
            "id": "reading-2",
            "title": "Business Process Improvement",
            "level": "Intermediate",
            "context": "Business process",
            "passage": "Before recommending automation, a business analyst evaluates the current process to identify delays, duplicate work, and unclear responsibilities. This analysis helps the organization determine whether technology is the right solution or whether the process itself must be redesigned.",
            "vocabulary": ["automation", "evaluate", "duplicate", "responsibilities", "redesigned"],
            "grammar": "Adverbial clause: Before recommending automation.",
            "questions": [
                {
                    "id": "r2q1",
                    "text": "Why does the analyst evaluate the current process?",
                    "options": [
                        "To identify delays and unclear responsibilities.",
                        "To replace all employees.",
                        "To avoid speaking with stakeholders.",
                        "To skip process redesign.",
                    ],
                    "answer": 0,
                    "explanation": "The passage mentions delays, duplicate work, and unclear responsibilities as analysis targets.",
                }
            ],
        },
    ],
    "vocabulary": [
        {
            "id": "v1",
            "word": "elicit",
            "part": "verb",
            "meaningId": "menggali atau memperoleh informasi",
            "meaningEn": "to draw out information",
            "example": "The analyst must elicit clear requirements from stakeholders.",
            "answer": "menggali",
        },
        {
            "id": "v2",
            "word": "validate",
            "part": "verb",
            "meaningId": "memastikan sesuatu benar atau sesuai kebutuhan",
            "meaningEn": "to confirm correctness or suitability",
            "example": "The team validates the requirement before development starts.",
            "answer": "memastikan",
        },
        {
            "id": "v3",
            "word": "prioritize",
            "part": "verb",
            "meaningId": "mengurutkan berdasarkan kepentingan",
            "meaningEn": "to arrange by importance",
            "example": "A product owner and analyst prioritize features for the next sprint.",
            "answer": "mengurutkan",
        },
        {"id": "v4", "word": "assess", "part": "verb", "meaningId": "menilai atau mengevaluasi", "meaningEn": "to evaluate or judge something", "example": "The analyst assesses the impact of a proposed change.", "answer": "menilai"},
        {"id": "v5", "word": "align", "part": "verb", "meaningId": "menyelaraskan", "meaningEn": "to make things support the same goal", "example": "The requirement must align with the business objective.", "answer": "menyelaraskan"},
        {"id": "v6", "word": "stakeholder", "part": "noun", "meaningId": "pihak terkait", "meaningEn": "a person or group affected by a project", "example": "The stakeholder explains the reporting problem to the analyst.", "answer": "pihak terkait"},
        {"id": "v7", "word": "objective", "part": "noun", "meaningId": "tujuan", "meaningEn": "a goal or intended result", "example": "The business objective is to reduce manual work.", "answer": "tujuan"},
        {"id": "v8", "word": "constraint", "part": "noun", "meaningId": "batasan", "meaningEn": "a limitation that affects a solution", "example": "Budget is a constraint for the project team.", "answer": "batasan"},
        {"id": "v9", "word": "scope", "part": "noun", "meaningId": "ruang lingkup", "meaningEn": "the boundary of what is included", "example": "The analyst clarifies the project scope before writing requirements.", "answer": "ruang lingkup"},
        {"id": "v10", "word": "assumption", "part": "noun", "meaningId": "asumsi", "meaningEn": "something believed to be true without full proof", "example": "The team documents each assumption during planning.", "answer": "asumsi"},
        {"id": "v11", "word": "issue", "part": "noun", "meaningId": "masalah", "meaningEn": "a problem that needs attention", "example": "The analyst identifies the main issue in the process.", "answer": "masalah"},
        {"id": "v12", "word": "impact", "part": "noun", "meaningId": "dampak", "meaningEn": "the effect of an action or change", "example": "The impact of the change must be analyzed.", "answer": "dampak"},
        {"id": "v13", "word": "process", "part": "noun", "meaningId": "proses", "meaningEn": "a series of steps to achieve a result", "example": "The current process causes delays in approval.", "answer": "proses"},
        {"id": "v14", "word": "workflow", "part": "noun", "meaningId": "alur kerja", "meaningEn": "the sequence of work activities", "example": "The analyst maps the workflow before recommending automation.", "answer": "alur kerja"},
        {"id": "v15", "word": "approval", "part": "noun", "meaningId": "persetujuan", "meaningEn": "formal permission or acceptance", "example": "The request requires approval from the manager.", "answer": "persetujuan"},
        {"id": "v16", "word": "evidence", "part": "noun", "meaningId": "bukti", "meaningEn": "information that supports a conclusion", "example": "The analyst uses evidence from interviews and reports.", "answer": "bukti"},
        {"id": "v17", "word": "define", "part": "verb", "meaningId": "mendefinisikan", "meaningEn": "to explain the exact meaning of something", "example": "The team defines the acceptance criteria clearly.", "answer": "mendefinisikan"},
        {"id": "v18", "word": "verify", "part": "verb", "meaningId": "memverifikasi", "meaningEn": "to check that something is correct", "example": "The analyst verifies the requirement with the stakeholder.", "answer": "memverifikasi"},
        {"id": "v19", "word": "clarify", "part": "verb", "meaningId": "memperjelas", "meaningEn": "to make something easier to understand", "example": "The analyst asks questions to clarify the problem.", "answer": "memperjelas"},
        {"id": "v20", "word": "determine", "part": "verb", "meaningId": "menentukan", "meaningEn": "to decide or discover something", "example": "The team determines the most important requirement.", "answer": "menentukan"},
        {"id": "v21", "word": "indicate", "part": "verb", "meaningId": "menunjukkan", "meaningEn": "to show or suggest something", "example": "The report indicates a delay in data collection.", "answer": "menunjukkan"},
        {"id": "v22", "word": "significant", "part": "adjective", "meaningId": "signifikan atau penting", "meaningEn": "important or large enough to notice", "example": "The delay has a significant impact on decision-making.", "answer": "signifikan"},
        {"id": "v23", "word": "feasible", "part": "adjective", "meaningId": "layak dilakukan", "meaningEn": "possible and practical to do", "example": "The analyst checks whether the solution is feasible.", "answer": "layak"},
        {"id": "v24", "word": "accurate", "part": "adjective", "meaningId": "akurat", "meaningEn": "correct and precise", "example": "Users need accurate data in the dashboard.", "answer": "akurat"},
        {"id": "v25", "word": "relevant", "part": "adjective", "meaningId": "relevan", "meaningEn": "closely connected to the topic", "example": "The analyst collects relevant information from users.", "answer": "relevan"},
        {"id": "v26", "word": "ambiguous", "part": "adjective", "meaningId": "ambigu atau tidak jelas", "meaningEn": "having more than one possible meaning", "example": "The requirement is ambiguous and needs clarification.", "answer": "ambigu"},
        {"id": "v27", "word": "consistent", "part": "adjective", "meaningId": "konsisten", "meaningEn": "staying the same in quality or meaning", "example": "The data format must be consistent across departments.", "answer": "konsisten"},
        {"id": "v28", "word": "monitor", "part": "verb", "meaningId": "memantau", "meaningEn": "to watch and check progress", "example": "The team monitors system performance after release.", "answer": "memantau"},
        {"id": "v29", "word": "measure", "part": "verb", "meaningId": "mengukur", "meaningEn": "to find the size, amount, or level", "example": "The analyst measures improvement using completion time.", "answer": "mengukur"},
        {"id": "v30", "word": "recommend", "part": "verb", "meaningId": "merekomendasikan", "meaningEn": "to suggest the best action", "example": "The analyst recommends a simpler approval workflow.", "answer": "merekomendasikan"},
    ],
    "progress": {},
    "state": {},
}

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

LISTENING_SCENARIO = {
    "id": "listening-1",
    "title": "Stakeholder Interview: Reporting Delay",
    "transcript": "Stakeholder: The monthly report is always late. Analyst: What causes the delay? Stakeholder: Data from two departments arrives in different formats. Analyst: So the main issue is inconsistent input data before consolidation.",
    "question": "What is the main issue discussed in the meeting?",
    "answer": "Inconsistent input data before consolidation.",
    "keywords": ["inconsistent", "format", "data", "consolidation"],
}


def load_data():
    if not DATA_FILE.exists():
        save_data(DEFAULT_DATA)
    with DATA_FILE.open("r", encoding="utf-8") as file:
        stored = json.load(file)
    data = {**DEFAULT_DATA, **stored}
    data["lessons"] = merge_by_id(data.get("lessons", []), DEFAULT_DATA["lessons"])
    data["vocabulary"] = merge_by_id(data.get("vocabulary", []), DEFAULT_DATA["vocabulary"])
    if data != stored:
        save_data(data)
    return data


def merge_by_id(current, defaults):
    seen = {item.get("id") for item in current}
    return current + [item for item in defaults if item.get("id") not in seen]


def save_data(data):
    DATA_DIR.mkdir(exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def tutor_reply(message):
    text = message.lower()
    if "operating" in text or "verb" in text:
        return "Dalam kalimat BA, operating biasanya bukan main verb jika ia menerangkan noun sebelumnya. Main verb membawa aksi utama, misalnya must elicit atau must ensure."
    if "requirement" in text:
        return "Requirement yang baik harus jelas, dapat diuji, dan tidak ambigu. Jika stakeholder berkata flexible, BA perlu bertanya kondisi, aktor, dan ukuran keberhasilannya."
    if "rekomendasi" in text or "latihan" in text:
        return "Latihan hari ini: pilih satu passage BA, cari main idea, lalu bedah satu kalimat panjang menjadi subject, main verb, dan phrase."
    return "Mulai dari subject dan main verb dulu. Setelah itu baru baca phrase tambahan, clause, dan konteks BA seperti stakeholder, requirement, atau business goal."


def grammar_breakdown(sentence):
    lowered = sentence.lower()
    return {
        "subject": "A business analyst" if "business analyst" in lowered else "Identify the noun phrase before the main verb",
        "mainVerb": "must elicit / must ensure" if "must" in lowered else "Find the finite verb after the subject",
        "phrase": "operating within a complex enterprise environment" if "operating" in lowered else "Look for modifier phrases",
        "pattern": "not only ... but also ..." if "not only" in lowered else "Subject + main verb + object/complement",
        "translation": "Terjemahan natural perlu menjaga makna BA: aktor, tindakan, kebutuhan stakeholder, dan tujuan bisnis.",
        "explanation": "Bagian -ing sering berfungsi sebagai penjelas noun, bukan verb utama. Cari modal atau finite verb untuk menemukan aksi utama.",
    }


def score_reading(lesson, answers):
    questions = lesson.get("questions", [])
    if not questions:
        return {"score": 0, "correct": 0, "total": 0, "details": []}
    details = []
    correct = 0
    for question in questions:
        selected = answers.get(question["id"])
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


def evaluate_writing(text):
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


def evaluate_listening(answer):
    lowered = answer.lower()
    matches = [keyword for keyword in LISTENING_SCENARIO["keywords"] if keyword in lowered]
    score = min(100, 35 + len(matches) * 20)
    return {
        "score": score,
        "isCorrect": score >= 75,
        "idealAnswer": LISTENING_SCENARIO["answer"],
        "explanation": "The stakeholder says the delay comes from department data arriving in different formats before consolidation.",
    }


def score_scenario(question_id, selected):
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


def recommendation(progress):
    if not progress:
        return {
            "weakness": "Grammar",
            "summary": "Belum ada data progress yang cukup.",
            "recommendation": "Mulai dari Grammar Breakdown dan satu Reading passage pendek.",
            "target": "Selesaikan satu latihan grammar dan satu vocabulary drill hari ini.",
        }
    weakness = min(progress, key=progress.get)
    plans = {
        "Reading": "Kerjakan satu passage BA dan fokus pada main idea serta vocabulary in context.",
        "Grammar": "Bedah satu kalimat panjang. Tandai subject, main verb, dan phrase tambahan.",
        "Vocabulary": "Latih elicit, validate, prioritize, dan assess dalam kalimat BA.",
        "Writing": "Tulis satu requirement statement yang measurable.",
        "Listening": "Baca transcript meeting, lalu simpulkan masalah utamanya dalam satu kalimat.",
        "Scenario": "Kerjakan satu scenario BA dan jelaskan alasan pilihanmu.",
    }
    return {
        "weakness": weakness,
        "summary": f"Area terlemah saat ini adalah {weakness}.",
        "recommendation": plans.get(weakness, "Mulai dari latihan pendek yang paling relevan."),
        "target": "Selesaikan satu latihan kecil dan catat pola kesalahan utama.",
    }


def progress_analytics(state):
    progress = state.get("progress", {})
    activity = state.get("activity", [])
    if not progress:
        return {
            "averageScore": 0,
            "weakestSkill": "Grammar",
            "strongestSkill": "Reading",
            "completedExercises": state.get("completedExercises", 0),
            "activityCount": len(activity),
            "status": "Belum ada data latihan.",
        }
    scores = list(progress.values())
    weakest = min(progress, key=progress.get)
    strongest = max(progress, key=progress.get)
    average = round(sum(scores) / len(scores))
    if average >= 75:
        status = "Progress kuat. Lanjutkan latihan advanced dan scenario."
    elif average >= 45:
        status = "Progress mulai terbentuk. Fokuskan latihan pada skill terlemah."
    else:
        status = "Masih tahap awal. Selesaikan latihan foundation secara konsisten."
    return {
        "averageScore": average,
        "weakestSkill": weakest,
        "strongestSkill": strongest,
        "completedExercises": state.get("completedExercises", 0),
        "activityCount": len(activity),
        "status": status,
    }


def indonesian_help(text, help_type="simple"):
    lowered = text.lower()
    keywords = []
    keyword_map = {
        "business analyst": "business analyst = analis bisnis",
        "elicit": "elicit = menggali informasi",
        "requirement": "requirement = kebutuhan sistem",
        "stakeholder": "stakeholder = pihak terkait",
        "ensure": "ensure = memastikan",
        "alignment": "alignment = keselarasan",
        "strategy": "strategy = strategi",
        "validate": "validate = memastikan benar",
        "prioritize": "prioritize = mengurutkan prioritas",
        "solution": "solution = solusi",
    }
    for key, label in keyword_map.items():
        if key in lowered:
            keywords.append(label)
    if not keywords:
        keywords.append("Cari kata kerja utama dan kata benda penting.")
    focus = {
        "simple": "Fokus dulu pada makna besar: siapa melakukan apa dan untuk tujuan apa.",
        "translate": "Terjemahkan natural, bukan kata-per-kata, agar mudah dipahami dalam Bahasa Indonesia.",
        "vocabulary": "Pahami kata kerja utama dan kata benda penting sebelum membaca seluruh kalimat.",
        "grammar": "Cari subject sebagai pelaku dan verb sebagai aksi utama. Phrase panjang bisa dibaca belakangan.",
    }
    if "must" in lowered:
        structure = "Subject + must + verb utama + object"
    elif "ing" in lowered:
        structure = "Subject + phrase tambahan + verb utama"
    else:
        structure = "Subject + verb + object/complement"
    return {
        "simpleMeaning": "Kalimat ini membahas pekerjaan atau keputusan Business Analyst dalam memahami kebutuhan, menjelaskan masalah, atau memastikan solusi sesuai tujuan bisnis.",
        "keywords": keywords,
        "structure": structure,
        "explanation": focus.get(help_type, focus["simple"]),
        "example": "The analyst clarifies requirements. Artinya: analis menjelaskan kebutuhan agar tidak ambigu.",
    }


def daily_vocabulary(vocabulary_items):
    today = time.strftime("%Y-%m-%d")
    selected = seeded_daily_items(vocabulary_items, today, 25)
    return {
        "date": today,
        "target": 25,
        "items": selected,
        "message": "Pengingat hari ini: selesaikan 25 kata vocabulary agar konsisten naik level.",
    }


def seeded_daily_items(items, seed_text, limit):
    if not items:
        return []
    decorated = []
    for item in items:
        source = f"{seed_text}-{item.get('id')}-{item.get('word')}".encode("utf-8")
        score = hashlib.sha256(source).hexdigest()
        decorated.append((score, item))
    decorated.sort(key=lambda pair: pair[0])
    return [item for _, item in decorated[: min(limit, len(decorated))]]


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if not parsed.path.startswith("/api/"):
            return super().do_GET()

        data = load_data()
        if parsed.path == "/api/health":
            return self.json_response({"ok": True, "service": "TOEFL Analyst AI API"})
        if parsed.path == "/api/lessons":
            return self.json_response({"lessons": data["lessons"]})
        if parsed.path.startswith("/api/lessons/"):
            lesson_id = parsed.path.rsplit("/", 1)[-1]
            lesson = next((item for item in data["lessons"] if item["id"] == lesson_id), None)
            return self.json_response({"lesson": lesson}, 200 if lesson else 404)
        if parsed.path == "/api/vocabulary":
            return self.json_response({"vocabulary": data["vocabulary"]})
        if parsed.path == "/api/vocabulary/daily":
            return self.json_response(daily_vocabulary(data["vocabulary"]))
        if parsed.path == "/api/listening/sessions/default":
            return self.json_response({"session": LISTENING_SCENARIO})
        if parsed.path == "/api/scenario/questions":
            return self.json_response({"questions": SCENARIO_QUESTIONS})
        if parsed.path == "/api/progress/summary":
            return self.json_response({"progress": data.get("progress", {})})
        if parsed.path == "/api/progress/analytics":
            return self.json_response({"analytics": progress_analytics(data.get("state", {}))})
        if parsed.path == "/api/state":
            return self.json_response({"state": data.get("state", {})})
        return self.json_response({"error": "Not found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if not parsed.path.startswith("/api/"):
            return self.json_response({"error": "Not found"}, 404)

        data = load_data()
        body = self.read_json()

        if parsed.path == "/api/auth/register":
            user = {
                "id": f"user-{int(time.time() * 1000)}",
                "name": body.get("name", "Junior BA Learner"),
                "email": body.get("email", "learner@example.local"),
                "targetScore": body.get("targetScore", 500),
                "weakness": body.get("weakness", "Grammar"),
                "level": body.get("level", "Foundation"),
            }
            data["users"].append(user)
            token = f"token-{user['id']}"
            data["sessions"][token] = user["id"]
            save_data(data)
            return self.json_response({"user": user, "token": token}, 201)

        if parsed.path == "/api/auth/login":
            user = data["users"][0] if data["users"] else {
                "id": "guest-user",
                "name": body.get("name", "Junior BA Learner"),
                "email": "guest@example.local",
                "targetScore": body.get("targetScore", 500),
                "weakness": body.get("weakness", "Grammar"),
                "level": "Foundation",
            }
            token = f"token-{user['id']}"
            data["sessions"][token] = user["id"]
            save_data(data)
            return self.json_response({"user": user, "token": token})

        if parsed.path == "/api/lessons":
            lesson = {**body, "id": body.get("id") or f"lesson-{int(time.time() * 1000)}"}
            data["lessons"].insert(0, lesson)
            save_data(data)
            return self.json_response({"lesson": lesson}, 201)

        if parsed.path == "/api/vocabulary":
            item = {**body, "id": body.get("id") or f"vocab-{int(time.time() * 1000)}"}
            data["vocabulary"].insert(0, item)
            save_data(data)
            return self.json_response({"item": item}, 201)

        if parsed.path == "/api/progress/record":
            data["progress"] = body
            save_data(data)
            return self.json_response({"progress": data["progress"]})

        if parsed.path == "/api/progress/analytics":
            return self.json_response({"analytics": progress_analytics(body)})

        if parsed.path == "/api/reading/submit-answer":
            lesson_id = body.get("lessonId")
            lesson = next((item for item in data["lessons"] if item["id"] == lesson_id), None)
            if not lesson:
                return self.json_response({"error": "Lesson not found"}, 404)
            return self.json_response(score_reading(lesson, body.get("answers", {})))

        if parsed.path == "/api/vocabulary/submit-answer":
            item = next((entry for entry in data["vocabulary"] if entry["id"] == body.get("itemId")), None)
            if not item:
                return self.json_response({"error": "Vocabulary item not found"}, 404)
            selected = body.get("answer")
            is_correct = selected == item.get("answer") or selected == item.get("meaningId")
            return self.json_response(
                {
                    "score": 100 if is_correct else 0,
                    "isCorrect": is_correct,
                    "correctAnswer": item.get("answer"),
                    "explanation": "Makna sudah sesuai konteks BA." if is_correct else "Perhatikan contoh kalimat dan makna Indonesia.",
                }
            )

        if parsed.path == "/api/state":
            data["state"] = body
            save_data(data)
            return self.json_response({"state": data["state"]})

        if parsed.path == "/api/grammar/breakdown":
            return self.json_response({"analysis": grammar_breakdown(body.get("sentence", ""))})

        if parsed.path == "/api/ai-tutor/chat":
            message = body.get("message", "")
            return self.json_response({"reply": tutor_reply(message)})

        if parsed.path == "/api/ai-tutor/recommendation":
            return self.json_response(recommendation(body.get("progress", {})))

        if parsed.path == "/api/help/indonesian":
            return self.json_response(indonesian_help(body.get("text", ""), body.get("type", "simple")))

        if parsed.path == "/api/writing/evaluate":
            return self.json_response(evaluate_writing(body.get("text", "")))

        if parsed.path == "/api/listening/generate-scenario":
            return self.json_response({"session": LISTENING_SCENARIO})

        if parsed.path == "/api/listening/submit-answer":
            return self.json_response(evaluate_listening(body.get("answer", "")))

        if parsed.path == "/api/scenario/submit-answer":
            result = score_scenario(body.get("questionId"), body.get("selected"))
            return self.json_response(result, 404 if "error" in result else 200)

        return self.json_response({"error": "Not found"}, 404)

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw or "{}")

    def json_response(self, payload, status=200):
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


if __name__ == "__main__":
    port = 8001
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"TOEFL Analyst AI running at http://127.0.0.1:{port}")
    server.serve_forever()
