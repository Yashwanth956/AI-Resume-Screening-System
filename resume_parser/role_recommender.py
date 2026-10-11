# resume_parser/role_recommender.py

from resume_parser.master_skills import normalize_skill
from resume_parser.job_roles import JOB_ROLES


# =========================================================
# GENERIC SKILLS
# =========================================================
# These skills are useful for many jobs.
# They should NOT strongly determine a career role.
# =========================================================

GENERIC_SKILLS = {
    "git",
    "github",
    "sql",
    "linux",
    "communication",
    "problem solving",
    "teamwork",
    "html",
    "css",
}


# =========================================================
# CORE SKILLS
# =========================================================
# Higher weight = stronger evidence for that role.
#
# 10 = extremely important
# 9  = very important
# 8  = important
# 7  = supporting core skill
# =========================================================

CORE_SKILLS = {

    # =====================================================
    # SOFTWARE DEVELOPMENT
    # =====================================================

    "Python Developer": {
        "Python": 10,
        "Flask": 9,
        "Django": 9,
        "FastAPI": 9,
        "REST API": 10,
        "Git": 3,
        "GitHub": 3,
    },

    "Java Developer": {
        "Java": 10,
        "Spring": 9,
        "Spring Boot": 10,
        "REST API": 8,
        "Git": 3,
    },

    "C++ Developer": {
        "C++": 10,
        "C": 8,
        "Data Structures": 9,
        "Algorithms": 9,
        "Git": 3,
    },

    "C# Developer": {
        "C#": 10,
        ".NET": 10,
        "ASP.NET": 9,
        "REST API": 7,
    },

    "Backend Developer": {
        "Python": 8,
        "Java": 8,
        "Node.js": 9,
        "Express.js": 9,
        "Flask": 9,
        "Django": 9,
        "FastAPI": 9,
        "REST API": 10,
        "MongoDB": 8,
        "SQL": 5,
    },

    "Frontend Developer": {
        "JavaScript": 10,
        "React": 10,
        "Angular": 9,
        "Vue.js": 9,
        "HTML": 7,
        "CSS": 7,
    },

    "Full Stack Developer": {
        "JavaScript": 10,
        "React": 9,
        "Node.js": 9,
        "Express.js": 8,
        "MongoDB": 8,
        "REST API": 8,
        "HTML": 6,
        "CSS": 6,
    },


    # =====================================================
    # AI / MACHINE LEARNING
    # =====================================================

    "AI/ML Engineer": {
        "Python": 10,
        "Artificial Intelligence": 10,
        "Machine Learning": 10,
        "Deep Learning": 9,
        "Scikit-learn": 9,
        "TensorFlow": 9,
        "PyTorch": 9,
        "NLP": 8,
        "Computer Vision": 8,
    },

    "Machine Learning Engineer": {
        "Python": 10,
        "Machine Learning": 10,
        "Deep Learning": 9,
        "Scikit-learn": 9,
        "TensorFlow": 9,
        "PyTorch": 9,
        "XGBoost": 8,
        "Feature Engineering": 8,
        "Data Preprocessing": 7,
    },

    "Data Scientist": {
        "Python": 10,
        "Machine Learning": 9,
        "Statistics": 10,
        "Pandas": 8,
        "NumPy": 8,
        "Scikit-learn": 9,
        "Data Analysis": 9,
        "Data Visualization": 8,
        "Matplotlib": 7,
    },

    "Data Analyst": {
        "Python": 7,
        "SQL": 8,
        "Pandas": 8,
        "NumPy": 6,
        "Microsoft Excel": 10,
        "Statistics": 9,
        "Data Analysis": 10,
        "Data Visualization": 9,
        "Matplotlib": 7,
    },

    "NLP Engineer": {
        "Python": 10,
        "NLP": 10,
        "Natural Language Processing": 10,
        "Machine Learning": 8,
        "Deep Learning": 8,
        "Transformers": 10,
        "BERT": 9,
        "GPT": 9,
        "Hugging Face": 9,
    },

    "Computer Vision Engineer": {
        "Python": 10,
        "Computer Vision": 10,
        "Deep Learning": 9,
        "OpenCV": 10,
        "TensorFlow": 8,
        "PyTorch": 8,
        "CNN": 10,
        "YOLO": 9,
    },

    "Generative AI Engineer": {
        "Python": 10,
        "Generative AI": 10,
        "Large Language Models": 10,
        "LLM": 10,
        "Transformers": 9,
        "NLP": 8,
        "GPT": 9,
        "Hugging Face": 9,
    },


    # =====================================================
    # CLOUD / DEVOPS
    # =====================================================

    "Cloud Engineer": {
        "AWS": 10,
        "Azure": 10,
        "Google Cloud": 10,
        "GCP": 10,
        "Docker": 9,
        "Kubernetes": 9,
    },

    "DevOps Engineer": {
        "AWS": 9,
        "Docker": 10,
        "Kubernetes": 10,
        "Jenkins": 9,
        "CI/CD": 10,
        "Linux": 6,
    },


    # =====================================================
    # CYBERSECURITY
    # =====================================================

    "Cybersecurity Analyst": {
        "Cybersecurity": 10,
        "Network Security": 10,
        "Information Security": 10,
        "SIEM": 9,
        "Firewall": 8,
        "IDS": 8,
        "IPS": 8,
    },

    "Security Engineer": {
        "Cybersecurity": 10,
        "Network Security": 10,
        "Information Security": 9,
        "Penetration Testing": 10,
        "Firewall": 8,
        "IDS": 8,
        "IPS": 8,
    },

    "Ethical Hacker": {
        "Cybersecurity": 10,
        "Ethical Hacking": 10,
        "Penetration Testing": 10,
        "Network Security": 9,
    },


    # =====================================================
    # DATABASE
    # =====================================================

    "Database Developer": {
        "SQL": 10,
        "MySQL": 10,
        "PostgreSQL": 10,
        "Oracle": 10,
        "MongoDB": 8,
    },

    "Database Administrator": {
        "SQL": 9,
        "MySQL": 9,
        "PostgreSQL": 9,
        "Oracle": 10,
        "MongoDB": 7,
        "Linux": 6,
    },


    # =====================================================
    # TESTING
    # =====================================================

    "Software Tester": {
        "Software Testing": 10,
        "Manual Testing": 10,
        "Test Cases": 8,
        "Bug Tracking": 8,
    },

    "Automation Test Engineer": {
        "Software Testing": 9,
        "Automation Testing": 10,
        "Selenium": 10,
        "Python": 7,
        "Java": 7,
    },


    # =====================================================
    # MOBILE
    # =====================================================

    "Android Developer": {
        "Android": 10,
        "Android Studio": 10,
        "Java": 9,
        "Kotlin": 10,
    },

    "Flutter Developer": {
        "Flutter": 10,
        "Dart": 10,
        "Android": 7,
    },


    # =====================================================
    # DIGITAL MARKETING
    # =====================================================

    "Digital Marketing Specialist": {
        "SEO": 10,
        "Google Ads": 10,
        "Meta Ads Manager": 10,
        "Content Strategy": 8,
        "Email Marketing": 8,
        "Google Analytics": 9,
        "Marketing Automation": 9,
        "HubSpot": 8,
        "A/B Testing": 7,
        "Copywriting": 7,
    },

    "SEO Specialist": {
        "SEO": 10,
        "Google Analytics": 8,
        "Content Strategy": 8,
        "Copywriting": 7,
    },

    "Performance Marketing Specialist": {
        "Google Ads": 10,
        "Meta Ads Manager": 10,
        "Google Analytics": 9,
        "A/B Testing": 8,
        "Marketing Automation": 7,
    },

    "Content Marketing Specialist": {
        "Content Strategy": 10,
        "Content Marketing": 10,
        "Copywriting": 9,
        "SEO": 8,
        "Canva": 7,
    },


    # =====================================================
    # MECHANICAL
    # =====================================================

    "Mechanical Design Engineer": {
        "Mechanical Design": 10,
        "CAD": 9,
        "SolidWorks": 10,
        "CATIA": 10,
        "AutoCAD": 9,
        "GD&T": 8,
    },

    "Automotive Design Engineer": {
        "Mechanical Design": 9,
        "Automotive Design": 10,
        "SolidWorks": 9,
        "CATIA": 10,
        "AutoCAD": 8,
        "GD&T": 8,
        "DFMEA": 9,
    },

    "FEA Engineer": {
        "FEA": 10,
        "ANSYS": 10,
        "Mechanical Design": 8,
        "CAD": 7,
        "GD&T": 6,
    },

    "Manufacturing Engineer": {
        "Manufacturing": 10,
        "Mechanical Design": 8,
        "CAD": 7,
        "Tooling": 9,
        "GD&T": 8,
        "DFMEA": 8,
    },
}


