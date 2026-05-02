const STORAGE_KEY = "toeflAnalystAiState";
const API_BASE = window.location.origin.includes("8001")
  ? `${window.location.origin}/api`
  : "http://127.0.0.1:8001/api";
let apiOnline = false;
let readingSimulationTimer = null;

const defaultState = {
  user: null,
  activeView: "dashboard",
  progress: {
    Reading: 0,
    Grammar: 0,
    Vocabulary: 0,
    Writing: 0,
    Listening: 0,
    Scenario: 0
  },
  completedExercises: 0,
  readingMode: "overview",
  readingAnswers: {},
  readingAnswerReviews: [],
  vocabularyAnswers: {},
  vocabularyDrill: {
    date: "",
    wordIds: [],
    answers: {}
  },
  scenarioAnswers: {},
  selectedReadingLessonId: "reading-1",
  activity: [],
  adminContent: {
    lessons: [],
    vocabulary: []
  },
  helpHistory: [],
  helpInput: "",
  contextualHelp: {
    cache: {},
    position: {
      x: null,
      y: null
    }
  },
  remoteContent: {
    lessons: null,
    vocabulary: null
  },
  integratedJourney: null,
  readingJourney: null,
  readingReview: null,
  readingTrainer: {
    selectedSubSkill: "main_idea",
    subskills: [],
    content: null,
    selectedAnswer: null,
    feedback: null
  },
  guidedReading: {
    lessonId: "",
    started: false,
    activeStep: 0,
    steps: [],
    passageMap: [],
    completed: false
  },
  readingSimulation: {
    mode: "short",
    session: null,
    answers: {},
    result: null,
    startedAtMs: null,
    history: []
  },
  grammarTrainer: {
    selectedTopic: "subject_verb",
    topics: [],
    trainer: null,
    answers: {},
    result: null
  },
  intermediateGrammarTrainer: {
    selectedTopic: "gerund_vs_main_verb",
    topics: [],
    trainer: null,
    answers: {},
    result: null
  },
  grammarErrorCorrection: {
    selectedErrorType: "missing_be_after_modal",
    categories: [],
    category: null,
    items: [],
    answers: {},
    result: null
  },
  grammarSentenceBuilder: {
    selectedLevel: "basic",
    selectedMode: "arrange_words",
    levels: [],
    items: [],
    answers: {},
    result: null
  },
  grammarAdvancedLab: {
    selectedTopic: "nominalization",
    topics: [],
    topic: null,
    practiceAnswers: {},
    rewriteAnswers: {},
    practiceResult: null,
    rewriteResult: null
  },
  grammarReview: null,
  grammarSimulation: {
    mode: "short",
    modes: [],
    session: null,
    answers: {},
    result: null,
    history: []
  },
  grammarHub: {
    activeSection: "menu",
    activeSubTopic: null
  },
  grammarProgress: {
    summary: null,
    modules: [],
    learningPath: [],
    recommendedSection: null,
    finishStatus: null
  },
  adaptivePractice: null,
  chat: [
    {
      role: "assistant",
      text: "Halo. Saya AI Tutor internal kamu. Tanyakan grammar, vocabulary, atau minta rekomendasi latihan hari ini."
    }
  ]
};

const lessons = [
  {
    id: "reading-1",
    title: "Stakeholder Needs and Strategy Alignment",
    level: "Foundation",
    context: "Requirement elicitation",
    passage:
      "A business analyst operating within a complex enterprise environment must not only elicit requirements but also ensure alignment between stakeholder needs and organizational strategy. When a stakeholder describes a problem vaguely, the analyst should clarify the expected outcome before proposing a solution.",
    vocabulary: ["elicit", "alignment", "stakeholder", "vaguely", "outcome"],
    grammar: "Reduced relative clause: operating within a complex enterprise environment.",
    questions: [
      {
        id: "r1q1",
        text: "What is the main idea of the passage?",
        options: [
          "Business analysts should write code immediately.",
          "Business analysts must connect requirements with stakeholder needs and strategy.",
          "Stakeholders should avoid discussing vague problems.",
          "Organizational strategy is unrelated to requirements."
        ],
        answer: 1,
        explanation:
          "The passage emphasizes eliciting requirements and aligning them with needs and strategy."
      },
      {
        id: "r1q2",
        text: "The word 'clarify' is closest in meaning to:",
        options: ["make clearer", "remove", "delay", "approve"],
        answer: 0,
        explanation:
          "Clarify means making vague information clearer before action."
      },
      {
        id: "r1q3",
        text: "What should the analyst do before proposing a solution?",
        options: [
          "Ask the developer to build it.",
          "Clarify the expected outcome.",
          "Ignore the stakeholder.",
          "Create a final contract."
        ],
        answer: 1,
        explanation:
          "The final sentence says the analyst should clarify the expected outcome first."
      }
    ]
  },
  {
    id: "reading-2",
    title: "Business Process Improvement",
    level: "Intermediate",
    context: "Business process",
    passage:
      "Before recommending automation, a business analyst evaluates the current process to identify delays, duplicate work, and unclear responsibilities. This analysis helps the organization determine whether technology is the right solution or whether the process itself must be redesigned.",
    vocabulary: ["automation", "evaluate", "duplicate", "responsibilities", "redesigned"],
    grammar: "Adverbial clause: Before recommending automation.",
    questions: [
      {
        id: "r2q1",
        text: "Why does the analyst evaluate the current process?",
        options: [
          "To identify delays and unclear responsibilities.",
          "To replace all employees.",
          "To avoid speaking with stakeholders.",
          "To skip process redesign."
        ],
        answer: 0,
        explanation:
          "The passage mentions delays, duplicate work, and unclear responsibilities as analysis targets."
      },
      {
        id: "r2q2",
        text: "What can the organization determine from the analysis?",
        options: [
          "Whether technology or process redesign is needed.",
          "Whether TOEFL is unnecessary.",
          "Whether all requirements are correct.",
          "Whether the analyst should stop the project."
        ],
        answer: 0,
        explanation:
          "The analysis compares technology as a solution with the need to redesign the process."
      }
    ]
  }
];

const vocabulary = [
  {
    id: "v1",
    word: "elicit",
    part: "verb",
    meaningId: "menggali atau memperoleh informasi",
    meaningEn: "to draw out information",
    example: "The analyst must elicit clear requirements from stakeholders.",
    answer: "menggali"
  },
  {
    id: "v2",
    word: "validate",
    part: "verb",
    meaningId: "memastikan sesuatu benar atau sesuai kebutuhan",
    meaningEn: "to confirm correctness or suitability",
    example: "The team validates the requirement before development starts.",
    answer: "memastikan"
  },
  {
    id: "v3",
    word: "prioritize",
    part: "verb",
    meaningId: "mengurutkan berdasarkan kepentingan",
    meaningEn: "to arrange by importance",
    example: "A product owner and analyst prioritize features for the next sprint.",
    answer: "mengurutkan"
  },
  {
    id: "v4",
    word: "assess",
    part: "verb",
    meaningId: "menilai atau mengevaluasi",
    meaningEn: "to evaluate or judge something",
    example: "The analyst assesses the impact of a proposed change.",
    answer: "menilai"
  },
  {
    id: "v5",
    word: "align",
    part: "verb",
    meaningId: "menyelaraskan",
    meaningEn: "to make things support the same goal",
    example: "The requirement must align with the business objective.",
    answer: "menyelaraskan"
  },
  {
    id: "v6",
    word: "stakeholder",
    part: "noun",
    meaningId: "pihak terkait",
    meaningEn: "a person or group affected by a project",
    example: "The stakeholder explains the reporting problem to the analyst.",
    answer: "pihak terkait"
  },
  {
    id: "v7",
    word: "objective",
    part: "noun",
    meaningId: "tujuan",
    meaningEn: "a goal or intended result",
    example: "The business objective is to reduce manual work.",
    answer: "tujuan"
  },
  {
    id: "v8",
    word: "constraint",
    part: "noun",
    meaningId: "batasan",
    meaningEn: "a limitation that affects a solution",
    example: "Budget is a constraint for the project team.",
    answer: "batasan"
  },
  {
    id: "v9",
    word: "scope",
    part: "noun",
    meaningId: "ruang lingkup",
    meaningEn: "the boundary of what is included",
    example: "The analyst clarifies the project scope before writing requirements.",
    answer: "ruang lingkup"
  },
  {
    id: "v10",
    word: "assumption",
    part: "noun",
    meaningId: "asumsi",
    meaningEn: "something believed to be true without full proof",
    example: "The team documents each assumption during planning.",
    answer: "asumsi"
  },
  {
    id: "v11",
    word: "issue",
    part: "noun",
    meaningId: "masalah",
    meaningEn: "a problem that needs attention",
    example: "The analyst identifies the main issue in the process.",
    answer: "masalah"
  },
  {
    id: "v12",
    word: "impact",
    part: "noun",
    meaningId: "dampak",
    meaningEn: "the effect of an action or change",
    example: "The impact of the change must be analyzed.",
    answer: "dampak"
  },
  {
    id: "v13",
    word: "process",
    part: "noun",
    meaningId: "proses",
    meaningEn: "a series of steps to achieve a result",
    example: "The current process causes delays in approval.",
    answer: "proses"
  },
  {
    id: "v14",
    word: "workflow",
    part: "noun",
    meaningId: "alur kerja",
    meaningEn: "the sequence of work activities",
    example: "The analyst maps the workflow before recommending automation.",
    answer: "alur kerja"
  },
  {
    id: "v15",
    word: "approval",
    part: "noun",
    meaningId: "persetujuan",
    meaningEn: "formal permission or acceptance",
    example: "The request requires approval from the manager.",
    answer: "persetujuan"
  },
  {
    id: "v16",
    word: "evidence",
    part: "noun",
    meaningId: "bukti",
    meaningEn: "information that supports a conclusion",
    example: "The analyst uses evidence from interviews and reports.",
    answer: "bukti"
  },
  {
    id: "v17",
    word: "define",
    part: "verb",
    meaningId: "mendefinisikan",
    meaningEn: "to explain the exact meaning of something",
    example: "The team defines the acceptance criteria clearly.",
    answer: "mendefinisikan"
  },
  {
    id: "v18",
    word: "verify",
    part: "verb",
    meaningId: "memverifikasi",
    meaningEn: "to check that something is correct",
    example: "The analyst verifies the requirement with the stakeholder.",
    answer: "memverifikasi"
  },
  {
    id: "v19",
    word: "clarify",
    part: "verb",
    meaningId: "memperjelas",
    meaningEn: "to make something easier to understand",
    example: "The analyst asks questions to clarify the problem.",
    answer: "memperjelas"
  },
  {
    id: "v20",
    word: "determine",
    part: "verb",
    meaningId: "menentukan",
    meaningEn: "to decide or discover something",
    example: "The team determines the most important requirement.",
    answer: "menentukan"
  },
  {
    id: "v21",
    word: "indicate",
    part: "verb",
    meaningId: "menunjukkan",
    meaningEn: "to show or suggest something",
    example: "The report indicates a delay in data collection.",
    answer: "menunjukkan"
  },
  {
    id: "v22",
    word: "significant",
    part: "adjective",
    meaningId: "signifikan atau penting",
    meaningEn: "important or large enough to notice",
    example: "The delay has a significant impact on decision-making.",
    answer: "signifikan"
  },
  {
    id: "v23",
    word: "feasible",
    part: "adjective",
    meaningId: "layak dilakukan",
    meaningEn: "possible and practical to do",
    example: "The analyst checks whether the solution is feasible.",
    answer: "layak"
  },
  {
    id: "v24",
    word: "accurate",
    part: "adjective",
    meaningId: "akurat",
    meaningEn: "correct and precise",
    example: "Users need accurate data in the dashboard.",
    answer: "akurat"
  },
  {
    id: "v25",
    word: "relevant",
    part: "adjective",
    meaningId: "relevan",
    meaningEn: "closely connected to the topic",
    example: "The analyst collects relevant information from users.",
    answer: "relevan"
  },
  {
    id: "v26",
    word: "ambiguous",
    part: "adjective",
    meaningId: "ambigu atau tidak jelas",
    meaningEn: "having more than one possible meaning",
    example: "The requirement is ambiguous and needs clarification.",
    answer: "ambigu"
  },
  {
    id: "v27",
    word: "consistent",
    part: "adjective",
    meaningId: "konsisten",
    meaningEn: "staying the same in quality or meaning",
    example: "The data format must be consistent across departments.",
    answer: "konsisten"
  },
  {
    id: "v28",
    word: "monitor",
    part: "verb",
    meaningId: "memantau",
    meaningEn: "to watch and check progress",
    example: "The team monitors system performance after release.",
    answer: "memantau"
  },
  {
    id: "v29",
    word: "measure",
    part: "verb",
    meaningId: "mengukur",
    meaningEn: "to find the size, amount, or level",
    example: "The analyst measures improvement using completion time.",
    answer: "mengukur"
  },
  {
    id: "v30",
    word: "recommend",
    part: "verb",
    meaningId: "merekomendasikan",
    meaningEn: "to suggest the best action",
    example: "The analyst recommends a simpler approval workflow.",
    answer: "merekomendasikan"
  }
];

const listeningScenario = {
  title: "Stakeholder Interview: Reporting Delay",
  transcript:
    "Stakeholder: The monthly report is always late. Analyst: What causes the delay? Stakeholder: Data from two departments arrives in different formats. Analyst: So the main issue is inconsistent input data before consolidation.",
  question: "What is the main issue discussed in the meeting?",
  answer: "Inconsistent input data before consolidation."
};

const scenarioQuestions = [
  {
    id: "s1",
    title: "Ambiguous Requirement",
    context: 'A stakeholder says, "The system should be more flexible."',
    question: "What should the business analyst do first?",
    options: [
      "Ask the developer to build the feature immediately.",
      "Clarify what flexible means through elicitation.",
      "Ignore the stakeholder because the statement is vague.",
      "Write the requirement exactly as spoken."
    ],
    answer: 1,
    explanation:
      "A BA should clarify vague language before documenting or proposing a solution."
  },
  {
    id: "s2",
    title: "Conflicting Stakeholder Priorities",
    context:
      "The finance team wants strict approval controls, while sales wants a faster checkout process.",
    question: "Which BA action best supports alignment?",
    options: [
      "Choose the finance team's request because controls are safer.",
      "Choose the sales team's request because speed improves revenue.",
      "Facilitate a discussion about business goals, risks, and measurable trade-offs.",
      "Send both requests directly to developers."
    ],
    answer: 2,
    explanation:
      "The BA should help stakeholders compare goals and trade-offs before solution decisions."
  },
  {
    id: "s3",
    title: "Solution Before Problem",
    context: 'A manager says, "We need a mobile app," but cannot explain the business problem.',
    question: "What is the best first question?",
    options: [
      "Which color should the mobile app use?",
      "What business outcome should this solution improve?",
      "Which developer is available this week?",
      "Can we skip user research?"
    ],
    answer: 1,
    explanation:
      "A BA should connect solution requests to business outcomes and user needs."
  }
];

const journeyDefinitions = {
  Reading: {
    goal: "Mampu membaca passage BA, menemukan ide utama, dan menjawab soal TOEFL-style.",
    steps: [
      {
        title: "Pahami arti umum",
        threshold: 0,
        detail: "Baca judul dan kalimat pertama. Cari siapa, melakukan apa, dan masalahnya apa.",
        next: "Gunakan Bantuan ID untuk menerjemahkan passage secara natural."
      },
      {
        title: "Cari main idea",
        threshold: 25,
        detail: "Tentukan ide utama sebelum melihat pilihan jawaban.",
        next: "Jawab pertanyaan main idea dan cocokkan dengan kata kunci passage."
      },
      {
        title: "Detail & vocabulary",
        threshold: 50,
        detail: "Temukan bukti jawaban di passage dan pahami kata dalam konteks.",
        next: "Latih vocabulary in context dari passage yang sama."
      },
      {
        title: "Inference",
        threshold: 75,
        detail: "Tarik kesimpulan dari informasi yang tidak disebutkan langsung.",
        next: "Kerjakan passage intermediate dan jelaskan alasan jawaban."
      },
      {
        title: "Advanced BA case",
        threshold: 90,
        detail: "Baca case lebih panjang seperti memo, proposal, dan meeting summary.",
        next: "Lanjut ke case advanced dan rangkum dalam Bahasa Inggris sederhana."
      }
    ]
  },
  Grammar: {
    goal: "Mampu membedah kalimat panjang menjadi subject, verb utama, phrase, clause, dan pola makna.",
    steps: [
      {
        title: "Subject + verb",
        threshold: 0,
        detail: "Cari pelaku dan aksi utama. Ini fondasi grammar.",
        next: "Ambil satu kalimat dan tandai subject serta main verb."
      },
      {
        title: "Object/complement",
        threshold: 25,
        detail: "Cari apa yang terkena aksi atau informasi pelengkap setelah verb.",
        next: "Pisahkan object dari phrase tambahan."
      },
      {
        title: "Phrase tambahan",
        threshold: 50,
        detail: "Kenali bagian yang membuat kalimat panjang, seperti operating within...",
        next: "Abaikan phrase dulu, lalu baca inti kalimatnya."
      },
      {
        title: "Clause & pattern",
        threshold: 75,
        detail: "Pahami clause, passive voice, reduced clause, dan not only...but also.",
        next: "Bandingkan dua kalimat dengan pola grammar yang sama."
      },
      {
        title: "Explain naturally",
        threshold: 90,
        detail: "Jelaskan grammar dengan Bahasa Indonesia sederhana.",
        next: "Tulis ulang penjelasan grammar untuk pemula."
      }
    ]
  },
  Vocabulary: {
    goal: "Mengingat kosakata TOEFL + Business Analyst dan memakai kata itu dalam kalimat kerja.",
    steps: [
      {
        title: "Kenali arti dasar",
        threshold: 0,
        detail: "Lihat word, arti Indonesia, dan contoh kalimat.",
        next: "Selesaikan 5 kata pertama tanpa mengejar sempurna."
      },
      {
        title: "Drill 25 kata",
        threshold: 25,
        detail: "Jawab target harian dan lihat kata mana yang salah.",
        next: "Selesaikan semua 25 kata hari ini."
      },
      {
        title: "Review kata salah",
        threshold: 50,
        detail: "Ulangi kata yang salah sampai tahu konteksnya.",
        next: "Buat satu kalimat sederhana dari 3 kata yang salah."
      },
      {
        title: "Gunakan dalam BA",
        threshold: 75,
        detail: "Pakai vocabulary dalam requirement, meeting, atau process sentence.",
        next: "Tulis 5 kalimat BA menggunakan kata hari ini."
      },
      {
        title: "Retention",
        threshold: 90,
        detail: "Pertahankan konsistensi beberapa hari agar kata tersimpan lama.",
        next: "Besok ulang kata yang salah sebelum mulai drill baru."
      }
    ]
  },
  Writing: {
    goal: "Mampu menulis requirement atau ringkasan profesional yang jelas, formal, dan terukur.",
    steps: [
      {
        title: "Kalimat sederhana",
        threshold: 0,
        detail: "Mulai dari pola The system must... atau The analyst identifies...",
        next: "Tulis satu requirement pendek dengan subject dan verb jelas."
      },
      {
        title: "Grammar dasar",
        threshold: 25,
        detail: "Perbaiki be verb, plural, dan verb form.",
        next: "Cek apakah adjective butuh 'be', seperti must be flexible."
      },
      {
        title: "Clarity",
        threshold: 50,
        detail: "Hilangkan kata ambigu seperti flexible tanpa ukuran.",
        next: "Tambahkan kondisi atau ukuran keberhasilan."
      },
      {
        title: "Coherence",
        threshold: 75,
        detail: "Susun kalimat agar alasan, masalah, dan solusi nyambung.",
        next: "Tulis versi revisi yang lebih formal."
      },
      {
        title: "Professional writing",
        threshold: 90,
        detail: "Tulis summary, recommendation, atau acceptance criteria.",
        next: "Buat satu paragraph pendek berdasarkan scenario BA."
      }
    ]
  },
  Listening: {
    goal: "Mampu memahami percakapan meeting BA dan menangkap masalah utama, aktor, serta keputusan.",
    steps: [
      {
        title: "Tangkap kata kunci",
        threshold: 0,
        detail: "Cari kata yang sering muncul: delay, data, format, approval.",
        next: "Baca transcript dan tandai 3 kata penting."
      },
      {
        title: "Main problem",
        threshold: 25,
        detail: "Temukan masalah utama yang sedang dibahas stakeholder.",
        next: "Jawab satu kalimat: masalah utamanya apa?"
      },
      {
        title: "Speaker intent",
        threshold: 50,
        detail: "Pahami maksud pembicara, bukan hanya arti kata.",
        next: "Tentukan siapa yang punya masalah dan siapa yang klarifikasi."
      },
      {
        title: "Transcript check",
        threshold: 75,
        detail: "Bandingkan jawaban dengan transcript dan vocabulary.",
        next: "Ulangi jawaban dengan kata sendiri dalam Bahasa Inggris sederhana."
      },
      {
        title: "Meeting summary",
        threshold: 90,
        detail: "Rangkum issue, cause, dan next action dari meeting.",
        next: "Tulis ringkasan 3 kalimat dari listening session."
      }
    ]
  }
};

let state = loadState();

const viewIds = {
  dashboard: "dashboardView",
  journey: "journeyView",
  help: "helpView",
  reading: "readingView",
  grammar: "grammarView",
  vocabulary: "vocabularyView",
  tutor: "tutorView",
  writing: "writingView",
  listening: "listeningView",
  scenario: "scenarioView",
  admin: "adminView"
};

document.addEventListener("DOMContentLoaded", async () => {
  bindShell();
  await hydrateFromApi();
  render();
});

function loadState() {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (!saved) return structuredClone(defaultState);
  const parsed = JSON.parse(saved);
  return {
    ...structuredClone(defaultState),
    ...parsed,
    progress: { ...defaultState.progress, ...(parsed.progress || {}) },
    adminContent: { ...defaultState.adminContent, ...(parsed.adminContent || {}) },
    contextualHelp: {
      cache: { ...(parsed.contextualHelp?.cache || {}) },
      position: { ...defaultState.contextualHelp.position, ...(parsed.contextualHelp?.position || {}) }
    },
    readingReview: parsed.readingReview || null,
    readingTrainer: { ...structuredClone(defaultState.readingTrainer), ...(parsed.readingTrainer || {}) },
    grammarTrainer: { ...structuredClone(defaultState.grammarTrainer), ...(parsed.grammarTrainer || {}) },
    intermediateGrammarTrainer: { ...structuredClone(defaultState.intermediateGrammarTrainer), ...(parsed.intermediateGrammarTrainer || {}) },
    grammarErrorCorrection: { ...structuredClone(defaultState.grammarErrorCorrection), ...(parsed.grammarErrorCorrection || {}) },
    grammarSentenceBuilder: { ...structuredClone(defaultState.grammarSentenceBuilder), ...(parsed.grammarSentenceBuilder || {}) },
    grammarAdvancedLab: { ...structuredClone(defaultState.grammarAdvancedLab), ...(parsed.grammarAdvancedLab || {}) },
    grammarReview: parsed.grammarReview || null,
    grammarSimulation: { ...structuredClone(defaultState.grammarSimulation), ...(parsed.grammarSimulation || {}) },
    grammarHub: { ...structuredClone(defaultState.grammarHub), ...(parsed.grammarHub || {}) },
    grammarProgress: { ...structuredClone(defaultState.grammarProgress), ...(parsed.grammarProgress || {}) },
    guidedReading: { ...structuredClone(defaultState.guidedReading), ...(parsed.guidedReading || {}) },
    readingSimulation: { ...structuredClone(defaultState.readingSimulation), ...(parsed.readingSimulation || {}) },
    chat: parsed.chat || structuredClone(defaultState.chat)
  };
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  if (apiOnline) {
    apiRequest("/state", {
      method: "POST",
      body: state
    }).catch(() => {
      apiOnline = false;
    });
  }
}

async function hydrateFromApi() {
  try {
    await apiRequest("/health");
    apiOnline = true;
    const [stateResponse, lessonsResponse, vocabularyResponse] = await Promise.all([
      apiRequest("/state"),
      apiRequest("/lessons"),
      apiRequest("/vocabulary")
    ]);
    if (stateResponse.state && Object.keys(stateResponse.state).length) {
      state = {
        ...state,
        ...stateResponse.state,
        progress: { ...defaultState.progress, ...(stateResponse.state.progress || state.progress) },
        adminContent: { ...defaultState.adminContent, ...(stateResponse.state.adminContent || state.adminContent) },
        contextualHelp: {
          cache: { ...(stateResponse.state.contextualHelp?.cache || state.contextualHelp?.cache || {}) },
          position: { ...defaultState.contextualHelp.position, ...(stateResponse.state.contextualHelp?.position || state.contextualHelp?.position || {}) }
        },
        readingReview: stateResponse.state.readingReview || state.readingReview || null,
        readingTrainer: { ...structuredClone(defaultState.readingTrainer), ...(stateResponse.state.readingTrainer || state.readingTrainer || {}) },
        grammarTrainer: { ...structuredClone(defaultState.grammarTrainer), ...(stateResponse.state.grammarTrainer || state.grammarTrainer || {}) },
        intermediateGrammarTrainer: { ...structuredClone(defaultState.intermediateGrammarTrainer), ...(stateResponse.state.intermediateGrammarTrainer || state.intermediateGrammarTrainer || {}) },
        grammarErrorCorrection: { ...structuredClone(defaultState.grammarErrorCorrection), ...(stateResponse.state.grammarErrorCorrection || state.grammarErrorCorrection || {}) },
        grammarSentenceBuilder: { ...structuredClone(defaultState.grammarSentenceBuilder), ...(stateResponse.state.grammarSentenceBuilder || state.grammarSentenceBuilder || {}) },
        grammarAdvancedLab: { ...structuredClone(defaultState.grammarAdvancedLab), ...(stateResponse.state.grammarAdvancedLab || state.grammarAdvancedLab || {}) },
        grammarReview: stateResponse.state.grammarReview || state.grammarReview || null,
        grammarSimulation: { ...structuredClone(defaultState.grammarSimulation), ...(stateResponse.state.grammarSimulation || state.grammarSimulation || {}) },
        grammarHub: { ...structuredClone(defaultState.grammarHub), ...(stateResponse.state.grammarHub || state.grammarHub || {}) },
        grammarProgress: { ...structuredClone(defaultState.grammarProgress), ...(stateResponse.state.grammarProgress || state.grammarProgress || {}) },
        guidedReading: { ...structuredClone(defaultState.guidedReading), ...(stateResponse.state.guidedReading || state.guidedReading || {}) },
        readingSimulation: { ...structuredClone(defaultState.readingSimulation), ...(stateResponse.state.readingSimulation || state.readingSimulation || {}) }
      };
    }
    state.remoteContent = {
      lessons: lessonsResponse.lessons || null,
      vocabulary: vocabularyResponse.vocabulary || null
    };
    const dailyVocabularyResponse = await apiRequest("/vocabulary/daily");
    state.remoteDailyVocabulary = dailyVocabularyResponse;
    const analyticsResponse = await apiRequest("/progress/analytics", {
      method: "POST",
      body: state
    });
    state.latestAnalytics = analyticsResponse.analytics;
    await refreshIntegratedJourney();
    await refreshReadingJourney();
    await refreshGrammarProgress();
  } catch (error) {
    apiOnline = false;
    state.integratedJourney = localJourneySummary();
    state.readingJourney = localReadingJourney();
    state.readingReview = localReadingReview();
    state.readingTrainer = localReadingTrainerState();
    state.grammarProgress = localGrammarProgress();
  }
}

async function refreshIntegratedJourney() {
  if (!apiOnline) {
    state.integratedJourney = localJourneySummary();
    return;
  }
  try {
    state.integratedJourney = await apiRequest(`/journey/summary${state.user?.id ? `?user_id=${encodeURIComponent(state.user.id)}` : ""}`);
    state.adaptivePractice = state.integratedJourney.adaptive_practice || null;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (error) {
    apiOnline = false;
    state.integratedJourney = localJourneySummary();
  }
}

async function refreshReadingJourney() {
  if (!apiOnline) {
    state.readingJourney = localReadingJourney();
    return;
  }
  try {
    const query = state.user?.id ? `?user_id=${encodeURIComponent(state.user.id)}` : "";
    const response = await apiRequest(`/reading/journey${query}`);
    state.readingJourney = response.reading_journey;
    await refreshReadingTrainer(state.readingTrainer?.selectedSubSkill || "main_idea");
    await refreshReadingReview();
    await refreshReadingSimulationHistory();
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (error) {
    apiOnline = false;
    state.readingJourney = localReadingJourney();
    state.readingReview = localReadingReview();
    state.readingTrainer = localReadingTrainerState();
  }
}

async function refreshReadingSimulationHistory() {
  if (!apiOnline) return;
  try {
    const query = state.user?.id ? `?user_id=${encodeURIComponent(state.user.id)}` : "";
    const response = await apiRequest(`/reading/simulation/history${query}`);
    state.readingSimulation.history = response.history || [];
  } catch (error) {
    state.readingSimulation.history = state.readingSimulation.history || [];
  }
}

async function refreshReadingReview() {
  if (!apiOnline) {
    state.readingReview = localReadingReview();
    return;
  }
  try {
    const query = state.user?.id ? `?user_id=${encodeURIComponent(state.user.id)}` : "";
    state.readingReview = await apiRequest(`/reading/review${query}`);
  } catch (error) {
    state.readingReview = localReadingReview();
  }
}

async function refreshReadingTrainer(subSkill = "main_idea") {
  if (!apiOnline) {
    state.readingTrainer = localReadingTrainerState(subSkill);
    return;
  }
  try {
    const query = state.user?.id ? `?user_id=${encodeURIComponent(state.user.id)}` : "";
    const [subskillsResponse, trainerResponse] = await Promise.all([
      apiRequest(`/reading/subskills${query}`),
      apiRequest(`/reading/trainer/${encodeURIComponent(subSkill)}${query}`)
    ]);
    state.readingTrainer = {
      selectedSubSkill: trainerResponse.sub_skill,
      subskills: subskillsResponse.subskills || [],
      content: trainerResponse,
      selectedAnswer: null,
      feedback: null
    };
  } catch (error) {
    apiOnline = false;
    state.readingTrainer = localReadingTrainerState(subSkill);
  }
}

async function refreshGrammarProgress() {
  if (!apiOnline) {
    state.grammarProgress = localGrammarProgress();
    return;
  }
  try {
    const query = state.user?.id ? `?user_id=${encodeURIComponent(state.user.id)}` : "";
    const response = await apiRequest(`/grammar/progress${query}`);
    state.grammarProgress = {
      summary: response.summary || null,
      modules: response.modules || [],
      learningPath: response.learning_path || [],
      recommendedSection: response.recommended_section || null,
      finishStatus: response.finish_status || null
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (error) {
    state.grammarProgress = localGrammarProgress();
  }
}

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: options.method || "GET",
    headers: {
      "Content-Type": "application/json"
    },
    body: options.body ? JSON.stringify(options.body) : undefined
  });
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }
  return response.json();
}

function bindShell() {
  document.getElementById("authForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const profile = {
      name: document.getElementById("nameInput").value.trim(),
      targetScore: Number(document.getElementById("targetInput").value),
      weakness: document.getElementById("weaknessInput").value,
      level: "Foundation"
    };
    if (apiOnline) {
      try {
        const response = await apiRequest("/auth/register", {
          method: "POST",
          body: {
            ...profile,
            email: `${profile.name.toLowerCase().replaceAll(" ", ".")}@example.local`
          }
        });
        state.user = response.user;
        state.token = response.token;
      } catch (error) {
        state.user = profile;
        apiOnline = false;
      }
    } else {
      state.user = profile;
    }
    state.activeView = "dashboard";
    saveState();
    await refreshIntegratedJourney();
    render();
  });

  document.querySelectorAll(".nav-item").forEach((button) => {
    button.addEventListener("click", async () => {
      state.activeView = button.dataset.view;
      if (state.activeView === "grammar") {
        await refreshGrammarProgress();
      }
      saveState();
      render();
    });
  });

  document.getElementById("logoutButton").addEventListener("click", () => {
    localStorage.removeItem(STORAGE_KEY);
    state = structuredClone(defaultState);
    render();
  });
}

function render() {
  const hasUser = Boolean(state.user);
  document.getElementById("app").classList.toggle("logged-out", !hasUser);
  document.getElementById("authView").classList.toggle("hidden", hasUser);
  document.querySelectorAll(".view").forEach((view) => view.classList.remove("active"));

  if (!hasUser) {
    document.querySelector(".sidebar").style.display = "none";
    return;
  }

  document.querySelector(".sidebar").style.display = "flex";
  document.getElementById("profileName").textContent = state.user.name;
  document.getElementById("profileGoal").textContent = `Target: ${state.user.targetScore} | Weakness: ${state.user.weakness}`;

  Object.entries(viewIds).forEach(([key, id]) => {
    document.getElementById(id).classList.toggle("active", state.activeView === key);
  });

  document.querySelectorAll(".nav-item").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === state.activeView);
  });

  renderDashboard();
  renderJourney();
  renderHelp();
  renderReading();
  renderGrammar();
  renderVocabulary();
  renderTutor();
  renderWriting();
  renderListening();
  renderScenario();
  renderAdmin();
}

function pageHeaderTemplate({ eyebrow, title, description, actions = "", status = "" }) {
  return `
    <header class="page-header">
      <div>
        <div class="page-header-meta">
          <span class="eyebrow">${escapeHtml(eyebrow || "")}</span>
          ${status ? `<span class="status-pill">${escapeHtml(status)}</span>` : ""}
        </div>
        <h2>${escapeHtml(title || "")}</h2>
        <p>${escapeHtml(description || "")}</p>
      </div>
      ${actions ? `<div class="page-actions">${actions}</div>` : ""}
    </header>
  `;
}

function emptyStateTemplate(title, body, action = "") {
  return `
    <div class="empty-state">
      <strong>${escapeHtml(title)}</strong>
      <p>${escapeHtml(body)}</p>
      ${action}
    </div>
  `;
}

function moduleQuickActions(actions) {
  return `
    <div class="quick-actions">
      ${actions.map((action) => `
        <button class="ghost-button" type="button" ${action.attr || ""}>${escapeHtml(action.label)}</button>
      `).join("")}
    </div>
  `;
}

function renderDashboard() {
  const weakest = getWeakestSkill();
  const recentActivity = state.activity.slice(0, 5);
  const apiStatus = apiOnline ? "Backend API aktif" : "Mode lokal";
  const recommendation = state.latestRecommendation?.recommendation || recommendationText();
  const analytics = state.latestAnalytics || localAnalytics();
  document.getElementById("dashboardView").innerHTML = `
    <header class="dashboard-hero">
      <div>
        <div class="page-header-meta">
          <span class="eyebrow">Beranda Belajar</span>
          <span class="status-pill">${apiStatus}</span>
        </div>
        <h2>Halo, ${escapeHtml(state.user.name)}. Fokus hari ini: ${escapeHtml(weakest)}.</h2>
        <p>Mulai dari satu langkah kecil: pahami arti umum, cari subject dan verb utama, lalu lanjutkan latihan dari rekomendasi journey.</p>
      </div>
      <div class="page-actions">
        <button class="primary-button" data-go="journey">Lihat Perjalanan</button>
        <button class="secondary-button" data-go="reading">Mulai Reading</button>
        <button class="ghost-button" data-go="help">Bantuan ID</button>
      </div>
    </header>

    <section class="dashboard-grid two">
      <article class="module-surface dashboard-next-card">
        <span class="soft-pill">Lanjut belajar</span>
        <h3>${skillLabel((state.integratedJourney || localJourneySummary()).journey?.next_recommended_module || weakest)}</h3>
        <p>${recommendation}</p>
        <div class="progress-bar"><span style="width:${overallProgress()}%"></span></div>
        <small>${overallProgress()}% progress rata-rata · ${state.completedExercises} latihan selesai</small>
      </article>
      <article class="module-surface">
        <span class="soft-pill">BA Learning Path</span>
        <div class="dashboard-step-list">
          ${["Stakeholder Need", "Requirement Clarity", "Strategy Alignment"].map((item, index) => `
            <div>
              <strong>${index + 1}</strong>
              <span>${item}</span>
            </div>
          `).join("")}
        </div>
      </article>
    </section>

    <section class="dashboard-progress-grid">
      ${Object.entries(state.progress).map(([skill, score]) => metricTemplate(skill, score)).join("")}
    </section>

    <section class="dashboard-grid three">
      ${dashboardAnalyticsCard("Average", analytics.averageScore, `${analytics.averageScore}%`, analytics.status)}
      ${dashboardAnalyticsCard("Weakest", analytics.weakestSkill, analytics.weakestSkill, "Skill prioritas hari ini.")}
      ${dashboardAnalyticsCard("Strongest", analytics.strongestSkill, analytics.strongestSkill, "Skill paling stabil.")}
    </section>

    <section class="dashboard-grid two">
      <article class="module-surface">
        <div class="section-heading">
          <div>
            <p class="eyebrow">Modul utama</p>
            <h3>Pilih latihan cepat</h3>
          </div>
        </div>
        <div class="dashboard-module-grid">
          ${[
            ["reading", "Reading", "Passage, trainer, simulation"],
            ["grammar", "Grammar", "Subject, verb, phrase"],
            ["vocabulary", "Vocabulary", "25 kata harian"],
            ["writing", "Writing", "Requirement statement"],
            ["listening", "Listening", "Transcript dan jawaban"],
            ["scenario", "Scenario BA", "Case study decision"]
          ].map(([view, title, desc]) => `
            <button class="module-card soft" data-go="${view}">
              <strong>${title}</strong>
              <span>${desc}</span>
            </button>
          `).join("")}
        </div>
      </article>
      <article class="module-surface">
        <div class="section-heading">
          <div>
            <p class="eyebrow">Recent Activity</p>
            <h3>${recentActivity.length} aktivitas terakhir</h3>
          </div>
        </div>
        ${
          recentActivity.length
            ? `<div class="activity-list">${recentActivity
                .map((item) => `<div class="activity-row"><strong>${item.module}</strong><span>${item.summary}</span><small>${item.score}</small></div>`)
                .join("")}</div>`
            : emptyStateTemplate("Belum ada aktivitas", "Mulai satu latihan untuk mengisi progress dan rekomendasi.")
        }
      </article>
    </section>

    ${integratedJourneySection()}
  `;

  document.querySelectorAll("[data-go]").forEach((button) => {
    button.addEventListener("click", () => {
      state.activeView = button.dataset.go;
      saveState();
      render();
    });
  });
  bindJourneyActions();

  if (apiOnline) {
    Promise.all([
      apiRequest("/ai-tutor/recommendation", {
        method: "POST",
        body: { progress: state.progress }
      }),
      apiRequest("/progress/analytics", {
        method: "POST",
        body: state
      })
    ])
      .then(([recommendationResponse, analyticsResponse]) => {
        state.latestRecommendation = recommendationResponse;
        state.latestAnalytics = analyticsResponse.analytics;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      })
      .catch(() => {
        apiOnline = false;
      });
  }
}

