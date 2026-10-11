import re


# =========================================================
# STOP WORDS
# =========================================================

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at",
    "be", "by", "for", "from", "has",
    "have", "in", "is", "it", "of",
    "on", "or", "that", "the", "this",
    "to", "was", "were", "will", "with",
    "which", "who", "you", "your",
    "their", "they", "we", "our",
    "into", "using", "such", "than",
    "these", "those",

    "responsible",
    "responsibilities",
    "role",
    "candidate",
    "work",
    "working",
    "experience",
    "skills",
    "skill",
    "ability",
    "strong",
    "knowledge",
    "including",
    "etc"
}


# =========================================================
# EXTRACT MEANINGFUL KEYWORDS
# =========================================================

def extract_meaningful_keywords(text):

    text = text.lower()

    words = re.findall(
        r"[a-zA-Z][a-zA-Z0-9+#.-]*",
        text
    )

    keywords = []

    for word in words:

        word = word.strip(
            ".,;:!?()[]{}"
        )

        if not word:
            continue

        if word in STOP_WORDS:
            continue

        # Keep important short technical terms
        if len(word) <= 2 and word not in {
            "ai",
            "ml",
            "nlp",
            "cv",
            "c",
            "r"
        }:
            continue

        if word not in keywords:

            keywords.append(
                word
            )

    return keywords


# =========================================================
# NORMALIZE KEYWORDS
# =========================================================

def normalize_keyword(keyword):

    keyword = keyword.lower().strip()

    aliases = {

        # API
        "apis": "api",
        "api": "api",

        # Application
        "applications": "application",
        "application": "application",

        # Model
        "models": "model",
        "model": "model",

        # System
        "systems": "system",
        "system": "system",

        # Algorithm
        "algorithms": "algorithm",
        "algorithm": "algorithm",

        # Prediction
        "predictions": "prediction",
        "prediction": "prediction",

        # Technology
        "technologies": "technology",
        "technology": "technology",

        # Solution
        "solutions": "solution",
        "solution": "solution",

        # Developer
        "developers": "developer",
        "developer": "developer",

        # Engineer
        "engineers": "engineer",
        "engineer": "engineer",

        # Database
        "databases": "database",
        "database": "database",

        # Service
        "services": "service",
        "service": "service",

        # Deployment
        "deployments": "deployment",
        "deployment": "deployment",

        # Projects
        "projects": "project",
        "project": "project",

        # Applications
        "apps": "application",

    }

    return aliases.get(
        keyword,
        keyword
    )


# =========================================================
# NORMALIZE KEYWORD LIST
# =========================================================

def normalize_keywords(keywords):

    normalized = []

    for keyword in keywords:

        value = normalize_keyword(
            keyword
        )

        if value not in normalized:

            normalized.append(
                value
            )

    return normalized


# =========================================================
# CALCULATE KEYWORD SCORE
# =========================================================

def calculate_keyword_score(
    resume_text,
    job_description
):

    # -----------------------------------------------------
    # Extract job keywords
    # -----------------------------------------------------

    job_keywords = (
        extract_meaningful_keywords(
            job_description
        )
    )


    # -----------------------------------------------------
    # Extract resume keywords
    # -----------------------------------------------------

    resume_keywords = (
        extract_meaningful_keywords(
            resume_text
        )
    )


    # -----------------------------------------------------
    # Normalize keywords
    # -----------------------------------------------------

    job_keywords = (
        normalize_keywords(
            job_keywords
        )
    )

    resume_keywords = set(
        normalize_keywords(
            resume_keywords
        )
    )


    # -----------------------------------------------------
    # No job keywords
    # -----------------------------------------------------

    if not job_keywords:

        return 0


    # -----------------------------------------------------
    # Find matching keywords
    # -----------------------------------------------------

    matching_keywords = []

    for keyword in job_keywords:

        if keyword in resume_keywords:

            matching_keywords.append(
                keyword
            )


    # -----------------------------------------------------
    # Calculate score
    # -----------------------------------------------------

    score = (
        len(matching_keywords)
        /
        len(job_keywords)
    ) * 100


    return round(
        score,
        2
    )