# =========================================================
# NORMALIZE SKILLS
# =========================================================

def normalize_set(skills):
    """
    Normalize a list of skills.

    Example:

        Python -> python
        PYTHON -> python
        python -> python
    """

    normalized = set()

    if not skills:
        return normalized

    for skill in skills:

        if not skill:
            continue

        normalized_skill = normalize_skill(skill)

        if normalized_skill:

            normalized.add(
                normalized_skill.strip().lower()
            )

    return normalized


# =========================================================
# GET SKILL WEIGHT
# =========================================================

def get_skill_weight(role, skill):
    """
    Return the importance of a skill for a role.

    Core skill:
        Uses role-specific weight.

    Generic skill:
        Weight = 1

    Other supporting skill:
        Weight = 3
    """

    role_weights = CORE_SKILLS.get(
        role,
        {}
    )

    skill_lower = (
        skill.strip().lower()
    )

    # -----------------------------------------------------
    # Check role-specific core skills
    # -----------------------------------------------------

    for core_skill, weight in role_weights.items():

        normalized_core = normalize_skill(
            core_skill
        )

        if not normalized_core:
            continue

        normalized_core = (
            normalized_core.strip().lower()
        )

        if normalized_core == skill_lower:
            return weight

    # -----------------------------------------------------
    # Generic skills
    # -----------------------------------------------------

    if skill_lower in GENERIC_SKILLS:
        return 1

    # -----------------------------------------------------
    # Supporting skill
    # -----------------------------------------------------

    return 3


