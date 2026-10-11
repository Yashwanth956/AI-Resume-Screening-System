# =========================================================
# resume_parser/jd_skill_extractor.py
# JOB DESCRIPTION SKILL EXTRACTOR
# =========================================================

import re

from resume_parser.master_skills import (
    ALL_SKILLS,
    normalize_skill
)


# =========================================================
# SECTION HEADINGS
# =========================================================

REQUIRED_HEADINGS = (
    "required skills",
    "required skill",
    "must have skills",
    "must-have skills",
    "mandatory skills",
    "core skills",
)

PREFERRED_HEADINGS = (
    "preferred skills",
    "preferred skill",
    "good to have",
    "good-to-have",
    "nice to have",
    "nice-to-have",
    "desirable skills",
)

STOP_HEADINGS = (
    "qualifications",
    "qualification",
    "education",
    "education requirements",
    "key responsibilities",
    "responsibilities",
    "role overview",
    "job responsibilities",
    "employment type",
    "experience",
    "about the role",
    "role description",
    "job description",
)


# =========================================================
# UNIQUE NORMALIZED SKILLS
# =========================================================

def unique_normalized_skills(skills):

    result = []
    seen = set()

    for skill in skills or []:

        normalized = normalize_skill(
            skill
        )

        if not normalized:
            continue

        normalized = (
            normalized
            .strip()
        )

        key = normalized.lower()

        if key not in seen:

            seen.add(
                key
            )

            result.append(
                normalized
            )

    return result


# =========================================================
# PREPARE JD TEXT
#
# Important:
# User may paste JD as:
#
# Required Skills: Python, SQL ...
# Preferred Skills: Docker, AWS ...
#
# all on one line.
#
# This function forces known headings onto new lines.
# =========================================================

def prepare_jd_text(job_description):

    if not job_description:
        return ""

    text = str(
        job_description
    )

    text = text.replace(
        "\r\n",
        "\n"
    )

    text = text.replace(
        "\r",
        "\n"
    )

    # -----------------------------------------------------
    # Put important headings on separate lines.
    # -----------------------------------------------------

    headings = list(
        REQUIRED_HEADINGS
    ) + list(
        PREFERRED_HEADINGS
    ) + list(
        STOP_HEADINGS
    )

    headings = sorted(
        headings,
        key=len,
        reverse=True
    )

    for heading in headings:

        pattern = (
            r"(?i)"
            r"(?<!\n)"
            r"(?<!^)"
            r"\s+"
            + re.escape(heading)
            + r"\s*:"
        )

        text = re.sub(
            pattern,
            "\n"
            + heading.title()
            + ":",
            text
        )

    # Normalize spaces without destroying lines.
    lines = []

    for line in text.splitlines():

        line = re.sub(
            r"[ \t]+",
            " ",
            line
        ).strip()

        if line:
            lines.append(
                line
            )

    return "\n".join(
        lines
    )


# =========================================================
# NORMALIZE HEADING
# =========================================================

