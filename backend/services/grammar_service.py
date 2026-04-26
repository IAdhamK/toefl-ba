def grammar_breakdown(sentence: str) -> dict:
    lowered = sentence.lower()
    return {
        "subject": "A business analyst" if "business analyst" in lowered else "Identify the noun phrase before the main verb",
        "mainVerb": "must elicit / must ensure" if "must" in lowered else "Find the finite verb after the subject",
        "phrase": "operating within a complex enterprise environment" if "operating" in lowered else "Look for modifier phrases",
        "pattern": "not only ... but also ..." if "not only" in lowered else "Subject + main verb + object/complement",
        "translation": "Terjemahan natural perlu menjaga makna BA: aktor, tindakan, kebutuhan stakeholder, dan tujuan bisnis.",
        "explanation": "Bagian -ing sering berfungsi sebagai penjelas noun, bukan verb utama. Cari modal atau finite verb untuk menemukan aksi utama.",
    }


def indonesian_help(text: str, help_type: str = "simple") -> dict:
    lowered = text.lower()
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
    keywords = [label for key, label in keyword_map.items() if key in lowered]
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
