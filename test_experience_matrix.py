# test_experience_matrix.py
# ============================================================
# EXPERIENCE ROBUSTNESS REGRESSION TEST
#
# Purpose:
# 1. Verify ATS experience scoring for:
#    - freshers
#    - ranges (0-2, 1-3)
#    - minimums (3+, 5+)
#    - no experience requirement
# 2. Scan every uploaded resume for suspicious disagreement between
#    stated experience and date-calculated experience.
#
# This test does NOT hard-code any candidate name.
# ============================================================

from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO

import pdfplumber

from resume_parser.ats_scorer import calculate_ats_score
from resume_parser.experience import extract_experience


UPLOAD_DIR = Path("uploads")


# ============================================================
# HELPERS
# ============================================================

def run_experience_case(
    label,
    candidate_years,
    jd_text,
    expected_score,
    expected_type=None,
):
    """
    Run calculate_ats_score with a minimal neutral candidate.
    We only validate the experience-related fields.
    """

    candidate_experience = {
        "total_years": float(candidate_years),
        "stated_years": float(candidate_years),
        "calculated_years": float(candidate_years),
        "date_ranges": [],
        "job_titles": [],
        "records": [],
        "experience_text": "",
        "has_experience_section": candidate_years > 0,
    }

    # Keep the non-experience inputs deliberately simple.
    result = calculate_ats_score(
        resume_skills=["Python"],
        job_skills=["Python"],
        resume_text="Python developer candidate.",
        job_description=jd_text,
        candidate_experience=candidate_experience,
        education=[],
        projects=[],
    )

    actual_score = result.get(
        "experience_score"
    )

    requirement = result.get(
        "experience_requirement",
        {}
    )

    actual_type = requirement.get(
        "requirement_type"
    )

    passed = True
    errors = []

    if actual_score != expected_score:
        passed = False
        errors.append(
            f"expected score {expected_score}, "
            f"got {actual_score}"
        )

    if (
        expected_type is not None
        and actual_type != expected_type
    ):
        passed = False
        errors.append(
            f"expected type '{expected_type}', "
            f"got '{actual_type}'"
        )

    print()
    print(label)
    print("-" * 72)
    print("Candidate Years:", candidate_years)
    print("Requirement:", requirement)
    print("Experience Score:", actual_score)
    print(
        "Status:",
        "PASS" if passed else "FAIL"
    )

    for error in errors:
        print("  ERROR:", error)

    return passed


def extract_pdf_text(pdf_path):
    parts = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                parts.append(text)

    return "\n".join(parts)


def quiet_extract_experience(text):
    """
    Some experience parser versions print debug details.
    Suppress them for a clean regression summary.
    """
    buffer = StringIO()

    with redirect_stdout(buffer):
        return extract_experience(text)


# ============================================================
# ATS EXPERIENCE REQUIREMENT MATRIX
# ============================================================

def test_experience_matrix():

    print()
    print("=" * 72)
    print("1. ATS EXPERIENCE REQUIREMENT MATRIX")
    print("=" * 72)

    cases = [

        # ----------------------------------------------------
        # No experience requirement
        # ----------------------------------------------------

        (
            "No requirement - fresher",
            0.0,
            """
            Python Developer.
            Strong Python skills required.
            """,
            100,
            "none",
        ),

        (
            "No requirement - experienced candidate",
            4.08,
            """
            Python Developer.
            Strong Python skills required.
            """,
            100,
            "none",
        ),

        # ----------------------------------------------------
        # Fresher wording
        # ----------------------------------------------------

        (
            "Explicit fresher role",
            0.0,
            """
            Python Developer.
            Freshers and recent graduates are welcome.
            """,
            100,
            "fresher",
        ),

        # ----------------------------------------------------
        # Range requirements
        # ----------------------------------------------------

        (
            "Fresher inside 0-2 year range",
            0.0,
            """
            Python Developer.
            Required experience: 0-2 years.
            """,
            100,
            "range",
        ),

        (
            "2 years inside 1-3 year range",
            2.0,
            """
            Python Developer.
            Required experience: 1-3 years.
            """,
            100,
            "range",
        ),

        (
            "0 years below 1-3 year range",
            0.0,
            """
            Python Developer.
            Required experience: 1-3 years.
            """,
            0,
            "range",
        ),

        # Known regression case from the current scorer:
        # 4.08 years against a 1-3 year range should be
        # slightly penalized for being above the requested max.
        (
            "4.08 years above 1-3 year range",
            4.08,
            """
            AI/ML Engineer.
            Required experience: 1-3 years.
            """,
            83.8,
            "range",
        ),

        (
            "4.08 years above 0-2 year range",
            4.08,
            """
            AI/ML Engineer.
            Required experience: 0-2 years.
            """,
            68.8,
            "range",
        ),

        # ----------------------------------------------------
        # Minimum / plus requirements
        # ----------------------------------------------------

        (
            "4.08 years meets 3+ requirement",
            4.08,
            """
            AI/ML Engineer.
            Minimum experience: 3+ years.
            """,
            100,
            "minimum",
        ),

        (
            "4.08 years below 5+ requirement",
            4.08,
            """
            Senior AI/ML Engineer.
            Minimum experience: 5+ years.
            """,
            81.6,
            "minimum",
        ),

        (
            "6 years meets 5+ requirement",
            6.0,
            """
            Senior AI/ML Engineer.
            At least 5 years of experience required.
            """,
            100,
            "minimum",
        ),
    ]

    passed = 0
    failed = 0

    for case in cases:

        ok = run_experience_case(
            *case
        )

        if ok:
            passed += 1
        else:
            failed += 1

    return passed, failed, len(cases)


