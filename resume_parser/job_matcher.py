from resume_parser.master_skills import normalize_skill
# =========================================================
# ANALYZE JOB MATCH
# =========================================================
def analyze_job_match(
    resume_skills,
    job_skills,
    master_skills=None
):

    """
    Compare resume skills against already extracted
    job-description skills.

    Parameters
    ----------
    resume_skills : list
        Skills extracted from the resume.

    job_skills : list
        Skills extracted from the job description.

    master_skills : list, optional
        Master skill list. Kept for compatibility with
        older versions of the project.
    """

    # =====================================================
    # VALIDATION
    # =====================================================

    if resume_skills is None:
        resume_skills = []

    if job_skills is None:
        job_skills = []

    # =====================================================
    # NORMALIZE RESUME SKILLS
    # =====================================================

    resume_normalized = set()

    for skill in resume_skills:

        if not skill:
            continue

        normalized = normalize_skill(skill)

        if normalized:

            resume_normalized.add(
                normalized.strip().lower()
            )

    # =====================================================
    # NORMALIZE JOB SKILLS
    # =====================================================

    job_normalized = []

    seen = set()

    for skill in job_skills:

        if not skill:
            continue

        normalized = normalize_skill(skill)

        if not normalized:
            continue

        normalized_lower = (
            normalized.strip().lower()
        )

        if normalized_lower not in seen:

            seen.add(
                normalized_lower
            )

            job_normalized.append(
                normalized_lower
            )

    # =====================================================
    # EMPTY JOB SKILLS
    # =====================================================

    if not job_normalized:

        return {
            "match_score": 0,
            "match_category": "Low Match",
            "matching_skills": [],
            "missing_skills": [],
            "high_priority_missing": [],
            "total_job_skills": 0,
            "matched_count": 0,
        }

    # =====================================================
    # MATCHING / MISSING
    # =====================================================

    matching_skills = []
    missing_skills = []

    for skill in job_normalized:

        if skill in resume_normalized:

            matching_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )

    # =====================================================
    # MATCH SCORE
    # =====================================================

    total_job_skills = len(
        job_normalized
    )

    matched_count = len(
        matching_skills
    )

    match_score = (
        matched_count
        /
        total_job_skills
    ) * 100

    match_score = round(
        match_score,
        2
    )

    # =====================================================
    # MATCH CATEGORY
    # =====================================================

    if match_score >= 80:

        match_category = "Strong Match"

    elif match_score >= 60:

        match_category = "Good Match"

    elif match_score >= 40:

        match_category = "Moderate Match"

    else:

        match_category = "Low Match"

    # =====================================================
    # HIGH PRIORITY MISSING SKILLS
    # =====================================================

    high_priority_keywords = {

        "artificial intelligence",
        "machine learning",
        "deep learning",
        "python",
        "nlp",
        "computer vision",
        "generative ai",
        "pytorch",
        "tensorflow",
        "scikit-learn",
        "data preprocessing",
        "feature engineering",
    }

    high_priority_missing = []

    for skill in missing_skills:

        if skill in high_priority_keywords:

            high_priority_missing.append(
                skill
            )

    # =====================================================
    # SORT
    # =====================================================

    matching_skills.sort()

    missing_skills.sort()

    high_priority_missing.sort()

    # =====================================================
    # RETURN
    # =====================================================

    return {

        "match_score":
            match_score,

        "match_category":
            match_category,

        "matching_skills":
            matching_skills,

        "missing_skills":
            missing_skills,

        "high_priority_missing":
            high_priority_missing,

        "total_job_skills":
            total_job_skills,

        "matched_count":
            matched_count,
    }