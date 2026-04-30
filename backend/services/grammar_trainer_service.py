from __future__ import annotations

from copy import deepcopy
from typing import Any

from backend.services.grammar_journey_service import get_grammar_journey, save_grammar_attempt
from backend.services.grammar_topic_service import get_grammar_topic, get_next_topic


BASIC_TRAINERS: dict[str, dict[str, Any]] = {
    "parts_of_speech": {
        "topic_id": "parts_of_speech",
        "level": "basic",
        "title": "Parts of Speech",
        "learning_objective": "Mengenali jenis kata agar kalimat Inggris lebih mudah dipetakan.",
        "explanation_id": "Sebelum mencari arti kalimat, pahami dulu fungsi kata: noun untuk benda/orang, verb untuk aksi, adjective untuk sifat, dan adverb untuk cara.",
        "beginner_tip": "Mulai dari noun dan verb. Dua jenis kata ini biasanya membentuk tulang utama kalimat.",
        "ba_context": "Dalam dokumen BA, parts of speech membantu membedakan actor, action, requirement, dan condition.",
        "examples": [
            {
                "sentence": "The analyst carefully reviews detailed requirements.",
                "simple_meaning_id": "Analis dengan hati-hati meninjau requirement yang detail.",
                "grammar_focus": "Noun + adverb + verb + adjective + noun",
                "breakdown": {
                    "subject": "The analyst",
                    "main_verb": "reviews",
                    "object": "detailed requirements",
                    "adverb": "carefully",
                },
            }
        ],
        "guided_items": [
            {
                "id": "parts_of_speech_guided_1",
                "instruction_id": "Pilih verb dalam kalimat ini.",
                "sentence": "The analyst reviews detailed requirements.",
                "target_part": "verb",
                "options": ["analyst", "reviews", "detailed"],
                "correct_answer": "reviews",
                "explanation_id": "\"reviews\" adalah verb karena menunjukkan aksi yang dilakukan analyst.",
                "beginner_tip": "Verb biasanya menjawab pertanyaan: melakukan apa?",
            }
        ],
        "quiz_items": [
            {
                "id": "parts_of_speech_quiz_1",
                "question_type": "choose_correct_pattern",
                "instruction_id": "Pilih jenis kata dari kata yang ditanyakan.",
                "sentence": "The analyst reviews detailed requirements.",
                "question": "Kata \"requirements\" termasuk jenis kata apa?",
                "options": ["noun", "verb", "adverb", "preposition"],
                "correct_answer": "noun",
                "explanation_id": "\"requirements\" adalah noun karena berarti kebutuhan atau hal yang dibahas.",
                "difficulty": "basic",
                "grammar_trap": "Jangan mengira semua kata panjang adalah verb.",
                "ba_context_note": "Requirement adalah noun utama dalam banyak dokumen BA.",
            }
        ],
    },
    "subject_verb": {
        "topic_id": "subject_verb",
        "level": "basic",
        "title": "Subject and Verb",
        "learning_objective": "Menemukan subject dan main verb dalam kalimat TOEFL + Business Analyst.",
        "explanation_id": "Subject adalah pelaku/topik utama. Main verb adalah aksi utama atau keadaan utama.",
        "beginner_tip": "Cari siapa pelakunya dulu, lalu cari aksi utama setelah subject.",
        "ba_context": "Skill ini penting saat membaca requirement, stakeholder statement, dan process description.",
        "examples": [
            {
                "sentence": "A business analyst must elicit requirements.",
                "simple_meaning_id": "Seorang business analyst harus menggali kebutuhan.",
                "grammar_focus": "Subject + modal + verb + object",
                "breakdown": {
                    "subject": "A business analyst",
                    "main_verb": "must elicit",
                    "object": "requirements",
                },
            }
        ],
        "guided_items": [
            {
                "id": "subject_verb_guided_1",
                "instruction_id": "Pilih main verb dalam kalimat ini.",
                "sentence": "A business analyst must elicit requirements.",
                "target_part": "main_verb",
                "options": ["A business analyst", "must elicit", "requirements"],
                "correct_answer": "must elicit",
                "explanation_id": "\"must elicit\" adalah main verb karena menunjukkan aksi utama yang harus dilakukan.",
                "beginner_tip": "Modal seperti must biasanya diikuti verb dasar.",
            }
        ],
        "quiz_items": [
            {
                "id": "subject_verb_quiz_1",
                "question_type": "identify_subject",
                "instruction_id": "Pilih subject dalam kalimat ini.",
                "sentence": "A business analyst must elicit requirements.",
                "question": "Mana subject kalimat ini?",
                "options": ["A business analyst", "must elicit", "requirements", "analyst must"],
                "correct_answer": "A business analyst",
                "explanation_id": "\"A business analyst\" adalah subject karena menjadi pelaku utama.",
                "difficulty": "basic",
                "grammar_trap": "Jangan memasukkan modal/verb ke dalam subject.",
                "ba_context_note": "Business analyst adalah actor yang melakukan elicitation.",
            },
            {
                "id": "subject_verb_quiz_2",
                "question_type": "identify_main_verb",
                "instruction_id": "Pilih main verb dalam kalimat ini.",
                "sentence": "A business analyst must elicit requirements.",
                "question": "Mana main verb kalimat ini?",
                "options": ["A business analyst", "must elicit", "requirements", "business"],
                "correct_answer": "must elicit",
                "explanation_id": "\"must elicit\" adalah main verb karena menunjukkan aksi utama.",
                "difficulty": "basic",
                "grammar_trap": "Jangan memilih noun seperti requirements sebagai verb.",
                "ba_context_note": "Elicit berarti menggali requirement dari stakeholder.",
            },
        ],
    },
    "object_complement": {
        "topic_id": "object_complement",
        "level": "basic",
        "title": "Object and Complement",
        "learning_objective": "Membedakan object dan complement setelah verb.",
        "explanation_id": "Object menerima aksi. Complement memberi penjelasan tambahan tentang subject atau object.",
        "beginner_tip": "Setelah verb, tanyakan: apa yang dikenai aksi? Atau bagian ini menjelaskan apa?",
        "ba_context": "Berguna saat memahami evaluation statement dan quality attribute.",
        "examples": [
            {
                "sentence": "The team considers the requirement important.",
                "simple_meaning_id": "Tim menganggap requirement itu penting.",
                "grammar_focus": "Subject + verb + object + complement",
                "breakdown": {
                    "subject": "The team",
                    "main_verb": "considers",
                    "object": "the requirement",
                    "complement": "important",
                },
            }
        ],
        "guided_items": [
            {
                "id": "object_complement_guided_1",
                "instruction_id": "Pilih object dalam kalimat ini.",
                "sentence": "The team considers the requirement important.",
                "target_part": "object",
                "options": ["The team", "considers", "the requirement", "important"],
                "correct_answer": "the requirement",
                "explanation_id": "\"the requirement\" adalah object karena hal itu yang dinilai oleh tim.",
                "beginner_tip": "Object biasanya berada setelah verb dan menerima aksi.",
            }
        ],
        "quiz_items": [
            {
                "id": "object_complement_quiz_1",
                "question_type": "identify_object",
                "instruction_id": "Pilih object dalam kalimat.",
                "sentence": "The team considers the requirement important.",
                "question": "Apa object kalimat ini?",
                "options": ["The team", "considers", "the requirement", "important"],
                "correct_answer": "the requirement",
                "explanation_id": "\"the requirement\" adalah object dari verb \"considers\".",
                "difficulty": "basic",
                "grammar_trap": "Jangan memilih important sebagai object; itu complement.",
                "ba_context_note": "Requirement adalah hal yang sedang dievaluasi.",
            },
            {
                "id": "object_complement_quiz_2",
                "question_type": "identify_object",
                "instruction_id": "Pilih complement dalam kalimat.",
                "sentence": "The team considers the requirement important.",
                "question": "Bagian mana yang menjadi complement?",
                "options": ["The team", "the requirement", "important", "considers"],
                "correct_answer": "important",
                "explanation_id": "\"important\" menjelaskan object \"the requirement\".",
                "difficulty": "basic",
                "grammar_trap": "Complement menjelaskan, bukan menerima aksi secara langsung.",
                "ba_context_note": "Dalam BA, complement sering menjelaskan status/kualitas requirement.",
            },
        ],
    },
    "modal_verb": {
        "topic_id": "modal_verb",
        "level": "basic",
        "title": "Modal Verb",
        "learning_objective": "Memahami must, should, can, may, dan could dalam kalimat BA.",
        "explanation_id": "Modal verb menunjukkan kewajiban, saran, kemampuan, atau kemungkinan.",
        "beginner_tip": "Setelah modal, pakai verb dasar: must clarify, should document, can improve.",
        "ba_context": "Modal sering muncul dalam requirement, policy, recommendation, dan risk statement.",
        "examples": [
            {
                "sentence": "The analyst should clarify the approval rule.",
                "simple_meaning_id": "Analis sebaiknya mengklarifikasi aturan approval.",
                "grammar_focus": "Subject + modal + base verb + object",
                "breakdown": {
                    "subject": "The analyst",
                    "modal": "should",
                    "main_verb": "should clarify",
                    "object": "the approval rule",
                },
            }
        ],
        "guided_items": [
            {
                "id": "modal_verb_guided_1",
                "instruction_id": "Pilih modal verb dalam kalimat ini.",
                "sentence": "The analyst should clarify the approval rule.",
                "target_part": "modal",
                "options": ["The analyst", "should", "clarify", "approval rule"],
                "correct_answer": "should",
                "explanation_id": "\"should\" adalah modal yang menunjukkan saran.",
                "beginner_tip": "Modal muncul sebelum verb dasar.",
            }
        ],
        "quiz_items": [
            {
                "id": "modal_verb_quiz_1",
                "question_type": "choose_correct_sentence",
                "instruction_id": "Pilih kalimat yang memakai modal dengan benar.",
                "sentence": "The analyst ___ clarify the issue.",
                "question": "Kalimat mana yang benar?",
                "options": ["The analyst must clarifies the issue.", "The analyst must clarify the issue.", "The analyst must clarified the issue.", "The analyst must clarification the issue."],
                "correct_answer": "The analyst must clarify the issue.",
                "explanation_id": "Setelah modal \"must\", gunakan verb dasar \"clarify\".",
                "difficulty": "basic",
                "grammar_trap": "Jangan memakai clarifies setelah modal.",
                "ba_context_note": "BA sering menggunakan must/should dalam requirement dan recommendation.",
            }
        ],
    },
    "simple_sentence_pattern": {
        "topic_id": "simple_sentence_pattern",
        "level": "basic",
        "title": "Simple Sentence Pattern",
        "learning_objective": "Mengenali pola kalimat dasar Subject + Verb + Object.",
        "explanation_id": "Pola dasar membuat kalimat panjang lebih mudah dibaca karena kamu tahu inti kalimatnya.",
        "beginner_tip": "Cari pola kecil dulu sebelum membaca phrase tambahan.",
        "ba_context": "Pola ini membantu menulis requirement yang jelas dan tidak ambigu.",
        "examples": [
            {
                "sentence": "Stakeholders provide feedback.",
                "simple_meaning_id": "Stakeholder memberikan feedback.",
                "grammar_focus": "Subject + verb + object",
                "breakdown": {
                    "subject": "Stakeholders",
                    "main_verb": "provide",
                    "object": "feedback",
                },
            }
        ],
        "guided_items": [
            {
                "id": "simple_sentence_pattern_guided_1",
                "instruction_id": "Pilih pola kalimat yang benar.",
                "sentence": "Stakeholders provide feedback.",
                "target_part": "pattern",
                "options": ["Subject + Verb + Object", "Verb + Subject + Object", "Object + Verb + Subject"],
                "correct_answer": "Subject + Verb + Object",
                "explanation_id": "Stakeholders = subject, provide = verb, feedback = object.",
                "beginner_tip": "Urutan dasar paling umum adalah Subject + Verb + Object.",
            }
        ],
        "quiz_items": [
            {
                "id": "simple_sentence_pattern_quiz_1",
                "question_type": "choose_correct_pattern",
                "instruction_id": "Pilih pola kalimat.",
                "sentence": "Stakeholders provide feedback.",
                "question": "Apa pola kalimat ini?",
                "options": ["Subject + Verb + Object", "Subject + Complement + Verb", "Verb + Object + Subject", "Object + Subject + Verb"],
                "correct_answer": "Subject + Verb + Object",
                "explanation_id": "Kalimat ini mengikuti pola Subject + Verb + Object.",
                "difficulty": "basic",
                "grammar_trap": "Jangan membaca object sebagai subject hanya karena muncul sebagai kata penting.",
                "ba_context_note": "Feedback adalah object yang diberikan stakeholder.",
            }
        ],
    },
    "simple_tense": {
        "topic_id": "simple_tense",
        "level": "basic",
        "title": "Simple Tense",
        "learning_objective": "Mengenali waktu kejadian dari bentuk verb sederhana.",
        "explanation_id": "Simple tense membantu membedakan kebiasaan, fakta umum, dan kejadian lampau.",
        "beginner_tip": "Lihat verb dan time signal seperti every week, yesterday, atau currently.",
        "ba_context": "Tense penting saat menulis status proyek dan process description.",
        "examples": [
            {
                "sentence": "The analyst interviews users every week.",
                "simple_meaning_id": "Analis mewawancarai user setiap minggu.",
                "grammar_focus": "Simple present for routine",
                "breakdown": {
                    "subject": "The analyst",
                    "main_verb": "interviews",
                    "object": "users",
                    "time_signal": "every week",
                },
            }
        ],
        "guided_items": [
            {
                "id": "simple_tense_guided_1",
                "instruction_id": "Pilih time signal dalam kalimat ini.",
                "sentence": "The analyst interviews users every week.",
                "target_part": "time_signal",
                "options": ["The analyst", "interviews", "users", "every week"],
                "correct_answer": "every week",
                "explanation_id": "\"every week\" menunjukkan rutinitas.",
                "beginner_tip": "Simple present sering dipakai untuk kegiatan rutin.",
            }
        ],
        "quiz_items": [
            {
                "id": "simple_tense_quiz_1",
                "question_type": "choose_correct_sentence",
                "instruction_id": "Pilih kalimat simple present yang benar.",
                "sentence": "The analyst ___ users every week.",
                "question": "Kalimat mana yang benar?",
                "options": ["The analyst interview users every week.", "The analyst interviews users every week.", "The analyst interviewed users every week.", "The analyst interviewing users every week."],
                "correct_answer": "The analyst interviews users every week.",
                "explanation_id": "Subject tunggal \"The analyst\" memakai verb \"interviews\" dalam simple present.",
                "difficulty": "basic",
                "grammar_trap": "Jangan lupa -s untuk subject tunggal pada simple present.",
                "ba_context_note": "Kalimat ini menggambarkan aktivitas rutin BA.",
            }
        ],
    },
    "prepositional_phrase": {
        "topic_id": "prepositional_phrase",
        "level": "basic",
        "title": "Prepositional Phrase",
        "learning_objective": "Mengenali phrase tambahan yang diawali preposition.",
        "explanation_id": "Prepositional phrase memberi informasi tambahan seperti tempat, waktu, cara, atau hubungan.",
        "beginner_tip": "Frasa yang diawali in/with/before/from sering bukan inti kalimat.",
        "ba_context": "Prepositional phrase sering muncul dalam project scope dan stakeholder context.",
        "examples": [
            {
                "sentence": "The analyst works with stakeholders in a complex project.",
                "simple_meaning_id": "Analis bekerja dengan stakeholder dalam proyek yang kompleks.",
                "grammar_focus": "Subject + verb + prepositional phrases",
                "breakdown": {
                    "subject": "The analyst",
                    "main_verb": "works",
                    "prepositional_phrase": "with stakeholders; in a complex project",
                },
            }
        ],
        "guided_items": [
            {
                "id": "prepositional_phrase_guided_1",
                "instruction_id": "Pilih prepositional phrase dalam kalimat.",
                "sentence": "The analyst works with stakeholders.",
                "target_part": "prepositional_phrase",
                "options": ["The analyst", "works", "with stakeholders"],
                "correct_answer": "with stakeholders",
                "explanation_id": "\"with stakeholders\" diawali preposition \"with\" dan memberi informasi tambahan.",
                "beginner_tip": "Prepositional phrase biasanya bukan subject atau main verb.",
            }
        ],
        "quiz_items": [
            {
                "id": "prepositional_phrase_quiz_1",
                "question_type": "simple_meaning_from_structure",
                "instruction_id": "Pilih fungsi phrase dalam kalimat.",
                "sentence": "The analyst works with stakeholders in a complex project.",
                "question": "Apa fungsi \"in a complex project\"?",
                "options": ["Subject utama", "Main verb", "Informasi tambahan tentang konteks proyek", "Object utama"],
                "correct_answer": "Informasi tambahan tentang konteks proyek",
                "explanation_id": "\"in a complex project\" menjelaskan konteks tempat/situasi pekerjaan.",
                "difficulty": "basic",
                "grammar_trap": "Jangan memilih noun di dalam phrase sebagai subject utama.",
                "ba_context_note": "Phrase ini membantu menjelaskan scope dan kompleksitas proyek.",
            }
        ],
    },
}


