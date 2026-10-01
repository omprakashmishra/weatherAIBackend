import os
import json
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


SYSTEM_PROMPT = (
    "You are a strict fact-checker. Reply ONLY with valid JSON in this exact shape:\n"
    "{\n"
    '  "verdict": "",\n'
    '  "confidence": 0,\n'
    '  "explanation": "",\n'
    '  "sources": [{"name": "", "url": ""}]\n'
    "}\n"
    "Rules:\n"
    "1. Detect the language of the claim and reply in that SAME language.\n"
    "2. Keep JSON keys in English.\n"
    "3. verdict must be one of: TRUE, FALSE, PARTIALLY TRUE, UNVERIFIABLE "
    "(translated into the claim's language).\n"
    "4. confidence is an integer 0-100.\n"
    "5. Max 3 sources. Never invent URLs. If unsure, leave url as empty string.\n"
    "6. If the claim cannot be verified, use UNVERIFIABLE and confidence < 50."
)


def fact_check(claim: str) -> dict:
    """Fact-check a claim with automatic retry for temporary Gemini errors."""

    max_retries = 3

    for attempt in range(max_retries):
        try:
            print(
                f"Gemini request: attempt {attempt + 1}/{max_retries}"
            )

            response = client.chat.completions.create(
                model="gemini-3.8-flash",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": claim,
                    },
                ],
                response_format={"type": "json_object"},
                temperature=0,
            )

            raw = response.choices[0].message.content

            try:
                return json.loads(raw)

            except json.JSONDecodeError:
                return {
                    "verdict": "UNVERIFIABLE",
                    "confidence": 0,
                    "explanation": "Model returned invalid JSON.",
                    "sources": [],
                }

        except Exception as e:
            error_message = str(e)

            print(f"Gemini error: {error_message}")

            # Retry temporary server/capacity errors.
            if "503" in error_message or "UNAVAILABLE" in error_message:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)
                    continue

            # Don't retry other errors.
            raise

    # Should only be reached if all retry attempts fail.
    return {
        "verdict": "UNVERIFIABLE",
        "confidence": 0,
        "explanation": "Gemini is temporarily unavailable. Please try again later.",
        "sources": [],
    }
