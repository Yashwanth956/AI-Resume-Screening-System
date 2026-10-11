import re
from datetime import datetime


# =========================================================
# EXPERIENCE HEADERS
# =========================================================

EXPERIENCE_HEADERS = {
    "experience",
    "work experience",
    "professional experience",
    "employment",
    "employment history",
    "work history",
    "career experience",
    "career history",
}


# =========================================================
# SECTION END HEADERS
# =========================================================

EXPERIENCE_END_HEADERS = {
    "education",

    "skills",
    "technical skills",
    "core skills",

    "projects",
    "project",
    "academic projects",

    "certification",
    "certifications",
    "certificate",
    "certificates",

    "achievements",
    "achievement",

    "publications",

    "strengths",
    "soft skills",

    "positions of responsibility",

    "extracurricular",
    "extracurricular activities",

    "interests",
    "hobbies",

    "references",
    "declaration",
}


# =========================================================
# KNOWN JOB TITLES
# =========================================================

KNOWN_JOB_TITLES = [

    # Software
    "Software Engineer",
    "Senior Software Engineer",
    "Software Developer",
    "Senior Software Developer",

    "Python Developer",
    "Java Developer",
    "C++ Developer",

    "Backend Developer",
    "Backend Engineer",

    "Frontend Developer",
    "Frontend Engineer",

    "Full Stack Developer",
    "Full Stack Engineer",

    "Web Developer",

    # AI / Data
    "AI Engineer",
    "AI/ML Engineer",
    "Machine Learning Engineer",

    "Data Scientist",
    "Data Analyst",
    "Data Engineer",

    "NLP Engineer",
    "Computer Vision Engineer",

    # Cloud / DevOps
    "DevOps Engineer",
    "Cloud Engineer",
    "Cloud Developer",
    "Site Reliability Engineer",

    # Security
    "Cybersecurity Analyst",
    "Cyber Security Analyst",
    "Security Analyst",
    "Security Engineer",
    "SOC Analyst",
    "Ethical Hacker",

    # Database
    "Database Developer",
    "Database Administrator",

    # Testing
    "Software Tester",
    "QA Engineer",
    "QA Analyst",
    "Test Engineer",
    "Automation Test Engineer",

    # Mobile
    "Android Developer",
    "Flutter Developer",
    "Mobile Application Developer",

    # Business
    "Business Analyst",
    "Project Manager",
    "Product Manager",

    # Other engineering
    "Mechanical Engineer",
    "Mechanical Design Engineer",
    "Manufacturing Engineer",
    "Civil Engineer",
    "Electrical Engineer",
    "Electronics Engineer",

    # Entry roles
    "Graduate Engineer Trainee",
    "Associate Software Engineer",
    "Junior Software Engineer",
    "Junior Developer",

    # Internships
    "Software Engineer Intern",
    "Software Developer Intern",
    "Python Developer Intern",
    "Machine Learning Intern",
    "Data Science Intern",
    "Data Analyst Intern",
    "Web Developer Intern",
    "Intern",
]


# =========================================================
# DESCRIPTION STARTERS
# =========================================================

DESCRIPTION_STARTERS = (
    "developed ",
    "built ",
    "implemented ",
    "designed ",
    "created ",
    "worked ",
    "managed ",
    "maintained ",
    "collaborated ",
    "performed ",
    "responsible ",
    "used ",
    "utilized ",
    "improved ",
    "optimized ",
    "deployed ",
    "configured ",
    "tested ",
    "supported ",
    "integrated ",
    "automated ",
    "analyzed ",
    "analysed ",
    "led ",
    "handled ",
    "monitored ",
)


# =========================================================
# DATE PATTERNS
# =========================================================

