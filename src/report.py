# === file: report.py ===
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import datetime
import re


def strip_markdown(md_text):
    # Remove markdown syntax: **bold**, *italic*, `code`, #### headings, etc.
    text = re.sub(r"[*`_]+", "", md_text)  # remove bold, italic, code
    text = re.sub(
        r"^#+\s*", "", text, flags=re.MULTILINE
    )  # remove headings like ## or ###
    return [line.strip() for line in text.split("\n") if line.strip()]


def save_reviews_to_pdf(responses, output_path="peer_review_report.pdf"):
    doc = SimpleDocTemplate(output_path, pagesize=LETTER)
    story = []

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    # Add title and timestamp
    story.append(Paragraph("PeerLens Review Report", title_style))
    story.append(
        Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", body_style)
    )
    story.append(Spacer(1, 0.3 * inch))

    # Add each reviewer response
    for reviewer, review in responses.items():
        story.append(Paragraph(f"{reviewer} Review", heading_style))
        for line in strip_markdown(review):
            story.append(Paragraph(line, body_style))
        story.append(Spacer(1, 0.2 * inch))

    # Build PDF
    doc.build(story)
    print(f"✅ PDF saved to: {output_path}")
