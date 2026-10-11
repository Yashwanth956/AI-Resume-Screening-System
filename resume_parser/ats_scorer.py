import re

from resume_parser.master_skills import normalize_skill
from resume_parser.keyword_matcher import calculate_keyword_score


# =========================================================
# SKILL HELPERS
# =========================================================

def _normalize_one_skill(skill):
    if skill is None:
        return ""

    try:
        standard_skill = normalize_skill(skill)
    except Exception:
        standard_skill = skill

    if not standard_skill:
        return ""

    return str(standard_skill).strip()


def normalize_skill_list(skills):
    """Convert a skill list into a normalized lowercase set."""

    normalized = set()

    if not skills:
        return normalized

    for skill in skills:
        standard_skill = _normalize_one_skill(skill)

        if standard_skill:
            normalized.add(standard_skill.lower())

    return normalized


# =========================================================
# SKILL SCORE
# =========================================================

def calculate_skill_score(resume_skills, job_skills):
    resume_normalized = normalize_skill_list(resume_skills)
    job_normalized = normalize_skill_list(job_skills)

    if not job_normalized:
        return 0

    matching = resume_normalized.intersection(job_normalized)

    score = (len(matching) / len(job_normalized)) * 100

    return round(score, 2)


# =========================================================
# MATCHING / MISSING SKILLS
# =========================================================

def get_matching_skills(resume_skills, job_skills):
    resume_normalized = normalize_skill_list(resume_skills)
    matching = []

    for skill in job_skills or []:
        normalized = _normalize_one_skill(skill)

        if not normalized:
            continue

        if normalized.lower() in resume_normalized:
            if normalized not in matching:
                matching.append(normalized)

    return matching


def get_missing_skills(resume_skills, job_skills):
    resume_normalized = normalize_skill_list(resume_skills)
    missing = []

    for skill in job_skills or []:
        normalized = _normalize_one_skill(skill)

        if not normalized:
            continue

        if normalized.lower() not in resume_normalized:
            if normalized not in missing:
                missing.append(normalized)

    return missing


# =========================================================
# EXPERIENCE REQUIREMENT EXTRACTION
# =========================================================

def _clean_jd_text(job_description):
    if not job_description:
        return ""

    text = str(job_description)
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_experience_requirement(job_description):
    """
    Return a structured experience requirement.

    Examples:
        0-2 years       -> min=0, max=2
        2 to 4 years    -> min=2, max=4
        3+ years        -> min=3, max=None
        at least 2      -> min=2, max=None
        up to 2 years   -> min=0, max=2
        fresher          -> min=0, max=1
        entry level      -> min=0, max=2
    """

    text = _clean_jd_text(job_description)

    result = {
        "min_years": 0.0,
        "max_years": None,
        "has_requirement": False,
        "requirement_type": "none",
        "matched_text": "",
    }

    if not text:
        return result

    # "No experience required" means experience should not
    # penalize either a fresher or an experienced candidate.
    if re.search(
        r"\b(?:no|zero)\s+(?:prior\s+|professional\s+|work\s+)?experience\s+(?:is\s+)?required\b",
        text,
        flags=re.IGNORECASE,
    ):
        result["requirement_type"] = "none_required"
        return result

    # -----------------------------------------------------
    # RANGE FIRST
    # 0-2 years
    # 2 to 4 years
    # -----------------------------------------------------

    match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\b",
        text,
        flags=re.IGNORECASE,
    )

    if match:
        minimum = float(match.group(1))
        maximum = float(match.group(2))

        if maximum < minimum:
            minimum, maximum = maximum, minimum

        return {
            "min_years": minimum,
            "max_years": maximum,
            "has_requirement": True,
            "requirement_type": "range",
            "matched_text": match.group(0),
        }

    # -----------------------------------------------------
    # 3+ years
    # -----------------------------------------------------

    match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*\+\s*(?:years?|yrs?)\b",
        text,
        flags=re.IGNORECASE,
    )

    if match:
        return {
            "min_years": float(match.group(1)),
            "max_years": None,
            "has_requirement": True,
            "requirement_type": "minimum",
            "matched_text": match.group(0),
        }

    # -----------------------------------------------------
    # minimum / at least
    # -----------------------------------------------------

    match = re.search(
        r"\b(?:minimum(?:\s+of)?|at\s+least)\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\b",
        text,
        flags=re.IGNORECASE,
    )

    if match:
        return {
            "min_years": float(match.group(1)),
            "max_years": None,
            "has_requirement": True,
            "requirement_type": "minimum",
            "matched_text": match.group(0),
        }

    # -----------------------------------------------------
    # up to / maximum
    # -----------------------------------------------------

    match = re.search(
        r"\b(?:up\s+to|maximum(?:\s+of)?|max(?:imum)?\.?)\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\b",
        text,
        flags=re.IGNORECASE,
    )

    if match:
        return {
            "min_years": 0.0,
            "max_years": float(match.group(1)),
            "has_requirement": True,
            "requirement_type": "maximum",
            "matched_text": match.group(0),
        }

    # -----------------------------------------------------
    # Exact/minimum-like wording
    # "2 years of experience"
    # "experience: 2 years"
    # -----------------------------------------------------

    exact_patterns = [
        r"\b(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s+(?:of\s+)?experience\b",
        r"\bexperience\s*(?::|-)?\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\b",
        r"\bexperience\s+of\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\b",
    ]

    for pattern in exact_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)

        if match:
            return {
                "min_years": float(match.group(1)),
                "max_years": None,
                "has_requirement": True,
                "requirement_type": "minimum",
                "matched_text": match.group(0),
            }

    # -----------------------------------------------------
    # Text-only entry-level wording
    # -----------------------------------------------------

    if re.search(r"\bfreshers?\b", text, flags=re.IGNORECASE):
        return {
            "min_years": 0.0,
            "max_years": 1.0,
            "has_requirement": True,
            "requirement_type": "fresher",
            "matched_text": "fresher",
        }

    if re.search(r"\bentry[- ]level\b", text, flags=re.IGNORECASE):
        return {
            "min_years": 0.0,
            "max_years": 2.0,
            "has_requirement": True,
            "requirement_type": "entry_level",
            "matched_text": "entry level",
        }

    return result


