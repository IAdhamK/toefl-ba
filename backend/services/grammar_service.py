from __future__ import annotations

import re


MODALS = ("must", "should", "can", "could", "may", "might", "will", "would")
ING_CONFUSION_WORDS = ("operating", "working", "analyzing", "managing", "reviewing", "validating")
RELATIVE_MARKERS = (" who ", " which ", " that ")
CONNECTORS = ("although", "because", "while", "whereas", "therefore", "however", "consequently")
ACADEMIC_CONNECTORS = ("therefore", "however", "consequently")
NOMINALIZATIONS = (
    "implementation",
    "decision",
    "analysis",
    "alignment",
    "validation",
    "prioritization",
    "documentation",
    "improvement",
)
PASSIVE_PATTERNS = (
    "is documented",
    "are documented",
    "was reviewed",
    "were reviewed",
    "is expected",
    "are required",
    "be implemented",
)
BA_KEYWORDS = (
    "business analyst",
    "requirements",
    "requirement",
    "stakeholder",
    "stakeholders",
    "strategy",
    "alignment",
    "implementation",
    "traceability",
    "ambiguity",
    "approval",
    "workflow",
)


def grammar_breakdown(sentence: str) -> dict:
    sentence = (sentence or "").strip()
    lowered = sentence.lower()
    subject = detect_main_subject(sentence)
    main_verb = detect_main_verb(sentence)
    modifier_phrases = detect_modifier_phrases(sentence)
    clauses = detect_clauses(sentence)
    grammar_patterns = detect_grammar_patterns(sentence)
    recommended_topic_id = detect_recommended_topic(sentence)
    phrase = modifier_phrases[0]["text"] if modifier_phrases else "Look for modifier phrases"
    pattern = _legacy_pattern(grammar_patterns)
    explanation = _legacy_explanation(sentence, grammar_patterns)
    translation = build_simple_meaning(sentence)

    return {
        # Backward-compatible fields used by the existing frontend.
        "subject": subject,
        "mainVerb": main_verb,
        "phrase": phrase,
        "pattern": pattern,
        "translation": translation,
        "explanation": explanation,
        # Deep Grammar Breakdown fields.
        "sentence_level": detect_sentence_level(sentence),
        "sentence_type": detect_sentence_type(sentence),
        "main_subject": subject,
        "main_verb": main_verb,
        "object_or_complement": detect_object_or_complement(sentence),
        "modifier_phrases": modifier_phrases,
        "clauses": clauses,
        "grammar_patterns": grammar_patterns,
        "common_trap": detect_common_trap(sentence),
        "simple_meaning_id": build_simple_meaning(sentence),
        "ba_context_meaning": build_ba_context_meaning(sentence),
        "structure_steps": build_structure_steps(sentence),
        "detected_keywords": detect_keywords(sentence),
        "grammar_focus": recommended_topic_id,
        "next_practice": _next_practice(recommended_topic_id),
        "recommended_topic_id": recommended_topic_id,
        "confidence_note": "Rule-based analysis. For unusual sentences, result may be approximate.",
    }


def detect_sentence_level(sentence: str) -> str:
    lowered = sentence.lower()
    patterns = detect_grammar_patterns(sentence)
    has_advanced = any(item in patterns for item in ("nominalization", "academic connector")) or (
        "passive voice" in patterns and len(sentence.split()) >= 14
    )
    if has_advanced:
        return "advanced"
    if any(
        [
            any(modal in lowered.split() for modal in MODALS),
            any(word in lowered for word in ING_CONFUSION_WORDS),
            "passive voice" in patterns,
            "relative clause" in patterns,
            "connector logic" in patterns,
            "parallel structure" in patterns,
        ]
    ):
        return "intermediate"
    return "basic"


def detect_sentence_type(sentence: str) -> str:
    lowered = f" {sentence.lower()} "
    if not sentence or len(sentence.split()) < 3:
        return "fragment_or_unclear"
    has_connector = any(connector in lowered for connector in CONNECTORS)
    has_relative = any(marker in lowered for marker in RELATIVE_MARKERS)
    has_coordinator = bool(re.search(r"\b(and|but|or)\b", lowered))
    if has_connector and has_coordinator:
        return "compound_complex"
    if has_connector or has_relative or "," in sentence:
        return "complex"
    if has_coordinator and len(sentence.split()) > 10:
        return "compound"
    return "simple"


