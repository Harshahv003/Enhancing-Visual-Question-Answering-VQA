/**
 * script.js
 * ----------
 * Handles all frontend interactivity for the VQA system:
 *  - Drag-and-drop / click image upload with preview
 *  - Character counter for the question input
 *  - Form submission via Fetch API (no page reload)
 *  - Loading animation with rotating messages
 *  - Answer display with copy-to-clipboard
 *  - Error display and reset
 *  - Step indicator updates
 */

/* ── DOM references ──────────────────────────────────────────────────────── */
const uploadZone     = document.getElementById("uploadZone");
const imageInput     = document.getElementById("imageInput");
const previewWrap    = document.getElementById("previewWrap");
const imagePreview   = document.getElementById("imagePreview");
const removeBtn      = document.getElementById("removeBtn");

const questionInput  = document.getElementById("questionInput");
const charCount      = document.getElementById("charCount");
const languageSelect = document.getElementById("languageSelect");

const submitBtn      = document.getElementById("submitBtn");
const loadingWrap    = document.getElementById("loadingWrap");
const loadingText    = document.getElementById("loadingText");

const answerWrap     = document.getElementById("answerWrap");
const answerText     = document.getElementById("answerText");
const answerLang     = document.getElementById("answerLang");
const englishNote    = document.getElementById("englishNote");
const englishText    = document.getElementById("englishText");
const copyBtn        = document.getElementById("copyBtn");
const resetBtn       = document.getElementById("resetBtn");

const errorWrap      = document.getElementById("errorWrap");
const errorText      = document.getElementById("errorText");
const errorResetBtn  = document.getElementById("errorResetBtn");

const steps = {
  1: document.getElementById("step-1"),
  2: document.getElementById("step-2"),
  3: document.getElementById("step-3"),
};

/* ── Loading messages ────────────────────────────────────────────────────── */
const LOADING_MESSAGES = [
  "Analysing image…",
  "Processing your question…",
  "Generating answer with Gemini…",
  "Applying translation…",
  "Almost there…",
];

let loadingInterval = null;

function startLoadingMessages() {
  let i = 0;
  loadingText.textContent = LOADING_MESSAGES[0];
  loadingInterval = setInterval(() => {
    i = (i + 1) % LOADING_MESSAGES.length;
    loadingText.textContent = LOADING_MESSAGES[i];
  }, 1800);
}

function stopLoadingMessages() {
  if (loadingInterval) {
    clearInterval(loadingInterval);
    loadingInterval = null;
  }
}

/* ── Step indicator ──────────────────────────────────────────────────────── */
function setStep(activeStep) {
  Object.entries(steps).forEach(([num, el]) => {
    const n = parseInt(num);
    el.classList.remove("active", "done");
    if (n < activeStep)  el.classList.add("done");
    if (n === activeStep) el.classList.add("active");
  });
}

/* ── Image upload & preview ──────────────────────────────────────────────── */
imageInput.addEventListener("change", function () {
  if (this.files && this.files[0]) {
    showPreview(this.files[0]);
  }
});

// Drag-and-drop support
uploadZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  uploadZone.classList.add("drag-over");
});
uploadZone.addEventListener("dragleave", () => {
  uploadZone.classList.remove("drag-over");
});
uploadZone.addEventListener("drop", (e) => {
  e.preventDefault();
  uploadZone.classList.remove("drag-over");
  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith("image/")) {
    // Assign to the input so FormData picks it up
    const dt = new DataTransfer();
    dt.items.add(file);
    imageInput.files = dt.files;
    showPreview(file);
  } else {
    showError("Please drop an image file (PNG, JPG, WEBP, GIF, or BMP).");
  }
});

function showPreview(file) {
  const reader = new FileReader();
  reader.onload = (e) => {
    imagePreview.src = e.target.result;
    imagePreview.alt = `Preview: ${file.name}`;
    uploadZone.classList.add("hidden");
    previewWrap.classList.remove("hidden");
    setStep(2);
  };
  reader.readAsDataURL(file);
}

removeBtn.addEventListener("click", () => {
  imageInput.value = "";
  imagePreview.src = "";
  uploadZone.classList.remove("hidden");
  previewWrap.classList.add("hidden");
  setStep(1);
  resetOutput();
});

