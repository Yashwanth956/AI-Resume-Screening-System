# test_all_resumes.py
# ============================================================
# GENERALIZATION + MULTI-RESUME REGRESSION TEST
#
# Goal:
# - Test ALL PDFs currently present in uploads/
# - Support fresher and experienced resumes
# - Avoid hard-coding one candidate's expected ATS/role
# - Validate the complete parsing/matching/recommendation flow
# - Validate EVERY role currently defined in JOB_ROLES
#
# IMPORTANT:
# Passing this test means the current resume set does not crash
# and the system respects key invariants. It does NOT prove that
# every resume format in the world is supported.
# ============================================================

from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO

import pdfplumber

from resume_parser.skills import extract_skills
from resume_parser.education import extract_education
from resume_parser.experience import extract_experience
from resume_parser.project import extract_projects
from resume_parser.jd_skill_extractor import extract_jd_skills
from resume_parser.job_matcher import analyze_job_match
from resume_parser.ats_scorer import calculate_ats_score
from resume_parser.role_recommender import recommend_job_roles
from resume_parser.job_roles import JOB_ROLES


# ============================================================
# CONFIG
# ============================================================

UPLOAD_DIR = Path("uploads")

TOP_N_ROLES = 5

# A resume with no detected skills is reported as a warning rather
# than an immediate failure because the file may be non-IT,
# image-only, malformed, or use unsupported wording.
FAIL_ON_ZERO_SKILLS = False


# ============================================================
# HELPERS
# ============================================================

def extract_pdf_text(pdf_path):
    """Extract text from a PDF using pdfplumber."""
    parts = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                parts.append(page_text)

    return "\n".join(parts).strip()


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def valid_percentage(value):
    return is_number(value) and 0 <= float(value) <= 100


def get_role_skill_names(role):
    """
    JOB_ROLES values may be a list/tuple/set or a dict.
    Iterating a dict gives the skill names, which is what we need.
    """
    required = JOB_ROLES.get(role, [])
    return list(required)


def build_role_jd(role):
    """
    Build a neutral JD from the role's own configured skills.

    We deliberately do NOT add an experience requirement here.
    That keeps this a parser/scorer smoke test for both freshers
    and experienced candidates instead of forcing one experience
    level onto every resume.
    """
    skills = get_role_skill_names(role)

    skill_text = ", ".join(skills)

    return f"""
We are hiring for the role of {role}.

Required technical skills:
{skill_text}

Candidates will be evaluated based on relevant technical skills,
education, projects and professional experience.
""".strip()


def quiet_extract_projects(text):
    """
    project.py currently prints debug output.
    Suppress it so the all-resume summary stays readable.
    """
    buffer = StringIO()

    with redirect_stdout(buffer):
        result = extract_projects(text)

    return result


def add_failure(failures, message):
    failures.append(message)


def add_warning(warnings, message):
    warnings.append(message)


# ============================================================
# ROLE CATALOG VALIDATION
# ============================================================

def test_role_catalog():
    failures = []
    warnings = []

    if not isinstance(JOB_ROLES, dict):
        add_failure(
            failures,
            f"JOB_ROLES must be a dict, got {type(JOB_ROLES).__name__}"
        )
        return failures, warnings

    if not JOB_ROLES:
        add_failure(failures, "JOB_ROLES is empty.")
        return failures, warnings

    seen_lower = set()

    for role, required_skills in JOB_ROLES.items():

        if not isinstance(role, str) or not role.strip():
            add_failure(
                failures,
                f"Invalid role name: {repr(role)}"
            )
            continue

        role_key = role.strip().lower()

        if role_key in seen_lower:
            add_failure(
                failures,
                f"Duplicate role name detected: {role}"
            )

        seen_lower.add(role_key)

        skill_names = list(required_skills)

        if not skill_names:
            add_failure(
                failures,
                f"{role}: no required skills configured."
            )
            continue

        normalized_seen = set()

        for skill in skill_names:

            if not isinstance(skill, str) or not skill.strip():
                add_failure(
                    failures,
                    f"{role}: invalid skill entry {repr(skill)}"
                )
                continue

            skill_key = skill.strip().lower()

            if skill_key in normalized_seen:
                add_warning(
                    warnings,
                    f"{role}: duplicate skill '{skill}'"
                )

            normalized_seen.add(skill_key)

    return failures, warnings


# ============================================================
# ROLE REACHABILITY TEST
# ============================================================

