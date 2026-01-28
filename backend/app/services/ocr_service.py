import cv2
import pytesseract
import numpy as np
from PIL import Image


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Takes image bytes and returns extracted text using OCR.
    Error-proof and Railway-compatible.
    """

    # Convert bytes to image
    image = Image.open(np.frombuffer(image_bytes, np.uint8))
    image = image.convert("RGB")

    # Convert PIL image to OpenCV format
    open_cv_image = np.array(image)
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    # Improve OCR accuracy
    gray = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    # OCR configuration
    custom_config = r"--oem 3 --psm 6"

    text = pytesseract.image_to_string(gray, config=custom_config)

    return text.strip()
