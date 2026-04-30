from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

from backend.services.grammar_journey_service import save_grammar_attempt


def _example(
    sentence: str,
    simpler: str,
    meaning: str,
    pattern: str,
    focus: str,
    breakdown: dict[str, str],
    usage: str,
    ba_note: str,
) -> dict[str, Any]:
    return {
        "sentence": sentence,
        "simpler_version": simpler,
        "simple_meaning_id": meaning,
        "advanced_pattern": pattern,
        "grammar_focus": focus,
        "breakdown": breakdown,
        "professional_usage_note": usage,
        "ba_context_note": ba_note,
    }


def _practice(
    item_id: str,
    topic_id: str,
    question_type: str,
    sentence: str,
    question: str,
    options: list[str],
    correct: str,
    explanation: str,
    pattern: str,
    simpler: str,
    related_topic_id: str,
) -> dict[str, Any]:
    return {
        "id": item_id,
        "topic_id": topic_id,
        "question_type": question_type,
        "instruction_id": "Pilih jawaban yang paling tepat.",
        "sentence": sentence,
        "question": question,
        "options": options,
        "correct_answer": correct,
        "explanation_id": explanation,
        "difficulty": "advanced",
        "advanced_pattern": pattern,
        "simpler_version": simpler,
        "related_topic_id": related_topic_id,
        "ba_context_note": "Dipakai untuk membaca atau menulis dokumen Business Analyst yang formal.",
    }


def _rewrite(
    item_id: str,
    topic_id: str,
    original: str,
    expected: str,
    explanation: str,
    rule: str,
    keywords: list[str],
    acceptable: list[str] | None = None,
    simpler: str | None = None,
) -> dict[str, Any]:
    return {
        "id": item_id,
        "topic_id": topic_id,
        "instruction_id": "Rewrite this sentence into a more formal Business Analyst sentence.",
        "original_sentence": original,
        "expected_answer": expected,
        "acceptable_answers": acceptable or [],
        "required_keywords": keywords,
        "explanation_id": explanation,
        "professional_usage_note": "Suitable for SRS, business requirement documents, system proposals, or formal analysis reports.",
        "simpler_version": simpler or original,
        "grammar_rule_id": rule,
        "difficulty": "advanced",
    }