# =========================================================
# CALCULATE ROLE SCORE
# =========================================================

def calculate_role_score(
    role,
    role_skills,
    resume_normalized
):
    """
    Calculate the recommendation score for one role.
    """

    total_weight = 0
    matched_weight = 0

    matching_skills = []
    missing_skills = []

    core_matches = []
    core_missing = []

    # -----------------------------------------------------
    # Process every role skill
    # -----------------------------------------------------

    for skill in role_skills:

        weight = get_skill_weight(
            role,
            skill
        )

        total_weight += weight

        if skill in resume_normalized:

            matched_weight += weight

            matching_skills.append(
                skill
            )

            # Core skill
            if weight >= 7:

                core_matches.append(
                    skill
                )

        else:

            missing_skills.append(
                skill
            )

            # Core skill missing
            if weight >= 7:

                core_missing.append(
                    skill
                )

    # -----------------------------------------------------
    # Weighted score
    # -----------------------------------------------------

    if total_weight > 0:

        weighted_score = (
            matched_weight
            /
            total_weight
        ) * 100

    else:

        weighted_score = 0

    # -----------------------------------------------------
    # Core skill statistics
    # -----------------------------------------------------

    total_core = (
        len(core_matches)
        +
        len(core_missing)
    )

    matched_core = len(
        core_matches
    )

    if total_core > 0:

        core_ratio = (
            matched_core
            /
            total_core
        )

    else:

        core_ratio = 0

    # -----------------------------------------------------
    # Domain strength
    # -----------------------------------------------------

    if matched_core == 0:

        domain_strength = 0

    elif core_ratio >= 0.80:

        domain_strength = 1.00

    elif core_ratio >= 0.60:

        domain_strength = 0.90

    elif core_ratio >= 0.40:

        domain_strength = 0.75

    else:

        domain_strength = 0.60

    # -----------------------------------------------------
    # Final score
    #
    # 80% weighted skill score
    # 20% core-domain score
    # -----------------------------------------------------

    final_score = (
        weighted_score * 0.80
        +
        (core_ratio * 100) * 0.20
    )

    # -----------------------------------------------------
    # No core skill = weak recommendation
    # -----------------------------------------------------

    if matched_core == 0:

        final_score *= 0.30

    # -----------------------------------------------------
    # Domain strength adjustment
    # -----------------------------------------------------

    if matched_core > 0:

        final_score *= domain_strength

    # -----------------------------------------------------
    # Small bonus for strong coverage
    # -----------------------------------------------------

    if core_ratio >= 0.80:

        final_score += 3

    elif core_ratio >= 0.60:

        final_score += 1.5

    # -----------------------------------------------------
    # Limit score
    # -----------------------------------------------------

    final_score = min(
        max(
            final_score,
            0
        ),
        100
    )

    return {

        "role": role,

        "score": round(
            final_score,
            2
        ),

        "matching_skills":
            sorted(
                matching_skills
            ),

        "missing_skills":
            sorted(
                missing_skills
            ),

        "matched_count":
            len(matching_skills),

        "total_skills":
            len(role_skills),

        "core_matches":
            sorted(
                core_matches
            ),

        "core_missing":
            sorted(
                core_missing
            ),

        "core_ratio":
            round(
                core_ratio * 100,
                2
            ),

        "weighted_score":
            round(
                weighted_score,
                2
            )
    }


# =========================================================
# RECOMMEND JOB ROLES
# =========================================================

def recommend_job_roles(
    resume_skills,
    top_n=10
):
    """
    Recommend job roles based on resume skills.

    Parameters
    ----------
    resume_skills : list
        Skills extracted from the resume.

    top_n : int
        Number of roles to return.

    Returns
    -------
    list
        Ranked job-role recommendations.
    """

    # -----------------------------------------------------
    # Normalize resume skills
    # -----------------------------------------------------

    resume_normalized = normalize_set(
        resume_skills
    )

    if not resume_normalized:

        return []

    recommendations = []

    # =====================================================
    # CHECK EVERY JOB ROLE
    # =====================================================

    for role, required_skills in JOB_ROLES.items():

        role_skills = []

        # -------------------------------------------------
        # Normalize role skills
        # -------------------------------------------------

        for skill in required_skills:

            normalized = normalize_skill(
                skill
            )

            if not normalized:
                continue

            normalized = (
                normalized
                .strip()
                .lower()
            )

            if normalized not in role_skills:

                role_skills.append(
                    normalized
                )

        if not role_skills:
            continue

        # -------------------------------------------------
        # Calculate role score
        # -------------------------------------------------

        result = calculate_role_score(
            role,
            role_skills,
            resume_normalized
        )

        recommendations.append(
            result
        )

    # =====================================================
    # SORT RECOMMENDATIONS
    # =====================================================

    recommendations.sort(
        key=lambda x: (
            x["score"],
            x["core_ratio"],
            x["matched_count"]
        ),
        reverse=True
    )

    # =====================================================
    # RETURN TOP ROLES
    # =====================================================

    return recommendations[:top_n]