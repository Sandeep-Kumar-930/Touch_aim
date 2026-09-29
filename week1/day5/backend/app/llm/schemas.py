from pydantic import BaseModel, Field


class Experience(BaseModel):

    company: str = ""

    role: str = ""

    duration: str = ""

    description: str = ""


class Education(BaseModel):

    degree: str = ""

    institution: str = ""

    year: str = ""


class Resume(BaseModel):

    name: str = ""

    email: str = ""

    phone: str = ""

    total_experience_years: float = 0.0

    skills: list[str] = Field(
        default_factory=list
    )

    experiences: list[Experience] = Field(
        default_factory=list
    )

    education: list[Education] = Field(
        default_factory=list
    )

    projects: list[str] = Field(
        default_factory=list
    )

    certifications: list[str] = Field(
        default_factory=list
    )


class JobDescription(BaseModel):

    role: str = ""

    required_skills: list[str] = Field(
        default_factory=list
    )

    preferred_skills: list[str] = Field(
        default_factory=list
    )

    minimum_experience: float = 0.0

    education_requirements: list[str] = Field(
        default_factory=list
    )

    responsibilities: list[str] = Field(
        default_factory=list
    )


class MatchResult(BaseModel):

    matching_skills: list[str] = Field(
        default_factory=list
    )

    missing_important_skills: list[str] = Field(
        default_factory=list
    )

    experience_requirement_met: bool = False

    overall_match_percentage: float = 0.0

    final_verdict: str = ""