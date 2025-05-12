# === file: config.py ===
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AUTOGEN_USE_DOCKER = False

JOURNAL_STYLES = {
    "Nature": {
        "tone": "very formal and academic",
        "focus": "scientific novelty, broad impact, and clarity of communication. you have a clear focus on the natural sciences.",
    },
    "NeurIPS": {
        "tone": "technical and concise",
        "focus": "experimental rigor, reproducibility, and clarity of claims. You have a clear focus on machine learning and AI.",
    },
    "PLoS ONE": {
        "tone": "neutral and constructive",
        "focus": "scientific validity regardless of impact or novelty. You have a clear focus on open science and reproducibility.",
    },
}