ADVANCED_TOPICS: dict[str, dict[str, Any]] = {
    "complex_sentence_mapping": {
        "topic_id": "complex_sentence_mapping",
        "level": "advanced",
        "title": "Complex Sentence Mapping",
        "learning_objective": "Memetakan main clause, subordinate clause, modifier, dan connector dalam kalimat panjang.",
        "explanation_id": "Kalimat kompleks perlu dipecah menjadi subject utama, verb utama, clause pendukung, dan informasi tambahan.",
        "professional_usage": "Useful for TOEFL reading, academic analysis, and formal requirement review.",
        "ba_context": "BA sering membaca kalimat panjang dalam proposal, policy, dan requirement documentation.",
        "common_trap": "Pemula sering menerjemahkan dari awal sampai akhir tanpa menemukan main clause.",
        "beginner_bridge": "Bayangkan kalimat panjang seperti peta. Cari jalan utama dulu: subject dan verb utama. Setelah itu baru lihat cabang seperti clause dan phrase.",
        "estimated_minutes": 15,
        "examples": [
            _example(
                "Although the proposed system improves efficiency, it may require additional training before users can adopt it effectively.",
                "The system improves efficiency, but users need training.",
                "Walaupun sistem meningkatkan efisiensi, sistem mungkin membutuhkan training tambahan agar user bisa menggunakannya efektif.",
                "Contrast connector + main clause + purpose clause",
                "complex_sentence_mapping",
                {"connector": "Although", "main_clause": "it may require additional training", "purpose_clause": "before users can adopt it effectively"},
                "This structure is common when discussing benefits and constraints.",
                "Cocok untuk menjelaskan trade-off solusi BA.",
            ),
            _example(
                "When stakeholder priorities conflict, the analyst must document assumptions so that the team can validate decisions later.",
                "The analyst documents assumptions when priorities conflict.",
                "Ketika prioritas stakeholder bertentangan, analyst harus mendokumentasikan asumsi agar tim bisa memvalidasi keputusan nanti.",
                "Time clause + main clause + purpose connector",
                "complex_sentence_mapping",
                {"time_clause": "When stakeholder priorities conflict", "main_verb": "must document", "purpose_clause": "so that the team can validate decisions later"},
                "Useful for formal reasoning in reports.",
                "Membantu BA menjelaskan alasan dokumentasi asumsi.",
            ),
        ],
        "practice_items": [
            _practice("complex_sentence_mapping_practice_1", "complex_sentence_mapping", "simplify_advanced_sentence", "Although the system improves efficiency, it may require additional training.", "What is the simpler meaning?", ["The system has benefits but needs training.", "The system does not improve efficiency.", "Training is unrelated to the system.", "Users cannot use any system."], "The system has benefits but needs training.", "Although menunjukkan kontras antara benefit dan constraint.", "contrast connector", "The system improves efficiency, but users need training.", "complex_sentence_mapping"),
            _practice("complex_sentence_mapping_practice_2", "complex_sentence_mapping", "identify_academic_connector", "When requirements change, the analyst should update the traceability matrix.", "Which part gives the condition/time?", ["When requirements change", "the analyst", "traceability matrix", "should update"], "When requirements change", "When memperkenalkan clause kondisi/waktu.", "subordinate clause", "If requirements change, update the matrix.", "complex_sentence_mapping"),
            _practice("complex_sentence_mapping_practice_3", "complex_sentence_mapping", "simplify_advanced_sentence", "The analyst documents assumptions so that stakeholders can validate decisions.", "What does so that show?", ["purpose", "contrast", "unrelated detail", "past action"], "purpose", "so that menjelaskan tujuan.", "purpose connector", "The analyst documents assumptions for validation.", "academic_connectors"),
        ],
        "rewrite_items": [
            _rewrite("complex_sentence_mapping_rewrite_1", "complex_sentence_mapping", "The workflow is useful. It is too complex. Users need training.", "Although the workflow is useful, it is too complex and may require user training.", "Although menggabungkan benefit dan constraint secara formal.", "Although + contrast + additional result", ["although", "workflow", "useful", "complex", "training"]),
        ],
    },
    "nominalization": {
        "topic_id": "nominalization",
        "level": "advanced",
        "title": "Nominalization",
        "learning_objective": "Mengubah verb/adjective menjadi noun agar kalimat formal lebih akademik.",
        "explanation_id": "Nominalization mengubah action menjadi konsep, misalnya implement menjadi implementation.",
        "professional_usage": "Common in formal reports, proposals, SRS, and academic TOEFL passages.",
        "ba_context": "BA memakai nominalization untuk menulis analysis, validation, implementation, dan prioritization.",
        "common_trap": "Terlalu banyak nominalization bisa membuat kalimat berat; gunakan saat butuh gaya formal.",
        "beginner_bridge": "Nominalization artinya mengubah verb menjadi noun. Contoh: implement menjadi implementation. Dalam tulisan formal, ini membuat kalimat terdengar lebih akademik dan profesional.",
        "estimated_minutes": 15,
        "examples": [
            _example("The implementation of an integrated requirement management system is expected to improve traceability.", "The team implements a requirement management system to improve traceability.", "Implementasi sistem manajemen requirement terpadu diharapkan meningkatkan keterlacakan.", "Nominalization + passive reporting structure", "nominalization", {"nominalized_subject": "The implementation of an integrated requirement management system", "main_verb": "is expected to improve", "object": "traceability"}, "Common in formal reports and system documentation.", "Cocok untuk proposal, SRS, atau dokumen strategi sistem informasi."),
            _example("The analysis of stakeholder needs may indicate several conflicting priorities.", "The analyst analyzes stakeholder needs and may find conflicting priorities.", "Analisis kebutuhan stakeholder mungkin menunjukkan beberapa prioritas yang bertentangan.", "Nominalized noun phrase + hedging modal", "nominalization", {"nominalized_subject": "The analysis of stakeholder needs", "main_verb": "may indicate", "object": "conflicting priorities"}, "Useful for cautious professional claims.", "Dipakai saat BA belum ingin menyatakan kepastian penuh."),
            _example("The validation of requirements reduces ambiguity before development begins.", "Validating requirements reduces ambiguity.", "Validasi requirement mengurangi ambiguitas sebelum development dimulai.", "Nominalization as subject", "nominalization", {"nominalized_subject": "The validation of requirements", "main_verb": "reduces", "object": "ambiguity"}, "Makes a process sound like a formal concept.", "Cocok untuk menjelaskan value dari validasi requirement."),
        ],
        "practice_items": [
            _practice("nominalization_practice_1", "nominalization", "identify_nominalization", "The implementation of the system is expected to improve traceability.", "Which word is a nominalization?", ["implementation", "system", "expected", "traceability"], "implementation", "Implementation berasal dari verb implement.", "nominalization", "The team implements the system.", "nominalization"),
            _practice("nominalization_practice_2", "nominalization", "identify_nominalization", "The analysis of stakeholder needs may indicate conflicting priorities.", "Which phrase is nominalized?", ["The analysis of stakeholder needs", "may indicate", "conflicting priorities", "stakeholder needs"], "The analysis of stakeholder needs", "Analysis adalah noun dari analyze.", "nominalized noun phrase", "The analyst analyzes stakeholder needs.", "nominalization"),
            _practice("nominalization_practice_3", "nominalization", "simplify_advanced_sentence", "The validation of requirements reduces ambiguity.", "Which simpler version matches?", ["Validating requirements reduces ambiguity.", "Requirements create ambiguity.", "Validation is not needed.", "Ambiguity validates requirements."], "Validating requirements reduces ambiguity.", "Validation of requirements berarti validating requirements.", "nominalization simplification", "Validating requirements reduces ambiguity.", "nominalization"),
            _practice("nominalization_practice_4", "nominalization", "choose_formal_sentence", "Choose the more formal sentence.", "Which sentence is more formal?", ["The implementation improves traceability.", "The team does stuff better.", "Users make reports fast.", "People check things."], "The implementation improves traceability.", "Implementation dan traceability adalah istilah formal.", "formal nominalization", "Implementing the system improves traceability.", "formal_ba_writing"),
        ],
        "rewrite_items": [
            _rewrite("nominalization_rewrite_1", "nominalization", "The team implements the system to improve traceability.", "The implementation of the system improves traceability.", "Implementation membuat action menjadi noun formal.", "nominalized subject + verb + object", ["implementation", "system", "improves", "traceability"]),
            _rewrite("nominalization_rewrite_2", "nominalization", "The analyst validates requirements to reduce ambiguity.", "The validation of requirements reduces ambiguity.", "Validation of requirements membuat kalimat lebih formal.", "nominalization + concise result", ["validation", "requirements", "reduces", "ambiguity"]),
        ],
    },
    "hedging_language": {
        "topic_id": "hedging_language",
        "level": "advanced",
        "title": "Hedging Language",
        "learning_objective": "Menyampaikan klaim secara hati-hati memakai may, might, could, likely, dan appear to.",
        "explanation_id": "Hedging membuat tulisan profesional tidak terlalu mutlak ketika evidence belum penuh.",
        "professional_usage": "Used in academic writing, risk analysis, and stakeholder recommendation.",
        "ba_context": "BA memakai hedging saat membuat asumsi atau rekomendasi awal.",
        "common_trap": "Pemula sering terlalu absolut: always, must, definitely, padahal evidence belum cukup.",
        "beginner_bridge": "Hedging artinya membuat kalimat lebih hati-hati. Misalnya 'will cause' menjadi 'may cause'. Ini berguna saat BA belum punya bukti lengkap.",
        "estimated_minutes": 14,
        "examples": [
            _example("The analysis of stakeholder needs may indicate several conflicting priorities.", "The analysis may show conflicting priorities.", "Analisis kebutuhan stakeholder mungkin menunjukkan prioritas yang bertentangan.", "Hedging modal may", "hedging_language", {"hedging": "may indicate", "claim": "conflicting priorities"}, "Prevents overclaiming.", "Cocok untuk early discovery."),
            _example("The delay could suggest a bottleneck in the approval workflow.", "The delay may show a bottleneck.", "Keterlambatan bisa menunjukkan bottleneck dalam approval workflow.", "Hedging modal could", "hedging_language", {"hedging": "could suggest", "issue": "bottleneck"}, "Useful for cautious diagnosis.", "BA belum langsung menyimpulkan akar masalah."),
        ],
        "practice_items": [
            _practice("hedging_language_practice_1", "hedging_language", "identify_hedging", "The analysis may indicate conflicting priorities.", "Which word shows hedging?", ["may", "analysis", "priorities", "indicate"], "may", "May membuat klaim lebih hati-hati.", "hedging modal", "The analysis might show conflicting priorities.", "hedging_language"),
            _practice("hedging_language_practice_2", "hedging_language", "choose_formal_sentence", "Choose the cautious sentence.", "Which sentence is better when evidence is incomplete?", ["The delay may indicate a bottleneck.", "The delay definitely proves failure.", "The workflow is always wrong.", "Users never understand the system."], "The delay may indicate a bottleneck.", "May indicate tidak terlalu absolut.", "cautious claim", "The delay might show a bottleneck.", "hedging_language"),
            _practice("hedging_language_practice_3", "hedging_language", "identify_hedging", "The proposed solution is likely to reduce manual work.", "Which phrase is hedging?", ["is likely to", "manual work", "reduce", "solution"], "is likely to", "Likely to menunjukkan kemungkinan, bukan kepastian mutlak.", "likelihood phrase", "The solution may reduce work.", "hedging_language"),
        ],
        "rewrite_items": [
            _rewrite("hedging_language_rewrite_1", "hedging_language", "The workflow causes every delay.", "The workflow may contribute to delays.", "May contribute lebih hati-hati dan profesional.", "hedging modal + precise verb", ["workflow", "may", "contribute", "delays"]),
            _rewrite("hedging_language_rewrite_2", "hedging_language", "The solution will fix all issues.", "The solution may address several key issues.", "May address several key issues lebih realistis.", "hedging modal + limited claim", ["solution", "may", "address", "issues"]),
        ],
    },
    "inversion": {
        "topic_id": "inversion",
        "level": "advanced",
        "title": "Inversion",
        "learning_objective": "Mengenali pola inversion seperti Only after ... can ... dalam kalimat formal.",
        "explanation_id": "Inversion menukar urutan subject dan auxiliary setelah ekspresi tertentu untuk penekanan.",
        "professional_usage": "Appears in formal TOEFL passages and polished professional writing.",
        "ba_context": "Bisa dipakai untuk menekankan prasyarat sebelum development.",
        "common_trap": "Pemula sering membaca 'can the team' sebagai pertanyaan, padahal ini statement inversion.",
        "beginner_bridge": "Inversion terlihat seperti pertanyaan karena auxiliary muncul sebelum subject. Namun kalimatnya bisa berupa statement formal, bukan pertanyaan.",
        "estimated_minutes": 15,
        "examples": [
            _example("Only after the requirements are validated can the team proceed to development.", "The team can proceed only after requirements are validated.", "Hanya setelah requirement divalidasi, tim dapat lanjut ke development.", "Only after + clause + auxiliary + subject + verb", "inversion", {"fronted_phrase": "Only after the requirements are validated", "auxiliary": "can", "subject": "the team", "main_verb": "proceed"}, "Adds emphasis to conditions.", "Menekankan gate sebelum development."),
            _example("Rarely does a single stakeholder represent all user needs.", "A single stakeholder rarely represents all user needs.", "Jarang sekali satu stakeholder mewakili semua kebutuhan user.", "Negative adverb + auxiliary inversion", "inversion", {"negative_adverb": "Rarely", "auxiliary": "does", "subject": "a single stakeholder", "main_verb": "represent"}, "Used for formal emphasis.", "Mengingatkan BA agar tidak hanya mengandalkan satu stakeholder."),
        ],
        "practice_items": [
            _practice("inversion_practice_1", "inversion", "identify_inversion_pattern", "Only after the requirements are validated can the team proceed.", "Which word is the auxiliary in the inversion?", ["can", "after", "requirements", "validated"], "can", "Can muncul sebelum subject the team karena inversion.", "Only after inversion", "The team can proceed only after validation.", "inversion"),
            _practice("inversion_practice_2", "inversion", "simplify_advanced_sentence", "Rarely does a single stakeholder represent all user needs.", "Which simpler version matches?", ["A single stakeholder rarely represents all user needs.", "A stakeholder always represents everyone.", "Stakeholders never have needs.", "One user validates all requirements."], "A single stakeholder rarely represents all user needs.", "Rarely does sama dengan does rarely dalam kalimat biasa.", "negative adverb inversion", "A single stakeholder rarely represents all needs.", "inversion"),
            _practice("inversion_practice_3", "inversion", "identify_inversion_pattern", "Only when the scope is clear should development begin.", "What condition must happen first?", ["the scope is clear", "development begins immediately", "the scope is ignored", "users stop testing"], "the scope is clear", "Only when menekankan prasyarat.", "Only when inversion", "Development should begin only when scope is clear.", "inversion"),
        ],
        "rewrite_items": [
            _rewrite("inversion_rewrite_1", "inversion", "The team can proceed only after the requirements are validated.", "Only after the requirements are validated can the team proceed.", "Only after di depan memicu inversion can the team.", "Only after + clause + auxiliary + subject + verb", ["only", "after", "requirements", "validated", "can", "team", "proceed"]),
        ],
    },
    "conditional_sentence": {
        "topic_id": "conditional_sentence",
        "level": "advanced",
        "title": "Conditional Sentence",
        "learning_objective": "Memahami if-condition untuk risiko, dampak, dan rekomendasi.",
        "explanation_id": "Conditional sentence menghubungkan kondisi dan akibat.",
        "professional_usage": "Useful in risk analysis, requirement impact, and recommendation writing.",
        "ba_context": "BA memakai conditional untuk menjelaskan apa yang terjadi jika proses tidak diperbaiki.",
        "common_trap": "Pemula sering mencampur will di if-clause untuk conditional type 1.",
        "beginner_bridge": "Conditional berarti kalimat 'jika... maka...'. Dalam BA, ini dipakai untuk menjelaskan risiko dan dampak.",
        "estimated_minutes": 14,
        "examples": [
            _example("If the approval workflow is not simplified, users may continue to experience delays.", "Users may still face delays if the workflow is not simplified.", "Jika approval workflow tidak disederhanakan, user mungkin terus mengalami keterlambatan.", "If + present, may + base verb", "conditional_sentence", {"condition": "If the approval workflow is not simplified", "result": "users may continue to experience delays"}, "Useful for risk statements.", "Menjelaskan dampak jika rekomendasi tidak dilakukan."),
            _example("If requirements are unclear, the team should not begin development.", "The team should wait when requirements are unclear.", "Jika requirement tidak jelas, tim sebaiknya tidak mulai development.", "If + present, should + base verb", "conditional_sentence", {"condition": "If requirements are unclear", "recommendation": "should not begin development"}, "Useful for governance rules.", "Menjelaskan quality gate."),
        ],
        "practice_items": [
            _practice("conditional_sentence_practice_1", "conditional_sentence", "identify_conditional_logic", "If the approval workflow is not simplified, users may continue to experience delays.", "Which part is the condition?", ["If the approval workflow is not simplified", "users may continue", "experience delays", "approval workflow"], "If the approval workflow is not simplified", "If-clause adalah kondisi.", "conditional logic", "If workflow is not simplified, delays may continue.", "conditional_sentence"),
            _practice("conditional_sentence_practice_2", "conditional_sentence", "identify_conditional_logic", "If requirements are unclear, the team should not begin development.", "What is the recommendation?", ["the team should not begin development", "requirements are unclear", "the team should code faster", "requirements are final"], "the team should not begin development", "Main clause berisi rekomendasi.", "if + recommendation", "Do not begin development when requirements are unclear.", "conditional_sentence"),
            _practice("conditional_sentence_practice_3", "conditional_sentence", "choose_formal_sentence", "Choose the correct conditional sentence.", "Which sentence is correct?", ["If the process remains manual, errors may continue.", "If the process will remains manual, errors may continue.", "If the process remain manual, errors continues.", "If manual process, errors."], "If the process remains manual, errors may continue.", "If-clause memakai present simple: remains.", "first conditional", "If process stays manual, errors may continue.", "conditional_sentence"),
        ],
        "rewrite_items": [
            _rewrite("conditional_sentence_rewrite_1", "conditional_sentence", "The workflow is not simplified. Users may still experience delays.", "If the workflow is not simplified, users may continue to experience delays.", "If menghubungkan kondisi dan dampak.", "If + present, may + base verb", ["if", "workflow", "not", "simplified", "users", "delays"]),
            _rewrite("conditional_sentence_rewrite_2", "conditional_sentence", "Requirements are unclear. Development should not begin.", "If requirements are unclear, development should not begin.", "If clause membuat rule lebih eksplisit.", "If + present, should + base verb", ["if", "requirements", "unclear", "development", "should", "not", "begin"]),
        ],
    },
    "academic_connectors": {
        "topic_id": "academic_connectors",
        "level": "advanced",
        "title": "Academic Connectors",
        "learning_objective": "Memakai connector formal untuk contrast, cause, result, dan addition.",
        "explanation_id": "Connector akademik membantu pembaca memahami hubungan antar ide.",
        "professional_usage": "Common in TOEFL writing, reports, and analysis documents.",
        "ba_context": "BA memakai connectors untuk reasoning: however, therefore, consequently, although.",
        "common_trap": "Pemula sering memakai connector yang artinya tidak sesuai hubungan ide.",
        "beginner_bridge": "Connector adalah kata penghubung logika. Cari dulu hubungan idenya: sebab, akibat, kontras, atau tambahan.",
        "estimated_minutes": 15,
        "examples": [
            _example("Although the system improves efficiency, it may require additional training.", "The system is efficient, but users may need training.", "Walaupun sistem meningkatkan efisiensi, sistem mungkin membutuhkan training tambahan.", "Although for contrast", "academic_connectors", {"connector": "Although", "contrast": "efficiency vs training"}, "Useful for balanced argument.", "Menjelaskan benefit dan cost."),
            _example("Consequently, the organization can reduce ambiguity in requirement documentation.", "As a result, ambiguity can be reduced.", "Akibatnya, organisasi dapat mengurangi ambiguitas dalam dokumentasi requirement.", "Consequently for result", "academic_connectors", {"connector": "Consequently", "result": "reduce ambiguity"}, "Formal result connector.", "Dipakai untuk menjelaskan dampak solusi."),
            _example("However, the proposed solution may require additional stakeholder training.", "But the solution may need training.", "Namun, solusi yang diusulkan mungkin membutuhkan training stakeholder tambahan.", "However for contrast", "academic_connectors", {"connector": "However", "contrast": "limitation"}, "Formal contrast connector.", "Dipakai untuk menyampaikan limitation."),
        ],
        "practice_items": [
            _practice("academic_connectors_practice_1", "academic_connectors", "identify_academic_connector", "Consequently, the organization can reduce ambiguity.", "What relation does consequently show?", ["result", "contrast", "example", "condition"], "result", "Consequently menunjukkan akibat.", "result connector", "As a result, ambiguity is reduced.", "academic_connectors"),
            _practice("academic_connectors_practice_2", "academic_connectors", "identify_academic_connector", "Although the system improves efficiency, it may require training.", "What relation does although show?", ["contrast", "result", "addition", "sequence"], "contrast", "Although menunjukkan kontras.", "contrast connector", "The system helps, but it needs training.", "academic_connectors"),
            _practice("academic_connectors_practice_3", "academic_connectors", "choose_formal_sentence", "Choose the sentence with correct connector logic.", "Which sentence is logical?", ["The data is inconsistent; therefore, the report cannot be finalized.", "The data is inconsistent; however, the report cannot be finalized.", "The data is inconsistent; although the report cannot be finalized.", "The data is inconsistent; meanwhile, requirements."], "The data is inconsistent; therefore, the report cannot be finalized.", "Inconsistent data causes the report problem, so therefore fits.", "cause-result connector", "Data problem causes report delay.", "academic_connectors"),
            _practice("academic_connectors_practice_4", "academic_connectors", "identify_academic_connector", "However, the solution may require additional training.", "What is however used for?", ["contrast", "cause", "purpose", "time"], "contrast", "However memperkenalkan limitation atau ide kontras.", "contrast connector", "But the solution may need training.", "academic_connectors"),
        ],
        "rewrite_items": [
            _rewrite("academic_connectors_rewrite_1", "academic_connectors", "The data is inconsistent. The report cannot be finalized.", "The data is inconsistent; therefore, the report cannot be finalized.", "Therefore menunjukkan sebab-akibat.", "Cause; therefore, result", ["data", "inconsistent", "therefore", "report", "cannot", "finalized"]),
            _rewrite("academic_connectors_rewrite_2", "academic_connectors", "The system improves efficiency. It requires training.", "Although the system improves efficiency, it requires training.", "Although menyatukan benefit dan limitation.", "Although + contrast", ["although", "system", "improves", "efficiency", "requires", "training"]),
        ],
    },
    "formal_ba_writing": {
        "topic_id": "formal_ba_writing",
        "level": "advanced",
        "title": "Formal BA Writing",
        "learning_objective": "Menulis kalimat Business Analyst yang formal, jelas, dan profesional.",
        "explanation_id": "Formal BA writing memakai verb profesional, noun phrase jelas, dan klaim yang tidak terlalu informal.",
        "professional_usage": "Suitable for SRS, BRD, user stories, system proposals, and stakeholder reports.",
        "ba_context": "Ini inti grammar profesional untuk pekerjaan BA.",
        "common_trap": "Kalimat terlalu informal seperti make reports faster atau people wait too long.",
        "beginner_bridge": "Formal BA writing berarti mengganti bahasa sehari-hari menjadi bahasa kerja yang jelas. Contoh: make reports faster menjadi generate reports more efficiently.",
        "estimated_minutes": 18,
        "examples": [
            _example("The proposed solution enables stakeholders to monitor progress more effectively.", "The solution helps stakeholders monitor progress better.", "Solusi yang diusulkan memungkinkan stakeholder memantau progres lebih efektif.", "formal verb phrase", "formal_ba_writing", {"subject": "The proposed solution", "main_verb": "enables", "object": "stakeholders", "complement": "to monitor progress more effectively"}, "Professional benefit statement.", "Cocok untuk proposal solusi."),
            _example("Consequently, the organization can reduce ambiguity in requirement documentation.", "The organization can make requirement documents clearer.", "Akibatnya, organisasi dapat mengurangi ambiguitas dalam dokumentasi requirement.", "academic connector + formal noun phrase", "formal_ba_writing", {"connector": "Consequently", "main_verb": "can reduce", "object": "ambiguity"}, "Formal impact statement.", "Cocok untuk final report."),
            _example("The feature should be intuitive for end users.", "The feature should be easy to use.", "Fitur tersebut sebaiknya intuitif bagi end user.", "modal + be + professional adjective", "formal_ba_writing", {"subject": "The feature", "main_verb": "should be", "complement": "intuitive for end users"}, "Formal usability requirement.", "Cocok untuk non-functional requirement."),
        ],
        "practice_items": [
            _practice("formal_ba_writing_practice_1", "formal_ba_writing", "choose_formal_sentence", "Choose the most formal BA sentence.", "Which sentence is best?", ["The system enables users to generate reports more efficiently.", "The system makes reports fast.", "People can do reports quick.", "Reports are kinda easy now."], "The system enables users to generate reports more efficiently.", "Enables users to generate reports more efficiently terdengar profesional.", "formal BA benefit statement", "The system helps users make reports faster.", "formal_ba_writing"),
            _practice("formal_ba_writing_practice_2", "formal_ba_writing", "choose_professional_rewrite", "Choose a professional rewrite.", "Which option is more professional?", ["Stakeholders experience delays in the approval workflow.", "People wait too long.", "The thing is slow.", "Approvals are bad."], "Stakeholders experience delays in the approval workflow.", "Stakeholders dan approval workflow lebih spesifik.", "problem statement", "People wait too long for approvals.", "formal_ba_writing"),
            _practice("formal_ba_writing_practice_3", "formal_ba_writing", "choose_formal_sentence", "Choose the clearer requirement.", "Which requirement is clearer?", ["The feature should be intuitive for end users.", "The feature should be nice.", "Users should like it.", "Make it good."], "The feature should be intuitive for end users.", "Intuitive for end users lebih jelas dan profesional.", "quality requirement", "The feature should be easy to use.", "formal_ba_writing"),
            _practice("formal_ba_writing_practice_4", "formal_ba_writing", "choose_professional_rewrite", "Choose the formal impact sentence.", "Which sentence is best?", ["The solution may reduce manual effort and improve traceability.", "The solution makes stuff easier.", "It fixes many things.", "People work less maybe."], "The solution may reduce manual effort and improve traceability.", "Manual effort dan traceability adalah istilah BA yang spesifik.", "formal impact statement", "The solution helps work become easier.", "formal_ba_writing"),
        ],
        "rewrite_items": [
            _rewrite("formal_ba_rewrite_1", "formal_ba_writing", "The system helps users make reports faster.", "The system enables users to generate reports more efficiently.", "Kata generate reports more efficiently terdengar lebih formal daripada make reports faster.", "formal verb phrase + adverb of manner", ["system", "users", "generate", "reports", "efficiently"], ["The system helps users generate reports more efficiently.", "The system allows users to generate reports more efficiently."]),
            _rewrite("formal_ba_rewrite_2", "formal_ba_writing", "People wait too long for approvals.", "Stakeholders experience delays in the approval workflow.", "Stakeholders dan approval workflow membuat kalimat lebih spesifik.", "professional noun phrase + process term", ["stakeholders", "delays", "approval", "workflow"]),
            _rewrite("formal_ba_rewrite_3", "formal_ba_writing", "The data is messy.", "The data is inconsistent and requires validation.", "Inconsistent and requires validation lebih actionable.", "precise adjective + action requirement", ["data", "inconsistent", "requires", "validation"]),
            _rewrite("formal_ba_rewrite_4", "formal_ba_writing", "The feature should be easy to use.", "The feature should be intuitive for end users.", "Intuitive for end users adalah wording formal untuk usability.", "modal + be + professional adjective", ["feature", "intuitive", "end", "users"]),
        ],
    },
}


