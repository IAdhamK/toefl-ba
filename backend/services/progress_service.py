from typing import Any


def progress_analytics(state: dict[str, Any]) -> dict[str, Any]:
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

    scores = [int(value or 0) for value in progress.values()]
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


def recommendation(progress: dict[str, int]) -> dict[str, str]:
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
