# Grammar Module Specification

Dokumen ini menjelaskan target pengembangan Grammar module untuk TOEFL Analyst AI. Ini adalah dokumen perencanaan, bukan implementasi kode. Semua fitur di bawah perlu dibangun bertahap agar fitur Grammar tetap stabil dan mudah dipahami oleh pemula.

## 1. Vision

Grammar module harus berkembang dari alat sederhana untuk memecah kalimat menjadi sebuah staged Grammar Learning Journey. User tidak hanya melihat subject dan verb, tetapi belajar memahami struktur kalimat Inggris dari dasar sampai pola TOEFL dan Business Analyst writing yang lebih profesional.

Untuk pemula Indonesia, Grammar harus menjawab pertanyaan praktis:

- "Siapa pelakunya?"
- "Apa aksi utamanya?"
- "Bagian mana yang hanya keterangan?"
- "Kenapa kata ini bukan verb utama?"
- "Bagaimana membuat kalimat BA yang jelas dan formal?"

## 2. Goals

- Membantu user memahami struktur kalimat Inggris langkah demi langkah.
- Membantu user mengidentifikasi subject, main verb, object, complement, phrase, dan clause.
- Membantu user menghindari grammar trap yang sering muncul di TOEFL.
- Membantu user memahami grammar dalam soal TOEFL-style.
- Membantu user menulis kalimat Business Analyst yang lebih jelas, formal, dan mudah dipahami.
- Membantu user membangun kebiasaan membaca kalimat panjang dengan cara memetakan struktur, bukan menebak arti kata per kata.

## 3. Target Users

Target utama adalah pembelajar Indonesia level beginner sampai intermediate yang ingin meningkatkan English untuk TOEFL dan konteks Business Analyst.

Karakter user:

- Masih sering bingung membedakan verb utama dan kata kerja bentuk `-ing`.
- Sering membaca kalimat Inggris dari kiri ke kanan tanpa melihat struktur.
- Membutuhkan penjelasan Bahasa Indonesia yang sederhana.
- Ingin memahami kalimat TOEFL, requirement, stakeholder statement, business process, dan report writing.
- Membutuhkan latihan kecil yang bertahap, bukan teori grammar panjang sekaligus.

## 4. Grammar Level Structure

### Basic

Objective:
User memahami pondasi kalimat sederhana. Fokusnya adalah mengenali jenis kata, subject, verb utama, object/complement, modal verb, tense sederhana, dan prepositional phrase.

Learning result:
User bisa membaca kalimat pendek dan menjawab: "Subject-nya apa? Verb utamanya apa? Informasi tambahannya apa?"

### Intermediate

Objective:
User mulai memahami kalimat yang lebih panjang dan sering muncul di TOEFL/BA context, seperti gerund, infinitive phrase, relative clause, passive voice, parallel structure, dan connector logic.

Learning result:
User bisa membedakan main clause dan tambahan informasi, serta tidak mudah tertipu oleh grammar trap.

### Advanced

Objective:
User memahami grammar untuk academic English dan professional BA writing. Fokusnya pada kalimat kompleks, nominalization, hedging language, inversion, conditional sentence, academic connectors, dan formal BA writing.

Learning result:
User bisa membaca teks TOEFL yang kompleks dan menulis kalimat Business Analyst yang formal, akurat, dan tidak terlalu kaku.

## 5. Basic Grammar Topics

### Parts of Speech

Purpose:
Mengenali fungsi kata seperti noun, verb, adjective, adverb, preposition, conjunction, dan pronoun.

Example sentence:
`The analyst reviews detailed requirements carefully.`

Beginner explanation:
`analyst` adalah noun, `reviews` adalah verb, `detailed` adalah adjective, dan `carefully` adalah adverb. Dalam Bahasa Indonesia: analis meninjau requirement yang detail dengan hati-hati.

### Subject and Verb

Purpose:
Menemukan pelaku utama dan aksi utama dalam kalimat.

Example sentence:
`The business analyst documents the stakeholder needs.`

Beginner explanation:
Subject-nya adalah `The business analyst`. Verb utamanya adalah `documents`. Artinya: Business Analyst mendokumentasikan kebutuhan stakeholder.

