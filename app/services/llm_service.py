import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("app/routes/.env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = (
    "You are a strict fact-checker. Reply ONLY with valid JSON in this exact shape:\n"
    '{\n'
    '  "verdict": "",\n'
    '  "confidence": 0,\n'
    '  "explanation": "",\n'
    '  "sources": [{"name": "", "url": ""}]\n'
    '}\n'
    "Rules:\n"
    "1. Detect the language of the claim and reply in that SAME language "
    "(verdict, explanation, source names).\n"
    "2. Keep JSON keys in English.\n"
    "3. verdict must be one of: TRUE, FALSE, PARTIALLY TRUE, UNVERIFIABLE "
    "translated into the claim's language.\n"
    "4. confidence is an integer 0-100.\n"
    "5. Max 3 sources. Never invent URLs. If unsure, leave url as empty string.\n"
    "6. If the claim cannot be verified, use the UNVERIFIABLE verdict and confidence < 50."
)


def fact_check(claim: str) -> dict:
    """Fact-check a claim. Returns dict with verdict, confidence, explanation, sources."""
    response = client.responses.create(
        model="gpt-5",
        instructions=SYSTEM_PROMPT,
        input=claim,
        text={"format": {"type": "json_object"}},
    )

    raw = response.output_text
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "verdict": "UNVERIFIABLE",
            "confidence": 0,
            "explanation": "Model returned invalid JSON.",
            "sources": [],
        }