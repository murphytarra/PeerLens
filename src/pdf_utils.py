# === file: pdf_utils.py ===
import os
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using pdfminer.six"""
    return extract_text(pdf_path)


def extract_images_from_pdf(pdf_path, output_folder):
    """Extracts images using PyMuPDF and saves them."""
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    image_paths = []

    for page_number in range(len(doc)):
        for img_index, img in enumerate(doc[page_number].get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_path = os.path.join(
                output_folder, f"page{page_number+1}_img{img_index+1}.{image_ext}"
            )
            with open(image_path, "wb") as f:
                f.write(image_bytes)
            image_paths.append(image_path)

    return image_paths


def structure_output(pdf_path, image_output_dir):
    """Combines text and images into a structured dictionary for AI processing."""
    text = extract_text_from_pdf(pdf_path)
    # images = extract_images_from_pdf(pdf_path, image_output_dir)

    structured_data = {
        "text": text,
        # "images": images,
        "metadata": {
            "source_file": str(pdf_path),
            "image_directory": str(image_output_dir),
        },
    }
    return structured_data
