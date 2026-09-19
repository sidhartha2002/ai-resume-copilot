import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv


# ============================================================
# Project configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# ============================================================
# Environment configuration
# ============================================================

load_dotenv()

try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except st.errors.StreamlitSecretNotFoundError:
    pass


# Import after environment configuration
from resume_critiquer.gemini_client import analyze_resume
from resume_critiquer.report_builder import build_markdown_report
from resume_critiquer.resume_parser import extract_text


# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title="AI Resume Copilot",
    page_icon="📄",
    layout="wide",
)


# ============================================================
# Session state
# ============================================================

if "review" not in st.session_state:
    st.session_state.review = None

if "target_role" not in st.session_state:
    st.session_state.target_role = ""

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

if "resume_name" not in st.session_state:
    st.session_state.resume_name = ""

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""


# ============================================================
# Styling
# ============================================================

st.markdown(
    """
    <style>

    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        color: #6b7280;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Header
# ============================================================

st.markdown(
    '<div class="hero-title">📄 AI Resume Copilot</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-subtitle">'
    "Upload your resume, choose a target role, and get "
    "actionable AI-powered feedback."
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.header("About")

    st.write(
        """
        AI Resume Copilot analyzes your resume against a
        target role and optionally a specific job description.
        """
    )

    st.divider()

    st.markdown("### Analysis includes")

    st.markdown(
        """
        ✅ Strengths

        ⚠️ Areas to improve

        🎯 Relevant skills

        🧩 Missing skills

        🔑 Keyword gaps

        💡 Recommendations

        ✍️ Rewritten bullet examples
        """
    )

    st.divider()

    if st.session_state.review is not None:

        if st.button(
            "🗑️ Clear analysis",
            use_container_width=True,
        ):
            st.session_state.review = None
            st.session_state.target_role = ""
            st.session_state.job_description = ""
            st.session_state.resume_name = ""
            st.session_state.resume_text = ""
            st.rerun()

    st.divider()

    st.caption(
        "Built with Python, Gemini, Pydantic and Streamlit."
    )


# ============================================================
# Input section
# ============================================================

with st.form("resume_analysis_form"):

    st.subheader("🎯 Target")

    target_role = st.text_input(
        "Target role",
        value=st.session_state.target_role,
        placeholder="e.g. Python Developer",
        help=(
            "The role you want the resume evaluated against."
        ),
    )

    st.subheader("📄 Resume")

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf"],
        help="Use a text-based PDF for best extraction quality.",
    )

    st.subheader("📋 Job Description")

    job_description = st.text_area(
        "Optional job description",
        value=st.session_state.job_description,
        placeholder=(
            "Paste the job description here for a more "
            "role-specific analysis."
        ),
        height=200,
    )

    submitted = st.form_submit_button(
        "🔍 Analyze Resume",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# Process submission
# ============================================================

if submitted:

    if uploaded_file is None:
        st.error("Please upload a resume PDF.")
        st.stop()

    if not target_role.strip():
        st.error("Please enter a target role.")
        st.stop()

    with st.spinner("📖 Reading your resume..."):

        resume_bytes = uploaded_file.getvalue()

        resume_text = extract_text(
            resume_bytes
        )

    if not resume_text:

        st.error(
            "No readable text was found in this PDF. "
            "Please use a text-based PDF rather than "
            "a scanned image."
        )

        st.stop()

    with st.spinner(
        "🤖 Analyzing your resume with Gemini..."
    ):

        try:

            review = analyze_resume(
                resume_text=resume_text,
                target_role=target_role.strip(),
                job_description=job_description.strip(),
            )

        except Exception as exc:

            st.error(
                "The AI analysis could not be completed."
            )

            st.exception(exc)

            st.stop()

    # Save results
    st.session_state.review = review
    st.session_state.target_role = target_role.strip()
    st.session_state.job_description = (
        job_description.strip()
    )
    st.session_state.resume_name = uploaded_file.name
    st.session_state.resume_text = resume_text


# ============================================================
# Results
# ============================================================

review = st.session_state.review

if review is not None:

    st.divider()

    st.header("📊 Analysis Results")

    st.caption(
        f"Resume: `{st.session_state.resume_name}`  •  "
        f"Target role: `{st.session_state.target_role}`"
    )

    # --------------------------------------------------------
    # Score
    # --------------------------------------------------------

    score_col1, score_col2 = st.columns(
        [1, 3]
    )

    with score_col1:

        st.metric(
            "Estimated Alignment",
            f"{review.estimated_match_score}/100",
        )

    with score_col2:

        st.progress(
            review.estimated_match_score / 100
        )

        st.caption(
            "Alignment estimate based on the supplied "
            "resume and role context — not an ATS guarantee."
        )

    # --------------------------------------------------------
    # Tabs
    # --------------------------------------------------------

    overview_tab, skills_tab, recommendations_tab, raw_tab = (
        st.tabs(
            [
                "📋 Overview",
                "🎯 Skills & Keywords",
                "💡 Recommendations",
                "📄 Extracted Text",
            ]
        )
    )

    # ========================================================
    # Overview
    # ========================================================

    with overview_tab:

        st.subheader("📝 Overall Assessment")

        st.write(review.summary)

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Strengths")

            for item in review.strengths:
                st.markdown(f"- {item}")

        with col2:

            st.subheader("⚠️ Areas to Improve")

            for item in review.weaknesses:
                st.markdown(f"- {item}")

    # ========================================================
    # Skills & Keywords
    # ========================================================

    with skills_tab:

        st.subheader("🎯 Relevant Skills")

        if review.matched_skills:

            skill_columns = st.columns(
                min(4, len(review.matched_skills))
            )

            for index, skill in enumerate(
                review.matched_skills
            ):

                with skill_columns[
                    index % len(skill_columns)
                ]:

                    st.success(skill)

        else:

            st.info(
                "No strong skill matches were identified."
            )

        st.subheader(
            "🧩 Missing or Weakly Demonstrated Skills"
        )

        if review.missing_skills:

            for item in review.missing_skills:
                st.markdown(f"- {item}")

        else:

            st.success(
                "No major missing skills identified."
            )

        st.subheader("🔑 Keyword Gaps")

        if review.keyword_gaps:

            for keyword in review.keyword_gaps:
                st.code(keyword)

        else:

            st.success(
                "No significant keyword gaps identified."
            )

    # ========================================================
    # Recommendations
    # ========================================================

    with recommendations_tab:

        st.subheader("💡 Recommended Improvements")

        for index, recommendation in enumerate(
            review.recommendations,
            start=1,
        ):

            st.markdown(
                f"**{index}.** {recommendation}"
            )

        st.divider()

        st.subheader("✍️ Example Rewritten Bullets")

        st.caption(
            "These suggestions should only strengthen "
            "experience already supported by the resume."
        )

        for bullet in review.rewritten_bullets:

            st.markdown(
                f"> {bullet}"
            )

        st.divider()

        # ----------------------------------------------------
        # Download report
        # ----------------------------------------------------

        report = build_markdown_report(
            review=review,
            target_role=st.session_state.target_role,
        )

        st.download_button(
            label="⬇️ Download Analysis Report",
            data=report,
            file_name="resume_analysis_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

    # ========================================================
    # Raw extracted text
    # ========================================================

    with raw_tab:

        st.caption(
            "This is the text extracted from the uploaded PDF "
            "before AI analysis."
        )

        st.text_area(
            "Extracted resume text",
            value=st.session_state.resume_text,
            height=500,
            disabled=True,
        )