def get_advanced_topics() -> list[dict[str, Any]]:
    return [
        {
            "topic_id": topic["topic_id"],
            "level": topic["level"],
            "title": topic["title"],
            "learning_objective": topic["learning_objective"],
            "professional_usage": topic["professional_usage"],
            "estimated_minutes": topic["estimated_minutes"],
        }
        for topic in ADVANCED_TOPICS.values()
    ]


def get_advanced_topic(topic_id: str) -> dict[str, Any] | None:
    topic = ADVANCED_TOPICS.get(topic_id)
    return deepcopy(topic) if topic else None


def get_advanced_practice_items(topic_id: str | None = None) -> list[dict[str, Any]]:
    topics = [ADVANCED_TOPICS[topic_id]] if topic_id and topic_id in ADVANCED_TOPICS else ADVANCED_TOPICS.values()
    return deepcopy([item for topic in topics for item in topic["practice_items"]])


def get_advanced_rewrite_items(topic_id: str | None = None) -> list[dict[str, Any]]:
    topics = [ADVANCED_TOPICS[topic_id]] if topic_id and topic_id in ADVANCED_TOPICS else ADVANCED_TOPICS.values()
    return deepcopy([item for topic in topics for item in topic["rewrite_items"]])


def submit_advanced_practice(payload: dict) -> dict[str, Any]:
    topic_id = payload.get("topic_id")
    result = score_advanced_practice_answers(topic_id, payload.get("answers") or {})
    recommendation = get_advanced_recommendation(result["score"], result["mistakes"], topic_id)
    attempt_update = save_grammar_attempt(
        {
            "user_id": payload.get("user_id") or "default-user",
            "topic_id": recommendation["review_topic_id"],
            "activity_type": "advanced_grammar_practice",
            "score": result["score"],
            "max_score": result["max_score"],
            "mistakes": result["mistakes"],
            "feedback": recommendation["mentor_message"],
            "activity_id": topic_id or "mixed_advanced_practice",
        }
    )
    return {"result": result, "recommendation": recommendation, "grammar_journey": attempt_update["grammar_journey"]}


