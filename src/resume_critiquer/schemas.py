from pydantic import BaseModel, Field


class ResumeReview(BaseModel):
    summary: str = Field(
        description="A concise overall assessment of the resume."
    )

    strengths: list[str] = Field(
        description="Strong aspects of the resume."
    )

    weaknesses: list[str] = Field(
        description="Specific areas that could be improved."
    )

    matched_skills: list[str] = Field(
        description="Skills from the resume relevant to the target role."
    )

    missing_skills: list[str] = Field(
        description=(
            "Important skills for the target role that are missing "
            "or not sufficiently demonstrated in the resume."
        )
    )

    keyword_gaps: list[str] = Field(
        description=(
            "Relevant keywords from the target role or job description "
            "that are missing from the resume."
        )
    )

    recommendations: list[str] = Field(
        description="Specific actionable recommendations for improvement."
    )

    rewritten_bullets: list[str] = Field(
        description=(
            "Examples of stronger resume bullet points based only on "
            "information already present in the resume."
        )
    )

    estimated_match_score: int = Field(
        ge=0,
        le=100,
        description=(
            "An estimated 0-100 alignment score between the resume "
            "and the target role. This is not an actual ATS score."
        ),
    )