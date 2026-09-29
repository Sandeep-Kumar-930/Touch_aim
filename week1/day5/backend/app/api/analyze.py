from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from app.services.document_parser import (
    extract_resume_text,
)

from app.services.jd_analyzer import (
    analyze_job_description,
)

from app.services.matcher import (
    match_resume_to_job,
)

from app.services.resume_parser import (
    parse_resume,
)


router = APIRouter(
    prefix="/api",
    tags=["Resume Analysis"],
)


@router.post("/analyze")
async def analyze_resume(
    job_description: str = Form(...),
    resume: UploadFile = File(...),
):
    """
    Analyze an uploaded resume against a job description.
    """

    if not resume.filename:
        raise HTTPException(
            status_code=400,
            detail="Resume file is required.",
        )

    filename = resume.filename.lower()

    if not (
        filename.endswith(".pdf")
        or filename.endswith(".docx")
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported.",
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty.",
        )

    try:

        file_bytes = await resume.read()

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded resume is empty.",
            )

        resume_text = extract_resume_text(
            resume.filename,
            file_bytes,
        )

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not extract text from "
                    "the uploaded resume."
                ),
            )

        job = analyze_job_description(
            job_description
        )

        parsed_resume = parse_resume(
            resume_text
        )

        match = match_resume_to_job(
            job,
            parsed_resume,
        )

        return {

            "status": "success",

            "candidate": {

                "name": parsed_resume.name,

                "email": parsed_resume.email,

                "phone": parsed_resume.phone,

                "experience_years": (
                    parsed_resume.total_experience_years
                ),

                "skills": parsed_resume.skills,

                "projects": parsed_resume.projects,

                "certifications": (
                    parsed_resume.certifications
                ),

                "experiences": [

                    experience.model_dump()

                    for experience
                    in parsed_resume.experiences

                ],

                "education": [

                    education.model_dump()

                    for education
                    in parsed_resume.education

                ],
            },

            "job": job.model_dump(),

            "analysis": match.model_dump(),

            "metadata": {

                "filename": resume.filename,

                "resume_text_length": len(
                    resume_text
                ),

            },
        }

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=f"Analysis failed: {str(error)}",

        )