import re


print("================================================")
print("PROJECT PARSER LOADED")
print("PROJECT.PY MODULE:", __name__)
print("================================================")


# =========================================================
# PROJECT SECTION HEADERS
# =========================================================

PROJECT_HEADERS = {
    "project",
    "projects",
    "academic project",
    "academic projects",
    "personal project",
    "personal projects",
    "technical project",
    "technical projects",
    "major project",
    "major projects",
    "key projects",
    "selected projects",
    "project experience",
}


# =========================================================
# PROJECT SECTION END HEADERS
# =========================================================

PROJECT_END_HEADERS = {
    "experience",
    "work experience",
    "professional experience",
    "employment",
    "internship",
    "internships",

    "education",

    "skill",
    "skills",
    "technical skill",
    "technical skills",

    "certificate",
    "certificates",
    "certification",
    "certifications",

    "achievement",
    "achievements",
    "achievements & certifications",
    "achievements and certifications",

    "position of responsibility",
    "positions of responsibility",

    "soft skills",
    "strengths",

    "extracurricular",
    "extracurricular activities",
    "extra curricular",
    "extra curricular activities",

    "leadership",
    "interests",
    "hobbies",
    "publications",
    "references",
    "declaration",
}


# =========================================================
# DESCRIPTION STARTERS
# =========================================================

DESCRIPTION_STARTERS = (
    "built ",
    "developed ",
    "implemented ",
    "designed ",
    "created ",
    "engineered ",
    "integrated ",
    "enabled ",
    "utilized ",
    "used ",
    "achieved ",
    "performed ",
    "managed ",
    "deployed ",
    "trained ",
    "evaluated ",
    "automated ",
    "contributed ",
    "supported ",
    "monitored ",
    "reduced ",
    "improved ",
    "generated ",
    "applied ",
    "configured ",
    "leveraged ",
    "ensured ",
    "building ",
    "implementing ",
    "deploying ",
    "developing ",
)


# =========================================================
# PROJECT TITLE KEYWORDS
# =========================================================

PROJECT_KEYWORDS = (
    "system",
    "application",
    "app",
    "platform",
    "dashboard",
    "website",
    "builder",
    "clone",
    "whiteboard",
    "management",
    "monitoring",
    "prediction",
    "predictive",
    "forecast",
    "forecasting",
    "classification",
    "detection",
    "optimization",
    "optimisation",
    "analyser",
    "analyzer",
    "visualization",
    "recommendation",
    "maintenance",
    "biometric",
    "fingerprint",
    "resume",
    "inventory",
    "healthcare",
    "storyboard",
    "waste",
    "disease",
    "carbon",
    "travel",
    "notes",
    "employee",
    "siem",
    "security",
    "expense",
    "extraction",
    "workforce",
)


# =========================================================
# TECHNOLOGY ALIASES
# =========================================================

