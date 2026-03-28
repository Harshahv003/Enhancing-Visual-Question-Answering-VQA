"""
utils/translator.py
--------------------
Translates the English VQA answer into regional languages
using the deep-translator library (Google Translate backend).

Supported languages:
    - English (en)  — returned as-is
    - Hindi   (hi)
    - Telugu  (te)
    - Urdu    (ur)
    - Kannada (kn)
"""

from deep_translator import GoogleTranslator


# Language code map — key is what the frontend sends, value is Google Translate code
SUPPORTED_LANGUAGES: dict[str, str] = {
    "english":  "en",
    "hindi":    "hi",
    "telugu":   "te",
    "urdu":     "ur",
    "kannada":  "kn",
}


def translate_answer(english_text: str, target_language: str) -> str:
    """
    Translate an English answer string into the target language.

    Parameters
    ----------
    english_text    : str   The English answer from Gemini.
    target_language : str   One of the SUPPORTED_LANGUAGES keys
                            e.g. "hindi", "telugu", "urdu", "kannada", "english"

    Returns
    -------
    str   Translated text (or the original if target is English / unsupported).

    Notes
    -----
    - Falls back to the original English text on translation failure
      so the user always gets *some* answer.
    - deep-translator splits long texts automatically; no length limit concern.
    """
    # Normalise to lowercase for lookup
    lang_key = target_language.strip().lower()

    # If English or not in our list, return as-is
    lang_code = SUPPORTED_LANGUAGES.get(lang_key)
    if not lang_code or lang_code == "en":
        return english_text

    try:
        translator = GoogleTranslator(source="en", target=lang_code)
        translated = translator.translate(english_text)
        return translated if translated else english_text

    except Exception as e:
        # Never crash the whole request because of a translation error
        print(f"[translator] Warning: Translation to '{target_language}' failed — {e}")
        return english_text   # Return English as a safe fallback


def get_supported_languages() -> list[str]:
    """
    Return a list of supported language display names (title-cased).
    Used by the frontend to populate the language dropdown.
    """
    return [lang.title() for lang in SUPPORTED_LANGUAGES.keys()]