def _intermediate_trainer(
    topic_id: str,
    title: str,
    learning_objective: str,
    explanation_id: str,
    beginner_tip: str,
    common_trap: str,
    ba_context: str,
    sentence: str,
    simple_meaning_id: str,
    grammar_focus: str,
    breakdown: dict[str, str],
    correct_answer: str,
    question_type: str,
    question: str,
    options: list[str],
    trap_type: str,
    trap_question: str,
    trap_options: list[str],
    trap_answer: str,
    review_topic: str | None = None,
) -> dict[str, Any]:
    review_topic = review_topic or topic_id
    return {
        "topic_id": topic_id,
        "level": "intermediate",
        "title": title,
        "learning_objective": learning_objective,
        "explanation_id": explanation_id,
        "beginner_tip": beginner_tip,
        "common_trap": common_trap,
        "ba_context": ba_context,
        "examples": [
            {
                "sentence": sentence,
                "simple_meaning_id": simple_meaning_id,
                "grammar_focus": grammar_focus,
                "breakdown": breakdown,
                "why_it_is_confusing": common_trap,
                "ba_context_note": ba_context,
            }
        ],
        "guided_items": [
            {
                "id": f"{topic_id}_guided_1",
                "instruction_id": "Pilih bagian grammar yang diminta.",
                "sentence": sentence,
                "target_part": question_type,
                "options": options,
                "correct_answer": correct_answer,
                "explanation_id": explanation_id,
                "common_trap": common_trap,
                "beginner_tip": beginner_tip,
            }
        ],
        "quiz_items": [
            {
                "id": f"{topic_id}_quiz_1",
                "question_type": question_type,
                "instruction_id": "Jawab pertanyaan grammar berdasarkan kalimat.",
                "sentence": sentence,
                "question": question,
                "options": options,
                "correct_answer": correct_answer,
                "explanation_id": explanation_id,
                "difficulty": "intermediate",
                "grammar_trap": common_trap,
                "ba_context_note": ba_context,
                "recommended_review_topic": review_topic,
            }
        ],
        "trap_items": [
            {
                "id": f"{topic_id}_trap_1",
                "trap_type": trap_type,
                "incorrect_assumption": common_trap,
                "sentence": sentence,
                "question": trap_question,
                "options": trap_options,
                "correct_answer": trap_answer,
                "explanation_id": explanation_id,
                "why_wrong_answers_are_wrong": [
                    "Pilihan lain tidak menjelaskan fungsi grammar utama dalam kalimat.",
                    "Pilihan lain biasanya muncul karena user membaca kata per kata, bukan struktur.",
                    "Cek kembali subject, main verb, dan phrase/clause tambahan.",
                ],
            }
        ],
    }