function renderJourney() {
  const summary = state.integratedJourney || localJourneySummary();
  const adaptive = state.adaptivePractice || summary.adaptive_practice || localAdaptivePractice(summary);
  document.getElementById("journeyView").innerHTML = `
    ${pageHeaderTemplate({
      eyebrow: "Perjalanan Belajar Saya",
      title: "Satu peta belajar untuk semua skill TOEFL + Business Analyst.",
      description: "Progress tersimpan di backend jika API aktif. Kamu bisa lanjut dari aktivitas terakhir, melihat skill lemah, dan mengambil latihan adaptif tanpa mulai dari nol.",
      actions: `<button id="refreshJourneyButton" class="ghost-button">Refresh Progress</button><button class="primary-button" data-journey-continue>Lanjutkan Belajar</button>`
    })}
    ${integratedJourneySection(true)}
    ${adaptivePracticeSection(adaptive)}
  `;
  document.getElementById("refreshJourneyButton").addEventListener("click", async () => {
    await refreshIntegratedJourney();
    renderJourney();
  });
  bindJourneyActions();
  bindAdaptiveActions();
}

function integratedJourneySection(expanded = false) {
  const summary = state.integratedJourney || localJourneySummary();
  const journey = summary.journey;
  const skills = summary.skills || [];
  const continueState = summary.continue_learning || {};
  const reviewList = summary.review_list || {};
  const dailyPlan = summary.daily_plan || [];
  const adaptive = state.adaptivePractice || summary.adaptive_practice || localAdaptivePractice(summary);
  return `
    <section class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm lg:p-6">
      <div class="mb-5 flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
        <div class="max-w-3xl">
          <span class="mb-3 inline-flex rounded-full bg-cyan-50 px-3 py-1 text-xs font-bold uppercase tracking-wide text-cyan-700">Perjalanan Belajar Saya</span>
          <h3 class="mb-2 text-xl font-black text-slate-900 lg:text-2xl">${journey.current_level} - skor keseluruhan ${Math.round(journey.overall_score || 0)}%</h3>
          <p class="text-sm leading-6 text-slate-600">${summary.mentor_message || "Progress Anda tersimpan. Hari ini cukup fokus ke satu langkah kecil dulu."}</p>
        </div>
        <button class="rounded-xl bg-cyan-700 px-4 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-cyan-800" data-journey-continue>Lanjutkan Belajar</button>
      </div>
      <div class="mb-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-6">
        ${journeyMetric("Level", journey.current_level)}
        ${journeyMetric("Overall", `${Math.round(journey.overall_score || 0)}%`)}
        ${journeyMetric("Streak", `${journey.learning_streak || 0} hari`)}
        ${journeyMetric("Latihan", journey.total_exercises || 0)}
        ${journeyMetric("Terkuat", skillLabel(journey.strongest_skill))}
        ${journeyMetric("Terlemah", skillLabel(journey.weakest_skill))}
      </div>
      <div class="mb-5 grid gap-4 xl:grid-cols-3">
        <div class="rounded-2xl border border-slate-200 bg-slate-50 p-4">
          <h3 class="mb-2 text-base font-extrabold text-slate-900">Continue Learning</h3>
          <p class="mb-2 text-lg font-black text-cyan-700">${skillLabel(continueState.recommended_module || journey.next_recommended_module)}</p>
          <p class="mb-3 text-sm leading-6 text-slate-600">${continueState.message || continueState.next_action || "Mulai dari modul yang paling lemah dulu."}</p>
          <small class="text-xs font-semibold text-slate-500">Aktivitas terakhir: ${formatDate(journey.last_activity_at) || "Belum ada aktivitas tersimpan"}</small>
        </div>
        <div class="rounded-2xl border border-cyan-100 bg-cyan-50 p-4">
          <h3 class="mb-2 text-base font-extrabold text-slate-900">Latihan Adaptif Hari Ini</h3>
          <p class="mb-2 font-black text-slate-900">${escapeHtml(adaptive.title)}</p>
          <p class="mb-4 text-sm leading-6 text-slate-600">${escapeHtml(adaptive.reason)}</p>
          <button class="rounded-xl bg-slate-900 px-4 py-2 text-sm font-bold text-white transition hover:bg-slate-700" data-open-journey>Detail latihan</button>
        </div>
        <div class="rounded-2xl border border-slate-200 bg-slate-50 p-4">
          <h3 class="mb-3 text-base font-extrabold text-slate-900">Daily Study Plan</h3>
          <div class="grid gap-2">
            ${dailyPlan.map((item) => `<div class="rounded-xl bg-white p-3"><div class="flex items-center justify-between gap-3"><strong class="text-sm text-slate-900">${skillLabel(item.skill_type)}</strong><small class="font-bold text-cyan-700">${item.duration}</small></div><p class="mt-1 text-sm leading-5 text-slate-600">${item.task}</p></div>`).join("")}
          </div>
        </div>
      </div>
      <section class="grid gap-4 md:grid-cols-2 2xl:grid-cols-3">
        ${skills.map(skillJourneyCard).join("")}
      </section>
      ${expanded ? reviewListTemplate(reviewList) : ""}
    </section>
  `;
}

function adaptivePracticeSection(adaptive) {
  return `
    <section class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm lg:p-6">
      <div class="mb-5 flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
        <div>
          <span class="mb-3 inline-flex rounded-full bg-emerald-50 px-3 py-1 text-xs font-bold uppercase tracking-wide text-emerald-700">AI Mentor Adaptif</span>
          <h3 class="mb-2 text-xl font-black text-slate-900 lg:text-2xl">${escapeHtml(adaptive.title)}</h3>
          <p class="max-w-3xl text-sm leading-6 text-slate-600">${escapeHtml(adaptive.mentor_message)}</p>
        </div>
        <div class="flex flex-wrap gap-3">
          <button class="rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-bold text-slate-700 transition hover:bg-slate-50" data-adaptive-refresh>Ambil Latihan Baru</button>
          <button class="rounded-xl bg-cyan-700 px-4 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-cyan-800" data-adaptive-complete>Saya Selesai</button>
        </div>
      </div>
      <div class="mb-5 rounded-2xl border border-amber-200 bg-amber-50 p-4">
        <strong class="mb-2 block text-sm text-slate-900">Prompt latihan</strong>
        <p class="text-sm leading-6 text-slate-700">${escapeHtml(adaptive.practice_prompt)}</p>
      </div>
      <div class="mb-5 grid gap-4 md:grid-cols-3">
        ${(adaptive.tasks || []).map((task, index) => `
          <article class="rounded-2xl border border-slate-200 bg-slate-50 p-4">
            <span class="mb-3 inline-flex rounded-full bg-white px-3 py-1 text-xs font-bold text-cyan-700">Step ${index + 1}</span>
            <strong class="mb-2 block text-base text-slate-900">${escapeHtml(task.title)}</strong>
            <p class="text-sm leading-6 text-slate-600">${escapeHtml(task.instruction)}</p>
          </article>
        `).join("")}
      </div>
      <div class="grid gap-4 xl:grid-cols-2">
        <div class="rounded-2xl border border-slate-200 bg-slate-50 p-4">
          <h3 class="mb-2 text-base font-extrabold text-slate-900">Kenapa ini dipilih?</h3>
          <p class="text-sm leading-6 text-slate-600">${escapeHtml(adaptive.reason)}</p>
        </div>
        <div class="rounded-2xl border border-slate-200 bg-slate-50 p-4">
          <h3 class="mb-3 text-base font-extrabold text-slate-900">Recent Attempts</h3>
          ${adaptive.recent_attempts?.length
            ? `<div class="grid gap-2">${adaptive.recent_attempts.map((item) => `<p class="rounded-xl bg-white p-3 text-sm text-slate-600"><strong class="text-slate-900">${skillLabel(item.skill_type)}</strong> - ${Math.round(item.accuracy || 0)}% <small class="ml-2 text-slate-500">${formatDate(item.created_at)}</small></p>`).join("")}</div>`
            : `<p class="text-sm leading-6 text-slate-500">Belum ada attempt untuk skill ini. Latihan pertama akan mulai membentuk rekomendasi.</p>`}
        </div>
      </div>
    </section>
  `;
}

function journeyMetric(label, value) {
  return `
    <div class="rounded-2xl border border-slate-200 bg-slate-50 p-4">
      <span class="mb-2 block text-xs font-bold uppercase tracking-wide text-slate-500">${label}</span>
      <strong class="block break-words text-lg font-black text-slate-900">${escapeHtml(String(value ?? "-"))}</strong>
    </div>
  `;
}

function skillJourneyCard(skill) {
  const score = Math.round(skill.average_score || 0);
  return `
    <article class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
      <div class="mb-3 flex items-center justify-between gap-3">
        <span class="rounded-full bg-cyan-50 px-3 py-1 text-xs font-bold text-cyan-700">${skillLabel(skill.skill_type)}</span>
        <strong class="text-sm text-slate-900">${skill.current_level}</strong>
      </div>
      <div class="mb-3 h-2 overflow-hidden rounded-full bg-slate-100"><span class="block h-full rounded-full bg-cyan-700" style="width:${score}%"></span></div>
      <div class="mb-3 flex flex-wrap items-center gap-3 text-xs font-bold text-slate-500">
        <span>${score}%</span>
        <span>${skill.completed_count || 0} latihan</span>
        <span>${statusLabel(skill.status)}</span>
      </div>
      <p class="mb-3 text-sm leading-6 text-slate-600">${skill.next_action || "Lanjutkan satu latihan pendek hari ini."}</p>
      <small class="text-xs font-semibold text-slate-500">Terakhir: ${formatDate(skill.last_activity_at) || "Belum pernah"}</small>
    </article>
  `;
}

function reviewListTemplate(reviewList) {
  const weakVocabulary = reviewList.weak_vocabulary || [];
  const weakGrammar = reviewList.weak_grammar_topics || [];
  const dueItems = reviewList.due_for_review || [];
  return `
    <section class="mt-5 grid gap-4 xl:grid-cols-3">
      <div class="rounded-2xl border border-slate-200 bg-slate-50 p-4">
        <h3 class="mb-3 text-base font-extrabold text-slate-900">Review Vocabulary</h3>
        ${weakVocabulary.length ? weakVocabulary.map((item) => `<p class="rounded-xl bg-white p-3 text-sm text-slate-600"><strong class="text-slate-900">${escapeHtml(item.word)}</strong> - ${escapeHtml(item.meaning || "review meaning")} <small class="ml-2 font-bold text-cyan-700">${item.status}</small></p>`).join("") : `<p class="text-sm leading-6 text-slate-500">Belum ada vocabulary lemah. Nanti akan muncul setelah drill.</p>`}
      </div>
      <div class="rounded-2xl border border-slate-200 bg-slate-50 p-4">
        <h3 class="mb-3 text-base font-extrabold text-slate-900">Review Grammar</h3>
        ${weakGrammar.length ? weakGrammar.map((item) => `<p class="rounded-xl bg-white p-3 text-sm text-slate-600"><strong class="text-slate-900">${escapeHtml(item.topic)}</strong> - mastery ${Math.round(item.mastery_score || 0)}%</p>`).join("") : `<p class="text-sm leading-6 text-slate-500">Belum ada topik grammar yang perlu review.</p>`}
      </div>
      <div class="rounded-2xl border border-slate-200 bg-slate-50 p-4">
        <h3 class="mb-3 text-base font-extrabold text-slate-900">Due Review</h3>
        ${dueItems.length ? dueItems.map((item) => `<p class="rounded-xl bg-white p-3 text-sm text-slate-600"><strong class="text-slate-900">${escapeHtml(item.item)}</strong><br><small class="text-slate-500">${formatDate(item.next_review_at)}</small></p>`).join("") : `<p class="text-sm leading-6 text-slate-500">Belum ada item yang jatuh tempo.</p>`}
      </div>
    </section>
  `;
}

function bindJourneyActions() {
  document.querySelectorAll("[data-journey-continue]").forEach((button) => {
    if (button.dataset.boundJourney === "true") return;
    button.dataset.boundJourney = "true";
    button.addEventListener("click", () => {
      const summary = state.integratedJourney || localJourneySummary();
      const moduleName = summary.continue_learning?.recommended_module || summary.journey?.next_recommended_module || "grammar";
      state.activeView = moduleToView(moduleName);
      saveState();
      render();
    });
  });
  document.querySelectorAll("[data-open-journey]").forEach((button) => {
    if (button.dataset.boundOpenJourney === "true") return;
    button.dataset.boundOpenJourney = "true";
    button.addEventListener("click", () => {
      state.activeView = "journey";
      saveState();
      render();
    });
  });
}

function bindAdaptiveActions() {
  document.querySelectorAll("[data-adaptive-refresh]").forEach((button) => {
    if (button.dataset.boundAdaptiveRefresh === "true") return;
    button.dataset.boundAdaptiveRefresh = "true";
    button.addEventListener("click", async () => {
      await refreshAdaptivePractice();
      renderJourney();
    });
  });
  document.querySelectorAll("[data-adaptive-complete]").forEach((button) => {
    if (button.dataset.boundAdaptiveComplete === "true") return;
    button.dataset.boundAdaptiveComplete = "true";
    button.addEventListener("click", async () => {
      await completeAdaptivePractice();
      renderJourney();
      renderDashboard();
    });
  });
}

async function refreshAdaptivePractice() {
  const summary = state.integratedJourney || localJourneySummary();
  const skillType = state.adaptivePractice?.skill_type || summary.journey?.next_recommended_module || "grammar";
  if (!apiOnline) {
    state.adaptivePractice = localAdaptivePractice(summary);
    return;
  }
  try {
    state.adaptivePractice = await apiRequest(`/journey/adaptive-practice?skill_type=${encodeURIComponent(skillType)}${state.user?.id ? `&user_id=${encodeURIComponent(state.user.id)}` : ""}`);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (error) {
    apiOnline = false;
    state.adaptivePractice = localAdaptivePractice(summary);
  }
}

async function completeAdaptivePractice() {
  const summary = state.integratedJourney || localJourneySummary();
  const adaptive = state.adaptivePractice || summary.adaptive_practice || localAdaptivePractice(summary);
  const score = Math.max(65, Math.round(summary.journey?.overall_score || 65));
  if (apiOnline) {
    try {
      const response = await apiRequest("/journey/adaptive-practice/complete", {
        method: "POST",
        body: {
          user_id: state.user?.id || "default-user",
          skill_type: adaptive.skill_type,
          score,
          max_score: 100,
          notes: "User menyelesaikan latihan adaptif dari halaman Perjalanan."
        }
      });
      state.adaptivePractice = response.next_practice;
      await refreshIntegratedJourney();
      return;
    } catch (error) {
      apiOnline = false;
    }
  }
  const label = skillLabel(adaptive.skill_type).replace(" BA", "");
  state.progress[label] = Math.max(state.progress[label] || 0, score);
  state.completedExercises += 1;
  addActivity("Adaptive", adaptive.title, score);
  state.adaptivePractice = localAdaptivePractice(localJourneySummary());
  saveState();
}

function moduleToView(skillType) {
  return skillType === "scenario" ? "scenario" : skillType || "grammar";
}

function skillLabel(skillType) {
  const labels = {
    reading: "Reading",
    grammar: "Grammar",
    vocabulary: "Vocabulary",
    writing: "Writing",
    listening: "Listening",
    scenario: "Scenario BA"
  };
  return labels[skillType] || skillType || "-";
}

function statusLabel(status) {
  const labels = {
    not_started: "Belum mulai",
    on_track: "On track",
    needs_practice: "Perlu latihan",
    needs_review: "Perlu review"
  };
  return labels[status] || status || "Belum mulai";
}

function formatDate(value) {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString("id-ID", { dateStyle: "medium", timeStyle: "short" });
}

function localJourneySummary() {
  const skillMap = {
    reading: "Reading",
    grammar: "Grammar",
    vocabulary: "Vocabulary",
    writing: "Writing",
    listening: "Listening",
    scenario: "Scenario"
  };
  const skills = Object.entries(skillMap).map(([skill_type, label]) => {
    const average = state.progress[label] || 0;
    return {
      skill_type,
      current_stage: "Foundation",
      current_level: scoreLevel(average),
      average_score: average,
      completed_count: Math.max(0, state.activity.filter((item) => item.module === label).length),
      last_activity_at: "",
      next_action: localNextAction(skill_type),
      status: average > 0 ? (average >= 70 ? "on_track" : "needs_review") : "not_started"
    };
  });
  const scores = skills.map((skill) => skill.average_score);
  const overall = scores.length ? Math.round(scores.reduce((sum, score) => sum + score, 0) / scores.length) : 0;
  const weakest = skills.reduce((lowest, skill) => (skill.average_score < lowest.average_score ? skill : lowest), skills[0]);
  const strongest = skills.reduce((highest, skill) => (skill.average_score > highest.average_score ? skill : highest), skills[0]);
  const summary = {
    journey: {
      current_level: scoreLevel(overall),
      overall_score: overall,
      total_exercises: state.completedExercises || 0,
      learning_streak: state.completedExercises ? 1 : 0,
      weakest_skill: weakest?.skill_type || "grammar",
      strongest_skill: strongest?.skill_type || "reading",
      next_recommended_module: weakest?.skill_type || "grammar",
      last_activity_at: ""
    },
    skills,
    continue_learning: {
      recommended_module: weakest?.skill_type || "grammar",
      next_action: localNextAction(weakest?.skill_type || "grammar"),
      message: `Lanjutkan ${skillLabel(weakest?.skill_type || "grammar")}: ${localNextAction(weakest?.skill_type || "grammar")}`
    },
    daily_plan: [
      { skill_type: weakest?.skill_type || "grammar", task: localNextAction(weakest?.skill_type || "grammar"), duration: "10 menit" },
      { skill_type: "vocabulary", task: "Review 10 kata yang sering salah.", duration: "10 menit" },
      { skill_type: "listening", task: "Short dialogue level 1.", duration: "10 menit" }
    ],
    review_list: { weak_vocabulary: [], weak_grammar_topics: [], due_for_review: [] },
    adaptive_practice: null,
    mentor_message: `Progress lokal tersimpan. Hari ini fokus ke ${skillLabel(weakest?.skill_type || "grammar")}.`
  };
  summary.adaptive_practice = localAdaptivePractice(summary);
  return summary;
}

function localAdaptivePractice(summary) {
  const skillType = summary.journey?.next_recommended_module || "grammar";
  return {
    skill_type: skillType,
    title: `Latihan Adaptif ${skillLabel(skillType)}`,
    level: summary.journey?.current_level || "Beginner 1",
    reason: `${skillLabel(skillType)} dipilih dari progress lokal sebagai fokus paling ringan hari ini.`,
    mentor_message: `Kita fokus ke ${skillLabel(skillType)}. Kerjakan 3 langkah pendek, lalu lanjut ke modul terkait.`,
    practice_prompt: localNextAction(skillType),
    recent_attempts: [],
    next_action: localNextAction(skillType),
    tasks: [
      { title: "Pahami tugas", instruction: localNextAction(skillType) },
      { title: "Kerjakan 10 menit", instruction: "Tulis jawaban singkat dan jangan mengejar sempurna dulu." },
      { title: "Catat kesalahan", instruction: "Tulis satu hal yang masih membingungkan untuk direview." }
    ]
  };
}

function localReadingJourney() {
  const score = state.progress.Reading || 0;
  const completed = state.activity.filter((item) => item.module === "Reading").length;
  const subskills = localReadingSubskills(score, completed);
  const weak = [...subskills].sort((a, b) => a.mastery_score - b.mastery_score).slice(0, 2);
  const strong = [...subskills].sort((a, b) => b.mastery_score - a.mastery_score).slice(0, 2);
  return {
    reading_level: readingScoreLevel(score),
    reading_level_step: Math.max(1, Math.min(10, Math.ceil(score / 10))),
    reading_score: score,
    completed_passages: completed,
    current_stage: "Reading Foundation",
    weak_subskills: weak,
    strong_subskills: strong,
    sub_skill_mastery: subskills,
    last_passage_id: state.selectedReadingLessonId,
    last_activity_at: "",
    next_recommended_action: completed
      ? `Fokus berikutnya: ${weak[0].label}. ${localReadingAction(weak[0].subskill)}`
      : "Mulai dari satu passage pendek. Baca judul, kalimat pertama, lalu cari arti umum bacaan."
  };
}

function localReadingSubskills(score = state.progress.Reading || 0, completed = state.activity.filter((item) => item.module === "Reading").length) {
  const definitions = [
    ["general_meaning", "Arti umum", score],
    ["main_idea", "Main idea", score],
    ["detail_information", "Detail informasi", Math.max(0, score - 5)],
    ["vocabulary_context", "Vocabulary in context", Math.max(0, score - 10)],
    ["reference", "Reference/pronoun", Math.max(0, score - 15)],
    ["sentence_simplification", "Kalimat kompleks", Math.max(0, score - 15)],
    ["inference", "Inference", Math.max(0, score - 20)],
    ["author_purpose", "Author purpose", Math.max(0, score - 20)],
    ["paragraph_function", "Fungsi paragraf", Math.max(0, score - 20)],
    ["ba_case_analysis", "BA case reading", Math.max(0, score - 10)]
  ];
  return definitions.map(([subskill, label, mastery]) => ({
    subskill,
    label,
    mastery_score: mastery,
    attempt_count: completed,
    status: completed ? "developing" : "not_started",
    trainer_available: ["main_idea", "detail_information", "vocabulary_context", "inference", "sentence_simplification"].includes(subskill)
  }));
}

function localReadingTrainerState(subSkill = state.readingTrainer?.selectedSubSkill || "main_idea") {
  const normalized = normalizeReadingSubskill(subSkill);
  return {
    selectedSubSkill: normalized,
    subskills: localReadingSubskills(),
    content: localReadingTrainerContent(normalized),
    selectedAnswer: null,
    feedback: null
  };
}

function localReadingReview() {
  const journey = state.readingJourney || localReadingJourney();
  const weak = journey.weak_subskills?.[0] || localReadingSubskills()[0];
  const recommended = normalizeReadingSubskill(weak?.subskill || "main_idea");
  const lowActivities = state.activity
    .filter((item) => item.module === "Reading" && Number(item.score || 0) < 70)
    .slice(-3)
    .map((item) => ({
      activity_id: item.title || "Reading activity",
      accuracy: item.score || 0,
      feedback: "Skor lokal masih perlu review."
    }));
  return {
    weakness_summary: {
      primary_weakness: weak,
      secondary_weakness: journey.weak_subskills?.[1] || null,
      low_score_passages: lowActivities,
      vocabulary_frequently_misunderstood: recommended === "vocabulary_context" ? [{ word: "clarify", meaning_id: "membuat lebih jelas", count: 1, reason: "Vocabulary context masih perlu dilatih." }] : [],
      bantuan_id_usage: { count: 0, level: "local", message: "Penggunaan Bantuan ID belum tersinkron ke backend." }
    },
    mistake_patterns: [{
      pattern: `Fokus review lokal: ${readingSubskillLabel(recommended)}.`,
      sub_skill: recommended,
      label: readingSubskillLabel(recommended),
      wrong_count: weak?.wrong_count || 0,
      attempt_count: weak?.attempt_count || 0,
      mastery_score: weak?.mastery_score || 0,
      recommendation: localReadingAction(recommended)
    }],
    recommended_sub_skill: recommended,
    recommended_practice: localReadingAction(recommended),
    review_items: [{
      id: `local-review-${recommended}`,
      type: "weak_subskill",
      title: `Latihan ulang ${readingSubskillLabel(recommended)}`,
      sub_skill: recommended,
      priority: 1,
      reason: "Berdasarkan progress lokal Reading.",
      action: localReadingAction(recommended)
    }],
    mentor_message: `Hari ini fokus ke ${readingSubskillLabel(recommended)}. Baca evidence sentence dulu sebelum memilih opsi.`
  };
}

function localReadingTrainerContent(subSkill) {
  const selectedLesson = getLessons().find((lesson) => lesson.id === state.selectedReadingLessonId) || getLessons()[0];
  const fallbackQuestion = selectedLesson.questions.find((question) => normalizeReadingSubskill(question.sub_skill || question.question_type || inferLocalQuestionSubskill(question)) === subSkill) || selectedLesson.questions[0];
  return {
    sub_skill: subSkill,
    label: readingSubskillLabel(subSkill),
    next_action: localReadingAction(subSkill),
    passage: {
      id: selectedLesson.id,
      title: selectedLesson.title,
      text: selectedLesson.passage
    },
    question: {
      ...fallbackQuestion,
      sub_skill: subSkill,
      question_type: subSkill,
      evidence_sentence: selectedLesson.passage,
      answer: fallbackQuestion.answer
    },
    guidance: {
      goal: `Latihan ${readingSubskillLabel(subSkill)}.`,
      tip: localReadingAction(subSkill)
    }
  };
}

function localGuidedReadingState(lesson) {
  const stepsResponse = buildLocalGuidedSteps(lesson);
  return {
    lessonId: lesson.id,
    started: true,
    activeStep: 0,
    steps: stepsResponse.steps,
    passageMap: stepsResponse.passageMap,
    completed: false
  };
}

function buildLocalGuidedSteps(lesson) {
  const sentences = splitLocalSentences(lesson.passage);
  const firstSentence = sentences[0] || lesson.passage;
  const subjectVerb = identifyLocalSubjectVerb(firstSentence);
  const vocab = lesson.vocabulary.map((word) => ({
    word,
    meaning_id: localOneWordMeaning(word),
    context_tip: "Pahami dari kalimat passage, bukan hanya hafalan arti kamus."
  }));
  const passageMap = [{
    paragraph_number: 1,
    text: lesson.passage,
    simple_meaning: localSimpleParagraphMeaning(lesson.passage),
    key_vocabulary: vocab,
    main_point: localMainIdea(lesson),
    possible_reading_skill: "main_idea",
    beginner_tip: "Cari subject, verb utama, lalu hubungan antar ide."
  }];
  return {
    steps: [
      guidedStep("title", 1, "Pahami judul", lesson.title, `Judul ini memberi sinyal bahwa bacaan membahas ${lesson.title.toLowerCase()}.`, "Tebak topik besar sebelum membaca detail."),
      guidedStep("first_sentence", 2, "Baca kalimat pertama", firstSentence, localSimpleParagraphMeaning(firstSentence), "Cari pelaku dan aksi utama."),
      {
        ...guidedStep("subject_verb", 3, "Temukan subject dan main verb", firstSentence, `Subject: ${subjectVerb.subject}. Main verb: ${subjectVerb.mainVerb}.`, "Pegang subject dan verb utama dulu."),
        subject: subjectVerb.subject,
        main_verb: subjectVerb.mainVerb,
        bantuan_context_type: "grammar_sentence"
      },
      {
        ...guidedStep("vocabulary", 4, "Kenali vocabulary penting", lesson.vocabulary.join(", "), "Kata-kata ini membantu memahami passage dan opsi jawaban.", "Pahami arti kata dari konteks."),
        key_vocabulary: vocab,
        bantuan_context_type: "vocabulary_example"
      },
      {
        ...guidedStep("paragraph_map", 5, "Pahami tiap paragraf", lesson.passage, "Baca passage per bagian kecil.", "Catat main point sebelum melihat pertanyaan."),
        paragraph_map: passageMap
      },
      {
        ...guidedStep("main_idea", 6, "Temukan main idea", lesson.passage, localMainIdea(lesson), "Pilih jawaban yang merangkum seluruh passage."),
        main_idea: localMainIdea(lesson),
        bantuan_context_type: "reading_question"
      },
      guidedStep("answer_question", 7, "Siap jawab pertanyaan", lesson.questions[0]?.text || "TOEFL-style question", "Sekarang kamu sudah siap menjawab dengan evidence.", "Jawab pertanyaan normal di bawah panel ini.")
    ],
    passageMap
  };
}

function guidedStep(id, step, title, focusText, explanation, action) {
  return {
    id,
    step,
    title,
    focus_text: focusText,
    simple_explanation: explanation,
    learner_action: action,
    bantuan_context_type: "reading_paragraph"
  };
}

function splitLocalSentences(text) {
  return String(text || "").replaceAll("?", ".").replaceAll("!", ".").split(".").map((item) => item.trim()).filter(Boolean);
}

function identifyLocalSubjectVerb(sentence) {
  const lower = String(sentence || "").toLowerCase();
  if (lower.includes("business analyst") && lower.includes("must")) {
    return { subject: "A business analyst", mainVerb: "must elicit / must ensure" };
  }
  if (lower.includes("analysis helps")) {
    return { subject: "This analysis", mainVerb: "helps" };
  }
  return { subject: "Bagian awal kalimat", mainVerb: "aksi utama setelah subject" };
}

function localSimpleParagraphMeaning(text) {
  const lower = String(text || "").toLowerCase();
  if (lower.includes("stakeholder") && lower.includes("strategy")) {
    return "Bagian ini menjelaskan bahwa kebutuhan stakeholder harus selaras dengan strategi organisasi.";
  }
  if (lower.includes("automation") || lower.includes("process")) {
    return "Bagian ini menjelaskan pentingnya mengevaluasi proses sebelum memilih solusi.";
  }
  return `Bagian ini membahas: ${String(text || "").slice(0, 120)}`;
}

function localMainIdea(lesson) {
  const lower = String(lesson.passage || "").toLowerCase();
  if (lower.includes("stakeholder") && lower.includes("strategy")) {
    return "Main idea: Business Analyst menghubungkan requirement, kebutuhan stakeholder, dan strategi organisasi.";
  }
  if (lower.includes("automation") && lower.includes("process")) {
    return "Main idea: Business Analyst mengevaluasi proses sebelum merekomendasikan automation.";
  }
  return `Main idea: passage ini membahas ${lesson.title.toLowerCase()}.`;
}

function normalizeReadingSubskill(value) {
  const aliases = {
    detail: "detail_information",
    vocabulary: "vocabulary_context",
    sentence_breakdown: "sentence_simplification"
  };
  const key = String(value || "main_idea").toLowerCase().replaceAll("-", "_").replaceAll(" ", "_");
  return aliases[key] || key;
}

function inferLocalQuestionSubskill(question) {
  const text = String(question?.text || "").toLowerCase();
  if (text.includes("main idea")) return "main_idea";
  if (text.includes("word") || text.includes("closest in meaning")) return "vocabulary_context";
  if (text.includes("infer")) return "inference";
  if (text.includes("simplif")) return "sentence_simplification";
  return "detail_information";
}

function readingSubskillLabel(subskill) {
  const labels = {
    general_meaning: "Arti umum",
    main_idea: "Main Idea",
    detail_information: "Detail",
    vocabulary_context: "Vocabulary Context",
    reference: "Reference",
    sentence_simplification: "Sentence Breakdown",
    inference: "Inference",
    author_purpose: "Author Purpose",
    paragraph_function: "Paragraph Function",
    ba_case_analysis: "BA Case"
  };
  return labels[subskill] || String(subskill || "").replaceAll("_", " ");
}

function readingScoreLevel(score) {
  if (score >= 95) return "TOEFL Reading Simulation";
  if (score >= 90) return "BA Case Reading";
  if (score >= 84) return "Author Purpose and Logic";
  if (score >= 78) return "Inference";
  if (score >= 70) return "Complex Sentence Breakdown";
  if (score >= 60) return "Reference and Pronoun";
  if (score >= 50) return "Vocabulary in Context";
  if (score >= 35) return "Find Supporting Details";
  if (score >= 20) return "Find Main Idea";
  return "Understand Simple Meaning";
}

function localReadingAction(subskill) {
  const actions = {
    general_meaning: "Pahami arti umum passage pendek sebelum melihat pilihan jawaban.",
    main_idea: "Pilih jawaban yang merangkum seluruh passage, bukan detail kecil.",
    detail_information: "Cocokkan pertanyaan dengan kalimat bukti di passage.",
    vocabulary_context: "Pahami arti kata dari kalimatnya, bukan hanya arti kamus.",
    inference: "Cari jawaban yang tersirat tetapi tetap didukung evidence passage.",
    sentence_simplification: "Sederhanakan kalimat panjang tanpa mengubah makna utama."
  };
  return actions[subskill] || actions.main_idea;
}

function scoreLevel(score) {
  if (score < 40) return "Beginner 1";
  if (score < 60) return "Beginner 2";
  if (score < 75) return "Intermediate 1";
  if (score < 90) return "Intermediate 2";
  return "Advanced";
}

function localNextAction(skillType) {
  const actions = {
    reading: "Lanjutkan latihan mencari main idea dalam passage Business Analyst.",
    grammar: "Latihan menemukan subject dan verb dalam kalimat panjang.",
    vocabulary: "Ulangi 10 kata yang paling sering salah.",
    writing: "Tulis paragraf pendek dengan struktur subject + verb yang jelas.",
    listening: "Dengarkan short dialogue dan jawab pertanyaan detail.",
    scenario: "Latihan menganalisis kebutuhan stakeholder dalam case BA."
  };
  return actions[skillType] || actions.grammar;
}

function metricTemplate(skill, score) {
  return `
    <div class="progress-card">
      <div>
        <span>${escapeHtml(skill)}</span>
        <strong>${score}%</strong>
      </div>
      <div class="progress-bar"><span style="width:${Math.min(Math.max(score, 0), 100)}%"></span></div>
    </div>
  `;
}

function dashboardAnalyticsCard(label, rawValue, displayValue, note) {
  const numeric = typeof rawValue === "number" ? rawValue : null;
  return `
    <div class="analytics-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(String(displayValue ?? "-"))}</strong>
      ${numeric !== null ? `<div class="progress-bar"><span style="width:${Math.min(Math.max(numeric, 0), 100)}%"></span></div>` : ""}
      <small>${escapeHtml(String(note || ""))}</small>
    </div>
  `;
}

function journeyPanel(moduleName) {
  const journey = journeyDefinitions[moduleName];
  if (!journey) return "";
  const score = state.progress[moduleName] || 0;
  const currentIndex = getJourneyCurrentIndex(journey.steps, score);
  const currentStep = journey.steps[currentIndex];
  const nextStep = journey.steps[Math.min(currentIndex + 1, journey.steps.length - 1)];
  const nextAction = score >= 90 ? currentStep.next : nextStep.next;
  return `
    <section class="journey-panel">
      <div class="journey-summary">
        <div>
          <p class="eyebrow">${moduleName} Journey</p>
          <h3>Sampai mana sekarang: ${currentStep.title}</h3>
          <p>${journey.goal}</p>
        </div>
        <div class="journey-score">
          <span>Progress</span>
          <strong>${score}</strong>
        </div>
      </div>
      <div class="journey-next">
        <strong>Kedepannya harus apa?</strong>
        <p>${nextAction}</p>
      </div>
      <div class="journey-steps">
        ${journey.steps.map((step, index) => journeyStepTemplate(step, index, currentIndex, score)).join("")}
      </div>
    </section>
  `;
}

function journeyStepTemplate(step, index, currentIndex, score) {
  const status = index < currentIndex
    ? "done"
    : index === currentIndex
      ? "current"
      : "upcoming";
  const label = status === "done" ? "Selesai" : status === "current" ? "Sekarang" : "Nanti";
  return `
    <article class="journey-step ${status}">
      <span>${label}</span>
      <strong>${step.title}</strong>
      <p>${step.detail}</p>
    </article>
  `;
}

function getJourneyCurrentIndex(steps, score) {
  let currentIndex = 0;
  steps.forEach((step, index) => {
    if (score >= step.threshold) currentIndex = index;
  });
  return currentIndex;
}

function renderHelp() {
  const lastHelp = state.helpHistory[0];
  document.getElementById("helpView").innerHTML = `
    ${pageHeaderTemplate({
      eyebrow: "Bantuan Bahasa Indonesia",
      title: "Tempel kalimat Inggris, lalu baca penjelasan versi pemula.",
      description: "Fokus pada arti sederhana, kata kunci, pola subject-verb, dan contoh kalimat yang mudah dipahami."
    })}

    <section class="module-grid two">
      <form id="helpForm" class="module-surface form-grid">
        <div class="helper-banner">
          <strong>Cara pakai cepat</strong>
          <p>Tempel kalimat dari Reading, Writing, Listening, atau Scenario. Pilih jenis bantuan, lalu tekan Jelaskan.</p>
        </div>
        <label>
          Kalimat atau kata bahasa Inggris
          <textarea id="helpInput" placeholder="Contoh: A business analyst must elicit clear requirements from stakeholders.">${escapeHtml(state.helpInput || "")}</textarea>
        </label>
        <label>
          Jenis bantuan
          <select id="helpType">
            <option value="simple">Jelaskan sangat sederhana</option>
            <option value="translate">Terjemahkan natural</option>
            <option value="vocabulary">Bedah kosakata penting</option>
            <option value="grammar">Cari subject dan verb</option>
          </select>
        </label>
        <button class="primary-button" type="submit">Jelaskan dalam Bahasa Indonesia</button>
      </form>
      <aside class="module-surface">
        <h3>Hasil Bantuan</h3>
        ${
          lastHelp
            ? helpResultTemplate(lastHelp)
            : emptyStateTemplate("Belum ada hasil", "Coba masukkan satu kalimat bahasa Inggris yang membuat bingung.")
        }
      </aside>
    </section>

    <section class="module-surface">
      <h3>Contekan Basic English</h3>
      <div class="cheat-grid">
        <div><strong>Subject</strong><span>Siapa atau apa yang dibicarakan.</span></div>
        <div><strong>Verb</strong><span>Aksi utama, misalnya elicit, validate, ensure.</span></div>
        <div><strong>Object</strong><span>Yang terkena aksi, misalnya requirements.</span></div>
        <div><strong>Phrase</strong><span>Tambahan informasi, sering membuat kalimat terasa panjang.</span></div>
      </div>
    </section>
  `;

  document.getElementById("helpForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const text = document.getElementById("helpInput").value.trim();
    const type = document.getElementById("helpType").value;
    if (!text) return;
    state.helpInput = text;
    let result = indonesianHelp(text, type);
    if (apiOnline) {
      try {
        result = await apiRequest("/help/indonesian", {
          method: "POST",
          body: { text, type }
        });
      } catch (error) {
        apiOnline = false;
      }
    }
    state.helpHistory.unshift(result);
    state.helpHistory = state.helpHistory.slice(0, 6);
    addActivity("Bantuan ID", text.slice(0, 48), 100);
    saveState();
    renderHelp();
    renderDashboard();
  });
}

