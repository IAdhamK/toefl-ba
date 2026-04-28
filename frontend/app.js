const STORAGE_KEY = "toeflAnalystAiState";
const API_BASE = window.location.origin.includes("8001")
  ? `${window.location.origin}/api`
  : "http://127.0.0.1:8001/api";
let apiOnline = false;

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
    guidedReading: { ...structuredClone(defaultState.guidedReading), ...(parsed.guidedReading || {}) },
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
        guidedReading: { ...structuredClone(defaultState.guidedReading), ...(stateResponse.state.guidedReading || state.guidedReading || {}) }
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
  } catch (error) {
    apiOnline = false;
    state.integratedJourney = localJourneySummary();
    state.readingJourney = localReadingJourney();
    state.readingReview = localReadingReview();
    state.readingTrainer = localReadingTrainerState();
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
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (error) {
    apiOnline = false;
    state.readingJourney = localReadingJourney();
    state.readingReview = localReadingReview();
    state.readingTrainer = localReadingTrainerState();
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
    button.addEventListener("click", () => {
      state.activeView = button.dataset.view;
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

function renderDashboard() {
  const weakest = getWeakestSkill();
  const recentActivity = state.activity.slice(0, 5);
  const apiStatus = apiOnline ? "Backend API aktif" : "Mode lokal";
  const recommendation = state.latestRecommendation?.recommendation || recommendationText();
  const analytics = state.latestAnalytics || localAnalytics();
  document.getElementById("dashboardView").innerHTML = `
    <header class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm lg:p-6">
      <div class="flex flex-col gap-5 xl:flex-row xl:items-start xl:justify-between">
        <div class="max-w-3xl">
          <div class="mb-3 flex flex-wrap items-center gap-2">
            <span class="rounded-full bg-cyan-50 px-3 py-1 text-xs font-bold uppercase tracking-wide text-cyan-700">Beranda Belajar</span>
            <span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">${apiStatus}</span>
            <span class="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">Tailwind UI</span>
          </div>
          <h2 class="mb-3 text-2xl font-black leading-tight text-slate-900 lg:text-4xl">Halo, ${escapeHtml(state.user.name)}. Fokus hari ini: ${escapeHtml(weakest)}.</h2>
          <p class="max-w-2xl text-sm leading-6 text-slate-600 lg:text-base">Ikuti alur kecil yang jelas: pahami arti umum, cari subject dan verb utama, lalu lanjutkan latihan dari rekomendasi journey.</p>
        </div>
        <div class="flex flex-wrap gap-3">
          <button class="rounded-xl bg-cyan-700 px-4 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-cyan-800" data-go="journey">Lihat Perjalanan</button>
          <button class="rounded-xl bg-slate-900 px-4 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-slate-700" data-go="reading">Mulai Reading</button>
          <button class="rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-bold text-slate-700 transition hover:bg-slate-50" data-go="help">Bantuan ID</button>
        </div>
      </div>
    </header>

    ${integratedJourneySection()}

    <section class="grid gap-4 md:grid-cols-3">
      ${[
        ["1", "Pahami arti umum", "Cari dulu siapa melakukan apa. Jangan langsung terjebak grammar panjang."],
        ["2", "Temukan subject dan verb", "Subject adalah pelaku. Verb adalah aksi utama yang membawa makna."],
        ["3", "Kerjakan latihan kecil", "Skor membantu arah belajar, bukan untuk membuat panik."]
      ].map(([number, title, body]) => `
        <article class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <span class="mb-4 grid h-9 w-9 place-items-center rounded-full bg-cyan-700 text-sm font-black text-white">${number}</span>
          <h3 class="mb-2 text-base font-extrabold text-slate-900">${title}</h3>
          <p class="text-sm leading-6 text-slate-600">${body}</p>
        </article>
      `).join("")}
    </section>

    <section class="grid gap-4 sm:grid-cols-2 xl:grid-cols-6">
      ${Object.entries(state.progress).map(([skill, score]) => metricTemplate(skill, score)).join("")}
    </section>

    <section class="grid gap-4 xl:grid-cols-[1.1fr_0.9fr]">
      <div class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div class="mb-4 flex items-center justify-between gap-3">
          <div>
            <h3 class="text-lg font-extrabold text-slate-900">Learning Path</h3>
            <p class="text-sm text-slate-500">Alur Business Analyst yang sedang dilatih.</p>
          </div>
          <span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-bold text-slate-600">BA Context</span>
        </div>
        <div class="grid gap-3 md:grid-cols-3">
          ${["Stakeholder Need", "Requirement Clarity", "Strategy Alignment"].map((item, index) => `
            <div class="rounded-xl border border-slate-200 bg-slate-50 p-4">
              <span class="mb-3 block text-xs font-bold text-cyan-700">Step ${index + 1}</span>
              <strong class="block text-sm text-slate-900">${item}</strong>
            </div>
          `).join("")}
        </div>
      </div>
      <div class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <h3 class="mb-2 text-lg font-extrabold text-slate-900">Rekomendasi AI Tutor</h3>
        <p class="mb-4 text-sm leading-6 text-slate-600">${recommendation}</p>
        ${state.latestRecommendation?.target ? `<p class="mb-4 text-sm"><strong>Target:</strong> ${state.latestRecommendation.target}</p>` : ""}
        <div class="mb-2 h-2 overflow-hidden rounded-full bg-slate-100"><span class="block h-full rounded-full bg-cyan-700" style="width:${overallProgress()}%"></span></div>
        <p class="text-xs font-semibold text-slate-500">Total latihan selesai: ${state.completedExercises}</p>
      </div>
    </section>

    <section class="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
      ${dashboardAnalyticsCard("Average", analytics.averageScore, `${analytics.averageScore}%`, analytics.status)}
      ${dashboardAnalyticsCard("Weakest", analytics.weakestSkill, analytics.weakestSkill, "Skill prioritas hari ini.")}
      ${dashboardAnalyticsCard("Strongest", analytics.strongestSkill, analytics.strongestSkill, "Skill paling stabil.")}
      ${dashboardAnalyticsCard("Exercises", analytics.completedExercises, analytics.completedExercises, "Total latihan selesai.")}
      ${dashboardAnalyticsCard("Activity", analytics.activityCount, analytics.activityCount, "Log aktivitas tersimpan.")}
    </section>

    <section class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div class="mb-4 flex items-center justify-between gap-3">
        <h3 class="text-lg font-extrabold text-slate-900">Recent Activity</h3>
        <span class="text-xs font-bold text-slate-500">${recentActivity.length} aktivitas</span>
      </div>
      ${
        recentActivity.length
          ? `<div class="grid gap-2">${recentActivity
              .map((item) => `<div class="grid gap-2 rounded-xl border border-slate-100 bg-slate-50 p-3 md:grid-cols-[140px_1fr_90px] md:items-center"><strong class="text-sm text-slate-900">${item.module}</strong><span class="min-w-0 truncate text-sm text-slate-600">${item.summary}</span><small class="text-sm font-bold text-cyan-700 md:text-right">${item.score}</small></div>`)
              .join("")}</div>`
          : `<p class="text-sm text-slate-500">Belum ada aktivitas. Mulai satu latihan untuk mengisi progress.</p>`
      }
    </section>
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
    <header class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm lg:p-6">
      <div class="flex flex-col gap-5 xl:flex-row xl:items-start xl:justify-between">
        <div class="max-w-4xl">
          <span class="mb-3 inline-flex rounded-full bg-cyan-50 px-3 py-1 text-xs font-bold uppercase tracking-wide text-cyan-700">Perjalanan Belajar Saya</span>
          <h2 class="mb-3 text-2xl font-black leading-tight text-slate-900 lg:text-4xl">Satu peta belajar untuk semua skill TOEFL + Business Analyst.</h2>
          <p class="max-w-3xl text-sm leading-6 text-slate-600 lg:text-base">Progress tersimpan di backend jika API aktif. Kamu bisa lanjut dari aktivitas terakhir, melihat skill lemah, dan mengambil latihan adaptif tanpa mulai dari nol.</p>
        </div>
        <div class="flex flex-wrap gap-3">
          <button id="refreshJourneyButton" class="rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-bold text-slate-700 transition hover:bg-slate-50">Refresh Progress</button>
          <button class="rounded-xl bg-cyan-700 px-4 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-cyan-800" data-journey-continue>Lanjutkan Belajar</button>
        </div>
      </div>
    </header>
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
    <div class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
      <div class="mb-3 flex items-center justify-between gap-3">
        <span class="text-xs font-bold uppercase tracking-wide text-slate-500">${skill}</span>
        <strong class="text-lg font-black text-slate-900">${score}%</strong>
      </div>
      <div class="h-2 overflow-hidden rounded-full bg-slate-100">
        <span class="block h-full rounded-full bg-cyan-700" style="width:${score}%"></span>
      </div>
    </div>
  `;
}

function dashboardAnalyticsCard(label, rawValue, displayValue, note) {
  const numeric = typeof rawValue === "number" ? rawValue : null;
  return `
    <div class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
      <span class="mb-2 block text-xs font-bold uppercase tracking-wide text-slate-500">${label}</span>
      <strong class="block break-words text-2xl font-black text-slate-900">${escapeHtml(String(displayValue ?? "-"))}</strong>
      ${numeric !== null ? `<div class="mt-3 h-2 overflow-hidden rounded-full bg-slate-100"><span class="block h-full rounded-full bg-cyan-700" style="width:${Math.min(Math.max(numeric, 0), 100)}%"></span></div>` : ""}
      <small class="mt-3 block text-xs leading-5 text-slate-500">${escapeHtml(String(note || ""))}</small>
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
    <header class="topbar">
      <div>
        <p class="eyebrow">Bantuan Bahasa Indonesia</p>
        <h2>Tempel kalimat Inggris, lalu baca penjelasan versi pemula.</h2>
        <p>Fitur ini dibuat untuk user yang masih basic. Hasilnya fokus pada arti sederhana, kata kunci, pola subject-verb, dan contoh kalimat yang lebih mudah.</p>
      </div>
    </header>

    <section class="content-grid">
      <form id="helpForm" class="panel form-grid">
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
      <aside class="panel">
        <h3>Hasil Bantuan</h3>
        ${
          lastHelp
            ? helpResultTemplate(lastHelp)
            : `<p class="muted">Belum ada hasil. Coba masukkan satu kalimat bahasa Inggris yang membuat bingung.</p>`
        }
      </aside>
    </section>

    <section class="panel">
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
  document.getElementById("readingView").innerHTML = `
    <header class="topbar">
      <div>
        <p class="eyebrow">Reading Analyzer</p>
        <h2>${selectedLesson.title}</h2>
        <p>${selectedLesson.passage} ${renderContextualHelpButton("reading", "reading_passage", selectedLesson.passage, readingHelpContext(selectedLesson))}</p>
        <div class="pill-row">
          <span class="pill">${selectedLesson.level}</span>
          <span class="pill">${selectedLesson.context}</span>
        </div>
      </div>
      <button id="readingHelpButton" class="ghost-button">Jelaskan bacaan ini</button>
    </header>
    ${journeyPanel("Reading")}
    ${readingJourneySummary()}
    ${readingReviewPanel()}
    ${guidedReadingPanel(selectedLesson)}
    ${readingSubskillProgress()}
    ${readingTrainerPanel()}

    <section class="content-grid">
      <div class="panel">
        ${beginnerTip("Cara mengerjakan Reading", "Baca judul dan kalimat pertama. Cari ide utama, lalu cocokkan pilihan jawaban dengan kata kunci yang sama maknanya.")}
        <h3>TOEFL-style Questions</h3>
        ${selectedLesson.questions.map((question, index) => readingQuestionTemplate(question, index, selectedLesson)).join("")}
        <button id="submitReading" class="primary-button">Submit Reading</button>
        <div id="readingResult"></div>
      </div>
      <aside class="panel">
        <h3>Lesson List</h3>
        <div class="lesson-list compact-list">
          ${allLessons.map((lesson) => `<button class="ghost-button ${lesson.id === selectedLesson.id ? "selected-control" : ""}" data-lesson="${lesson.id}">${lesson.title}</button>`).join("")}
        </div>
        <h3>Grammar Insight</h3>
        <p>${selectedLesson.grammar} ${renderContextualHelpButton("grammar", "grammar_explanation", selectedLesson.grammar)}</p>
        <h3>Vocabulary</h3>
        <div class="pill-row">${selectedLesson.vocabulary.map((word) => `<span class="pill">${word} ${renderContextualHelpButton("vocabulary", "vocabulary_word", word)}</span>`).join("")}</div>
      </aside>
    </section>
  `;

  document.getElementById("readingHelpButton").addEventListener("click", () => {
    openHelpWith(selectedLesson.passage);
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

  document.getElementById("submitReading").addEventListener("click", async () => {
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
    document.getElementById("readingResult")?.scrollIntoView({ behavior: "smooth", block: "center" });
  });

  document.getElementById("retryWeakReadingSkillButton")?.addEventListener("click", async () => {
    const subSkill = state.readingReview?.recommended_sub_skill || "main_idea";
    if (apiOnline) {
      await refreshReadingTrainer(subSkill);
    } else {
      state.readingTrainer = localReadingTrainerState(subSkill);
    }
    saveState();
    renderReading();
    document.getElementById("readingTrainerPanel")?.scrollIntoView({ behavior: "smooth", block: "start" });
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
}

function readingJourneySummary() {
  const journey = state.readingJourney || localReadingJourney();
  const strongest = journey.strong_subskills?.[0];
  const weakest = journey.weak_subskills?.[0];
  return `
    <section class="panel">
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
      <button id="continueReadingButton" class="primary-button" type="button">Lanjutkan Reading</button>
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
    <section class="panel">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Reading Review</p>
          <h3>Laporan kelemahan Reading</h3>
          <p>${escapeHtml(review.mentor_message || "Review membantu kamu tahu pola salah dan latihan berikutnya.")}</p>
        </div>
        <button id="retryWeakReadingSkillButton" class="primary-button" type="button">Latihan Ulang Skill Lemah</button>
      </div>
      <div class="drill-result-grid">
        <div class="metric">
          <span class="muted">Weakness utama</span>
          <strong class="metric-word">${escapeHtml(primary.label || readingSubskillLabel(review.recommended_sub_skill))}</strong>
          <small>${Math.round(primary.mastery_score || 0)}% mastery</small>
        </div>
        <div class="metric">
          <span class="muted">Weakness kedua</span>
          <strong class="metric-word">${escapeHtml(secondary.label || "Belum ada")}</strong>
          <small>${Math.round(secondary.mastery_score || 0)}% mastery</small>
        </div>
        <div class="metric">
          <span class="muted">Recommended practice</span>
          <strong class="metric-word">${escapeHtml(readingSubskillLabel(review.recommended_sub_skill))}</strong>
          <small>${escapeHtml(review.recommended_practice || "")}</small>
        </div>
        <div class="metric">
          <span class="muted">Bantuan ID</span>
          <strong class="metric-word">${escapeHtml(weakness.bantuan_id_usage?.level || "normal")}</strong>
          <small>${escapeHtml(weakness.bantuan_id_usage?.message || "")}</small>
        </div>
      </div>
      <div class="content-grid compact-grid">
        <div>
          <h3>Mistake pattern</h3>
          <div class="lesson-list compact-list">
            ${patterns.length ? patterns.map((item) => `
              <p><strong>${escapeHtml(item.label || readingSubskillLabel(item.sub_skill))}</strong><br>${escapeHtml(item.pattern || "")}<br><span class="muted">${escapeHtml(item.recommendation || "")}</span></p>
            `).join("") : `<p class="muted">Belum ada pola salah yang cukup kuat.</p>`}
          </div>
        </div>
        <div>
          <h3>Review queue</h3>
          <div class="lesson-list compact-list">
            ${queue.length ? queue.map((item) => `
              <p><strong>${escapeHtml(item.title || "")}</strong><br>${escapeHtml(item.reason || "")}<br><span class="muted">${escapeHtml(item.action || "")}</span></p>
            `).join("") : `<p class="muted">Belum ada item review.</p>`}
          </div>
        </div>
      </div>
      ${(lowPassages.length || vocab.length) ? `
        <div class="content-grid compact-grid">
          <div>
            <h3>Passage skor rendah</h3>
            <div class="lesson-list compact-list">
              ${lowPassages.length ? lowPassages.map((item) => `<p><strong>${escapeHtml(item.activity_id || "")}</strong><br><span class="muted">Skor ${Math.round(item.accuracy || 0)}% · ${escapeHtml(item.feedback || "")}</span></p>`).join("") : `<p class="muted">Belum ada passage rendah.</p>`}
            </div>
          </div>
          <div>
            <h3>Vocabulary perlu review</h3>
            <div class="lesson-list compact-list">
              ${vocab.length ? vocab.map((item) => `<p><strong>${escapeHtml(item.word || "")}</strong>: ${escapeHtml(item.meaning_id || "")}<br><span class="muted">${escapeHtml(item.reason || "")}</span></p>`).join("") : `<p class="muted">Belum ada vocabulary Reading yang sering salah.</p>`}
            </div>
          </div>
        </div>
      ` : ""}
    </section>
  `;
}

function guidedReadingPanel(lesson) {
  const guided = state.guidedReading?.lessonId === lesson.id ? state.guidedReading : structuredClone(defaultState.guidedReading);
  const hasSteps = guided.started && guided.steps?.length;
  const activeIndex = Math.min(guided.activeStep || 0, Math.max((guided.steps || []).length - 1, 0));
  const visibleSteps = hasSteps ? guided.steps.slice(0, activeIndex + 1) : [];
  return `
    <section class="panel" id="guidedReadingPanel">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Guided Reading Mode</p>
          <h3>Baca passage langkah demi langkah</h3>
          <p>Mode ini membantu pemula memahami judul, kalimat pertama, subject/verb, vocabulary, paragraph map, dan main idea sebelum menjawab soal.</p>
        </div>
        <button id="startGuidedReadingButton" class="primary-button" type="button">${hasSteps ? "Ulangi Guided Reading" : "Mulai Guided Reading"}</button>
      </div>
      ${hasSteps ? `
        <div class="lesson-list">
          ${visibleSteps.map((step) => guidedReadingStepCard(step, lesson)).join("")}
        </div>
        ${guided.completed ? "" : `
          <button id="nextGuidedReadingStepButton" class="ghost-button" type="button">
            ${activeIndex >= guided.steps.length - 1 ? "Selesai Guided Reading" : "Lanjut ke Langkah Berikutnya"}
          </button>
        `}
        ${guided.completed ? resultTemplate("success", "Guided Reading selesai", "Aktivitas pendukung sudah dicatat. Sekarang lanjut jawab TOEFL-style Questions di bawah.") : ""}
      ` : `
        ${beginnerTip("Kenapa pakai Guided Reading?", "Kalau masih basic, jangan langsung loncat ke soal. Pahami dulu bagian kecil dari passage supaya pilihan jawaban lebih mudah dibandingkan.")}
      `}
    </section>
  `;
}

function guidedReadingStepCard(step, lesson) {
  const contextType = step.bantuan_context_type || "reading_paragraph";
  const helpContext = readingHelpContext(lesson, lesson.questions?.[0]);
  return `
    <div class="question">
      <p class="eyebrow">Step ${step.step}</p>
      <h3>${escapeHtml(step.title || "")} ${step.focus_text ? renderContextualHelpButton("reading", contextType, step.focus_text, helpContext) : ""}</h3>
      ${step.focus_text ? `<p>${escapeHtml(step.focus_text)}</p>` : ""}
      ${step.subject || step.main_verb ? `
        <div class="drill-result-grid">
          <div class="metric">
            <span class="muted">Subject</span>
            <strong class="metric-word">${escapeHtml(step.subject || "-")}</strong>
          </div>
          <div class="metric">
            <span class="muted">Main Verb</span>
            <strong class="metric-word">${escapeHtml(step.main_verb || "-")}</strong>
          </div>
        </div>
      ` : ""}
      ${step.key_vocabulary?.length ? guidedVocabularyList(step.key_vocabulary) : ""}
      ${step.paragraph_map?.length ? guidedParagraphMap(step.paragraph_map, lesson) : ""}
      ${step.main_idea ? `<p><strong>Main idea:</strong> ${escapeHtml(step.main_idea)}</p>` : ""}
      <p>${escapeHtml(step.simple_explanation || "")}</p>
      <p class="muted">${escapeHtml(step.learner_action || "")}</p>
    </div>
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
    <section class="panel">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Reading Sub-skill Progress</p>
          <h3>Progress kemampuan Reading</h3>
        </div>
      </div>
      <div class="drill-result-grid">
        ${subskills.map((item) => `
          <div class="metric">
            <span class="muted">${escapeHtml(item.label || readingSubskillLabel(item.subskill))}</span>
            <strong>${Math.round(item.mastery_score || 0)}%</strong>
            <small>${readingMasteryStatusLabel(item.status)} · ${item.attempt_count || 0} latihan</small>
          </div>
        `).join("")}
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
    <section class="panel" id="readingTrainerPanel">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Reading Trainer</p>
          <h3>Latihan berdasarkan sub-skill</h3>
          <p>${escapeHtml(trainer.guidance?.tip || "Pilih tipe latihan, jawab soal, lalu lihat feedback.")}</p>
        </div>
      </div>
      <div class="pill-row">
        ${buttons.map(([value, label]) => `
          <button class="ghost-button ${subSkill === value ? "selected-control" : ""}" type="button" data-reading-trainer-subskill="${value}">
            ${label}
          </button>
        `).join("")}
      </div>
      <div class="content-grid compact-grid">
        <div>
          <h3>${escapeHtml(passage.title || "Trainer Passage")}</h3>
          <p>${escapeHtml(passage.text || "")} ${renderContextualHelpButton("reading", "reading_paragraph", passage.text || "", baseContext)}</p>
          <p class="muted">${escapeHtml(trainer.guidance?.goal || "")}</p>
        </div>
        <div class="question">
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
          ${feedback ? readingTrainerFeedbackTemplate(feedback) : `<p class="muted">Pilih jawaban untuk menyimpan latihan ${escapeHtml(readingSubskillLabel(subSkill))}.</p>`}
        </div>
      </div>
    </section>
  `;
}

function readingTrainerFeedbackTemplate(feedback) {
  const type = feedback.is_correct ? "success" : "warning";
  const title = feedback.is_correct ? "Jawaban benar" : "Perlu review";
  const message = feedback.message || feedback.explanation || "Feedback tersimpan.";
  return resultTemplate(
    type,
    title,
    `${message}${feedback.evidence_sentence ? ` Evidence: ${feedback.evidence_sentence}` : ""}`
  );
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
    <div class="question">
      <h3>${index + 1}. ${question.text} ${renderContextualHelpButton("reading", "reading_question", question.text, baseContext)}</h3>
      <div class="question-options">
        ${question.options
          .map(
            (option, optionIndex) => `
              <div class="option-help-row">
                <button class="option-button ${selected === optionIndex ? "selected" : ""}" data-reading-question="${question.id}" data-option="${optionIndex}">
                  ${String.fromCharCode(65 + optionIndex)}. ${option}
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
      <p class="muted">${question.explanation}</p>
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
    <section class="panel">
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
    <div class="question">
      <p class="eyebrow">Review Soal ${index + 1} · ${escapeHtml(readingSubskillLabel(review.related_reading_sub_skill))}</p>
      <h3>${escapeHtml(review.question_text || question.text || "")} ${renderContextualHelpButton("reading", "reading_question", review.question_text || question.text || "", baseContext)}</h3>
      <div class="drill-result-grid">
        <div class="metric">
          <span class="muted">Jawaban Anda</span>
          <strong class="metric-word">${escapeHtml(review.selected_answer?.label || "-")}. ${escapeHtml(review.selected_answer?.text || "-")}</strong>
        </div>
        <div class="metric">
          <span class="muted">Jawaban Benar</span>
          <strong class="metric-word">${escapeHtml(review.correct_answer?.label || "-")}. ${escapeHtml(review.correct_answer?.text || "-")}</strong>
        </div>
      </div>
      <p><strong>Bukti dari Passage:</strong> ${escapeHtml(review.evidence_sentence || "-")} ${renderContextualHelpButton("reading", "reading_paragraph", review.evidence_sentence || lesson.passage, baseContext)}</p>
      <p><strong>Penjelasan langsung:</strong> ${escapeHtml(review.direct_explanation || "")}</p>
      <p><strong>Kenapa benar:</strong> ${escapeHtml(review.why_correct_answer_is_correct || "")}</p>
      ${review.why_selected_answer_is_wrong ? `<p><strong>Kenapa salah:</strong> ${escapeHtml(review.why_selected_answer_is_wrong)}</p>` : ""}
      <div class="lesson-list compact-list">
        ${Object.entries(analysis).map(([letter, item]) => `
          <div>
            <h3>Opsi ${letter} ${renderContextualHelpButton("reading", "reading_option", optionTextFromReview(question, letter, item), {
              ...baseContext,
              option_label: letter,
              option_text: optionTextFromReview(question, letter, item)
            })}</h3>
            <p><strong>Arti:</strong> ${escapeHtml(item.meaning || "")}</p>
            <p><strong>Hubungan dengan passage:</strong> ${escapeHtml(item.relation_to_passage || "")}</p>
            <p><strong>Status:</strong> ${escapeHtml(item.correct_or_wrong === "correct" ? "benar" : "salah")} · ${escapeHtml(item.reason || "")}</p>
          </div>
        `).join("")}
      </div>
      <p class="muted">${escapeHtml(review.next_practice_recommendation || "")}</p>
    </div>
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
  const grammarSample = "A business analyst operating within a complex enterprise environment must not only elicit requirements but also ensure alignment between stakeholder needs and organizational strategy.";
  document.getElementById("grammarView").innerHTML = `
    <header class="topbar">
      <div>
        <p class="eyebrow">Grammar Breakdown Engine</p>
        <h2>Bedah struktur kalimat profesional.</h2>
        <p>Masukkan kalimat BA untuk melihat subject, main verb, clause, phrase, pattern, dan terjemahan natural.</p>
      </div>
      <button id="grammarHelpButton" class="ghost-button">Bantu pahami grammar</button>
    </header>
    ${journeyPanel("Grammar")}
    <section class="content-grid">
      <form id="grammarForm" class="panel form-grid">
        ${beginnerTip("Cara membaca grammar", "Cari subject dulu, lalu verb utama. Abaikan sementara phrase panjang yang hanya menambahkan informasi.")}
        <label>
          Kalimat
          <textarea id="grammarInput">${grammarSample}</textarea>
        </label>
        ${renderContextualHelpButton("grammar", "grammar_sentence", grammarSample)}
        <button class="primary-button" type="submit">Analyze Grammar</button>
      </form>
      <div id="grammarResult" class="panel">
        <p class="muted">Hasil breakdown akan muncul di sini.</p>
      </div>
    </section>
  `;

  document.getElementById("grammarHelpButton").addEventListener("click", () => {
    openHelpWith(document.getElementById("grammarInput").value);
  });

  document.getElementById("grammarForm").addEventListener("submit", async (event) => {
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
    renderDashboard();
    renderJourney();
  });
  bindContextualHelpButtons(document.getElementById("grammarView"));
}

function grammarAnalysis(sentence) {
  const hasOperating = sentence.toLowerCase().includes("operating");
  const hasMust = sentence.toLowerCase().includes("must");
  return `
    <h3>Structure</h3>
    <p><strong>Subject:</strong> A business analyst</p>
    <p><strong>Main verb:</strong> ${hasMust ? "must elicit / must ensure" : "identify the finite verb after the subject"}</p>
    <p><strong>Phrase:</strong> ${hasOperating ? "operating within a complex enterprise environment" : "look for modifier phrases around the noun"}</p>
    <p><strong>Pattern:</strong> not only ... but also ...</p>
    <h3>Penjelasan sederhana</h3>
    <p>Bagian dengan -ing sering bukan verb utama. Dalam contoh ini, <strong>operating</strong> menjelaskan business analyst. Verb utama muncul bersama modal <strong>must</strong>.</p>
    <h3>Terjemahan natural</h3>
    <p>Seorang business analyst yang bekerja dalam lingkungan enterprise kompleks harus menggali requirement dan memastikan keselarasan antara kebutuhan stakeholder dan strategi organisasi.</p>
    <h3>Latihan serupa</h3>
    <p>The analyst working with multiple stakeholders must clarify priorities and document agreed requirements. ${renderContextualHelpButton("grammar", "grammar_sentence", "The analyst working with multiple stakeholders must clarify priorities and document agreed requirements.")}</p>
  `;
}

function grammarApiTemplate(analysis) {
  return `
    <h3>Structure</h3>
    <p><strong>Subject:</strong> ${analysis.subject}</p>
    <p><strong>Main verb:</strong> ${analysis.mainVerb}</p>
    <p><strong>Phrase:</strong> ${analysis.phrase}</p>
    <p><strong>Pattern:</strong> ${analysis.pattern}</p>
    <h3>Penjelasan sederhana</h3>
    <p>${analysis.explanation} ${renderContextualHelpButton("grammar", "grammar_explanation", analysis.explanation)}</p>
    <h3>Terjemahan natural</h3>
    <p>${analysis.translation}</p>
  `;
}

function renderVocabulary() {
  const vocabularyItems = getVocabulary();
  ensureDailyVocabularyDrill(vocabularyItems);
  const dailyItems = getDailyVocabularyItems(vocabularyItems);
  const drillStats = getVocabularyDrillStats(dailyItems);
  document.getElementById("vocabularyView").innerHTML = `
    <header class="topbar">
      <div>
        <p class="eyebrow">Vocabulary Drill</p>
        <h2>Target hari ini: 25 kata vocabulary.</h2>
        <p>Setiap hari aplikasi memilih kata random. Jawab arti Indonesia yang paling tepat, lalu lihat hasil drill sampai mana.</p>
      </div>
      <button id="vocabHelpButton" class="ghost-button">Cara hafal kata</button>
    </header>
    ${journeyPanel("Vocabulary")}

    <section class="reminder-card ${drillStats.completed ? "done" : ""}">
      <div>
        <strong>${drillStats.completed ? "Target harian selesai" : "Pengingat belajar hari ini"}</strong>
        <p>${drillStats.completed ? "Bagus. Kamu sudah menyelesaikan 25 kata hari ini. Ulangi kata yang salah agar makin nempel." : `Masih ada ${drillStats.remaining} kata lagi. Target kecil: jawab 25 kata, tidak harus sempurna.`}</p>
      </div>
      <button id="resetDailyDrill" class="ghost-button">Acak ulang drill</button>
    </section>

    ${beginnerTip("Cara menghafal vocabulary", "Baca word, lihat contoh kalimat, pilih arti Indonesia. Kalau salah, catat kata itu untuk diulang besok.")}

    <section class="drill-result-grid">
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

    <section class="panel">
      <h3>Drill 25 Kata Hari Ini</h3>
      <div class="drill-list">
        ${dailyItems.map((item, index) => vocabularyDrillTemplate(item, index, vocabularyItems)).join("")}
      </div>
    </section>

    <section class="panel">
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
    <article class="lesson-card drill-card ${answered ? (answered.isCorrect ? "correct" : "wrong") : ""}">
      <div class="pill-row">
        <span class="pill">#${index + 1}</span>
        <span class="pill">${item.part}</span>
        <span class="pill">BA Context</span>
      </div>
      <h3>${item.word}</h3>
      <p>${item.example}</p>
      <p class="muted">${item.meaningEn}</p>
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
    <header class="topbar">
      <div>
        <p class="eyebrow">AI Tutor Internal</p>
        <h2>Mentor TOEFL untuk calon Business Analyst.</h2>
        <p>Tulis pertanyaan dalam Bahasa Indonesia. Contoh: "Apa arti elicit?" atau "Kenapa operating bukan verb utama?"</p>
      </div>
    </header>
    <section class="content-grid">
      <div class="panel">
        <div id="chatLog" class="chat-log">
          ${state.chat.map((message) => `
            <div class="chat-message ${message.role}">
              <p>${escapeHtml(message.text)}</p>
              ${renderContextualHelpButton("tutor", message.role === "assistant" ? "tutor_message" : "user_sentence", message.text)}
            </div>
          `).join("")}
        </div>
      </div>
      <form id="chatForm" class="panel form-grid">
        ${beginnerTip("Tips bertanya", "Kalau bingung, tulis saja kalimat Inggrisnya lalu tanya: artinya apa, subject-nya apa, verb-nya apa.")}
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
    <header class="topbar">
      <div>
        <p class="eyebrow">Writing Evaluator</p>
        <h2>Latihan writing profesional.</h2>
        <p>Tulis requirement statement atau ringkasan meeting, lalu dapatkan feedback awal.</p>
      </div>
      <button id="writingHelpButton" class="ghost-button">Bantu susun kalimat</button>
    </header>
    ${journeyPanel("Writing")}
    <section class="content-grid">
      <form id="writingForm" class="panel form-grid">
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
      <div id="writingResult" class="panel"><p class="muted">Feedback akan muncul di sini.</p></div>
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
    document.getElementById("writingResult").innerHTML = `
      <h3>Score: ${feedback.score}</h3>
      <p><strong>Main issue:</strong> ${feedback.issues.join(" ")}</p>
      <p><strong>Revised:</strong> ${feedback.revised} ${renderContextualHelpButton("writing", "writing_feedback", feedback.revised)}</p>
      <p><strong>Next practice:</strong> ${feedback.recommendation}</p>
    `;
    bindContextualHelpButtons(document.getElementById("writingResult"));
    renderDashboard();
    renderJourney();
  });
  bindContextualHelpButtons(document.getElementById("writingView"));
}

function renderListening() {
  document.getElementById("listeningView").innerHTML = `
    <header class="topbar">
      <div>
        <p class="eyebrow">AI Listening Engine</p>
        <h2>${listeningScenario.title}</h2>
        <p>Baca transcript pelan-pelan. Tujuan awalnya bukan menangkap semua kata, tapi menemukan masalah utama dalam meeting.</p>
      </div>
      <button id="listeningHelpButton" class="ghost-button">Jelaskan transcript</button>
    </header>
    ${journeyPanel("Listening")}
    <section class="content-grid">
      <div class="panel">
        ${beginnerTip("Cara memahami listening", "Cari kata yang diulang atau ditekankan: late, delay, data, different formats. Biasanya itu petunjuk masalah utama.")}
        <h3>Transcript</h3>
        <p>${listeningScenario.transcript} ${renderContextualHelpButton("listening", "listening_transcript", listeningScenario.transcript, listeningHelpContext())}</p>
      </div>
      <form id="listeningForm" class="panel form-grid">
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
    <header class="topbar">
      <div>
        <p class="eyebrow">Scenario-Based BA Practice</p>
        <h2>Latih keputusan Business Analyst dalam bahasa Inggris.</h2>
        <p>Pilih tindakan terbaik untuk situasi kerja BA. Modul ini menggabungkan reasoning BA, reading comprehension, dan vocabulary profesional.</p>
      </div>
      <button id="scenarioHelpButton" class="ghost-button">Bantu pahami skenario</button>
    </header>
    ${beginnerTip("Cara menjawab scenario", "Sebagai BA, jangan langsung membuat solusi. Biasanya langkah pertama adalah clarify, elicit, validate, atau align.")}
    <section class="lesson-list">
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
    <article class="lesson-card">
      <div class="pill-row">
        <span class="pill">BA Decision</span>
        <span class="pill">Scenario</span>
      </div>
      <h3>${item.title}</h3>
      <p>${item.context} ${renderContextualHelpButton("scenario", "scenario_case", item.context, scenarioHelpContext(item))}</p>
      <p><strong>${item.question}</strong> ${renderContextualHelpButton("scenario", "scenario_question", item.question, scenarioHelpContext(item))}</p>
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
    <header class="topbar">
      <div>
        <p class="eyebrow">Admin CMS</p>
        <h2>Kelola konten latihan awal.</h2>
        <p>CMS lokal ini menyimpan konten tambahan di browser. Pada tahap backend, struktur ini bisa dipindahkan ke PostgreSQL dan endpoint lesson/vocabulary.</p>
      </div>
    </header>
    <section class="content-grid">
      <form id="lessonForm" class="panel form-grid">
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
      <form id="vocabForm" class="panel form-grid">
        <h3>Tambah Vocabulary</h3>
        <label>Word<input id="vocabWord" required value="assess" /></label>
        <label>Part of speech<input id="vocabPart" required value="verb" /></label>
        <label>Meaning Indonesia<input id="vocabMeaningId" required value="menilai" /></label>
        <label>Meaning English<input id="vocabMeaningEn" required value="to evaluate or judge something" /></label>
        <label>Example<textarea id="vocabExample" required>The analyst assesses the impact of the proposed change.</textarea></label>
        <button class="primary-button" type="submit">Simpan Vocabulary</button>
      </form>
    </section>
    <section class="panel">
      <h3>Konten Tambahan</h3>
      <div class="content-grid">
        <div>
          <p class="muted">Lessons: ${state.adminContent.lessons.length}</p>
          <div class="lesson-list compact-list">
            ${
              state.adminContent.lessons
                .map((lesson) => `<div class="activity-row"><strong>${lesson.title}</strong><span>${lesson.context}</span><small>${lesson.level}</small></div>`)
                .join("") || "<p class='muted'>Belum ada lesson tambahan.</p>"
            }
          </div>
        </div>
        <div>
          <p class="muted">Vocabulary: ${state.adminContent.vocabulary.length}</p>
          <div class="lesson-list compact-list">
            ${
              state.adminContent.vocabulary
                .map((item) => `<div class="activity-row"><strong>${item.word}</strong><span>${item.meaningId}</span><small>${item.part}</small></div>`)
                .join("") || "<p class='muted'>Belum ada vocabulary tambahan.</p>"
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
