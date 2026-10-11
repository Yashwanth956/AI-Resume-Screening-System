# ============================================================
# resume_parser/skills.py
# Resume Skill Extraction
# ============================================================

import re

from resume_parser.master_skills import (
    ALL_SKILLS,
    normalize_skill,
)

# New comprehensive master_skills.py exposes SKILL_SEARCH_MAP.
# Keep a safe fallback so this module still imports with older versions.
try:
    from resume_parser.master_skills import SKILL_SEARCH_MAP
except ImportError:
    SKILL_SEARCH_MAP = {
        str(skill).strip().lower(): normalize_skill(skill)
        for skill in ALL_SKILLS
        if skill
    }


# ============================================================
# SECTION HEADINGS
# ============================================================

SKILL_SECTION_HEADINGS = {
    "skills",
    "technical skills",
    "technical skill",
    "core skills",
    "key skills",
    "professional skills",
    "programming skills",
    "technical expertise",
    "technologies",
    "technology",
    "tech stack",
    "technical proficiency",
    "skills & technologies",
    "skills and technologies",
    "tools & technologies",
    "tools and technologies",
    "technical stack",
    "competencies",
    "core competencies",
}

SECTION_END_HEADINGS = {
    "education",
    "academic qualifications",
    "academic background",
    "experience",
    "work experience",
    "professional experience",
    "employment",
    "employment history",
    "work history",
    "internships",
    "internship",
    "projects",
    "project",
    "certificates",
    "certificate",
    "certifications",
    "achievements",
    "awards",
    "publications",
    "research",
    "activities",
    "extracurricular activities",
    "interests",
    "hobbies",
    "strengths",
    "summary",
    "professional summary",
    "profile",
    "profile summary",
    "objective",
    "career objective",
    "about me",
    "references",
    "declaration",
}


# ============================================================
# FULL-RESUME SAFETY
# ============================================================
#
# These short aliases can be useful inside a dedicated Skills section,
# but are too ambiguous to scan across ordinary prose.
#
# Examples:
#   Go -> English verb
#   R  -> initial/grade
#   C  -> initial/grade
#   CV -> curriculum vitae, not always Computer Vision
#   AD -> advertisement, not always Active Directory
#   CAN -> ordinary English word, not always CAN Bus
#
# Canonical multi-word forms such as "Computer Vision",
# "Active Directory" and "CAN Bus" are still detected.
# ============================================================

AMBIGUOUS_FULL_RESUME_TERMS = {
    "c",
    "r",
    "go",
    "cv",
    "ad",
    "can",
    "ts",
}


# ============================================================
# TEXT HELPERS
# ============================================================

def _clean_text(text):
    if not text:
        return ""

    text = str(text)

    # Fix a common PDF split-word artifact:
    # "secu-\nrity" -> "security"
    text = re.sub(
        r"([A-Za-z])-\s*\n\s*([a-z])",
        r"\1\2",
        text,
    )

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    text = text.replace("\t", " ")
    text = text.replace("\u00a0", " ")

    # Common PDF bullet characters.
    for bullet in (
        "\u2022",
        "\uf0b7",
        "\u25cf",
        "\u25aa",
        "\u25e6",
        "\u2023",
    ):
        text = text.replace(bullet, " ")

    return text


def _normalize_line(line):
    if not line:
        return ""

    line = str(line).strip()

    line = re.sub(
        r"^[\s•●▪◦‣*\-]+",
        "",
        line,
    )

    line = re.sub(
        r"\s+",
        " ",
        line,
    )

    return line.strip()


def _heading_key(line):
    """Normalize a possible section heading for exact comparison."""

    value = _normalize_line(line).lower()

    # A heading commonly appears as "TECHNICAL SKILLS:".
    value = value.strip("#:- ")

    # Do not treat long content lines as headings.
    if len(value) > 60:
        return ""

    return value


def _is_section_heading(line, headings):
    return _heading_key(line) in headings


# ============================================================
# EXTRACT SKILLS SECTIONS
# ============================================================

