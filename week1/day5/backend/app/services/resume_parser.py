import json

from app.llm.client import generate_json
from app.llm.schemas import Resume


SYSTEM_PROMPT = """
You are an expert resume information extraction system.

Your task is to extract structured information from a resume.

Rules:

1. Use ONLY information present in the resume.
2. Never invent skills, jobs, companies, education,
   projects, certifications, dates, or contact information.
3. Return valid JSON only.
4. If information is unavailable, use an empty string,
   empty list, or 0.
5. Estimate total experience only when it can reasonably
   be calculated from the information provided.
"""


def parse_resume(
    resume_text: str,
) -> Resume:

    user_prompt = f"""
Extract structured information from this resume.

Return exactly this JSON structure:

{{
    "name": "",
    "email": "",
    "phone": "",
    "total_experience_years": 0,
    "skills": [],
    "experiences": [
        {{
            "company": "",
            "role": "",
            "duration": "",
            "description": ""
        }}
    ],
    "education": [
        {{
            "degree": "",
            "institution": "",
            "year": ""
        }}
    ],
    "projects": [],
    "certifications": []
}}

RESUME TEXT:

{resume_text}
"""

    result = generate_json(
        SYSTEM_PROMPT,
        user_prompt,
    )

    data = json.loads(result)

    return Resume.model_validate(data)