INTERMEDIATE_TRAINERS: dict[str, dict[str, Any]] = {
    "gerund_vs_main_verb": _intermediate_trainer(
        "gerund_vs_main_verb",
        "Gerund vs Main Verb",
        "Membedakan kata -ing yang hanya modifier dengan main verb kalimat.",
        "\"working\" bukan main verb. Itu menjelaskan \"the analyst\". Main verb adalah \"must clarify\".",
        "Cari modal seperti must, should, can. Setelah modal biasanya ada verb utama.",
        "Banyak pemula mengira semua kata -ing adalah verb utama.",
        "Dalam konteks BA, kalimat ini menjelaskan tugas BA ketika berinteraksi dengan banyak stakeholder.",
        "The analyst working with stakeholders must clarify priorities.",
        "Analis yang bekerja dengan stakeholder harus memperjelas prioritas.",
        "Reduced phrase + modal verb",
        {
            "main_subject": "The analyst",
            "modifier_phrase": "working with stakeholders",
            "main_verb": "must clarify",
            "object": "priorities",
        },
        "must clarify",
        "identify_main_verb",
        "Mana main verb kalimat ini?",
        ["working", "must clarify", "stakeholders", "priorities"],
        "ing_as_main_verb",
        "Why is 'working' not the main verb?",
        ["Because it is only describing the analyst", "Because it is the object", "Because it is a noun", "Because it is a connector"],
        "Because it is only describing the analyst",
    ),
    "infinitive_phrase": _intermediate_trainer(
        "infinitive_phrase",
        "Infinitive Phrase",
        "Memahami frasa to + verb sebagai tujuan atau pelengkap.",
        "\"to understand stakeholder expectations\" menjelaskan tujuan interviews, bukan main verb.",
        "Jika melihat to + verb, tanyakan: ini tujuan dari aksi apa?",
        "User sering mengira to + verb adalah main verb utama.",
        "BA menggunakan infinitive phrase untuk menjelaskan tujuan interview, workshop, atau analysis.",
        "The analyst uses interviews to understand stakeholder expectations.",
        "Analis menggunakan interview untuk memahami ekspektasi stakeholder.",
        "Main verb + infinitive purpose phrase",
        {
            "main_subject": "The analyst",
            "main_verb": "uses",
            "object": "interviews",
            "infinitive_phrase": "to understand stakeholder expectations",
        },
        "to understand stakeholder expectations",
        "identify_modifier_phrase",
        "Bagian mana yang menunjukkan tujuan dari interviews?",
        ["The analyst", "uses", "interviews", "to understand stakeholder expectations"],
        "infinitive_as_main_verb",
        "Why is 'to understand' not the main verb?",
        ["Because it explains purpose", "Because it is the subject", "Because it is an object noun", "Because it is a connector"],
        "Because it explains purpose",
    ),
    "relative_clause": _intermediate_trainer(
        "relative_clause",
        "Relative Clause",
        "Memahami clause dengan who, which, atau that yang menjelaskan noun.",
        "\"that the team approved\" menjelaskan requirement mana yang dimaksud.",
        "Cari noun sebelum that/who/which. Clause setelahnya biasanya menjelaskan noun itu.",
        "User sering membaca relative clause sebagai kalimat utama.",
        "Relative clause sering muncul dalam requirement approval dan documentation.",
        "The requirement that the team approved must be documented.",
        "Requirement yang disetujui tim harus didokumentasikan.",
        "Relative clause + modal/passive meaning",
        {
            "main_subject": "The requirement",
            "relative_clause": "that the team approved",
            "main_verb": "must be documented",
        },
        "that the team approved",
        "identify_relative_clause",
        "Mana relative clause dalam kalimat ini?",
        ["The requirement", "that the team approved", "must be documented", "the team"],
        "relative_clause_as_main_clause",
        "What does 'that the team approved' do?",
        ["It explains the requirement", "It is the main verb", "It is the object", "It is a connector only"],
        "It explains the requirement",
    ),
    "reduced_relative_clause": _intermediate_trainer(
        "reduced_relative_clause",
        "Reduced Relative Clause",
        "Memahami relative clause yang dipendekkan tanpa that/who/which.",
        "\"working with stakeholders\" menjelaskan analyst. Verb utama adalah \"must document\".",
        "Jika ada -ing atau V3 setelah noun, cek apakah itu hanya menjelaskan noun.",
        "User may think 'working' is the main verb.",
        "Reduced relative clause membuat kalimat dokumentasi BA lebih ringkas.",
        "The analyst working with stakeholders must document the requirement.",
        "Analis yang bekerja dengan stakeholder harus mendokumentasikan requirement.",
        "Reduced relative clause + modal verb",
        {
            "main_subject": "The analyst",
            "modifier_phrase": "working with stakeholders",
            "main_verb": "must document",
            "object": "the requirement",
        },
        "working with stakeholders",
        "identify_modifier_phrase",
        "Bagian mana yang hanya menjelaskan analyst?",
        ["The analyst", "working with stakeholders", "must document", "the requirement"],
        "ing_as_main_verb",
        "Why is 'working' not the main verb?",
        ["Because it is only describing the analyst", "Because it is the object", "Because it is a noun", "Because it is a connector"],
        "Because it is only describing the analyst",
    ),
    "passive_voice": _intermediate_trainer(
        "passive_voice",
        "Passive Voice",
        "Mengenali pola be + V3 saat fokus kalimat ada pada proses/hasil.",
        "\"is reviewed\" adalah passive voice karena workflow menerima aksi review.",
        "Cari pola be + V3 seperti is reviewed, are documented, was approved.",
        "User sering menerjemahkan passive seperti active sehingga pelaku dan objek tertukar.",
        "Passive voice sering dipakai dalam process governance dan documentation.",
        "The workflow is reviewed before automation is proposed.",
        "Workflow ditinjau sebelum automation diusulkan.",
        "Passive voice + connector phrase",
        {
            "main_subject": "The workflow",
            "passive_voice": "is reviewed",
            "connector_phrase": "before automation is proposed",
        },
        "is reviewed",
        "identify_passive_voice",
        "Mana bentuk passive voice?",
        ["The workflow", "is reviewed", "before", "automation"],
        "passive_as_active",
        "Why is this passive voice?",
        ["Because it uses be + past participle", "Because it has a modal", "Because it starts with The", "Because it has before"],
        "Because it uses be + past participle",
    ),
    "parallel_structure": _intermediate_trainer(
        "parallel_structure",
        "Parallel Structure",
        "Mengenali item grammar yang bentuknya sejajar.",
        "identify, document, dan validate adalah verb sejajar dalam satu daftar aksi.",
        "Dalam daftar aksi, pastikan bentuk verb-nya konsisten.",
        "User sering mencampur verb, gerund, dan noun dalam satu daftar.",
        "Parallel structure penting untuk requirement list dan BA recommendation.",
        "The analyst must identify issues, document requirements, and validate solutions.",
        "Analis harus mengidentifikasi masalah, mendokumentasikan requirement, dan memvalidasi solusi.",
        "Modal verb + parallel verbs",
        {
            "main_subject": "The analyst",
            "main_verb": "must identify / document / validate",
            "parallel_items": "identify issues; document requirements; validate solutions",
        },
        "identify issues, document requirements, and validate solutions",
        "choose_correct_parallel_structure",
        "Mana struktur paralel yang benar?",
        ["identify issues, document requirements, and validate solutions", "identify issues, documenting requirements, and validate solutions", "identification issues, document requirements, and validating solutions"],
        "mixed_parallel_forms",
        "Why is the first option parallel?",
        ["Because all actions use base verb form", "Because all words are nouns", "Because it has no object", "Because it uses passive voice"],
        "Because all actions use base verb form",
    ),
    "connector_logic": _intermediate_trainer(
        "connector_logic",
        "Connector Logic",
        "Memahami hubungan ide seperti sebab, akibat, kontras, dan waktu.",
        "\"Although\" menunjukkan kontras: proses lambat, tetapi automation belum tentu solusi terbaik.",
        "Jangan hanya terjemahkan connector; pahami hubungan logikanya.",
        "User sering melewatkan contrast connector seperti although/however.",
        "Connector logic dipakai saat menulis reasoning dalam recommendation dan impact analysis.",
        "Although the process is slow, automation is not always the best solution.",
        "Walaupun prosesnya lambat, automation belum tentu solusi terbaik.",
        "Contrast connector + main clause",
        {
            "connector": "Although",
            "dependent_clause": "the process is slow",
            "main_clause": "automation is not always the best solution",
        },
        "Although",
        "choose_correct_connector",
        "Connector apa yang menunjukkan kontras?",
        ["Although", "Because", "Therefore", "And"],
        "connector_meaning_confusion",
        "What relation does 'Although' show?",
        ["Contrast", "Cause", "Result", "Addition"],
        "Contrast",
    ),
}


