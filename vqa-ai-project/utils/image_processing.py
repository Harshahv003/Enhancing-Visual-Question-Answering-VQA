"""
utils/image_processing.py
--------------------------
Handles all image loading, validation, and preprocessing
before the image is sent to the Gemini Vision API.
"""

from PIL import Image, UnidentifiedImageError
import io


# Supported image MIME types
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "bmp"}

# Target size for the vision model input
TARGET_SIZE = (512, 512)


def allowed_file(filename: str) -> bool:
    """
    Check if the uploaded file has an allowed extension.

    Parameters
    ----------
    filename : str  e.g. "photo.jpg"

    Returns
    -------
    bool
    """
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def preprocess_image(file_bytes: bytes) -> Image.Image:
    """
    Load raw bytes from an uploaded file, validate it is a real image,
    resize and normalise it for the Gemini Vision API.

    Parameters
    ----------
    file_bytes : bytes
        Raw bytes from request.files['image'].read()

    Returns
    -------
    PIL.Image.Image
        A clean RGB image ready to be passed to the model.

    Raises
    ------
    ValueError
        If the bytes cannot be decoded as a valid image.
    """
    try:
        # Open image from bytes
        image = Image.open(io.BytesIO(file_bytes))
    except UnidentifiedImageError:
        raise ValueError(
            "The uploaded file could not be read as an image. "
            "Please upload a valid PNG, JPG, JPEG, WEBP, GIF, or BMP file."
        )

    # Convert to RGB — handles RGBA, P (palette), L (grayscale), etc.
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Resize using high-quality Lanczos resampling
    # Gemini works well with images up to 1024×1024; 512×512 is a good balance
    image = image.resize(TARGET_SIZE, Image.LANCZOS)

    return image


def get_image_info(pil_image: Image.Image) -> dict:
    """
    Return basic metadata about the preprocessed image (for debugging / logging).

    Parameters
    ----------
    pil_image : PIL.Image.Image

    Returns
    -------
    dict  { "size": (w, h), "mode": str }
    """
    return {
        "size": pil_image.size,
        "mode": pil_image.mode,
    }