def _extract_skill_sections(text):
    if not text:
        return []

    lines = text.splitlines()

    sections = []
    current = []
    in_skill_section = False

    for raw_line in lines:
        line = _normalize_line(raw_line)

        if not line:
            continue

        key = _heading_key(line)

        # Standard standalone heading.
        if key in SKILL_SECTION_HEADINGS:
            if current:
                sections.append("\n".join(current))
                current = []

            in_skill_section = True
            continue

        # Inline heading, e.g.
        # "Technical Skills: Python, SQL, Git"
        inline_match = re.match(
            r"^([^:]{1,45})\s*:\s*(.+)$",
            line,
        )

        if inline_match:
            possible_heading = _heading_key(
                inline_match.group(1)
            )

            if possible_heading in SKILL_SECTION_HEADINGS:
                if current:
                    sections.append("\n".join(current))
                    current = []

                in_skill_section = True

                inline_body = inline_match.group(2).strip()
                if inline_body:
                    current.append(inline_body)

                continue

        if in_skill_section and key in SECTION_END_HEADINGS:
            if current:
                sections.append("\n".join(current))

            current = []
            in_skill_section = False
            continue

        if in_skill_section:
            current.append(line)

    if current:
        sections.append("\n".join(current))

    return sections


# ============================================================
# SEARCH MAP
# ============================================================

def _build_search_map():
    """
    Build one search map from master_skills.py.

    The new master file contains:
        canonical skill -> itself
        alias           -> canonical skill

    Older master files still work because of the import fallback.
    """

    lookup = {}

    for term, canonical in SKILL_SEARCH_MAP.items():
        if not term or not canonical:
            continue

        normalized = normalize_skill(canonical)

        if not normalized:
            continue

        lookup[str(term).strip().lower()] = normalized.strip()

    # Guarantee every canonical ALL_SKILLS item is searchable.
    for skill in ALL_SKILLS:
        if not skill:
            continue

        canonical = normalize_skill(skill)

        if not canonical:
            continue

        lookup.setdefault(
            str(skill).strip().lower(),
            canonical.strip(),
        )

    return lookup


SKILL_LOOKUP = _build_search_map()


# ============================================================
# SEARCH PATTERN
# ============================================================

def _create_search_pattern(term):
    """
    Create a boundary-safe case-insensitive pattern.

    Text is whitespace-normalized before searching, so multi-word
    skills can match even when the original PDF wrapped a line.
    """

    term = str(term).strip()

    if not term:
        return None

    # Flexible spaces inside multi-word terms.
    pieces = re.split(r"\s+", term)
    body = r"\s+".join(
        re.escape(piece)
        for piece in pieces
        if piece
    )

    if not body:
        return None

    # Alphanumeric boundary rather than \b so C++, C#, .NET,
    # CI/CD, TCP/IP, etc. work correctly.
    return (
        r"(?<![A-Za-z0-9])"
        + body
        + r"(?![A-Za-z0-9])"
    )


# ============================================================
# CONTEXT FILTERS
# ============================================================

def _allow_match(term, canonical, text, match, structured_section):
    """Filter a few known false-positive contexts."""

    term_key = str(term).strip().lower()
    canonical_key = str(canonical).strip().lower()

    if not structured_section:
        if term_key in AMBIGUOUS_FULL_RESUME_TERMS:
            return False

    # Do not infer SQL skill merely from the attack name
    # "SQL Injection" in a cybersecurity project/resume.
    if canonical_key == "sql":
        after = text[
            match.end():
            match.end() + 30
        ]

        if re.match(
            r"\s+injection\b",
            after,
            flags=re.IGNORECASE,
        ):
            return False

    return True


# ============================================================
# FIND SKILLS IN TEXT
# ============================================================