def detect_main_subject(sentence: str) -> str:
    lowered = sentence.lower()
    if "business analyst" in lowered:
        return _matching_phrase(sentence, "business analyst", "A business analyst")
    if lowered.startswith("the implementation"):
        return "The implementation of an integrated requirement management system"
    match = re.match(r"^\s*([A-Z][^,.]+?)\s+(must|should|can|could|may|might|will|would|is|are|was|were|reviews?|documents?|provides?|works?)\b", sentence)
    if match:
        return match.group(1).strip()
    words = sentence.split()
    return " ".join(words[:2]) if words else "Identify the noun phrase before the main verb"


def detect_main_verb(sentence: str) -> str:
    lowered = sentence.lower()
    if "not only" in lowered and "but also" in lowered and "must" in lowered:
        return "must elicit / must ensure"
    modal_match = re.search(r"\b(must|should|can|could|may|might|will|would)\s+([a-z]+)\b", lowered)
    if modal_match:
        return f"{modal_match.group(1)} {modal_match.group(2)}"
    if "is expected to improve" in lowered:
        return "is expected to improve"
    passive_match = re.search(r"\b(is|are|was|were|be)\s+([a-z]+ed|required|expected|implemented)\b", lowered)
    if passive_match:
        return passive_match.group(0)
    finite_match = re.search(r"\b(reviews?|documents?|provides?|works?|evaluates?|supports?|reduces?|improves?)\b", lowered)
    return finite_match.group(0) if finite_match else "Find the finite verb after the subject"


def detect_object_or_complement(sentence: str) -> str:
    lowered = sentence.lower()
    if "elicit requirements" in lowered and "ensure alignment" in lowered:
        return "requirements; alignment between stakeholder needs and organizational strategy"
    if "elicit requirements" in lowered:
        return "requirements from stakeholders" if "from stakeholders" in lowered else "requirements"
    if "approval rule" in lowered:
        return "the approval rule"
    if "traceability" in lowered and "ambiguity" in lowered:
        return "traceability; ambiguity; strategic alignment"
    return "Object/complement appears after the main verb; review manually if the sentence is unusual."


def detect_modifier_phrases(sentence: str) -> list[dict]:
    lowered = sentence.lower()
    phrases = []
    if "operating within a complex enterprise environment" in lowered:
        phrases.append(
            {
                "text": "operating within a complex enterprise environment",
                "function": "reduced relative clause / modifier",
                "explanation_id": "Bagian ini menjelaskan business analyst, bukan aksi utama.",
            }
        )
    if "of an integrated requirement management system" in lowered:
        phrases.append(
            {
                "text": "of an integrated requirement management system",
                "function": "prepositional phrase",
                "explanation_id": "Bagian ini menjelaskan implementation yang sedang dibahas.",
            }
        )
    if "between stakeholder needs and organizational strategy" in lowered:
        phrases.append(
            {
                "text": "between stakeholder needs and organizational strategy",
                "function": "prepositional phrase",
                "explanation_id": "Bagian ini menjelaskan alignment atau keselarasan.",
            }
        )
    return phrases


def detect_clauses(sentence: str) -> list[dict]:
    lowered = sentence.lower()
    if not sentence:
        return []
    clauses = [
        {
            "type": "main_clause",
            "text": _main_clause_text(sentence),
            "explanation_id": "Ini bagian utama kalimat.",
        }
    ]
    if any(marker in f" {lowered} " for marker in RELATIVE_MARKERS):
        clauses.append(
            {
                "type": "relative_clause",
                "text": "Clause dengan who/which/that menjelaskan noun sebelumnya.",
                "explanation_id": "Relative clause memberi informasi tambahan tentang noun.",
            }
        )
    if any(connector in f" {lowered} " for connector in CONNECTORS):
        clauses.append(
            {
                "type": "connector_clause",
                "text": "Clause dengan connector menunjukkan hubungan logika.",
                "explanation_id": "Perhatikan connector untuk memahami sebab, akibat, atau kontras.",
            }
        )
    return clauses