### Object and Complement

Purpose:
Memahami bagian setelah verb: apakah menjadi object, complement, atau informasi pelengkap.

Example sentence:
`The team considers the requirement important.`

Beginner explanation:
`the requirement` adalah object. `important` adalah complement yang menjelaskan object tersebut. Artinya: tim menganggap requirement itu penting.

### Modal Verb

Purpose:
Memahami kata bantu seperti `must`, `should`, `can`, `may`, dan `could`.

Example sentence:
`The analyst must clarify the problem before proposing a solution.`

Beginner explanation:
`must` berarti harus. Kalimat ini berarti analis harus mengklarifikasi masalah sebelum mengusulkan solusi.

### Simple Sentence Pattern

Purpose:
Mengenali pola dasar seperti Subject + Verb + Object.

Example sentence:
`Stakeholders provide feedback.`

Beginner explanation:
`Stakeholders` adalah subject, `provide` adalah verb, dan `feedback` adalah object. Polanya sederhana: Subject + Verb + Object.

### Simple Tense

Purpose:
Memahami waktu kejadian dalam kalimat sederhana.

Example sentence:
`The analyst interviews users every week.`

Beginner explanation:
`interviews` menunjukkan simple present. Artinya kegiatan ini terjadi secara rutin: analis mewawancarai user setiap minggu.

### Prepositional Phrase

Purpose:
Mengenali frasa yang diawali preposition seperti `in`, `on`, `with`, `before`, `after`, dan `from`.

Example sentence:
`The analyst works with stakeholders in a complex project.`

Beginner explanation:
`with stakeholders` dan `in a complex project` adalah prepositional phrase. Bagian ini memberi informasi tambahan, bukan verb utama.

## 6. Intermediate Grammar Topics

### Gerund vs Main Verb

Purpose:
Membedakan kata kerja bentuk `-ing` yang menjadi noun/modifier dengan verb utama.

Example sentence:
`Operating within a complex environment, the analyst must align requirements with strategy.`

Beginner explanation:
`Operating` bukan verb utama. Verb utama adalah `must align`. Bagian awal hanya menjelaskan kondisi analis.

Common trap:
User sering mengira kata pertama berakhiran `-ing` adalah aksi utama, padahal main verb muncul setelah subject utama.

### Infinitive Phrase

Purpose:
Memahami frasa `to + verb` sebagai tujuan atau pelengkap.

Example sentence:
`The analyst uses interviews to understand stakeholder expectations.`

Beginner explanation:
`to understand stakeholder expectations` menjelaskan tujuan interviews: untuk memahami ekspektasi stakeholder.

Common trap:
User mengira `to understand` adalah verb utama. Verb utama kalimat ini adalah `uses`.

### Relative Clause

Purpose:
Memahami clause yang menjelaskan noun, biasanya memakai `who`, `which`, atau `that`.

Example sentence:
`The requirement that the team approved must be documented.`

Beginner explanation:
`that the team approved` menjelaskan requirement mana yang dimaksud.

Common trap:
User membaca relative clause sebagai kalimat utama, padahal itu hanya penjelas noun.

### Reduced Relative Clause

Purpose:
Memahami relative clause yang dipendekkan.

Example sentence:
`The requirements approved by stakeholders are ready for development.`

Beginner explanation:
`approved by stakeholders` berarti `that were approved by stakeholders`. Bagian ini menjelaskan requirements.

Common trap:
User mengira `approved` adalah verb utama. Verb utama kalimat adalah `are`.

### Passive Voice

Purpose:
Memahami kalimat pasif saat fokusnya pada proses/hasil, bukan pelaku.

Example sentence:
`The workflow is reviewed before automation is proposed.`

Beginner explanation:
Workflow ditinjau dulu sebelum automation diusulkan. Fokusnya pada workflow dan automation, bukan siapa yang melakukan.

Common trap:
User sering menerjemahkan passive voice seperti active voice sehingga makna proses menjadi salah.

### Parallel Structure

Purpose:
Memastikan item dalam daftar atau pasangan grammar memiliki bentuk yang seimbang.

Example sentence:
`The analyst identifies issues, documents requirements, and validates solutions.`

