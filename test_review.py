import sys
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


load_dotenv()


from resume_critiquer.gemini_client import analyze_resume


resume_path = PROJECT_ROOT / "sample_resume.pdf"

resume_text = ""

from resume_critiquer.resume_parser import extract_text

resume_text = extract_text(
    resume_path.read_bytes()
)


review = analyze_resume(
    resume_text=resume_text,
    target_role="Python Developer",
    job_description="""
We are looking for a Python Developer who has experience with
Python, REST APIs, Git, SQL, testing and cloud technologies.
Experience with FastAPI or Django is a plus.
""",
)


print("\n===== SUMMARY =====")
print(review.summary)

print("\n===== STRENGTHS =====")
for item in review.strengths:
    print("-", item)

print("\n===== WEAKNESSES =====")
for item in review.weaknesses:
    print("-", item)

print("\n===== MATCHED SKILLS =====")
for item in review.matched_skills:
    print("-", item)

print("\n===== MISSING SKILLS =====")
for item in review.missing_skills:
    print("-", item)

print("\n===== KEYWORD GAPS =====")
for item in review.keyword_gaps:
    print("-", item)

print("\n===== RECOMMENDATIONS =====")
for item in review.recommendations:
    print("-", item)

print("\n===== REWRITTEN BULLETS =====")
for item in review.rewritten_bullets:
    print("-", item)

print("\n===== ESTIMATED ALIGNMENT =====")
print(f"{review.estimated_match_score}/100")