function helpResultTemplate(result) {
  return `
    <div class="help-result">
      <p><strong>Arti mudah:</strong> ${result.simpleMeaning}</p>
      <p><strong>Kata kunci:</strong> ${result.keywords.join(", ")}</p>
      <p><strong>Pola kalimat:</strong> ${result.structure}</p>
      <p><strong>Penjelasan:</strong> ${result.explanation}</p>
      <p><strong>Contoh mudah:</strong> ${result.example}</p>
    </div>
  `;
}

function indonesianHelp(text, type) {
  const lowered = text.toLowerCase();
  const keywords = [];
  if (lowered.includes("business analyst")) keywords.push("business analyst = analis bisnis");
  if (lowered.includes("elicit")) keywords.push("elicit = menggali informasi");
  if (lowered.includes("requirement")) keywords.push("requirement = kebutuhan sistem");
  if (lowered.includes("stakeholder")) keywords.push("stakeholder = pihak terkait");
  if (lowered.includes("ensure")) keywords.push("ensure = memastikan");
  if (!keywords.length) keywords.push("Cari kata kerja utama dan kata benda penting.");
  const focus = {
    simple: "Fokus dulu ke makna umum, bukan semua detail grammar.",
    translate: "Terjemahkan natural agar terdengar seperti Bahasa Indonesia sehari-hari.",
    vocabulary: "Pahami kata kerja dan kata benda penting lebih dulu.",
    grammar: "Cari subject sebagai pelaku dan verb sebagai aksi utama."
  };
  return {
    simpleMeaning: "Kalimat ini membahas pekerjaan Business Analyst dalam memahami kebutuhan dan memastikan tujuan bisnis tetap selaras.",
    keywords,
    structure: lowered.includes("must") ? "Subject + must + verb utama + object" : "Subject + verb + informasi tambahan",
    explanation: focus[type] || focus.simple,
    example: "The analyst clarifies requirements. Artinya: analis menjelaskan kebutuhan agar tidak ambigu."
  };
}

function renderContextualHelpButton(module, contextType, text, extraContext = {}) {
  const key = contextualHelpKey(module, contextType, text, extraContext);
  return `
    <span class="context-help-wrap">
      <button
        type="button"
        class="context-help-button"
        data-context-help="true"
        data-help-key="${escapeAttribute(key)}"
        data-help-module="${escapeAttribute(module)}"
        data-help-context-type="${escapeAttribute(contextType)}"
        data-help-text="${escapeAttribute(text)}"
        data-help-extra="${escapeAttribute(JSON.stringify(extraContext || {}))}"
      >Bantuan ID</button>
    </span>
  `;
}

function contextualHelpKey(module, contextType, text, extraContext = {}) {
  return `${module}:${contextType}:v3:${hashText(`${String(text || "")}:${JSON.stringify(extraContext || {})}`)}`;
}

function bindContextualHelpButtons(root = document) {
  root.querySelectorAll("[data-context-help]").forEach((button) => {
    if (button.dataset.boundContextHelp) return;
    button.dataset.boundContextHelp = "true";
    button.addEventListener("click", async (event) => {
      event.preventDefault();
      event.stopPropagation();
      const text = button.dataset.helpText || "";
      const module = button.dataset.helpModule || "general";
      const contextType = button.dataset.helpContextType || "general";
      const extraContext = parseHelpExtra(button.dataset.helpExtra);
      const key = button.dataset.helpKey || contextualHelpKey(module, contextType, text, extraContext);
      const floatingPanel = showContextualHelpPanel({
        title: helpContextLabel(module, contextType),
        body: `<p class="muted">Sedang menjelaskan...</p>`,
        trigger: button
      });
      const cached = state.contextualHelp?.cache?.[key];
      if (cached) {
        floatingPanel.content.innerHTML = renderContextualHelpResult(cached);
        return;
      }

      try {
        const result = await explainTextWithBantuanID(text, module, contextType, extraContext);
        state.contextualHelp.cache[key] = result;
        saveState();
        floatingPanel.content.innerHTML = renderContextualHelpResult(result);
        logContextualHelpUsage(module, contextType, text);
      } catch (error) {
        floatingPanel.content.innerHTML = `<p class="muted">Maaf, Bantuan ID belum dapat memproses teks ini. Coba lagi nanti.</p>`;
      }
    });
  });
}

function showContextualHelpPanel({ title, body, trigger }) {
  const panel = ensureFloatingHelpPanel();
  const content = panel.querySelector("[data-floating-help-content]");
  const titleNode = panel.querySelector("[data-floating-help-title]");
  titleNode.textContent = title || "Bantuan ID";
  content.innerHTML = body || "";
  panel.classList.remove("hidden");
  panel.setAttribute("aria-hidden", "false");
  placeFloatingHelpPanel(panel, trigger);
  return { panel, content };
}

function ensureFloatingHelpPanel() {
  let panel = document.getElementById("contextualHelpFloat");
  if (panel) return panel;

  panel = document.createElement("section");
  panel.id = "contextualHelpFloat";
  panel.className = "floating-help-panel hidden";
  panel.setAttribute("aria-hidden", "true");
  panel.innerHTML = `
    <div class="floating-help-header" data-floating-help-handle>
      <div>
        <small>Bantuan Kontekstual</small>
        <strong data-floating-help-title>Bantuan ID</strong>
      </div>
      <button type="button" class="floating-help-close" data-floating-help-close aria-label="Tutup Bantuan ID">×</button>
    </div>
    <div class="floating-help-content" data-floating-help-content></div>
  `;
  document.body.appendChild(panel);

  panel.querySelector("[data-floating-help-close]").addEventListener("click", () => closeContextualHelpPanel());
  enableFloatingHelpDrag(panel, panel.querySelector("[data-floating-help-handle]"));
  return panel;
}

function closeContextualHelpPanel() {
  const panel = document.getElementById("contextualHelpFloat");
  if (!panel) return;
  panel.classList.add("hidden");
  panel.setAttribute("aria-hidden", "true");
}

function placeFloatingHelpPanel(panel, trigger) {
  if (state.contextualHelp.position.x !== null && state.contextualHelp.position.y !== null) {
    setFloatingHelpPosition(panel, state.contextualHelp.position.x, state.contextualHelp.position.y);
    return;
  }
  const rect = trigger?.getBoundingClientRect();
  const fallbackX = window.innerWidth - 440;
  const fallbackY = 120;
  const x = rect ? rect.left : fallbackX;
  const y = rect ? rect.bottom + 10 : fallbackY;
  setFloatingHelpPosition(panel, x, y);
}

function setFloatingHelpPosition(panel, x, y) {
  const margin = 12;
  const width = panel.offsetWidth || 390;
  const height = panel.offsetHeight || 320;
  const maxX = Math.max(margin, window.innerWidth - width - margin);
  const maxY = Math.max(margin, window.innerHeight - height - margin);
  const nextX = Math.min(Math.max(margin, x), maxX);
  const nextY = Math.min(Math.max(margin, y), maxY);
  panel.style.left = `${nextX}px`;
  panel.style.top = `${nextY}px`;
  state.contextualHelp.position = { x: Math.round(nextX), y: Math.round(nextY) };
}

function enableFloatingHelpDrag(panel, handle) {
  let dragging = false;
  let offsetX = 0;
  let offsetY = 0;

  handle.addEventListener("pointerdown", (event) => {
    if (event.target.closest("[data-floating-help-close]")) return;
    dragging = true;
    const rect = panel.getBoundingClientRect();
    offsetX = event.clientX - rect.left;
    offsetY = event.clientY - rect.top;
    handle.setPointerCapture(event.pointerId);
    panel.classList.add("dragging");
  });

  handle.addEventListener("pointermove", (event) => {
    if (!dragging) return;
    setFloatingHelpPosition(panel, event.clientX - offsetX, event.clientY - offsetY);
  });

  handle.addEventListener("pointerup", (event) => {
    if (!dragging) return;
    dragging = false;
    panel.classList.remove("dragging");
    saveState();
    handle.releasePointerCapture(event.pointerId);
  });
}

function helpContextLabel(module, contextType) {
  const moduleLabels = {
    reading: "Reading",
    grammar: "Grammar",
    vocabulary: "Vocabulary",
    tutor: "AI Tutor",
    writing: "Writing",
    listening: "Listening",
    scenario: "Scenario BA"
  };
  const cleanedContext = String(contextType || "content").replaceAll("_", " ");
  return `${moduleLabels[module] || "Bantuan ID"} · ${cleanedContext}`;
}

async function explainTextWithBantuanID(text, module, contextType, extraContext = {}) {
  if (apiOnline) {
    try {
      return await apiRequest("/ai/contextual-help", {
        method: "POST",
        body: {
          text,
          module,
          context_type: contextType,
          user_level: "beginner",
          extra_context: {
            user_id: state.user?.id || "default-user",
            ...(extraContext || {})
          }
        }
      });
    } catch (error) {
      apiOnline = false;
    }
  }
  return localContextualHelp(text, module, contextType, extraContext);
}

function parseHelpExtra(value) {
  try {
    return value ? JSON.parse(value) : {};
  } catch (error) {
    return {};
  }
}

function localContextualHelp(text, module, contextType, extraContext = {}) {
  const legacy = indonesianHelp(text, module === "grammar" ? "grammar" : "simple");
  const directMeaning = localDirectMeaning(text);
  const questionLike = isQuestionLike(text);
  return {
    text,
    module,
    context_type: contextType,
    explanation_id: contextualHelpKey(module, contextType, text, extraContext),
    source: "local",
    explanation: {
      simple_meaning_id: directMeaning || localBasicMeaning(text),
      sentence_structure: questionLike ? "Ini adalah pertanyaan. Fokus pada apa yang ditanyakan." : legacy.structure,
      subject: questionLike ? "" : (text.toLowerCase().includes("business analyst") ? "A business analyst" : ""),
      verb: questionLike ? "" : (text.toLowerCase().includes("must") ? "must + verb utama" : ""),
      object_or_complement: questionLike ? "" : "",
      grammar_pattern: questionLike ? "Question" : legacy.structure,
      important_vocabulary: legacy.keywords.map((item) => {
        const [word, meaning] = item.split(" = ");
        return {
          word,
          meaning_id: meaning || item,
          one_word_meaning_id: localOneWordMeaning(word),
          contextual_meaning_id: `Dalam kalimat ini, ${word} perlu dipahami sesuai konteks TOEFL atau Business Analyst.`
        };
      }),
      beginner_explanation: questionLike ? "Baca kata tanya seperti what atau which, lalu jawab hal yang diminta." : legacy.explanation,
      tips: questionLike ? "Jangan bedah seperti kalimat biasa dulu. Cari maksud pertanyaannya." : "Baca pelan, cari subject dan verb, lalu baru pahami detail tambahan."
    }
  };
}

function renderContextualHelpResult(result) {
  const explanation = result.explanation || {};
  const vocabulary = explanation.important_vocabulary || [];
  const keyVocabulary = explanation.key_vocabulary || [];
  const combinedVocabulary = vocabulary.length ? vocabulary : keyVocabulary;
  const vocabularyHtml = combinedVocabulary.length
    ? `
      <ul class="context-vocab-list">
        ${combinedVocabulary.map((item) => `
          <li>
            <strong>${escapeHtml(item.word || "")}</strong>
            <span><b>Arti singkat:</b> ${escapeHtml(item.one_word_meaning_id || localOneWordMeaning(item.word || ""))}</span>
            <span><b>Arti umum:</b> ${escapeHtml(item.meaning_id || "")}</span>
            <span><b>Dalam contoh ini:</b> ${escapeHtml(item.contextual_meaning_id || "Artinya mengikuti konteks kalimat yang sedang dibaca.")}</span>
          </li>
        `).join("")}
      </ul>
    `
    : `<p class="muted">Belum ada kosakata khusus yang terdeteksi.</p>`;
  const extras = [
    ["Maksud pertanyaan", explanation.question_intent],
    ["Yang harus dicari", explanation.what_to_find],
    ["Cara menjawab", explanation.how_to_answer],
    ["Jebakan yang harus dihindari", explanation.trap_to_avoid],
    ["Maksud opsi", explanation.option_meaning],
    ["Hubungan dengan konteks", explanation.relation_to_context],
    ["Kemungkinan jawaban", explanation.likely_correctness_hint],
    ["Alasan", explanation.why],
    ["Kata kunci", explanation.key_words],
    ["Pesan utama", explanation.main_message],
    ["Poin penting", explanation.key_points],
    ["Fokus grammar", explanation.grammar_focus],
    ["Tips reading", explanation.reading_tip],
    ["Arti kata", explanation.word_meaning_id],
    ["Arti satu kata", explanation.word_one_word_meaning_id],
    ["Arti dalam contoh kalimat", explanation.word_contextual_meaning_id],
    ["Jenis kata", explanation.word_class],
    ["Konteks BA", explanation.ba_context],
    ["Cara mengingat", explanation.memory_tip],
    ["Contoh kalimat", explanation.example_sentence],
    ["Makna BA / TOEFL", explanation.ba_toefl_context],
    ["Main verb", explanation.main_verb],
    ["Modifier", explanation.modifier],
    ["Warning pemula", explanation.beginner_warning],
    ["Kalimat sederhana", explanation.simplified_sentence],
    ["Maksud kalimat", explanation.writing_meaning],
    ["Feedback clarity", explanation.clarity_feedback],
    ["Masalah grammar", explanation.grammar_issue],
    ["Versi lebih baik", explanation.better_sentence || explanation.improved_sentence],
    ["Alasan perbaikan", explanation.improvement_reason || explanation.why_better],
    ["Tips writing", explanation.writing_tip],
    ["Fokus listening", explanation.listening_focus],
    ["Kata kunci listening", explanation.listening_keywords || explanation.keywords_to_hear],
    ["Maksud pembicara", explanation.speaker_intent],
    ["Tips listening", explanation.listening_tip],
    ["Strategi menjawab", explanation.answer_strategy],
    ["Masalah bisnis", explanation.business_problem],
    ["Stakeholder need", explanation.stakeholder_need],
    ["Tindakan BA yang disarankan", explanation.suggested_ba_action],
    ["Petunjuk memilih jawaban", explanation.answer_hint],
    ["Aksi belajar", explanation.learner_action],
    ["Tips pemula", explanation.beginner_tip],
    ["Penjelasan konteks", explanation.context_explanation]
  ]
    .filter(([, value]) => value)
    .map(([label, value]) => `<p><strong>${label}:</strong> ${renderContextValue(value)}</p>`)
    .join("");
  const directMeaning = explanation.direct_meaning_id || explanation.simple_meaning_id || "Teks ini perlu dipahami dari konteksnya.";

  return `
    <div class="context-help-card">
      <strong>Bantuan ID</strong>
      <p><strong>Arti langsung:</strong> ${escapeHtml(directMeaning)}</p>
      ${contextHelpLine("Struktur kalimat", explanation.sentence_structure || explanation.grammar_pattern)}
      ${contextHelpLine("Subject", explanation.subject)}
      ${contextHelpLine("Verb", explanation.verb || explanation.main_verb)}
      ${contextHelpLine("Object/Complement", explanation.object_or_complement)}
      ${combinedVocabulary.length ? `<div><strong>Kosakata penting:</strong>${vocabularyHtml}</div>` : ""}
      <p><strong>Penjelasan konteks:</strong> ${escapeHtml(explanation.beginner_explanation || "Pahami maksud umum dulu sebelum detail grammar.")}</p>
      <p><strong>Tips memahami:</strong> ${escapeHtml(explanation.tips || "Cari kata kunci, lalu cocokkan dengan konteks modul.")}</p>
      ${extras}
      <small class="muted">Sumber: ${escapeHtml(result.source || "mock")}</small>
    </div>
  `;
}

function contextHelpLine(label, value) {
  if (!value) return "";
  return `<p><strong>${label}:</strong> ${escapeHtml(value)}</p>`;
}

function renderContextValue(value) {
  if (Array.isArray(value)) {
    return value.map((item) => {
      if (typeof item === "object" && item !== null) {
        return escapeHtml(`${item.word || item.label || ""}${item.meaning_id ? ` = ${item.meaning_id}` : ""}`);
      }
      return escapeHtml(item);
    }).join(", ");
  }
  if (typeof value === "object" && value !== null) {
    return escapeHtml(JSON.stringify(value));
  }
  return escapeHtml(value);
}

function isQuestionLike(text) {
  const lowered = String(text || "").trim().toLowerCase();
  return lowered.endsWith("?") || ["what ", "which ", "why ", "how ", "when ", "where ", "who ", "can "].some((prefix) => lowered.startsWith(prefix));
}

function localDirectMeaning(text) {
  const key = String(text || "").trim().toLowerCase().replace(/[.?]$/, "").replace(/\s+/g, " ");
  const meanings = {
    "what business outcome should this solution improve": "Pertanyaan ini berarti: hasil bisnis apa yang harus diperbaiki oleh solusi ini?",
    "which ba action best supports alignment": "Pertanyaan ini berarti: tindakan Business Analyst mana yang paling membantu menyelaraskan tujuan atau kebutuhan stakeholder?",
    "what is the best first question": "Pertanyaan ini berarti: pertanyaan pertama apa yang paling tepat untuk diajukan?",
    "what is the main purpose of the conversation": "Pertanyaan ini berarti: apa tujuan utama dari percakapan tersebut?",
    "which color should the mobile app use": "Pilihan ini berarti: menanyakan warna apa yang harus dipakai aplikasi mobile.",
    "which developer is available this week": "Pilihan ini berarti: menanyakan developer mana yang tersedia minggu ini.",
    "can we skip user research": "Pilihan ini berarti: menanyakan apakah riset user bisa dilewati."
  };
  return meanings[key] || "";
}

function localBasicMeaning(text) {
  const cleaned = String(text || "").trim();
  if (!cleaned) return "Teks kosong, belum ada yang bisa dijelaskan.";
  return `Maksud teks ini: ${cleaned}`;
}

function localOneWordMeaning(word) {
  const map = {
    "elicit": "menggali",
    "requirement": "kebutuhan",
    "requirements": "kebutuhan",
    "stakeholder": "pemangku-kepentingan",
    "stakeholders": "pemangku-kepentingan",
    "maintain": "menjaga",
    "approval": "persetujuan",
    "workflow": "alur",
    "delay": "tertunda",
    "delays": "keterlambatan",
    "purpose": "tujuan",
    "conversation": "percakapan"
  };
  return map[String(word || "").toLowerCase()] || "konteks";
}

function logContextualHelpUsage(module, contextType, text) {
  addActivity("Bantuan ID", `${module}: ${String(text || "").slice(0, 42)}`, 100);
  saveState();
}

