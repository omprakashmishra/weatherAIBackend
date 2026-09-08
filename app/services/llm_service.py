import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("app/routes/.env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_response():
    response = client.responses.create(
        model="gpt-5",
        input="Say hello in one short sentence."
    )

    return response.output_text