MONTH_NAME = (
    r"(?:"
    r"Jan(?:uary)?|"
    r"Feb(?:ruary)?|"
    r"Mar(?:ch)?|"
    r"Apr(?:il)?|"
    r"May|"
    r"Jun(?:e)?|"
    r"Jul(?:y)?|"
    r"Aug(?:ust)?|"
    r"Sep(?:tember)?|"
    r"Sept(?:ember)?|"
    r"Oct(?:ober)?|"
    r"Nov(?:ember)?|"
    r"Dec(?:ember)?"
    r")"
)

MONTH_YEAR = (
    rf"{MONTH_NAME}"
    rf"\s*[,.-]?\s*"
    rf"20\d{{2}}"
)

NUMERIC_MONTH_YEAR = (
    r"(?:0?[1-9]|1[0-2])"
    r"[/.-]"
    r"20\d{2}"
)

YEAR_ONLY = (
    r"20\d{2}"
)

DATE_TOKEN = (
    rf"(?:"
    rf"{MONTH_YEAR}|"
    rf"{NUMERIC_MONTH_YEAR}|"
    rf"{YEAR_ONLY}"
    rf")"
)

END_DATE_TOKEN = (
    rf"(?:"
    rf"Present|"
    rf"Current|"
    rf"Now|"
    rf"{DATE_TOKEN}"
    rf")"
)


DATE_RANGE_PATTERN = re.compile(

    rf"(?P<start>{DATE_TOKEN})"

    rf"\s*"

    rf"(?:-|–|—|to)"

    rf"\s*"

    rf"(?P<end>{END_DATE_TOKEN})",

    re.IGNORECASE
)


# =========================================================
# MONTH LOOKUP
# =========================================================

MONTHS = {
    "jan": 1,
    "january": 1,

    "feb": 2,
    "february": 2,

    "mar": 3,
    "march": 3,

    "apr": 4,
    "april": 4,

    "may": 5,

    "jun": 6,
    "june": 6,

    "jul": 7,
    "july": 7,

    "aug": 8,
    "august": 8,

    "sep": 9,
    "sept": 9,
    "september": 9,

    "oct": 10,
    "october": 10,

    "nov": 11,
    "november": 11,

    "dec": 12,
    "december": 12,
}


# =========================================================
# NORMALIZE SECTION HEADING
# =========================================================

