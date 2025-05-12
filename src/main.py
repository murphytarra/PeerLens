# === file: main.py ===
import os
from config import AUTOGEN_USE_DOCKER
from pdf_utils import structure_output
from reviewers import get_all_reviewers
from review_engine import run_reviews, print_reviews
from report import save_reviews_to_pdf

# Disable Docker for AutoGen (if not needed)
os.environ["AUTOGEN_USE_DOCKER"] = str(AUTOGEN_USE_DOCKER)

# === Load PDF ===
pdf_file = "/Users/taramurphy/Downloads/example.pdf"
output_folder = "example_extracted"

structured = structure_output(pdf_file, output_folder)
manuscript_text = structured["text"]

# === Select Journal ===
journal = "NeurIPS"
reviewers = get_all_reviewers(journal=journal)

# === Run Reviews ===
responses = run_reviews(reviewers, manuscript_text)
print_reviews(responses)

# === Export to PDF ===s
save_reviews_to_pdf(responses)