def extract_required_experience(job_description):
    """
    Backward-compatible helper.

    Returns the minimum required years. New scoring should use
    extract_experience_requirement() so that ranges such as 0-2
    years are not confused with "no requirement".
    """

    requirement = extract_experience_requirement(job_description)
    return float(requirement.get("min_years", 0.0))


# =========================================================
# EXPERIENCE SCORE
# =========================================================

def _candidate_years(candidate_experience):
    if not candidate_experience:
        return 0.0

    try:
        return max(
            0.0,
            float(candidate_experience.get("total_years", 0) or 0),
        )
    except (TypeError, ValueError, AttributeError):
        return 0.0


def calculate_experience_score(candidate_experience, job_description):
    """
    Range-aware experience compatibility.

    Rules:
      - If JD has no experience requirement: 100 for everyone.
      - Candidate inside a stated range: 100.
      - Candidate below minimum: proportional score.
      - Candidate above a stated maximum: gradual penalty,
        never lower than 50 solely for being over-experienced.
      - Minimum-only requirements such as 3+ years do not
        penalize additional experience.
    """

    if not job_description:
        return 0

    requirement = extract_experience_requirement(job_description)
    candidate_years = _candidate_years(candidate_experience)

    if not requirement["has_requirement"]:
        return 100

    minimum = float(requirement.get("min_years", 0.0) or 0.0)
    maximum = requirement.get("max_years")

    if maximum is not None:
        maximum = float(maximum)

        # Perfect range match, including fresher 0 years in 0-2.
        if minimum <= candidate_years <= maximum:
            return 100

        # Below the lower bound.
        if candidate_years < minimum:
            if minimum <= 0:
                return 100

            score = (candidate_years / minimum) * 100
            return round(max(0, min(score, 100)), 2)

        # Above the upper bound.
        # Penalize gently because extra experience is not the
        # same as lacking a required qualification.
        excess_years = candidate_years - maximum
        score = 100 - (excess_years * 15)

        return round(max(50, min(score, 100)), 2)

    # Minimum-only requirement, e.g. 3+ years.
    if candidate_years >= minimum:
        return 100

    if minimum <= 0:
        return 100

    score = (candidate_years / minimum) * 100
    return round(max(0, min(score, 100)), 2)


# =========================================================
# EDUCATION
# =========================================================

# =========================================================
# EDUCATION SCORE
# =========================================================

