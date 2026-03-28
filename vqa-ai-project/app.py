"""
app.py
-------
Main Flask application for the AI Visual Question Answering (VQA) System.
Bridges computer vision and NLP through Google Gemini Vision API.

Run with:
    python app.py
Then open:  http://127.0.0.1:5000
"""

import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# ── Utils ────────────────────────────────────────────────────────────────────
from utils.image_processing import preprocess_image, allowed_file
from utils.question_processing import process_question
from utils.translator import translate_answer, get_supported_languages

# ── Model ────────────────────────────────────────────────────────────────────
from models.vqa_model import get_answer

# ── Load environment variables ───────────────────────────────────────────────
load_dotenv()   # reads GEMINI_API_KEY (and others) from .env

# ── App setup ────────────────────────────────────────────────────────────────
app = Flask(__name__)

# Maximum allowed upload size: 16 MB
app.config["MAX_CONTENT_LENGTH"] = int(
    os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024)
)

# Temporary upload folder (Flask never stores anything permanently here)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Render the main VQA interface, passing the supported languages list."""
    languages = get_supported_languages()
    return render_template("index.html", languages=languages)


@app.route("/ask", methods=["POST"])
def ask():
    """
    POST /ask
    ---------
    Expects multipart/form-data with:
        image    : image file (PNG / JPG / JPEG / WEBP / GIF / BMP)
        question : natural language question string
        language : output language name e.g. "telugu" (default: "english")

    Returns JSON:
        { "answer": "...", "language": "...", "english_answer": "..." }
    or on error:
        { "error": "human-readable message" }, HTTP 4xx/5xx
    """

    # ── 1. Validate image ────────────────────────────────────────────────────
    if "image" not in request.files:
        return jsonify({"error": "No image was uploaded. Please select an image file."}), 400

    image_file = request.files["image"]

    if image_file.filename == "":
        return jsonify({"error": "No image file selected. Please choose an image."}), 400

    if not allowed_file(image_file.filename):
        return jsonify({
            "error": "Unsupported file type. Please upload a PNG, JPG, JPEG, WEBP, GIF, or BMP image."
        }), 400

    # ── 2. Validate question ─────────────────────────────────────────────────
    raw_question = request.form.get("question", "")
    try:
        question = process_question(raw_question)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # ── 3. Get target language ───────────────────────────────────────────────
    language = request.form.get("language", "english").strip().lower()

    # ── 4. Pre-process the image ─────────────────────────────────────────────
    try:
        image_bytes = image_file.read()
        pil_image = preprocess_image(image_bytes)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # ── 5. Get answer from VQA model ─────────────────────────────────────────
    try:
        english_answer = get_answer(pil_image, question)
    except EnvironmentError as e:
        return jsonify({"error": f"Configuration error: {str(e)}"}), 500
    except RuntimeError as e:
        return jsonify({"error": f"AI model error: {str(e)}"}), 502

    # ── 6. Translate if needed ───────────────────────────────────────────────
    final_answer = translate_answer(english_answer, language)

    # ── 7. Return result ─────────────────────────────────────────────────────
    return jsonify({
        "answer":         final_answer,
        "language":       language.title(),
        "english_answer": english_answer,   # always include for debugging
    })


# ── Error handlers ───────────────────────────────────────────────────────────

@app.errorhandler(413)
def file_too_large(e):
    """Handle uploads exceeding MAX_CONTENT_LENGTH."""
    return jsonify({
        "error": "Image file is too large. Please upload an image under 16 MB."
    }), 413


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found."}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "An unexpected server error occurred. Please try again."}), 500


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
