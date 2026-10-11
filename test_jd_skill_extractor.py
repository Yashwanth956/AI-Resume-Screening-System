# test_jd_skill_extractor.py
# Regression test for current JD skill extractor API

from resume_parser.jd_skill_extractor import extract_jd_skills
from resume_parser.ats_scorer import (
    get_matching_skills,
    get_missing_skills,
    calculate_skill_score,
)

# ============================================================
# CURRENT RESUME SKILLS
# ============================================================

resume_skills = [
    "Algorithms",
    "Artificial Intelligence",
    "C",
    "Computer Vision",
    "CSS",
    "Data Preprocessing",
    "Deep Learning",
    "Feature Engineering",
    "Flask",
    "Forecasting",
    "Generative AI",
    "Git",
    "GitHub",
    "Google Colab",
    "HTML",
    "Machine Learning",
    "Matplotlib",
    "MongoDB",
    "Monitoring",
    "NLP",
    "NumPy",
    "OpenCV",
    "Pandas",
    "Python",
    "Reinforcement Learning",
    "REST API",
    "Scikit-learn",
    "SQL",
    "TensorFlow",
    "VS Code",
]

# ============================================================
# JOB DESCRIPTION
# ============================================================

job_description = """
We are looking for an AI/ML Engineer.

The candidate should have strong knowledge of
Python, Artificial Intelligence, Machine Learning,
Deep Learning, TensorFlow, PyTorch, Scikit-learn,
NLP, Computer Vision, Generative AI,
Data Preprocessing and Feature Engineering.

Experience with developing AI applications and
machine learning models is preferred.
"""

# ============================================================
# JD SKILL EXTRACTION
# ============================================================

print("=" * 60)
print("JD SKILL EXTRACTION TEST")
print("=" * 60)

job_skills = extract_jd_skills(job_description)

print("\nEXTRACTED JOB SKILLS")
print("-" * 60)

for skill in job_skills:
    print(f"- {skill}")

print(f"\nTotal Job Skills: {len(job_skills)}")

# ============================================================
# MATCHING / MISSING / SCORE
# ============================================================

matching_skills = get_matching_skills(
    resume_skills,
    job_skills,
)

missing_skills = get_missing_skills(
    resume_skills,
    job_skills,
)

match_score = calculate_skill_score(
    resume_skills,
    job_skills,
)

print("\nMATCHING SKILLS")
print("-" * 60)

for skill in matching_skills:
    print(f"- {skill}")

print("\nMISSING SKILLS")
print("-" * 60)

for skill in missing_skills:
    print(f"- {skill}")

print("\n" + "-" * 60)
print(f"Matched Skills: {len(matching_skills)}/{len(job_skills)}")
print(f"JD Skill Match: {match_score}%")
print("-" * 60)

# ============================================================
# REGRESSION CHECKS
# ============================================================

expected_job_skills = {
    "Artificial Intelligence",
    "Computer Vision",
    "Data Preprocessing",
    "Deep Learning",
    "Feature Engineering",
    "Generative AI",
    "Machine Learning",
    "NLP",
    "Python",
    "PyTorch",
    "Scikit-learn",
    "TensorFlow",
}

assert set(job_skills) == expected_job_skills, (
    "JD extraction regression detected.\n"
    f"Expected: {sorted(expected_job_skills)}\n"
    f"Actual:   {sorted(job_skills)}"
)

assert missing_skills == ["PyTorch"], (
    "Unexpected missing skills: "
    f"{missing_skills}"
)

assert match_score == 91.67, (
    f"Expected skill score 91.67, got {match_score}"
)

print("\nREGRESSION STATUS: PASS")