def calculate_education_score(
    education,
    job_description
):

    """
    Compare candidate education with the education
    requirement mentioned in the job description.

    Supports:
        Bachelor's degree
        Master's degree
        Bachelor's or Master's degree
        B.Tech / B.E
        B.Sc / BCA
        M.Tech / MCA / M.Sc
        PhD
        equivalent practical experience
    """

    # =====================================================
    # BASIC VALIDATION
    # =====================================================

    if not job_description:
        return 0

    if not education:
        return 0

    # =====================================================
    # BUILD EDUCATION TEXT
    #
    # This is intentionally inside this function so
    # build_education_text() is NOT required.
    # =====================================================

    education_parts = []

    if isinstance(
        education,
        list
    ):

        for item in education:

            if isinstance(
                item,
                dict
            ):

                for value in item.values():

                    if value:

                        education_parts.append(
                            str(value)
                        )

            elif item:

                education_parts.append(
                    str(item)
                )

    elif isinstance(
        education,
        dict
    ):

        for value in education.values():

            if value:

                education_parts.append(
                    str(value)
                )

    else:

        education_parts.append(
            str(education)
        )

    education_text = (
        " ".join(
            education_parts
        )
        .lower()
        .replace("\u2019", "'")
        .replace("\u2018", "'")
    )

    jd = (
        str(
            job_description
        )
        .lower()
        .replace("\u2019", "'")
        .replace("\u2018", "'")
    )

    # =====================================================
    # DETECT CANDIDATE DEGREE LEVEL
    #
    # 0 = Unknown
    # 1 = Bachelor's
    # 2 = Master's
    # 3 = PhD
    # =====================================================

    candidate_level = 0

    # -----------------------------------------------------
    # PhD
    # -----------------------------------------------------

    phd_patterns = [

        r"\bph\.?\s*d\.?\b",

        r"\bphd\b",

        r"\bdoctorate\b",

        r"\bdoctoral\b",
    ]

    if any(
        re.search(
            pattern,
            education_text,
            re.IGNORECASE
        )
        for pattern in phd_patterns
    ):

        candidate_level = 3

    # -----------------------------------------------------
    # Master's
    # -----------------------------------------------------

    if candidate_level == 0:

        master_patterns = [

            r"\bmaster(?:'s)?\b",

            r"\bmaster of technology\b",

            r"\bmaster of engineering\b",

            r"\bmaster of science\b",

            r"\bm\.?\s*tech\b",

            r"\bmtech\b",

            r"\bm\.?\s*e\.?\b",

            r"\bm\.?\s*sc\.?\b",

            r"\bmsc\b",

            r"\bmca\b",

            r"\bmba\b",
        ]

        if any(
            re.search(
                pattern,
                education_text,
                re.IGNORECASE
            )
            for pattern in master_patterns
        ):

            candidate_level = 2

    # -----------------------------------------------------
    # Bachelor's
    # -----------------------------------------------------

    if candidate_level == 0:

        bachelor_patterns = [

            r"\bbachelor(?:'s)?\b",

            r"\bbachelor of technology\b",

            r"\bbachelor of engineering\b",

            r"\bbachelor of science\b",

            r"\bbachelor of computer applications\b",

            r"\bb\.?\s*tech\b",

            r"\bbtech\b",

            r"\bb\.?\s*e\.?\b",

            r"\bb\.?\s*sc\.?\b",

            r"\bbsc\b",

            r"\bbca\b",

            r"\bbba\b",

            r"\bb\.?\s*com\b",

            r"\bbcom\b",
        ]

        if any(
            re.search(
                pattern,
                education_text,
                re.IGNORECASE
            )
            for pattern in bachelor_patterns
        ):

            candidate_level = 1

    # =====================================================
    # DETECT JD EDUCATION REQUIREMENT
    # =====================================================

    jd_has_bachelor = bool(
        re.search(
            r"\bbachelor(?:'s)?\b",
            jd,
            re.IGNORECASE
        )
    )

    jd_has_master = bool(
        re.search(
            r"\bmaster(?:'s)?\b",
            jd,
            re.IGNORECASE
        )
    )

    jd_has_phd = bool(
        re.search(
            r"\b(?:ph\.?\s*d\.?|phd|doctorate|doctoral)\b",
            jd,
            re.IGNORECASE
        )
    )

    # =====================================================
    # BACHELOR'S OR MASTER'S
    #
    # Example:
    #
    # "Bachelor's or Master's degree"
    #
    # Bachelor's is enough.
    # =====================================================

    bachelor_or_master = bool(
        re.search(
            r"\bbachelor(?:'s)?\b"
            r".{0,30}"
            r"\bor\b"
            r".{0,30}"
            r"\bmaster(?:'s)?\b",
            jd,
            re.IGNORECASE
        )
    )

    if bachelor_or_master:

        if candidate_level >= 1:
            return 100

        return 0

    # =====================================================
    # BACHELOR'S REQUIREMENT
    # =====================================================

    if jd_has_bachelor:

        if candidate_level >= 1:
            return 100

        return 0

    # =====================================================
    # MASTER'S REQUIREMENT
    # =====================================================

    if jd_has_master:

        if candidate_level >= 2:
            return 100

        # Bachelor's candidate for Master's-only role.
        if candidate_level == 1:
            return 50

        return 0

    # =====================================================
    # PhD REQUIREMENT
    # =====================================================

    if jd_has_phd:

        if candidate_level >= 3:
            return 100

        if candidate_level == 2:
            return 50

        return 0

    # =====================================================
    # JD MAY SAY "DEGREE" WITHOUT LEVEL
    # =====================================================

    if re.search(
        r"\bdegree\b",
        jd,
        re.IGNORECASE
    ):

        if candidate_level >= 1:
            return 100

        return 0

    # =====================================================
    # NO EDUCATION REQUIREMENT
    # =====================================================

    return 100