def normalize_heading(line):

    if not line:
        return ""

    value = str(
        line
    ).strip().lower()

    value = value.rstrip(
        ":|-"
    )

    value = re.sub(
        r"[^a-z0-9 ]+",
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
# CLEAN TEXT
# =========================================================

def clean_text(text):

    if not text:
        return ""

    text = str(
        text
    )

    text = text.replace(
        "\r\n",
        "\n"
    )

    text = text.replace(
        "\r",
        "\n"
    )

    text = text.replace(
        "\xa0",
        " "
    )

    text = text.replace(
        "\u00ad",
        ""
    )

    text = re.sub(
        r"\(cid:\d+\)",
        " ",
        text
    )

    # Fix PDF word splitting:
    #
    # develop-
    # ment
    #
    # -> development

    text = re.sub(
        r"([A-Za-z])-\s*\n\s*([a-z])",
        r"\1\2",
        text
    )

    # Horizontal spaces only.
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


# =========================================================
# EXTRACT EXPERIENCE SECTION
# =========================================================

def extract_experience_section(text):

    if not text:
        return ""

    cleaned = clean_text(
        text
    )

    lines = [
        line.strip()
        for line in cleaned.splitlines()
        if line.strip()
    ]

    start = -1

    for index, line in enumerate(
        lines
    ):

        heading = normalize_heading(
            line
        )

        if heading in EXPERIENCE_HEADERS:

            start = index

            break

    # -----------------------------------------------------
    # No experience section found.
    #
    # Very important:
    # Do NOT use Education dates as work experience.
    # -----------------------------------------------------

    if start == -1:
        return ""

    end = len(
        lines
    )

    for index in range(
        start + 1,
        len(lines)
    ):

        heading = normalize_heading(
            lines[index]
        )

        if heading in EXPERIENCE_END_HEADERS:

            end = index

            break

    return "\n".join(
        lines[
            start + 1:end
        ]
    ).strip()


# =========================================================
# EXPLICIT/STATED EXPERIENCE
# =========================================================

def extract_stated_years(text):

    if not text:
        return 0.0

    patterns = [

        # 3 years of experience
        r"\b(\d+(?:\.\d+)?)\s*\+?\s*years?"
        r"\s+(?:of\s+)?experience\b",

        # 3+ years experience
        r"\b(\d+(?:\.\d+)?)\s*\+\s*years?"
        r"\s+experience\b",

        # experience: 3 years
        r"\bexperience\s*[:\-]?\s*"
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\b",

        # 3 yrs of experience
        r"\b(\d+(?:\.\d+)?)\s*\+?\s*yrs?"
        r"\s+(?:of\s+)?experience\b",
    ]

    values = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for value in matches:

            try:

                values.append(
                    float(value)
                )

            except ValueError:
                pass

    if not values:
        return 0.0

    return max(
        values
    )


# =========================================================
# PARSE DATE
# =========================================================

def parse_date(
    value,
    is_end=False
):

    if not value:
        return None

    value = str(
        value
    ).strip()

    lower = value.lower()

    # -----------------------------------------------------
    # PRESENT
    # -----------------------------------------------------

    if lower in {
        "present",
        "current",
        "now",
    }:

        today = datetime.now()

        return datetime(
            today.year,
            today.month,
            1
        )

    # -----------------------------------------------------
    # MONTH NAME + YEAR
    #
    # Jan 2024
    # January 2024
    # -----------------------------------------------------

    match = re.search(

        rf"(?P<month>{MONTH_NAME})"
        rf"\s*[,.-]?\s*"
        rf"(?P<year>20\d{{2}})",

        value,

        flags=re.IGNORECASE
    )

    if match:

        month_name = (
            match.group(
                "month"
            )
            .lower()
        )

        year = int(
            match.group(
                "year"
            )
        )

        month = MONTHS.get(
            month_name
        )

        # Handle Sept separately.
        if month is None:

            short = month_name[:3]

            month = MONTHS.get(
                short
            )

        if month:

            return datetime(
                year,
                month,
                1
            )

    # -----------------------------------------------------
    # MM/YYYY
    # -----------------------------------------------------

    match = re.search(
        r"\b"
        r"(?P<month>0?[1-9]|1[0-2])"
        r"[/.-]"
        r"(?P<year>20\d{2})"
        r"\b",
        value
    )

    if match:

        return datetime(
            int(
                match.group(
                    "year"
                )
            ),
            int(
                match.group(
                    "month"
                )
            ),
            1
        )

    # -----------------------------------------------------
    # YEAR ONLY
    #
    # For:
    #
    # 2022 - 2024
    #
    # start = Jan 2022
    # end   = Dec 2024
    # -----------------------------------------------------

    match = re.fullmatch(
        r"\s*(20\d{2})\s*",
        value
    )

    if match:

        year = int(
            match.group(1)
        )

        month = (
            12
            if is_end
            else 1
        )

        return datetime(
            year,
            month,
            1
        )

    return None


# =========================================================
# EXTRACT DATE RANGES
# =========================================================



# =========================================================
# NON-EMPLOYMENT / CAREER-BREAK FILTER
# =========================================================

NON_EMPLOYMENT_MARKERS = (
    "career break",
    "career gap",
    "employment gap",
    "gap in employment",
    "personal break",
    "planned break",
    "break in career",
    "unemployed",
    "between jobs",
)


def exclude_non_employment_ranges(
    experience_text,
    date_ranges
):

    if not experience_text or not date_ranges:
        return date_ranges or []

    lines = [
        line.strip()
        for line in experience_text.splitlines()
        if line.strip()
    ]

    kept_ranges = []

    for item in date_ranges:

        date_text = str(
            item.get(
                "text",
                ""
            )
        ).strip()

        if not date_text:
            kept_ranges.append(item)
            continue

        matched_index = -1

        for index, line in enumerate(lines):

            if date_text.lower() in line.lower():
                matched_index = index
                break

        if matched_index == -1:
            kept_ranges.append(item)
            continue

        context_lines = [
            lines[matched_index]
        ]

        if matched_index > 0:
            context_lines.insert(
                0,
                lines[matched_index - 1]
            )

        context = " ".join(
            context_lines
        ).lower()

        is_non_employment = any(
            marker in context
            for marker in NON_EMPLOYMENT_MARKERS
        )

        if is_non_employment:
            continue

        kept_ranges.append(item)

    return kept_ranges


def extract_date_ranges(
    experience_text
):

    if not experience_text:

        return []

    ranges = []

    seen = set()

    for match in DATE_RANGE_PATTERN.finditer(
        experience_text
    ):

        start_text = match.group(
            "start"
        )

        end_text = match.group(
            "end"
        )

        start = parse_date(
            start_text,
            is_end=False
        )

        end = parse_date(
            end_text,
            is_end=True
        )

        if not start or not end:
            continue

        # Invalid date range
        if start > end:
            continue

        # Avoid future end dates
        now = datetime.now()

        current_month = datetime(
            now.year,
            now.month,
            1
        )

        if end > current_month:

            end = current_month

        text_value = match.group(
            0
        ).strip()

        key = (
            start.year,
            start.month,
            end.year,
            end.month
        )

        if key in seen:
            continue

        seen.add(
            key
        )

        ranges.append(
            {
                "start": start,
                "end": end,
                "text": text_value,
                "present": (
                    end_text.lower()
                    in {
                        "present",
                        "current",
                        "now",
                    }
                )
            }
        )

    return ranges


# =========================================================
# MONTH INDEX
# =========================================================

def month_index(date_value):

    return (
        date_value.year * 12
        + date_value.month
    )


# =========================================================
# CALCULATE EXPERIENCE
#
# IMPORTANT:
#
# Uses UNION of employment periods.
#
# Example:
#
# Jan 2023 - Dec 2024
# Jun 2024 - Jun 2025
#
# The overlapping months are counted only once.
# =========================================================

def calculate_date_experience(
    date_ranges
):

    if not date_ranges:
        return 0.0

    intervals = []

    for item in date_ranges:

        start = item.get(
            "start"
        )

        end = item.get(
            "end"
        )

        if not start or not end:
            continue

        start_value = month_index(
            start
        )

        end_value = month_index(
            end
        )

        if end_value < start_value:
            continue

        intervals.append(
            (
                start_value,
                end_value
            )
        )

    if not intervals:
        return 0.0

    intervals.sort(
        key=lambda item: item[0]
    )

    merged = []

    current_start = intervals[0][0]
    current_end = intervals[0][1]

    for start, end in intervals[1:]:

        # Overlap or directly adjacent
        if start <= current_end + 1:

            current_end = max(
                current_end,
                end
            )

        else:

            merged.append(
                (
                    current_start,
                    current_end
                )
            )

            current_start = start
            current_end = end

    merged.append(
        (
            current_start,
            current_end
        )
    )

    total_months = 0

    for start, end in merged:

        # Inclusive month counting:
        #
        # Jan 2024 - Dec 2024
        # = 12 months
        total_months += (
            end - start + 1
        )

    return round(
        total_months / 12,
        2
    )


# =========================================================
# DESCRIPTION LINE
# =========================================================

def is_description_line(line):

    if not line:
        return False

    value = line.strip()

    value = re.sub(
        r"^[•●▪◦∗*-]+\s*",
        "",
        value
    )

    return value.lower().startswith(
        DESCRIPTION_STARTERS
    )


# =========================================================
# GENERIC JOB TITLE CHECK
# =========================================================

def looks_like_job_title(line):

    if not line:
        return False

    value = line.strip()

    if not value:
        return False

    if is_description_line(
        value
    ):
        return False

    if DATE_RANGE_PATTERN.search(
        value
    ):
        value = DATE_RANGE_PATTERN.sub(
            "",
            value
        ).strip(
            " |-–—,"
        )

    if not value:
        return False

    if len(
        value.split()
    ) > 12:
        return False

    if value.endswith(
        (
            ".",
            ";",
            "!",
            "?",
        )
    ):
        return False

    title_words = (
        "engineer",
        "developer",
        "analyst",
        "scientist",
        "consultant",
        "manager",
        "specialist",
        "administrator",
        "architect",
        "tester",
        "intern",
        "associate",
        "lead",
        "executive",
        "trainee",
    )

    lower = value.lower()

    return any(
        word in lower
        for word in title_words
    )


# =========================================================
# EXTRACT JOB TITLES
# =========================================================

def extract_job_titles(
    experience_text
):

    if not experience_text:
        return []

    titles = []

    # -----------------------------------------------------
    # Known titles
    # -----------------------------------------------------

    for title in KNOWN_JOB_TITLES:

        if re.search(
            r"\b"
            + re.escape(title)
            + r"\b",
            experience_text,
            flags=re.IGNORECASE
        ):

            if title not in titles:

                titles.append(
                    title
                )

    # -----------------------------------------------------
    # Unknown titles
    # -----------------------------------------------------

    for raw_line in experience_text.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        # Remove date range if same line.
        line_without_date = (
            DATE_RANGE_PATTERN.sub(
                "",
                line
            )
            .strip(
                " |-–—,"
            )
        )

        if not line_without_date:
            continue

        if looks_like_job_title(
            line_without_date
        ):

            # Split:
            #
            # Software Engineer | ABC Technologies
            #
            # Prefer title-looking component.
            parts = re.split(
                r"\s*[|@]\s*",
                line_without_date
            )

            candidate = ""

            for part in parts:

                if looks_like_job_title(
                    part
                ):

                    candidate = part.strip()

                    break

            if not candidate:

                candidate = (
                    line_without_date
                )

            key = candidate.lower()

            if not any(
                existing.lower() == key
                for existing in titles
            ):

                titles.append(
                    candidate
                )

    return titles


# =========================================================
# EXPERIENCE RECORDS
# =========================================================

def extract_experience_records(
    experience_text,
    date_ranges
):

    if not experience_text:
        return []

    records = []

    lines = [
        line.strip()
        for line in experience_text.splitlines()
        if line.strip()
    ]

    for item in date_ranges:

        date_text = item.get(
            "text",
            ""
        )

        job_title = ""

        # -------------------------------------------------
        # Try to find the date on a line and inspect
        # surrounding lines.
        # -------------------------------------------------

        matched_index = -1

        for index, line in enumerate(
            lines
        ):

            if (
                date_text
                and date_text.lower()
                in line.lower()
            ):

                matched_index = index
                break

        if matched_index >= 0:

            current_line = lines[
                matched_index
            ]

            without_date = (
                DATE_RANGE_PATTERN.sub(
                    "",
                    current_line
                )
                .strip(
                    " |-–—,"
                )
            )

            if looks_like_job_title(
                without_date
            ):

                job_title = (
                    without_date
                )

            # Search two lines above.
            if not job_title:

                start_index = max(
                    0,
                    matched_index - 2
                )

                previous_lines = lines[
                    start_index:
                    matched_index
                ]

                for previous in reversed(
                    previous_lines
                ):

                    if looks_like_job_title(
                        previous
                    ):

                        job_title = (
                            previous
                        )

                        break

        records.append(
            {
                "job_title": job_title,

                "date_range": date_text,

                "start": item[
                    "start"
                ].strftime(
                    "%Y-%m"
                ),

                "end": (
                    "Present"
                    if item.get(
                        "present"
                    )
                    else item[
                        "end"
                    ].strftime(
                        "%Y-%m"
                    )
                )
            }
        )

    return records


# =========================================================
# EMPTY RESULT
# =========================================================

def empty_experience():

    return {
        "total_years": 0.0,
        "stated_years": 0.0,
        "calculated_years": 0.0,

        "date_ranges": [],

        "job_titles": [],

        "records": [],

        "experience_text": "",

        "has_experience_section": False,
    }


# =========================================================
# MAIN EXPERIENCE EXTRACTION
# =========================================================

def extract_experience(text):

    if not text:

        return empty_experience()

    # =====================================================
    # CLEAN RESUME
    # =====================================================

    cleaned_resume = clean_text(
        text
    )


    # =====================================================
    # EXPLICIT EXPERIENCE
    #
    # This may appear in profile/summary:
    #
    # "Software engineer with 4 years of experience"
    # =====================================================

    stated_years = (
        extract_stated_years(
            cleaned_resume
        )
    )


    # =====================================================
    # EXPERIENCE SECTION ONLY
    # =====================================================

    experience_text = (
        extract_experience_section(
            cleaned_resume
        )
    )


    # =====================================================
    # NO EXPERIENCE SECTION
    # =====================================================

    if not experience_text:

        return {
            "total_years": round(
                stated_years,
                2
            ),

            "stated_years": round(
                stated_years,
                2
            ),

            "calculated_years": 0.0,

            "date_ranges": [],

            "job_titles": [],

            "records": [],

            "experience_text": "",

            "has_experience_section": False,
        }


    # =====================================================
    # DATE RANGES ONLY FROM EXPERIENCE SECTION
    # =====================================================

    date_ranges = (
        extract_date_ranges(
            experience_text
        )
    )

    # Remove declared non-employment periods before experience calculation.
    date_ranges = exclude_non_employment_ranges(
        experience_text,
        date_ranges
    )


    # =====================================================
    # CALCULATED YEARS
    # =====================================================

    calculated_years = (
        calculate_date_experience(
            date_ranges
        )
    )


    # =====================================================
    # JOB TITLES
    # =====================================================

    job_titles = (
        extract_job_titles(
            experience_text
        )
    )


    # =====================================================
    # EXPERIENCE RECORDS
    # =====================================================

    records = (
        extract_experience_records(
            experience_text,
            date_ranges
        )
    )


    # =====================================================
    # FINAL EXPERIENCE
    #
    # If both are available, use the larger value.
    #
    # Example:
    #
    # Summary:
    # "4+ years of experience"
    #
    # Resume may list only recent 3.5 years of roles.
    # =====================================================

    if (
        stated_years > 0
        and calculated_years > 0
    ):

        total_years = max(
            stated_years,
            calculated_years
        )

    elif calculated_years > 0:

        total_years = (
            calculated_years
        )

    else:

        total_years = (
            stated_years
        )


    # =====================================================
    # DEBUG
    # =====================================================

    print()
    print(
        "========== EXPERIENCE PARSER =========="
    )

    print(
        "Experience section found:",
        bool(
            experience_text
        )
    )

    print(
        "Stated years:",
        stated_years
    )

    print(
        "Calculated years:",
        calculated_years
    )

    print(
        "Total years:",
        total_years
    )

    print(
        "Date ranges:",
        [
            item["text"]
            for item in date_ranges
        ]
    )

    print(
        "Job titles:",
        job_titles
    )

    print(
        "Records:",
        records
    )

    print(
        "======================================="
    )


    # =====================================================
    # RETURN
    # =====================================================

    return {

        "total_years": round(
            total_years,
            2
        ),

        "stated_years": round(
            stated_years,
            2
        ),

        "calculated_years": round(
            calculated_years,
            2
        ),

        "date_ranges": [
            item["text"]
            for item in date_ranges
        ],

        "job_titles": job_titles,

        "records": records,

        "experience_text":
            experience_text,

        "has_experience_section": True,
    }