TECHNOLOGY_ALIASES = {

    # Programming
    "python": "Python",
    "java": "Java",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "kotlin": "Kotlin",
    "c++": "C++",

    # Web
    "html": "HTML",
    "html5": "HTML",
    "css": "CSS",
    "css3": "CSS",

    "react": "React",
    "react.js": "React",
    "reactjs": "React",

    "next.js": "Next.js",
    "nextjs": "Next.js",

    "node.js": "Node.js",
    "nodejs": "Node.js",

    "express": "Express.js",
    "express.js": "Express.js",
    "expressjs": "Express.js",

    "flask": "Flask",
    "django": "Django",
    "fastapi": "FastAPI",

    "spring": "Spring",
    "spring boot": "Spring Boot",
    "springboot": "Spring Boot",
    "spring security": "Spring Security",

    "tailwind css": "Tailwind CSS",

    # Database
    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mongodb": "MongoDB",
    "mongoose": "Mongoose",
    "oracle": "Oracle",

    # Backend/API
    "rest api": "REST API",
    "rest apis": "REST API",
    "restful api": "REST API",
    "restful apis": "REST API",

    "jwt": "JWT",
    "jwt authentication": "JWT Authentication",

    "socket.io": "Socket.io",
    "socketio": "Socket.io",

    "passport.js": "Passport.js",
    "oauth": "OAuth",
    "google oauth": "Google OAuth",

    # AI / ML
    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",
    "artificialintelligence": "Artificial Intelligence",

    "ml": "Machine Learning",
    "machine learning": "Machine Learning",

    "deep learning": "Deep Learning",

    "data science": "Data Science",
    "data visualization": "Data Visualization",

    "nlp": "NLP",
    "natural language processing": "NLP",

    "computer vision": "Computer Vision",

    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "keras": "Keras",

    "scikit-learn": "Scikit-learn",
    "scikit learn": "Scikit-learn",

    "numpy": "NumPy",
    "pandas": "Pandas",
    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",

    "opencv": "OpenCV",

    "hugging face": "Hugging Face",
    "huggingface": "Hugging Face",
    "transformers": "Transformers",

    "stable diffusion": "Stable Diffusion",

    "xgboost": "XGBoost",

    "k-means": "K-Means",
    "kmeans": "K-Means",

    "cnn": "CNN",
    "lstm": "LSTM",
    "bi-lstm": "Bi-LSTM",
    "bilstm": "Bi-LSTM",

    "vgg16": "VGG16",
    "unet": "UNet",
    "resnet": "ResNet",
    "resnet-50": "ResNet-50",
    "resnet 50": "ResNet-50",

    # Security
    "cybersecurity": "Cybersecurity",
    "cyber security": "Cybersecurity",
    "network security": "Network Security",

    "siem": "SIEM",

    "splunk": "Splunk",
    "wireshark": "Wireshark",
    "nmap": "Nmap",
    "burp suite": "Burp Suite",
    "metasploit": "Metasploit",
    "nessus": "Nessus",

    "ids": "IDS",
    "ips": "IPS",

    "linux": "Linux",
    "bash": "Bash",

    # Other
    "iot": "IoT",
    "gsm": "GSM",

    "mern": "MERN Stack",
    "mern stack": "MERN Stack",

    "full stack": "Full Stack",

    "predictive analytics": "Predictive Analytics",
    "system architecture": "System Architecture",

    "biometrics": "Biometrics",
    "image processing": "Image Processing",
}


# =========================================================
# TECHNOLOGY REGEX
# =========================================================

TECHNOLOGY_KEYS = sorted(
    TECHNOLOGY_ALIASES.keys(),
    key=len,
    reverse=True
)


TECHNOLOGY_PATTERN = re.compile(
    r"(?<![A-Za-z0-9+#.-])("
    + "|".join(
        re.escape(item)
        for item in TECHNOLOGY_KEYS
    )
    + r")(?![A-Za-z0-9+#.-])",
    re.IGNORECASE
)


# =========================================================
# BULLETS
# =========================================================

BULLET_CHARS = (
    "•",
    "●",
    "▪",
    "◦",
    "∗",
    "*",
)


# =========================================================
# UNIQUE LIST
# =========================================================

def unique_list(values):

    result = []
    seen = set()

    for value in values or []:

        if value is None:
            continue

        value = str(value).strip()

        if not value:
            continue

        key = value.lower()

        if key not in seen:

            seen.add(key)
            result.append(value)

    return result


# =========================================================
# SECTION NORMALIZATION
# =========================================================

