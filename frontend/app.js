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
    cache: {}
  },
  remoteContent: {
    lessons: null,
    vocabulary: null
  },
  integratedJourney: null,
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
    contextualHelp: { cache: { ...(parsed.contextualHelp?.cache || {}) } },
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
        contextualHelp: { cache: { ...(stateResponse.state.contextualHelp?.cache || state.contextualHelp?.cache || {}) } }
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
  } catch (error) {
    apiOnline = false;
    state.integratedJourney = localJourneySummary();
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

function renderContextualHelpButton(module, contextType, text) {
  const key = contextualHelpKey(module, contextType, text);
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
      >Bantuan ID</button>
      <div class="context-help-panel hidden" data-context-help-panel="${escapeAttribute(key)}"></div>
    </span>
  `;
}

function contextualHelpKey(module, contextType, text) {
  return `${module}:${contextType}:${hashText(String(text || ""))}`;
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
      const key = button.dataset.helpKey || contextualHelpKey(module, contextType, text);
      const panel = document.querySelector(`[data-context-help-panel="${cssEscape(key)}"]`);
      if (!panel) return;

      if (panel.dataset.open === "true") {
        panel.dataset.open = "false";
        panel.classList.add("hidden");
        return;
      }

      panel.dataset.open = "true";
      panel.classList.remove("hidden");
      const cached = state.contextualHelp?.cache?.[key];
      if (cached) {
        panel.innerHTML = renderContextualHelpResult(cached);
        return;
      }

      panel.innerHTML = `<p class="muted">Sedang menjelaskan...</p>`;
      try {
        const result = await explainTextWithBantuanID(text, module, contextType);
        state.contextualHelp.cache[key] = result;
        saveState();
        panel.innerHTML = renderContextualHelpResult(result);
        logContextualHelpUsage(module, contextType, text);
      } catch (error) {
        panel.innerHTML = `<p class="muted">Maaf, Bantuan ID belum dapat memproses teks ini. Coba lagi nanti.</p>`;
      }
    });
  });
}

async function explainTextWithBantuanID(text, module, contextType) {
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
            user_id: state.user?.id || "default-user"
          }
        }
      });
    } catch (error) {
      apiOnline = false;
    }
  }
  return localContextualHelp(text, module, contextType);
}

function localContextualHelp(text, module, contextType) {
  const legacy = indonesianHelp(text, module === "grammar" ? "grammar" : "simple");
  return {
    text,
    module,
    context_type: contextType,
    explanation_id: contextualHelpKey(module, contextType, text),
    source: "local",
    explanation: {
      simple_meaning_id: legacy.simpleMeaning,
      sentence_structure: legacy.structure,
      subject: text.toLowerCase().includes("business analyst") ? "A business analyst" : "Cari noun sebelum verb utama.",
      verb: text.toLowerCase().includes("must") ? "must + verb utama" : "Cari aksi utama dalam kalimat.",
      object_or_complement: "Bagian setelah verb biasanya menjadi object atau informasi tambahan.",
      grammar_pattern: legacy.structure,
      important_vocabulary: legacy.keywords.map((item) => {
        const [word, meaning] = item.split(" = ");
        return { word, meaning_id: meaning || item };
      }),
      beginner_explanation: legacy.explanation,
      tips: "Baca pelan, cari subject dan verb, lalu baru pahami detail tambahan."
    }
  };
}

function renderContextualHelpResult(result) {
  const explanation = result.explanation || {};
  const vocabulary = explanation.important_vocabulary || [];
  const vocabularyHtml = vocabulary.length
    ? `<ul>${vocabulary.map((item) => `<li><strong>${escapeHtml(item.word || "")}</strong>: ${escapeHtml(item.meaning_id || "")}</li>`).join("")}</ul>`
    : `<p class="muted">Belum ada kosakata khusus yang terdeteksi.</p>`;
  const extras = [
    ["Arti kata", explanation.word_meaning_id],
    ["Jenis kata", explanation.word_class],
    ["Cara mengingat", explanation.memory_tip],
    ["Contoh kalimat", explanation.example_sentence],
    ["Makna BA / TOEFL", explanation.ba_toefl_context],
    ["Maksud kalimat", explanation.writing_meaning],
    ["Masalah grammar", explanation.grammar_issue],
    ["Versi lebih baik", explanation.better_sentence],
    ["Alasan perbaikan", explanation.improvement_reason],
    ["Kata kunci listening", Array.isArray(explanation.listening_keywords) ? explanation.listening_keywords.join(", ") : explanation.listening_keywords],
    ["Maksud pembicara", explanation.speaker_intent],
    ["Tips listening", explanation.listening_tip],
    ["Konteks Business Analyst", explanation.ba_context],
    ["Masalah bisnis", explanation.business_problem],
    ["Stakeholder terlibat", explanation.stakeholders],
    ["Petunjuk memilih jawaban", explanation.answer_hint]
  ]
    .filter(([, value]) => value)
    .map(([label, value]) => `<p><strong>${label}:</strong> ${escapeHtml(value)}</p>`)
    .join("");

  return `
    <div class="context-help-card">
      <strong>Bantuan ID</strong>
      <p><strong>Arti sederhana:</strong> ${escapeHtml(explanation.simple_meaning_id || "Teks ini perlu dipahami dari konteksnya.")}</p>
      <p><strong>Struktur kalimat:</strong> ${escapeHtml(explanation.sentence_structure || explanation.grammar_pattern || "Subject + Verb + Object/Complement")}</p>
      <p><strong>Subject:</strong> ${escapeHtml(explanation.subject || "Belum terdeteksi")}</p>
      <p><strong>Verb:</strong> ${escapeHtml(explanation.verb || "Belum terdeteksi")}</p>
      <p><strong>Object/Complement:</strong> ${escapeHtml(explanation.object_or_complement || "Lihat bagian setelah verb utama.")}</p>
      <div><strong>Kosakata penting:</strong>${vocabularyHtml}</div>
      <p><strong>Penjelasan konteks:</strong> ${escapeHtml(explanation.beginner_explanation || "Pahami maksud umum dulu sebelum detail grammar.")}</p>
      <p><strong>Tips memahami:</strong> ${escapeHtml(explanation.tips || "Cari kata kunci, lalu cocokkan dengan konteks modul.")}</p>
      ${extras}
      <small class="muted">Sumber: ${escapeHtml(result.source || "mock")}</small>
    </div>
  `;
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
        <p>${selectedLesson.passage} ${renderContextualHelpButton("reading", "reading_passage", selectedLesson.passage)}</p>
        <div class="pill-row">
          <span class="pill">${selectedLesson.level}</span>
          <span class="pill">${selectedLesson.context}</span>
        </div>
      </div>
      <button id="readingHelpButton" class="ghost-button">Jelaskan bacaan ini</button>
    </header>
    ${journeyPanel("Reading")}

    <section class="content-grid">
      <div class="panel">
        ${beginnerTip("Cara mengerjakan Reading", "Baca judul dan kalimat pertama. Cari ide utama, lalu cocokkan pilihan jawaban dengan kata kunci yang sama maknanya.")}
        <h3>TOEFL-style Questions</h3>
        ${selectedLesson.questions.map((question, index) => readingQuestionTemplate(question, index)).join("")}
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
    if (apiOnline) {
      try {
        const response = await apiRequest("/reading/submit-answer", {
          method: "POST",
          body: {
            user_id: state.user?.id || "default-user",
            lessonId: selectedLesson.id,
            answers: state.readingAnswers
          }
        });
        score = response.score;
        details = response.details || [];
      } catch (error) {
        apiOnline = false;
      }
    }
    state.progress.Reading = Math.max(state.progress.Reading, score);
    state.completedExercises += 1;
    addActivity("Reading", selectedLesson.title, score);
    saveState();
    await refreshIntegratedJourney();
    document.getElementById("readingResult").innerHTML = resultTemplate(
      score >= 70 ? "success" : "warning",
      `Skor Reading: ${score}`,
      score >= 70
        ? "Bagus. Kamu sudah menangkap main idea dan detail penting."
        : "Ulangi passage dan perhatikan kata kunci seperti analyst, stakeholder, dan outcome."
    ) + (details.length ? `<div class="lesson-list compact-list">${details.map((detail) => `<p class="muted">${detail.questionId}: ${detail.isCorrect ? "Correct" : "Review"} - ${detail.explanation}</p>`).join("")}</div>` : "");
    renderDashboard();
    renderJourney();
  });
  bindContextualHelpButtons(document.getElementById("readingView"));
}

function readingQuestionTemplate(question, index) {
  const selected = state.readingAnswers[question.id];
  return `
    <div class="question">
      <h3>${index + 1}. ${question.text} ${renderContextualHelpButton("reading", "reading_question", question.text)}</h3>
      <div class="question-options">
        ${question.options
          .map(
            (option, optionIndex) => `
              <div class="option-help-row">
                <button class="option-button ${selected === optionIndex ? "selected" : ""}" data-reading-question="${question.id}" data-option="${optionIndex}">
                  ${String.fromCharCode(65 + optionIndex)}. ${option}
                </button>
                ${renderContextualHelpButton("reading", "reading_option", option)}
              </div>
            `
          )
          .join("")}
      </div>
      <p class="muted">${question.explanation}</p>
    </div>
  `;
}

function scoreReading(lesson) {
  const correct = lesson.questions.filter((question) => state.readingAnswers[question.id] === question.answer).length;
  return Math.round((correct / lesson.questions.length) * 100);
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
      <h3>${item.word} ${renderContextualHelpButton("vocabulary", "vocabulary_word", item.word)}</h3>
      <p>${item.example} ${renderContextualHelpButton("vocabulary", "vocabulary_example", item.example)}</p>
      <p class="muted">${item.meaningEn}</p>
      <div class="question-options">
        ${options
          .map((option) => `
            <div class="option-help-row">
              <button class="option-button ${answered?.selected === option ? "selected" : ""}" data-vocab-drill="${item.id}" data-answer="${option}">${option}</button>
              ${renderContextualHelpButton("vocabulary", "vocabulary_option", option)}
            </div>
          `)
          .join("")}
      </div>
      ${answered === undefined ? "" : resultTemplate(answered.isCorrect ? "success" : "danger", answered.isCorrect ? "Benar" : "Belum tepat", answered.isCorrect ? "Makna sudah sesuai konteks." : `Jawaban benar: ${item.meaningId}`)}
    </article>
  `;
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
        <p>${listeningScenario.transcript} ${renderContextualHelpButton("listening", "listening_transcript", listeningScenario.transcript)}</p>
      </div>
      <form id="listeningForm" class="panel form-grid">
        <label>
          ${listeningScenario.question} ${renderContextualHelpButton("listening", "listening_question", listeningScenario.question)}
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
      <p>${item.context} ${renderContextualHelpButton("scenario", "scenario_case", item.context)}</p>
      <p><strong>${item.question}</strong> ${renderContextualHelpButton("scenario", "scenario_question", item.question)}</p>
      <div class="question-options">
        ${item.options
          .map(
            (option, index) => `
              <div class="option-help-row">
                <button class="option-button ${selected === index ? "selected" : ""}" data-scenario="${item.id}" data-option="${index}">
                  ${String.fromCharCode(65 + index)}. ${option}
                </button>
                ${renderContextualHelpButton("scenario", "scenario_option", option)}
              </div>
            `
          )
          .join("")}
      </div>
      ${answered ? resultTemplate(isCorrect ? "success" : "warning", isCorrect ? "Reasoning tepat" : "Reasoning perlu diperbaiki", item.explanation) : ""}
    </article>
  `;
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

function cssEscape(value) {
  if (window.CSS?.escape) return window.CSS.escape(value);
  return String(value).replace(/[^a-zA-Z0-9_-]/g, "\\$&");
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