def normalize_heading(line):

    if not line:
        return ""

    value = str(
        line
    ).strip().lower()

    # Keep only heading part before colon.
    if ":" in value:

        value = value.split(
            ":",
            1
        )[0]

    value = re.sub(
        r"[^a-z0-9 -]+",
        " ",
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


# =========================================================
# CHECK HEADING TYPE
# =========================================================

def is_required_heading(line):

    heading = normalize_heading(
        line
    )

    return heading in REQUIRED_HEADINGS


def is_preferred_heading(line):

    heading = normalize_heading(
        line
    )

    return heading in PREFERRED_HEADINGS


def is_stop_heading(line):

    heading = normalize_heading(
        line
    )

    return (
        heading in STOP_HEADINGS
        or heading in REQUIRED_HEADINGS
        or heading in PREFERRED_HEADINGS
    )


# =========================================================
# EXTRACT SECTION BODY
# =========================================================

def extract_section_text(
    job_description,
    target="required"
):

    text = prepare_jd_text(
        job_description
    )

    if not text:
        return ""

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    collecting = False
    result = []

    for line in lines:

        if target == "required":

            if is_required_heading(
                line
            ):

                collecting = True

                # Handle:
                #
                # Required Skills: Python, SQL
                if ":" in line:

                    after = line.split(
                        ":",
                        1
                    )[1].strip()

                    if after:
                        result.append(
                            after
                        )

                continue

        elif target == "preferred":

            if is_preferred_heading(
                line
            ):

                collecting = True

                if ":" in line:

                    after = line.split(
                        ":",
                        1
                    )[1].strip()

                    if after:
                        result.append(
                            after
                        )

                continue

        if collecting:

            # Stop at another known section.
            if is_stop_heading(
                line
            ):

                break

            result.append(
                line
            )

    return "\n".join(
        result
    ).strip()


# =========================================================
# EXTRACT SKILLS FROM TEXT
# =========================================================

def extract_skills_from_text(text):

    if not text:
        return []

    text_lower = str(
        text
    ).lower()

    extracted = []

    # -----------------------------------------------------
    # Important:
    #
    # Search BOTH:
    #
    # 1. raw value from ALL_SKILLS
    # 2. canonical normalized value
    #
    # This helps with aliases such as:
    #
    # REST APIs -> REST API
    # scikit learn -> Scikit-learn
    # ML -> Machine Learning
    # -----------------------------------------------------

    for raw_skill in ALL_SKILLS:

        if not raw_skill:
            continue

        canonical_skill = normalize_skill(
            raw_skill
        )

        if not canonical_skill:
            continue

        search_values = [
            str(
                raw_skill
            ).strip(),

            str(
                canonical_skill
            ).strip(),
        ]

        found = False

        for search_value in search_values:

            if not search_value:
                continue

            skill_lower = (
                search_value
                .lower()
            )

            pattern = (
                r"(?<![a-zA-Z0-9])"
                + re.escape(
                    skill_lower
                )
                + r"(?![a-zA-Z0-9])"
            )

            if re.search(
                pattern,
                text_lower
            ):

                found = True
                break

        if found:

            extracted.append(
                canonical_skill
            )

    result = unique_normalized_skills(
        extracted
    )

    result.sort(
        key=lambda item:
            item.lower()
    )

    return result


# =========================================================
# JD SKILL ANALYSIS
# =========================================================

def analyze_jd_skills(
    job_description
):

    if not job_description:

        return {
            "required_skills": [],
            "preferred_skills": [],
            "all_skills": [],
            "required_section_found": False,
            "preferred_section_found": False,
        }

    prepared = prepare_jd_text(
        job_description
    )

    required_text = extract_section_text(
        prepared,
        target="required"
    )

    preferred_text = extract_section_text(
        prepared,
        target="preferred"
    )

    required_section_found = bool(
        required_text
    )

    preferred_section_found = bool(
        preferred_text
    )

    # =====================================================
    # REQUIRED SKILLS
    # =====================================================

    if required_section_found:

        required_skills = (
            extract_skills_from_text(
                required_text
            )
        )

    else:

        # -------------------------------------------------
        # Fallback for older/simple JDs without headings.
        #
        # Example:
        #
        # "Looking for Python developer with SQL,
        # Flask and Git."
        #
        # In this case use entire JD.
        # -------------------------------------------------

        required_skills = (
            extract_skills_from_text(
                prepared
            )
        )

    # =====================================================
    # PREFERRED SKILLS
    # =====================================================

    preferred_skills = (
        extract_skills_from_text(
            preferred_text
        )
        if preferred_section_found
        else []
    )

    # -----------------------------------------------------
    # If the same skill appears in Required and Preferred,
    # keep it only in Required.
    # -----------------------------------------------------

    required_keys = {
        skill.lower()
        for skill in required_skills
    }

    preferred_skills = [
        skill
        for skill in preferred_skills
        if skill.lower()
        not in required_keys
    ]

    # =====================================================
    # ALL JD SKILLS
    # =====================================================

    all_skills = unique_normalized_skills(
        required_skills
        + preferred_skills
    )

    all_skills.sort(
        key=lambda item:
            item.lower()
    )

    return {

        "required_skills":
            required_skills,

        "preferred_skills":
            preferred_skills,

        "all_skills":
            all_skills,

        "required_section_found":
            required_section_found,

        "preferred_section_found":
            preferred_section_found,
    }


# =========================================================
# MAIN FUNCTION
#
# IMPORTANT:
#
# Existing app.py expects:
#
#     job_skills = extract_jd_skills(jd)
#
# So this function continues returning ONLY a list.
#
# It now returns REQUIRED skills only.
# =========================================================

def extract_jd_skills(
    job_description
):

    analysis = analyze_jd_skills(
        job_description
    )

    return analysis.get(
        "required_skills",
        []
    )


# =========================================================
# PREFERRED SKILLS HELPER
# =========================================================

def extract_preferred_skills(
    job_description
):

    analysis = analyze_jd_skills(
        job_description
    )

    return analysis.get(
        "preferred_skills",
        []
    )


# =========================================================
# ALL JD SKILLS HELPER
# =========================================================

def extract_all_jd_skills(
    job_description
):

    analysis = analyze_jd_skills(
        job_description
    )

    return analysis.get(
        "all_skills",
        []
    )


# =========================================================
# BACKWARD COMPATIBILITY
# =========================================================

extract_job_skills = extract_jd_skills