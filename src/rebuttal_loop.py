# === file: rebuttal_loop.py ===
from pdf_utils import extract_text_from_pdf
from reviewers import get_all_reviewers
import re

# === Step 1: Load Inputs ===
paper_path = "/Users/taramurphy/Downloads/example.pdf"
review_path = (
    "/Users/taramurphy/Documents/2025/code/mcp_tara/src/peer_review_report.pdf"
)
rebuttal_path = "/Users/taramurphy/Downloads/example.pdf"

paper_text = extract_text_from_pdf(paper_path)
review_text = extract_text_from_pdf(review_path)
rebuttal_text = extract_text_from_pdf(rebuttal_path)


# === Step 2: Identify Rebuttals Per Reviewer ===
def get_rebuttals_by_reviewer(rebuttal_text, reviewer_names):
    rebuttals = {}
    for name in reviewer_names:
        pattern = rf"{name}.*?(?=\n[A-Z][a-z]+Reviewer|\Z)"
        match = re.search(pattern, rebuttal_text, re.DOTALL)
        rebuttals[name] = (
            match.group(0).strip() if match else "No specific rebuttal found."
        )
    return rebuttals


# === Step 3: Reviewer Re-Evaluation ===
def run_rebuttal_round(paper_text, review_text, rebuttal_text, reviewers):
    responses = {}
    reviewer_names = [agent.name for agent in reviewers]
    rebuttals = get_rebuttals_by_reviewer(rebuttal_text, reviewer_names)

    for agent in reviewers:
        original = extract_reviewer_section(agent.name, review_text)
        rebuttal = rebuttals.get(agent.name, "No rebuttal provided.")

        prompt = f"""
You previously reviewed a manuscript with this feedback:

--- Original Review ---
{original}

The author has now responded:

--- Author Rebuttal ---
{rebuttal}

Please re-evaluate your original concerns in light of the author's response.
Return a revised review with:
- Updated Summary
- Remaining Concerns
- Final Verdict: Accept / Revise / Reject
"""
        response = agent.run(message=prompt, max_turns=1, user_input=False)
        response.process()
        responses[agent.name] = response.messages[-1]["content"]

    return responses


# === Helper: Extract Individual Review Section ===
def extract_reviewer_section(reviewer_name, review_text):
    import re

    pattern = rf"{reviewer_name} Review\n+(.*?)(?=\n\w+Reviewer Review|\Z)"
    match = re.search(pattern, review_text, re.DOTALL)
    return match.group(1).strip() if match else "No review found."


# === Example Usage ===
if __name__ == "__main__":
    reviewers = get_all_reviewers(journal="NeurIPS")
    round_num = 1
    while True:
        print(f"\n===== ROUND {round_num} =====")
        feedback = run_rebuttal_round(paper_text, review_text, rebuttal_text, reviewers)

        all_accept = True
        for name, review in feedback.items():
            print(f"\n--- {name} ---\n{review}\n")
            if "accept" not in review.lower():
                all_accept = False

        if all_accept:
            print(
                "\n✅ All reviewers have accepted. The paper is ready for publication!"
            )
            break
        else:
            print(
                "\n🔁 Some reviewers still have concerns. Please revise and upload a new rebuttal."
            )
            break  # or allow user input to continue loop
        round_num += 1
