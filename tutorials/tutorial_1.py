# === main.py ===
"""
Tutorial: Run Simulated Peer Reviews on a Research Manuscript

This script demonstrates how to:
1. Load a research manuscript (PDF),
2. Automatically extract and structure its content,
3. Select a target journal (to tailor reviewer expectations),
4. Generate reviewer-style feedback from multiple agents,
5. Export the results into a formatted PDF review report.

Perfect for testing, training, or preparing for real peer review.

---

Required Modules:
- config.py             # Contains environment flags like AUTOGEN_USE_DOCKER
- pdf_utils.py          # Extracts and structures text from PDF
- reviewers.py          # Sets up reviewer agents tailored to a journal
- review_engine.py      # Handles the review loop and response formatting
- report.py             # Outputs the final reviews as a PDF file
"""

import os
from config import AUTOGEN_USE_DOCKER
from pdf_utils import structure_output
from reviewers import get_all_reviewers
from review_engine import run_reviews, print_reviews
from report import save_reviews_to_pdf

# Step 1: Configure Environment
# If you do not need Docker for AutoGen, disable it here
os.environ["AUTOGEN_USE_DOCKER"] = str(AUTOGEN_USE_DOCKER)

# Step 2: Load and Extract Manuscript
# Provide the path to your research paper (PDF)
pdf_file = "/Users/taramurphy/Downloads/example.pdf"

# Choose where the extracted text and data should be stored
output_folder = "example_extracted"

# Use OCR and layout parsing to extract structured text from the manuscript
print(f"🔍 Extracting text from {pdf_file}...")
structured = structure_output(pdf_file, output_folder)
manuscript_text = structured["text"]

# Step 3: Select Journal
# Choose a journal (e.g., NeurIPS, Nature, Science) to tailor reviewer behavior
journal = "NeurIPS"
print(f"📚 Setting up reviewers for journal: {journal}")
reviewers = get_all_reviewers(journal=journal)

# Step 4: Run the Simulated Reviews
# Each reviewer will evaluate the manuscript and provide comments and scores
print("🧠 Running reviews...")
responses = run_reviews(reviewers, manuscript_text)

# Display the results in the terminal
print("📄 Review Responses:")
print_reviews(responses)

# Step 5: Export Reviews to PDF
# Save the entire review session to a formatted PDF file
print("💾 Saving reviews to PDF...")
save_reviews_to_pdf(responses)

print("✅ Review workflow complete!")