def normalize_section_name(line):

    if not line:
        return ""

    value = str(line).strip().lower()

    value = value.rstrip(
        ":|"
    )

    value = re.sub(
        r"[^a-z0-9& ]+",
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
# TEXT CLEANING
# =========================================================

def clean_text(text):

    if not text:
        return ""

    text = str(text)

    # -----------------------------------------------------
    # Basic PDF cleanup
    # -----------------------------------------------------

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

    # Weird PDF extraction characters
    text = text.replace(
        "\ufffe",
        ""
    )

    text = text.replace(
        "\ufffd",
        ""
    )

    # -----------------------------------------------------
    # Remove CID markers
    # -----------------------------------------------------

    text = re.sub(
        r"\(cid:\d+\)",
        " ",
        text
    )

    # -----------------------------------------------------
    # CRITICAL FIX:
    #
    # secu-
    # rity
    #
    # becomes:
    #
    # security
    #
    # Also:
    #
    # min-
    # imize
    #
    # -> minimize
    # -----------------------------------------------------

    text = re.sub(
        r"([A-Za-z])-\s*\n\s*([a-z])",
        r"\1\2",
        text
    )

    # -----------------------------------------------------
    # Put inline bullets onto their own lines
    # -----------------------------------------------------

    text = re.sub(
        r"[ \t]*([•●▪◦∗])\s*",
        r"\n\1 ",
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
# PAGE NUMBER
# =========================================================

def is_page_number(line):

    if not line:
        return False

    return bool(
        re.fullmatch(
            r"(?:page\s*)?\d+",
            line.strip(),
            flags=re.IGNORECASE
        )
    )


# =========================================================
# TECHNOLOGY EXTRACTION
# =========================================================

def extract_technologies(text):

    if not text:
        return []

    technologies = []

    text_value = str(text)

    for match in TECHNOLOGY_PATTERN.finditer(
        text_value
    ):

        raw = match.group(1).lower()

        # =================================================
        # CONTEXT FILTERS
        # =================================================

        # Venu resume:
        #
        # "SQL Injection"
        #
        # SQL here is an attack name, not necessarily
        # a technology used in the project.
        if raw == "sql":

            after_match = text_value[
                match.end():
                match.end() + 25
            ]

            if re.match(
                r"\s+injection\b",
                after_match,
                flags=re.IGNORECASE
            ):
                continue

        technology = TECHNOLOGY_ALIASES.get(
            raw
        )

        if technology:
            technologies.append(
                technology
            )

    return unique_list(
        technologies
    )

# =========================================================
# TECHNOLOGY LABEL
# =========================================================

def is_technology_label_line(line):

    if not line:
        return False

    return bool(
        re.match(
            r"^(?:technologies?|tech stack|stack|tech)\s*:",
            line.strip(),
            flags=re.IGNORECASE
        )
    )


# =========================================================
# TECHNOLOGY-ONLY LINE
# =========================================================

def is_technology_only_line(line):

    if not line:
        return False

    value = line.strip()

    if not extract_technologies(
        value
    ):
        return False

    # GitHub / demo are not technologies
    working = re.sub(
        r"\b(?:github|live demo|demo)\b",
        "",
        value,
        flags=re.IGNORECASE
    )

    # Remove all recognized technology aliases.
    working = TECHNOLOGY_PATTERN.sub(
        "",
        working
    )

    # Remove separators.
    working = re.sub(
        r"[\s|,/;:+&().\-–—]+",
        "",
        working
    )

    return working == ""


# =========================================================
# CATEGORY LINE
# =========================================================

def is_category_line(line):

    if not line:
        return False

    value = line.strip()

    if "/" not in value:
        return False

    parts = [
        part.strip()
        for part in value.split("/")
        if part.strip()
    ]

    if len(parts) < 2:
        return False

    technology_parts = 0

    for part in parts:

        if extract_technologies(
            part
        ):
            technology_parts += 1

    return technology_parts >= 2


# =========================================================
# BULLET HELPERS
# =========================================================

def is_bullet_line(line):

    if not line:
        return False

    return line.strip().startswith(
        BULLET_CHARS
    )


def is_standalone_bullet(line):

    if not line:
        return False

    return line.strip() in BULLET_CHARS


def remove_bullet(line):

    if not line:
        return ""

    value = str(line).strip()

    value = re.sub(
        r"^[•●▪◦∗*]+\s*",
        "",
        value
    )

    return value.strip()


# =========================================================
# DESCRIPTION
# =========================================================

def clean_description(line):

    if not line:
        return ""

    value = remove_bullet(
        line
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    value = re.sub(
        r"\s+([,.!?;:])",
        r"\1",
        value
    )

    return value.strip()


def starts_description(line):

    if not line:
        return False

    value = remove_bullet(
        line
    ).strip()

    lower = value.lower()

    return lower.startswith(
        DESCRIPTION_STARTERS
    )

# =========================================================
# PROJECT DATE RANGES
# =========================================================

MONTH_NAME_PATTERN = (
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


DATE_RANGE_PATTERNS = (

    # January 2025 - August 2025
    # Oct 2024 - Present

    rf"\b"
    rf"{MONTH_NAME_PATTERN}"
    rf"\s+20\d{{2}}"
    rf"\s*[–—-]\s*"
    rf"(?:"
    rf"{MONTH_NAME_PATTERN}\s+20\d{{2}}"
    rf"|Present"
    rf"|Current"
    rf"|Ongoing"
    rf")"
    rf"\b",

    # 01/2025 - 08/2025
    # 01/2025 - Present

    r"\b"
    r"\d{1,2}/\d{4}"
    r"\s*[–—-]\s*"
    r"(?:"
    r"\d{1,2}/\d{4}"
    r"|Present"
    r"|Current"
    r"|Ongoing"
    r")"
    r"\b",

    # 2024 - 2025
    # 2024 - Present

    r"\b"
    r"\d{4}"
    r"\s*[–—-]\s*"
    r"(?:"
    r"\d{4}"
    r"|Present"
    r"|Current"
    r"|Ongoing"
    r")"
    r"\b",
)

def contains_date_range(line):

    if not line:
        return False

    for pattern in DATE_RANGE_PATTERNS:

        if re.search(
            pattern,
            line,
            flags=re.IGNORECASE
        ):
            return True

    return False

def remove_project_date(line):

    if not line:
        return ""

    value = str(
        line
    ).strip()

    for pattern in DATE_RANGE_PATTERNS:

        value = re.sub(
            pattern,
            "",
            value,
            flags=re.IGNORECASE
        )

    # Clean remaining separators.
    #
    # Internal Knowledge Assistant |
    #
    # becomes:
    #
    # Internal Knowledge Assistant

    value = re.sub(
        r"\s*\|\s*$",
        "",
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip(
        " -–—|:"
    )


# =========================================================
# REMOVE LINK TEXT
# =========================================================

def remove_project_links(value):

    value = re.sub(
        r"\s*(?:[|—–-]\s*)?\bGitHub\b.*$",
        "",
        value,
        flags=re.IGNORECASE
    )

    value = re.sub(
        r"\s*(?:[|—–-]\s*)?\bLive\s+Demo\b.*$",
        "",
        value,
        flags=re.IGNORECASE
    )

    return value.strip()


# =========================================================
# REMOVE TRAILING TECH FROM FIRST TITLE PART
# =========================================================

def remove_trailing_technology_from_title(
    title
):

    if not title:
        return "", []

    working = title.strip()

    found = []

    aliases = sorted(
        TECHNOLOGY_ALIASES.keys(),
        key=len,
        reverse=True
    )

    changed = True

    while changed:

        changed = False

        for alias in aliases:

            # Avoid removing very short aliases
            # such as AI / ML from normal titles.
            if len(alias) <= 2:
                continue

            pattern = re.compile(
                r"\s+"
                + re.escape(alias)
                + r"\s*$",
                re.IGNORECASE
            )

            match = pattern.search(
                working
            )

            if not match:
                continue

            technology = (
                TECHNOLOGY_ALIASES[
                    alias
                ]
            )

            found.append(
                technology
            )

            working = working[
                :match.start()
            ].strip(
                " -–—|"
            )

            changed = True

            break

    return (
        working,
        unique_list(found)
    )


# =========================================================
# CLEAN PROJECT TITLE
# =========================================================

def clean_project_title(title):

    if not title:
        return ""

    value = remove_project_date(
        title
    )

    value = remove_bullet(
        value
    )

    value = remove_project_links(
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip(
        " |—–-:"
    )


# =========================================================
# SPLIT TITLE + TECHNOLOGIES
# =========================================================

def split_title_and_technologies(line):

    if not line:
        return "", []

    value = remove_project_date(
        line.strip()
    )

    technologies = []

    # -----------------------------------------------------
    # Pipe format
    #
    # Workforce Twin ... HTML | JavaScript | Flask
    #
    # Expense ... Spring Boot | React | MySQL |
    # -----------------------------------------------------

    if "|" in value:

        parts = [
            part.strip()
            for part in value.split("|")
            if part.strip()
        ]

        if parts:

            first_part = parts[0]

            first_part, trailing_tech = (
                remove_trailing_technology_from_title(
                    first_part
                )
            )

            technologies.extend(
                trailing_tech
            )

            for part in parts[1:]:

                if part.lower() in {
                    "github",
                    "live demo",
                    "demo",
                }:
                    continue

                technologies.extend(
                    extract_technologies(
                        part
                    )
                )

            title = clean_project_title(
                first_part
            )

            # Technologies may also be mentioned
            # naturally in title.
            technologies.extend(
                extract_technologies(
                    title
                )
            )

            return (
                title,
                unique_list(
                    technologies
                )
            )

    # -----------------------------------------------------
    # Non-pipe format
    # -----------------------------------------------------

    title = clean_project_title(
        value
    )

    technologies.extend(
        extract_technologies(
            title
        )
    )

    return (
        title,
        unique_list(
            technologies
        )
    )


# =========================================================
# EDUCATION-LINE PROTECTION
# =========================================================

def is_academic_line(line):

    if not line:
        return False

    lower = line.lower()

    patterns = (
        "university",
        "junior college",
        "high school",
        "board of intermediate",
        "board of secondary",
        "intermediate education",
        "secondary education",
        "bachelor of technology",
        "b.tech",
        "cgpa",
        "percentage",
    )

    return any(
        pattern in lower
        for pattern in patterns
    )


# =========================================================
# PROJECT TITLE DETECTION
# =========================================================

def is_project_title(line):

    if not line:
        return False

    value = line.strip()

    if not value:
        return False

    lower = value.lower()

    normalized = normalize_section_name(
        value
    )

    if normalized in PROJECT_HEADERS:
        return False

    if normalized in PROJECT_END_HEADERS:
        return False

    if is_page_number(
        value
    ):
        return False

    if is_bullet_line(
        value
    ):
        return False

    if is_standalone_bullet(
        value
    ):
        return False

    if is_technology_label_line(
        value
    ):
        return False

    if is_technology_only_line(
        value
    ):
        return False

    if is_category_line(
        value
    ):
        return False

    if is_academic_line(
        value
    ):
        return False

    if starts_description(
        value
    ):
        return False

    # -----------------------------------------------------
    # Sentence fragments are not project titles.
    #
    # Fixes:
    #
    # extraction.
    # reduction recommendations.
    # impact using charts and dashboards.
    # -----------------------------------------------------

    if value.endswith(
        (
            ".",
            ",",
            ";",
            "!",
            "?",
        )
    ):
        return False

    # -----------------------------------------------------
    # CRITICAL:
    # Lowercase PDF continuation lines are descriptions.
    #
    # Example:
    #
    # rity alerts, implementing rule-based detection...
    #
    # Must NOT become project title.
    # -----------------------------------------------------

    first_alpha = re.search(
        r"[A-Za-z]",
        value
    )

    if (
        first_alpha
        and first_alpha.group(0).islower()
        and "|" not in value
        and not contains_date_range(value)
    ):
        return False

    words = value.split()

    if len(words) > 20:
        return False

    # -----------------------------------------------------
    # Pipe + technology
    # -----------------------------------------------------

    if "|" in value:

        parts = [
            part.strip()
            for part in value.split("|")
            if part.strip()
        ]

        if len(parts) >= 2:

            technology_parts = sum(
                1
                for part in parts[1:]
                if extract_technologies(
                    part
                )
            )

            if technology_parts >= 1:
                return True

    # -----------------------------------------------------
    # GitHub suffix
    # -----------------------------------------------------

    if re.search(
        r"\bgithub\b",
        value,
        flags=re.IGNORECASE
    ):
        return True

    # -----------------------------------------------------
    # Date range
    # -----------------------------------------------------

    if contains_date_range(
        value
    ):

        cleaned = remove_project_date(
            value
        )

        if (
            2
            <= len(cleaned.split())
            <= 16
        ):
            return True

    # -----------------------------------------------------
    # Project vocabulary
    # -----------------------------------------------------

    if any(
        keyword in lower
        for keyword in PROJECT_KEYWORDS
    ):
        return True

    # -----------------------------------------------------
    # Short Title Case fallback
    #
    # Travel Easy
    # Collaborative Whiteboard
    # -----------------------------------------------------

    if 2 <= len(words) <= 8:

        capitalized = sum(
            1
            for word in words
            if word
            and word[0].isupper()
        )

        if capitalized >= 2:
            return True

    return False


# =========================================================
# FIND PROJECT SECTION
# =========================================================

def find_project_section(lines):

    for index, line in enumerate(
        lines
    ):

        normalized = normalize_section_name(
            line
        )

        if normalized in PROJECT_HEADERS:

            return index

    return -1


# =========================================================
# FIND PROJECT END
# =========================================================

def find_project_end(
    lines,
    start
):

    if start < 0:
        return len(lines)

    for index in range(
        start + 1,
        len(lines)
    ):

        normalized = normalize_section_name(
            lines[index]
        )

        if normalized in PROJECT_END_HEADERS:

            return index

    return len(lines)


# =========================================================
# SAVE PROJECT
# =========================================================

def save_project(
    projects,
    project
):

    if not project:
        return

    title = clean_project_title(
        project.get(
            "title",
            ""
        )
    )

    if not title:
        return

    if is_academic_line(
        title
    ):
        return

    if title.endswith(
        (
            ".",
            ",",
            ";",
        )
    ):
        return

    descriptions = unique_list(
        project.get(
            "description",
            []
        )
    )

    technologies = unique_list(
        project.get(
            "technologies",
            []
        )
    )

    # -----------------------------------------------------
    # Extract technologies from title
    # -----------------------------------------------------

    technologies.extend(
        extract_technologies(
            title
        )
    )

    # -----------------------------------------------------
    # Extract technologies from descriptions
    # -----------------------------------------------------

    description_text = " ".join(
        descriptions
    )

    technologies.extend(
        extract_technologies(
            description_text
        )
    )

    technologies = unique_list(
        technologies
    )

    # GitHub isn't project technology.
    technologies = [
        item
        for item in technologies
        if item.lower() != "github"
    ]

    title_key = re.sub(
        r"[^a-z0-9]+",
        " ",
        title.lower()
    ).strip()

    # -----------------------------------------------------
    # Merge duplicate projects
    # -----------------------------------------------------

    for existing in projects:

        existing_key = re.sub(
            r"[^a-z0-9]+",
            " ",
            existing["title"].lower()
        ).strip()

        if existing_key == title_key:

            existing[
                "technologies"
            ] = unique_list(
                existing[
                    "technologies"
                ]
                + technologies
            )

            existing[
                "description"
            ] = unique_list(
                existing[
                    "description"
                ]
                + descriptions
            )

            return

    projects.append(
        {
            "title": title,
            "technologies": technologies,
            "description": descriptions,
        }
    )


# =========================================================
# APPEND DESCRIPTION CONTINUATION
# =========================================================

def append_continuation(
    current,
    new_part
):

    current = current.strip()
    new_part = new_part.strip()

    if not current:
        return new_part

    if not new_part:
        return current

    # Extra safety for PDF hyphenation.
    if current.endswith(
        "-"
    ) and new_part[0].islower():

        return (
            current[:-1]
            + new_part
        )

    return (
        current
        + " "
        + new_part
    )


# =========================================================
# PARSE PROJECTS
# =========================================================

def parse_projects(lines):

    projects = []

    current_project = None
    current_description = ""

    # -----------------------------------------------------
    # Flush description
    # -----------------------------------------------------

    def flush_description():

        nonlocal current_description
        nonlocal current_project

        value = clean_description(
            current_description
        )

        if (
            current_project
            and value
            and value not in current_project[
                "description"
            ]
        ):

            current_project[
                "description"
            ].append(
                value
            )

        current_description = ""

    # -----------------------------------------------------
    # Flush project
    # -----------------------------------------------------

    def flush_project():

        nonlocal current_project

        flush_description()

        if current_project:

            save_project(
                projects,
                current_project
            )

        current_project = None

    # -----------------------------------------------------
    # Parse
    # -----------------------------------------------------

    for raw_line in lines:

        line = str(
            raw_line
        ).strip()

        if not line:
            continue

        normalized = normalize_section_name(
            line
        )

        if normalized in PROJECT_END_HEADERS:

            flush_project()
            break

        if is_page_number(
            line
        ):
            continue

        # -------------------------------------------------
        # Standalone bullet artifact
        # -------------------------------------------------

        if is_standalone_bullet(
            line
        ):
            continue

        # -------------------------------------------------
        # IMPORTANT:
        #
        # Handle technology continuation BEFORE title.
        #
        # Yamini:
        #
        # JWT | REST APIs
        #
        # must belong to Expense Splitter.
        # -------------------------------------------------

        if (
            current_project
            and is_technology_only_line(
                line
            )
        ):

            current_project[
                "technologies"
            ] = unique_list(
                current_project[
                    "technologies"
                ]
                + extract_technologies(
                    line
                )
            )

            continue

        # -------------------------------------------------
        # Technology label
        # -------------------------------------------------

        if (
            current_project
            and is_technology_label_line(
                line
            )
        ):

            current_project[
                "technologies"
            ] = unique_list(
                current_project[
                    "technologies"
                ]
                + extract_technologies(
                    line
                )
            )

            continue

        # -------------------------------------------------
        # Category
        #
        # Data Science/Data Visualization Project
        # -------------------------------------------------

        if (
            current_project
            and is_category_line(
                line
            )
        ):

            current_project[
                "technologies"
            ] = unique_list(
                current_project[
                    "technologies"
                ]
                + extract_technologies(
                    line
                )
            )

            continue

        # -------------------------------------------------
        # NEW PROJECT TITLE
        # -------------------------------------------------

        if is_project_title(
            line
        ):

            flush_project()

            (
                title,
                technologies
            ) = split_title_and_technologies(
                line
            )

            if not title:
                continue

            current_project = {
                "title": title,
                "technologies": technologies,
                "description": [],
            }

            continue

        # Ignore content until first project title.
        if current_project is None:
            continue

        # -------------------------------------------------
        # REAL BULLET
        # -------------------------------------------------

        if is_bullet_line(
            line
        ):

            value = clean_description(
                line
            )

            if not value:
                continue

            flush_description()

            current_description = value

            continue

        # -------------------------------------------------
        # Description starts without bullet
        # -------------------------------------------------

        if starts_description(
            line
        ):

            flush_description()

            current_description = (
                clean_description(
                    line
                )
            )

            continue

        # -------------------------------------------------
        # Wrapped description continuation
        #
        # Venu:
        #
        # security alerts, implementing...
        #
        # Yamini:
        #
        # using agent-based modelling...
        #
        # -------------------------------------------------

        value = clean_description(
            line
        )

        if not value:
            continue

        current_description = (
            append_continuation(
                current_description,
                value
            )
        )

    flush_project()

    return projects


# =========================================================
# PROJECT SECTION TEXT
# =========================================================

def extract_project_section(
    text
):

    if not text:
        return ""

    cleaned_text = clean_text(
        text
    )

    lines = [
        line.strip()
        for line in cleaned_text.splitlines()
        if line.strip()
    ]

    start = find_project_section(
        lines
    )

    if start == -1:
        return ""

    end = find_project_end(
        lines,
        start
    )

    return "\n".join(
        lines[
            start + 1:end
        ]
    )


# =========================================================
# MAIN EXTRACTOR
# =========================================================

def extract_projects(
    text
):

    print()
    print(
        "========== PROJECT EXTRACTION =========="
    )

    if not text:

        print(
            "Empty resume text."
        )

        return []

    cleaned_text = clean_text(
        text
    )

    lines = [
        line.strip()
        for line in cleaned_text.splitlines()
        if line.strip()
    ]

    start = find_project_section(
        lines
    )

    print(
        "Project section start:",
        start
    )

    if start == -1:

        print(
            "PROJECTS section not found."
        )

        return []

    end = find_project_end(
        lines,
        start
    )

    print(
        "Project section end:",
        end
    )

    project_lines = lines[
        start + 1:end
    ]

    print()
    print(
        "========== PROJECT LINES =========="
    )

    for line in project_lines:

        print(
            repr(line)
        )

    print(
        "==================================="
    )

    projects = parse_projects(
        project_lines
    )

    print()
    print(
        "========== EXTRACTED PROJECTS =========="
    )

    for index, project in enumerate(
        projects,
        start=1
    ):

        print()
        print(
            f"Project #{index}"
        )

        print(
            "Title:",
            project["title"]
        )

        print(
            "Technologies:",
            project[
                "technologies"
            ]
        )

        print(
            "Descriptions:"
        )

        for description in project[
            "description"
        ]:

            print(
                " -",
                description
            )

    print(
        "========================================"
    )

    return projects


# =========================================================
# BACKWARD COMPATIBILITY
# =========================================================

extract_project = extract_projects


def print_projects(
    projects
):

    if not projects:

        print(
            "No projects found."
        )

        return

    for index, project in enumerate(
        projects,
        start=1
    ):

        print()
        print(
            f"Project #{index}"
        )

        print(
            "Title:",
            project.get(
                "title",
                ""
            )
        )

        print(
            "Technologies:",
            project.get(
                "technologies",
                []
            )
        )

        print(
            "Descriptions:"
        )

        for description in project.get(
            "description",
            []
        ):

            print(
                " -",
                description
            )