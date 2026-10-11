# =========================================================
# resume_parser/education.py
# Robust education extraction for multiple resume layouts
# =========================================================

import re


# =========================================================
# SECTION HEADINGS
# =========================================================

EDUCATION_HEADERS = {
    "education",
    "academic background",
    "educational background",
    "academic qualifications",
    "qualifications",
}

SECTION_END_HEADERS = {
    "technical skills",
    "technical skill",
    "skills",
    "soft skills",
    "technical competencies",
    "programming",
    "data science & ml",
    "development tools",
    "learning concepts",
    "projects",
    "project",
    "academic projects",
    "personal projects",
    "technical projects",
    "experience",
    "work experience",
    "professional experience",
    "employment",
    "internship",
    "internships",
    "certifications",
    "certificates",
    "certificate",
    "achievements",
    "achievements & certifications",
    "strengths",
    "positions of responsibility",
    "publications",
    "hobbies",
    "interests",
    "declaration",
    "references",
    "extracurricular",
}

MONTH_PATTERN = (
    r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|"
    r"may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|"
    r"oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
)

INSTITUTION_WORDS = (
    "university",
    "institute",
    "institution",
    "college",
    "collage",
    "school",
    "academy",
    "polytechnic",
    "campus",
)

BOARD_TOKENS = (
    "tsbie",
    "bse telangana",
    "board/university",
)

LOCATION_HINTS = {
    "hyderabad",
    "chennai",
    "kodad",
    "telangana",
    "visakhapatnam",
    "suryapet",
    "andhra pradesh",
}


# =========================================================
# NORMALIZATION
# =========================================================

def normalize_text(text):

    if not text:
        return ""

    text = str(text)

    text = (
        text
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("(cid:127)", " ")
        .replace("(cid:131)", " ")
        .replace("•", " ")
        .replace("∗", " ")
        .replace("–", "-")
        .replace("—", "-")
        .replace("−", "-")
        .replace("\u00a0", " ")
    )

    lines = []

    for line in text.splitlines():

        line = re.sub(
            r"[ \t]+",
            " ",
            line
        ).strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def normalize_heading(line):

    if not line:
        return ""

    value = (
        str(line)
        .strip()
        .lower()
        .rstrip(":")
        .strip()
    )

    value = re.sub(
        r"[^a-z0-9&/+ ]",
        "",
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


def is_table_header(line):

    if not line:
        return False

    lower = str(line).lower()

    header_words = (
        "qualification",
        "institution",
        "board",
        "university",
        "year",
        "score",
    )

    hits = sum(
        1
        for word in header_words
        if word in lower
    )

    return hits >= 4


# =========================================================
# SCORE EXTRACTION
# =========================================================

def find_score(line):

    if not line:
        return ""

    value = str(line)

    # CGPA: 8.4 / 10.0
    match = re.search(
        r"\bcgpa\s*[:\-]?\s*(\d+(?:\.\d+)?)",
        value,
        re.IGNORECASE
    )

    if match:
        return "CGPA: " + match.group(1)

    # GPA
    match = re.search(
        r"\bgpa\s*[:\-]?\s*(\d+(?:\.\d+)?)",
        value,
        re.IGNORECASE
    )

    if match:
        return "GPA: " + match.group(1)

    # Percentage / Percent
    match = re.search(
        r"\b(?:percentage|percent)\s*[:\-]?\s*"
        r"(\d+(?:\.\d+)?)\s*%?",
        value,
        re.IGNORECASE
    )

    if match:
        return (
            "Percentage: "
            + match.group(1)
            + "%"
        )

    # Standalone percentage
    match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*%",
        value
    )

    if match:
        return (
            "Percentage: "
            + match.group(1)
            + "%"
        )

    # x/10 or x/10.0
    match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*/\s*10(?:\.0)?\b",
        value
    )

    if match:
        return (
            match.group(1)
            + "/10"
        )

    # x/100
    match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*/\s*100\b",
        value
    )

    if match:
        return (
            match.group(1)
            + "/100"
        )

    return ""


# =========================================================
# DATE / PASSING YEAR EXTRACTION
# =========================================================

