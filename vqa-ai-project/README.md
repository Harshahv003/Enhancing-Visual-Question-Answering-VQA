# 🤖 AI Visual Question Answering (VQA) System

> **Bridging Computer Vision and NLP** — Upload an image, ask a question in English, get an answer in Hindi, Telugu, Urdu, Kannada, or English.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey?logo=flask)
![Gemini](https://img.shields.io/badge/Gemini-Vision%20API-orange?logo=google)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 Demo

| Upload → Ask → Answer |
|---|
| Users upload any image, type a question, choose an output language, and receive an AI-generated answer in seconds. |

---

## ✨ Features

- **Multimodal AI** — Combines image understanding and natural language via Google Gemini Vision API
- **Multilingual Output** — Hindi · Telugu · Urdu · Kannada · English
- **Real-time Responses** — Answers generated in under 2.5 seconds
- **Drag-and-Drop Upload** — Intuitive image upload with preview
- **Copy to Clipboard** — One-click answer copying
- **Error Handling** — Friendly messages for invalid inputs, API errors, and oversized files
- **Modular Codebase** — Easy to extend with new models or languages

---

## 🗂️ Project Structure

```
vqa-ai-project/
├── app.py                      # Flask application (main entry point)
├── requirements.txt            # Python dependencies
├── .env                        # API key (NOT committed to git)
├── .gitignore
├── README.md
│
├── models/
│   └── vqa_model.py            # Gemini Vision API integration
│
├── utils/
│   ├── image_processing.py     # PIL image resize + validation
│   ├── question_processing.py  # Text cleaning + validation
│   └── translator.py           # deep-translator multilingual output
│
├── templates/
│   └── index.html              # Main UI (Jinja2 template)
│
├── static/
│   ├── style.css               # Modern dark-theme UI
│   └── script.js               # Drag-drop, fetch, loading, copy
│
├── uploads/                    # Temporary upload buffer (auto-created)
└── demo_screenshots/           # Add screenshots here for GitHub
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/vqa-ai-project.git
cd vqa-ai-project
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

1. Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Create a free API key
3. Open `.env` and replace the placeholder:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 5. Run the app

```bash
python app.py
```

Then open your browser at **http://127.0.0.1:5000**

---

## 🔌 API Reference

### `POST /ask`

| Field      | Type   | Required | Description                                       |
|------------|--------|----------|---------------------------------------------------|
| `image`    | File   | ✅       | Image file (PNG / JPG / WEBP / GIF / BMP, ≤ 16MB) |
| `question` | String | ✅       | Natural language question (3–500 chars)           |
| `language` | String | ❌       | Output language (default: `english`)              |

**Success Response:**
```json
{
  "answer": "The shirt is red.",
  "language": "Telugu",
  "english_answer": "The shirt is red."
}
```

**Error Response:**
```json
{
  "error": "No image was uploaded. Please select an image file."
}
```

---

## 🌐 Supported Languages

| Language | Code |
|----------|------|
| English  | en   |
| Hindi    | hi   |
| Telugu   | te   |
| Urdu     | ur   |
| Kannada  | kn   |

---

## 🧠 Technical Architecture

```
User → Upload Image + Question
         ↓
  Flask (app.py) receives request
         ↓
  image_processing.py  →  PIL resize (512×512) + validate
  question_processing.py → clean + validate text
         ↓
  models/vqa_model.py  →  Gemini 1.5 Flash (multimodal)
         ↓
  English answer generated
         ↓
  translator.py  →  deep-translator → target language
         ↓
  JSON response  →  script.js  →  UI display
```

**Complexity:**
- Image preprocessing: O(n) — n = pixels
- Question tokenisation: O(m) — m = tokens
- Gemini API call: O(n·m) — dominant term
- Output rendering: O(1)

---

## 🛠️ Technologies Used

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask 3.0 |
| AI/Vision | Google Gemini 1.5 Flash (Generative AI API) |
| Image Processing | Pillow (PIL) |
| Translation | deep-translator (Google Translate) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Environment | python-dotenv |

---

## 📋 Requirements

```
flask==3.0.3
google-generativeai==0.7.2
Pillow==10.4.0
python-dotenv==1.0.1
deep-translator==1.11.4
werkzeug==3.0.4
```

---

## 🔒 Security Notes

- `.env` is in `.gitignore` — **never commit your API key**
- Uploaded files are validated by extension and MIME type
- Maximum upload size: 16 MB (configurable in `.env`)
- All inputs are sanitised before processing

---

## 🚀 Future Improvements

- [ ] Voice input/output support (Web Speech API)
- [ ] Multi-turn conversation (chat history per session)
- [ ] Offline model fallback (BLIP-2 / LLaVA local inference)
- [ ] More language support (Tamil, Malayalam, Marathi…)
- [ ] Attention heatmap visualisation (explainability)
- [ ] Docker deployment support
- [ ] Cloud deployment guide (Render / Railway / GCP)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Authors

Final Year Project — Department of CSE (AI & ML)  
**Dhanekula Institute of Engineering & Technology**, Ganguru, Vijayawada

- Mr. R Madhukanth (Guide)
- Aseervad Abhishek Sripathi
- Soma Sekhara Rao Kadiyala
- Harsha Vardhan Attaluri
- Krishna Babu Kondaimanchilli
- Mohammad Shahid

---

## 📚 References

- Antol et al., "VQA: Visual Question Answering," ICCV 2015
- Anderson et al., "Bottom-Up and Top-Down Attention," CVPR 2018
- Radford et al., "CLIP," ICML 2021
- Kim et al., "ViLT," ICML 2021
- Li et al., "BLIP," arXiv 2022
- Google Cloud Generative AI on Vertex AI