function renderReading() {
  const allLessons = getLessons();
  const selectedLesson = allLessons.find((lesson) => lesson.id === state.selectedReadingLessonId) || allLessons[0];
  const activeMode = normalizeReadingMode(state.readingMode);
  state.readingMode = activeMode;
  document.getElementById("readingView").innerHTML = `
    ${readingJourneyLabTop()}
    ${readingHero(selectedLesson)}
    ${readingModeTabs(activeMode)}
    <section class="reading-workspace">
      ${readingActivePanel(activeMode, selectedLesson, allLessons)}
    </section>
  `;

  document.getElementById("readingHelpButton")?.addEventListener("click", () => {
    openHelpWith(selectedLesson.passage);
  });

  document.querySelectorAll("[data-reading-mode]").forEach((button) => {
    button.addEventListener("click", () => {
      state.readingMode = normalizeReadingMode(button.dataset.readingMode);
      saveState();
      renderReading();
    });
  });

  document.querySelectorAll("[data-lesson]").forEach((button) => {
    button.addEventListener("click", () => {
      state.selectedReadingLessonId = button.dataset.lesson;
      state.guidedReading = structuredClone(defaultState.guidedReading);
      saveState();
      renderReading();
    });
  });

  document.querySelectorAll("[data-reading-question]").forEach((button) => {
    button.addEventListener("click", () => {
      state.readingAnswers[button.dataset.readingQuestion] = Number(button.dataset.option);
      renderReading();
    });
  });

  document.getElementById("submitReading")?.addEventListener("click", async () => {
    let score = scoreReading(selectedLesson);
    let details = [];
    let answerReviews = localReadingAnswerReviews(selectedLesson);
    let readingResponse = null;
    if (apiOnline) {
      try {
        readingResponse = await apiRequest("/reading/submit-answer", {
          method: "POST",
          body: {
            user_id: state.user?.id || "default-user",
            lessonId: selectedLesson.id,
            answers: state.readingAnswers
          }
        });
        score = readingResponse.score;
        details = readingResponse.details || [];
        answerReviews = readingResponse.answer_reviews || answerReviews;
      } catch (error) {
        apiOnline = false;
      }
    }
    state.progress.Reading = Math.max(state.progress.Reading, score);
    state.completedExercises += 1;
    addActivity("Reading", selectedLesson.title, score);
    if (readingResponse?.reading_journey_update) {
      state.readingJourney = readingResponse.reading_journey_update;
    }
    state.readingAnswerReviews = answerReviews;
    saveState();
    await refreshIntegratedJourney();
    await refreshReadingJourney();
    document.getElementById("readingResult").innerHTML = resultTemplate(
      score >= 70 ? "success" : "warning",
      `Skor Reading: ${score}`,
      score >= 70
        ? "Bagus. Kamu sudah menangkap main idea dan detail penting."
        : "Ulangi passage dan perhatikan kata kunci seperti analyst, stakeholder, dan outcome."
    ) + (details.length ? `<div class="lesson-list compact-list">${details.map((detail) => `<p class="muted">${detail.questionId}: ${detail.isCorrect ? "Correct" : "Review"} - ${detail.explanation}</p>`).join("")}</div>` : "")
      + readingAnswerReviewPanel(answerReviews, selectedLesson);
    bindContextualHelpButtons(document.getElementById("readingResult"));
    renderDashboard();
    renderJourney();
  });
  document.getElementById("continueReadingButton")?.addEventListener("click", () => {
    state.readingMode = "practice";
    saveState();
    renderReading();
    document.getElementById("readingPracticePanel")?.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  document.getElementById("retryWeakReadingSkillButton")?.addEventListener("click", async () => {
    const subSkill = state.readingReview?.recommended_sub_skill || "main_idea";
    if (apiOnline) {
      await refreshReadingTrainer(subSkill);
    } else {
      state.readingTrainer = localReadingTrainerState(subSkill);
    }
    state.readingMode = "trainer";
    saveState();
    renderReading();
    document.getElementById("readingTrainerPanel")?.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  document.querySelectorAll("[data-simulation-mode]").forEach((button) => {
    button.addEventListener("click", () => {
      state.readingSimulation.mode = button.dataset.simulationMode;
      saveState();
      renderReading();
    });
  });

  document.getElementById("startReadingSimulationButton")?.addEventListener("click", async () => {
    await startReadingSimulation();
  });

  document.querySelectorAll("[data-simulation-question]").forEach((button) => {
    button.addEventListener("click", () => {
      state.readingSimulation.answers[button.dataset.simulationQuestion] = Number(button.dataset.simulationOption);
      saveState();
      renderReading();
    });
  });

  document.getElementById("submitReadingSimulationButton")?.addEventListener("click", async () => {
    await submitReadingSimulation();
  });

  document.getElementById("startGuidedReadingButton")?.addEventListener("click", async () => {
    await startGuidedReading(selectedLesson);
  });

  document.getElementById("nextGuidedReadingStepButton")?.addEventListener("click", async () => {
    await nextGuidedReadingStep(selectedLesson);
  });

  document.querySelectorAll("[data-reading-trainer-subskill]").forEach((button) => {
    button.addEventListener("click", async () => {
      const subSkill = button.dataset.readingTrainerSubskill;
      state.readingTrainer = { ...(state.readingTrainer || {}), selectedSubSkill: subSkill, selectedAnswer: null, feedback: null };
      if (apiOnline) {
        await refreshReadingTrainer(subSkill);
      } else {
        state.readingTrainer = localReadingTrainerState(subSkill);
      }
      saveState();
      renderReading();
    });
  });

  document.querySelectorAll("[data-reading-trainer-answer]").forEach((button) => {
    button.addEventListener("click", async () => {
      const selected = Number(button.dataset.readingTrainerAnswer);
      await submitReadingTrainerAnswer(selected);
    });
  });
  bindContextualHelpButtons(document.getElementById("readingView"));
  setupReadingSimulationTimer();
}

function normalizeReadingMode(mode) {
  const allowed = ["overview", "practice", "guided", "trainer", "review", "simulation"];
  return allowed.includes(mode) ? mode : "overview";
}

function readingJourneyLabTop() {
  const journey = state.readingJourney || localReadingJourney();
  const strongest = journey.strong_subskills?.[0];
  const weakest = journey.weak_subskills?.[0];
  const score = Math.round(journey.reading_score || 0);
  return `
    <section class="reading-top-grid">
      <article class="reading-journey-lab-card">
        <div>
          <p class="eyebrow">Reading Journey Lab</p>
          <h2>${escapeHtml(journey.reading_level || "Understand Simple Meaning")}</h2>
          <p>${escapeHtml(journey.next_recommended_action || "Mulai dari memahami arti umum passage.")}</p>
        </div>
        <div class="reading-journey-mini-grid">
          ${readingMiniStat("Completed", `${journey.completed_passages || 0} passage`)}
          ${readingMiniStat("Skill kuat", strongest?.label || "Belum ada")}
          ${readingMiniStat("Skill lemah", weakest?.label || "Belum ada")}
          ${readingMiniStat("Aktivitas terakhir", journey.last_activity_at ? formatDate(journey.last_activity_at) : "Belum ada")}
        </div>
      </article>
      <article class="reading-score-overview-card">
        <span>Reading Score</span>
        <strong>${score}</strong>
        ${readingPercentBar(score)}
        <small>${escapeHtml(journey.reading_level || "Level awal")}</small>
        <button class="primary-button" type="button" data-reading-mode="practice">Lanjutkan Reading</button>
      </article>
    </section>
  `;
}

function readingHero(lesson) {
  const journey = state.readingJourney || localReadingJourney();
  const review = state.readingReview || localReadingReview();
  const weakSkill = review.recommended_sub_skill || journey.weak_subskills?.[0]?.subskill || "main_idea";
  return `
    <header class="reading-hero">
      <div class="reading-hero-copy">
        <p class="eyebrow">Reading Lab</p>
        <h2>${escapeHtml(lesson.title)}</h2>
        <p class="reading-passage-preview">
          ${escapeHtml(lesson.passage)}
          ${renderContextualHelpButton("reading", "reading_passage", lesson.passage, readingHelpContext(lesson))}
        </p>
        <div class="pill-row">
          <span class="pill">${escapeHtml(lesson.level || "Foundation")}</span>
          <span class="pill">${escapeHtml(lesson.context || "Business Analyst")}</span>
          <span class="pill">${escapeHtml(readingSubskillLabel(weakSkill))} perlu fokus</span>
        </div>
      </div>
      <div class="reading-hero-side">
        <div class="reading-hero-actions">
          <button class="primary-button" type="button" data-reading-mode="practice">Kerjakan Soal</button>
          <button class="ghost-button" type="button" data-reading-mode="guided">Guided Reading</button>
          <button id="readingHelpButton" class="ghost-button" type="button">Jelaskan bacaan</button>
        </div>
      </div>
    </header>
  `;
}

function readingModeTabs(activeMode) {
  const guidanceTabs = [
    ["overview", "Overview", "Ringkasan"],
    ["guided", "Guided", "Langkah pelan"],
    ["trainer", "Trainer", "Sub-skill"],
    ["review", "Review", "Pola salah"]
  ];
  const testingTabs = [
    ["practice", "Practice", "Soal TOEFL"],
    ["simulation", "Simulation", "Timer"]
  ];
  return `
    <nav class="reading-mode-shell" aria-label="Reading modes">
      <section class="reading-mode-group guidance">
        <div class="reading-mode-group-label">
          <span>Guidance Lab</span>
          <small>Belajar pelan, review, dan perbaiki skill</small>
        </div>
        <div class="reading-mode-tabs guidance-tabs">
          ${guidanceTabs.map(([mode, label, hint]) => readingModeTabButton(mode, label, hint, activeMode, "guidance")).join("")}
        </div>
      </section>
      <section class="reading-mode-group testing">
        <div class="reading-mode-group-label">
          <span>Testing Zone</span>
          <small>Uji pemahaman dengan soal dan timer</small>
        </div>
        <div class="reading-mode-tabs testing-tabs">
          ${testingTabs.map(([mode, label, hint]) => readingModeTabButton(mode, label, hint, activeMode, "testing")).join("")}
        </div>
      </section>
    </nav>
  `;
}

function readingModeTabButton(mode, label, hint, activeMode, group) {
  return `
    <button class="reading-mode-tab ${group} ${activeMode === mode ? "active" : ""}" type="button" data-reading-mode="${mode}">
      <strong>${label}</strong>
      <span>${hint}</span>
    </button>
  `;
}

function readingActivePanel(activeMode, selectedLesson, allLessons) {
  if (activeMode === "practice") return readingPracticeLayout(selectedLesson, allLessons);
  if (activeMode === "guided") return readingGuidedLayout(selectedLesson, allLessons);
  if (activeMode === "trainer") return `${readingSubskillProgress()}${readingTrainerPanel()}`;
  if (activeMode === "review") return readingReviewPanel();
  if (activeMode === "simulation") return readingSimulationPanel();
  return readingOverviewLayout(selectedLesson, allLessons);
}

function readingOverviewLayout(selectedLesson, allLessons) {
  return `
    <section class="reading-overview-grid">
      <div class="reading-overview-main">
        ${readingSubskillProgress()}
        ${readingNextStepsPanel()}
      </div>
      ${readingLessonSidebar(allLessons, selectedLesson)}
    </section>
  `;
}

function readingNextStepsPanel() {
  return `
    <section class="panel reading-next-steps">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Alur belajar Reading</p>
          <h3>Pilih mode sesuai kebutuhan hari ini</h3>
          <p>Mulai dari Guided kalau masih bingung, Practice untuk soal normal, Trainer untuk skill lemah, atau Simulation untuk latihan timer.</p>
        </div>
      </div>
      <div class="reading-action-grid">
        <button class="metric ghost-button" type="button" data-reading-mode="guided">
          <span class="muted">Step-by-step</span>
          <strong class="metric-word">Guided Reading</strong>
          <small>Pahami judul, subject/verb, vocabulary, dan main idea.</small>
        </button>
        <button class="metric ghost-button" type="button" data-reading-mode="practice">
          <span class="muted">TOEFL questions</span>
          <strong class="metric-word">Practice</strong>
          <small>Kerjakan soal dari passage aktif dan lihat review jawaban.</small>
        </button>
        <button class="metric ghost-button" type="button" data-reading-mode="trainer">
          <span class="muted">Skill lemah</span>
          <strong class="metric-word">Trainer</strong>
          <small>Latihan main idea, detail, inference, vocabulary, dan sentence breakdown.</small>
        </button>
        <button class="metric ghost-button" type="button" data-reading-mode="simulation">
          <span class="muted">Timed mode</span>
          <strong class="metric-word">Simulation</strong>
          <small>Latihan Reading dengan timer dan final report.</small>
        </button>
      </div>
    </section>
  `;
}

function readingPracticeLayout(selectedLesson, allLessons) {
  return `
    <section class="reading-practice-layout" id="readingPracticePanel">
      <div class="panel reading-practice-panel">
        ${readingPracticeGuide()}
        <div class="section-heading">
          <div>
            <p class="eyebrow">TOEFL-style Questions</p>
            <h3>Jawab berdasarkan passage aktif</h3>
            <p>Pilih opsi yang paling didukung oleh passage. Setelah submit, baca Answer Review untuk melihat bukti dan alasan.</p>
          </div>
          <span class="pill">${selectedLesson.questions.length} soal</span>
        </div>
        ${selectedLesson.questions.map((question, index) => readingQuestionTemplate(question, index, selectedLesson)).join("")}
        <div class="reading-submit-bar">
          <span>${selectedReadingAnswerCount(selectedLesson)}/${selectedLesson.questions.length} soal dijawab</span>
          <button id="submitReading" class="primary-button" type="button">Submit Reading</button>
        </div>
        <div id="readingResult"></div>
      </div>
      ${readingLessonSidebar(allLessons, selectedLesson)}
    </section>
  `;
}

function readingPracticeGuide() {
  const steps = [
    ["1", "Baca judul", "Tangkap topik sebelum melihat opsi."],
    ["2", "Cari main idea", "Pilih jawaban yang merangkum passage."],
    ["3", "Cek evidence", "Cocokkan opsi dengan kalimat bukti."]
  ];
  return `
    <div class="reading-practice-guide">
      <div>
        <span class="reading-badge">Cara cepat</span>
        <h3>Cara mengerjakan Reading</h3>
      </div>
      <div class="reading-guide-steps">
        ${steps.map(([number, title, text]) => `
          <article>
            <strong>${number}</strong>
            <div>
              <b>${title}</b>
              <p>${text}</p>
            </div>
          </article>
        `).join("")}
      </div>
    </div>
  `;
}

function selectedReadingAnswerCount(lesson) {
  return lesson.questions.filter((question) => state.readingAnswers[question.id] !== undefined).length;
}

function readingGuidedLayout(selectedLesson, allLessons) {
  return `
    <section class="reading-practice-layout">
      <div>${guidedReadingPanel(selectedLesson)}</div>
      ${readingLessonSidebar(allLessons, selectedLesson)}
    </section>
  `;
}

function readingLessonSidebar(allLessons, selectedLesson) {
  return `
    <aside class="panel reading-resource-panel">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Passage aktif</p>
          <h3>${escapeHtml(selectedLesson.title)}</h3>
        </div>
      </div>
      <div class="lesson-list compact-list reading-lesson-list">
        ${allLessons.map((lesson) => `
          <button class="ghost-button ${lesson.id === selectedLesson.id ? "selected-control" : ""}" type="button" data-lesson="${lesson.id}">
            ${escapeHtml(lesson.title)}
          </button>
        `).join("")}
      </div>
      <div class="reading-resource-card">
        <h3>Grammar Insight</h3>
        <p>${escapeHtml(selectedLesson.grammar || "")} ${renderContextualHelpButton("grammar", "grammar_explanation", selectedLesson.grammar || "")}</p>
      </div>
      <div class="reading-resource-card">
        <h3>Vocabulary</h3>
        <div class="pill-row">
          ${(selectedLesson.vocabulary || []).map((word) => `<span class="pill">${escapeHtml(word)} ${renderContextualHelpButton("vocabulary", "vocabulary_word", word)}</span>`).join("")}
        </div>
      </div>
    </aside>
  `;
}

function readingJourneySummary() {
  const journey = state.readingJourney || localReadingJourney();
  const strongest = journey.strong_subskills?.[0];
  const weakest = journey.weak_subskills?.[0];
  return `
    <section class="panel reading-journey-card">
      <div class="journey-summary">
        <div>
          <p class="eyebrow">Reading Journey Foundation</p>
          <h3>${escapeHtml(journey.reading_level || "Understand Simple Meaning")}</h3>
          <p>${escapeHtml(journey.next_recommended_action || "Mulai dari memahami arti umum passage.")}</p>
        </div>
        <div class="journey-score">
          <span>Reading Score</span>
          <strong>${Math.round(journey.reading_score || 0)}</strong>
        </div>
      </div>
      <div class="drill-result-grid">
        <div class="metric">
          <span class="muted">Completed Passages</span>
          <strong>${journey.completed_passages || 0}</strong>
          <small>Passage yang sudah disubmit</small>
        </div>
        <div class="metric">
          <span class="muted">Strongest Sub-skill</span>
          <strong class="metric-word">${escapeHtml(strongest?.label || "Belum ada")}</strong>
          <small>${Math.round(strongest?.mastery_score || 0)}%</small>
        </div>
        <div class="metric">
          <span class="muted">Weakest Sub-skill</span>
          <strong class="metric-word">${escapeHtml(weakest?.label || "Belum ada")}</strong>
          <small>${Math.round(weakest?.mastery_score || 0)}%</small>
        </div>
        <div class="metric">
          <span class="muted">Last Passage</span>
          <strong class="metric-word">${escapeHtml(journey.last_passage_id || state.selectedReadingLessonId || "-")}</strong>
          <small>${journey.last_activity_at ? formatDate(journey.last_activity_at) : "Belum ada aktivitas backend"}</small>
        </div>
      </div>
      <div class="reading-focus-banner">
        <div>
          <strong>Fokus berikutnya</strong>
          <p>${escapeHtml(journey.next_recommended_action || "Kerjakan satu passage pendek dan cek Answer Review setelah submit.")}</p>
        </div>
        <button id="continueReadingButton" class="primary-button" type="button">Lanjutkan Reading</button>
      </div>
    </section>
  `;
}

function readingReviewPanel() {
  const review = state.readingReview || localReadingReview();
  const weakness = review.weakness_summary || {};
  const primary = weakness.primary_weakness || {};
  const secondary = weakness.secondary_weakness || {};
  const patterns = review.mistake_patterns || [];
  const queue = review.review_items || [];
  const lowPassages = weakness.low_score_passages || [];
  const vocab = weakness.vocabulary_frequently_misunderstood || [];
  return `
    <section class="panel reading-review-panel">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Reading Review</p>
          <h3>Laporan kelemahan Reading</h3>
          <p>${escapeHtml(review.mentor_message || "Review membantu kamu tahu pola salah dan latihan berikutnya.")}</p>
        </div>
        <button id="retryWeakReadingSkillButton" class="primary-button" type="button">Latihan Ulang Skill Lemah</button>
      </div>
      <div class="reading-review-hero">
        <div>
          <span class="reading-badge warning">Prioritas review</span>
          <h3>${escapeHtml(primary.label || readingSubskillLabel(review.recommended_sub_skill))}</h3>
          <p>${escapeHtml(review.recommended_practice || "Latihan ulang skill terlemah dengan passage pendek.")}</p>
        </div>
        <div class="reading-review-stats">
          ${readingMiniStat("Mastery utama", `${Math.round(primary.mastery_score || 0)}%`)}
          ${readingMiniStat("Weakness kedua", secondary.label || "Belum ada")}
          ${readingMiniStat("Bantuan ID", weakness.bantuan_id_usage?.level || "normal")}
        </div>
      </div>
      <div class="reading-two-column">
        <div class="reading-soft-card">
          <h3>Mistake pattern</h3>
          <div class="reading-list-stack">
            ${patterns.length ? patterns.map((item) => `
              <article class="reading-list-item">
                <strong>${escapeHtml(item.label || readingSubskillLabel(item.sub_skill))}</strong>
                <p>${escapeHtml(item.pattern || "")}</p>
                <small>${escapeHtml(item.recommendation || "")}</small>
              </article>
            `).join("") : `<p class="muted">Belum ada pola salah yang cukup kuat.</p>`}
          </div>
        </div>
        <div class="reading-soft-card">
          <h3>Review queue</h3>
          <div class="reading-list-stack">
            ${queue.length ? queue.map((item) => `
              <article class="reading-list-item">
                <strong>${escapeHtml(item.title || "")}</strong>
                <p>${escapeHtml(item.reason || "")}</p>
                <small>${escapeHtml(item.action || "")}</small>
              </article>
            `).join("") : `<p class="muted">Belum ada item review.</p>`}
          </div>
        </div>
      </div>
      ${(lowPassages.length || vocab.length) ? `
        <div class="reading-two-column">
          <div class="reading-soft-card">
            <h3>Passage skor rendah</h3>
            <div class="reading-list-stack">
              ${lowPassages.length ? lowPassages.map((item) => `
                <article class="reading-list-item">
                  <strong>${escapeHtml(item.activity_id || "")}</strong>
                  <p>Skor ${Math.round(item.accuracy || 0)}% · ${escapeHtml(readingAttemptFeedbackSummary(item.feedback))}</p>
                </article>
              `).join("") : `<p class="muted">Belum ada passage rendah.</p>`}
            </div>
          </div>
          <div class="reading-soft-card">
            <h3>Vocabulary perlu review</h3>
            <div class="reading-list-stack">
              ${vocab.length ? vocab.map((item) => `
                <article class="reading-list-item">
                  <strong>${escapeHtml(item.word || "")}: ${escapeHtml(item.meaning_id || "")}</strong>
                  <p>${escapeHtml(item.reason || "")}</p>
                </article>
              `).join("") : `<p class="muted">Belum ada vocabulary Reading yang sering salah.</p>`}
            </div>
          </div>
        </div>
      ` : ""}
    </section>
  `;
}

function readingSimulationPanel() {
  const simulation = state.readingSimulation || structuredClone(defaultState.readingSimulation);
  const session = simulation.session;
  const result = simulation.result;
  const modes = [
    ["short", "Short", "1 passage · 5 soal · 10 menit"],
    ["medium", "Medium", "2 passage · 10 soal · 20 menit"],
    ["full", "Full Practice", "3 passage · 15 soal · 30 menit"]
  ];
  const answered = session ? Object.keys(simulation.answers || {}).length : 0;
  const totalQuestions = session?.question_count || 0;
  return `
    <section class="panel reading-simulation-panel" id="readingSimulationPanel">
      <div class="section-heading">
        <div>
          <p class="eyebrow">TOEFL Reading Simulation</p>
          <h3>Latihan Reading dengan timer</h3>
          <p>Mode simulasi melatih fokus seperti TOEFL. Bantuan ID dibatasi supaya hasil lebih mirip ujian.</p>
        </div>
        ${session && !result ? `
          <div class="reading-timer-card">
            <span>Sisa waktu</span>
            <strong id="readingSimulationTimer">${formatSimulationTime(remainingSimulationSeconds())}</strong>
            <small>${answered}/${totalQuestions} soal dijawab</small>
          </div>
        ` : ""}
      </div>
      <div class="reading-simulation-modes">
        ${modes.map(([mode, label, description]) => `
          <button class="reading-mode-card ${simulation.mode === mode ? "selected-control" : ""}" type="button" data-simulation-mode="${mode}">
            <span>${label}</span>
            <strong>${description}</strong>
          </button>
        `).join("")}
      </div>
      <div class="reading-note">
        <strong>Catatan simulasi</strong>
        <p>Bantuan ID tidak ditampilkan di dalam soal simulasi. Setelah submit, fokus ke hasil prioritas, sub-skill lemah, dan Answer Review.</p>
      </div>
      ${!session ? `
        <button id="startReadingSimulationButton" class="primary-button" type="button">Mulai Simulasi</button>
      ` : ""}
      ${session && !result ? readingSimulationSessionTemplate(session, simulation.answers || {}) : ""}
      ${result ? readingSimulationResultTemplate(result) : ""}
      ${simulation.history?.length ? `
        <div class="reading-history-block">
          <h3>Riwayat simulasi</h3>
          <div class="reading-history-list">
            ${simulation.history.slice(0, 3).map((item) => `
              <article>
                <strong>${escapeHtml(simulationModeLabel(item.mode))}</strong>
                <span>Score ${Math.round(item.total_score || 0)}</span>
                <p>${escapeHtml(item.recommended_next_practice || "")}</p>
              </article>
            `).join("")}
          </div>
        </div>
      ` : ""}
    </section>
  `;
}

function readingSimulationSessionTemplate(session, answers) {
  const answered = Object.keys(answers || {}).length;
  return `
    <div class="reading-simulation-progress">
      <span>${answered}/${session.question_count || 0} soal terjawab</span>
      ${readingPercentBar((answered / Math.max(session.question_count || 1, 1)) * 100)}
    </div>
    <div class="reading-sim-passage-list">
      ${(session.passages || []).map((passage, passageIndex) => `
        <article class="reading-sim-passage-card">
          <p class="eyebrow">Passage ${passageIndex + 1}</p>
          <h3>${escapeHtml(passage.title || "")}</h3>
          <p class="reading-sim-passage-text">${escapeHtml(passage.text || "")}</p>
          <div class="reading-sim-question-list">
            ${(passage.questions || []).map((question, questionIndex) => readingSimulationQuestionTemplate(question, answers, questionIndex)).join("")}
          </div>
        </article>
      `).join("")}
    </div>
    <button id="submitReadingSimulationButton" class="primary-button" type="button">Submit Simulasi</button>
  `;
}

function readingSimulationQuestionTemplate(question, answers, questionIndex) {
  const selected = answers[question.id];
  return `
    <div class="reading-sim-question-card">
      <div class="reading-question-topline">
        <h3>${questionIndex + 1}. ${escapeHtml(question.text || "")}</h3>
        <span>${escapeHtml(readingSubskillLabel(question.sub_skill))}</span>
      </div>
      <div class="question-options">
        ${(question.options || []).map((option, optionIndex) => `
          <button class="option-button ${selected === optionIndex ? "selected" : ""}" type="button" data-simulation-question="${question.id}" data-simulation-option="${optionIndex}">
            ${String.fromCharCode(65 + optionIndex)}. ${escapeHtml(option)}
          </button>
        `).join("")}
      </div>
    </div>
  `;
}

function readingSimulationResultTemplate(result) {
  const weakest = result.weakest_sub_skill || {};
  const strongest = result.strongest_sub_skill || {};
  const score = Math.round(result.total_score || 0);
  const accuracy = Math.round(result.accuracy || 0);
  const tone = accuracy >= 70 ? "success" : accuracy >= 45 ? "warning" : "danger";
  const statusText = accuracy >= 70
    ? "Simulasi stabil. Lanjut naikkan speed dan konsistensi."
    : accuracy >= 45
      ? "Masih berkembang. Fokus satu sub-skill lemah dulu."
      : "Perlu penguatan dasar. Ulangi Guided Reading sebelum simulasi berikutnya.";
  return `
    <section class="reading-result-report ${tone}">
      <div class="reading-result-main">
        <span class="reading-badge ${tone}">Final report</span>
        <h3>Score ${score}</h3>
        <p>${escapeHtml(statusText)}</p>
        <div class="reading-result-meta">
          <span>Accuracy ${accuracy}%</span>
          <span>Waktu ${formatSimulationTime(result.time_spent_seconds || 0)}</span>
          <span>${result.correct || 0}/${result.total_questions || 0} benar</span>
        </div>
      </div>
      <div class="reading-result-action">
        <strong>Latihan berikutnya</strong>
        <p>${escapeHtml(result.recommended_next_practice || "Ulangi latihan sub-skill terlemah.")}</p>
        <div class="inline-actions">
          <button class="primary-button" type="button" data-reading-mode="trainer">Latih Skill Lemah</button>
          <button id="startReadingSimulationButton" class="ghost-button" type="button">Simulasi Baru</button>
        </div>
      </div>
    </section>
    <div class="reading-two-column">
      <div class="reading-soft-card">
        <span class="reading-badge success">Paling kuat</span>
        <h3>${escapeHtml(strongest.label || "-")}</h3>
        ${readingPercentBar(strongest.accuracy || 0)}
        <p>${Math.round(strongest.accuracy || 0)}% akurat di sub-skill ini.</p>
      </div>
      <div class="reading-soft-card">
        <span class="reading-badge warning">Perlu fokus</span>
        <h3>${escapeHtml(weakest.label || "-")}</h3>
        ${readingPercentBar(weakest.accuracy || 0)}
        <p>${Math.round(weakest.accuracy || 0)}% akurat. Mulai dari review evidence dan kata kunci.</p>
      </div>
    </div>
    <div class="reading-section-title">
      <h3>Sub-skill breakdown</h3>
      <p>Lihat skill mana yang sudah aman dan mana yang perlu latihan ulang.</p>
    </div>
    <div class="reading-skill-grid">
      ${(result.sub_skill_breakdown || []).map((item) => `
        ${readingSkillBreakdownCard(item)}
      `).join("")}
    </div>
    <div class="reading-section-title">
      <h3>Answer Review</h3>
      <p>Review ini dibuat ringkas supaya kamu tahu alasan salah/benar tanpa membaca ulang semuanya.</p>
    </div>
    <div class="reading-review-summary-grid">
      ${(result.answer_review_summary || []).slice(0, 5).map((review) => `
        ${readingSimulationReviewCard(review)}
      `).join("")}
    </div>
  `;
}

function readingMiniStat(label, value) {
  return `
    <div>
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(String(value || "-"))}</strong>
    </div>
  `;
}

function readingAttemptFeedbackSummary(feedback) {
  const text = String(feedback || "").trim();
  if (!text) return "Baca ulang evidence sentence dan cek ulang pilihan jawaban.";
  if (text.startsWith("SIMULATION_RESULT:")) {
    try {
      const result = JSON.parse(text.replace("SIMULATION_RESULT:", ""));
      return `Simulasi ${simulationModeLabel(result.mode)}: ${Math.round(result.total_score || result.accuracy || 0)}%. Fokus berikutnya: ${result.recommended_next_practice || "latihan sub-skill terlemah."}`;
    } catch (error) {
      return "Hasil simulasi tersimpan. Fokus review sub-skill terlemah dan evidence sentence.";
    }
  }
  return text.length > 160 ? `${text.slice(0, 157)}...` : text;
}

function readingPercentBar(value) {
  const percent = Math.max(0, Math.min(100, Math.round(Number(value || 0))));
  return `<div class="reading-progress-line" aria-label="Progress ${percent}%"><span style="width: ${percent}%"></span></div>`;
}

function readingSkillBreakdownCard(item) {
  const accuracy = Math.round(item.accuracy || item.mastery_score || 0);
  const tone = accuracy >= 70 ? "success" : accuracy >= 40 ? "warning" : "danger";
  const hasScoreDetail = item.correct !== undefined && item.total !== undefined;
  const detail = hasScoreDetail
    ? `${item.correct || 0}/${item.total || 0} benar`
    : `${item.attempt_count || 0} latihan`;
  return `
    <article class="reading-skill-card ${tone}">
      <div>
        <strong>${escapeHtml(item.label || readingSubskillLabel(item.sub_skill || item.subskill))}</strong>
        <span>${accuracy}%</span>
      </div>
      ${readingPercentBar(accuracy)}
      <small>${escapeHtml(detail)}</small>
    </article>
  `;
}

function readingSimulationReviewCard(review) {
  const correct = Boolean(review.is_correct);
  const selected = review.selected_answer?.label
    ? `${review.selected_answer.label}. ${review.selected_answer.text || ""}`
    : "";
  const answer = review.correct_answer?.label
    ? `${review.correct_answer.label}. ${review.correct_answer.text || ""}`
    : "";
  return `
    <article class="reading-answer-mini-card ${correct ? "correct" : "review"}">
      <div class="reading-answer-mini-head">
        <span class="reading-badge ${correct ? "success" : "warning"}">${correct ? "Benar" : "Review"}</span>
        <small>${escapeHtml(readingSubskillLabel(review.related_reading_sub_skill))}</small>
      </div>
      <h3>${escapeHtml(review.question_text || "")}</h3>
      ${selected || answer ? `
        <p><strong>Anda:</strong> ${escapeHtml(selected || "-")}<br><strong>Benar:</strong> ${escapeHtml(answer || "-")}</p>
      ` : ""}
      <p>${escapeHtml(review.direct_explanation || "")}</p>
      <small>Evidence: ${escapeHtml(review.evidence_sentence || "-")}</small>
    </article>
  `;
}

function simulationModeLabel(mode) {
  const labels = {
    short: "Short simulation",
    medium: "Medium simulation",
    full: "Full practice"
  };
  return labels[mode] || mode || "Simulation";
}

async function startReadingSimulation() {
  let session = localReadingSimulationSession(state.readingSimulation.mode || "short");
  if (apiOnline) {
    try {
      session = await apiRequest("/reading/simulation/start", {
        method: "POST",
        body: {
          user_id: state.user?.id || "default-user",
          mode: state.readingSimulation.mode || "short"
        }
      });
    } catch (error) {
      apiOnline = false;
    }
  }
  state.readingSimulation = {
    ...state.readingSimulation,
    mode: session.mode,
    session,
    answers: {},
    result: null,
    startedAtMs: Date.now()
  };
  saveState();
  renderReading();
}

async function submitReadingSimulation() {
  const simulation = state.readingSimulation;
  if (!simulation?.session) return;
  let result = localReadingSimulationResult(simulation);
  if (apiOnline) {
    try {
      result = await apiRequest("/reading/simulation/submit", {
        method: "POST",
        body: {
          user_id: state.user?.id || "default-user",
          session_id: simulation.session.session_id,
          mode: simulation.session.mode,
          session: simulation.session,
          answers: simulation.answers || {},
          time_spent_seconds: simulationElapsedSeconds()
        }
      });
      state.readingJourney = result.reading_journey || state.readingJourney;
      await refreshReadingSimulationHistory();
    } catch (error) {
      apiOnline = false;
    }
  }
  state.readingSimulation = {
    ...simulation,
    result
  };
  state.progress.Reading = Math.max(state.progress.Reading, result.total_score || 0);
  addActivity("Reading", `TOEFL Simulation ${simulation.session.mode}`, result.total_score || 0);
  saveState();
  await refreshIntegratedJourney();
  await refreshReadingJourney();
  renderReading();
  renderDashboard();
  renderJourney();
}

function setupReadingSimulationTimer() {
  if (readingSimulationTimer) {
    clearInterval(readingSimulationTimer);
    readingSimulationTimer = null;
  }
  if (!state.readingSimulation?.session || state.readingSimulation?.result) return;
  readingSimulationTimer = setInterval(() => {
    const target = document.getElementById("readingSimulationTimer");
    if (!target) {
      clearInterval(readingSimulationTimer);
      readingSimulationTimer = null;
      return;
    }
    target.textContent = formatSimulationTime(remainingSimulationSeconds());
  }, 1000);
}

function remainingSimulationSeconds() {
  const simulation = state.readingSimulation || {};
  const duration = Number(simulation.session?.duration_seconds || 0);
  const elapsed = simulationElapsedSeconds();
  return Math.max(0, duration - elapsed);
}

function simulationElapsedSeconds() {
  const started = state.readingSimulation?.startedAtMs;
  if (!started) return 0;
  return Math.max(0, Math.round((Date.now() - started) / 1000));
}

function formatSimulationTime(totalSeconds) {
  const seconds = Math.max(0, Number(totalSeconds || 0));
  const minutes = Math.floor(seconds / 60);
  const rest = seconds % 60;
  return `${String(minutes).padStart(2, "0")}:${String(rest).padStart(2, "0")}`;
}

function localReadingSimulationSession(mode = "short") {
  const durationMap = { short: 600, medium: 1200, full: 1800 };
  const passageCount = mode === "short" ? 1 : mode === "medium" ? 2 : 2;
  const passages = localSimulationPassages().slice(0, passageCount);
  return {
    session_id: `local-sim-${mode}-${Date.now()}`,
    mode,
    label: mode === "short" ? "Short simulation" : mode === "medium" ? "Medium simulation" : "Full practice simulation",
    duration_minutes: Math.round((durationMap[mode] || 600) / 60),
    duration_seconds: durationMap[mode] || 600,
    started_at: new Date().toISOString(),
    bantuan_id_policy: "Bantuan ID dibatasi dalam simulation mode.",
    passages,
    question_count: passages.reduce((total, passage) => total + passage.questions.length, 0)
  };
}

function localSimulationPassages() {
  const baseLessons = getLessons();
  return baseLessons.map((lesson) => ({
    id: `local-${lesson.id}`,
    title: lesson.title,
    text: lesson.passage,
    questions: [
      ...lesson.questions.map((question) => ({
        ...question,
        sub_skill: inferLocalQuestionSubskill(question)
      })),
      {
        id: `${lesson.id}-sim-extra-1`,
        text: "What can be inferred from the passage?",
        options: ["The analyst should clarify before solving.", "Coding is the first step.", "Stakeholders are unrelated.", "Strategy should be ignored."],
        answer: 0,
        sub_skill: "inference",
        explanation: "The passage implies clarification and alignment come before solution work."
      },
      {
        id: `${lesson.id}-sim-extra-2`,
        text: "Which sentence best summarizes the passage?",
        options: ["A BA connects needs, requirements, and outcomes.", "A BA ignores the process.", "A BA only writes code.", "A BA avoids questions."],
        answer: 0,
        sub_skill: "sentence_simplification",
        explanation: "The summary preserves the main meaning of the passage."
      }
    ].slice(0, 5)
  }));
}

function localReadingSimulationResult(simulation) {
  const answers = simulation.answers || {};
  const flat = [];
  (simulation.session.passages || []).forEach((passage) => {
    (passage.questions || []).forEach((question) => flat.push({ passage, question }));
  });
  let correct = 0;
  const buckets = {};
  const reviews = [];
  flat.forEach(({ passage, question }) => {
    const selected = answers[question.id];
    const isCorrect = selected === question.answer;
    correct += isCorrect ? 1 : 0;
    const subSkill = question.sub_skill || inferLocalQuestionSubskill(question);
    buckets[subSkill] = buckets[subSkill] || { sub_skill: subSkill, label: readingSubskillLabel(subSkill), correct: 0, total: 0 };
    buckets[subSkill].total += 1;
    buckets[subSkill].correct += isCorrect ? 1 : 0;
    if (selected !== undefined) {
      reviews.push(localReadingAnswerReview({ id: passage.id, passage: passage.text, questions: [question] }, question, selected));
    }
  });
  const total = flat.length || 1;
  const accuracy = Math.round((correct / total) * 100);
  const breakdown = Object.values(buckets).map((item) => ({ ...item, accuracy: Math.round((item.correct / Math.max(item.total, 1)) * 100) }));
  const strongest = [...breakdown].sort((a, b) => b.accuracy - a.accuracy)[0] || null;
  const weakest = [...breakdown].sort((a, b) => a.accuracy - b.accuracy)[0] || null;
  return {
    session_id: simulation.session.session_id,
    mode: simulation.session.mode,
    total_score: accuracy,
    accuracy,
    correct,
    total_questions: total,
    time_spent_seconds: simulationElapsedSeconds(),
    sub_skill_breakdown: breakdown,
    strongest_sub_skill: strongest,
    weakest_sub_skill: weakest,
    recommended_next_practice: localReadingAction(weakest?.sub_skill || "main_idea"),
    answer_review_summary: reviews
  };
}

function guidedReadingPanel(lesson) {
  const guided = state.guidedReading?.lessonId === lesson.id ? state.guidedReading : structuredClone(defaultState.guidedReading);
  const hasSteps = guided.started && guided.steps?.length;
  const activeIndex = Math.min(guided.activeStep || 0, Math.max((guided.steps || []).length - 1, 0));
  const visibleSteps = hasSteps ? guided.steps.slice(0, activeIndex + 1) : [];
  return `
    <section class="panel reading-guided-panel" id="guidedReadingPanel">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Guided Reading Mode</p>
          <h3>Baca passage langkah demi langkah</h3>
          <p>Mode ini membantu pemula memahami judul, kalimat pertama, subject/verb, vocabulary, paragraph map, dan main idea sebelum menjawab soal.</p>
        </div>
        <button id="startGuidedReadingButton" class="primary-button" type="button">${hasSteps ? "Ulangi Guided Reading" : "Mulai Guided Reading"}</button>
      </div>
      ${hasSteps ? `
        <div class="reading-step-track">
          ${guided.steps.map((step, index) => `
            <span class="${index < activeIndex ? "done" : index === activeIndex ? "current" : ""}">${step.step}</span>
          `).join("")}
        </div>
        <div class="reading-guided-list">
          ${visibleSteps.map((step) => guidedReadingStepCard(step, lesson)).join("")}
        </div>
        ${guided.completed ? "" : `
          <button id="nextGuidedReadingStepButton" class="ghost-button" type="button">
            ${activeIndex >= guided.steps.length - 1 ? "Selesai Guided Reading" : "Lanjut ke Langkah Berikutnya"}
          </button>
        `}
        ${guided.completed ? resultTemplate("success", "Guided Reading selesai", "Aktivitas pendukung sudah dicatat. Sekarang lanjut jawab TOEFL-style Questions di bawah.") : ""}
      ` : `
        <div class="reading-empty-state">
          <strong>Mulai dari memahami bacaan, bukan menebak opsi.</strong>
          <p>Guided Reading akan membuka langkah kecil: judul, kalimat pertama, subject/verb, vocabulary, paragraph map, lalu main idea.</p>
        </div>
      `}
    </section>
  `;
}

function guidedReadingStepCard(step, lesson) {
  const contextType = step.bantuan_context_type || "reading_paragraph";
  const helpContext = readingHelpContext(lesson, lesson.questions?.[0]);
  return `
    <article class="reading-guided-card">
      <span class="reading-badge">Step ${step.step}</span>
      <h3>${escapeHtml(step.title || "")} ${step.focus_text ? renderContextualHelpButton("reading", contextType, step.focus_text, helpContext) : ""}</h3>
      ${step.focus_text ? `<p class="reading-focus-text">${escapeHtml(step.focus_text)}</p>` : ""}
      ${step.subject || step.main_verb ? `
        <div class="reading-two-column">
          <div class="reading-soft-card compact">
            <span class="muted">Subject</span>
            <strong>${escapeHtml(step.subject || "-")}</strong>
          </div>
          <div class="reading-soft-card compact">
            <span class="muted">Main Verb</span>
            <strong>${escapeHtml(step.main_verb || "-")}</strong>
          </div>
        </div>
      ` : ""}
      ${step.key_vocabulary?.length ? guidedVocabularyList(step.key_vocabulary) : ""}
      ${step.paragraph_map?.length ? guidedParagraphMap(step.paragraph_map, lesson) : ""}
      ${step.main_idea ? `<p><strong>Main idea:</strong> ${escapeHtml(step.main_idea)}</p>` : ""}
      <p>${escapeHtml(step.simple_explanation || "")}</p>
      <p class="muted">${escapeHtml(step.learner_action || "")}</p>
    </article>
  `;
}

function guidedVocabularyList(items) {
  return `
    <div class="lesson-list compact-list">
      ${items.map((item) => `
        <p><strong>${escapeHtml(item.word || "")}</strong>: ${escapeHtml(item.meaning_id || "")}<br><span class="muted">${escapeHtml(item.context_tip || "")}</span></p>
      `).join("")}
    </div>
  `;
}

function guidedParagraphMap(paragraphs, lesson) {
  return `
    <div class="lesson-list compact-list">
      ${paragraphs.map((paragraph) => `
        <div>
          <h3>Paragraf ${paragraph.paragraph_number} ${renderContextualHelpButton("reading", "reading_paragraph", paragraph.text || "", readingHelpContext(lesson, lesson.questions?.[0]))}</h3>
          <p>${escapeHtml(paragraph.simple_meaning || "")}</p>
          <p><strong>Main point:</strong> ${escapeHtml(paragraph.main_point || "")}</p>
          <p class="muted">Skill: ${escapeHtml(readingSubskillLabel(paragraph.possible_reading_skill))} · ${escapeHtml(paragraph.beginner_tip || "")}</p>
        </div>
      `).join("")}
    </div>
  `;
}

async function startGuidedReading(lesson) {
  let guided = localGuidedReadingState(lesson);
  if (apiOnline) {
    try {
      const [stepsResponse, mapResponse] = await Promise.all([
        apiRequest("/reading/guided-steps", {
          method: "POST",
          body: {
            lesson_id: lesson.id,
            title: lesson.title,
            passage: lesson.passage,
            vocabulary: lesson.vocabulary,
            question_text: lesson.questions?.[0]?.text || ""
          }
        }),
        apiRequest("/reading/passage-map", {
          method: "POST",
          body: {
            lesson_id: lesson.id,
            title: lesson.title,
            passage: lesson.passage,
            vocabulary: lesson.vocabulary
          }
        })
      ]);
      guided = {
        lessonId: lesson.id,
        started: true,
        activeStep: 0,
        steps: stepsResponse.steps || guided.steps,
        passageMap: mapResponse.paragraphs || guided.passageMap,
        completed: false
      };
    } catch (error) {
      apiOnline = false;
    }
  }
  state.guidedReading = guided;
  saveState();
  renderReading();
}

async function nextGuidedReadingStep(lesson) {
  if (!state.guidedReading?.started || state.guidedReading.lessonId !== lesson.id) {
    await startGuidedReading(lesson);
    return;
  }
  const lastIndex = Math.max((state.guidedReading.steps || []).length - 1, 0);
  if ((state.guidedReading.activeStep || 0) >= lastIndex) {
    state.guidedReading.completed = true;
    addActivity("Reading", `Guided Reading: ${lesson.title}`, 100);
    saveState();
    renderDashboard();
    renderJourney();
    renderReading();
    return;
  }
  state.guidedReading.activeStep = (state.guidedReading.activeStep || 0) + 1;
  saveState();
  renderReading();
}

function readingSubskillProgress() {
  const subskills = state.readingTrainer?.subskills?.length
    ? state.readingTrainer.subskills
    : (state.readingJourney?.sub_skill_mastery || localReadingSubskills());
  return `
    <section class="panel reading-subskill-panel">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Reading Sub-skill Progress</p>
          <h3>Progress kemampuan Reading</h3>
          <p>Setiap skill punya progress sendiri. Prioritaskan yang merah/kuning sebelum masuk simulasi lagi.</p>
        </div>
      </div>
      <div class="reading-skill-grid">
        ${subskills.map((item) => readingSkillBreakdownCard({
          ...item,
          sub_skill: item.sub_skill || item.subskill,
          accuracy: item.mastery_score,
          attempt_count: item.attempt_count
        })).join("")}
      </div>
    </section>
  `;
}

function readingTrainerPanel() {
  const trainer = state.readingTrainer?.content || localReadingTrainerContent(state.readingTrainer?.selectedSubSkill || "main_idea");
  const subSkill = trainer.sub_skill || state.readingTrainer?.selectedSubSkill || "main_idea";
  const question = trainer.question || {};
  const passage = trainer.passage || {};
  const selected = state.readingTrainer?.selectedAnswer;
  const feedback = state.readingTrainer?.feedback;
  const buttons = [
    ["main_idea", "Main Idea"],
    ["detail_information", "Detail"],
    ["vocabulary_context", "Vocabulary Context"],
    ["inference", "Inference"],
    ["sentence_simplification", "Sentence Breakdown"]
  ];
  const baseContext = {
    passage_title: passage.title || "",
    passage_text: passage.text || "",
    question_text: question.text || "",
    correct_answer: question.options?.[question.answer] || "",
    explanation: question.explanation || "",
    tags: [trainer.label, "Reading Trainer"].filter(Boolean)
  };
  return `
    <section class="panel reading-trainer-panel" id="readingTrainerPanel">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Reading Trainer</p>
          <h3>Latihan berdasarkan sub-skill</h3>
          <p>${escapeHtml(trainer.guidance?.tip || "Pilih tipe latihan, jawab soal, lalu lihat feedback.")}</p>
        </div>
      </div>
      <div class="reading-trainer-tabs">
        ${buttons.map(([value, label]) => `
          <button class="${subSkill === value ? "selected-control" : ""}" type="button" data-reading-trainer-subskill="${value}">
            ${label}
          </button>
        `).join("")}
      </div>
      <div class="reading-trainer-layout">
        <div class="reading-soft-card reading-trainer-passage">
          <span class="reading-badge">Passage</span>
          <h3>${escapeHtml(passage.title || "Trainer Passage")}</h3>
          <p>${escapeHtml(passage.text || "")} ${renderContextualHelpButton("reading", "reading_paragraph", passage.text || "", baseContext)}</p>
          <p class="muted">${escapeHtml(trainer.guidance?.goal || "")}</p>
        </div>
        <div class="reading-question-card">
          <span class="reading-badge warning">${escapeHtml(readingSubskillLabel(subSkill))}</span>
          <h3>${escapeHtml(question.text || "")} ${renderContextualHelpButton("reading", "reading_question", question.text || "", baseContext)}</h3>
          <div class="question-options">
            ${(question.options || []).map((option, index) => `
              <div class="option-help-row">
                <button class="option-button ${selected === index ? "selected" : ""}" type="button" data-reading-trainer-answer="${index}">
                  ${String.fromCharCode(65 + index)}. ${escapeHtml(option)}
                </button>
                ${renderContextualHelpButton("reading", "reading_option", option, {
                  ...baseContext,
                  option_label: String.fromCharCode(65 + index),
                  option_text: option
                })}
              </div>
            `).join("")}
          </div>
          ${feedback ? readingTrainerFeedbackTemplate(feedback) : `<div class="reading-note"><strong>Belum dijawab</strong><p>Pilih satu opsi untuk menyimpan latihan ${escapeHtml(readingSubskillLabel(subSkill))}.</p></div>`}
        </div>
      </div>
    </section>
  `;
}

function readingTrainerFeedbackTemplate(feedback) {
  const message = feedback.message || feedback.explanation || "Feedback tersimpan.";
  return `
    <div class="reading-feedback-card ${feedback.is_correct ? "success" : "warning"}">
      <span class="reading-badge ${feedback.is_correct ? "success" : "warning"}">${feedback.is_correct ? "Jawaban benar" : "Perlu review"}</span>
      <p>${escapeHtml(message)}</p>
      ${feedback.evidence_sentence ? `<small>Evidence: ${escapeHtml(feedback.evidence_sentence)}</small>` : ""}
    </div>
  `;
}

async function submitReadingTrainerAnswer(selected) {
  const trainer = state.readingTrainer?.content || localReadingTrainerContent(state.readingTrainer?.selectedSubSkill || "main_idea");
  const subSkill = trainer.sub_skill || "main_idea";
  const question = trainer.question || {};
  let feedback = localReadingTrainerFeedback(trainer, selected);
  if (apiOnline) {
    try {
      const response = await apiRequest("/reading/attempt", {
        method: "POST",
        body: {
          user_id: state.user?.id || "default-user",
          passage_id: trainer.passage?.id || `trainer-${subSkill}`,
          activity_type: "reading_subskill_trainer",
          sub_skill: subSkill,
          selected,
          correct_answer: question.answer,
          mistakes: feedback.is_correct ? [] : [{ question_id: question.id, selected }],
          feedback: feedback.message
        }
      });
      feedback = response.answer_feedback || feedback;
      state.readingJourney = response.reading_journey || state.readingJourney;
      await refreshReadingTrainer(subSkill);
    } catch (error) {
      apiOnline = false;
    }
  }
  state.readingTrainer = {
    ...(state.readingTrainer || localReadingTrainerState(subSkill)),
    selectedSubSkill: subSkill,
    selectedAnswer: selected,
    feedback
  };
  state.progress.Reading = Math.max(state.progress.Reading, feedback.is_correct ? 80 : 45);
  addActivity("Reading", `${readingSubskillLabel(subSkill)} trainer`, feedback.is_correct ? 100 : 0);
  saveState();
  renderReading();
  renderDashboard();
  renderJourney();
}

function localReadingTrainerFeedback(trainer, selected) {
  const question = trainer.question || {};
  const isCorrect = selected === question.answer;
  const correctAnswer = question.options?.[question.answer] || "";
  return {
    is_correct: isCorrect,
    selected_index: selected,
    correct_index: question.answer,
    correct_answer: correctAnswer,
    evidence_sentence: question.evidence_sentence,
    explanation: question.explanation,
    message: isCorrect
      ? `Benar. ${question.explanation || "Jawaban sesuai evidence passage."}`
      : `Belum tepat. Jawaban yang lebih kuat: ${correctAnswer}. ${question.explanation || "Cocokkan lagi dengan evidence passage."}`
  };
}

function readingMasteryStatusLabel(status) {
  const labels = {
    not_started: "belum mulai",
    needs_review: "perlu review",
    developing: "berkembang",
    strong: "kuat"
  };
  return labels[status] || "belajar";
}

function readingQuestionTemplate(question, index, lesson) {
  const selected = state.readingAnswers[question.id];
  const baseContext = readingHelpContext(lesson, question);
  return `
    <div class="question reading-question-card reading-practice-question-card">
      <div class="reading-question-header">
        <div>
          <span class="reading-badge">Soal ${index + 1}</span>
          <h3>${escapeHtml(question.text)}</h3>
        </div>
        ${renderContextualHelpButton("reading", "reading_question", question.text, baseContext)}
      </div>
      <div class="question-options">
        ${question.options
          .map(
            (option, optionIndex) => `
              <div class="option-help-row reading-option-row ${selected === optionIndex ? "selected" : ""}">
                <button class="option-button ${selected === optionIndex ? "selected" : ""}" type="button" data-reading-question="${question.id}" data-option="${optionIndex}">
                  <span class="option-letter">${String.fromCharCode(65 + optionIndex)}</span>
                  <span>${escapeHtml(option)}</span>
                </button>
                ${renderContextualHelpButton("reading", "reading_option", option, {
                  ...baseContext,
                  option_label: String.fromCharCode(65 + optionIndex),
                  option_text: option
                })}
              </div>
            `
          )
          .join("")}
      </div>
      <div class="reading-question-hint">
        <strong>Petunjuk setelah submit</strong>
        <p>${escapeHtml(question.explanation || "")}</p>
      </div>
    </div>
  `;
}

function readingHelpContext(lesson, question = null) {
  return {
    passage_title: lesson?.title || "",
    passage_text: lesson?.passage || "",
    question_text: question?.text || "",
    correct_answer: question ? question.options?.[question.answer] || "" : "",
    explanation: question?.explanation || "",
    tags: [lesson?.context, lesson?.level].filter(Boolean)
  };
}

function scoreReading(lesson) {
  const correct = lesson.questions.filter((question) => state.readingAnswers[question.id] === question.answer).length;
  return Math.round((correct / lesson.questions.length) * 100);
}

function localReadingAnswerReviews(lesson) {
  return lesson.questions
    .filter((question) => state.readingAnswers[question.id] !== undefined)
    .map((question) => localReadingAnswerReview(lesson, question, state.readingAnswers[question.id]));
}

function localReadingAnswerReview(lesson, question, selectedIndex) {
  const correctIndex = question.answer;
  const selectedText = question.options[selectedIndex] || "";
  const correctText = question.options[correctIndex] || "";
  const isCorrect = selectedIndex === correctIndex;
  const evidence = localEvidenceSentence(lesson.passage, correctText);
  const distractorAnalysis = {};
  question.options.forEach((option, index) => {
    const letter = String.fromCharCode(65 + index);
    const correct = index === correctIndex;
    distractorAnalysis[letter] = {
      meaning: localOptionMeaning(option),
      relation_to_passage: correct ? "Sesuai dengan passage dan bukti utama." : localOptionRelation(option),
      correct_or_wrong: correct ? "correct" : "wrong",
      reason: correct
        ? `Opsi ini didukung oleh evidence: ${evidence}`
        : `${index === selectedIndex ? "Ini pilihan Anda, tetapi " : ""}${localOptionWrongReason(option)}`
    };
  });
  return {
    question_id: question.id,
    question_text: question.text,
    selected_answer: { label: String.fromCharCode(65 + selectedIndex), index: selectedIndex, text: selectedText },
    correct_answer: { label: String.fromCharCode(65 + correctIndex), index: correctIndex, text: correctText },
    is_correct: isCorrect,
    direct_explanation: isCorrect
      ? `Jawaban Anda benar. Opsi ${String.fromCharCode(65 + correctIndex)} paling sesuai dengan passage.`
      : `Jawaban Anda belum tepat. Jawaban yang lebih kuat adalah opsi ${String.fromCharCode(65 + correctIndex)}.`,
    evidence_sentence: evidence,
    why_correct_answer_is_correct: question.explanation || "Jawaban benar didukung oleh evidence passage.",
    why_selected_answer_is_wrong: isCorrect ? "" : localOptionWrongReason(selectedText),
    distractor_analysis: distractorAnalysis,
    related_reading_sub_skill: inferLocalQuestionSubskill(question),
    next_practice_recommendation: isCorrect
      ? `Lanjutkan latihan ${readingSubskillLabel(inferLocalQuestionSubskill(question))}.`
      : `Ulangi ${readingSubskillLabel(inferLocalQuestionSubskill(question))}: cocokkan opsi dengan evidence sentence.`
  };
}

function readingAnswerReviewPanel(reviews, lesson) {
  if (!reviews?.length) return "";
  return `
    <section class="panel reading-answer-review-panel">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Answer Review</p>
          <h3>Kenapa jawaban benar atau salah?</h3>
          <p>Pelajari bukti dari passage dan analisis setiap opsi supaya tidak hanya tahu skor.</p>
        </div>
      </div>
      <div class="lesson-list">
        ${reviews.map((review, index) => readingAnswerReviewCard(review, lesson, index)).join("")}
      </div>
    </section>
  `;
}

function readingAnswerReviewCard(review, lesson, index) {
  const question = lesson.questions.find((item) => item.id === review.question_id) || lesson.questions[index] || {};
  const baseContext = readingHelpContext(lesson, question);
  const analysis = review.distractor_analysis || {};
  return `
    <article class="reading-answer-card ${review.is_correct ? "correct" : "review"}">
      <div class="reading-answer-mini-head">
        <span class="reading-badge ${review.is_correct ? "success" : "warning"}">${review.is_correct ? "Benar" : "Perlu review"}</span>
        <small>Soal ${index + 1} · ${escapeHtml(readingSubskillLabel(review.related_reading_sub_skill))}</small>
      </div>
      <h3>${escapeHtml(review.question_text || question.text || "")} ${renderContextualHelpButton("reading", "reading_question", review.question_text || question.text || "", baseContext)}</h3>
      <div class="reading-two-column">
        <div class="reading-soft-card compact">
          <span>Jawaban Anda</span>
          <strong>${escapeHtml(review.selected_answer?.label || "-")}. ${escapeHtml(review.selected_answer?.text || "-")}</strong>
        </div>
        <div class="reading-soft-card compact">
          <span>Jawaban Benar</span>
          <strong>${escapeHtml(review.correct_answer?.label || "-")}. ${escapeHtml(review.correct_answer?.text || "-")}</strong>
        </div>
      </div>
      <div class="reading-evidence-box">
        <strong>Bukti dari passage</strong>
        <p>${escapeHtml(review.evidence_sentence || "-")} ${renderContextualHelpButton("reading", "reading_paragraph", review.evidence_sentence || lesson.passage, baseContext)}</p>
      </div>
      <div class="reading-list-stack">
        <article class="reading-list-item"><strong>Penjelasan langsung</strong><p>${escapeHtml(review.direct_explanation || "")}</p></article>
        <article class="reading-list-item"><strong>Kenapa jawaban benar</strong><p>${escapeHtml(review.why_correct_answer_is_correct || "")}</p></article>
        ${review.why_selected_answer_is_wrong ? `<article class="reading-list-item"><strong>Kenapa jawaban Anda salah</strong><p>${escapeHtml(review.why_selected_answer_is_wrong)}</p></article>` : ""}
      </div>
      <div class="reading-distractor-grid">
        ${Object.entries(analysis).map(([letter, item]) => `
          <article class="${item.correct_or_wrong === "correct" ? "correct" : ""}">
            <h3>Opsi ${letter} ${renderContextualHelpButton("reading", "reading_option", optionTextFromReview(question, letter, item), {
              ...baseContext,
              option_label: letter,
              option_text: optionTextFromReview(question, letter, item)
            })}</h3>
            <p><strong>Arti:</strong> ${escapeHtml(item.meaning || "")}</p>
            <p>${escapeHtml(item.relation_to_passage || "")}</p>
            <small>${escapeHtml(item.correct_or_wrong === "correct" ? "Benar" : "Salah")} · ${escapeHtml(item.reason || "")}</small>
          </article>
        `).join("")}
      </div>
      <p class="muted">${escapeHtml(review.next_practice_recommendation || "")}</p>
    </article>
  `;
}

function optionTextFromReview(question, letter, item) {
  const index = letter.charCodeAt(0) - 65;
  return question?.options?.[index] || item?.meaning || "";
}

function localEvidenceSentence(passage, correctText) {
  const sentences = splitLocalSentences(passage);
  const lowerCorrect = String(correctText || "").toLowerCase();
  if (lowerCorrect.includes("requirements") && lowerCorrect.includes("stakeholder")) {
    return sentences.find((sentence) => sentence.toLowerCase().includes("requirements") && sentence.toLowerCase().includes("stakeholder")) || sentences[0] || passage;
  }
  if (lowerCorrect.includes("clarify") || lowerCorrect.includes("clearer") || lowerCorrect.includes("outcome")) {
    return sentences.find((sentence) => sentence.toLowerCase().includes("clarify") || sentence.toLowerCase().includes("outcome")) || sentences[0] || passage;
  }
  return sentences[0] || passage;
}

function localOptionMeaning(option) {
  const lowered = String(option || "").toLowerCase();
  const map = {
    "business analysts should write code immediately.": "Business Analyst sebaiknya langsung menulis kode.",
    "business analysts must connect requirements with stakeholder needs and strategy.": "Business Analyst harus menghubungkan requirement dengan kebutuhan stakeholder dan strategi.",
    "stakeholders should avoid discussing vague problems.": "Stakeholder sebaiknya menghindari membahas masalah yang masih samar.",
    "organizational strategy is unrelated to requirements.": "Strategi organisasi tidak berhubungan dengan requirement.",
    "make clearer": "membuat lebih jelas",
    "remove": "menghapus",
    "delay": "menunda",
    "approve": "menyetujui"
  };
  return map[lowered] || `Arti opsi: ${option}`;
}

function localOptionRelation(option) {
  const lowered = String(option || "").toLowerCase();
  if (lowered.includes("write code")) return "Tidak didukung oleh passage.";
  if (lowered.includes("avoid discussing")) return "Kurang sesuai dengan passage.";
  if (lowered.includes("unrelated")) return "Bertentangan dengan passage.";
  return "Perlu dicek dengan bukti passage; opsi ini bukan yang paling kuat.";
}

function localOptionWrongReason(option) {
  const lowered = String(option || "").toLowerCase();
  if (lowered.includes("write code")) return "passage membahas requirement dan alignment, bukan coding langsung.";
  if (lowered.includes("avoid discussing")) return "passage meminta analyst mengklarifikasi masalah samar, bukan stakeholder menghindarinya.";
  if (lowered.includes("unrelated")) return "passage justru menyatakan requirement perlu selaras dengan strategy.";
  return "opsi ini tidak paling sesuai dengan evidence passage.";
}

function renderGrammar() {
  const activeSection = state.grammarHub?.activeSection || "menu";
  document.getElementById("grammarView").innerHTML = `
    ${pageHeaderTemplate({
      eyebrow: "Grammar Lab",
      title: activeSection === "menu" ? "Grammar Learning Path" : grammarSectionTitle(activeSection),
      description: activeSection === "menu"
        ? "Belajar grammar dari dasar sampai siap simulasi. Ikuti urutan yang disarankan agar tidak bingung mulai dari mana."
        : "Kerjakan satu area grammar saja. Setelah selesai, kembali ke Grammar Learning Path untuk memilih langkah berikutnya.",
      actions: ""
    })}
    ${renderGrammarActiveSection(activeSection)}
  `;

  document.querySelectorAll("[data-grammar-hub-section]").forEach((button) => {
    button.addEventListener("click", () => {
      setGrammarSection(button.dataset.grammarHubSection);
    });
  });

  document.querySelectorAll("[data-grammar-back]").forEach((button) => {
    button.addEventListener("click", () => {
      setGrammarSection("menu");
    });
  });

  const grammarHelpButton = document.getElementById("grammarHelpButton");
  if (grammarHelpButton) {
    grammarHelpButton.addEventListener("click", () => {
      openHelpWith(document.getElementById("grammarInput").value);
    });
  }

  const grammarForm = document.getElementById("grammarForm");
  if (grammarForm) {
    grammarForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const sentence = document.getElementById("grammarInput").value.trim();
      state.progress.Grammar = Math.max(state.progress.Grammar, 80);
      state.completedExercises += 1;
      addActivity("Grammar", "Sentence breakdown", 80);
      saveState();
      let analysisHtml = grammarAnalysis(sentence);
      if (apiOnline) {
        try {
          const response = await apiRequest("/grammar/breakdown", {
            method: "POST",
            body: { sentence, user_id: state.user?.id || "default-user" }
          });
          analysisHtml = grammarApiTemplate(response.analysis);
        } catch (error) {
          apiOnline = false;
        }
      }
      document.getElementById("grammarResult").innerHTML = analysisHtml;
      bindContextualHelpButtons(document.getElementById("grammarResult"));
      await refreshIntegratedJourney();
      await refreshGrammarProgress();
      renderDashboard();
      renderJourney();
    });
  }

  document.querySelectorAll("[data-grammar-trainer-topic]").forEach((button) => {
    button.addEventListener("click", async () => {
      await loadBasicGrammarTrainer(button.dataset.grammarTrainerTopic);
      renderGrammar();
    });
  });

  document.querySelectorAll("[data-grammar-quiz-answer]").forEach((select) => {
    select.addEventListener("change", () => {
      state.grammarTrainer.answers[select.dataset.grammarQuizAnswer] = select.value;
      state.grammarTrainer.result = null;
      saveState();
    });
  });

  const trainerForm = document.getElementById("basicGrammarTrainerForm");
  if (trainerForm) {
    trainerForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      await submitBasicGrammarTrainer();
      renderGrammar();
    });
  }

  document.querySelectorAll("[data-intermediate-grammar-topic]").forEach((button) => {
    button.addEventListener("click", async () => {
      await loadIntermediateGrammarTrainer(button.dataset.intermediateGrammarTopic);
      renderGrammar();
    });
  });

  document.querySelectorAll("[data-intermediate-grammar-answer]").forEach((select) => {
    select.addEventListener("change", () => {
      state.intermediateGrammarTrainer.answers[select.dataset.intermediateGrammarAnswer] = select.value;
      state.intermediateGrammarTrainer.result = null;
      saveState();
    });
  });

  const intermediateTrainerForm = document.getElementById("intermediateGrammarTrainerForm");
  if (intermediateTrainerForm) {
    intermediateTrainerForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      await submitIntermediateGrammarTrainer();
      renderGrammar();
    });
  }

  document.querySelectorAll("[data-grammar-error-type]").forEach((button) => {
    button.addEventListener("click", async () => {
      await loadGrammarErrorCorrection(button.dataset.grammarErrorType);
      renderGrammar();
    });
  });

  document.querySelectorAll("[data-grammar-error-answer]").forEach((select) => {
    select.addEventListener("change", () => {
      state.grammarErrorCorrection.answers[select.dataset.grammarErrorAnswer] = select.value;
      state.grammarErrorCorrection.result = null;
      saveState();
    });
  });

  const errorCorrectionForm = document.getElementById("grammarErrorCorrectionForm");
  if (errorCorrectionForm) {
    errorCorrectionForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      await submitGrammarErrorCorrection();
      renderGrammar();
    });
  }

  document.querySelectorAll("[data-sentence-builder-level]").forEach((button) => {
    button.addEventListener("click", async () => {
      await loadGrammarSentenceBuilder(button.dataset.sentenceBuilderLevel, state.grammarSentenceBuilder.selectedMode);
      renderGrammar();
    });
  });

  document.querySelectorAll("[data-sentence-builder-mode]").forEach((button) => {
    button.addEventListener("click", async () => {
      await loadGrammarSentenceBuilder(state.grammarSentenceBuilder.selectedLevel, button.dataset.sentenceBuilderMode);
      renderGrammar();
    });
  });

  document.querySelectorAll("[data-sentence-builder-answer]").forEach((input) => {
    input.addEventListener("input", () => {
      state.grammarSentenceBuilder.answers[input.dataset.sentenceBuilderAnswer] = input.value;
      state.grammarSentenceBuilder.result = null;
      saveState();
    });
  });

  const sentenceBuilderForm = document.getElementById("grammarSentenceBuilderForm");
  if (sentenceBuilderForm) {
    sentenceBuilderForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      await submitGrammarSentenceBuilder();
      renderGrammar();
    });
  }

  document.querySelectorAll("[data-advanced-grammar-topic]").forEach((button) => {
    button.addEventListener("click", async () => {
      await loadGrammarAdvancedLab(button.dataset.advancedGrammarTopic);
      renderGrammar();
    });
  });

  document.querySelectorAll("[data-advanced-practice-answer]").forEach((select) => {
    select.addEventListener("change", () => {
      state.grammarAdvancedLab.practiceAnswers[select.dataset.advancedPracticeAnswer] = select.value;
      state.grammarAdvancedLab.practiceResult = null;
      saveState();
    });
  });

  document.querySelectorAll("[data-advanced-rewrite-answer]").forEach((input) => {
    input.addEventListener("input", () => {
      state.grammarAdvancedLab.rewriteAnswers[input.dataset.advancedRewriteAnswer] = input.value;
      state.grammarAdvancedLab.rewriteResult = null;
      saveState();
    });
  });

  const advancedPracticeForm = document.getElementById("advancedGrammarPracticeForm");
  if (advancedPracticeForm) {
    advancedPracticeForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      await submitAdvancedGrammarPractice();
      renderGrammar();
    });
  }

  const advancedRewriteForm = document.getElementById("advancedGrammarRewriteForm");
  if (advancedRewriteForm) {
    advancedRewriteForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      await submitAdvancedGrammarRewrite();
      renderGrammar();
    });
  }

  const refreshGrammarReviewButton = document.getElementById("refreshGrammarReviewButton");
  if (refreshGrammarReviewButton) {
    refreshGrammarReviewButton.addEventListener("click", async () => {
      await loadGrammarReview();
      renderGrammar();
    });
  }

  document.querySelectorAll("[data-grammar-simulation-mode]").forEach((button) => {
    button.addEventListener("click", () => {
      state.grammarSimulation.mode = button.dataset.grammarSimulationMode;
      state.grammarSimulation.session = null;
      state.grammarSimulation.result = null;
      state.grammarSimulation.answers = {};
      saveState();
      renderGrammar();
    });
  });

  const startGrammarSimulationButton = document.getElementById("startGrammarSimulationButton");
  if (startGrammarSimulationButton) {
    startGrammarSimulationButton.addEventListener("click", async () => {
      await startGrammarSimulation();
      renderGrammar();
    });
  }

  document.querySelectorAll("[data-grammar-simulation-answer]").forEach((input) => {
    const eventName = input.tagName === "SELECT" ? "change" : "input";
    input.addEventListener(eventName, () => {
      state.grammarSimulation.answers[input.dataset.grammarSimulationAnswer] = input.value;
      state.grammarSimulation.result = null;
      saveState();
    });
  });

  const grammarSimulationForm = document.getElementById("grammarSimulationForm");
  if (grammarSimulationForm) {
    grammarSimulationForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      await submitGrammarSimulation();
      renderGrammar();
    });
  }
  bindContextualHelpButtons(document.getElementById("grammarView"));
}