# =========================================================
# PROJECT HELPERS
# =========================================================

def _project_field(project, primary, fallback):
    if not isinstance(project, dict):
        return None

    value = project.get(primary)

    if value in (None, "", []):
        value = project.get(fallback)

    return value


def build_project_text(projects):
    """
    Supports BOTH project schemas:

        New/current parser:
        {
            "title": "...",
            "technologies": [...],
            "description": [...]
        }

        Older parser:
        {
            "name": "...",
            "tech_stack": [...],
            "description": [...]
        }
    """

    if not projects:
        return ""

    parts = []

    if isinstance(projects, list):
        iterable = projects
    elif isinstance(projects, dict):
        iterable = [projects]
    else:
        iterable = [projects]

    for project in iterable:
        if not isinstance(project, dict):
            if project:
                parts.append(str(project))
            continue

        title = _project_field(project, "title", "name")
        technologies = _project_field(project, "technologies", "tech_stack")
        description = project.get("description", [])

        if title:
            parts.append(str(title))

        if isinstance(technologies, (list, tuple, set)):
            parts.extend(str(item) for item in technologies if item)
        elif technologies:
            parts.append(str(technologies))

        if isinstance(description, (list, tuple, set)):
            parts.extend(str(item) for item in description if item)
        elif description:
            parts.append(str(description))

    return " ".join(parts).lower()


def extract_project_skills(projects):
    skills = []

    if not projects:
        return skills

    if isinstance(projects, list):
        iterable = projects
    elif isinstance(projects, dict):
        iterable = [projects]
    else:
        return skills

    for project in iterable:
        if not isinstance(project, dict):
            continue

        technologies = _project_field(project, "technologies", "tech_stack")

        if isinstance(technologies, (list, tuple, set)):
            skills.extend(item for item in technologies if item)
        elif technologies:
            skills.append(technologies)

    return skills


def _text_contains_skill(text, skill):
    if not text or not skill:
        return False

    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(skill.lower())
        + r"(?![a-z0-9])"
    )

    return bool(re.search(pattern, text.lower()))


def get_project_matching_skills(projects, job_skills):
    if not projects or not job_skills:
        return []

    project_text = build_project_text(projects)
    project_skill_set = normalize_skill_list(extract_project_skills(projects))

    matching = []

    for skill in job_skills:
        normalized = _normalize_one_skill(skill)

        if not normalized:
            continue

        key = normalized.lower()

        if (
            key in project_skill_set
            or _text_contains_skill(project_text, key)
        ):
            if normalized not in matching:
                matching.append(normalized)

    return matching


# =========================================================
# PROJECT SCORE
# =========================================================

def calculate_project_score(projects, job_skills):
    if not projects:
        return 0

    job_normalized = normalize_skill_list(job_skills)

    if not job_normalized:
        return 50

    matching = get_project_matching_skills(projects, job_skills)

    score = (len(matching) / len(job_normalized)) * 100

    return round(score, 2)


# =========================================================
# RESUME QUALITY SCORE
# =========================================================

