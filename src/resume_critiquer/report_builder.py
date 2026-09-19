from .schemas import ResumeReview


def build_markdown_report(
    review: ResumeReview,
    target_role: str,
) -> str:
    """Build a downloadable Markdown resume analysis report."""

    lines = [
        "# AI Resume Analysis Report",
        "",
        f"**Target Role:** {target_role}",
        "",
        "## Estimated Role Alignment",
        "",
        f"**{review.estimated_match_score}/100**",
        "",
        "> This is an estimated alignment indicator based on "
        "the provided resume and role context. It is not an "
        "actual ATS score.",
        "",
        "## Overall Assessment",
        "",
        review.summary,
        "",
        "## Strengths",
        "",
    ]

    for item in review.strengths:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Areas to Improve",
            "",
        ]
    )

    for item in review.weaknesses:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Relevant Skills",
            "",
        ]
    )

    for item in review.matched_skills:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Missing or Weakly Demonstrated Skills",
            "",
        ]
    )

    for item in review.missing_skills:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Keyword Gaps",
            "",
        ]
    )

    for item in review.keyword_gaps:
        lines.append(f"- `{item}`")

    lines.extend(
        [
            "",
            "## Recommendations",
            "",
        ]
    )

    for item in review.recommendations:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Example Rewritten Bullets",
            "",
        ]
    )

    for item in review.rewritten_bullets:
        lines.append(f"> {item}")
        lines.append("")

    return "\n".join(lines)