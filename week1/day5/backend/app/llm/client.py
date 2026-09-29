import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# --------------------------------------------------
# Project root
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[5]

ENV_FILE = PROJECT_ROOT / ".env"


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv(ENV_FILE)


GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if not GROQ_API_KEY:
    raise RuntimeError(
        f"GROQ_API_KEY was not found in {ENV_FILE}"
    )


# --------------------------------------------------
# Groq client
# --------------------------------------------------

client = Groq(
    api_key=GROQ_API_KEY
)


# --------------------------------------------------
# Model
# --------------------------------------------------

MODEL = "openai/gpt-oss-120b"


# --------------------------------------------------
# Generate JSON
# --------------------------------------------------

def generate_json(
    system_prompt: str,
    user_prompt: str,
) -> str:

    response = client.chat.completions.create(
        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],

        response_format={
            "type": "json_object"
        },

        temperature=0,
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            "Groq returned an empty response."
        )

    return content