# === file: rebuttal_ui.py ===
import streamlit as st
from pdf_utils import extract_text_from_pdf
from reviewers import get_all_reviewers
from rebuttal_loop import run_rebuttal_round

st.set_page_config(page_title="PeerLens Rebuttal Loop", layout="wide")
st.title("📝 PeerLens Rebuttal Loop")

# === Upload Inputs ===
paper_file = st.file_uploader("Upload Original Paper PDF", type="pdf")
review_file = st.file_uploader("Upload Review Report PDF", type="pdf")
rebuttal_file = st.file_uploader("Upload Rebuttal PDF", type="pdf")
journal = st.selectbox("Select Journal", ["NeurIPS", "Nature", "PLoS ONE"])

if paper_file and review_file and rebuttal_file:
    st.success("All files uploaded. Ready to run rebuttal loop.")

    # Extract text from each file
    with st.spinner("Extracting PDFs..."):
        paper_text = extract_text_from_pdf(paper_file)
        review_text = extract_text_from_pdf(review_file)
        rebuttal_text = extract_text_from_pdf(rebuttal_file)

    reviewers = get_all_reviewers(journal=journal)
    st.write("Running rebuttal loop...")

    feedback = run_rebuttal_round(paper_text, review_text, rebuttal_text, reviewers)

    all_accept = True
    for name, review in feedback.items():
        st.subheader(f"{name} Verdict")
        st.markdown(f"```\n{review}\n```")
        if "accept" not in review.lower():
            all_accept = False

    if all_accept:
        st.success(
            "🎉 All reviewers have accepted! Your paper is ready for submission."
        )
    else:
        st.warning(
            "Some reviewers still have concerns. Please revise your rebuttal and try again."
        )
else:
    st.info("Please upload all three PDF files to begin.")