def detect_grammar_patterns(sentence: str) -> list[str]:
    lowered = sentence.lower()
    patterns = []
    if any(modal in lowered.split() for modal in MODALS):
        patterns.append("modal verb")
    if any(word in lowered for word in ING_CONFUSION_WORDS):
        patterns.append("reduced relative clause")
    if any(marker in f" {lowered} " for marker in RELATIVE_MARKERS):
        patterns.append("relative clause")
    if any(pattern in lowered for pattern in PASSIVE_PATTERNS) or re.search(r"\b(is|are|was|were|be)\s+\w+ed\b", lowered):
        patterns.append("passive voice")
    if ("not only" in lowered and "but also" in lowered) or ("both" in lowered and "and" in lowered) or ("either" in lowered and "or" in lowered) or ("neither" in lowered and "nor" in lowered) or _has_comma_parallel_verbs(lowered):
        patterns.append("parallel structure")
    if any(word in lowered for word in NOMINALIZATIONS):
        patterns.append("nominalization")
    if any(connector in f" {lowered} " for connector in CONNECTORS):
        patterns.append("academic connector" if any(connector in f" {lowered} " for connector in ACADEMIC_CONNECTORS) else "connector logic")
    if not patterns:
        patterns.append("simple sentence pattern")
    return patterns


def detect_common_trap(sentence: str) -> str:
    lowered = sentence.lower()
    main_verb = detect_main_verb(sentence)
    if any(word in lowered for word in ING_CONFUSION_WORDS):
        return f"User may think 'operating' or another -ing phrase is the main verb, but the main verb is '{main_verb}'."
    if "not only" in lowered and "but also" in lowered:
        return "User may miss that not only ... but also ... creates two parallel actions or ideas."
    if any(word in lowered for word in NOMINALIZATIONS):
        return "User may focus on long noun forms and miss the main passive or action structure."
    if "passive voice" in detect_grammar_patterns(sentence):
        return "User may translate passive voice like active voice and misunderstand what receives the action."
    return "Focus on the subject and main verb before translating every word."


def detect_recommended_topic(sentence: str) -> str:
    lowered = sentence.lower()
    patterns = detect_grammar_patterns(sentence)
    if any(word in lowered for word in ING_CONFUSION_WORDS):
        return "gerund_vs_main_verb"
    if "reduced relative clause" in patterns:
        return "reduced_relative_clause"
    if "relative clause" in patterns:
        return "relative_clause"
    if "passive voice" in patterns:
        return "passive_voice"
    if "parallel structure" in patterns:
        return "parallel_structure"
    if "nominalization" in patterns:
        return "nominalization"
    if "academic connector" in patterns:
        return "academic_connectors"
    if "connector logic" in patterns:
        return "connector_logic"
    if "modal verb" in patterns:
        return "modal_verb"
    return "subject_verb"


def build_structure_steps(sentence: str) -> list[str]:
    steps = [
        "Cari subject utama.",
        "Cari modal atau finite verb sebagai main verb.",
        "Lihat object/complement setelah verb.",
    ]
    lowered = sentence.lower()
    if any(word in lowered for word in ING_CONFUSION_WORDS):
        steps.insert(1, "Abaikan dulu phrase -ing yang hanya menjelaskan subject.")
    if "not only" in lowered and "but also" in lowered:
        steps.append("Periksa pola paralel seperti not only ... but also ...")
    if any(word in lowered for word in NOMINALIZATIONS):
        steps.append("Sederhanakan nominalization menjadi aksi agar makna lebih jelas.")
    return steps


def build_simple_meaning(sentence: str) -> str:
    lowered = sentence.lower()
    if "must not only elicit requirements" in lowered:
        return "Seorang business analyst yang bekerja dalam lingkungan enterprise kompleks harus menggali requirement dan memastikan keselarasan antara kebutuhan stakeholder dan strategi organisasi."
    if "must elicit requirements" in lowered:
        return "Seorang business analyst harus menggali kebutuhan dari stakeholder."
    if "implementation of an integrated requirement management system" in lowered:
        return "Implementasi sistem manajemen requirement terintegrasi diharapkan meningkatkan traceability, mengurangi ambiguity, dan mendukung alignment strategis."
    return "Makna sederhana: cari siapa pelaku, apa aksi utama, dan informasi tambahan setelah aksi."