function renderGrammarActiveSection(activeSection) {
  const sections = {
    menu: renderGrammarHub,
    breakdown: () => renderGrammarSectionShell(
      "Grammar Breakdown",
      "Bedah satu kalimat untuk menemukan subject, main verb, phrase, clause, dan makna Bahasa Indonesia.",
      grammarBreakdownPanel()
    ),
    basic_trainer: () => renderGrammarSectionShell(
      "Basic Grammar Trainer",
      "Latihan dasar: parts of speech, subject, verb, object, modal, dan pola kalimat sederhana.",
      basicGrammarTrainerPanel()
    ),
    intermediate_trainer: () => renderGrammarSectionShell(
      "Intermediate Grammar Trainer",
      "Latihan kalimat panjang: gerund, relative clause, reduced clause, passive voice, connector, dan parallel structure.",
      intermediateGrammarTrainerPanel()
    ),
    error_correction: () => renderGrammarSectionShell(
      "Grammar Error Correction",
      "Cari kesalahan grammar dan pilih corrected sentence yang benar.",
      grammarErrorCorrectionPanel()
    ),
    sentence_builder: () => renderGrammarSectionShell(
      "Grammar Sentence Builder",
      "Susun kata, lengkapi kalimat, gabungkan kalimat, dan tulis ulang kalimat BA.",
      grammarSentenceBuilderPanel()
    ),
    advanced_lab: () => renderGrammarSectionShell(
      "Advanced Grammar Lab",
      "Latihan grammar formal: nominalization, hedging, inversion, conditional, academic connector, dan formal BA writing.",
      grammarAdvancedLabPanel()
    ),
    review: () => renderGrammarSectionShell(
      "Grammar Review",
      "Lihat kelemahan grammar, pola salah berulang, dan rekomendasi latihan ulang.",
      grammarReviewPanel()
    ),
    simulation: () => renderGrammarSectionShell(
      "Grammar Simulation",
      "Uji kemampuan grammar melalui simulasi short, medium, atau full.",
      grammarSimulationPanel()
    )
  };
  return (sections[activeSection] || sections.menu)();
}

function renderGrammarHub() {
  return `
    <section class="module-surface">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Grammar Hub</p>
          <h2>Grammar Learning Path</h2>
          <p>Belajar grammar dari dasar sampai siap simulasi. Lihat status tiap module, lanjutkan rekomendasi, lalu kejar target finish.</p>
        </div>
        <span class="pill">8 langkah belajar</span>
      </div>
      ${renderGrammarProgressSummary()}
      ${renderGrammarStartHereCard()}
      ${renderGrammarLearningPathWithProgress()}
      ${renderGrammarFinishTarget()}
      ${renderGrammarQuickPick()}
    </section>
  `;
}

function renderGrammarProgressSummary() {
  const summary = getGrammarProgressSummary();
  const recommended = state.grammarProgress?.recommendedSection || {};
  return `
    <article class="module-card">
      <div class="section-heading compact">
        <div>
          <p class="eyebrow">Progress Grammar Kamu</p>
          <h3>${summary.progressPercent}% selesai · ${escapeHtml(summary.level)}</h3>
          <p>${escapeHtml(summary.nextAction || "Ikuti langkah yang direkomendasikan satu per satu.")}</p>
        </div>
        <span class="soft-pill">Finish: ${escapeHtml(summary.finishTarget || "Full Simulation 75%")}</span>
      </div>
      <div class="progress-bar" aria-label="Progress Grammar">
        <span style="width: ${clampPercent(summary.progressPercent)}%"></span>
      </div>
      <div class="module-grid three">
        <div class="module-card soft">
          <span>Overall Grammar Progress</span>
          <h3>${summary.progressPercent}%</h3>
        </div>
        <div class="module-card soft">
          <span>Active Module</span>
          <h3>${escapeHtml(recommended.title || grammarSectionMeta(summary.activeModule || "basic_trainer").title)}</h3>
        </div>
        <div class="module-card soft">
          <span>Completed Modules</span>
          <h3>${summary.completedModules}/${summary.totalModules}</h3>
        </div>
      </div>
    </article>
  `;
}

function renderGrammarStartHereCard() {
  const summary = getGrammarProgressSummary();
  const recommendedSection = getGrammarRecommendedSection();
  const recommendedMeta = grammarSectionMeta(recommendedSection);
  const recommended = state.grammarProgress?.recommendedSection || {};
  const hasStarted = summary.score > 0 || summary.completedTopics > 0;
  const beginnerCopy = hasStarted
    ? `Lanjutkan dari ${recommendedMeta.title}. ${recommended.reason || "Rekomendasi ini mengikuti progress grammar yang tersimpan."}`
    : "Belum tahu harus mulai dari mana? Mulai dari Basic Grammar Trainer. Di tahap ini kamu akan belajar menemukan subject, main verb, object, dan pola kalimat dasar.";
  return `
    <article class="module-card soft">
      <div class="section-heading compact">
        <div>
          <p class="eyebrow">Mulai dari Sini</p>
          <h3>Belajar terarah, satu langkah dulu</h3>
          <p>${escapeHtml(beginnerCopy)}</p>
        </div>
        <span class="soft-pill">${escapeHtml(summary.level)}</span>
      </div>
      <div class="module-grid three">
        <div class="stat-tile">
          <span>Level grammar</span>
          <strong>${escapeHtml(summary.level)}</strong>
        </div>
        <div class="stat-tile">
          <span>Progress</span>
          <strong>${summary.progressPercent}%</strong>
        </div>
        <div class="stat-tile">
          <span>Langkah berikutnya</span>
          <strong>${escapeHtml(recommendedMeta.title)}</strong>
        </div>
      </div>
      <button class="primary-button mt-3" type="button" data-grammar-hub-section="${escapeHtml(recommendedSection)}">Mulai Belajar Terarah</button>
    </article>
  `;
}

function renderGrammarLearningPath() {
  const steps = [
    {
      number: 1,
      title: "Basic Foundation",
      module: "Basic Grammar Trainer",
      description: "Belajar subject, verb, object, modal, dan pola kalimat sederhana.",
      target: "Paham siapa melakukan apa.",
      section: "basic_trainer",
      badge: "Mulai di sini"
    },
    {
      number: 2,
      title: "Sentence Breakdown",
      module: "Grammar Breakdown",
      description: "Bedah satu kalimat untuk menemukan inti kalimat dan phrase tambahan.",
      target: "Bisa menemukan main subject dan main verb.",
      section: "breakdown",
      badge: "Bedah kalimat"
    },
    {
      number: 3,
      title: "Intermediate Grammar",
      module: "Intermediate Grammar Trainer",
      description: "Latihan gerund, relative clause, reduced clause, passive voice, connector, dan parallel structure.",
      target: "Tidak bingung saat membaca kalimat panjang.",
      section: "intermediate_trainer",
      badge: "Kalimat panjang"
    },
    {
      number: 4,
      title: "Error Correction",
      module: "Grammar Error Correction",
      description: "Cari kesalahan grammar dan pilih corrected sentence yang benar.",
      target: "Bisa mengenali pola grammar yang salah.",
      section: "error_correction",
      badge: "Cari salah"
    },
    {
      number: 5,
      title: "Sentence Builder",
      module: "Grammar Sentence Builder",
      description: "Susun kata, lengkapi kalimat, gabungkan kalimat, dan tulis ulang kalimat BA.",
      target: "Bisa membuat kalimat sendiri.",
      section: "sentence_builder",
      badge: "Buat kalimat"
    },
    {
      number: 6,
      title: "Advanced Grammar",
      module: "Advanced Grammar Lab",
      description: "Latihan nominalization, hedging, conditional sentence, academic connector, dan formal BA writing.",
      target: "Bisa memahami kalimat akademik dan profesional.",
      section: "advanced_lab",
      badge: "Formal"
    },
    {
      number: 7,
      title: "Review Weakness",
      module: "Grammar Review",
      description: "Lihat kelemahan grammar dan pola salah yang sering berulang.",
      target: "Tahu bagian mana yang harus diulang.",
      section: "review",
      badge: "Review"
    },
    {
      number: 8,
      title: "Final Test",
      module: "Grammar Simulation",
      description: "Uji kemampuan grammar melalui simulasi short, medium, atau full.",
      target: "Finish jika full simulation minimal 75%.",
      section: "simulation",
      badge: "Finish line"
    }
  ];
  return `
    <div class="mt-4">
      <div class="section-heading compact">
        <div>
          <p class="eyebrow">Roadmap</p>
          <h3>Alur Belajar yang Disarankan</h3>
          <p>Ikuti urutan ini jika kamu masih pemula. Kamu tetap bisa lompat ke bagian lain saat butuh latihan tertentu.</p>
        </div>
      </div>
      <div class="module-grid two">
        ${steps.map((step) => grammarPathStepCard(step)).join("")}
      </div>
    </div>
  `;
}

function renderGrammarLearningPathWithProgress() {
  const path = state.grammarProgress?.learningPath?.length
    ? state.grammarProgress.learningPath
    : localGrammarPathModules();
  return `
    <div class="mt-4">
      <div class="section-heading compact">
        <div>
          <p class="eyebrow">Roadmap</p>
          <h3>Alur Belajar yang Disarankan</h3>
          <p>Setiap langkah sekarang punya status. Mulai dari yang direkomendasikan, ulangi yang lemah, lalu selesaikan simulasi.</p>
        </div>
      </div>
      <div class="module-grid two">
        ${path.map((step, index) => grammarPathStepCard({ step: step.step || index + 1, ...step })).join("")}
      </div>
    </div>
  `;
}

function renderGrammarFinishTarget() {
  const summary = getGrammarProgressSummary();
  const finish = state.grammarProgress?.finishStatus || {};
  const modules = getGrammarProgressModules();
  return `
    <article class="module-card mt-4">
      <div class="section-heading compact">
        <div>
          <p class="eyebrow">Target Finish Grammar</p>
          <h3>Target selesai yang jelas</h3>
          <p>${escapeHtml(finish.message || "Kamu dianggap selesai Grammar Lab jika sudah mampu menyelesaikan Full Grammar Simulation dengan skor minimal 75%. Jika belum sampai sana, cukup ikuti langkah yang direkomendasikan satu per satu.")}</p>
        </div>
        <span class="pill">${finish.is_finished ? "Finish" : `${summary.progressPercent}% progress`}</span>
      </div>
      <div class="tag-row">
        ${modules.map((module) => `<span class="soft-pill">${escapeHtml(module.title)} · ${getModuleStatusLabel(module.status)}</span>`).join("")}
      </div>
    </article>
  `;
}

function renderGrammarQuickPick() {
  const cards = [
    ["basic_trainer", "1. Basic Grammar Trainer", "Mulai dari fondasi: subject, verb, object, modal, dan simple sentence. Cocok untuk kamu yang masih bingung menentukan verb utama.", "Mulai di sini"],
    ["breakdown", "2. Grammar Breakdown", "Gunakan saat kamu menemukan kalimat panjang dan ingin tahu mana subject, main verb, phrase, clause, dan maknanya.", "Bedah Kalimat"],
    ["intermediate_trainer", "3. Intermediate Grammar Trainer", "Latihan membedakan main verb, -ing phrase, relative clause, passive voice, connector, dan parallel structure.", "Kalimat Panjang"],
    ["error_correction", "4. Error Correction", "Latihan menemukan grammar error seperti must be, subject-verb agreement, passive voice, dan connector yang salah.", "Cari Kesalahan"],
    ["sentence_builder", "5. Sentence Builder", "Latihan menyusun dan menulis kalimat sendiri agar kamu tidak hanya paham grammar, tetapi juga bisa menggunakannya.", "Buat Kalimat"],
    ["advanced_lab", "6. Advanced Grammar Lab", "Latihan grammar untuk kalimat TOEFL, akademik, dan Business Analyst formal seperti nominalization dan hedging.", "Formal & Akademik"],
    ["review", "7. Grammar Review", "Lihat pola salah yang sering muncul dan dapatkan rekomendasi latihan berikutnya.", "Ulangi Kelemahan"],
    ["simulation", "8. Grammar Simulation", "Uji seluruh kemampuan grammar. Target finish: Full Simulation minimal 75%.", "Finish Line"]
  ];
  return `
    <div class="mt-4">
      <div class="section-heading compact">
        <div>
          <p class="eyebrow">Pilih Cepat</p>
          <h3>Butuh fitur tertentu?</h3>
          <p>Pakai kartu ini kalau kamu sudah tahu bagian yang ingin dibuka.</p>
        </div>
      </div>
      <div class="module-grid two">
        ${cards.map(([section, title, description, badge]) => grammarHubCard(section, title, description, badge)).join("")}
      </div>
    </div>
  `;
}

function grammarPathStepCard(step) {
  const module = step.module_id ? step : getGrammarModuleBySection(step.section);
  const section = module.section || step.section;
  const title = step.title || module.title;
  const description = step.description || module.description;
  const target = step.target || module.next_action;
  const status = module.status || "not_started";
  const buttonLabel = getModuleButtonLabel(status);
  return `
    <article class="module-card soft">
      <div class="split-row">
        <span class="pill">${step.number || step.step}</span>
        <span class="soft-pill">${getModuleStatusLabel(status)}</span>
      </div>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(description)}</p>
      <div class="progress-bar" aria-label="Progress ${escapeHtml(title)}">
        <span style="width: ${clampPercent(module.progress_percent)}%"></span>
      </div>
      <p><strong>Progress:</strong> ${module.completed_items || 0}/${module.total_items || 0} · <strong>Last score:</strong> ${formatScore(module.last_score)}</p>
      <p><strong>Target:</strong> ${escapeHtml(target || "Ikuti latihan sampai mencapai target skor.")}</p>
      <button class="ghost-button" type="button" data-grammar-hub-section="${escapeHtml(section)}">${escapeHtml(buttonLabel)}</button>
    </article>
  `;
}

function grammarHubCard(section, title, description, badge) {
  const module = getGrammarModuleBySection(section);
  const status = module.status || "not_started";
  return `
    <article class="module-card soft">
      <div class="split-row">
        <span class="soft-pill">${escapeHtml(badge)}</span>
        <span class="soft-pill">${getModuleStatusLabel(status)}</span>
      </div>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(description)}</p>
      <div class="progress-bar" aria-label="Progress ${escapeHtml(title)}">
        <span style="width: ${clampPercent(module.progress_percent)}%"></span>
      </div>
      <p><strong>Progress:</strong> ${module.completed_items || 0}/${module.total_items || 0} · <strong>Last score:</strong> ${formatScore(module.last_score)}</p>
      <p>${escapeHtml(module.next_action || "Buka module ini untuk mulai latihan.")}</p>
      <button class="primary-button" type="button" data-grammar-hub-section="${escapeHtml(section)}">${escapeHtml(getModuleButtonLabel(status))}</button>
    </article>
  `;
}

function getGrammarRecommendedSection() {
  const progressRecommended = state.grammarProgress?.recommendedSection?.section;
  if (progressRecommended) return progressRecommended;
  const reviewPractice = state.grammarReview?.recommended_practice || null;
  const mappedReviewSection = mapGrammarRecommendationToSection(reviewPractice);
  if (mappedReviewSection) return mappedReviewSection;

  const summary = getGrammarProgressSummary();
  if (!summary.score || summary.score < 30) return "basic_trainer";
  if (summary.score < 50) return "breakdown";
  if (summary.score < 65) return "intermediate_trainer";
  if (summary.score < 75) return "error_correction";
  if (summary.score < 85) return "sentence_builder";
  return "simulation";
}

function getGrammarProgressSummary() {
  const progressSummary = state.grammarProgress?.summary;
  if (progressSummary) {
    return {
      score: Math.round(Number(progressSummary.grammar_score || 0)),
      level: progressSummary.grammar_level || "Basic 1 - Sentence Foundation",
      completedTopics: Number(progressSummary.completed_modules || 0),
      progressPercent: Math.round(Number(progressSummary.overall_progress_percent || 0)),
      activeModule: progressSummary.active_module || "basic_trainer",
      nextAction: progressSummary.next_action || "",
      finishTarget: progressSummary.finish_target || "Full Grammar Simulation minimal 75%",
      completedModules: Number(progressSummary.completed_modules || 0),
      totalModules: Number(progressSummary.total_modules || 8)
    };
  }
  const review = state.grammarReview || {};
  const weakness = review.weakness_summary || {};
  const journeySkills = Array.isArray(state.integratedJourney?.skills) ? state.integratedJourney.skills : [];
  const grammarSkill = journeySkills.find((skill) => skill.skill_type === "grammar") || {};
  const scoreCandidates = [
    weakness.average_grammar_score,
    state.grammarJourney?.grammar_score,
    grammarSkill.average_score,
    state.progress?.Grammar
  ].map((value) => Number(value)).filter((value) => Number.isFinite(value));
  const score = Math.max(0, Math.min(100, Math.round(scoreCandidates.find((value) => value >= 0) || 0)));
  const level = state.grammarJourney?.grammar_level
    || weakness.readiness_level
    || grammarSkill.current_level
    || (score >= 85 ? "Advanced 1 - Professional Grammar Usage" : score >= 50 ? "Intermediate 1 - Phrase and Clause Awareness" : "Basic 1 - Sentence Foundation");
  const completedTopics = Number(state.grammarJourney?.completed_topics || weakness.completed_grammar_attempts || grammarSkill.completed_count || 0);
  return {
    score,
    level,
    completedTopics,
    progressPercent: score,
    activeModule: score < 30 ? "basic_trainer" : score < 50 ? "breakdown" : score < 65 ? "intermediate_trainer" : score < 75 ? "error_correction" : score < 85 ? "sentence_builder" : "simulation",
    nextAction: "Ikuti langkah Grammar yang direkomendasikan.",
    finishTarget: "Full Grammar Simulation minimal 75%",
    completedModules: 0,
    totalModules: 8
  };
}

function getGrammarProgressModules() {
  const modules = state.grammarProgress?.modules || [];
  return modules.length ? modules : localGrammarPathModules();
}

function getGrammarModuleBySection(section) {
  return getGrammarProgressModules().find((module) => module.section === section) || {
    module_id: section,
    title: grammarSectionMeta(section).title,
    description: "",
    status: "not_started",
    progress_percent: 0,
    completed_items: 0,
    total_items: section === "simulation" ? 3 : 1,
    last_score: null,
    best_score: null,
    attempt_count: 0,
    next_action: "Mulai module ini untuk mencatat progress.",
    recommended: false,
    section
  };
}

function getModuleStatusLabel(status) {
  const labels = {
    not_started: "Belum mulai",
    in_progress: "Sedang berjalan",
    need_review: "Perlu diulang",
    completed: "Selesai",
    recommended: "Direkomendasikan",
    locked: "Belum dibuka"
  };
  return labels[status] || labels.not_started;
}

function getModuleButtonLabel(status) {
  const labels = {
    not_started: "Mulai",
    in_progress: "Lanjutkan",
    need_review: "Ulangi",
    completed: "Selesai",
    recommended: "Direkomendasikan",
    locked: "Belum dibuka"
  };
  return labels[status] || "Mulai";
}

function openGrammarModuleFromProgress(section) {
  setGrammarSection(section || "basic_trainer");
}

function clampPercent(value) {
  const number = Number(value || 0);
  return Math.max(0, Math.min(100, Math.round(number)));
}

function formatScore(score) {
  if (score === null || score === undefined || Number.isNaN(Number(score))) return "Belum ada";
  return `${Math.round(Number(score))}%`;
}

function localGrammarProgress() {
  const score = Number(state.progress?.Grammar || 0);
  const recommendedSection = score < 30 ? "basic_trainer" : score < 50 ? "breakdown" : score < 65 ? "intermediate_trainer" : score < 75 ? "error_correction" : score < 85 ? "sentence_builder" : "simulation";
  const modules = localGrammarPathModules().map((module) => ({
    ...module,
    status: module.section === recommendedSection ? "recommended" : module.status,
    recommended: module.section === recommendedSection
  }));
  return {
    summary: {
      overall_progress_percent: score,
      grammar_level: score >= 85 ? "Advanced 1 - Professional Grammar Usage" : score >= 50 ? "Intermediate 1 - Phrase and Clause Awareness" : "Basic 1 - Sentence Foundation",
      grammar_score: score,
      completed_modules: modules.filter((module) => module.status === "completed").length,
      total_modules: modules.length,
      active_module: recommendedSection,
      next_action: grammarSectionMeta(recommendedSection).title,
      finish_target: "Full Grammar Simulation minimal 75%"
    },
    modules,
    learningPath: modules.map((module, index) => ({ step: index + 1, ...module })),
    recommendedSection: {
      section: recommendedSection,
      title: grammarSectionMeta(recommendedSection).title,
      reason: "Fallback lokal: mulai dari langkah yang sesuai progress saat ini.",
      next_action: "Lanjutkan latihan Grammar yang direkomendasikan."
    },
    finishStatus: {
      is_finished: false,
      finish_rule: "Full Grammar Simulation minimal 75%",
      full_simulation_score: 0,
      message: "Belum finish. Ikuti rekomendasi berikutnya sampai siap full simulation minimal 75%."
    }
  };
}

function localGrammarPathModules() {
  const data = [
    ["basic_trainer", "Basic Grammar Trainer", "Latihan fondasi: subject, verb, object, modal, dan pola kalimat sederhana.", 7],
    ["breakdown", "Grammar Breakdown", "Bedah kalimat untuk menemukan subject, main verb, phrase, clause, dan makna Bahasa Indonesia.", 5],
    ["intermediate_trainer", "Intermediate Grammar Trainer", "Latihan kalimat panjang: gerund, relative clause, passive voice, connector, dan parallel structure.", 7],
    ["error_correction", "Grammar Error Correction", "Cari kesalahan grammar dan pilih corrected sentence yang benar.", 12],
    ["sentence_builder", "Grammar Sentence Builder", "Susun kata, lengkapi kalimat, gabungkan kalimat, dan tulis ulang kalimat BA.", 5],
    ["advanced_lab", "Advanced Grammar Lab", "Latihan grammar formal untuk TOEFL, akademik, dan Business Analyst writing.", 7],
    ["review", "Grammar Review", "Lihat kelemahan grammar, pola salah berulang, dan rekomendasi latihan ulang.", 1],
    ["simulation", "Grammar Simulation", "Uji kemampuan grammar melalui simulasi short, medium, atau full.", 3]
  ];
  return data.map(([section, title, description, total], index) => ({
    step: index + 1,
    module_id: section === "breakdown" ? "grammar_breakdown" : section,
    title,
    description,
    status: "not_started",
    progress_percent: 0,
    completed_items: 0,
    total_items: total,
    last_score: null,
    best_score: null,
    attempt_count: 0,
    next_action: "Mulai latihan ini untuk mengisi progress.",
    recommended: false,
    target_score: section === "simulation" ? 75 : 70,
    section
  }));
}

