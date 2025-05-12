# === file: run_rebuttal.py ===
import os
from pdf_utils import extract_text_from_pdf
from reviewers import get_all_reviewers
from rebuttal_loop import run_rebuttal_round
from report import save_reviews_to_pdf

# === CONFIGURATION ===
paper_path = "/Users/taramurphy/Downloads/example.pdf"
review_path = (
    "/Users/taramurphy/Documents/2025/code/mcp_tara/src/peer_review_report.pdf"
)
rebuttal_path = "/Users/taramurphy/Downloads/example.pdf"
journal = "NeurIPS"
output_dir = "rebuttal_outputs"

# === Load Inputs ===
print("📄 Extracting PDF text...")
paper_text = extract_text_from_pdf(paper_path)
review_text = extract_text_from_pdf(review_path)
rebuttal_text = extract_text_from_pdf(rebuttal_path)

# === Run Rebuttal Round ===
print("🤖 Getting reviewers...")
reviewers = get_all_reviewers(journal=journal)

print("🧠 Running rebuttal evaluation...")
feedback = run_rebuttal_round(paper_text, review_text, rebuttal_text, reviewers)

# === Display & Save ===
os.makedirs(output_dir, exist_ok=True)
round_num = 1
text_output = os.path.join(output_dir, f"rebuttal_round_{round_num}.txt")
pdf_output = os.path.join(output_dir, f"rebuttal_round_{round_num}.pdf")

all_accept = True
with open(text_output, "w") as f:
    for name, review in feedback.items():
        print(f"\n--- {name} ---\n{review}\n")
        f.write(f"--- {name} ---\n{review}\n\n")
        if "accept" not in review.lower():
            all_accept = False

print(f"💾 Text feedback saved to {text_output}")

# Save to PDF
save_reviews_to_pdf(feedback, output_path=pdf_output)
print(f"📄 PDF feedback saved to {pdf_output}")

if all_accept:
    print("\n✅ All reviewers have accepted. The paper is ready for publication!")
else:
    print(
        "\n🔁 Some reviewers still have concerns. Please revise and run again with a new rebuttal."
    )
