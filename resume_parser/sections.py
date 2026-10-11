import re


# =========================================================
# SECTION ALIASES
# =========================================================

SECTION_ALIASES = {

    "summary": [
        "summary",
        "professional summary",
        "career summary",
        "profile",
        "about me",
        "objective",
        "career objective",
        "professional profile"
    ],

    "skills": [
        "skills",
        "technical skills",
        "technical skill",
        "core skills",
        "key skills",
        "technical competencies",
        "technical proficiencies",
        "skills & technologies",
        "skills and technologies",
        "technologies",
        "technical knowledge",
        "programming skills"
    ],

    "projects": [
        "projects",
        "project",
        "academic projects",
        "personal projects",
        "key projects",
        "major projects",
        "project experience",
        "academic project",
        "personal project"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history",
        "career history",
        "professional background",
        "internship experience",
        "internships",
        "employment"
    ],

    "education": [
        "education",
        "educational background",
        "educational qualifications",
        "academic background",
        "academic qualifications",
        "academic details",
        "qualification",
        "qualifications"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "certificate",
        "professional certifications",
        "courses",
        "training",
        "licenses"
    ],

    "achievements": [
        "achievements",
        "accomplishments",
        "awards",
        "honors",
        "honours"
    ],

    "strengths": [
        "strengths",
        "key strengths",
        "core strengths",
        "personal strengths"
    ],

    "declaration": [
        "declaration",
        "declarations"
    ],

    "references": [
        "references",
        "referees"
    ]
}


# =========================================================
# NORMALIZE HEADING
# =========================================================

def normalize_heading(text):

    if not text:
        return ""

    text = str(text).strip()

    # Remove bullets
    text = re.sub(
        r"^[•●▪◦■□\-–—*]+\s*",
        "",
        text
    )

    # Remove trailing colon
    text = re.sub(
        r":\s*$",
        "",
        text
    )

    # Normalize spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip().lower()


# =========================================================
# DETECT ONE SECTION HEADING
# =========================================================

def detect_section_heading(line):

    normalized = normalize_heading(line)

    if not normalized:
        return None

    for section_name, aliases in SECTION_ALIASES.items():

        for alias in aliases:

            if normalized == alias.lower():

                return section_name

    return None


# =========================================================
# DETECT ALL SECTIONS
# =========================================================

def detect_sections(text):

    sections = {}

    if not text:
        return sections

    lines = text.splitlines()

    current_section = None

    for line in lines:

        line = line.strip()

        if not line:
            continue

        detected = detect_section_heading(line)

        # New section
        if detected:

            current_section = detected

            if current_section not in sections:

                sections[current_section] = []

            continue

        # Add line to current section
        if current_section:

            sections[current_section].append(line)

    return sections


# =========================================================
# GET SECTION
# =========================================================

def get_section(text, section_name):

    sections = detect_sections(text)

    content = sections.get(
        section_name,
        []
    )

    return "\n".join(content).strip()


# =========================================================
# GET SECTION LINES
# =========================================================

def get_section_lines(text, section_name):

    sections = detect_sections(text)

    return sections.get(
        section_name,
        [])


# =========================================================
# DEBUG PRINT
# =========================================================

def print_sections(text):

    sections = detect_sections(text)

    print(
        "\n========== DETECTED SECTIONS =========="
    )

    if not sections:

        print("NO SECTIONS DETECTED")

    else:

        for section_name, content in sections.items():

            print(
                f"\n[{section_name.upper()}]"
            )

            if content:

                for line in content:

                    print(line)

            else:

                print("(empty)")

    print(
        "\n========================================"
    )