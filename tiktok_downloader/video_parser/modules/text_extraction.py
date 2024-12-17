import pytesseract
from PIL import Image
import os

def extract_text_from_frames(frame_folder, output_folder):
    """
    Extract text from video frames using OCR.
    """
    os.makedirs(output_folder, exist_ok=True)
    extracted_text = {}

    for frame_file in os.listdir(frame_folder):
        frame_path = os.path.join(frame_folder, frame_file)
        text = pytesseract.image_to_string(Image.open(frame_path))
        extracted_text[frame_file] = text

    print("Text extraction complete.")
    return extracted_text