# ============================================================
# REAL RESUME CONSISTENCY SCAN
# ============================================================

def scan_resume_experience():

    print()
    print("=" * 72)
    print("2. REAL RESUME EXPERIENCE CONSISTENCY SCAN")
    print("=" * 72)

    if not UPLOAD_DIR.exists():
        print(
            "WARNING: uploads/ folder not found. "
            "Skipping resume scan."
        )
        return 0, 0, []

    pdf_files = sorted(
        UPLOAD_DIR.glob("*.pdf")
    )

    scanned = 0
    warnings = []

    for pdf_path in pdf_files:

        try:
            text = extract_pdf_text(
                pdf_path
            )

            experience = quiet_extract_experience(
                text
            )

        except Exception as exc:

            warnings.append(
                (
                    pdf_path.name,
                    f"parser error: "
                    f"{type(exc).__name__}: {exc}"
                )
            )

            continue

        scanned += 1

        stated = float(
            experience.get(
                "stated_years",
                0
            ) or 0
        )

        calculated = float(
            experience.get(
                "calculated_years",
                0
            ) or 0
        )

        total = float(
            experience.get(
                "total_years",
                0
            ) or 0
        )

        if total < 0:
            warnings.append(
                (
                    pdf_path.name,
                    f"negative total experience: {total}"
                )
            )

        # If BOTH sources exist and disagree substantially,
        # report it for review rather than failing the parser.
        if (
            stated > 0
            and calculated > 0
            and abs(
                stated - calculated
            ) >= 1.0
        ):
            warnings.append(
                (
                    pdf_path.name,
                    (
                        f"stated={stated} years, "
                        f"calculated={calculated} years, "
                        f"total={total} years"
                    )
                )
            )

    print("Resumes Scanned:", scanned)
    print(
        "Experience Consistency Warnings:",
        len(warnings)
    )

    if warnings:

        print()
        print(
            "Warnings are diagnostic, not automatic failures:"
        )

        for filename, warning in warnings:
            print(
                f"  - {filename}: {warning}"
            )

    else:

        print(
            "No major stated-vs-calculated "
            "experience discrepancies found."
        )

    return scanned, len(warnings), warnings


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 72)
    print("EXPERIENCE ROBUSTNESS REGRESSION TEST")
    print("=" * 72)

    passed, failed, total = (
        test_experience_matrix()
    )

    scanned, warning_count, warnings = (
        scan_resume_experience()
    )

    print()
    print("=" * 72)
    print("FINAL SUMMARY")
    print("=" * 72)

    print(
        "ATS Experience Cases:",
        total
    )

    print(
        "ATS Cases PASS:",
        passed
    )

    print(
        "ATS Cases FAIL:",
        failed
    )

    print(
        "Real Resumes Scanned:",
        scanned
    )

    print(
        "Diagnostic Warnings:",
        warning_count
    )

    print()

    if failed == 0:

        print(
            "REGRESSION STATUS: PASS"
        )

        print(
            "Experience scoring works across "
            "fresher, range, minimum and "
            "no-requirement cases."
        )

        raise SystemExit(0)

    else:

        print(
            "REGRESSION STATUS: FAIL"
        )

        print(
            "One or more ATS experience cases "
            "need investigation."
        )

        raise SystemExit(1)


if __name__ == "__main__":
    main()
