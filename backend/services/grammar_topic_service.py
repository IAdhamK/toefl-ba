from __future__ import annotations

from copy import deepcopy
from typing import Any


GRAMMAR_LEVELS: list[dict[str, Any]] = [
    {
        "id": "basic",
        "title": "Basic Grammar",
        "description": "Pondasi membaca kalimat Inggris pendek secara pelan dan jelas.",
        "objective": "User bisa menemukan subject, main verb, object/complement, dan informasi tambahan.",
    },
    {
        "id": "intermediate",
        "title": "Intermediate Grammar",
        "description": "Pola kalimat yang sering membuat pemula terkecoh di TOEFL dan konteks BA.",
        "objective": "User bisa membedakan main clause, phrase, clause, connector, dan grammar trap.",
    },
    {
        "id": "advanced",
        "title": "Advanced Grammar",
        "description": "Grammar untuk academic reading dan Business Analyst writing yang lebih formal.",
        "objective": "User bisa membaca kalimat kompleks dan menulis analisis BA dengan lebih profesional.",
    },
]


GRAMMAR_TOPICS: list[dict[str, Any]] = [
    {
        "id": "parts_of_speech",
        "level": "basic",
        "order": 1,
        "title": "Parts of Speech",
        "short_title": "Word Types",
        "purpose": "Mengenali fungsi kata seperti noun, verb, adjective, adverb, preposition, conjunction, dan pronoun.",
        "explanation_id": "Jenis kata membantu kamu tahu peran setiap kata sebelum membaca kalimat panjang.",
        "example_sentence": "The analyst reviews detailed requirements carefully.",
        "example_meaning_id": "Analis meninjau requirement yang detail dengan hati-hati.",
        "beginner_tip": "Cari dulu kata benda dan kata kerja. Itu biasanya tulang utama kalimat.",
        "common_trap": "Jangan menerjemahkan kata satu per satu tanpa tahu jenis katanya.",
        "ba_context": "Dipakai saat membaca requirement, stakeholder note, dan business report.",
        "estimated_minutes": 8,
        "status_default": "not_started",
    },
    {
        "id": "subject_verb",
        "level": "basic",
        "order": 2,
        "title": "Subject and Verb",
        "short_title": "Subject + Verb",
        "purpose": "Menemukan pelaku utama dan aksi utama dalam kalimat.",
        "explanation_id": "Subject adalah pelaku/topik utama. Verb adalah aksi atau keadaan utama.",
        "example_sentence": "The business analyst documents the stakeholder needs.",
        "example_meaning_id": "Business Analyst mendokumentasikan kebutuhan stakeholder.",
        "beginner_tip": "Tanya: siapa yang melakukan sesuatu? Lalu cari aksi utamanya.",
        "common_trap": "Jangan mengira semua kata kerja bentuk -ing adalah main verb.",
        "ba_context": "Penting untuk memahami siapa melakukan apa dalam requirement dan process description.",
        "estimated_minutes": 10,
        "status_default": "not_started",
    },
    {
        "id": "object_complement",
        "level": "basic",
        "order": 3,
        "title": "Object and Complement",
        "short_title": "Object/Complement",
        "purpose": "Memahami bagian setelah verb: object, complement, atau informasi pelengkap.",
        "explanation_id": "Object menerima aksi. Complement menjelaskan subject atau object.",
        "example_sentence": "The team considers the requirement important.",
        "example_meaning_id": "Tim menganggap requirement itu penting.",
        "beginner_tip": "Setelah menemukan verb, lihat bagian setelahnya: apa yang terkena aksi atau dijelaskan?",
        "common_trap": "Complement kadang terlihat seperti object, padahal fungsinya memberi penjelasan.",
        "ba_context": "Berguna saat membaca stakeholder evaluation dan acceptance criteria.",
        "estimated_minutes": 10,
        "status_default": "not_started",
    },
    {
        "id": "modal_verb",
        "level": "basic",
        "order": 4,
        "title": "Modal Verb",
        "short_title": "Modal",
        "purpose": "Memahami kata bantu seperti must, should, can, may, dan could.",
        "explanation_id": "Modal verb menunjukkan kewajiban, saran, kemampuan, atau kemungkinan.",
        "example_sentence": "The analyst must clarify the problem before proposing a solution.",
        "example_meaning_id": "Analis harus mengklarifikasi masalah sebelum mengusulkan solusi.",
        "beginner_tip": "Setelah modal, biasanya verb utama memakai bentuk dasar.",
        "common_trap": "Jangan tambahkan -s setelah verb yang mengikuti modal, misalnya must clarifies.",
        "ba_context": "Sering muncul dalam requirement, recommendation, dan risk statement.",
        "estimated_minutes": 8,
        "status_default": "not_started",
    },
    {
        "id": "simple_sentence_pattern",
        "level": "basic",
        "order": 5,
        "title": "Simple Sentence Pattern",
        "short_title": "Sentence Pattern",
        "purpose": "Mengenali pola dasar seperti Subject + Verb + Object.",
        "explanation_id": "Pola dasar membantu kamu membaca kalimat tanpa panik saat ada banyak kata tambahan.",
        "example_sentence": "Stakeholders provide feedback.",
        "example_meaning_id": "Stakeholder memberikan feedback.",
        "beginner_tip": "Mulai dari pola kecil dulu: subject, verb, lalu object jika ada.",
        "common_trap": "Jangan langsung fokus pada semua kata tambahan sebelum menemukan pola utama.",
        "ba_context": "Dipakai untuk membuat requirement sentence yang jelas.",
        "estimated_minutes": 9,
        "status_default": "not_started",
    },
    {
        "id": "simple_tense",
        "level": "basic",
        "order": 6,
        "title": "Simple Tense",
        "short_title": "Tense",
        "purpose": "Memahami waktu kejadian dalam kalimat sederhana.",
        "explanation_id": "Simple tense membantu membedakan kebiasaan, fakta umum, dan kejadian lampau.",
        "example_sentence": "The analyst interviews users every week.",
        "example_meaning_id": "Analis mewawancarai user setiap minggu.",
        "beginner_tip": "Perhatikan verb dan time signal seperti every week, yesterday, atau currently.",
        "common_trap": "Jangan hanya melihat time signal; bentuk verb tetap harus dicek.",
        "ba_context": "Berguna untuk process description dan project update.",
        "estimated_minutes": 10,
        "status_default": "not_started",
    },
    {
        "id": "prepositional_phrase",
        "level": "basic",
        "order": 7,
        "title": "Prepositional Phrase",
        "short_title": "Prep Phrase",
        "purpose": "Mengenali frasa yang diawali preposition seperti in, on, with, before, after, dan from.",
        "explanation_id": "Prepositional phrase biasanya memberi informasi tambahan tentang tempat, waktu, cara, atau hubungan.",
        "example_sentence": "The analyst works with stakeholders in a complex project.",
        "example_meaning_id": "Analis bekerja dengan stakeholder dalam proyek yang kompleks.",
        "beginner_tip": "Jika bagian kalimat diawali in/with/before/from, cek apakah itu hanya keterangan tambahan.",
        "common_trap": "Jangan menganggap noun di dalam prepositional phrase sebagai subject utama.",
        "ba_context": "Sering muncul saat menjelaskan project context dan stakeholder relationship.",
        "estimated_minutes": 9,
        "status_default": "not_started",
    },
    {
        "id": "gerund_vs_main_verb",
        "level": "intermediate",
        "order": 1,
        "title": "Gerund vs Main Verb",
        "short_title": "Gerund/Main Verb",
        "purpose": "Membedakan kata kerja bentuk -ing sebagai noun/modifier dengan verb utama.",
        "explanation_id": "Tidak semua kata berakhiran -ing adalah verb utama kalimat.",
        "example_sentence": "Operating within a complex environment, the analyst must align requirements with strategy.",
        "example_meaning_id": "Saat bekerja dalam lingkungan kompleks, analis harus menyelaraskan requirement dengan strategy.",
        "beginner_tip": "Cari subject utama dulu. Main verb biasanya muncul setelah subject utama.",
        "common_trap": "Mengira Operating adalah main verb, padahal main verb-nya adalah must align.",
        "ba_context": "Muncul saat membaca kalimat panjang tentang kondisi kerja analis.",
        "estimated_minutes": 12,
        "status_default": "not_started",
    },
    {
        "id": "infinitive_phrase",
        "level": "intermediate",
        "order": 2,
        "title": "Infinitive Phrase",
        "short_title": "To + Verb",
        "purpose": "Memahami frasa to + verb sebagai tujuan atau pelengkap.",
        "explanation_id": "Infinitive phrase sering menjelaskan tujuan suatu aksi.",
        "example_sentence": "The analyst uses interviews to understand stakeholder expectations.",
        "example_meaning_id": "Analis menggunakan interview untuk memahami ekspektasi stakeholder.",
        "beginner_tip": "Jika melihat to + verb, tanyakan: ini tujuan dari aksi apa?",
        "common_trap": "Menganggap to understand sebagai main verb, padahal main verb-nya uses.",
        "ba_context": "Berguna dalam kalimat tentang teknik elicitation dan analysis purpose.",
        "estimated_minutes": 11,
        "status_default": "not_started",
    },
    {
        "id": "relative_clause",
        "level": "intermediate",
        "order": 3,
        "title": "Relative Clause",
        "short_title": "Who/Which/That",
        "purpose": "Memahami clause yang menjelaskan noun dengan who, which, atau that.",
        "explanation_id": "Relative clause memberi informasi tambahan tentang noun sebelumnya.",
        "example_sentence": "The requirement that the team approved must be documented.",
        "example_meaning_id": "Requirement yang disetujui tim harus didokumentasikan.",
        "beginner_tip": "Cari noun yang dijelaskan oleh that/who/which.",
        "common_trap": "Mengira relative clause adalah kalimat utama.",
        "ba_context": "Sering muncul dalam requirement documentation dan approval notes.",
        "estimated_minutes": 12,
        "status_default": "not_started",
    },
    {
        "id": "reduced_relative_clause",
        "level": "intermediate",
        "order": 4,
        "title": "Reduced Relative Clause",
        "short_title": "Reduced Clause",
        "purpose": "Memahami relative clause yang dipendekkan.",
        "explanation_id": "Reduced relative clause memotong kata seperti that is atau that were.",
        "example_sentence": "The requirements approved by stakeholders are ready for development.",
        "example_meaning_id": "Requirement yang disetujui stakeholder sudah siap untuk development.",
        "beginner_tip": "Jika ada verb bentuk V3 setelah noun, cek apakah itu menjelaskan noun.",
        "common_trap": "Mengira approved adalah main verb, padahal main verb-nya are.",
        "ba_context": "Berguna saat membaca approval status dan project documentation.",
        "estimated_minutes": 13,
        "status_default": "not_started",
    },
    {
        "id": "passive_voice",
        "level": "intermediate",
        "order": 5,
        "title": "Passive Voice",
        "short_title": "Passive",
        "purpose": "Memahami kalimat pasif saat fokusnya pada proses atau hasil.",
        "explanation_id": "Passive voice menaruh fokus pada hal yang dikenai aksi.",
        "example_sentence": "The workflow is reviewed before automation is proposed.",
        "example_meaning_id": "Workflow ditinjau sebelum automation diusulkan.",
        "beginner_tip": "Cari pola be + V3, seperti is reviewed atau was approved.",
        "common_trap": "Menerjemahkan passive voice seperti active voice.",
        "ba_context": "Sering dipakai saat menjelaskan process governance dan documentation.",
        "estimated_minutes": 12,
        "status_default": "not_started",
    },
    {
        "id": "parallel_structure",
        "level": "intermediate",
        "order": 6,
        "title": "Parallel Structure",
        "short_title": "Parallel",
        "purpose": "Memastikan item dalam daftar atau pasangan grammar memiliki bentuk yang seimbang.",
        "explanation_id": "Parallel structure membuat kalimat lebih rapi dan mudah dibaca.",
        "example_sentence": "The analyst identifies issues, documents requirements, and validates solutions.",
        "example_meaning_id": "Analis mengidentifikasi masalah, mendokumentasikan requirement, dan memvalidasi solusi.",
        "beginner_tip": "Dalam daftar aksi, cek apakah bentuk verb-nya sejajar.",
        "common_trap": "Mencampur bentuk identifies, documenting, dan validates dalam satu daftar.",
        "ba_context": "Penting untuk requirement list, responsibility statement, dan report writing.",
        "estimated_minutes": 11,
        "status_default": "not_started",
    },
    {
        "id": "connector_logic",
        "level": "intermediate",
        "order": 7,
        "title": "Connector Logic",
        "short_title": "Connectors",
        "purpose": "Memahami hubungan ide melalui because, although, therefore, however, dan while.",
        "explanation_id": "Connector menunjukkan hubungan sebab, akibat, kontras, atau waktu.",
        "example_sentence": "Although the process is slow, automation is not always the best solution.",
        "example_meaning_id": "Walaupun prosesnya lambat, automation belum tentu solusi terbaik.",
        "beginner_tip": "Jangan hanya terjemahkan connector; pahami hubungan antar ide.",
        "common_trap": "Mengabaikan although/however sehingga makna kontras hilang.",
        "ba_context": "Berguna untuk reasoning dalam recommendation dan impact analysis.",
        "estimated_minutes": 12,
        "status_default": "not_started",
    },
    {
        "id": "complex_sentence_mapping",
        "level": "advanced",
        "order": 1,
        "title": "Complex Sentence Mapping",
        "short_title": "Sentence Map",
        "purpose": "Memetakan main clause, subordinate clause, phrase, dan modifier.",
        "explanation_id": "Kalimat panjang bisa dipahami jika dipisah menjadi bagian utama dan tambahan.",
        "example_sentence": "Before recommending automation, the analyst evaluates whether the current process should be redesigned.",
        "example_meaning_id": "Sebelum merekomendasikan automation, analis mengevaluasi apakah proses saat ini harus didesain ulang.",
        "beginner_tip": "Cari main clause terlebih dahulu, lalu baca phrase dan clause tambahan.",
        "common_trap": "Membaca semua bagian kalimat dengan bobot yang sama.",
        "ba_context": "Dipakai dalam process analysis dan solution evaluation.",
        "estimated_minutes": 15,
        "status_default": "not_started",
    },
    {
        "id": "nominalization",
        "level": "advanced",
        "order": 2,
        "title": "Nominalization",
        "short_title": "Noun Form",
        "purpose": "Memahami perubahan verb/adjective menjadi noun agar tulisan lebih formal.",
        "explanation_id": "Nominalization membuat kalimat terlihat lebih formal dan academic.",
        "example_sentence": "The evaluation of stakeholder feedback supports better prioritization.",
        "example_meaning_id": "Evaluasi feedback stakeholder mendukung prioritas yang lebih baik.",
        "beginner_tip": "Perhatikan noun formal seperti evaluation, prioritization, dan implementation.",
        "common_trap": "Menulis terlalu banyak noun formal sampai kalimat menjadi berat.",
        "ba_context": "Sering dipakai dalam business case, report, dan recommendation.",
        "estimated_minutes": 14,
        "status_default": "not_started",
    },
    {
        "id": "hedging_language",
        "level": "advanced",
        "order": 3,
        "title": "Hedging Language",
        "short_title": "Hedging",
        "purpose": "Memahami bahasa yang tidak terlalu absolut seperti may, might, likely, dan appears to.",
        "explanation_id": "Hedging membantu menyampaikan analisis dengan hati-hati saat bukti belum lengkap.",
        "example_sentence": "The delay may indicate a bottleneck in the approval workflow.",
        "example_meaning_id": "Keterlambatan itu mungkin menunjukkan bottleneck dalam alur approval.",
        "beginner_tip": "Kata seperti may atau likely berarti kemungkinan, bukan kepastian.",
        "common_trap": "Menganggap may indicate sebagai kepastian penuh.",
        "ba_context": "Penting untuk risk analysis dan stakeholder communication.",
        "estimated_minutes": 13,
        "status_default": "not_started",
    },
    {
        "id": "inversion",
        "level": "advanced",
        "order": 4,
        "title": "Inversion",
        "short_title": "Inversion",
        "purpose": "Memahami susunan kata formal yang tidak biasa.",
        "explanation_id": "Inversion mengubah urutan subject dan auxiliary untuk penekanan formal.",
        "example_sentence": "Only after the requirements are validated can the team estimate the solution accurately.",
        "example_meaning_id": "Hanya setelah requirement divalidasi, tim dapat mengestimasi solusi dengan akurat.",
        "beginner_tip": "Jika kalimat diawali only/rarely/never, perhatikan susunan auxiliary dan subject.",
        "common_trap": "Menganggap can the team sebagai pertanyaan biasa.",
        "ba_context": "Dipakai untuk menekankan syarat penting dalam project decision.",
        "estimated_minutes": 15,
        "status_default": "not_started",
    },
    {
        "id": "conditional_sentence",
        "level": "advanced",
        "order": 5,
        "title": "Conditional Sentence",
        "short_title": "If Clause",
        "purpose": "Memahami hubungan syarat dan hasil.",
        "explanation_id": "Conditional sentence menjelaskan apa yang terjadi jika kondisi tertentu terpenuhi.",
        "example_sentence": "If the approval process remains unclear, the implementation may be delayed.",
        "example_meaning_id": "Jika proses approval tetap tidak jelas, implementation mungkin tertunda.",
        "beginner_tip": "Pisahkan if-clause dan result-clause.",
        "common_trap": "Tidak membedakan kondisi, hasil, dan tingkat kemungkinan.",
        "ba_context": "Dipakai untuk risk, impact, dan dependency analysis.",
        "estimated_minutes": 13,
        "status_default": "not_started",
    },
    {
        "id": "academic_connectors",
        "level": "advanced",
        "order": 6,
        "title": "Academic Connectors",
        "short_title": "Academic Links",
        "purpose": "Memahami connector formal seperti therefore, nevertheless, consequently, dan in contrast.",
        "explanation_id": "Academic connectors membuat hubungan ide terlihat jelas dalam tulisan formal.",
        "example_sentence": "The data is inconsistent; therefore, the report cannot be finalized.",
        "example_meaning_id": "Data tidak konsisten; karena itu, report belum bisa difinalkan.",
        "beginner_tip": "Tandai connector dan tentukan apakah artinya sebab-akibat, kontras, atau tambahan.",
        "common_trap": "Memakai connector formal tanpa memahami logikanya.",
        "ba_context": "Berguna dalam executive summary dan recommendation report.",
        "estimated_minutes": 12,
        "status_default": "not_started",
    },
    {
        "id": "formal_ba_writing",
        "level": "advanced",
        "order": 7,
        "title": "Formal BA Writing",
        "short_title": "BA Writing",
        "purpose": "Membuat kalimat BA yang formal, jelas, dan tidak ambigu.",
        "explanation_id": "Formal BA writing menekankan clarity, scope, constraint, dan business impact.",
        "example_sentence": "The proposed solution should address the approval delay without increasing manual workload.",
        "example_meaning_id": "Solusi yang diusulkan harus menangani delay approval tanpa menambah beban kerja manual.",
        "beginner_tip": "Sebutkan solusi, masalah, dan batasan dengan jelas.",
        "common_trap": "Membuat kalimat terlalu umum seperti the system should be better.",
        "ba_context": "Dipakai dalam requirement, acceptance criteria, dan stakeholder recommendation.",
        "estimated_minutes": 15,
        "status_default": "not_started",
    },
]