function mapGrammarRecommendationToSection(recommendation) {
  if (!recommendation) return null;
  const raw = [
    recommendation.recommended_module,
    recommendation.related_phase_module,
    recommendation.target_endpoint,
    recommendation.next_action,
    recommendation.reason
  ].filter(Boolean).join(" ").toLowerCase();
  if (!raw) return null;
  if (raw.includes("sentence-builder") || raw.includes("sentence builder") || raw.includes("grammar_sentence_builder")) return "sentence_builder";
  if (raw.includes("error-correction") || raw.includes("error correction")) return "error_correction";
  if (raw.includes("trainer/intermediate") || raw.includes("intermediate")) return "intermediate_trainer";
  if (raw.includes("trainer/basic") || raw.includes("basic")) return "basic_trainer";
  if (raw.includes("advanced") || raw.includes("formal_ba_writing") || raw.includes("nominalization")) return "advanced_lab";
  if (raw.includes("simulation")) return "simulation";
  if (raw.includes("review")) return "review";
  if (raw.includes("breakdown")) return "breakdown";
  return null;
}

function grammarSectionMeta(section) {
  const meta = {
    breakdown: { title: "Grammar Breakdown" },
    basic_trainer: { title: "Basic Grammar Trainer" },
    intermediate_trainer: { title: "Intermediate Grammar Trainer" },
    error_correction: { title: "Grammar Error Correction" },
    sentence_builder: { title: "Grammar Sentence Builder" },
    advanced_lab: { title: "Advanced Grammar Lab" },
    review: { title: "Grammar Review" },
    simulation: { title: "Grammar Simulation" }
  };
  return meta[section] || meta.basic_trainer;
}

function setGrammarSection(section) {
  state.grammarHub = {
    ...(state.grammarHub || {}),
    activeSection: section || "menu",
    activeSubTopic: null
  };
  saveState();
  renderGrammar();
  if ((section || "menu") === "menu") {
    refreshGrammarProgress().then(() => renderGrammar()).catch(() => {});
  }
}

function grammarBackButton() {
  return `<button class="ghost-button" type="button" data-grammar-back>Kembali ke Grammar Learning Path</button>`;
}

function renderGrammarSectionShell(title, subtitle, content) {
  return `
    <section class="module-surface">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Grammar Focus</p>
          <h2>${escapeHtml(title)}</h2>
          <p>${escapeHtml(subtitle)}</p>
        </div>
        ${grammarBackButton()}
      </div>
    </section>
    ${content}
  `;
}

function grammarSectionTitle(activeSection) {
  const titles = {
    breakdown: "Grammar Breakdown",
    basic_trainer: "Basic Grammar Trainer",
    intermediate_trainer: "Intermediate Grammar Trainer",
    error_correction: "Grammar Error Correction",
    sentence_builder: "Grammar Sentence Builder",
    advanced_lab: "Advanced Grammar Lab",
    review: "Grammar Review",
    simulation: "Grammar Simulation"
  };
  return titles[activeSection] || "Grammar Lab";
}

function grammarBreakdownPanel() {
  const grammarSample = "A business analyst operating within a complex enterprise environment must not only elicit requirements but also ensure alignment between stakeholder needs and organizational strategy.";
  return `
    <section class="module-grid two">
      <form id="grammarForm" class="module-surface form-grid">
        ${beginnerTip("Cara membaca grammar", "Cari subject dulu, lalu verb utama. Abaikan sementara phrase panjang yang hanya menambahkan informasi.")}
        <label>
          Kalimat
          <textarea id="grammarInput">${grammarSample}</textarea>
        </label>
        ${renderContextualHelpButton("grammar", "grammar_sentence", grammarSample)}
        <button class="ghost-button" id="grammarHelpButton" type="button">Bantu pahami grammar</button>
        <button class="primary-button" type="submit">Analyze Grammar</button>
      </form>
      <div id="grammarResult" class="module-surface grammar-result-panel">
        ${emptyStateTemplate("Hasil breakdown akan muncul di sini", "Submit satu kalimat untuk melihat Subject, Main Verb, Phrase, Pattern, dan terjemahan.")}
      </div>
    </section>
  `;
}

function grammarAnalysis(sentence) {
  const hasOperating = sentence.toLowerCase().includes("operating");
  const hasMust = sentence.toLowerCase().includes("must");
  return `
    <div class="grammar-breakdown-grid">
      ${grammarChip("Subject", "A business analyst")}
      ${grammarChip("Main Verb", hasMust ? "must elicit / must ensure" : "identify finite verb after subject")}
      ${grammarChip("Phrase", hasOperating ? "operating within a complex enterprise environment" : "modifier phrase around noun")}
      ${grammarChip("Pattern", "not only ... but also ...")}
    </div>
    <div class="module-card soft">
      <h3>Penjelasan sederhana</h3>
      <p>Bagian dengan -ing sering bukan verb utama. Dalam contoh ini, <strong>operating</strong> menjelaskan business analyst. Verb utama muncul bersama modal <strong>must</strong>.</p>
    </div>
    <div class="module-card">
      <h3>Terjemahan natural</h3>
      <p>Seorang business analyst yang bekerja dalam lingkungan enterprise kompleks harus menggali requirement dan memastikan keselarasan antara kebutuhan stakeholder dan strategi organisasi.</p>
    </div>
    <div class="module-card">
      <h3>Latihan serupa</h3>
      <p>The analyst working with multiple stakeholders must clarify priorities and document agreed requirements. ${renderContextualHelpButton("grammar", "grammar_sentence", "The analyst working with multiple stakeholders must clarify priorities and document agreed requirements.")}</p>
    </div>
  `;
}

function grammarApiTemplate(analysis) {
  const hasDeepFields = Boolean(analysis.sentence_level || analysis.grammar_patterns || analysis.structure_steps);
  return `
    <div class="grammar-breakdown-grid">
      ${grammarChip("Subject", analysis.subject)}
      ${grammarChip("Main Verb", analysis.mainVerb)}
      ${grammarChip("Phrase", analysis.phrase)}
      ${grammarChip("Pattern", analysis.pattern)}
      ${hasDeepFields ? grammarChip("Level", analysis.sentence_level) : ""}
      ${hasDeepFields ? grammarChip("Type", analysis.sentence_type) : ""}
    </div>
    <div class="module-card soft">
      <h3>Penjelasan sederhana</h3>
      <p>${analysis.explanation} ${renderContextualHelpButton("grammar", "grammar_explanation", analysis.explanation)}</p>
    </div>
    <div class="module-card">
      <h3>Terjemahan natural</h3>
      <p>${analysis.translation}</p>
    </div>
    ${hasDeepFields ? `
      <div class="module-card">
        <h3>Deep Grammar Breakdown</h3>
        <div class="grammar-breakdown-grid">
          ${grammarChip("Main Subject", analysis.main_subject)}
          ${grammarChip("Main Verb", analysis.main_verb)}
          ${grammarChip("Object/Complement", analysis.object_or_complement)}
          ${grammarChip("Recommended Topic", analysis.recommended_topic_id)}
        </div>
      </div>
      ${analysis.simple_meaning_id ? `
        <div class="module-card soft">
          <h3>Arti sederhana</h3>
          <p>${escapeHtml(analysis.simple_meaning_id)}</p>
        </div>
      ` : ""}
      ${analysis.ba_context_meaning ? `
        <div class="module-card">
          <h3>Makna dalam konteks BA</h3>
          <p>${escapeHtml(analysis.ba_context_meaning)}</p>
        </div>
      ` : ""}
      ${grammarDeepList("Modifier Phrases", analysis.modifier_phrases, (item) => `<strong>${escapeHtml(item.text || "-")}</strong><p>${escapeHtml(item.explanation_id || item.function || "")}</p><small>${escapeHtml(item.function || "")}</small>`)}
      ${grammarDeepList("Clauses", analysis.clauses, (item) => `<strong>${escapeHtml(item.type || "-")}</strong><p>${escapeHtml(item.text || "")}</p><small>${escapeHtml(item.explanation_id || "")}</small>`)}
      ${grammarSimpleList("Grammar Patterns", analysis.grammar_patterns)}
      ${analysis.common_trap ? `
        <div class="module-card">
          <h3>Common Trap</h3>
          <p>${escapeHtml(analysis.common_trap)}</p>
        </div>
      ` : ""}
      ${grammarSimpleList("Langkah memahami struktur", analysis.structure_steps)}
      ${grammarSimpleList("Detected Keywords", analysis.detected_keywords)}
      <div class="module-card soft">
        <h3>Next Practice</h3>
        <p>${escapeHtml(analysis.next_practice || "Practice Subject and Verb foundation.")}</p>
        <small>${escapeHtml(analysis.confidence_note || "")}</small>
      </div>
    ` : ""}
  `;
}

function grammarDeepList(title, items, renderItem) {
  if (!Array.isArray(items) || !items.length) return "";
  return `
    <div class="module-card">
      <h3>${escapeHtml(title)}</h3>
      <div class="module-card-list">
        ${items.map((item) => `<div class="case-box soft">${renderItem(item)}</div>`).join("")}
      </div>
    </div>
  `;
}

function grammarSimpleList(title, items) {
  if (!Array.isArray(items) || !items.length) return "";
  return `
    <div class="module-card">
      <h3>${escapeHtml(title)}</h3>
      <div class="helper-list">
        ${items.map((item) => `<span class="soft-pill">${escapeHtml(item)}</span>`).join("")}
      </div>
    </div>
  `;
}

function grammarChip(label, value) {
  return `
    <article class="grammar-chip">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value || "-")}</strong>
    </article>
  `;
}

function basicGrammarTrainerPanel() {
  const topics = state.grammarTrainer.topics?.length ? state.grammarTrainer.topics : localBasicGrammarTrainerTopics();
  const trainer = state.grammarTrainer.trainer || localBasicGrammarTrainer(state.grammarTrainer.selectedTopic || "subject_verb");
  const result = state.grammarTrainer.result;
  return `
    <section class="module-surface">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Basic Grammar Trainer</p>
          <h2>Latihan grammar dasar bertahap</h2>
          <p>Pilih topic, baca contoh, lalu jawab quiz pendek. Skor akan masuk ke Grammar Journey jika backend aktif.</p>
        </div>
        <span class="pill">Learn -> Practice -> Quiz</span>
      </div>
      <div class="quick-actions">
        ${topics.map((topic) => `
          <button class="ghost-button ${topic.topic_id === trainer.topic_id ? "selected-control" : ""}" type="button" data-grammar-trainer-topic="${escapeHtml(topic.topic_id)}">
            ${escapeHtml(topic.title)}
          </button>
        `).join("")}
      </div>
      <div class="module-grid two">
        <article class="module-card soft">
          <span class="soft-pill">${escapeHtml(trainer.level)} · ${escapeHtml(trainer.title)}</span>
          <h3>${escapeHtml(trainer.learning_objective)}</h3>
          <p>${escapeHtml(trainer.explanation_id)}</p>
          <p><strong>Tips pemula:</strong> ${escapeHtml(trainer.beginner_tip)}</p>
          <p><strong>Konteks BA:</strong> ${escapeHtml(trainer.ba_context)}</p>
        </article>
        <article class="module-card">
          <h3>Contoh breakdown</h3>
          ${(trainer.examples || []).map((item) => `
            <div class="case-box soft">
              <p><strong>${escapeHtml(item.sentence)}</strong> ${renderContextualHelpButton("grammar", "grammar_sentence", item.sentence)}</p>
              <p>${escapeHtml(item.simple_meaning_id)}</p>
              <small>${escapeHtml(item.grammar_focus)}</small>
              <div class="grammar-breakdown-grid">
                ${Object.entries(item.breakdown || {}).map(([key, value]) => grammarChip(labelFromKey(key), value)).join("")}
              </div>
            </div>
          `).join("")}
        </article>
      </div>
      <div class="module-grid two">
        <article class="module-card">
          <h3>Guided Practice</h3>
          ${(trainer.guided_items || []).map((item) => `
            <div class="case-box soft">
              <span class="soft-pill">${escapeHtml(item.target_part)}</span>
              <p><strong>${escapeHtml(item.instruction_id)}</strong></p>
              <p>${escapeHtml(item.sentence)} ${renderContextualHelpButton("grammar", "grammar_sentence", item.sentence)}</p>
              <p><strong>Jawaban:</strong> ${escapeHtml(item.correct_answer)}</p>
              <p>${escapeHtml(item.explanation_id)}</p>
              <small>${escapeHtml(item.beginner_tip)}</small>
            </div>
          `).join("")}
        </article>
        <form id="basicGrammarTrainerForm" class="module-card">
          <h3>Quiz pendek</h3>
          ${(trainer.quiz_items || []).map((item) => `
            <label>
              ${escapeHtml(item.instruction_id)}
              <span class="muted">${escapeHtml(item.sentence)}</span>
              <strong>${escapeHtml(item.question)}</strong>
              <select data-grammar-quiz-answer="${escapeHtml(item.id)}">
                <option value="">Pilih jawaban</option>
                ${(item.options || []).map((option) => `<option value="${escapeHtml(option)}" ${state.grammarTrainer.answers?.[item.id] === option ? "selected" : ""}>${escapeHtml(option)}</option>`).join("")}
              </select>
            </label>
          `).join("")}
          <button class="primary-button" type="submit">Submit Basic Trainer</button>
          ${result ? grammarTrainerResultTemplate(result) : emptyStateTemplate("Belum submit quiz", "Pilih jawaban pada quiz pendek, lalu submit untuk melihat skor dan rekomendasi.")}
        </form>
      </div>
    </section>
  `;
}

async function loadBasicGrammarTrainer(topicId = "subject_verb") {
  const selectedTopic = topicId || "subject_verb";
  if (apiOnline) {
    try {
      const [topicsResponse, trainerResponse] = await Promise.all([
        apiRequest("/grammar/trainer/basic"),
        apiRequest(`/grammar/trainer/basic/${encodeURIComponent(selectedTopic)}`)
      ]);
      state.grammarTrainer = {
        selectedTopic,
        topics: topicsResponse.topics || [],
        trainer: trainerResponse.trainer,
        answers: {},
        result: null
      };
      saveState();
      return;
    } catch (error) {
      apiOnline = false;
    }
  }
  state.grammarTrainer = {
    selectedTopic,
    topics: localBasicGrammarTrainerTopics(),
    trainer: localBasicGrammarTrainer(selectedTopic),
    answers: {},
    result: null
  };
  saveState();
}

async function submitBasicGrammarTrainer() {
  const topicId = state.grammarTrainer.selectedTopic || "subject_verb";
  if (apiOnline) {
    try {
      const response = await apiRequest("/grammar/trainer/basic/submit", {
        method: "POST",
        body: {
          user_id: state.user?.id || "default-user",
          topic_id: topicId,
          answers: state.grammarTrainer.answers || {}
        }
      });
      state.grammarTrainer.result = response;
      await refreshIntegratedJourney();
      await refreshGrammarProgress();
      saveState();
      return;
    } catch (error) {
      apiOnline = false;
    }
  }
  const trainer = state.grammarTrainer.trainer || localBasicGrammarTrainer(topicId);
  const details = (trainer.quiz_items || []).map((item) => {
    const userAnswer = state.grammarTrainer.answers?.[item.id] || "";
    return {
      question_id: item.id,
      is_correct: userAnswer === item.correct_answer,
      user_answer: userAnswer,
      correct_answer: item.correct_answer,
      explanation_id: item.explanation_id
    };
  });
  const correctCount = details.filter((item) => item.is_correct).length;
  const totalQuestions = details.length || 1;
  const score = Math.round((correctCount / totalQuestions) * 100);
  state.grammarTrainer.result = {
    result: {
      topic_id: topicId,
      score,
      max_score: 100,
      correct_count: correctCount,
      total_questions: details.length,
      is_passed: score >= 70,
      details
    },
    recommendation: {
      next_action: score >= 70 ? "Lanjut ke topic Basic berikutnya." : "Ulangi contoh dan guided practice dulu.",
      next_topic_id: "object_complement",
      mentor_message: score >= 70 ? "Bagus. Kamu sudah memahami latihan dasar ini." : "Tidak apa-apa. Ulangi pelan-pelan dari subject dan verb."
    }
  };
  saveState();
}

function grammarTrainerResultTemplate(response) {
  const result = response.result || {};
  const recommendation = response.recommendation || {};
  return `
    <div class="alert ${result.is_passed ? "success" : "warning"}">
      <strong>Score ${Math.round(result.score || 0)}/${result.max_score || 100}</strong>
      <p>${escapeHtml(recommendation.mentor_message || "Quiz selesai.")}</p>
      <p>${escapeHtml(recommendation.next_action || "")}</p>
    </div>
    <div class="module-card-list">
      ${(result.details || []).map((item) => `
        <div class="case-box ${item.is_correct ? "soft" : ""}">
          <strong>${item.is_correct ? "Benar" : "Perlu review"} · ${escapeHtml(item.question_id)}</strong>
          <p>Jawaban Anda: ${escapeHtml(item.user_answer || "-")}</p>
          <p>Jawaban benar: ${escapeHtml(item.correct_answer || "-")}</p>
          <small>${escapeHtml(item.explanation_id || "")}</small>
        </div>
      `).join("")}
    </div>
  `;
}

function intermediateGrammarTrainerPanel() {
  const data = state.intermediateGrammarTrainer;
  const topics = data.topics?.length ? data.topics : localIntermediateGrammarTrainerTopics();
  const trainer = data.trainer || localIntermediateGrammarTrainer(data.selectedTopic || "gerund_vs_main_verb");
  const result = data.result;
  return `
    <section class="module-surface">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Intermediate Grammar Trainer</p>
          <h2>Latihan kalimat panjang TOEFL + BA</h2>
          <p>Fokus pada jebakan grammar: -ing bukan main verb, relative clause, passive voice, parallel structure, dan connector logic.</p>
        </div>
        <span class="pill">Trap-aware practice</span>
      </div>
      <div class="quick-actions">
        ${topics.map((topic) => `
          <button class="ghost-button ${topic.topic_id === trainer.topic_id ? "selected-control" : ""}" type="button" data-intermediate-grammar-topic="${escapeHtml(topic.topic_id)}">
            ${escapeHtml(topic.title)}
          </button>
        `).join("")}
      </div>
      <div class="module-grid two">
        <article class="module-card soft">
          <span class="soft-pill">${escapeHtml(trainer.level)} · ${escapeHtml(trainer.title)}</span>
          <h3>${escapeHtml(trainer.learning_objective)}</h3>
          <p>${escapeHtml(trainer.explanation_id)}</p>
          <p><strong>Common trap:</strong> ${escapeHtml(trainer.common_trap || "")}</p>
          <p><strong>Tips:</strong> ${escapeHtml(trainer.beginner_tip)}</p>
          <p><strong>Konteks BA:</strong> ${escapeHtml(trainer.ba_context)}</p>
        </article>
        <article class="module-card">
          <h3>Contoh intermediate breakdown</h3>
          ${(trainer.examples || []).map((item) => `
            <div class="case-box soft">
              <p><strong>${escapeHtml(item.sentence)}</strong> ${renderContextualHelpButton("grammar", "grammar_sentence", item.sentence)}</p>
              <p>${escapeHtml(item.simple_meaning_id)}</p>
              <small>${escapeHtml(item.grammar_focus)}</small>
              <p><strong>Mengapa membingungkan:</strong> ${escapeHtml(item.why_it_is_confusing || "")}</p>
              <div class="grammar-breakdown-grid">
                ${Object.entries(item.breakdown || {}).map(([key, value]) => grammarChip(labelFromKey(key), value)).join("")}
              </div>
            </div>
          `).join("")}
        </article>
      </div>
      <div class="module-grid two">
        <article class="module-card">
          <h3>Guided + Trap Practice</h3>
          ${(trainer.guided_items || []).map((item) => intermediatePracticeCard(item)).join("")}
          ${(trainer.trap_items || []).map((item) => `
            <div class="case-box">
              <span class="soft-pill">${escapeHtml(item.trap_type)}</span>
              <p><strong>${escapeHtml(item.question)}</strong></p>
              <p>${escapeHtml(item.sentence)}</p>
              <p><strong>Jawaban:</strong> ${escapeHtml(item.correct_answer)}</p>
              <p>${escapeHtml(item.explanation_id)}</p>
            </div>
          `).join("")}
        </article>
        <form id="intermediateGrammarTrainerForm" class="module-card">
          <h3>Quiz + Trap Check</h3>
          ${[...(trainer.quiz_items || []), ...(trainer.trap_items || [])].map((item) => `
            <label>
              ${escapeHtml(item.instruction_id || item.trap_type || "Trap check")}
              <span class="muted">${escapeHtml(item.sentence)}</span>
              <strong>${escapeHtml(item.question)}</strong>
              <select data-intermediate-grammar-answer="${escapeHtml(item.id)}">
                <option value="">Pilih jawaban</option>
                ${(item.options || []).map((option) => `<option value="${escapeHtml(option)}" ${data.answers?.[item.id] === option ? "selected" : ""}>${escapeHtml(option)}</option>`).join("")}
              </select>
            </label>
          `).join("")}
          <button class="primary-button" type="submit">Submit Intermediate Trainer</button>
          ${result ? grammarTrainerResultTemplate(result) : emptyStateTemplate("Belum submit intermediate quiz", "Jawab quiz dan trap check untuk melihat skor, mistakes, dan rekomendasi.")}
        </form>
      </div>
    </section>
  `;
}

function intermediatePracticeCard(item) {
  return `
    <div class="case-box soft">
      <span class="soft-pill">${escapeHtml(item.target_part)}</span>
      <p><strong>${escapeHtml(item.instruction_id)}</strong></p>
      <p>${escapeHtml(item.sentence)} ${renderContextualHelpButton("grammar", "grammar_sentence", item.sentence)}</p>
      <p><strong>Jawaban:</strong> ${escapeHtml(item.correct_answer)}</p>
      <p>${escapeHtml(item.explanation_id)}</p>
      <small>${escapeHtml(item.common_trap || item.beginner_tip || "")}</small>
    </div>
  `;
}

async function loadIntermediateGrammarTrainer(topicId = "gerund_vs_main_verb") {
  const selectedTopic = topicId || "gerund_vs_main_verb";
  if (apiOnline) {
    try {
      const [topicsResponse, trainerResponse] = await Promise.all([
        apiRequest("/grammar/trainer/intermediate"),
        apiRequest(`/grammar/trainer/intermediate/${encodeURIComponent(selectedTopic)}`)
      ]);
      state.intermediateGrammarTrainer = {
        selectedTopic,
        topics: topicsResponse.topics || [],
        trainer: trainerResponse.trainer,
        answers: {},
        result: null
      };
      saveState();
      return;
    } catch (error) {
      apiOnline = false;
    }
  }
  state.intermediateGrammarTrainer = {
    selectedTopic,
    topics: localIntermediateGrammarTrainerTopics(),
    trainer: localIntermediateGrammarTrainer(selectedTopic),
    answers: {},
    result: null
  };
  saveState();
}

async function submitIntermediateGrammarTrainer() {
  const topicId = state.intermediateGrammarTrainer.selectedTopic || "gerund_vs_main_verb";
  if (apiOnline) {
    try {
      const response = await apiRequest("/grammar/trainer/intermediate/submit", {
        method: "POST",
        body: {
          user_id: state.user?.id || "default-user",
          topic_id: topicId,
          answers: state.intermediateGrammarTrainer.answers || {}
        }
      });
      state.intermediateGrammarTrainer.result = response;
      await refreshIntegratedJourney();
      await refreshGrammarProgress();
      saveState();
      return;
    } catch (error) {
      apiOnline = false;
    }
  }
  const trainer = state.intermediateGrammarTrainer.trainer || localIntermediateGrammarTrainer(topicId);
  const items = [...(trainer.quiz_items || []), ...(trainer.trap_items || [])];
  const details = items.map((item) => {
    const userAnswer = state.intermediateGrammarTrainer.answers?.[item.id] || "";
    return {
      question_id: item.id,
      is_correct: userAnswer === item.correct_answer,
      user_answer: userAnswer,
      correct_answer: item.correct_answer,
      explanation_id: item.explanation_id
    };
  });
  const correctCount = details.filter((item) => item.is_correct).length;
  const totalQuestions = details.length || 1;
  const score = Math.round((correctCount / totalQuestions) * 100);
  state.intermediateGrammarTrainer.result = {
    result: {
      topic_id: topicId,
      level: "intermediate",
      score,
      max_score: 100,
      correct_count: correctCount,
      total_questions: details.length,
      is_passed: score >= 70,
      details,
      mistakes: details.filter((item) => !item.is_correct)
    },
    recommendation: {
      next_action: score >= 70 ? "Lanjut ke topic intermediate berikutnya." : "Ulangi trap item sebelum lanjut.",
      next_topic_id: topicId,
      mentor_message: score >= 70 ? "Bagus. Kamu mulai menguasai kalimat panjang." : "Fokus dulu membedakan main verb dan phrase tambahan.",
      review_topic_id: topicId
    }
  };
  saveState();
}

function localIntermediateGrammarTrainerTopics() {
  return [
    { topic_id: "gerund_vs_main_verb", title: "Gerund vs Main Verb", level: "intermediate", learning_objective: "Bedakan -ing phrase dan main verb.", estimated_minutes: 12 },
    { topic_id: "relative_clause", title: "Relative Clause", level: "intermediate", learning_objective: "Pahami clause yang menjelaskan noun.", estimated_minutes: 12 },
    { topic_id: "passive_voice", title: "Passive Voice", level: "intermediate", learning_objective: "Kenali be + V3.", estimated_minutes: 12 }
  ];
}

function localIntermediateGrammarTrainer(topicId = "gerund_vs_main_verb") {
  return {
    topic_id: topicId,
    level: "intermediate",
    title: topicId === "passive_voice" ? "Passive Voice" : topicId === "relative_clause" ? "Relative Clause" : "Gerund vs Main Verb",
    learning_objective: "Latihan memahami kalimat panjang TOEFL + BA.",
    explanation_id: "Pisahkan main subject, modifier phrase, dan main verb.",
    beginner_tip: "Cari main verb setelah subject utama.",
    common_trap: "Jangan menganggap semua kata -ing sebagai main verb.",
    ba_context: "Dipakai dalam requirement, process, dan stakeholder analysis.",
    examples: [
      {
        sentence: "The analyst working with stakeholders must clarify priorities.",
        simple_meaning_id: "Analis yang bekerja dengan stakeholder harus memperjelas prioritas.",
        grammar_focus: "Reduced phrase + modal verb",
        breakdown: { main_subject: "The analyst", modifier_phrase: "working with stakeholders", main_verb: "must clarify", object: "priorities" },
        why_it_is_confusing: "working terlihat seperti verb, tetapi hanya modifier.",
        ba_context_note: "Menjelaskan tugas BA dengan stakeholder."
      }
    ],
    guided_items: [
      {
        id: `${topicId}_guided_1`,
        instruction_id: "Pilih main verb.",
        sentence: "The analyst working with stakeholders must clarify priorities.",
        target_part: "main_verb",
        options: ["working", "must clarify", "stakeholders", "priorities"],
        correct_answer: "must clarify",
        explanation_id: "Main verb adalah must clarify.",
        common_trap: "working bukan main verb.",
        beginner_tip: "Cari modal must."
      }
    ],
    quiz_items: [
      {
        id: `${topicId}_quiz_1`,
        question_type: "identify_main_verb",
        instruction_id: "Pilih main verb.",
        sentence: "The analyst working with stakeholders must clarify priorities.",
        question: "Mana main verb?",
        options: ["working", "must clarify", "stakeholders", "priorities"],
        correct_answer: "must clarify",
        explanation_id: "Main verb adalah must clarify.",
        difficulty: "intermediate",
        grammar_trap: "working hanya modifier.",
        ba_context_note: "BA perlu clarify priorities.",
        recommended_review_topic: topicId
      }
    ],
    trap_items: [
      {
        id: `${topicId}_trap_1`,
        trap_type: "ing_as_main_verb",
        incorrect_assumption: "working adalah main verb",
        sentence: "The analyst working with stakeholders must clarify priorities.",
        question: "Why is working not the main verb?",
        options: ["Because it is only describing the analyst", "Because it is the object", "Because it is a noun"],
        correct_answer: "Because it is only describing the analyst",
        explanation_id: "working with stakeholders menjelaskan analyst.",
        why_wrong_answers_are_wrong: ["Object adalah priorities.", "working bukan noun di sini."]
      }
    ]
  };
}

function grammarErrorCorrectionPanel() {
  const data = state.grammarErrorCorrection;
  const categories = data.categories?.length ? data.categories : localGrammarErrorCategories();
  const category = data.category || localGrammarErrorCategory(data.selectedErrorType || "missing_be_after_modal");
  const items = data.items?.length ? data.items : localGrammarErrorItems(category.error_type);
  const result = data.result;
  return `
    <section class="module-surface">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Grammar Error Correction</p>
          <h2>Perbaiki kalimat yang salah</h2>
          <p>Pilih jenis error, pahami aturan, lalu pilih kalimat yang benar. Fokusnya adalah tahu kenapa kalimat salah.</p>
        </div>
        <span class="pill">Error -> Rule -> Correction</span>
      </div>
      <div class="quick-actions">
        ${categories.map((item) => `
          <button class="ghost-button ${item.error_type === category.error_type ? "selected-control" : ""}" type="button" data-grammar-error-type="${escapeHtml(item.error_type)}">
            ${escapeHtml(item.title)}
          </button>
        `).join("")}
      </div>
      <div class="module-grid two">
        <article class="module-card soft">
          <span class="soft-pill">${escapeHtml(category.level)} · ${escapeHtml(category.error_type)}</span>
          <h3>${escapeHtml(category.title)}</h3>
          <p>${escapeHtml(category.learning_objective)}</p>
          <p><strong>Aturan:</strong> ${escapeHtml(category.explanation_id)}</p>
          <p><strong>Trap:</strong> ${escapeHtml(category.common_trap)}</p>
          <p><strong>Konteks BA:</strong> ${escapeHtml(category.ba_context)}</p>
        </article>
        <article class="module-card">
          <h3>Contoh koreksi</h3>
          ${(category.examples || []).map((item) => `
            <div class="case-box soft">
              <p><strong>Salah:</strong> ${escapeHtml(item.incorrect_sentence)}</p>
              <p><strong>Benar:</strong> ${escapeHtml(item.corrected_sentence)}</p>
              <p>${escapeHtml(item.why_wrong_id)}</p>
              <small>${escapeHtml(item.correction_rule_id)}</small>
            </div>
          `).join("")}
        </article>
      </div>
      <form id="grammarErrorCorrectionForm" class="module-card">
        <h3>Correction quiz</h3>
        ${items.map((item) => `
          <label>
            ${escapeHtml(item.instruction_id)}
            <span class="muted">Salah: ${escapeHtml(item.incorrect_sentence)}</span>
            <strong>${escapeHtml(item.question)}</strong>
            <select data-grammar-error-answer="${escapeHtml(item.id)}">
              <option value="">Pilih jawaban</option>
              ${(item.options || []).map((option) => `<option value="${escapeHtml(option)}" ${data.answers?.[item.id] === option ? "selected" : ""}>${escapeHtml(option)}</option>`).join("")}
            </select>
            <small>${escapeHtml(item.hint_id || "")}</small>
          </label>
        `).join("")}
        <button class="primary-button" type="submit">Submit Error Correction</button>
        ${result ? grammarErrorCorrectionResultTemplate(result) : emptyStateTemplate("Belum submit correction", "Pilih kalimat yang benar untuk melihat skor, corrected sentence, dan rekomendasi.")}
      </form>
    </section>
  `;
}

async function loadGrammarErrorCorrection(errorType = "missing_be_after_modal") {
  const selectedErrorType = errorType || "missing_be_after_modal";
  if (apiOnline) {
    try {
      const [categoriesResponse, detailResponse] = await Promise.all([
        apiRequest("/grammar/error-correction/categories"),
        apiRequest(`/grammar/error-correction/${encodeURIComponent(selectedErrorType)}`)
      ]);
      state.grammarErrorCorrection = {
        selectedErrorType,
        categories: categoriesResponse.categories || [],
        category: detailResponse.category,
        items: detailResponse.items || [],
        answers: {},
        result: null
      };
      saveState();
      return;
    } catch (error) {
      apiOnline = false;
    }
  }
  const category = localGrammarErrorCategory(selectedErrorType);
  state.grammarErrorCorrection = {
    selectedErrorType,
    categories: localGrammarErrorCategories(),
    category,
    items: localGrammarErrorItems(selectedErrorType),
    answers: {},
    result: null
  };
  saveState();
}

async function submitGrammarErrorCorrection() {
  const errorType = state.grammarErrorCorrection.selectedErrorType || "missing_be_after_modal";
  if (apiOnline) {
    try {
      const response = await apiRequest("/grammar/error-correction/submit", {
        method: "POST",
        body: {
          user_id: state.user?.id || "default-user",
          error_type: errorType,
          answers: state.grammarErrorCorrection.answers || {}
        }
      });
      state.grammarErrorCorrection.result = response;
      await refreshIntegratedJourney();
      await refreshGrammarProgress();
      saveState();
      return;
    } catch (error) {
      apiOnline = false;
    }
  }
  const items = state.grammarErrorCorrection.items?.length ? state.grammarErrorCorrection.items : localGrammarErrorItems(errorType);
  const details = items.map((item) => {
    const userAnswer = state.grammarErrorCorrection.answers?.[item.id] || "";
    return {
      item_id: item.id,
      is_correct: userAnswer === item.correct_answer,
      user_answer: userAnswer,
      correct_answer: item.correct_answer,
      incorrect_sentence: item.incorrect_sentence,
      corrected_sentence: item.corrected_sentence,
      explanation_id: item.explanation_id
    };
  });
  const correctCount = details.filter((item) => item.is_correct).length;
  const totalQuestions = details.length || 1;
  const score = Math.round((correctCount / totalQuestions) * 100);
  state.grammarErrorCorrection.result = {
    result: {
      score,
      max_score: 100,
      correct_count: correctCount,
      total_questions: details.length,
      is_passed: score >= 70,
      details,
      mistakes: details.filter((item) => !item.is_correct)
    },
    recommendation: {
      next_action: score >= 70 ? "Lanjut ke error type berikutnya." : "Ulangi aturan dan corrected sentence dulu.",
      review_error_type: errorType,
      review_topic_id: "modal_verb",
      mentor_message: score >= 70 ? "Bagus. Kamu mulai bisa mengenali grammar error umum." : "Pelan-pelan. Bandingkan kalimat salah dan benar."
    }
  };
  saveState();
}

function grammarErrorCorrectionResultTemplate(response) {
  const result = response.result || {};
  const recommendation = response.recommendation || {};
  return `
    <div class="alert ${result.is_passed ? "success" : "warning"}">
      <strong>Score ${Math.round(result.score || 0)}/${result.max_score || 100}</strong>
      <p>${escapeHtml(recommendation.mentor_message || "Correction selesai.")}</p>
      <p>${escapeHtml(recommendation.next_action || "")}</p>
    </div>
    <div class="module-card-list">
      ${(result.details || []).map((item) => `
        <div class="case-box ${item.is_correct ? "soft" : ""}">
          <strong>${item.is_correct ? "Benar" : "Perlu koreksi"} · ${escapeHtml(item.item_id)}</strong>
          <p><strong>Salah:</strong> ${escapeHtml(item.incorrect_sentence || "-")}</p>
          <p><strong>Jawaban Anda:</strong> ${escapeHtml(item.user_answer || "-")}</p>
          <p><strong>Corrected:</strong> ${escapeHtml(item.corrected_sentence || item.correct_answer || "-")}</p>
          <small>${escapeHtml(item.explanation_id || "")}</small>
        </div>
      `).join("")}
    </div>
  `;
}

function localGrammarErrorCategories() {
  return [
    { error_type: "missing_be_after_modal", level: "basic", title: "Missing be after modal", learning_objective: "Gunakan must be + adjective.", related_topic_id: "modal_verb" },
    { error_type: "subject_verb_agreement", level: "basic", title: "Subject-Verb Agreement", learning_objective: "Cocokkan subject dan verb.", related_topic_id: "subject_verb" },
    { error_type: "passive_voice_error", level: "intermediate", title: "Passive Voice Error", learning_objective: "Gunakan be + V3.", related_topic_id: "passive_voice" }
  ];
}

function localGrammarErrorCategory(errorType = "missing_be_after_modal") {
  const match = localGrammarErrorCategories().find((item) => item.error_type === errorType) || localGrammarErrorCategories()[0];
  return {
    ...match,
    explanation_id: "Pilih struktur grammar yang benar dan bandingkan dengan kalimat salah.",
    beginner_tip: "Cari subject, modal/verb, lalu bentuk kata setelahnya.",
    common_trap: "Pemula sering menerjemahkan langsung dari Bahasa Indonesia.",
    ba_context: "Error correction membantu requirement dan report writing lebih profesional.",
    examples: [
      {
        incorrect_sentence: "The system must flexible for all users.",
        corrected_sentence: "The system must be flexible for all users.",
        why_wrong_id: "Setelah must dan sebelum adjective flexible, perlu be.",
        correction_rule_id: "Subject + modal + be + adjective"
      }
    ]
  };
}

function localGrammarErrorItems(errorType = "missing_be_after_modal") {
  const category = localGrammarErrorCategory(errorType);
  return [
    {
      id: `${errorType}_1`,
      error_type: errorType,
      level: category.level,
      instruction_id: "Pilih perbaikan kalimat yang paling tepat.",
      incorrect_sentence: "The system must flexible for all users.",
      question: "Which sentence is correct?",
      options: ["The system must flexible for all users.", "The system must be flexible for all users.", "The system must is flexible for all users."],
      correct_answer: "The system must be flexible for all users.",
      corrected_sentence: "The system must be flexible for all users.",
      explanation_id: "Setelah modal must, gunakan be sebelum adjective.",
      hint_id: "must + be + adjective",
      related_topic_id: category.related_topic_id
    }
  ];
}