def submit_advanced_rewrite(payload: dict) -> dict[str, Any]:
    topic_id = payload.get("topic_id")
    result = score_advanced_rewrite_answers(topic_id, payload.get("answers") or {})
    recommendation = get_advanced_recommendation(result["score"], result["mistakes"], topic_id)
    attempt_update = save_grammar_attempt(
        {
            "user_id": payload.get("user_id") or "default-user",
            "topic_id": recommendation["review_topic_id"],
            "activity_type": "advanced_grammar_rewrite",
            "score": result["score"],
            "max_score": result["max_score"],
            "mistakes": result["mistakes"],
            "feedback": recommendation["mentor_message"],
            "activity_id": topic_id or "mixed_advanced_rewrite",
        }
    )
    return {"result": result, "recommendation": recommendation, "grammar_journey": attempt_update["grammar_journey"]}


def normalize_advanced_answer(answer: str) -> str:
    normalized = str(answer or "").strip().lower()
    normalized = re.sub(r"[.?!]+$", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized


def score_advanced_practice_answers(topic_id: str | None, answers: dict) -> dict[str, Any]:
    items = get_advanced_practice_items(topic_id)
    details = []
    for item in items:
        if item["id"] not in answers:
            continue
        user_answer = answers.get(item["id"], "")
        is_correct = normalize_advanced_answer(user_answer) == normalize_advanced_answer(item["correct_answer"])
        details.append(
            {
                "item_id": item["id"],
                "is_correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": item["correct_answer"],
                "explanation_id": item["explanation_id"],
                "advanced_pattern": item["advanced_pattern"],
                "related_topic_id": item["related_topic_id"],
            }
        )
    return _score_details(details, correct_key="is_correct")


def score_advanced_rewrite_answers(topic_id: str | None, answers: dict) -> dict[str, Any]:
    items = get_advanced_rewrite_items(topic_id)
    details = []
    for item in items:
        if item["id"] not in answers:
            continue
        user_answer = str(answers.get(item["id"], ""))
        partial_score, missing = _score_rewrite_answer(user_answer, item)
        details.append(
            {
                "item_id": item["id"],
                "is_correct": partial_score >= 100,
                "partial_score": partial_score,
                "user_answer": user_answer,
                "expected_answer": item["expected_answer"],
                "acceptable_answers": item["acceptable_answers"],
                "required_keywords": item["required_keywords"],
                "missing_keywords": missing,
                "explanation_id": item["explanation_id"],
                "grammar_rule_id": item["grammar_rule_id"],
                "related_topic_id": item["topic_id"],
            }
        )
    return _score_details(details, correct_key="partial_score")


def get_advanced_recommendation(score: float, mistakes: list, topic_id: str | None = None) -> dict[str, Any]:
    review_topic_id = mistakes[0].get("related_topic_id") if mistakes else topic_id or "formal_ba_writing"
    if score >= 85:
        return {
            "next_action": "Lanjutkan ke advanced topic lain atau coba rewrite dengan kalimat sendiri.",
            "review_topic_id": review_topic_id,
            "mentor_message": "Bagus. Kamu mulai memahami grammar formal yang sering muncul di TOEFL dan dokumen BA.",
        }
    if score >= 70:
        return {
            "next_action": "Ulangi item yang belum sempurna dan fokus pada pola advanced yang sama.",
            "review_topic_id": review_topic_id,
            "mentor_message": "Progress sudah baik. Perkuat lagi pilihan connector, nominalization, atau wording formal.",
        }
    return {
        "next_action": "Kembali ke beginner bridge dan simpler version sebelum mencoba rewrite advanced lagi.",
        "review_topic_id": review_topic_id,
        "mentor_message": "Pelan-pelan. Pecah kalimat advanced menjadi versi sederhana dulu, lalu bangun kembali versi formalnya.",
    }


def _score_details(details: list[dict[str, Any]], correct_key: str) -> dict[str, Any]:
    total = len(details)
    if correct_key == "partial_score":
        score = round(sum(item.get("partial_score", 0) for item in details) / total, 1) if total else 0
        correct = len([item for item in details if item.get("partial_score", 0) >= 70])
        mistakes = [item for item in details if item.get("partial_score", 0) < 70]
    else:
        correct = len([item for item in details if item.get("is_correct")])
        score = round((correct / total) * 100, 1) if total else 0
        mistakes = [item for item in details if not item.get("is_correct")]
    return {
        "score": score,
        "max_score": 100,
        "correct_count": correct,
        "total_questions": total,
        "is_passed": score >= 70,
        "details": details,
        "mistakes": mistakes,
    }


def _score_rewrite_answer(user_answer: str, item: dict[str, Any]) -> tuple[float, list[str]]:
    normalized_user = normalize_advanced_answer(user_answer)
    accepted = [item["expected_answer"], *item.get("acceptable_answers", [])]
    if normalized_user in {normalize_advanced_answer(answer) for answer in accepted}:
        return 100, []
    keywords = item.get("required_keywords", [])
    matched = [keyword for keyword in keywords if keyword.lower() in normalized_user]
    missing = [keyword for keyword in keywords if keyword.lower() not in normalized_user]
    score = round((len(matched) / len(keywords)) * 100, 1) if keywords else 0
    return score, missing
