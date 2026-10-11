# ============================================================
# RESUME IMPROVEMENT SUGGESTIONS
# AI Resume Screening & Job Recommendation System
# ============================================================


def _safe_float(
    value,
    default=None
):

    try:

        if value is None:
            return default

        return float(value)

    except (
        TypeError,
        ValueError
    ):

        return default


# ============================================================
# REMOVE DUPLICATE SUGGESTIONS
# ============================================================

def _unique_suggestions(
    suggestions
):

    unique = []

    seen = set()

    for suggestion in suggestions:

        suggestion = str(
            suggestion
        ).strip()

        if not suggestion:
            continue

        key = suggestion.lower()

        if key not in seen:

            seen.add(key)

            unique.append(
                suggestion
            )

    return unique


# ============================================================
# GENERATE SUGGESTIONS
# ============================================================

def generate_suggestions(
    ats_score,
    missing_skills=None,
    projects=None,
    experience=None,
    ats_result=None,
    recommended_roles=None,
    job_skills=None
):

    """
    Generate practical resume improvement suggestions.

    Existing calls using only:

        generate_suggestions(
            ats_score,
            missing_skills,
            projects,
            experience
        )

    will continue to work.

    Optional advanced inputs:

        ats_result
        recommended_roles
        job_skills
    """

    suggestions = []

    missing_skills = (
        missing_skills
        or []
    )

    projects = (
        projects
        or []
    )

    experience = (
        experience
        or {}
    )

    ats_result = (
        ats_result
        or {}
    )

    recommended_roles = (
        recommended_roles
        or []
    )

    job_skills = (
        job_skills
        or []
    )


    # ========================================================
    # ATS SCORE
    # ========================================================

    score = _safe_float(
        ats_score,
        0
    )

    if score < 50:

        suggestions.append(
            "Your ATS score is low. Focus on improving alignment with the job description, especially required skills and relevant keywords."
        )

    elif score < 75:

        suggestions.append(
            "Your ATS score is moderate. Improve the resume by adding more relevant skills, keywords and evidence of practical work related to the job."
        )

    elif score < 90:

        suggestions.append(
            "Your ATS score is good, but there is still room to improve job-specific keywords, skills or project relevance."
        )


    # ========================================================
    # COMPONENT SCORES
    # ========================================================

    skill_score = _safe_float(
        ats_result.get(
            "skill_score"
        )
    )

    keyword_score = _safe_float(
        ats_result.get(
            "keyword_score"
        )
    )

    experience_score = _safe_float(
        ats_result.get(
            "experience_score"
        )
    )

    education_score = _safe_float(
        ats_result.get(
            "education_score"
        )
    )

    project_score = _safe_float(
        ats_result.get(
            "project_score"
        )
    )

    resume_quality_score = _safe_float(
        ats_result.get(
            "resume_quality_score"
        )
    )


    # ========================================================
    # SKILLS
    # ========================================================

    if missing_skills:

        skills_text = ", ".join(
            str(skill)
            for skill in missing_skills[:8]
        )

        suggestions.append(
            "Consider developing these job-required skills where relevant: "
            + skills_text
            + "."
        )

    elif (
        skill_score is not None
        and skill_score >= 90
    ):

        # Strong skill match.
        # No unnecessary negative suggestion.
        pass


    if (
        skill_score is not None
        and skill_score < 60
    ):

        suggestions.append(
            "Your skill match with this job is relatively low. Prioritize the most important skills mentioned in the job description."
        )


    # ========================================================
    # KEYWORDS
    # ========================================================

    if (
        keyword_score is not None
        and keyword_score < 50
    ):

        suggestions.append(
            "The resume has low keyword alignment with the job description. Use important job-related terminology where it accurately represents your experience."
        )

    elif (
        keyword_score is not None
        and keyword_score < 70
    ):

        suggestions.append(
            "Improve keyword alignment by using more relevant terminology from the job description where it truthfully matches your skills and work."
        )


    # ========================================================
    # PROJECTS
    # ========================================================

    if len(projects) == 0:

        suggestions.append(
            "Add at least one academic, personal or professional project that demonstrates skills relevant to the target job."
        )

    else:

        if (
            project_score is not None
            and project_score == 0
        ):

            if job_skills:

                job_skill_text = ", ".join(
                    str(skill)
                    for skill in job_skills[:5]
                )

                suggestions.append(
                    "You have projects, but they do not currently demonstrate the required job skills such as "
                    + job_skill_text
                    + ". Mention these technologies in project descriptions only if they were genuinely used."
                )

            else:

                suggestions.append(
                    "You have projects, but they show little alignment with the skills required by this job. Strengthen project descriptions with relevant technologies and outcomes where accurate."
                )

        elif (
            project_score is not None
            and project_score < 50
        ):

            suggestions.append(
                "Your projects only partially match the job requirements. Highlight relevant technologies, responsibilities and measurable outcomes more clearly."
            )

        elif (
            project_score is None
            and len(projects) < 2
        ):

            suggestions.append(
                "Consider adding another relevant project to strengthen your practical profile."
            )


    # ========================================================
    # EXPERIENCE
    # ========================================================

    total_experience = _safe_float(
        experience.get(
            "total_years"
        ),
        0
    )

    if total_experience == 0:

        # Do not penalize a fresher when the ATS already
        # considers zero experience acceptable.

        if (
            experience_score is None
            or experience_score < 100
        ):

            suggestions.append(
                "Build practical experience through internships, freelance work, open-source contributions or substantial personal projects."
            )

    elif (
        experience_score is not None
        and experience_score < 70
    ):

        suggestions.append(
            "Your experience is below the level requested in the job description. Emphasize the most relevant responsibilities, achievements and transferable experience."
        )


    # ========================================================
    # EDUCATION
    # ========================================================

    if (
        education_score is not None
        and education_score < 50
    ):

        suggestions.append(
            "The education requirement does not strongly match this job. Emphasize relevant coursework, certifications and practical skills without misrepresenting your qualification."
        )


    # ========================================================
    # RESUME QUALITY
    # ========================================================

    if (
        resume_quality_score is not None
        and resume_quality_score < 60
    ):

        suggestions.append(
            "Improve resume structure by clearly separating sections such as Summary, Skills, Education, Experience and Projects."
        )


    # ========================================================
    # TOP RECOMMENDED ROLE
    # ========================================================

    if recommended_roles:

        top_role = recommended_roles[0]

        if isinstance(
            top_role,
            dict
        ):

            role_name = (
                top_role.get(
                    "role"
                )
                or top_role.get(
                    "job_role"
                )
                or top_role.get(
                    "title"
                )
            )

            role_missing = (
                top_role.get(
                    "missing_skills"
                )
                or []
            )

            if (
                role_name
                and role_missing
            ):

                role_skill_text = ", ".join(
                    str(skill)
                    for skill in role_missing[:5]
                )

                suggestions.append(
                    "For the recommended "
                    + str(role_name)
                    + " role, consider strengthening: "
                    + role_skill_text
                    + "."
                )


    # ========================================================
    # DEFAULT
    # ========================================================

    suggestions = _unique_suggestions(
        suggestions
    )

    if not suggestions:

        suggestions.append(
            "Your resume is strongly aligned with this job. Continue keeping skills, experience and projects specific, measurable and relevant."
        )


    # Avoid an excessively long result page.

    return suggestions[:10]