Beginner explanation:
Tiga aksi memakai bentuk verb yang sejajar: `identifies`, `documents`, `validates`.

Common trap:
Mencampur bentuk kata, misalnya `identifies issues, documenting requirements, and validates solutions`.

### Connector Logic

Purpose:
Memahami hubungan ide melalui connector seperti `because`, `although`, `therefore`, `however`, dan `while`.

Example sentence:
`Although the process is slow, automation is not always the best solution.`

Beginner explanation:
`Although` menunjukkan kontras. Walaupun proses lambat, automation belum tentu solusi terbaik.

Common trap:
User hanya menerjemahkan kata connector, tetapi tidak menangkap hubungan logika antar ide.

## 7. Advanced Grammar Topics

### Complex Sentence Mapping

Purpose:
Memetakan kalimat panjang menjadi main clause, subordinate clause, phrase, dan modifier.

Example sentence:
`Before recommending automation, the analyst evaluates whether the current process should be redesigned.`

Professional explanation:
Main clause adalah `the analyst evaluates`. Bagian `Before recommending automation` adalah time/condition phrase, dan `whether the current process should be redesigned` adalah noun clause sebagai object.

Business Analyst usage:
Dipakai untuk menjelaskan keputusan analisis yang bergantung pada kondisi proses bisnis.

### Nominalization

Purpose:
Memahami perubahan verb/adjective menjadi noun agar tulisan lebih formal.

Example sentence:
`The evaluation of stakeholder feedback supports better prioritization.`

Professional explanation:
`evaluation` berasal dari `evaluate`, dan `prioritization` berasal dari `prioritize`. Nominalization membuat kalimat terdengar lebih formal.

Business Analyst usage:
Dipakai dalam report, business case, dan documentation agar tulisan lebih profesional.

### Hedging Language

Purpose:
Memahami bahasa yang tidak terlalu absolut, seperti `may`, `might`, `could`, `likely`, dan `appears to`.

Example sentence:
`The delay may indicate a bottleneck in the approval workflow.`

Professional explanation:
`may indicate` menunjukkan kemungkinan, bukan kepastian. Ini membuat analisis lebih hati-hati.

Business Analyst usage:
BA sering menggunakan hedging saat bukti belum lengkap dan masih perlu validasi.

### Inversion

Purpose:
Memahami susunan kata yang tidak biasa dalam gaya formal atau academic English.

Example sentence:
`Only after the requirements are validated can the team estimate the solution accurately.`

Professional explanation:
Kalimat memakai inversion: `can the team estimate`, bukan `the team can estimate`, karena diawali ekspresi pembatas `Only after`.

Business Analyst usage:
Dipakai untuk menekankan urutan atau syarat penting dalam keputusan proyek.

### Conditional Sentence

Purpose:
Memahami hubungan syarat dan hasil.

Example sentence:
`If the approval process remains unclear, the implementation may be delayed.`

Professional explanation:
Kalimat ini menjelaskan kondisi dan konsekuensi. Jika proses approval tetap tidak jelas, implementation mungkin tertunda.

Business Analyst usage:
Dipakai untuk risk analysis, impact analysis, dan recommendation.

### Academic Connectors

Purpose:
Memahami connector formal seperti `therefore`, `nevertheless`, `consequently`, `in contrast`, dan `as a result`.

Example sentence:
`The data is inconsistent; therefore, the report cannot be finalized.`

Professional explanation:
`therefore` menunjukkan hubungan sebab-akibat. Data tidak konsisten, akibatnya report belum bisa difinalkan.

Business Analyst usage:
Dipakai untuk menulis reasoning yang jelas dalam report dan recommendation.

### Formal BA Writing

Purpose:
Membantu user menulis kalimat formal, jelas, dan tidak ambigu dalam konteks BA.

Example sentence:
`The proposed solution should address the approval delay without increasing manual workload.`

Professional explanation:
Kalimat ini jelas karena menyebut solution, problem yang ditangani, dan constraint yang harus dihindari.

Business Analyst usage:
Dipakai dalam requirement, acceptance criteria, recommendation, dan stakeholder communication.

## 8. Future Feature Modules

### Grammar Diagnostic