def calculate_resume_quality_score(resume_text, candidate_experience=None):
    """
    Fresher-aware and experienced-candidate-aware quality score.

    Fresher:
        education + skills + summary/profile + projects

    Experienced candidate:
        education + skills + summary/profile + experience
    """

    if not resume_text:
        return 0

    text = str(resume_text).lower()
    candidate_years = _candidate_years(candidate_experience)

    checks = [
        any(term in text for term in ("education", "academic qualification")),
        any(term in text for term in ("technical skills", "skills", "skill set")),
        any(term in text for term in ("professional summary", "summary", "profile", "objective")),
    ]

    if candidate_years > 0:
        checks.append(
            any(
                term in text
                for term in (
                    "professional experience",
                    "work experience",
                    "employment history",
                    "experience",
                )
            )
        )
    else:
        checks.append(
            any(
                term in text
                for term in (
                    "projects",
                    "project",
                    "academic projects",
                )
            )
        )

    score = (sum(1 for item in checks if item) / len(checks)) * 100

    return round(score, 2)


# =========================================================
# KEYWORD SCORE
# =========================================================

def safe_keyword_score(resume_text, job_description):
    if not resume_text or not job_description:
        return 0

    try:
        score = calculate_keyword_score(resume_text, job_description)
        return round(float(score), 2)
    except Exception as e:
        print("Keyword score error:", e)
        return 0


# =========================================================
# FINAL ATS SCORE
# =========================================================

def calculate_ats_score(
    resume_skills,
    job_skills,
    resume_text="",
    job_description="",
    candidate_experience=None,
    education=None,
    projects=None,
):
    """
    Weighting:
        Skills          = 40%
        Keywords        = 20%
        Experience      = 15%
        Education       = 10%
        Projects        = 10%
        Resume Quality  = 5%
    """

    # -----------------------------------------------------
    # Skills
    # -----------------------------------------------------

    skill_score = calculate_skill_score(resume_skills, job_skills)
    matching_skills = get_matching_skills(resume_skills, job_skills)
    missing_skills = get_missing_skills(resume_skills, job_skills)

    # -----------------------------------------------------
    # Keywords
    # -----------------------------------------------------

    keyword_score = safe_keyword_score(resume_text, job_description)

    # -----------------------------------------------------
    # Experience
    # -----------------------------------------------------

    experience_requirement = extract_experience_requirement(job_description)
    experience_score = calculate_experience_score(
        candidate_experience,
        job_description,
    )

    # -----------------------------------------------------
    # Education
    # -----------------------------------------------------

    education_score = calculate_education_score(
        education,
        job_description,
    )

    # -----------------------------------------------------
    # Projects
    # -----------------------------------------------------

    project_matching_skills = get_project_matching_skills(
        projects,
        job_skills,
    )

    project_score = calculate_project_score(
        projects,
        job_skills,
    )

    # -----------------------------------------------------
    # Resume quality
    # -----------------------------------------------------

    resume_quality_score = calculate_resume_quality_score(
        resume_text,
        candidate_experience,
    )

    # -----------------------------------------------------
    # Final score
    # -----------------------------------------------------

    final_score = (
        skill_score * 0.40
        + keyword_score * 0.20
        + experience_score * 0.15
        + education_score * 0.10
        + project_score * 0.10
        + resume_quality_score * 0.05
    )

    final_score = round(
        min(max(final_score, 0), 100),
        2,
    )

    # -----------------------------------------------------
    # Debug
    # -----------------------------------------------------

    print("\n========== ATS SCORE BREAKDOWN ==========")
    print("Skill Score:", skill_score)
    print("Keyword Score:", keyword_score)
    print("Experience Score:", experience_score)
    print("Experience Requirement:", experience_requirement)
    print("Education Score:", education_score)
    print("Project Score:", project_score)
    print("Project Matching Skills:", project_matching_skills)
    print("Resume Quality Score:", resume_quality_score)
    print("-----------------------------------------")
    print("FINAL ATS SCORE:", final_score)
    print("=========================================")

    return {
        "score": final_score,
        "skill_score": skill_score,
        "keyword_score": keyword_score,
        "experience_score": experience_score,
        "education_score": education_score,
        "project_score": project_score,
        "resume_quality_score": resume_quality_score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "project_matching_skills": project_matching_skills,
        "experience_requirement": experience_requirement,
    }