def get_basic_trainer_topics() -> list[dict[str, Any]]:
    topics = []
    for trainer in BASIC_TRAINERS.values():
        topic = get_grammar_topic(trainer["topic_id"]) or {}
        topics.append(
            {
                "topic_id": trainer["topic_id"],
                "title": trainer["title"],
                "level": trainer["level"],
                "learning_objective": trainer["learning_objective"],
                "estimated_minutes": topic.get("estimated_minutes", 10),
            }
        )
    return topics


def get_basic_grammar_trainer(topic_id: str) -> dict[str, Any] | None:
    trainer = BASIC_TRAINERS.get(topic_id)
    return deepcopy(trainer) if trainer else None


def submit_basic_grammar_trainer(payload: dict) -> dict[str, Any]:
    topic_id = payload.get("topic_id") or "subject_verb"
    result = score_trainer_answers(topic_id, payload.get("answers") or {})
    recommendation = get_basic_trainer_recommendation(topic_id, result["score"])
    mistakes = [
        {
            "question_id": detail["question_id"],
            "user_answer": detail["user_answer"],
            "correct_answer": detail["correct_answer"],
        }
        for detail in result["details"]
        if not detail["is_correct"]
    ]
    attempt_update = save_grammar_attempt(
        {
            "user_id": payload.get("user_id") or "default-user",
            "topic_id": topic_id,
            "activity_type": "basic_grammar_trainer",
            "score": result["score"],
            "max_score": result["max_score"],
            "mistakes": mistakes,
            "feedback": recommendation["mentor_message"],
        }
    )
    return {
        "result": result,
        "recommendation": recommendation,
        "grammar_journey": attempt_update["grammar_journey"],
    }