def test_all_roles_reachable():
    """
    Every configured role should be reachable by the recommender
    when a synthetic candidate has all skills configured for that role.

    This checks role coverage without tying the system to one resume.
    """
    failures = []
    warnings = []

    total_roles = len(JOB_ROLES)

    for role in JOB_ROLES:

        synthetic_skills = get_role_skill_names(role)

        try:
            recommendations = recommend_job_roles(
                synthetic_skills,
                top_n=total_roles
            )

        except Exception as exc:
            add_failure(
                failures,
                f"{role}: recommender crashed: {type(exc).__name__}: {exc}"
            )
            continue

        returned_roles = [
            item.get("role")
            for item in recommendations
            if isinstance(item, dict)
        ]

        if role not in returned_roles:
            add_failure(
                failures,
                f"{role}: role is configured but not reachable "
                f"from its own required skills."
            )
            continue

        own_result = next(
            item
            for item in recommendations
            if item.get("role") == role
        )

        score = own_result.get("score")

        if not valid_percentage(score):
            add_failure(
                failures,
                f"{role}: invalid recommendation score {score}"
            )

        matched_count = own_result.get("matched_count", 0)
        total_skills = own_result.get("total_skills", 0)

        if matched_count <= 0:
            add_failure(
                failures,
                f"{role}: matched_count is {matched_count}"
            )

        if total_skills <= 0:
            add_failure(
                failures,
                f"{role}: total_skills is {total_skills}"
            )

    return failures, warnings


# ============================================================
# SINGLE RESUME TEST
# ============================================================

