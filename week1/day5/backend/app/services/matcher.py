from app.llm.schemas import (
    JobDescription,
    MatchResult,
    Resume,
)


def normalize(value: str) -> str:
    return value.strip().lower()


def match_resume_to_job(
    job: JobDescription,
    resume: Resume,
) -> MatchResult:

    resume_skills = {
        normalize(skill)
        for skill in resume.skills
    }

    matching_skills = []

    missing_skills = []

    for skill in job.required_skills:

        if normalize(skill) in resume_skills:

            matching_skills.append(skill)

        else:

            missing_skills.append(skill)

    # ---------------------------------------------
    # Skill score
    # ---------------------------------------------

    if job.required_skills:

        skill_score = (
            len(matching_skills)
            / len(job.required_skills)
        ) * 100

    else:

        skill_score = 100

    # ---------------------------------------------
    # Experience score
    # ---------------------------------------------

    if job.minimum_experience <= 0:

        experience_score = 100

    elif (
        resume.total_experience_years
        >= job.minimum_experience
    ):

        experience_score = 100

    else:

        experience_score = (
            resume.total_experience_years
            / job.minimum_experience
        ) * 100

    experience_score = min(
        experience_score,
        100,
    )

    # ---------------------------------------------
    # Overall score
    # ---------------------------------------------

    overall_score = (
        skill_score * 0.60
        + experience_score * 0.40
    )

    # ---------------------------------------------
    # Experience requirement
    # ---------------------------------------------

    experience_met = (
        resume.total_experience_years
        >= job.minimum_experience
    )

    if job.minimum_experience <= 0:

        experience_met = True

    # ---------------------------------------------
    # Verdict
    # ---------------------------------------------

    if overall_score >= 80:

        verdict = "Excellent match"

    elif overall_score >= 65:

        verdict = "Good match"

    elif overall_score >= 50:

        verdict = "Moderate match"

    else:

        verdict = "Low match"

    return MatchResult(

        matching_skills=matching_skills,

        missing_important_skills=missing_skills,

        experience_requirement_met=experience_met,

        overall_match_percentage=round(
            overall_score,
            2,
        ),

        final_verdict=verdict,
    )