function grammarSentenceBuilderPanel() {
  const data = state.grammarSentenceBuilder;
  const levels = data.levels?.length ? data.levels : localSentenceBuilderLevels();
  const selectedLevel = data.selectedLevel || "basic";
  const selectedMode = data.selectedMode || "arrange_words";
  const activeLevel = levels.find((level) => level.id === selectedLevel) || levels[0];
  const modes = activeLevel?.modes || ["arrange_words", "complete_sentence", "fix_word_order"];
  const activeMode = modes.includes(selectedMode) ? selectedMode : modes[0];
  const items = data.items?.length ? data.items : localSentenceBuilderItems(selectedLevel, activeMode);
  const result = data.result;
  return `
    <section class="module-surface">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Grammar Sentence Builder</p>
          <h2>Bangun kalimat BA yang benar</h2>
          <p>Latihan aktif untuk menyusun word order, melengkapi pola grammar, menggabungkan ide, dan menulis kalimat BA yang lebih formal.</p>
        </div>
        <span class="pill">Build -> Check -> Improve</span>
      </div>
      <div class="quick-actions">
        ${levels.map((level) => `
          <button class="ghost-button ${level.id === selectedLevel ? "selected-control" : ""}" type="button" data-sentence-builder-level="${escapeHtml(level.id)}">
            ${escapeHtml(level.title)}
          </button>
        `).join("")}
      </div>
      <div class="quick-actions">
        ${modes.map((mode) => `
          <button class="ghost-button ${mode === activeMode ? "selected-control" : ""}" type="button" data-sentence-builder-mode="${escapeHtml(mode)}">
            ${escapeHtml(sentenceBuilderModeLabel(mode))}
          </button>
        `).join("")}
      </div>
      <article class="module-card soft">
        <span class="soft-pill">${escapeHtml(activeLevel?.id || selectedLevel)} · ${escapeHtml(activeMode)}</span>
        <h3>${escapeHtml(activeLevel?.description || "Latihan membangun kalimat.")}</h3>
        <p>Isi jawaban dengan kalimat atau kata yang menurutmu paling tepat. Untuk rewrite formal, sistem menerima partial credit berdasarkan kata kunci penting.</p>
      </article>
      <form id="grammarSentenceBuilderForm" class="module-card">
        <h3>Sentence builder practice</h3>
        <div class="module-card-list">
          ${items.map((item) => `
            <label class="case-box soft">
              <span class="soft-pill">${escapeHtml(sentenceBuilderModeLabel(item.mode))} · ${escapeHtml(item.related_topic_id)}</span>
              <strong>${escapeHtml(item.instruction_id)}</strong>
              <span class="muted">${escapeHtml(item.prompt_text)}</span>
              ${(item.input_parts || []).length ? `<small>Input parts: ${escapeHtml(item.input_parts.join(" / "))}</small>` : ""}
              <input type="text" data-sentence-builder-answer="${escapeHtml(item.id)}" value="${escapeHtml(data.answers?.[item.id] || "")}" placeholder="Tulis jawaban kamu di sini" />
              <small>${escapeHtml(item.beginner_tip || "")}</small>
            </label>
          `).join("")}
        </div>
        <button class="primary-button" type="submit">Submit Sentence Builder</button>
        ${result ? grammarSentenceBuilderResultTemplate(result) : emptyStateTemplate("Belum submit Sentence Builder", "Tulis jawabanmu, lalu submit untuk melihat expected answer, grammar rule, dan rekomendasi.")}
      </form>
    </section>
  `;
}

function sentenceBuilderModeLabel(mode) {
  const labels = {
    arrange_words: "Arrange Words",
    complete_sentence: "Complete Sentence",
    combine_sentences: "Combine Sentences",
    rewrite_formal_ba_sentence: "Rewrite Formal BA",
    fix_word_order: "Fix Word Order"
  };
  return labels[mode] || labelFromKey(mode);
}

async function loadGrammarSentenceBuilder(level = "basic", mode = null) {
  const selectedLevel = level || "basic";
  const fallbackLevel = localSentenceBuilderLevels().find((item) => item.id === selectedLevel) || localSentenceBuilderLevels()[0];
  const selectedMode = mode && fallbackLevel.modes.includes(mode) ? mode : fallbackLevel.modes[0];
  if (apiOnline) {
    try {
      const [levelsResponse, itemsResponse] = await Promise.all([
        apiRequest("/grammar/sentence-builder/levels"),
        apiRequest(`/grammar/sentence-builder?level=${encodeURIComponent(selectedLevel)}&mode=${encodeURIComponent(selectedMode)}`)
      ]);
      state.grammarSentenceBuilder = {
        selectedLevel,
        selectedMode,
        levels: levelsResponse.levels || [],
        items: itemsResponse.items || [],
        answers: {},
        result: null
      };
      saveState();
      return;
    } catch (error) {
      apiOnline = false;
    }
  }
  state.grammarSentenceBuilder = {
    selectedLevel,
    selectedMode,
    levels: localSentenceBuilderLevels(),
    items: localSentenceBuilderItems(selectedLevel, selectedMode),
    answers: {},
    result: null
  };
  saveState();
}

async function submitGrammarSentenceBuilder() {
  const level = state.grammarSentenceBuilder.selectedLevel || "basic";
  const mode = state.grammarSentenceBuilder.selectedMode || "arrange_words";
  if (apiOnline) {
    try {
      const response = await apiRequest("/grammar/sentence-builder/submit", {
        method: "POST",
        body: {
          user_id: state.user?.id || "default-user",
          level,
          mode,
          answers: state.grammarSentenceBuilder.answers || {}
        }
      });
      state.grammarSentenceBuilder.result = response;
      await refreshIntegratedJourney();
      await refreshGrammarProgress();
      saveState();
      return;
    } catch (error) {
      apiOnline = false;
    }
  }
  const items = state.grammarSentenceBuilder.items?.length ? state.grammarSentenceBuilder.items : localSentenceBuilderItems(level, mode);
  const details = items.map((item) => {
    const userAnswer = state.grammarSentenceBuilder.answers?.[item.id] || "";
    const isCorrect = normalizeLocalSentence(userAnswer) === normalizeLocalSentence(item.expected_answer);
    return {
      item_id: item.id,
      is_correct: isCorrect,
      partial_score: isCorrect ? 100 : 0,
      user_answer: userAnswer,
      expected_answer: item.expected_answer,
      explanation_id: item.explanation_id,
      grammar_rule_id: item.grammar_rule_id,
      related_topic_id: item.related_topic_id
    };
  });
  const correctCount = details.filter((item) => item.is_correct).length;
  const score = details.length ? Math.round((correctCount / details.length) * 100) : 0;
  state.grammarSentenceBuilder.result = {
    result: {
      score,
      max_score: 100,
      correct_count: correctCount,
      total_questions: details.length,
      is_passed: score >= 70,
      details,
      mistakes: details.filter((item) => !item.is_correct)
    },
    recommendation: {
      next_action: score >= 70 ? "Lanjutkan ke mode Sentence Builder berikutnya." : "Ulangi word order dasar: subject, verb, object.",
      review_topic_id: details.find((item) => !item.is_correct)?.related_topic_id || "modal_verb",
      mentor_message: score >= 70 ? "Bagus. Kamu mulai bisa membangun kalimat yang rapi." : "Tidak apa-apa. Bangun kalimat dari bagian paling kecil dulu."
    }
  };
  saveState();
}

function grammarSentenceBuilderResultTemplate(response) {
  const result = response.result || {};
  const recommendation = response.recommendation || {};
  return `
    <div class="alert ${result.is_passed ? "success" : "warning"}">
      <strong>Score ${Math.round(result.score || 0)}/${result.max_score || 100}</strong>
      <p>${escapeHtml(recommendation.mentor_message || "Sentence Builder selesai.")}</p>
      <p>${escapeHtml(recommendation.next_action || "")}</p>
    </div>
    <div class="module-card-list">
      ${(result.details || []).map((item) => `
        <div class="case-box ${item.partial_score >= 70 ? "soft" : ""}">
          <strong>${item.partial_score >= 70 ? "Cukup baik" : "Perlu review"} · ${escapeHtml(item.item_id)}</strong>
          <p><strong>Jawaban Anda:</strong> ${escapeHtml(item.user_answer || "-")}</p>
          <p><strong>Expected:</strong> ${escapeHtml(item.expected_answer || "-")}</p>
          <p><strong>Rule:</strong> ${escapeHtml(item.grammar_rule_id || "-")}</p>
          <small>${escapeHtml(item.explanation_id || "")}</small>
        </div>
      `).join("")}
    </div>
  `;
}

function localSentenceBuilderLevels() {
  return [
    { id: "basic", title: "Basic Sentence Builder", description: "Susun kalimat dasar Subject + Verb + Object.", modes: ["arrange_words", "complete_sentence", "fix_word_order"] },
    { id: "intermediate", title: "Intermediate Sentence Builder", description: "Gabungkan ide dan phrase kalimat panjang.", modes: ["combine_sentences", "arrange_words", "complete_sentence", "fix_word_order"] },
    { id: "advanced_preview", title: "Advanced Preview", description: "Preview menulis kalimat BA formal.", modes: ["rewrite_formal_ba_sentence", "combine_sentences"] }
  ];
}

function localSentenceBuilderItems(level = "basic", mode = "arrange_words") {
  const items = [
    {
      id: "arrange_basic_modal_1",
      level: "basic",
      mode: "arrange_words",
      related_topic_id: "modal_verb",
      instruction_id: "Susun kata berikut menjadi kalimat yang benar.",
      prompt_text: "must / requirements / elicit / A business analyst",
      input_parts: ["must", "requirements", "elicit", "A business analyst"],
      expected_answer: "A business analyst must elicit requirements.",
      explanation_id: "Pola yang benar adalah Subject + modal + verb + object.",
      grammar_rule_id: "Subject + modal + base verb + object",
      beginner_tip: "Cari subject dulu, lalu modal, lalu verb utama."
    },
    {
      id: "complete_basic_be_1",
      level: "basic",
      mode: "complete_sentence",
      related_topic_id: "modal_verb",
      instruction_id: "Isi bagian kosong.",
      prompt_text: "The system must ___ flexible for all users.",
      input_parts: ["The system must", "___", "flexible"],
      expected_answer: "be",
      explanation_id: "Setelah modal must dan sebelum adjective, gunakan be.",
      grammar_rule_id: "modal + be + adjective",
      beginner_tip: "must be flexible adalah pola benar."
    },
    {
      id: "fix_order_basic_modal_1",
      level: "basic",
      mode: "fix_word_order",
      related_topic_id: "modal_verb",
      instruction_id: "Perbaiki word order.",
      prompt_text: "Must the system generate reports automatically.",
      input_parts: ["Must", "the system", "generate", "reports", "automatically"],
      expected_answer: "The system must generate reports automatically.",
      explanation_id: "Untuk pernyataan, subject muncul sebelum modal.",
      grammar_rule_id: "Subject + modal + base verb + object",
      beginner_tip: "Jangan mulai dengan modal jika bukan pertanyaan."
    },
    {
      id: "combine_intermediate_parallel_1",
      level: "intermediate",
      mode: "combine_sentences",
      related_topic_id: "parallel_structure",
      instruction_id: "Gabungkan dua kalimat.",
      prompt_text: "The analyst interviews users. The analyst documents requirements.",
      input_parts: ["The analyst interviews users.", "The analyst documents requirements."],
      expected_answer: "The analyst interviews users and documents requirements.",
      explanation_id: "Dua aksi dengan subject sama bisa digabung memakai and.",
      grammar_rule_id: "Subject + verb + object + and + verb + object",
      beginner_tip: "Jangan ulangi subject jika pelakunya sama."
    },
    {
      id: "rewrite_advanced_formal_1",
      level: "advanced_preview",
      mode: "rewrite_formal_ba_sentence",
      related_topic_id: "formal_ba_writing",
      instruction_id: "Tulis ulang menjadi kalimat BA formal.",
      prompt_text: "The system helps users make reports faster.",
      input_parts: ["The system helps users make reports faster."],
      expected_answer: "The system helps users generate reports more efficiently.",
      explanation_id: "generate reports dan more efficiently terdengar lebih formal.",
      grammar_rule_id: "formal verb + professional adverb",
      beginner_tip: "Ganti kata umum dengan kata profesional yang tetap jelas."
    }
  ];
  return items.filter((item) => (!level || item.level === level) && (!mode || item.mode === mode));
}

function normalizeLocalSentence(value) {
  return String(value || "").trim().toLowerCase().replace(/[.?!]+$/, "").replace(/\s+/g, " ");
}

function grammarAdvancedLabPanel() {
  const data = state.grammarAdvancedLab;
  const topics = data.topics?.length ? data.topics : localAdvancedGrammarTopics();
  const topic = data.topic || localAdvancedGrammarTopic(data.selectedTopic || "nominalization");
  return `
    <section class="module-surface">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Advanced Grammar Lab</p>
          <h2>Grammar formal untuk TOEFL + dokumen BA</h2>
          <p>Pahami pola advanced seperti nominalization, hedging, inversion, conditional, connector akademik, dan formal BA writing.</p>
        </div>
        <span class="pill">Advanced but guided</span>
      </div>
      <div class="quick-actions">
        ${topics.map((item) => `
          <button class="ghost-button ${item.topic_id === topic.topic_id ? "selected-control" : ""}" type="button" data-advanced-grammar-topic="${escapeHtml(item.topic_id)}">
            ${escapeHtml(item.title)}
          </button>
        `).join("")}
      </div>
      <div class="module-grid two">
        <article class="module-card soft">
          <span class="soft-pill">${escapeHtml(topic.level)} · ${escapeHtml(topic.topic_id)}</span>
          <h3>${escapeHtml(topic.title)}</h3>
          <p>${escapeHtml(topic.learning_objective)}</p>
          <p><strong>Bridge pemula:</strong> ${escapeHtml(topic.beginner_bridge)}</p>
          <p><strong>Professional usage:</strong> ${escapeHtml(topic.professional_usage)}</p>
          <p><strong>Trap:</strong> ${escapeHtml(topic.common_trap)}</p>
        </article>
        <article class="module-card">
          <h3>Contoh advanced</h3>
          ${(topic.examples || []).slice(0, 2).map((item) => `
            <div class="case-box soft">
              <p><strong>${escapeHtml(item.sentence)}</strong> ${renderContextualHelpButton("grammar", "grammar_sentence", item.sentence)}</p>
              <p>${escapeHtml(item.simple_meaning_id)}</p>
              <small>Simpler: ${escapeHtml(item.simpler_version)}</small>
              <div class="grammar-breakdown-grid">
                ${Object.entries(item.breakdown || {}).map(([key, value]) => grammarChip(labelFromKey(key), value)).join("")}
              </div>
            </div>
          `).join("")}
        </article>
      </div>
      <div class="module-grid two">
        <form id="advancedGrammarPracticeForm" class="module-card">
          <h3>Advanced practice</h3>
          ${(topic.practice_items || []).slice(0, 4).map((item) => `
            <label>
              ${escapeHtml(item.instruction_id)}
              <span class="muted">${escapeHtml(item.sentence)}</span>
              <strong>${escapeHtml(item.question)}</strong>
              <select data-advanced-practice-answer="${escapeHtml(item.id)}">
                <option value="">Pilih jawaban</option>
                ${(item.options || []).map((option) => `<option value="${escapeHtml(option)}" ${data.practiceAnswers?.[item.id] === option ? "selected" : ""}>${escapeHtml(option)}</option>`).join("")}
              </select>
            </label>
          `).join("")}
          <button class="primary-button" type="submit">Submit Advanced Practice</button>
          ${data.practiceResult ? advancedGrammarResultTemplate(data.practiceResult, "practice") : emptyStateTemplate("Belum submit advanced practice", "Jawab soal pilihan untuk melihat score dan feedback advanced grammar.")}
        </form>
        <form id="advancedGrammarRewriteForm" class="module-card">
          <h3>Advanced rewrite</h3>
          ${(topic.rewrite_items || []).slice(0, 4).map((item) => `
            <label>
              ${escapeHtml(item.instruction_id)}
              <span class="muted">${escapeHtml(item.original_sentence)}</span>
              <input type="text" data-advanced-rewrite-answer="${escapeHtml(item.id)}" value="${escapeHtml(data.rewriteAnswers?.[item.id] || "")}" placeholder="Tulis versi formal kamu" />
              <small>Keyword penting: ${escapeHtml((item.required_keywords || []).join(", "))}</small>
            </label>
          `).join("")}
          <button class="primary-button" type="submit">Submit Advanced Rewrite</button>
          ${data.rewriteResult ? advancedGrammarResultTemplate(data.rewriteResult, "rewrite") : emptyStateTemplate("Belum submit advanced rewrite", "Tulis ulang kalimat informal menjadi kalimat BA yang lebih formal.")}
        </form>
      </div>
    </section>
  `;
}

async function loadGrammarAdvancedLab(topicId = "nominalization") {
  const selectedTopic = topicId || "nominalization";
  if (apiOnline) {
    try {
      const [topicsResponse, topicResponse] = await Promise.all([
        apiRequest("/grammar/advanced/topics"),
        apiRequest(`/grammar/advanced/topics/${encodeURIComponent(selectedTopic)}`)
      ]);
      state.grammarAdvancedLab = {
        selectedTopic,
        topics: topicsResponse.topics || [],
        topic: topicResponse.topic,
        practiceAnswers: {},
        rewriteAnswers: {},
        practiceResult: null,
        rewriteResult: null
      };
      saveState();
      return;
    } catch (error) {
      apiOnline = false;
    }
  }
  state.grammarAdvancedLab = {
    selectedTopic,
    topics: localAdvancedGrammarTopics(),
    topic: localAdvancedGrammarTopic(selectedTopic),
    practiceAnswers: {},
    rewriteAnswers: {},
    practiceResult: null,
    rewriteResult: null
  };
  saveState();
}

async function submitAdvancedGrammarPractice() {
  const topicId = state.grammarAdvancedLab.selectedTopic || "nominalization";
  if (apiOnline) {
    try {
      const response = await apiRequest("/grammar/advanced/practice/submit", {
        method: "POST",
        body: {
          user_id: state.user?.id || "default-user",
          topic_id: topicId,
          answers: state.grammarAdvancedLab.practiceAnswers || {}
        }
      });
      state.grammarAdvancedLab.practiceResult = response;
      await refreshIntegratedJourney();
      await refreshGrammarProgress();
      saveState();
      return;
    } catch (error) {
      apiOnline = false;
    }
  }
  state.grammarAdvancedLab.practiceResult = localAdvancedResult(state.grammarAdvancedLab.practiceAnswers || {}, state.grammarAdvancedLab.topic?.practice_items || []);
  saveState();
}

async function submitAdvancedGrammarRewrite() {
  const topicId = state.grammarAdvancedLab.selectedTopic || "nominalization";
  if (apiOnline) {
    try {
      const response = await apiRequest("/grammar/advanced/rewrite/submit", {
        method: "POST",
        body: {
          user_id: state.user?.id || "default-user",
          topic_id: topicId,
          answers: state.grammarAdvancedLab.rewriteAnswers || {}
        }
      });
      state.grammarAdvancedLab.rewriteResult = response;
      await refreshIntegratedJourney();
      await refreshGrammarProgress();
      saveState();
      return;
    } catch (error) {
      apiOnline = false;
    }
  }
  state.grammarAdvancedLab.rewriteResult = localAdvancedResult(state.grammarAdvancedLab.rewriteAnswers || {}, state.grammarAdvancedLab.topic?.rewrite_items || []);
  saveState();
}

function advancedGrammarResultTemplate(response, type = "practice") {
  const result = response.result || {};
  const recommendation = response.recommendation || {};
  return `
    <div class="alert ${result.is_passed ? "success" : "warning"}">
      <strong>Score ${Math.round(result.score || 0)}/${result.max_score || 100}</strong>
      <p>${escapeHtml(recommendation.mentor_message || "Advanced Grammar selesai.")}</p>
      <p>${escapeHtml(recommendation.next_action || "")}</p>
    </div>
    <div class="module-card-list">
      ${(result.details || []).map((item) => `
        <div class="case-box ${item.is_correct || item.partial_score >= 70 ? "soft" : ""}">
          <strong>${item.is_correct || item.partial_score >= 70 ? "Cukup baik" : "Perlu review"} · ${escapeHtml(item.item_id)}</strong>
          <p><strong>Jawaban Anda:</strong> ${escapeHtml(item.user_answer || "-")}</p>
          <p><strong>${type === "rewrite" ? "Expected" : "Correct"}:</strong> ${escapeHtml(item.expected_answer || item.correct_answer || "-")}</p>
          ${item.required_keywords ? `<small>Required keywords: ${escapeHtml(item.required_keywords.join(", "))}</small>` : ""}
          <small>${escapeHtml(item.explanation_id || "")}</small>
        </div>
      `).join("")}
    </div>
  `;
}

function localAdvancedGrammarTopics() {
  return [
    { topic_id: "nominalization", level: "advanced", title: "Nominalization", learning_objective: "Ubah action menjadi noun formal.", professional_usage: "Formal reports.", estimated_minutes: 15 },
    { topic_id: "formal_ba_writing", level: "advanced", title: "Formal BA Writing", learning_objective: "Tulis kalimat BA profesional.", professional_usage: "SRS, BRD, proposals.", estimated_minutes: 18 },
    { topic_id: "academic_connectors", level: "advanced", title: "Academic Connectors", learning_objective: "Pilih connector logika.", professional_usage: "TOEFL writing and reports.", estimated_minutes: 15 }
  ];
}

function localAdvancedGrammarTopic(topicId = "nominalization") {
  const topic = localAdvancedGrammarTopics().find((item) => item.topic_id === topicId) || localAdvancedGrammarTopics()[0];
  return {
    ...topic,
    explanation_id: "Pahami versi sederhana dulu, lalu lihat pola formalnya.",
    ba_context: "Dipakai dalam dokumen Business Analyst formal.",
    common_trap: "Kalimat advanced sering terlihat sulit karena subject-nya panjang.",
    beginner_bridge: "Ubah kalimat advanced menjadi versi sederhana dulu. Setelah paham makna, pelajari pola formalnya.",
    examples: [
      {
        sentence: "The implementation of the system is expected to improve traceability.",
        simpler_version: "The team implements the system to improve traceability.",
        simple_meaning_id: "Implementasi sistem diharapkan meningkatkan traceability.",
        breakdown: { subject: "The implementation of the system", main_verb: "is expected to improve", object: "traceability" }
      }
    ],
    practice_items: [
      {
        id: `${topic.topic_id}_practice_1`,
        instruction_id: "Pilih jawaban yang paling tepat.",
        sentence: "The implementation of the system is expected to improve traceability.",
        question: "Which word is nominalization?",
        options: ["implementation", "system", "expected", "traceability"],
        correct_answer: "implementation",
        explanation_id: "Implementation berasal dari verb implement."
      }
    ],
    rewrite_items: [
      {
        id: `${topic.topic_id}_rewrite_1`,
        instruction_id: "Rewrite this sentence into a formal BA sentence.",
        original_sentence: "The system helps users make reports faster.",
        expected_answer: "The system enables users to generate reports more efficiently.",
        required_keywords: ["system", "users", "generate", "reports", "efficiently"],
        explanation_id: "Generate reports more efficiently lebih formal."
      }
    ]
  };
}

function localAdvancedResult(answers, items) {
  const details = (items || []).map((item) => {
    const userAnswer = answers[item.id] || "";
    const correct = item.correct_answer || item.expected_answer || "";
    const isCorrect = normalizeLocalSentence(userAnswer) === normalizeLocalSentence(correct);
    return {
      item_id: item.id,
      is_correct: isCorrect,
      partial_score: isCorrect ? 100 : 0,
      user_answer: userAnswer,
      correct_answer: item.correct_answer,
      expected_answer: item.expected_answer,
      required_keywords: item.required_keywords,
      explanation_id: item.explanation_id,
      related_topic_id: "formal_ba_writing"
    };
  });
  const score = details.length ? Math.round((details.filter((item) => item.is_correct).length / details.length) * 100) : 0;
  return {
    result: {
      score,
      max_score: 100,
      correct_count: details.filter((item) => item.is_correct).length,
      total_questions: details.length,
      is_passed: score >= 70,
      details,
      mistakes: details.filter((item) => !item.is_correct)
    },
    recommendation: {
      next_action: score >= 70 ? "Lanjutkan ke advanced topic lain." : "Baca beginner bridge dan simpler version dulu.",
      review_topic_id: "formal_ba_writing",
      mentor_message: score >= 70 ? "Bagus. Kamu mulai memahami grammar advanced." : "Pecah kalimat advanced menjadi versi sederhana dulu."
    }
  };
}

function grammarReviewPanel() {
  const review = state.grammarReview || localGrammarReview();
  const weakness = review.weakness_summary || {};
  const primary = weakness.primary_weakness || {};
  const secondary = weakness.secondary_weakness || {};
  const recommended = review.recommended_practice || {};
  return `
    <section class="module-surface">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Grammar Review</p>
          <h2>Pola salah dan latihan ulang</h2>
          <p>Review ini merangkum topik grammar yang masih lemah, pola kesalahan berulang, dan latihan yang sebaiknya diulang berikutnya.</p>
        </div>
        <button id="refreshGrammarReviewButton" class="ghost-button" type="button">Refresh Review</button>
      </div>
      <div class="alert ${weakness.review_priority === "high" ? "warning" : "success"}">
        <strong>${escapeHtml(review.mentor_message || "Mulai kerjakan beberapa latihan grammar agar review lebih akurat.")}</strong>
        <p>Recommended: ${escapeHtml(recommended.next_action || "Latihan ulang grammar foundation.")}</p>
      </div>
      <div class="module-grid three">
        <article class="module-card soft">
          <span class="soft-pill">Primary weakness</span>
          <h3>${escapeHtml(primary.title || "Subject and Verb")}</h3>
          <p>Mastery: <strong>${Math.round(primary.mastery_score || 0)}%</strong></p>
          <small>${escapeHtml(primary.reason || "Belum cukup data attempt.")}</small>
        </article>
        <article class="module-card">
          <span class="soft-pill">Secondary weakness</span>
          <h3>${escapeHtml(secondary.title || "Modal Verb")}</h3>
          <p>Mastery: <strong>${Math.round(secondary.mastery_score || 0)}%</strong></p>
          <small>${escapeHtml(secondary.reason || "Topik cadangan untuk review.")}</small>
        </article>
        <article class="module-card">
          <span class="soft-pill">${escapeHtml(weakness.readiness_level || "Basic 1")}</span>
          <h3>${Math.round(weakness.average_grammar_score || 0)}% avg score</h3>
          <p>${Number(weakness.completed_grammar_attempts || 0)} grammar attempts</p>
          <small>Review priority: ${escapeHtml(weakness.review_priority || "high")}</small>
        </article>
      </div>
      <div class="module-grid two">
        <article class="module-card">
          <h3>Mistake patterns</h3>
          <div class="module-card-list">
            ${(review.mistake_patterns || []).slice(0, 4).map((pattern) => `
              <div class="case-box soft">
                <span class="soft-pill">${escapeHtml(pattern.severity || "medium")} · ${escapeHtml(pattern.related_phase_module || "Grammar")}</span>
                <strong>${escapeHtml(pattern.title)}</strong>
                <p>${escapeHtml(pattern.pattern_explanation_id || "")}</p>
                <small>Frequency: ${Number(pattern.frequency || 0)} · ${escapeHtml(pattern.example_mistake || "")}</small>
              </div>
            `).join("")}
          </div>
        </article>
        <article class="module-card">
          <h3>Review queue</h3>
          <div class="module-card-list">
            ${(review.review_queue || []).slice(0, 5).map((item) => `
              <div class="case-box">
                <span class="soft-pill">Priority ${Number(item.priority || 1)} · ${escapeHtml(item.status || "pending")}</span>
                <strong>${escapeHtml(item.title)}</strong>
                <p>${escapeHtml(item.reason || "")}</p>
                <small>${escapeHtml(item.action_label || "")} · ${Number(item.estimated_minutes || 10)} menit</small>
              </div>
            `).join("")}
          </div>
        </article>
      </div>
      <article class="module-card soft">
        <h3>Recommended practice</h3>
        <p><strong>${escapeHtml(recommended.recommended_module || "basic_trainer")}</strong> · ${escapeHtml(recommended.recommended_topic_id || "subject_verb")}</p>
        <p>${escapeHtml(recommended.reason || "Latihan ini dipilih dari weakness dan mistake pattern.")}</p>
        <small>Endpoint: ${escapeHtml(recommended.target_endpoint || "/api/grammar/trainer/basic/subject_verb")}</small>
      </article>
    </section>
  `;
}

async function loadGrammarReview() {
  if (apiOnline) {
    try {
      state.grammarReview = await apiRequest(`/grammar/review?user_id=${encodeURIComponent(state.user?.id || "default-user")}`);
      saveState();
      return;
    } catch (error) {
      apiOnline = false;
    }
  }
  state.grammarReview = localGrammarReview();
  saveState();
}

function localGrammarReview() {
  return {
    weakness_summary: {
      primary_weakness: {
        topic_id: "subject_verb",
        title: "Subject and Verb",
        mastery_score: 0,
        reason: "Belum cukup data attempt. Mulai dari subject dan verb."
      },
      secondary_weakness: {
        topic_id: "modal_verb",
        title: "Modal Verb",
        mastery_score: 0,
        reason: "Modal verb menjadi fondasi requirement sentence."
      },
      average_grammar_score: state.progress?.Grammar || 0,
      completed_grammar_attempts: 0,
      review_priority: "high",
      readiness_level: "Basic 1 - Sentence Foundation"
    },
    mistake_patterns: [
      {
        pattern_id: "pattern_subject_verb",
        topic_id: "subject_verb",
        title: "Grammar foundation belum cukup data",
        mistake_type: "unknown_grammar_issue",
        frequency: 1,
        severity: "medium",
        pattern_explanation_id: "Kerjakan beberapa latihan grammar agar pola kesalahan bisa dianalisis.",
        example_mistake: "Belum cukup attempt.",
        recommended_action: "Latihan ulang mencari subject dan main verb.",
        recommended_endpoint: "/api/grammar/trainer/basic/subject_verb",
        related_phase_module: "Basic Grammar Trainer"
      }
    ],
    review_queue: [
      {
        review_id: "review_subject_verb",
        priority: 1,
        topic_id: "subject_verb",
        title: "Review Subject and Verb",
        reason: "Fondasi awal grammar.",
        action_label: "Latihan ulang Subject and Verb",
        target_endpoint: "/api/grammar/trainer/basic/subject_verb",
        estimated_minutes: 10,
        source: "fallback",
        status: "pending"
      }
    ],
    recommended_practice: {
      recommended_topic_id: "subject_verb",
      recommended_module: "basic_trainer",
      reason: "Mulai dari fondasi grammar.",
      next_action: "Latihan ulang mencari subject dan main verb.",
      target_endpoint: "/api/grammar/trainer/basic/subject_verb",
      estimated_minutes: 10,
      difficulty: "basic"
    },
    mentor_message: "Belum cukup data review. Kerjakan latihan Grammar dulu agar analisis lebih akurat.",
    recent_attempts: []
  };
}

function grammarSimulationPanel() {
  const data = state.grammarSimulation;
  const modes = data.modes?.length ? data.modes : localGrammarSimulationModes();
  const activeMode = modes.find((mode) => mode.id === data.mode) || modes[0];
  const session = data.session;
  const result = data.result?.result || data.result;
  return `
    <section class="module-surface">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Grammar Simulation</p>
          <h2>Timed Grammar readiness test</h2>
          <p>Simulasi ini mencampur Basic, Intermediate, Advanced, Error Correction, Sentence Builder, dan Grammar Meaning. Bantuan ID dibatasi supaya terasa seperti tes.</p>
        </div>
        <span class="pill">No Bantuan ID during test</span>
      </div>
      <div class="module-grid three">
        ${modes.map((mode) => `
          <button class="module-card text-left ${mode.id === activeMode.id ? "selected-control" : ""}" type="button" data-grammar-simulation-mode="${escapeHtml(mode.id)}">
            <span class="soft-pill">${escapeHtml(mode.id)}</span>
            <h3>${escapeHtml(mode.title)}</h3>
            <p>${Number(mode.question_count)} soal · ${Number(mode.duration_minutes)} menit</p>
            <small>${escapeHtml(mode.description)}</small>
          </button>
        `).join("")}
      </div>
      <button id="startGrammarSimulationButton" class="primary-button" type="button">Mulai Simulasi Grammar</button>
      ${session ? grammarSimulationSessionTemplate(session) : emptyStateTemplate("Belum ada simulasi aktif", "Pilih mode lalu mulai simulasi untuk mengerjakan soal grammar campuran.")}
      ${result ? grammarSimulationResultTemplate(result) : ""}
      ${(data.history || []).length ? `
        <article class="module-card">
          <h3>Riwayat simulasi</h3>
          <div class="module-card-list">
            ${data.history.slice(0, 5).map((item) => `
              <div class="case-box soft">
                <strong>${escapeHtml(item.mode)} · score ${Math.round(item.total_score || 0)}</strong>
                <p>${escapeHtml(item.recommended_next_practice || "")}</p>
              </div>
            `).join("")}
          </div>
        </article>
      ` : ""}
    </section>
  `;
}

function grammarSimulationSessionTemplate(session) {
  return `
    <form id="grammarSimulationForm" class="module-card">
      <div class="section-heading">
        <div>
          <h3>${escapeHtml(session.title)}</h3>
          <p>${Number(session.question_count)} soal · ${Number(session.duration_minutes)} menit · ${escapeHtml(session.instructions_id)}</p>
        </div>
        <span class="pill">${escapeHtml(session.mode)}</span>
      </div>
      <div class="module-card-list">
        ${(session.questions || []).map((question, index) => `
          <label class="case-box soft">
            <span class="soft-pill">Soal ${index + 1} · ${escapeHtml(question.level)} · ${escapeHtml(question.skill_area)}</span>
            <strong>${escapeHtml(question.instruction_id)}</strong>
            <span class="muted">${escapeHtml(question.sentence || "")}</span>
            <p>${escapeHtml(question.question)}</p>
            ${(question.options || []).length ? `
              <select data-grammar-simulation-answer="${escapeHtml(question.id)}">
                <option value="">Pilih jawaban</option>
                ${question.options.map((option) => `<option value="${escapeHtml(option)}" ${state.grammarSimulation.answers?.[question.id] === option ? "selected" : ""}>${escapeHtml(option)}</option>`).join("")}
              </select>
            ` : `
              <input type="text" data-grammar-simulation-answer="${escapeHtml(question.id)}" value="${escapeHtml(state.grammarSimulation.answers?.[question.id] || "")}" placeholder="Tulis jawaban simulasi" />
            `}
          </label>
        `).join("")}
      </div>
      <button class="primary-button" type="submit">Submit Grammar Simulation</button>
    </form>
  `;
}

function grammarSimulationResultTemplate(result) {
  return `
    <article class="module-card soft">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Simulation result</p>
          <h2>Score ${Math.round(result.total_score || 0)}/${result.max_score || 100}</h2>
          <p>${Number(result.correct_count || 0)}/${Number(result.total_questions || 0)} benar · ${Number(result.time_spent_seconds || 0)} detik</p>
        </div>
        <span class="pill">${escapeHtml(result.mode || "simulation")}</span>
      </div>
      <p><strong>Next practice:</strong> ${escapeHtml(result.recommended_next_practice || "")}</p>
      <div class="module-grid two">
        <div class="module-card">
          <h3>Level breakdown</h3>
          ${(result.level_breakdown || []).map((item) => `<p>${escapeHtml(item.level)}: <strong>${Math.round(item.score || 0)}%</strong> (${Number(item.correct_count)}/${Number(item.total_questions)})</p>`).join("")}
        </div>
        <div class="module-card">
          <h3>Sub-skill breakdown</h3>
          ${(result.subskill_breakdown || []).map((item) => `<p>${escapeHtml(item.skill_area)}: <strong>${Math.round(item.score || 0)}%</strong> · ${escapeHtml(item.status)}</p>`).join("")}
        </div>
      </div>
      <div class="module-card">
        <h3>Answer review summary</h3>
        <div class="module-card-list">
          ${(result.answer_review_summary || []).slice(0, 8).map((item) => `
            <div class="case-box ${item.is_correct ? "soft" : ""}">
              <strong>${item.is_correct ? "Benar" : "Review"} · ${escapeHtml(item.question_id)}</strong>
              <p>Jawaban Anda: ${escapeHtml(item.user_answer || "-")}</p>
              <p>Correct: ${escapeHtml(item.correct_answer || "-")}</p>
              <small>${escapeHtml(item.explanation_id || "")}</small>
            </div>
          `).join("")}
        </div>
      </div>
    </article>
  `;
}

async function startGrammarSimulation() {
  const mode = state.grammarSimulation.mode || "short";
  if (apiOnline) {
    try {
      const [modesResponse, sessionResponse] = await Promise.all([
        apiRequest("/grammar/simulation/modes"),
        apiRequest("/grammar/simulation/start", {
          method: "POST",
          body: { user_id: state.user?.id || "default-user", mode }
        })
      ]);
      state.grammarSimulation = {
        mode,
        modes: modesResponse.modes || [],
        session: sessionResponse.session,
        answers: {},
        result: null,
        history: state.grammarSimulation.history || []
      };
      saveState();
      return;
    } catch (error) {
      apiOnline = false;
    }
  }
  state.grammarSimulation = {
    mode,
    modes: localGrammarSimulationModes(),
    session: localGrammarSimulationSession(mode),
    answers: {},
    result: null,
    history: state.grammarSimulation.history || []
  };
  saveState();
}

