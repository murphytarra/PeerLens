# === file: reviewers.py ===
from autogen import ConversableAgent, LLMConfig
from config import JOURNAL_STYLES

llm_config = LLMConfig(api_type="openai", model="gpt-4o-mini")


def create_reviewer(name, role_desc, journal="Nature"):
    tone = JOURNAL_STYLES[journal]["tone"]
    focus = JOURNAL_STYLES[journal]["focus"]

    prompt = (
        f"You are a peer reviewer for the journal {journal}. "
        f"Your tone should be {tone}. Focus on {focus}. "
        f"You are acting as a {role_desc}.\n\n"
        "Provide a structured review with:\n"
        "- Summary\n"
        "- Major Concerns\n"
        "- Minor Suggestions\n"
        "- Score (0–10)"
    )

    return ConversableAgent(name=name, system_message=prompt, llm_config=llm_config)


def get_all_reviewers(journal="Nature"):
    return [
        create_reviewer(
            "MethodologistReviewer", "methodology and reproducibility expert", journal
        ),
        create_reviewer("DomainExpertReviewer", "domain-specific evaluator", journal),
        create_reviewer(
            "ContrarianReviewer", "skeptical and critical reviewer", journal
        ),
    ]
