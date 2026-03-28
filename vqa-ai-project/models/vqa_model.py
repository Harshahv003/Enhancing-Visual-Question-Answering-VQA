"""
models/vqa_model.py
--------------------
Core VQA model using Google Gemini Vision API.
Accepts a PIL Image and a natural language question,
returns a descriptive natural language answer.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


def _configure_gemini():
    """
    Configure the Gemini API client using the key from .env.
    Raises a clear error if the key is missing.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        raise EnvironmentError(
            "GEMINI_API_KEY is not set. "
            "Open your .env file and paste your key from "
            "https://aistudio.google.com/app/apikey"
        )
    genai.configure(api_key=api_key)


def get_answer(pil_image, question: str) -> str:
    """
    Send an image + question to Gemini Vision and return the answer.

    Parameters
    ----------
    pil_image : PIL.Image.Image
        The preprocessed image object.
    question  : str
        The cleaned natural-language question from the user.

    Returns
    -------
    str
        The model's descriptive answer in English.

    Raises
    ------
    EnvironmentError : API key missing or invalid.
    RuntimeError     : Gemini API call failed.
    """
    try:
        _configure_gemini()

        # Use gemini-1.5-flash — fast, multimodal, free-tier friendly
        # NEW — replace with this
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")

        # Build a clear prompt that encourages a thorough but concise answer
        prompt = (
            f"You are an AI assistant that answers questions about images precisely and helpfully.\n\n"
            f"Question: {question}\n\n"
            f"Please provide a clear, accurate, and concise answer based only on what you observe "
            f"in the image. Do not fabricate details that are not visible."
        )

        # Send both the image and the prompt to the model
        response = model.generate_content([pil_image, prompt])

        # Extract and return the text answer
        if response and response.text:
            return response.text.strip()
        else:
            return "The model returned an empty response. Please try again with a different question."

    except EnvironmentError:
        raise  # Re-raise so Flask can return a 500 with a useful message

    except Exception as e:
        raise RuntimeError(f"Gemini API error: {str(e)}")