def build_ba_context_meaning(sentence: str) -> str:
    lowered = sentence.lower()
    if "requirements" in lowered and "stakeholder" in lowered and "strategy" in lowered:
        return "Dalam konteks Business Analyst, kalimat ini menjelaskan bahwa BA tidak hanya mengumpulkan requirement, tetapi juga memastikan requirement sesuai kebutuhan stakeholder dan strategi organisasi."
    if "traceability" in lowered or "ambiguity" in lowered:
        return "Dalam konteks Business Analyst, kalimat ini menjelaskan manfaat sistem requirement management: requirement lebih mudah dilacak, tidak ambigu, dan selaras dengan tujuan strategis."
    if "requirements" in lowered:
        return "Dalam konteks Business Analyst, kalimat ini berkaitan dengan proses menggali, mendokumentasikan, atau memvalidasi requirement."
    return "Dalam konteks Business Analyst, pahami actor, aksi, object, dan dampak bisnis dari kalimat."


def detect_keywords(sentence: str) -> list[str]:
    lowered = sentence.lower()
    return [keyword for keyword in BA_KEYWORDS if keyword in lowered]


def _legacy_pattern(patterns: list[str]) -> str:
    if "parallel structure" in patterns:
        return "not only ... but also ..." if "modal verb" in patterns else "parallel verbs/items"
    if "passive voice" in patterns:
        return "be + past participle"
    if "modal verb" in patterns:
        return "Subject + modal + verb + object/complement"
    return "Subject + main verb + object/complement"


def _legacy_explanation(sentence: str, patterns: list[str]) -> str:
    if "reduced relative clause" in patterns:
        return "Bagian -ing seperti operating sering bukan verb utama. Verb utama muncul bersama modal atau finite verb."
    if "passive voice" in patterns:
        return "Kalimat pasif memakai pola be + past participle. Fokusnya pada hal yang menerima aksi."
    if "nominalization" in patterns:
        return "Nominalization membuat kalimat formal, tetapi pemula perlu menyederhanakannya menjadi aksi agar makna jelas."
    return "Cari subject sebagai pelaku dan verb sebagai aksi utama. Phrase panjang bisa dibaca belakangan."


def _next_practice(topic_id: str) -> str:
    labels = {
        "modal_verb": "Practice Modal Verb in requirement and recommendation sentences.",
        "gerund_vs_main_verb": "Practice Gerund vs Main Verb and Reduced Relative Clause.",
        "reduced_relative_clause": "Practice Reduced Relative Clause in long TOEFL sentences.",
        "relative_clause": "Practice Relative Clause with who, which, and that.",
        "passive_voice": "Practice Passive Voice in process and documentation sentences.",
        "parallel_structure": "Practice Parallel Structure in BA recommendations.",
        "nominalization": "Practice Nominalization in formal BA writing.",
        "academic_connectors": "Practice Academic Connectors for cause, contrast, and result.",
        "connector_logic": "Practice Connector Logic in TOEFL-style sentences.",
        "subject_verb": "Practice Subject and Verb foundation.",
    }
    return labels.get(topic_id, "Practice Subject and Verb foundation.")


def _matching_phrase(sentence: str, marker: str, fallback: str) -> str:
    pattern = re.compile(rf"\b(a|the)?\s*{re.escape(marker)}\b", re.IGNORECASE)
    match = pattern.search(sentence)
    return match.group(0).strip() if match else fallback


def _main_clause_text(sentence: str) -> str:
    if len(sentence) <= 120:
        return sentence
    return f"{sentence[:117]}..."


def _has_comma_parallel_verbs(lowered: str) -> bool:
    return "," in lowered and sum(1 for verb in ("improve", "reduce", "support", "document", "validate") if verb in lowered) >= 2


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