def get_intermediate_trainer_topics() -> list[dict[str, Any]]:
    topics = []
    for trainer in INTERMEDIATE_TRAINERS.values():
        topic = get_grammar_topic(trainer["topic_id"]) or {}
        topics.append(
            {
                "topic_id": trainer["topic_id"],
                "title": trainer["title"],
                "level": trainer["level"],
                "learning_objective": trainer["learning_objective"],
                "estimated_minutes": topic.get("estimated_minutes", 12),
            }
        )
    return topics


def get_intermediate_grammar_trainer(topic_id: str) -> dict[str, Any] | None:
    trainer = INTERMEDIATE_TRAINERS.get(topic_id)
    return deepcopy(trainer) if trainer else None


def submit_intermediate_grammar_trainer(payload: dict) -> dict[str, Any]:
    topic_id = payload.get("topic_id") or "gerund_vs_main_verb"
    result = score_intermediate_trainer_answers(topic_id, payload.get("answers") or {})
    recommendation = get_intermediate_trainer_recommendation(topic_id, result["score"], result["mistakes"])
    attempt_update = save_grammar_attempt(
        {
            "user_id": payload.get("user_id") or "default-user",
            "topic_id": topic_id,
            "activity_type": "intermediate_grammar_trainer",
            "score": result["score"],
            "max_score": result["max_score"],
            "mistakes": result["mistakes"],
            "feedback": recommendation["mentor_message"],
        }
    )
    return {
        "result": result,
        "recommendation": recommendation,
        "grammar_journey": attempt_update["grammar_journey"],
    }