async function submitGrammarSimulation() {
  const session = state.grammarSimulation.session;
  if (!session) return;
  if (apiOnline) {
    try {
      const response = await apiRequest("/grammar/simulation/submit", {
        method: "POST",
        body: {
          user_id: state.user?.id || "default-user",
          session_id: session.session_id,
          mode: session.mode,
          session,
          answers: state.grammarSimulation.answers || {},
          time_spent_seconds: 120
        }
      });
      const historyResponse = await apiRequest(`/grammar/simulation/history?user_id=${encodeURIComponent(state.user?.id || "default-user")}`);
      state.grammarSimulation.result = response.result;
      state.grammarSimulation.history = historyResponse.history || [];
      await refreshIntegratedJourney();
      await refreshGrammarProgress();
      saveState();
      return;
    } catch (error) {
      apiOnline = false;
    }
  }
  const details = (session.questions || []).map((question) => {
    const answer = state.grammarSimulation.answers?.[question.id] || "";
    const isCorrect = normalizeLocalSentence(answer) === normalizeLocalSentence(question.correct_answer);
    return {
      question_id: question.id,
      is_correct: isCorrect,
      partial_score: isCorrect ? 100 : 0,
      user_answer: answer,
      correct_answer: question.correct_answer,
      explanation_id: question.explanation_id,
      topic_id: question.topic_id,
      skill_area: question.skill_area,
      level: question.level
    };
  });
  const score = details.length ? Math.round(details.filter((item) => item.is_correct).length / details.length * 100) : 0;
  state.grammarSimulation.result = {
    session_id: session.session_id,
    user_id: state.user?.id || "default-user",
    mode: session.mode,
    total_score: score,
    max_score: 100,
    correct_count: details.filter((item) => item.is_correct).length,
    total_questions: details.length,
    time_spent_seconds: 120,
    level_breakdown: [],
    subskill_breakdown: [],
    answer_review_summary: details,
    recommended_next_practice: "Ulangi Grammar Review untuk melihat area lemah.",
    recommendation: { next_action: "Ulangi Grammar Review untuk melihat area lemah." }
  };
  saveState();
}

function localGrammarSimulationModes() {
  return [
    { id: "short", title: "Short Grammar Simulation", duration_minutes: 10, question_count: 10, description: "Quick mixed grammar review." },
    { id: "medium", title: "Medium Grammar Simulation", duration_minutes: 20, question_count: 20, description: "Mixed practice." },
    { id: "full", title: "Full Grammar Readiness Simulation", duration_minutes: 40, question_count: 40, description: "Complete readiness test." }
  ];
}

function localGrammarSimulationSession(mode = "short") {
  return {
    session_id: `local-grammar-sim-${Date.now()}`,
    user_id: state.user?.id || "default-user",
    mode,
    title: "Local Grammar Simulation",
    duration_minutes: mode === "full" ? 40 : mode === "medium" ? 20 : 10,
    question_count: 2,
    started_at: new Date().toISOString(),
    instructions_id: "Jawab semua soal Grammar.",
    help_policy: { bantuan_id_allowed: false, show_explanation_during_test: false, show_explanation_after_submit: true },
    questions: [
      {
        id: "local_grammar_sim_1",
        level: "basic",
        question_type: "identify_subject",
        topic_id: "subject_verb",
        instruction_id: "Pilih subject.",
        sentence: "A business analyst must elicit requirements.",
        question: "Which part is the subject?",
        options: ["A business analyst", "must elicit", "requirements"],
        correct_answer: "A business analyst",
        explanation_id: "Subject adalah pelaku utama.",
        skill_area: "subject_detection"
      },
      {
        id: "local_grammar_sim_2",
        level: "intermediate",
        question_type: "identify_main_verb",
        topic_id: "gerund_vs_main_verb",
        instruction_id: "Pilih main verb.",
        sentence: "The analyst working with stakeholders must clarify priorities.",
        question: "Which one is the main verb?",
        options: ["working", "must clarify", "stakeholders"],
        correct_answer: "must clarify",
        explanation_id: "working hanya modifier.",
        skill_area: "main_verb_detection"
      }
    ]
  };
}

function localBasicGrammarTrainerTopics() {
  return [
    { topic_id: "subject_verb", title: "Subject and Verb", level: "basic", learning_objective: "Temukan pelaku dan aksi utama.", estimated_minutes: 10 },
    { topic_id: "object_complement", title: "Object and Complement", level: "basic", learning_objective: "Bedakan object dan complement.", estimated_minutes: 10 },
    { topic_id: "modal_verb", title: "Modal Verb", level: "basic", learning_objective: "Pahami must, should, can.", estimated_minutes: 8 }
  ];
}

function localBasicGrammarTrainer(topicId = "subject_verb") {
  const base = {
    topic_id: topicId,
    level: "basic",
    title: topicId === "object_complement" ? "Object and Complement" : topicId === "modal_verb" ? "Modal Verb" : "Subject and Verb",
    learning_objective: "Latihan grammar dasar untuk membaca kalimat BA.",
    explanation_id: "Cari struktur utama kalimat sebelum menerjemahkan detail.",
    beginner_tip: "Mulai dari subject, verb, lalu object atau complement.",
    ba_context: "Dipakai saat membaca requirement dan stakeholder statement.",
    examples: [
      {
        sentence: "A business analyst must elicit requirements.",
        simple_meaning_id: "Seorang business analyst harus menggali kebutuhan.",
        grammar_focus: "Subject + modal + verb + object",
        breakdown: { subject: "A business analyst", main_verb: "must elicit", object: "requirements" }
      }
    ],
    guided_items: [
      {
        id: `${topicId}_guided_1`,
        instruction_id: "Pilih main verb dalam kalimat ini.",
        sentence: "A business analyst must elicit requirements.",
        target_part: "main_verb",
        options: ["A business analyst", "must elicit", "requirements"],
        correct_answer: "must elicit",
        explanation_id: "\"must elicit\" adalah aksi utama.",
        beginner_tip: "Modal must diikuti verb dasar."
      }
    ],
    quiz_items: [
      {
        id: `${topicId}_quiz_1`,
        question_type: "identify_main_verb",
        instruction_id: "Pilih main verb.",
        sentence: "A business analyst must elicit requirements.",
        question: "Mana main verb kalimat ini?",
        options: ["A business analyst", "must elicit", "requirements"],
        correct_answer: "must elicit",
        explanation_id: "\"must elicit\" adalah main verb.",
        difficulty: "basic",
        grammar_trap: "Jangan pilih subject sebagai verb.",
        ba_context_note: "Elicit berarti menggali requirement."
      }
    ]
  };
  return base;
}

function labelFromKey(key) {
  return String(key || "")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function renderVocabulary() {
  const vocabularyItems = getVocabulary();
  ensureDailyVocabularyDrill(vocabularyItems);
  const dailyItems = getDailyVocabularyItems(vocabularyItems);
  const drillStats = getVocabularyDrillStats(dailyItems);
  document.getElementById("vocabularyView").innerHTML = `
    ${pageHeaderTemplate({
      eyebrow: "Vocabulary Drill",
      title: "Target hari ini: 25 kata vocabulary.",
      description: "Jawab arti Indonesia yang paling tepat. Fokus harian kecil lebih penting daripada menghafal semua sekaligus.",
      actions: `<button id="vocabHelpButton" class="ghost-button">Cara hafal kata</button>`
    })}
    ${journeyPanel("Vocabulary")}

    <section class="reminder-card ${drillStats.completed ? "done" : ""}">
      <div>
        <strong>${drillStats.completed ? "Target harian selesai" : "Pengingat belajar hari ini"}</strong>
        <p>${drillStats.completed ? "Bagus. Kamu sudah menyelesaikan 25 kata hari ini. Ulangi kata yang salah agar makin nempel." : `Masih ada ${drillStats.remaining} kata lagi. Target kecil: jawab 25 kata, tidak harus sempurna.`}</p>
      </div>
      <button id="resetDailyDrill" class="ghost-button">Acak ulang drill</button>
    </section>

    <section class="vocab-progress-panel">
      <div class="metric">
        <span class="muted">Terjawab</span>
        <strong>${drillStats.answered}/${drillStats.total}</strong>
        <div class="progress-bar"><span style="width:${drillStats.progressPercent}%"></span></div>
      </div>
      <div class="metric">
        <span class="muted">Benar</span>
        <strong>${drillStats.correct}</strong>
        <small>Akurasi ${drillStats.accuracyPercent}%</small>
      </div>
      <div class="metric">
        <span class="muted">Salah</span>
        <strong>${drillStats.wrong}</strong>
        <small>${drillStats.reviewWords.length ? `Ulangi: ${drillStats.reviewWords.slice(0, 3).join(", ")}` : "Belum ada kata salah."}</small>
      </div>
      <div class="metric">
        <span class="muted">Status</span>
        <strong class="metric-word">${drillStats.completed ? "Selesai" : "Berjalan"}</strong>
        <small>${state.vocabularyDrill.date}</small>
      </div>
    </section>

    <section class="module-surface">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Daily Drill</p>
          <h3>Drill 25 Kata Hari Ini</h3>
          <p>Baca word, lihat contoh kalimat, lalu pilih arti Indonesia. Kata yang salah akan muncul di ringkasan review.</p>
        </div>
      </div>
      <div class="drill-list">
        ${dailyItems.map((item, index) => vocabularyDrillTemplate(item, index, vocabularyItems)).join("")}
      </div>
    </section>

    <section class="module-surface">
      <h3>Bank Kosakata</h3>
      <p class="muted">Total kosakata tersedia: ${vocabularyItems.length}. Drill harian mengambil 25 kata secara acak setiap hari.</p>
      <div class="vocab-bank">
        ${vocabularyItems.map((item) => `<span class="pill">${item.word} = ${item.meaningId} ${renderContextualHelpButton("vocabulary", "vocabulary_word", item.word)}</span>`).join("")}
      </div>
    </section>
  `;

  document.getElementById("vocabHelpButton").addEventListener("click", () => {
    openHelpWith("elicit, validate, prioritize, assess, stakeholder, requirement");
  });

  document.getElementById("resetDailyDrill").addEventListener("click", () => {
    state.vocabularyDrill = createVocabularyDrill(vocabularyItems, true);
    saveState();
    renderVocabulary();
    renderDashboard();
  });

  document.querySelectorAll("[data-vocab-drill]").forEach((button) => {
    button.addEventListener("click", async () => {
      const item = getVocabulary().find((entry) => entry.id === button.dataset.vocabDrill);
      let isCorrect = button.dataset.answer === item.answer || button.dataset.answer === item.meaningId;
      let score = isCorrect ? 100 : 0;
      if (apiOnline) {
        try {
          const response = await apiRequest("/vocabulary/submit-answer", {
            method: "POST",
            body: {
              user_id: state.user?.id || "default-user",
              itemId: item.id,
              answer: button.dataset.answer
            }
          });
          isCorrect = response.isCorrect;
          score = response.score;
        } catch (error) {
          apiOnline = false;
        }
      }
      state.vocabularyAnswers[item.id] = isCorrect;
      state.vocabularyDrill.answers[item.id] = {
        selected: button.dataset.answer,
        isCorrect,
        answeredAt: new Date().toISOString()
      };
      state.progress.Vocabulary = Math.max(state.progress.Vocabulary, calculateVocabularyScore());
      state.completedExercises += 1;
      addActivity("Vocabulary", item.word, score);
      saveState();
      await refreshIntegratedJourney();
      renderVocabulary();
      renderDashboard();
      renderJourney();
    });
  });
  bindContextualHelpButtons(document.getElementById("vocabularyView"));
}

function vocabularyDrillTemplate(item, index, allItems) {
  const answered = state.vocabularyDrill.answers[item.id];
  const options = vocabularyOptions(item, allItems);
  return `
    <article class="vocab-card ${answered ? (answered.isCorrect ? "correct" : "wrong") : ""}">
      <div class="vocab-card-head">
        <span class="pill">#${index + 1}</span>
        <span class="pill">${escapeHtml(item.part)}</span>
      </div>
      <h3>${escapeHtml(item.word)}</h3>
      <p class="vocab-example">${escapeHtml(item.example)}</p>
      <p class="muted">${escapeHtml(item.meaningEn)}</p>
      <div class="question-options">
        ${options
          .map((option) => `
            <button class="option-button ${answered?.selected === option ? "selected" : ""}" data-vocab-drill="${item.id}" data-answer="${option}">${option}</button>
          `)
          .join("")}
      </div>
      ${answered === undefined ? "" : resultTemplate(answered.isCorrect ? "success" : "danger", answered.isCorrect ? "Benar" : "Belum tepat", answered.isCorrect ? "Makna sudah sesuai konteks." : `Jawaban benar: ${item.meaningId}`)}
    </article>
  `;
}

function vocabularyHelpContext(item) {
  return {
    word: item.word,
    meaning: item.meaningId,
    meaning_en: item.meaningEn,
    example: item.example,
    answer: item.answer
  };
}

function calculateVocabularyScore() {
  const dailyItems = getDailyVocabularyItems(getVocabulary());
  const stats = getVocabularyDrillStats(dailyItems);
  return stats.total ? stats.accuracyPercent : 0;
}

function todayKey() {
  return new Date().toLocaleDateString("en-CA");
}

function ensureDailyVocabularyDrill(vocabularyItems) {
  const date = todayKey();
  const currentIds = new Set(vocabularyItems.map((item) => item.id));
  const expectedSize = Math.min(25, vocabularyItems.length);
  const isValid =
    state.vocabularyDrill.date === date &&
    state.vocabularyDrill.wordIds.length === expectedSize &&
    state.vocabularyDrill.wordIds.every((id) => currentIds.has(id));
  if (!isValid) {
    state.vocabularyDrill = createVocabularyDrill(vocabularyItems);
    saveState();
  }
}

function createVocabularyDrill(vocabularyItems, forceShuffle = false) {
  const date = todayKey();
  const seed = `${date}-${forceShuffle ? Date.now() : "daily"}`;
  return {
    date,
    wordIds: seededShuffle(vocabularyItems, seed).slice(0, Math.min(25, vocabularyItems.length)).map((item) => item.id),
    answers: {}
  };
}

function getDailyVocabularyItems(vocabularyItems) {
  const byId = new Map(vocabularyItems.map((item) => [item.id, item]));
  return state.vocabularyDrill.wordIds.map((id) => byId.get(id)).filter(Boolean);
}

function getVocabularyDrillStats(dailyItems) {
  const answers = state.vocabularyDrill.answers || {};
  const total = dailyItems.length;
  const answered = dailyItems.filter((item) => answers[item.id]).length;
  const correct = dailyItems.filter((item) => answers[item.id]?.isCorrect).length;
  const wrong = dailyItems.filter((item) => answers[item.id] && !answers[item.id].isCorrect).length;
  const remaining = Math.max(0, total - answered);
  const reviewWords = dailyItems.filter((item) => answers[item.id] && !answers[item.id].isCorrect).map((item) => item.word);
  return {
    total,
    answered,
    correct,
    wrong,
    remaining,
    reviewWords,
    completed: total > 0 && answered >= total,
    progressPercent: total ? Math.round((answered / total) * 100) : 0,
    accuracyPercent: answered ? Math.round((correct / answered) * 100) : 0
  };
}

function vocabularyOptions(item, allItems) {
  const distractors = seededShuffle(
    allItems.filter((entry) => entry.id !== item.id),
    `${state.vocabularyDrill.date}-${item.id}`
  )
    .map((entry) => entry.meaningId)
    .slice(0, 3);
  return seededShuffle(dedupeValues([item.meaningId, ...distractors]), `${item.id}-options`).slice(0, 4);
}

function seededShuffle(items, seedText) {
  return [...items]
    .map((item, index) => ({
      item,
      score: hashText(`${seedText}-${item.id || item}-${index}`)
    }))
    .sort((a, b) => a.score - b.score)
    .map((entry) => entry.item);
}

function hashText(text) {
  let hash = 2166136261;
  for (let index = 0; index < text.length; index += 1) {
    hash ^= text.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

function dedupeValues(values) {
  return values.filter((value, index, array) => value && array.indexOf(value) === index);
}

function renderTutor() {
  document.getElementById("tutorView").innerHTML = `
    ${pageHeaderTemplate({
      eyebrow: "AI Tutor Internal",
      title: "Mentor TOEFL untuk calon Business Analyst.",
      description: "Tanyakan grammar, vocabulary, writing, atau minta latihan singkat dalam Bahasa Indonesia."
    })}
    <section class="tutor-layout">
      <div class="module-surface tutor-chat-panel">
        <div id="chatLog" class="chat-log">
          ${state.chat.map((message) => `
            <div class="chat-message ${message.role}">
              <p>${escapeHtml(message.text)}</p>
              ${renderContextualHelpButton("tutor", message.role === "assistant" ? "tutor_message" : "user_sentence", message.text)}
            </div>
          `).join("")}
        </div>
      </div>
      <form id="chatForm" class="module-surface form-grid tutor-input-panel">
        ${beginnerTip("Tips bertanya", "Kalau bingung, tulis saja kalimat Inggrisnya lalu tanya: artinya apa, subject-nya apa, verb-nya apa.")}
        ${moduleQuickActions([
          { label: "Jelaskan grammar", attr: `data-chat-prompt="Jelaskan grammar kalimat ini secara sederhana."` },
          { label: "Buat latihan", attr: `data-chat-prompt="Buatkan latihan TOEFL kecil untuk saya."` },
          { label: "Review vocabulary", attr: `data-chat-prompt="Review 5 vocabulary BA yang sering muncul."` }
        ])}
        <label>
          Pertanyaan
          <textarea id="chatInput" placeholder="Contoh: Saya tidak paham kenapa operating bukan verb utama."></textarea>
        </label>
        <button class="primary-button" type="submit">Kirim ke Tutor</button>
      </form>
    </section>
  `;

  document.getElementById("chatForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const input = document.getElementById("chatInput").value.trim();
    if (!input) return;
    state.chat.push({ role: "user", text: input });
    let reply = tutorReply(input);
    if (apiOnline) {
      try {
        const response = await apiRequest("/ai-tutor/chat", {
          method: "POST",
          body: { message: input, progress: state.progress }
        });
        reply = response.reply;
      } catch (error) {
        apiOnline = false;
      }
    }
    state.chat.push({ role: "assistant", text: reply });
    saveState();
    renderTutor();
  });
  document.querySelectorAll("[data-chat-prompt]").forEach((button) => {
    button.addEventListener("click", () => {
      document.getElementById("chatInput").value = button.dataset.chatPrompt;
      document.getElementById("chatInput").focus();
    });
  });
  bindContextualHelpButtons(document.getElementById("tutorView"));
}

function tutorReply(input) {
  const text = input.toLowerCase();
  if (text.includes("operating") || text.includes("verb")) {
    return "Dalam kalimat BA, operating biasanya bukan main verb jika ia menerangkan noun sebelumnya. Main verb adalah kata kerja yang membawa aksi utama, misalnya must elicit atau must ensure.";
  }
  if (text.includes("rekomendasi") || text.includes("latihan")) {
    return recommendationText();
  }
  if (text.includes("requirement")) {
    return "Requirement yang baik harus jelas, dapat diuji, dan tidak ambigu. Jika stakeholder berkata 'flexible', BA perlu bertanya: flexible dalam kondisi apa, untuk siapa, dan bagaimana cara mengukurnya.";
  }
  return "Saya sarankan mulai dari satu kalimat pendek, temukan subject dan main verb, lalu cek apakah ada phrase tambahan. Untuk konteks BA, selalu hubungkan arti kalimat dengan stakeholder, requirement, atau business goal.";
}

function renderWriting() {
  const writingPrompt = "Write a clear Business Analyst requirement statement. Use: The system must + verb + object + condition.";
  const writingSample = "The system must flexible for all user and make report faster.";
  document.getElementById("writingView").innerHTML = `
    ${pageHeaderTemplate({
      eyebrow: "Writing Evaluator",
      title: "Latihan writing profesional.",
      description: "Tulis requirement statement atau ringkasan meeting, lalu dapatkan feedback yang dipisah menjadi score, issue, revised sentence, dan next practice.",
      actions: `<button id="writingHelpButton" class="ghost-button">Bantu susun kalimat</button>`
    })}
    ${journeyPanel("Writing")}
    <section class="module-grid two writing-layout">
      <form id="writingForm" class="module-surface form-grid">
        ${beginnerTip("Formula writing basic", "Gunakan pola: The system must + verb + object + condition. Tambahkan ukuran agar requirement jelas.")}
        <div class="helper-banner">
          <strong>Prompt writing</strong>
          <p>${writingPrompt} ${renderContextualHelpButton("writing", "writing_prompt", writingPrompt)}</p>
        </div>
        <label>
          Tulisan user
          <textarea id="writingInput">${writingSample}</textarea>
        </label>
        ${renderContextualHelpButton("writing", "writing_sentence", writingSample)}
        <button class="primary-button" type="submit">Evaluate Writing</button>
      </form>
      <div id="writingResult" class="module-surface">
        ${emptyStateTemplate("Feedback akan muncul di sini", "Submit tulisan untuk melihat score, grammar issue, suggestion, dan revised sentence.")}
      </div>
    </section>
  `;

  document.getElementById("writingHelpButton").addEventListener("click", () => {
    openHelpWith(document.getElementById("writingInput").value);
  });

  document.getElementById("writingForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const text = document.getElementById("writingInput").value.trim();
    let feedback = {
      score: 68,
      issues: ["Grammar agreement and vague requirement."],
      revised: "The system must be flexible enough to generate reports faster for different user roles.",
      recommendation: "Write one measurable acceptance criterion."
    };
    if (apiOnline) {
      try {
        feedback = await apiRequest("/writing/evaluate", {
          method: "POST",
          body: { text, user_id: state.user?.id || "default-user" }
        });
      } catch (error) {
        apiOnline = false;
      }
    }
    state.progress.Writing = Math.max(state.progress.Writing, feedback.score);
    state.completedExercises += 1;
    addActivity("Writing", "Requirement statement feedback", feedback.score);
    saveState();
    await refreshIntegratedJourney();
    document.getElementById("writingResult").innerHTML = writingFeedbackTemplate(feedback);
    bindContextualHelpButtons(document.getElementById("writingResult"));
    renderDashboard();
    renderJourney();
  });
  bindContextualHelpButtons(document.getElementById("writingView"));
}

function writingFeedbackTemplate(feedback) {
  return `
    <div class="writing-feedback-grid">
      <article class="analytics-card">
        <span>Score</span>
        <strong>${Math.round(feedback.score || 0)}</strong>
        <div class="progress-bar"><span style="width:${Math.min(Math.max(feedback.score || 0, 0), 100)}%"></span></div>
      </article>
      <article class="module-card soft">
        <h3>Grammar issue</h3>
        <p>${escapeHtml((feedback.issues || []).join(" ") || "Belum ada issue utama.")}</p>
      </article>
      <article class="module-card">
        <h3>Revised sentence</h3>
        <p>${escapeHtml(feedback.revised || "")} ${renderContextualHelpButton("writing", "writing_feedback", feedback.revised || "")}</p>
      </article>
      <article class="module-card">
        <h3>Next practice</h3>
        <p>${escapeHtml(feedback.recommendation || "Tulis ulang satu kalimat dengan ukuran yang jelas.")}</p>
      </article>
    </div>
  `;
}

function renderListening() {
  document.getElementById("listeningView").innerHTML = `
    ${pageHeaderTemplate({
      eyebrow: "AI Listening Engine",
      title: listeningScenario.title,
      description: "Latihan listening masih mock, tetapi alurnya dibuat seperti latihan nyata: dengar/scan transcript, pahami pertanyaan, lalu jawab.",
      actions: `<button id="listeningHelpButton" class="ghost-button">Jelaskan transcript</button>`
    })}
    ${journeyPanel("Listening")}
    <section class="module-grid two listening-layout">
      <div class="module-surface">
        <div class="audio-placeholder">
          <strong>Mock Audio</strong>
          <span>Transcript tersedia untuk latihan basic</span>
        </div>
        ${beginnerTip("Cara memahami listening", "Cari kata yang diulang atau ditekankan: late, delay, data, different formats. Biasanya itu petunjuk masalah utama.")}
        <h3>Transcript</h3>
        <p>${listeningScenario.transcript} ${renderContextualHelpButton("listening", "listening_transcript", listeningScenario.transcript, listeningHelpContext())}</p>
      </div>
      <form id="listeningForm" class="module-surface form-grid">
        <label>
          ${listeningScenario.question} ${renderContextualHelpButton("listening", "listening_question", listeningScenario.question, listeningHelpContext())}
          <textarea id="listeningInput"></textarea>
        </label>
        <button class="primary-button" type="submit">Submit Listening</button>
        <div id="listeningResult"></div>
      </form>
    </section>
  `;

  document.getElementById("listeningHelpButton").addEventListener("click", () => {
    openHelpWith(listeningScenario.transcript);
  });

  document.getElementById("listeningForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const answer = document.getElementById("listeningInput").value.toLowerCase();
    let result = {
      score: answer.includes("inconsistent") || answer.includes("format") || answer.includes("data") ? 85 : 45,
      isCorrect: answer.includes("inconsistent") || answer.includes("format") || answer.includes("data"),
      idealAnswer: listeningScenario.answer,
      explanation: "Jawaban ideal menangkap masalah data sebelum consolidation."
    };
    if (apiOnline) {
      try {
        result = await apiRequest("/listening/submit-answer", {
          method: "POST",
          body: { answer, user_id: state.user?.id || "default-user" }
        });
      } catch (error) {
        apiOnline = false;
      }
    }
    state.progress.Listening = Math.max(state.progress.Listening, result.score);
    state.completedExercises += 1;
    addActivity("Listening", listeningScenario.title, result.score);
    saveState();
    await refreshIntegratedJourney();
    document.getElementById("listeningResult").innerHTML = resultTemplate(
      result.isCorrect ? "success" : "warning",
      result.isCorrect ? "Jawaban sesuai" : "Perlu diperjelas",
      `${result.explanation} Jawaban ideal: ${result.idealAnswer}`
    );
    renderDashboard();
    renderJourney();
  });
  bindContextualHelpButtons(document.getElementById("listeningView"));
}

function listeningHelpContext() {
  return {
    transcript: listeningScenario.transcript,
    question_text: listeningScenario.question,
    ideal_answer: listeningScenario.answer
  };
}

function renderScenario() {
  document.getElementById("scenarioView").innerHTML = `
    ${pageHeaderTemplate({
      eyebrow: "Scenario-Based BA Practice",
      title: "Latih keputusan Business Analyst dalam bahasa Inggris.",
      description: "Pisahkan konteks kasus, pertanyaan, opsi, dan alasan. Jangan langsung memilih solusi sebelum memahami masalah bisnis.",
      actions: `<button id="scenarioHelpButton" class="ghost-button">Bantu pahami skenario</button>`
    })}
    ${beginnerTip("Cara menjawab scenario", "Sebagai BA, jangan langsung membuat solusi. Biasanya langkah pertama adalah clarify, elicit, validate, atau align.")}
    <section class="scenario-list">
      ${scenarioQuestions.map(scenarioTemplate).join("")}
    </section>
  `;

  document.getElementById("scenarioHelpButton").addEventListener("click", () => {
    openHelpWith(scenarioQuestions[0].context);
  });

  document.querySelectorAll("[data-scenario]").forEach((button) => {
    button.addEventListener("click", async () => {
      const scenario = scenarioQuestions.find((item) => item.id === button.dataset.scenario);
      const selected = Number(button.dataset.option);
      let score = selected === scenario.answer ? 100 : 0;
      state.scenarioAnswers[scenario.id] = selected;
      if (apiOnline) {
        try {
          const response = await apiRequest("/scenario/submit-answer", {
            method: "POST",
            body: {
              user_id: state.user?.id || "default-user",
              questionId: scenario.id,
              selected
            }
          });
          score = response.score;
        } catch (error) {
          apiOnline = false;
        }
      }
      state.progress.Scenario = Math.max(state.progress.Scenario, score);
      state.completedExercises += 1;
      addActivity("Scenario", scenario.title, score);
      saveState();
      await refreshIntegratedJourney();
      renderScenario();
      renderDashboard();
      renderJourney();
    });
  });
  bindContextualHelpButtons(document.getElementById("scenarioView"));
}

function scenarioTemplate(item) {
  const selected = state.scenarioAnswers[item.id];
  const answered = selected !== undefined;
  const isCorrect = selected === item.answer;
  return `
    <article class="scenario-card">
      <div class="pill-row">
        <span class="pill">BA Decision</span>
        <span class="pill">Scenario</span>
      </div>
      <h3>${item.title}</h3>
      <div class="case-box">
        <strong>Konteks kasus</strong>
        <p>${item.context} ${renderContextualHelpButton("scenario", "scenario_case", item.context, scenarioHelpContext(item))}</p>
      </div>
      <div class="case-box soft">
        <strong>Pertanyaan BA</strong>
        <p>${item.question} ${renderContextualHelpButton("scenario", "scenario_question", item.question, scenarioHelpContext(item))}</p>
      </div>
      <div class="question-options">
        ${item.options
          .map(
            (option, index) => `
              <div class="option-help-row">
                <button class="option-button ${selected === index ? "selected" : ""}" data-scenario="${item.id}" data-option="${index}">
                  ${String.fromCharCode(65 + index)}. ${option}
                </button>
                ${renderContextualHelpButton("scenario", "scenario_option", option, {
                  ...scenarioHelpContext(item),
                  option_label: String.fromCharCode(65 + index),
                  option_text: option
                })}
              </div>
            `
          )
          .join("")}
      </div>
      ${answered ? resultTemplate(isCorrect ? "success" : "warning", isCorrect ? "Reasoning tepat" : "Reasoning perlu diperbaiki", item.explanation) : ""}
    </article>
  `;
}

function scenarioHelpContext(item) {
  return {
    case_text: item.context,
    question_text: item.question,
    correct_answer: item.options?.[item.answer] || "",
    explanation: item.explanation,
    ba_skill: item.title
  };
}

function renderAdmin() {
  document.getElementById("adminView").innerHTML = `
    ${pageHeaderTemplate({
      eyebrow: "Admin CMS",
      title: "Kelola konten latihan awal.",
      description: "CMS lokal ini menyimpan konten tambahan di browser dan backend jika API aktif. Edit/delete penuh masih roadmap, jadi UI hanya menampilkan tambah dan daftar konten."
    })}
    <section class="module-grid two admin-editor-grid">
      <form id="lessonForm" class="module-surface form-grid">
        <h3>Tambah Reading Lesson</h3>
        <label>Judul<input id="lessonTitle" required value="Solution Evaluation Memo" /></label>
        <label>Level
          <select id="lessonLevel">
            <option>Foundation</option>
            <option>Intermediate</option>
            <option>Advanced</option>
          </select>
        </label>
        <label>Konteks BA<input id="lessonContext" required value="Solution evaluation" /></label>
        <label>Passage<textarea id="lessonPassage" required>The analyst evaluates whether the proposed solution improves reporting accuracy and supports stakeholder decision-making.</textarea></label>
        <button class="primary-button" type="submit">Simpan Lesson</button>
      </form>
      <form id="vocabForm" class="module-surface form-grid">
        <h3>Tambah Vocabulary</h3>
        <label>Word<input id="vocabWord" required value="assess" /></label>
        <label>Part of speech<input id="vocabPart" required value="verb" /></label>
        <label>Meaning Indonesia<input id="vocabMeaningId" required value="menilai" /></label>
        <label>Meaning English<input id="vocabMeaningEn" required value="to evaluate or judge something" /></label>
        <label>Example<textarea id="vocabExample" required>The analyst assesses the impact of the proposed change.</textarea></label>
        <button class="primary-button" type="submit">Simpan Vocabulary</button>
      </form>
    </section>
    <section class="module-surface">
      <h3>Konten Tambahan</h3>
      <div class="module-grid two">
        <div>
          <p class="muted">Lessons: ${state.adminContent.lessons.length}</p>
          <div class="lesson-list compact-list">
            ${
              state.adminContent.lessons
                .map((lesson) => `<div class="activity-row"><strong>${lesson.title}</strong><span>${lesson.context}</span><small>${lesson.level}</small></div>`)
                .join("") || emptyStateTemplate("Belum ada lesson tambahan", "Tambah lesson dari form di atas. Edit/delete akan ditambahkan pada fase CMS berikutnya.")
            }
          </div>
        </div>
        <div>
          <p class="muted">Vocabulary: ${state.adminContent.vocabulary.length}</p>
          <div class="lesson-list compact-list">
            ${
              state.adminContent.vocabulary
                .map((item) => `<div class="activity-row"><strong>${item.word}</strong><span>${item.meaningId}</span><small>${item.part}</small></div>`)
                .join("") || emptyStateTemplate("Belum ada vocabulary tambahan", "Tambah vocabulary dari form di atas. Edit/delete belum aktif.")
            }
          </div>
        </div>
      </div>
    </section>
  `;

  document.getElementById("lessonForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const now = Date.now();
    const lesson = {
      id: `custom-reading-${now}`,
      title: document.getElementById("lessonTitle").value.trim(),
      level: document.getElementById("lessonLevel").value,
      context: document.getElementById("lessonContext").value.trim(),
      passage: document.getElementById("lessonPassage").value.trim(),
      vocabulary: ["evaluate", "solution", "stakeholder"],
      grammar: "Focus: identify subject, main verb, and object in a professional BA sentence.",
      questions: [
        {
          id: `custom-q-${now}`,
          text: "What is the main purpose of the passage?",
          options: [
            "To describe a BA-related professional situation.",
            "To ignore stakeholder needs.",
            "To remove all business goals.",
            "To avoid analysis."
          ],
          answer: 0,
          explanation: "The passage describes a Business Analyst context and its purpose."
        }
      ]
    };
    let savedLesson = lesson;
    if (apiOnline) {
      try {
        const response = await apiRequest("/lessons", {
          method: "POST",
          body: lesson
        });
        savedLesson = response.lesson;
        state.remoteContent.lessons = [savedLesson, ...(state.remoteContent.lessons || [])];
      } catch (error) {
        apiOnline = false;
      }
    }
    state.adminContent.lessons.unshift(savedLesson);
    state.selectedReadingLessonId = savedLesson.id;
    saveState();
    renderAdmin();
  });

  document.getElementById("vocabForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const meaningId = document.getElementById("vocabMeaningId").value.trim();
    const item = {
      id: `custom-vocab-${Date.now()}`,
      word: document.getElementById("vocabWord").value.trim(),
      part: document.getElementById("vocabPart").value.trim(),
      meaningId,
      meaningEn: document.getElementById("vocabMeaningEn").value.trim(),
      example: document.getElementById("vocabExample").value.trim(),
      answer: meaningId
    };
    let savedItem = item;
    if (apiOnline) {
      try {
        const response = await apiRequest("/vocabulary", {
          method: "POST",
          body: item
        });
        savedItem = response.item;
        state.remoteContent.vocabulary = [savedItem, ...(state.remoteContent.vocabulary || [])];
      } catch (error) {
        apiOnline = false;
      }
    }
    state.adminContent.vocabulary.unshift(savedItem);
    saveState();
    renderAdmin();
  });
}

function recommendationText() {
  const skill = getWeakestSkill();
  const messages = {
    Reading: "Kerjakan satu passage BA pendek dan fokus pada main idea serta vocabulary in context.",
    Grammar: "Bedah satu kalimat panjang. Cari subject, main verb, lalu phrase tambahan.",
    Vocabulary: "Latih 3 kata BA hari ini: elicit, validate, dan prioritize.",
    Writing: "Tulis satu requirement statement yang jelas dan dapat diuji.",
    Listening: "Dengarkan atau baca satu meeting transcript pendek, lalu simpulkan masalah utamanya.",
    Scenario: "Kerjakan satu skenario BA dan latih memilih tindakan yang paling tepat sebelum solusi dibuat."
  };
  return messages[skill];
}

function beginnerTip(title, body) {
  return `
    <div class="beginner-tip">
      <strong>${title}</strong>
      <p>${body}</p>
    </div>
  `;
}

function openHelpWith(text) {
  state.helpInput = text;
  state.activeView = "help";
  saveState();
  render();
}

function getWeakestSkill() {
  return Object.entries(state.progress).sort((a, b) => a[1] - b[1])[0][0];
}

function overallProgress() {
  const scores = Object.values(state.progress);
  return Math.round(scores.reduce((sum, score) => sum + score, 0) / scores.length);
}

function localAnalytics() {
  const progressEntries = Object.entries(state.progress);
  const scores = progressEntries.map((entry) => entry[1]);
  const averageScore = scores.length ? Math.round(scores.reduce((sum, score) => sum + score, 0) / scores.length) : 0;
  const sorted = [...progressEntries].sort((a, b) => a[1] - b[1]);
  return {
    averageScore,
    weakestSkill: sorted[0]?.[0] || "Grammar",
    strongestSkill: sorted[sorted.length - 1]?.[0] || "Reading",
    completedExercises: state.completedExercises,
    activityCount: state.activity.length,
    status: averageScore >= 45 ? "Progress mulai terbentuk." : "Masih tahap awal."
  };
}

function resultTemplate(type, title, body) {
  return `<div class="result-box ${type}"><strong>${title}</strong><p>${body}</p></div>`;
}

function getLessons() {
  if (state.remoteContent.lessons) {
    return dedupeById([...state.adminContent.lessons, ...state.remoteContent.lessons]);
  }
  return dedupeById([...state.adminContent.lessons, ...lessons]);
}

function getVocabulary() {
  if (state.remoteContent.vocabulary) {
    return dedupeById([...state.adminContent.vocabulary, ...state.remoteContent.vocabulary]);
  }
  return dedupeById([...state.adminContent.vocabulary, ...vocabulary]);
}

function calculateScenarioScore() {
  const correct = scenarioQuestions.filter((item) => state.scenarioAnswers[item.id] === item.answer).length;
  return Math.round((correct / scenarioQuestions.length) * 100);
}

function addActivity(module, summary, score) {
  state.activity.unshift({
    module,
    summary,
    score: `Score ${score}`
  });
  state.activity = state.activity.slice(0, 12);
}

function dedupeById(items) {
  const seen = new Set();
  return items.filter((item) => {
    if (seen.has(item.id)) return false;
    seen.add(item.id);
    return true;
  });
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll("\n", "&#10;").replaceAll("\r", "");
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