def _topic_counts() -> dict[str, int]:
    return {level["id"]: len([topic for topic in GRAMMAR_TOPICS if topic["level"] == level["id"]]) for level in GRAMMAR_LEVELS}


def get_grammar_levels() -> list[dict[str, Any]]:
    counts = _topic_counts()
    levels = []
    for level in GRAMMAR_LEVELS:
        item = deepcopy(level)
        item["topic_count"] = counts.get(level["id"], 0)
        levels.append(item)
    return levels


def get_grammar_topics(level: str | None = None) -> list[dict[str, Any]]:
    normalized = level.lower() if level else None
    topics = [topic for topic in GRAMMAR_TOPICS if normalized is None or topic["level"] == normalized]
    return deepcopy(sorted(topics, key=lambda item: (_level_order(item["level"]), item["order"])))


def get_grammar_topic(topic_id: str) -> dict[str, Any] | None:
    for topic in GRAMMAR_TOPICS:
        if topic["id"] == topic_id:
            return deepcopy(topic)
    return None


def get_next_topic(topic_id: str | None = None) -> dict[str, Any] | None:
    ordered = sorted(GRAMMAR_TOPICS, key=lambda item: (_level_order(item["level"]), item["order"]))
    if not ordered:
        return None
    if not topic_id:
        return deepcopy(next((topic for topic in ordered if topic["id"] == "subject_verb"), ordered[0]))
    for index, topic in enumerate(ordered):
        if topic["id"] == topic_id:
            return deepcopy(ordered[(index + 1) % len(ordered)])
    return deepcopy(next((topic for topic in ordered if topic["id"] == "subject_verb"), ordered[0]))


def get_topic_summary() -> dict[str, Any]:
    counts = _topic_counts()
    return {
        "total_topics": len(GRAMMAR_TOPICS),
        "levels": counts,
        "recommended_start_topic": "subject_verb",
    }


def _level_order(level: str) -> int:
    order = {"basic": 0, "intermediate": 1, "advanced": 2}
    return order.get(level, 99)