def find_duration(line):

    if not line:
        return ""

    value = str(line)

    # MM/YYYY - MM/YYYY
    match = re.search(
        r"\b(\d{1,2}/(?:19|20)\d{2})"
        r"\s*-\s*"
        r"(\d{1,2}/(?:19|20)\d{2})\b",
        value,
        re.IGNORECASE
    )

    if match:
        return (
            match.group(1)
            + " - "
            + match.group(2)
        )

    # Nov 2022 - Apr 2026
    match = re.search(
        rf"\b({MONTH_PATTERN}\s+(?:19|20)\d{{2}})"
        rf"\s*-\s*"
        rf"({MONTH_PATTERN}\s+(?:19|20)\d{{2}}|present|current)\b",
        value,
        re.IGNORECASE
    )

    if match:
        return (
            match.group(1)
            + " - "
            + match.group(2)
        )

    # 2022 - 2026
    match = re.search(
        r"\b((?:19|20)\d{2})"
        r"\s*-\s*"
        r"((?:19|20)\d{2})\b",
        value
    )

    if match:
        return (
            match.group(1)
            + " - "
            + match.group(2)
        )

    # Expected graduation
    match = re.search(
        rf"\b(?:expected\s+graduation|graduation\s+expected)"
        rf"\s*[:\-]?\s*"
        rf"({MONTH_PATTERN}\s+(?:19|20)\d{{2}})\b",
        value,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    # Graduation / passing year
    match = re.search(
        r"\b(?:graduation|graduated|passing\s+year|passing|passed)"
        r"\s*[:\-]?\s*((?:19|20)\d{2})\b",
        value,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    # Single MM/YYYY
    match = re.search(
        r"\b(\d{1,2}/(?:19|20)\d{2})\b",
        value
    )

    if match:
        return match.group(1)

    # Compact table row year: only accept if the line also
    # contains a score or a known board token.
    if (
        find_score(value)
        or any(
            token in value.lower()
            for token in BOARD_TOKENS
        )
    ):

        match = re.search(
            r"\b((?:19|20)\d{2})\b",
            value
        )

        if match:
            return match.group(1)

    # Standalone year
    match = re.fullmatch(
        r"\s*((?:19|20)\d{2})\s*",
        value
    )

    if match:
        return match.group(1)

    return ""


def is_standalone_duration(line):

    if not line:
        return False

    value = str(line).strip()

    if re.fullmatch(
        r"\d{1,2}/(?:19|20)\d{2}"
        r"\s*-\s*"
        r"\d{1,2}/(?:19|20)\d{2}",
        value
    ):
        return True

    if re.fullmatch(
        r"(?:19|20)\d{2}"
        r"\s*-\s*"
        r"(?:19|20)\d{2}",
        value
    ):
        return True

    if re.fullmatch(
        rf"{MONTH_PATTERN}\s+(?:19|20)\d{{2}}"
        rf"\s*-\s*"
        rf"{MONTH_PATTERN}\s+(?:19|20)\d{{2}}",
        value,
        re.IGNORECASE
    ):
        return True

    if re.fullmatch(
        r"\d{1,2}/(?:19|20)\d{2}",
        value
    ):
        return True

    if re.fullmatch(
        r"(?:19|20)\d{2}",
        value
    ):
        return True

    return False


# =========================================================
# QUALIFICATION DETECTION
# =========================================================

def identify_degree(line):

    if not line:
        return ""

    value = str(line).strip()
    lower = value.lower()

    # Strong degree names
    strong_patterns = [

        (
            "B.Tech",
            [
                r"\bb\.?\s*tech\.?\b",
                r"\bbtech\b",
                r"\bbachelor\s+of\s+technology\b",
            ],
        ),

        (
            "B.E",
            [
                r"(?<![\w.])b\.?\s*e\.?(?![\w.])",
                r"\bbachelor\s+of\s+engineering\b",
            ],
        ),

        (
            "B.Sc",
            [
                r"(?<![\w.])b\.?\s*sc\.?(?![\w.])",
                r"\bbsc\b",
                r"\bbachelor\s+of\s+science\b",
            ],
        ),

        (
            "BCA",
            [
                r"\bbca\b",
                r"\bbachelor\s+of\s+computer\s+applications\b",
            ],
        ),

        (
            "BBA",
            [
                r"\bbba\b",
                r"\bbachelor\s+of\s+business\s+administration\b",
            ],
        ),

        (
            "B.Com",
            [
                r"(?<![\w.])b\.?\s*com\.?(?![\w.])",
                r"\bbcom\b",
                r"\bbachelor\s+of\s+commerce\b",
            ],
        ),

        (
            "B.A",
            [
                r"(?<![\w.])b\.?\s*a\.?(?![\w.])",
                r"\bbachelor\s+of\s+arts\b",
            ],
        ),

        (
            "M.Tech",
            [
                r"\bm\.?\s*tech\.?\b",
                r"\bmtech\b",
                r"\bmaster\s+of\s+technology\b",
            ],
        ),

        (
            "M.E",
            [
                r"(?<![\w.])m\.?\s*e\.?(?![\w.])",
                r"\bmaster\s+of\s+engineering\b",
            ],
        ),

        (
            "M.Sc",
            [
                r"(?<![\w.])m\.?\s*sc\.?(?![\w.])",
                r"\bmsc\b",
                r"\bmaster\s+of\s+science\b",
            ],
        ),

        (
            "MCA",
            [
                r"\bmca\b",
                r"\bmaster\s+of\s+computer\s+applications\b",
            ],
        ),

        (
            "MBA",
            [
                r"\bmba\b",
                r"\bmaster\s+of\s+business\s+administration\b",
            ],
        ),

        (
            "PhD",
            [
                r"\bph\.?\s*d\.?\b",
                r"\bdoctorate\b",
                r"\bdoctoral\b",
            ],
        ),
    ]

    for degree_name, patterns in strong_patterns:

        for pattern in patterns:

            if re.search(
                pattern,
                lower,
                re.IGNORECASE
            ):

                return degree_name

    # Board / Intermediate qualification
    if (
        "state board of intermediate" in lower
        or "board of intermediate education" in lower
        or lower.startswith("intermediate")
        or lower.startswith("higher secondary")
        or lower.startswith("senior secondary")
        or re.match(r"^12th\b", lower)
        or re.match(r"^class\s+12\b", lower)
    ):

        return "Intermediate"

    # SSC qualification
    if (
        "board of secondary education" in lower
        or "bord of secondary education" in lower
        or lower.startswith("secondary education")
        or lower.startswith("secondary school certificate")
        or re.match(r"^ssc\b", lower)
        or re.match(r"^10th\b", lower)
        or re.match(r"^class\s+10\b", lower)
    ):

        return "SSC"

    if lower.startswith("diploma"):
        return "Diploma"

    return ""


# =========================================================
# INSTITUTION HELPERS
# =========================================================

def repair_institution_spacing(value):

    if not value:
        return ""

    value = str(value).strip()

    alpha_count = len(
        re.findall(
            r"[A-Za-z]",
            value
        )
    )

    if (
        value.count(" ") >= 2
        or alpha_count < 18
    ):

        return value

    value = re.sub(
        r"(?<=[a-z])(?=[A-Z])",
        " ",
        value
    )

    value = re.sub(
        r"(?<=\.)(?=[A-Z])",
        " ",
        value
    )

    value = re.sub(
        r"(R&D)(?=[A-Z])",
        r"\1 ",
        value
    )

    replacements = {
        "Instituteof": "Institute of ",
        "Collegeof": "College of ",
        "Schoolof": "School of ",
        "Universityof": "University of ",
        "Scienceand": "Science and ",
        "Artsand": "Arts and ",
        "Researchand": "Research and ",
        "Engineeringand": "Engineering and ",
        "Technologyand": "Technology and ",
    }

    for old, new in replacements.items():

        value = re.sub(
            re.escape(old),
            new,
            value,
            flags=re.IGNORECASE
        )

    value = re.sub(
        r"\s+",
        " ",
        value
    ).strip()

    return value


def looks_like_institution(line):

    if not line:
        return False

    value = str(line).strip()
    lower = value.lower()

    if is_table_header(value):
        return False

    if identify_degree(value):
        return False

    return any(
        word in lower
        for word in INSTITUTION_WORDS
    )


def clean_institution(line):

    if not line:
        return ""

    value = str(line).strip()

    # Pipe-separated layout: take the institution part.
    if "|" in value:

        parts = [
            part.strip()
            for part in value.split("|")
            if part.strip()
        ]

        for part in parts:

            if (
                any(
                    word in part.lower()
                    for word in INSTITUTION_WORDS
                )
                and not identify_degree(part)
            ):

                return repair_institution_spacing(
                    part.strip(" ,-:|")
                )

    # Remove score text
    value = re.sub(
        r"\bcgpa\s*[:\-]?\s*"
        r"\d+(?:\.\d+)?(?:\s*/\s*10(?:\.0)?)?",
        " ",
        value,
        flags=re.IGNORECASE
    )

    value = re.sub(
        r"\bgpa\s*[:\-]?\s*"
        r"\d+(?:\.\d+)?",
        " ",
        value,
        flags=re.IGNORECASE
    )

    value = re.sub(
        r"\b(?:percentage|percent)"
        r"\s*[:\-]?\s*"
        r"\d+(?:\.\d+)?\s*%?",
        " ",
        value,
        flags=re.IGNORECASE
    )

    value = re.sub(
        r"\b\d+(?:\.\d+)?\s*%",
        " ",
        value
    )

    value = re.sub(
        r"\b\d+(?:\.\d+)?\s*/\s*(?:10(?:\.0)?|100)\b",
        " ",
        value
    )

    # Remove dates
    value = re.sub(
        rf"\b{MONTH_PATTERN}\s+(?:19|20)\d{{2}}"
        rf"\s*-\s*"
        rf"(?:{MONTH_PATTERN}\s+(?:19|20)\d{{2}}|present|current)\b",
        " ",
        value,
        flags=re.IGNORECASE
    )

    value = re.sub(
        r"\b\d{1,2}/(?:19|20)\d{2}"
        r"\s*-\s*"
        r"\d{1,2}/(?:19|20)\d{2}\b",
        " ",
        value
    )

    value = re.sub(
        r"\b(?:19|20)\d{2}"
        r"\s*-\s*"
        r"(?:19|20)\d{2}\b",
        " ",
        value
    )

    value = re.sub(
        r"\b\d{1,2}/(?:19|20)\d{2}\b",
        " ",
        value
    )

    # Remove compact table year
    value = re.sub(
        r"\b(?:19|20)\d{2}\b",
        " ",
        value
    )

    value = re.sub(
        r"\s*[|]\s*",
        " ",
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    ).strip(" ,-:|")

    return repair_institution_spacing(
        value
    )


def repeated_institution_phrase(value):

    if not value:
        return ""

    words = str(value).split()

    institution_end_words = {
        "university",
        "college",
        "collage",
        "institute",
        "school",
    }

    for start in range(
        len(words)
    ):

        for size in range(
            1,
            7
        ):

            end = start + size
            second_end = end + size

            if second_end > len(words):
                break

            first = words[
                start:end
            ]

            second = words[
                end:second_end
            ]

            if (
                [w.lower() for w in first]
                == [w.lower() for w in second]
                and first[-1].strip(",.").lower()
                in institution_end_words
            ):

                return " ".join(
                    first
                ).strip(" ,")

    return ""


def extract_inline_institution(
    line,
    degree_type
):

    if not line:
        return ""

    value = str(line).strip()
    lower_value = value.lower()

    # Canonical qualification lines such as:
    #   Telangana State Board of Intermediate Education (TSBIE)
    #   Secondary Education (School)
    #   Board of Secondary Education-SSC Kodad
    # are qualifications, not inline institutions.
    if degree_type == "Intermediate":

        if (
            "board of intermediate education" in lower_value
            or "state board of intermediate" in lower_value
        ):
            return ""

        if lower_value.startswith("intermediate"):

            tail = re.sub(
                r"(?i)^intermediate\b",
                "",
                value,
                count=1
            )

            if not any(
                word in tail.lower()
                for word in INSTITUTION_WORDS
            ):
                return ""

    if degree_type == "SSC":

        if (
            "board of secondary education" in lower_value
            or "bord of secondary education" in lower_value
            or lower_value.startswith("secondary education")
        ):

            if re.search(
                r"(?i)\bssc\b",
                value
            ):

                tail = re.split(
                    r"(?i)\bssc\b",
                    value,
                    maxsplit=1
                )[-1]

                if not any(
                    word in tail.lower()
                    for word in INSTITUTION_WORDS
                ):
                    return ""

            else:
                return ""

        if lower_value.startswith("ssc"):

            tail = re.sub(
                r"(?i)^ssc\b",
                "",
                value,
                count=1
            )

            if not any(
                word in tail.lower()
                for word in INSTITUTION_WORDS
            ):
                return ""

    # Remove score/date from a working copy.
    work = value

    work = re.sub(
        r"\bcgpa\s*[:\-]?\s*"
        r"\d+(?:\.\d+)?(?:\s*/\s*10(?:\.0)?)?",
        " ",
        work,
        flags=re.IGNORECASE
    )

    work = re.sub(
        r"\b(?:percentage|percent)"
        r"\s*[:\-]?\s*"
        r"\d+(?:\.\d+)?\s*%?",
        " ",
        work,
        flags=re.IGNORECASE
    )

    work = re.sub(
        r"\b\d+(?:\.\d+)?\s*%",
        " ",
        work
    )

    work = re.sub(
        r"\b\d+(?:\.\d+)?\s*/\s*(?:10(?:\.0)?|100)\b",
        " ",
        work
    )

    work = re.sub(
        r"\b\d{1,2}/(?:19|20)\d{2}"
        r"\s*-\s*"
        r"\d{1,2}/(?:19|20)\d{2}\b",
        " ",
        work
    )

    work = re.sub(
        r"\b(?:19|20)\d{2}"
        r"\s*-\s*"
        r"(?:19|20)\d{2}\b",
        " ",
        work
    )

    work = re.sub(
        r"\b(?:19|20)\d{2}\b",
        " ",
        work
    )

    work = re.sub(
        r"\s+",
        " ",
        work
    ).strip(" ,-")

    # Vikas-style duplicate institution:
    # Parul University Parul University
    repeated = repeated_institution_phrase(
        work
    )

    if repeated:
        return clean_institution(
            repeated
        )

    # Strip the qualification prefix for compact table rows.
    remainder = work

    if degree_type == "B.Tech":

        remainder = re.sub(
            r"(?i)^.*?\bb\.?\s*tech\.?\b",
            "",
            remainder,
            count=1
        ).strip(" ,-")

        # Common branch/specialization prefixes before institution.
        remainder = re.sub(
            r"(?i)^(?:cse|ece|eee|it)"
            r"(?:\s*\([^)]*\))?\s*",
            "",
            remainder
        ).strip(" ,-")

    elif degree_type == "Intermediate":

        remainder = re.sub(
            r"(?i)^.*?\bintermediate\b",
            "",
            remainder,
            count=1
        ).strip(" ,-")

    elif degree_type == "SSC":

        remainder = re.sub(
            r"(?i)^.*?\bssc\b",
            "",
            remainder,
            count=1
        ).strip(" ,-")

    # In table rows, board usually comes after comma.
    if "," in remainder:

        before_comma = (
            remainder
            .split(",", 1)[0]
            .strip()
        )

        if any(
            word in before_comma.lower()
            for word in INSTITUTION_WORDS
        ):

            return clean_institution(
                before_comma
            )

    # Same-line institution ending in a known institution word.
    match = re.search(
        r"(?i)([A-Za-z0-9.&'()\- ]{2,80}?"
        r"(?:University|College|Collage|Institute|School))\b",
        remainder
    )

    if match:

        candidate = (
            match.group(1)
            .strip(" ,-")
        )

        # Remove obvious qualification leftovers.
        candidate = re.sub(
            r"(?i)^(?:cse|ece|eee|it)"
            r"(?:\s*\([^)]*\))?\s*",
            "",
            candidate
        ).strip()

        if candidate:
            return clean_institution(
                candidate
            )

    return ""


# =========================================================
# DEGREE CLEANING
# =========================================================

def extract_degree_location(
    line,
    degree_type
):

    if not line:
        return ""

    value = str(line).strip()

    if degree_type == "SSC":

        # Example:
        # Board of Secondary Education-SSC Kodad
        match = re.search(
            r"(?i)\bssc\b\s+([A-Za-z][A-Za-z .'-]{1,30})$",
            value
        )

        if match:

            location = (
                match.group(1)
                .strip(" ,-")
            )

            if (
                not find_score(location)
                and not find_duration(location)
            ):
                return location

    return ""


def clean_degree(
    line,
    inline_institution="",
    degree_location=""
):

    if not line:
        return ""

    value = str(line).strip()

    # Remove scores
    value = re.sub(
        r"\bcgpa\s*[:\-]?\s*"
        r"\d+(?:\.\d+)?(?:\s*/\s*10(?:\.0)?)?",
        " ",
        value,
        flags=re.IGNORECASE
    )

    value = re.sub(
        r"\bgpa\s*[:\-]?\s*"
        r"\d+(?:\.\d+)?",
        " ",
        value,
        flags=re.IGNORECASE
    )

    value = re.sub(
        r"\b(?:percentage|percent)"
        r"\s*[:\-]?\s*"
        r"\d+(?:\.\d+)?\s*%?",
        " ",
        value,
        flags=re.IGNORECASE
    )

    value = re.sub(
        r"\b\d+(?:\.\d+)?\s*%",
        " ",
        value
    )

    value = re.sub(
        r"\b\d+(?:\.\d+)?\s*/\s*(?:10(?:\.0)?|100)\b",
        " ",
        value
    )

    # Remove date ranges / years
    value = re.sub(
        rf"\b{MONTH_PATTERN}\s+(?:19|20)\d{{2}}"
        rf"\s*-\s*"
        rf"{MONTH_PATTERN}\s+(?:19|20)\d{{2}}\b",
        " ",
        value,
        flags=re.IGNORECASE
    )

    value = re.sub(
        r"\b\d{1,2}/(?:19|20)\d{2}"
        r"\s*-\s*"
        r"\d{1,2}/(?:19|20)\d{2}\b",
        " ",
        value
    )

    value = re.sub(
        r"\b(?:19|20)\d{2}"
        r"\s*-\s*"
        r"(?:19|20)\d{2}\b",
        " ",
        value
    )

    value = re.sub(
        r"\b(?:19|20)\d{2}\b",
        " ",
        value
    )

    # Remove inline institution (possibly repeated).
    if inline_institution:

        escaped = re.escape(
            inline_institution
        )

        value = re.sub(
            escaped,
            " ",
            value,
            flags=re.IGNORECASE
        )

        value = re.sub(
            escaped,
            " ",
            value,
            flags=re.IGNORECASE
        )

    # Remove board tails only for compact table rows where
    # an inline institution was extracted (for example Vikas).
    if inline_institution:

        value = re.sub(
            r"(?i),?\s*\bTSBIE\b.*$",
            "",
            value
        )

        value = re.sub(
            r"(?i),?\s*\bBSE\s+Telangana\b.*$",
            "",
            value
        )

    if degree_location:

        value = re.sub(
            re.escape(
                degree_location
            )
            + r"\s*$",
            "",
            value,
            flags=re.IGNORECASE
        )

    value = re.sub(
        r"\s+",
        " ",
        value
    ).strip(" ,-|")

    return value


# =========================================================
# SMALL-LINE HELPERS
# =========================================================

def split_specialization_location(line):

    if not line:
        return "", ""

    value = str(line).strip()

    match = re.fullmatch(
        r"\(([^)]+)\)\s*(.*)",
        value
    )

    if not match:
        return "", ""

    specialization = (
        "("
        + match.group(1).strip()
        + ")"
    )

    location = (
        match.group(2)
        .strip(" ,-")
    )

    return (
        specialization,
        location
    )


def looks_like_location(line):

    if not line:
        return False

    value = str(line).strip()
    lower = value.lower()

    if (
        identify_degree(value)
        or looks_like_institution(value)
        or find_score(value)
        or find_duration(value)
        or is_table_header(value)
    ):

        return False

    if lower in LOCATION_HINTS:
        return True

    # Conservative generic location line.
    if (
        len(value) <= 30
        and len(value.split()) <= 4
        and re.fullmatch(
            r"[A-Za-z][A-Za-z .'-]*",
            value
        )
    ):
        return True

    return False


def append_location(
    institution,
    location
):

    if not location:
        return institution

    location = str(
        location
    ).strip(" ,")

    if not institution:
        return institution

    if location.lower() in institution.lower():
        return institution

    return (
        institution.rstrip(" ,")
        + ", "
        + location
    )


# =========================================================
# MAIN EDUCATION EXTRACTOR
# =========================================================

def extract_education(text):

    if not text:
        return []

    text = normalize_text(
        text
    )

    if not text:
        return []

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return []

    # =====================================================
    # 1. FIND EDUCATION SECTION
    # =====================================================

    education_start = -1

    for index, line in enumerate(
        lines
    ):

        if normalize_heading(
            line
        ) in EDUCATION_HEADERS:

            education_start = (
                index + 1
            )

            break

    # Fallback when heading is missing.
    if education_start == -1:

        for index, line in enumerate(
            lines
        ):

            if identify_degree(
                line
            ):

                education_start = index
                break

    if education_start == -1:
        return []

    # =====================================================
    # 2. FIND END OF EDUCATION SECTION
    # =====================================================

    education_end = len(
        lines
    )

    for index in range(
        education_start,
        len(lines)
    ):

        if normalize_heading(
            lines[index]
        ) in SECTION_END_HEADERS:

            education_end = index
            break

    education_lines = lines[
        education_start:
        education_end
    ]

    if not education_lines:
        return []

    # =====================================================
    # 3. STATE-MACHINE PARSING
    # =====================================================

    records = []

    current = None

    pending_institution = ""
    pending_duration = ""
    pending_score = ""
    pending_location = ""

    def finalize_current():

        nonlocal current

        if not current:
            return

        # If a location was captured before an institution,
        # apply it now.
        if (
            current.get("institution")
            and current.get("_location")
        ):

            current[
                "institution"
            ] = append_location(
                current["institution"],
                current["_location"]
            )

        current.pop(
            "_location",
            None
        )

        if current.get(
            "degree"
        ):

            records.append(
                current
            )

        current = None

    for index, line in enumerate(
        education_lines
    ):

        if is_table_header(
            line
        ):
            continue

        degree_type = identify_degree(
            line
        )

        # -------------------------------------------------
        # NEW QUALIFICATION
        # -------------------------------------------------

        if degree_type:

            finalize_current()

            inline_institution = (
                extract_inline_institution(
                    line,
                    degree_type
                )
            )

            degree_location = (
                extract_degree_location(
                    line,
                    degree_type
                )
            )

            current = {
                "degree": clean_degree(
                    line,
                    inline_institution,
                    degree_location
                ),
                "institution": (
                    inline_institution
                    or pending_institution
                ),
                "score": (
                    find_score(line)
                    or pending_score
                ),
                "duration": (
                    find_duration(line)
                    or pending_duration
                ),
                "_location": (
                    degree_location
                    or pending_location
                ),
            }

            pending_institution = ""
            pending_duration = ""
            pending_score = ""
            pending_location = ""

            continue

        # -------------------------------------------------
        # SPECIALIZATION + LOCATION, e.g. "(MPC) Kodad"
        # -------------------------------------------------

        specialization, spec_location = (
            split_specialization_location(
                line
            )
        )

        if specialization:

            if current:

                if (
                    specialization.lower()
                    not in current[
                        "degree"
                    ].lower()
                ):

                    current[
                        "degree"
                    ] = (
                        current[
                            "degree"
                        ]
                        + " "
                        + specialization
                    ).strip()

                if spec_location:

                    if current[
                        "institution"
                    ]:

                        current[
                            "institution"
                        ] = append_location(
                            current[
                                "institution"
                            ],
                            spec_location
                        )

                    else:

                        current[
                            "_location"
                        ] = spec_location

            else:

                pending_location = (
                    spec_location
                )

            continue

        # -------------------------------------------------
        # INSTITUTION LINE
        # -------------------------------------------------

        if looks_like_institution(
            line
        ):

            institution = (
                clean_institution(
                    line
                )
            )

            line_duration = (
                find_duration(
                    line
                )
            )

            line_score = find_score(
                line
            )

            if current:

                # If current already has an institution,
                # this institution belongs to the NEXT
                # qualification in institution-first layouts.
                if current[
                    "institution"
                ]:

                    pending_institution = (
                        institution
                    )

                    if line_duration:
                        pending_duration = (
                            line_duration
                        )

                    if line_score:
                        pending_score = (
                            line_score
                        )

                else:

                    current[
                        "institution"
                    ] = institution

                    if current[
                        "_location"
                    ]:

                        current[
                            "institution"
                        ] = append_location(
                            current[
                                "institution"
                            ],
                            current[
                                "_location"
                            ]
                        )

                        current[
                            "_location"
                        ] = ""

                    if (
                        not current[
                            "duration"
                        ]
                        and line_duration
                    ):

                        current[
                            "duration"
                        ] = line_duration

                    if (
                        not current[
                            "score"
                        ]
                        and line_score
                    ):

                        current[
                            "score"
                        ] = line_score

            else:

                pending_institution = (
                    institution
                )

                if line_duration:
                    pending_duration = (
                        line_duration
                    )

                if line_score:
                    pending_score = (
                        line_score
                    )

            continue

        # -------------------------------------------------
        # SCORE + DATE/PASSING YEAR
        #
        # A single line may contain both, for example:
        # CGPA: 9.3 Graduation: 2022 - 2026
        # -------------------------------------------------

        score = find_score(
            line
        )

        duration = find_duration(
            line
        )

        if score:

            if current:

                if not current[
                    "score"
                ]:

                    current[
                        "score"
                    ] = score

            else:

                pending_score = (
                    score
                )

        if duration:

            if current:

                # Yashwitha layout:
                #
                # CGPA: 9.0
                # 2020 - 2022
                # Board of Intermediate Education
                #
                # The new date belongs to NEXT record because
                # current already has its score.
                if (
                    is_standalone_duration(
                        line
                    )
                    and current[
                        "score"
                    ]
                    and current[
                        "duration"
                    ]
                ):

                    pending_duration = (
                        duration
                    )

                elif (
                    is_standalone_duration(
                        line
                    )
                    and current[
                        "score"
                    ]
                    and not current[
                        "duration"
                    ]
                    and current[
                        "institution"
                    ]
                ):

                    # If score+institution already exist and
                    # a new qualification follows, treat date
                    # as pending for next record.
                    next_line = (
                        education_lines[
                            index + 1
                        ]
                        if (
                            index + 1
                            < len(
                                education_lines
                            )
                        )
                        else ""
                    )

                    if identify_degree(
                        next_line
                    ):

                        pending_duration = (
                            duration
                        )

                    else:

                        current[
                            "duration"
                        ] = duration

                elif not current[
                    "duration"
                ]:

                    current[
                        "duration"
                    ] = duration

                else:

                    pending_duration = (
                        duration
                    )

            else:

                pending_duration = (
                    duration
                )

            continue

        if score:
            continue

        # -------------------------------------------------
        # SHORT LOCATION LINE
        # -------------------------------------------------

        if looks_like_location(
            line
        ):

            if current:

                if current[
                    "institution"
                ]:

                    current[
                        "institution"
                    ] = append_location(
                        current[
                            "institution"
                        ],
                        line
                    )

                else:

                    current[
                        "_location"
                    ] = line

            else:

                pending_location = (
                    line
                )

            continue

        # Ignore unrecognized lines inside education section.

    finalize_current()

    # =====================================================
    # 4. DEDUPLICATE
    # =====================================================

    cleaned_records = []
    seen = set()

    for record in records:

        key = (
            record[
                "degree"
            ].lower().strip(),

            record[
                "institution"
            ].lower().strip(),

            record[
                "score"
            ].lower().strip(),

            record[
                "duration"
            ].lower().strip(),
        )

        if key in seen:
            continue

        seen.add(
            key
        )

        cleaned_records.append(
            record
        )

    return cleaned_records


# Backward-compatible alias
extract_education_details = (
    extract_education
)


# =========================================================
# OPTIONAL MANUAL TEST
# =========================================================

if __name__ == "__main__":

    sample = """
    EDUCATION
    CVR College of Engineering, Hyderabad Nov 2022 - Apr 2026
    Bachelor of Technology in Electronics and Communication Engineering
    CGPA: 8.4 / 10.0
    """

    print(
        extract_education(
            sample
        )
    )