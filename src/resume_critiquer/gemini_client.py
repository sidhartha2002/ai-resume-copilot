import os

from google import genai
from google.genai import types

from .schemas import ResumeReview


MODEL_NAME = "gemini-3.8-flash"


client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


def analyze_resume(
    resume_text: str,
    target_role: str,
    job_description: str = "",
) -> ResumeReview:

    prompt = f"""
You are an experienced technical recruiter and resume reviewer.

Analyze the resume for the target role below.

TARGET ROLE:
{target_role}

JOB DESCRIPTION:
{job_description or "No job description was provided."}

RESUME:
{resume_text}

Your task:

1. Summarize the resume for the target role.
2. Identify genuine strengths.
3. Identify concrete weaknesses.
4. Identify skills relevant to the target role.
5. Identify important missing or weakly demonstrated skills.
6. Identify relevant keywords that may be missing.
7. Give actionable recommendations.
8. Rewrite several existing resume bullets to make them clearer,
   stronger, and more achievement-oriented.

Important rules:

- Do not invent experience.
- Do not invent technologies.
- Do not invent certifications.
- Do not invent achievements.
- Do not invent education.
- Base your assessment only on the supplied resume and job description.
- If the job description is absent, evaluate against the target role.
- The match score is only an estimated alignment indicator.
- It is NOT an actual ATS score.

Return the result according to the provided schema.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ResumeReview,
        ),
    )

    if response.parsed is None:
        raise RuntimeError(
            "Gemini did not return the expected structured response."
        )

    return response.parsed