def score_intermediate_trainer_answers(topic_id: str, answers: dict) -> dict[str, Any]:
    trainer = get_intermediate_grammar_trainer(topic_id)
    if not trainer:
        return {
            "topic_id": topic_id,
            "level": "intermediate",
            "score": 0,
            "max_score": 100,
            "correct_count": 0,
            "total_questions": 0,
            "is_passed": False,
            "details": [],
            "mistakes": [],
        }
    scored_items = list(trainer.get("quiz_items", [])) + list(trainer.get("trap_items", []))
    details = []
    for item in scored_items:
        user_answer = answers.get(item["id"], "")
        is_correct = _normalize_answer(user_answer) == _normalize_answer(item["correct_answer"])
        details.append(
            {
                "question_id": item["id"],
                "is_correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": item["correct_answer"],
                "explanation_id": item["explanation_id"],
            }
        )
    total = len(details)
    correct = len([item for item in details if item["is_correct"]])
    score = round((correct / total) * 100, 1) if total else 0
    mistakes = [
        {
            "question_id": item["question_id"],
            "user_answer": item["user_answer"],
            "correct_answer": item["correct_answer"],
            "explanation_id": item["explanation_id"],
        }
        for item in details
        if not item["is_correct"]
    ]
    return {
        "topic_id": topic_id,
        "level": "intermediate",
        "score": score,
        "max_score": 100,
        "correct_count": correct,
        "total_questions": total,
        "is_passed": score >= 70,
        "details": details,
        "mistakes": mistakes,
    }


