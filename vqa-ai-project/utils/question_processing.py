"""
utils/question_processing.py
-----------------------------
Cleans and validates the user's natural language question
before it is passed to the VQA model.
"""

import re


# Hard limits
MIN_QUESTION_LENGTH = 3      # characters
MAX_QUESTION_LENGTH = 500    # characters


def clean_question(raw_question: str) -> str:
    """
    Strip, normalise whitespace, and remove potentially harmful
    control characters from the user's question.

    Parameters
    ----------
    raw_question : str   Raw text from the HTML form input.

    Returns
    -------
    str   Cleaned question string.
    """
    if not isinstance(raw_question, str):
        raise TypeError("Question must be a string.")

    # Strip leading/trailing whitespace
    question = raw_question.strip()

    # Collapse multiple spaces / tabs / newlines into a single space
    question = re.sub(r"\s+", " ", question)

    # Remove null bytes and ASCII control characters (keep printable + unicode)
    question = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", question)

    return question


def validate_question(question: str) -> tuple[bool, str]:
    """
    Validate the cleaned question.

    Parameters
    ----------
    question : str   Already cleaned question.

    Returns
    -------
    (is_valid: bool, error_message: str)
    error_message is an empty string when is_valid is True.
    """
    if not question:
        return False, "Question cannot be empty. Please type a question about the image."

    if len(question) < MIN_QUESTION_LENGTH:
        return False, f"Question is too short (minimum {MIN_QUESTION_LENGTH} characters)."

    if len(question) > MAX_QUESTION_LENGTH:
        return False, (
            f"Question is too long ({len(question)} characters). "
            f"Please keep it under {MAX_QUESTION_LENGTH} characters."
        )

    return True, ""


def process_question(raw_question: str) -> str:
    """
    Convenience wrapper: clean then validate the question.
    Returns the cleaned question on success, raises ValueError on failure.

    Parameters
    ----------
    raw_question : str

    Returns
    -------
    str   Validated, cleaned question.

    Raises
    ------
    ValueError  If validation fails.
    """
    cleaned = clean_question(raw_question)
    is_valid, error_msg = validate_question(cleaned)

    if not is_valid:
        raise ValueError(error_msg)

    return cleaned