def test_resume(pdf_path):
    failures = []
    warnings = []
    details = {}

    # --------------------------------------------------------
    # PDF text
    # --------------------------------------------------------

    try:
        text = extract_pdf_text(pdf_path)
    except Exception as exc:
        add_failure(
            failures,
            f"PDF extraction crashed: {type(exc).__name__}: {exc}"
        )

        return {
            "status": "FAIL",
            "failures": failures,
            "warnings": warnings,
            "details": details,
        }

    details["characters"] = len(text)

    if not text:
        add_failure(
            failures,
            "No extractable text found in PDF."
        )

        return {
            "status": "FAIL",
            "failures": failures,
            "warnings": warnings,
            "details": details,
        }

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    try:
        skills = extract_skills(text)
    except Exception as exc:
        add_failure(
            failures,
            f"Skill extraction crashed: {type(exc).__name__}: {exc}"
        )
        skills = []

    if not isinstance(skills, list):
        add_failure(
            failures,
            f"Skills must be a list, got {type(skills).__name__}"
        )
        skills = []

    details["skills"] = len(skills)

    if not skills:
        message = "No recognized skills were extracted."

        if FAIL_ON_ZERO_SKILLS:
            add_failure(failures, message)
        else:
            add_warning(warnings, message)

    if len(skills) != len(set(skills)):
        add_warning(
            warnings,
            "Duplicate skills detected in extracted skill list."
        )

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    try:
        education = extract_education(text)
    except Exception as exc:
        add_failure(
            failures,
            f"Education extraction crashed: {type(exc).__name__}: {exc}"
        )
        education = []

    if not isinstance(education, list):
        add_failure(
            failures,
            f"Education must be a list, got {type(education).__name__}"
        )
        education = []

    details["education"] = len(education)

    if not education:
        add_warning(
            warnings,
            "No education records extracted."
        )

    for index, record in enumerate(education, start=1):

        if not isinstance(record, dict):
            add_failure(
                failures,
                f"Education #{index} is not a dictionary."
            )
            continue

        for key in ("degree", "institution", "score", "duration"):
            if key not in record:
                add_failure(
                    failures,
                    f"Education #{index} missing key '{key}'."
                )

    # --------------------------------------------------------
    # Experience
    # --------------------------------------------------------

    try:
        experience = extract_experience(text)
    except Exception as exc:
        add_failure(
            failures,
            f"Experience extraction crashed: {type(exc).__name__}: {exc}"
        )
        experience = {}

    if not isinstance(experience, dict):
        add_failure(
            failures,
            f"Experience must be a dict, got {type(experience).__name__}"
        )
        experience = {}

    total_years = experience.get("total_years", 0)

    if not is_number(total_years):
        add_failure(
            failures,
            f"Experience total_years is not numeric: {total_years}"
        )
        total_years = 0

    if total_years < 0:
        add_failure(
            failures,
            f"Experience cannot be negative: {total_years}"
        )

    details["experience"] = total_years

    # --------------------------------------------------------
    # Projects
    # --------------------------------------------------------

    try:
        projects = quiet_extract_projects(text)
    except Exception as exc:
        add_failure(
            failures,
            f"Project extraction crashed: {type(exc).__name__}: {exc}"
        )
        projects = []

    if not isinstance(projects, list):
        add_failure(
            failures,
            f"Projects must be a list, got {type(projects).__name__}"
        )
        projects = []

    details["projects"] = len(projects)

    for index, project in enumerate(projects, start=1):

        if not isinstance(project, dict):
            add_failure(
                failures,
                f"Project #{index} is not a dictionary."
            )
            continue

        if "title" not in project:
            add_failure(
                failures,
                f"Project #{index} missing 'title'."
            )

        if "technologies" not in project:
            add_failure(
                failures,
                f"Project #{index} missing 'technologies'."
            )

        if "description" not in project:
            add_failure(
                failures,
                f"Project #{index} missing 'description'."
            )

        elif not isinstance(project.get("description"), list):
            add_failure(
                failures,
                f"Project #{index} description must be a list."
            )

    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    try:
        recommendations = recommend_job_roles(
            skills,
            top_n=TOP_N_ROLES
        )
    except Exception as exc:
        add_failure(
            failures,
            f"Role recommender crashed: {type(exc).__name__}: {exc}"
        )
        recommendations = []

    if not isinstance(recommendations, list):
        add_failure(
            failures,
            "Recommendations must be a list."
        )
        recommendations = []

    details["recommendations"] = len(recommendations)

    returned_roles = []

    for index, item in enumerate(recommendations, start=1):

        if not isinstance(item, dict):
            add_failure(
                failures,
                f"Recommendation #{index} is not a dictionary."
            )
            continue

        role = item.get("role")
        score = item.get("score")

        if role not in JOB_ROLES:
            add_failure(
                failures,
                f"Recommendation #{index} returned unknown role: {role}"
            )

        if not valid_percentage(score):
            add_failure(
                failures,
                f"Recommendation #{index} has invalid score: {score}"
            )

        if role:
            returned_roles.append(role)

    if len(returned_roles) != len(set(returned_roles)):
        add_failure(
            failures,
            "Duplicate recommended roles returned."
        )

    if skills and not recommendations:
        add_warning(
            warnings,
            "Skills were extracted but no job recommendations were returned."
        )

    # --------------------------------------------------------
    # Full ATS + Job Match smoke test
    #
    # We use the candidate's top recommended configured role to
    # build a role-appropriate JD. This avoids comparing every
    # resume against the same AI/ML job.
    # --------------------------------------------------------

    if recommendations:

        top_role = recommendations[0].get("role")
        details["top_role"] = top_role

        if top_role in JOB_ROLES:

            job_description = build_role_jd(top_role)

            try:
                job_skills = extract_jd_skills(
                    job_description
                )
            except Exception as exc:
                add_failure(
                    failures,
                    f"JD skill extraction crashed: "
                    f"{type(exc).__name__}: {exc}"
                )
                job_skills = []

            details["job_skills"] = len(job_skills)

            if not job_skills:
                add_warning(
                    warnings,
                    f"No JD skills extracted for top role '{top_role}'."
                )

            if job_skills:

                try:
                    match_result = analyze_job_match(
                        skills,
                        job_skills
                    )

                    match_score = match_result.get(
                        "match_score",
                        0
                    )

                    if not valid_percentage(match_score):
                        add_failure(
                            failures,
                            f"Invalid job match score: {match_score}"
                        )

                    details["job_match"] = match_score

                except Exception as exc:
                    add_failure(
                        failures,
                        f"Job matcher crashed: "
                        f"{type(exc).__name__}: {exc}"
                    )

                try:
                    ats_result = calculate_ats_score(
                        resume_skills=skills,
                        job_skills=job_skills,
                        resume_text=text,
                        job_description=job_description,
                        candidate_experience=experience,
                        education=education,
                        projects=projects,
                    )

                    required_score_keys = [
                        "score",
                        "skill_score",
                        "keyword_score",
                        "experience_score",
                        "education_score",
                        "project_score",
                        "resume_quality_score",
                    ]

                    for key in required_score_keys:

                        value = ats_result.get(key)

                        if not valid_percentage(value):
                            add_failure(
                                failures,
                                f"ATS '{key}' invalid: {value}"
                            )

                    details["ats"] = ats_result.get(
                        "score"
                    )

                except Exception as exc:
                    add_failure(
                        failures,
                        f"ATS scorer crashed: "
                        f"{type(exc).__name__}: {exc}"
                    )

    # --------------------------------------------------------
    # Final status
    # --------------------------------------------------------

    status = "PASS" if not failures else "FAIL"

    return {
        "status": status,
        "failures": failures,
        "warnings": warnings,
        "details": details,
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 72)
    print("MULTI-RESUME GENERALIZATION REGRESSION TEST")
    print("=" * 72)

    # --------------------------------------------------------
    # 1. Role catalog
    # --------------------------------------------------------

    print()
    print("1. ROLE CATALOG VALIDATION")
    print("-" * 72)

    role_failures, role_warnings = test_role_catalog()

    print("Configured Roles:", len(JOB_ROLES))

    if role_failures:
        print("Role Catalog: FAIL")
        for item in role_failures:
            print("  ERROR:", item)
    else:
        print("Role Catalog: PASS")

    for item in role_warnings:
        print("  WARNING:", item)

    # --------------------------------------------------------
    # 2. Role reachability
    # --------------------------------------------------------

    print()
    print("2. ALL-ROLE REACHABILITY TEST")
    print("-" * 72)

    reach_failures, reach_warnings = test_all_roles_reachable()

    if reach_failures:
        print("Role Reachability: FAIL")
        for item in reach_failures:
            print("  ERROR:", item)
    else:
        print(
            f"Role Reachability: PASS "
            f"({len(JOB_ROLES)}/{len(JOB_ROLES)} roles reachable)"
        )

    for item in reach_warnings:
        print("  WARNING:", item)

    # --------------------------------------------------------
    # 3. Resume discovery
    # --------------------------------------------------------

    print()
    print("3. RESUME DISCOVERY")
    print("-" * 72)

    if not UPLOAD_DIR.exists():
        print("FAIL: uploads/ folder does not exist.")
        raise SystemExit(1)

    pdf_files = sorted(
        UPLOAD_DIR.glob("*.pdf")
    )

    print("PDF Resumes Found:", len(pdf_files))

    if not pdf_files:
        print("FAIL: No PDF resumes found in uploads/.")
        raise SystemExit(1)

    # --------------------------------------------------------
    # 4. Test every resume
    # --------------------------------------------------------

    print()
    print("4. RESUME PIPELINE TESTS")
    print("-" * 72)

    resume_results = []

    for pdf_path in pdf_files:

        result = test_resume(pdf_path)

        resume_results.append(
            (pdf_path, result)
        )

        details = result["details"]

        print()
        print(
            f"[{result['status']}] "
            f"{pdf_path.name}"
        )

        print(
            "  Skills:",
            details.get("skills", 0),
            "| Education:",
            details.get("education", 0),
            "| Experience:",
            details.get("experience", 0),
            "| Projects:",
            details.get("projects", 0),
        )

        if details.get("top_role"):
            print(
                "  Top Role:",
                details.get("top_role")
            )

        if "ats" in details:
            print(
                "  ATS:",
                details.get("ats"),
                "| Job Match:",
                details.get("job_match", 0),
            )

        for warning in result["warnings"]:
            print(
                "  WARNING:",
                warning
            )

        for failure in result["failures"]:
            print(
                "  ERROR:",
                failure
            )

    # --------------------------------------------------------
    # 5. Final summary
    # --------------------------------------------------------

    passed = sum(
        1
        for _, result in resume_results
        if result["status"] == "PASS"
    )

    failed = len(resume_results) - passed

    warning_count = sum(
        len(result["warnings"])
        for _, result in resume_results
    )

    global_failures = (
        len(role_failures)
        + len(reach_failures)
        + failed
    )

    print()
    print("=" * 72)
    print("FINAL REGRESSION SUMMARY")
    print("=" * 72)

    print("Configured IT Roles:", len(JOB_ROLES))
    print("Resumes Tested:", len(resume_results))
    print("Resume PASS:", passed)
    print("Resume FAIL:", failed)
    print("Warnings:", warning_count)

    print()
    print("Resume Results:")

    for pdf_path, result in resume_results:
        print(
            f"  {pdf_path.name}: "
            f"{result['status']}"
        )

    print()

    if global_failures == 0:

        print(
            "REGRESSION STATUS: PASS"
        )

        print(
            "All discovered resumes completed the pipeline, "
            "and all configured job roles are reachable."
        )

        raise SystemExit(0)

    else:

        print(
            "REGRESSION STATUS: FAIL"
        )

        print(
            "At least one resume or configured job role "
            "needs investigation."
        )

        raise SystemExit(1)


if __name__ == "__main__":
    main()