def _find_skills_in_text(text, structured_section=False):
    if not text:
        return []

    # Preserve punctuation, but collapse whitespace so wrapped
    # phrases such as "Machine\nLearning" are searchable.
    searchable_text = re.sub(
        r"\s+",
        " ",
        str(text),
    ).strip()

    found = []

    # Longest search phrases first. This improves stability for
    # phrases such as "Hugging Face Transformers" and "REST APIs".
    search_items = sorted(
        SKILL_LOOKUP.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    )

    for term, canonical in search_items:
        if not term or not canonical:
            continue

        pattern = _create_search_pattern(term)

        if not pattern:
            continue

        try:
            match = re.search(
                pattern,
                searchable_text,
                flags=re.IGNORECASE,
            )
        except re.error:
            continue

        if not match:
            continue

        if not _allow_match(
            term=term,
            canonical=canonical,
            text=searchable_text,
            match=match,
            structured_section=structured_section,
        ):
            continue

        found.append(canonical)

    return found


# ============================================================
# UNIQUE + SORT
# ============================================================

def _unique_skills(skills):
    result = []
    seen = set()

    for skill in skills or []:
        normalized = normalize_skill(skill)

        if not normalized:
            continue

        normalized = normalized.strip()
        key = normalized.lower()

        if key in seen:
            continue

        seen.add(key)
        result.append(normalized)

    return result


def _sort_skills(skills):
    return sorted(
        skills,
        key=lambda value: value.lower(),
    )


# ============================================================
# MAIN FUNCTION
# ============================================================

def extract_skills(text):
    """
    Extract canonical skills from a resume.

    Strategy:
    1. Preserve line structure while cleaning PDF text.
    2. Detect explicit Skills / Technical Skills sections.
    3. Search those sections using canonical names + aliases.
    4. Also enrich from the complete resume so technologies used
       only in Experience or Projects are not lost.
    5. Apply stricter filters during full-resume scanning to reduce
       false positives from short/ambiguous terms.
    6. Normalize and deduplicate the result.
    """

    if not text:
        return []

    cleaned_text = _clean_text(text)

    if not cleaned_text.strip():
        return []

    result = []

    # --------------------------------------------------------
    # 1. Strong evidence: explicit skill sections
    # --------------------------------------------------------
    skill_sections = _extract_skill_sections(
        cleaned_text
    )

    for section in skill_sections:
        result.extend(
            _find_skills_in_text(
                section,
                structured_section=True,
            )
        )

    # --------------------------------------------------------
    # 2. Resume-wide enrichment
    # --------------------------------------------------------
    # This is intentionally run even when a Skills section exists.
    # Experienced resumes often mention important tools only inside
    # Experience / Projects (e.g. MLflow, FAISS, Kubernetes).
    result.extend(
        _find_skills_in_text(
            cleaned_text,
            structured_section=False,
        )
    )

    return _sort_skills(
        _unique_skills(result)
    )


# ============================================================
# BACKWARD-COMPATIBILITY ALIAS
# ============================================================

def extract_resume_skills(text):
    return extract_skills(text)


# ============================================================
# DEBUG FUNCTION
# ============================================================

def debug_skill_extraction(text):
    cleaned = _clean_text(text)
    sections = _extract_skill_sections(cleaned)
    skills = extract_skills(cleaned)

    print()
    print("=" * 70)
    print("SKILL EXTRACTION DEBUG")
    print("=" * 70)

    print("\nDetected Skill Sections:")

    if sections:
        for index, section in enumerate(sections, start=1):
            print(f"\nSECTION {index}:")
            print(section)
    else:
        print("No explicit Skills / Technical Skills section found.")

    print("\nFinal Extracted Skills:")

    if skills:
        for skill in skills:
            print("-", skill)
    else:
        print("No skills detected.")

    print("=" * 70)


# ============================================================
# SELF TEST
# ============================================================

if __name__ == "__main__":

    sample_resume = """
    MEERA NAIR
    AI / ML Engineer

    TECHNICAL SKILLS
    Python, SQL, Pandas, NumPy, scikit-learn, TensorFlow,
    XGBoost, NLP, Hugging Face Transformers, sentence embeddings,
    RAG, LangChain, FAISS, FastAPI, MLflow, Docker, Git, AWS S3.

    PROFESSIONAL EXPERIENCE
    Built retrieval-augmented generation applications and model
    inference endpoints. Worked with Chroma DB and Kubernetes.

    PROJECTS
    Security Log Analyzer
    Detected SQL Injection attacks in web server logs.
    """

    debug_skill_extraction(sample_resume)