/* ── Character counter ───────────────────────────────────────────────────── */
questionInput.addEventListener("input", function () {
  const len = this.value.length;
  charCount.textContent = len;
  charCount.style.color = len >= 450 ? "#ff8888" : "var(--text-faint)";
  if (len > 0 && imageInput.files.length > 0) setStep(2);
});

/* ── Form submission ─────────────────────────────────────────────────────── */
submitBtn.addEventListener("click", handleSubmit);

// Allow pressing Enter in the question box to submit
questionInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleSubmit();
  }
});

async function handleSubmit() {
  // ── Client-side validation ──────────────────────────────────────────────
  if (!imageInput.files || imageInput.files.length === 0) {
    showError("Please upload an image first.");
    return;
  }
  const question = questionInput.value.trim();
  if (!question) {
    showError("Please type a question about the image.");
    questionInput.focus();
    return;
  }
  if (question.length < 3) {
    showError("Your question is too short. Please ask a complete question.");
    return;
  }

  // ── Build FormData ──────────────────────────────────────────────────────
  const formData = new FormData();
  formData.append("image",    imageInput.files[0]);
  formData.append("question", question);
  formData.append("language", languageSelect.value);

  // ── UI: loading state ───────────────────────────────────────────────────
  setStep(3);
  submitBtn.disabled = true;
  submitBtn.querySelector(".btn-text").textContent = "Processing…";
  resetOutput();
  loadingWrap.classList.remove("hidden");
  startLoadingMessages();

  try {
    // ── API call ──────────────────────────────────────────────────────────
    const response = await fetch("/ask", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      // Server returned 4xx / 5xx
      throw new Error(data.error || `Server error (${response.status})`);
    }

    // ── Show answer ───────────────────────────────────────────────────────
    showAnswer(data);

  } catch (err) {
    // Network failure or server error
    showError(err.message || "Connection failed. Please check your internet and try again.");
  } finally {
    // ── Restore UI ────────────────────────────────────────────────────────
    stopLoadingMessages();
    loadingWrap.classList.add("hidden");
    submitBtn.disabled = false;
    submitBtn.querySelector(".btn-text").textContent = "Get Answer";
  }
}

/* ── Display helpers ─────────────────────────────────────────────────────── */
function showAnswer(data) {
  const { answer, language, english_answer } = data;

  answerText.textContent = answer;
  answerLang.textContent = language || "English";

  // Show English original if translated to another language
  const isTranslated = (language || "").toLowerCase() !== "english";
  if (isTranslated && english_answer && english_answer !== answer) {
    englishText.textContent = english_answer;
    englishNote.classList.remove("hidden");
  } else {
    englishNote.classList.add("hidden");
  }

  answerWrap.classList.remove("hidden");
  answerWrap.scrollIntoView({ behavior: "smooth", block: "nearest" });

  copyBtn.textContent  = "⎘ Copy";
  copyBtn.classList.remove("copied");
}

function showError(message) {
  errorText.textContent = message;
  errorWrap.classList.remove("hidden");
  errorWrap.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function resetOutput() {
  answerWrap.classList.add("hidden");
  errorWrap.classList.add("hidden");
  answerText.textContent = "";
  errorText.textContent  = "";
}

/* ── Copy to clipboard ───────────────────────────────────────────────────── */
copyBtn.addEventListener("click", async () => {
  const text = answerText.textContent;
  try {
    await navigator.clipboard.writeText(text);
    copyBtn.textContent = "✓ Copied!";
    copyBtn.classList.add("copied");
    setTimeout(() => {
      copyBtn.textContent = "⎘ Copy";
      copyBtn.classList.remove("copied");
    }, 2500);
  } catch {
    // Fallback for older browsers
    const ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
    copyBtn.textContent = "✓ Copied!";
  }
});

/* ── Reset / Try again ───────────────────────────────────────────────────── */
function fullReset() {
  resetOutput();
  setStep(imageInput.files.length > 0 ? 2 : 1);
  questionInput.focus();
}
resetBtn.addEventListener("click", fullReset);
errorResetBtn.addEventListener("click", fullReset);

/* ── Init ────────────────────────────────────────────────────────────────── */
setStep(1);