def get_intermediate_trainer_recommendation(topic_id: str, score: float, mistakes: list) -> dict[str, Any]:
    next_topic = get_next_topic(topic_id) or {}
    if score >= 70:
        return {
            "next_action": f"Lanjut ke topic berikutnya: {next_topic.get('title', 'Intermediate Grammar berikutnya')}.",
            "next_topic_id": next_topic.get("id"),
            "mentor_message": "Bagus. Kamu mulai bisa membaca struktur kalimat yang lebih panjang.",
            "review_topic_id": topic_id,
        }
    review_topic_id = topic_id
    if mistakes:
        first = mistakes[0]["question_id"]
        if "trap" in first:
            review_topic_id = topic_id
    return {
        "next_action": "Ulangi contoh, guided practice, dan trap item sebelum lanjut topic berikutnya.",
        "next_topic_id": topic_id,
        "mentor_message": "Topic intermediate memang lebih menantang. Fokus dulu pada main verb dan bagian yang hanya menjelaskan noun.",
        "review_topic_id": review_topic_id,
    }


def score_trainer_answers(topic_id: str, answers: dict) -> dict[str, Any]:
    trainer = get_basic_grammar_trainer(topic_id)
    if not trainer:
        return {
            "topic_id": topic_id,
            "score": 0,
            "max_score": 100,
            "correct_count": 0,
            "total_questions": 0,
            "is_passed": False,
            "details": [],
        }
    details = []
    for item in trainer["quiz_items"]:
        user_answer = answers.get(item["id"], "")
        is_correct = _normalize_answer(user_answer) == _normalize_answer(item["correct_answer"])
        details.append(
            {
                "question_id": item["id"],
                "is_correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": item["correct_answer"],
                "explanation_id": item["explanation_id"],
            }
        )
    total = len(details)
    correct = len([item for item in details if item["is_correct"]])
    score = round((correct / total) * 100, 1) if total else 0
    return {
        "topic_id": topic_id,
        "score": score,
        "max_score": 100,
        "correct_count": correct,
        "total_questions": total,
        "is_passed": score >= 70,
        "details": details,
    }


def get_basic_trainer_recommendation(topic_id: str, score: float) -> dict[str, Any]:
    next_topic = get_next_topic(topic_id) or {}
    if score >= 70:
        return {
            "next_action": f"Lanjut ke topic berikutnya: {next_topic.get('title', 'Grammar Basic berikutnya')}.",
            "next_topic_id": next_topic.get("id"),
            "mentor_message": "Bagus. Kamu sudah memahami dasar topic ini. Lanjutkan pelan-pelan ke topic berikutnya.",
        }
    return {
        "next_action": "Ulangi contoh dan guided practice sebelum mencoba quiz lagi.",
        "next_topic_id": topic_id,
        "mentor_message": "Belum apa-apa. Fokus ke struktur utama dulu: subject, verb, lalu informasi tambahan.",
    }


def _normalize_answer(value: Any) -> str:
    return str(value or "").strip().lower()