Tes awal untuk mengetahui level grammar user, topic lemah, dan rekomendasi urutan belajar.

### Grammar Topic Library

Kumpulan topic grammar dengan contoh TOEFL + Business Analyst, penjelasan Indonesia, common trap, dan latihan kecil.

### Grammar Journey

Ringkasan progress grammar user: level, score, completed topics, weakest topic, strongest topic, dan next recommended action.

### Grammar Trainer

Latihan per topic dengan pertanyaan bertahap, feedback langsung, dan update journey.

### Deep Sentence Breakdown

Analisis kalimat panjang: subject, main verb, object/complement, phrase, clause, grammar pattern, dan trap.

### Grammar Error Correction

Latihan memperbaiki kalimat salah dan memahami alasan koreksi.

### Sentence Builder

Latihan menyusun kalimat dari komponen grammar: subject, verb, object, connector, modifier, dan BA context.

### Grammar Review

Halaman review topic lemah, kesalahan berulang, dan latihan ulang yang direkomendasikan.

### Mistake Pattern Analysis

Analisis pola kesalahan, misalnya sering salah membedakan gerund vs main verb atau passive vs active.

### Grammar Simulation

Simulasi TOEFL-style grammar dan BA writing grammar dengan timer, scoring, dan final report.

## 9. Proposed API Endpoints

Endpoint berikut hanya perencanaan. Jangan dianggap sudah tersedia sampai fase implementasi dibuat.

- `GET /api/grammar/levels`
- `GET /api/grammar/topics`
- `GET /api/grammar/topics/{topic_id}`
- `GET /api/grammar/journey`
- `POST /api/grammar/attempt`
- `GET /api/grammar/trainer/{topic_id}`
- `POST /api/grammar/trainer/submit`
- `POST /api/grammar/breakdown/deep`
- `GET /api/grammar/error-correction/{topic_id}`
- `POST /api/grammar/error-correction/submit`
- `GET /api/grammar/sentence-builder/{level}`
- `POST /api/grammar/sentence-builder/submit`
- `GET /api/grammar/review`
- `GET /api/grammar/mistake-patterns`
- `POST /api/grammar/simulation/start`
- `POST /api/grammar/simulation/submit`

## 10. Proposed UI Flow

Future Grammar page structure:

1. Grammar Journey summary
   - Current grammar level
   - Grammar score
   - Completed topics
   - Weakest topic
   - Next recommended topic
2. Level selector
   - Basic
   - Intermediate
   - Advanced
3. Topic list
   - Topic cards grouped by level
   - Status: not started, in progress, completed, needs review
4. Trainer panel
   - Short explanation
   - Practice question
   - Answer choices or input
   - Feedback
5. Sentence breakdown panel
   - User input sentence
   - Structure map
   - Indonesian explanation
6. Error correction panel
   - Incorrect sentence
   - User correction
   - Correct answer and explanation
7. Sentence builder panel
   - Build sentence from guided parts
   - BA context prompt
8. Review panel
   - Weak topics
   - Repeated mistakes
   - Recommended practice
9. Simulation panel
   - Timed set
   - Final score
   - Mistake summary

## 11. Learning Flow

Use this learning flow:

```text
Learn -> Breakdown -> Guided Practice -> Quiz -> Feedback -> Review
```

Meaning:

- Learn: user reads a simple explanation and example.
- Breakdown: user sees how the sentence is structured.
- Guided Practice: user answers with hints.
- Quiz: user answers without much help.
- Feedback: user learns why an answer is correct or wrong.
- Review: user repeats weak topics later.

## 12. Success Criteria

Grammar module can be considered successful when:

- User can clearly see their Grammar level and next action.
- User can learn grammar topic by topic, not only paste a sentence.
- Basic topics help users identify subject, verb, object, and complement.
- Intermediate topics help users avoid common TOEFL grammar traps.
- Advanced topics help users understand formal BA/academic writing.
- Every practice attempt gives useful Indonesian feedback.
- Weak topics are tracked and recommended for review.
- Existing `/api/grammar/breakdown` behavior remains backward compatible.
- The UI remains beginner-friendly and does not overwhelm users with grammar theory.
