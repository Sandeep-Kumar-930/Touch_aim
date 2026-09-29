import json

from app.llm.client import generate_json
from app.llm.schemas import JobDescription


SYSTEM_PROMPT = """
You are an expert Job Description analysis system.

Extract the actual requirements from the supplied job description.

Rules:

1. Separate required skills from preferred skills.
2. Identify minimum experience.
3. Identify education requirements.
4. Identify important responsibilities.
5. Never invent requirements.
6. Return valid JSON only.
"""


def analyze_job_description(
    job_description: str,
) -> JobDescription:

    user_prompt = f"""
Analyze this job description.

Return exactly this JSON structure:

{{
    "role": "",
    "required_skills": [],
    "preferred_skills": [],
    "minimum_experience": 0,
    "education_requirements": [],
    "responsibilities": []
}}

JOB DESCRIPTION:

{job_description}
"""

    result = generate_json(
        SYSTEM_PROMPT,
        user_prompt,
    )

    data = json.loads(result)

    return JobDescription.model_validate(data)