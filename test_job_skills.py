from resume_parser.job_matcher import extract_job_skills
from resume_parser.master_skills import (
    ALL_SKILLS,
    SKILL_ALIASES
)


job_description = """
We are looking for an AI/ML Engineer with strong Python
programming skills.

Required skills:
Python, Machine Learning, Deep Learning,
TensorFlow, Scikit-learn, NLP, Computer Vision,
SQL, Git, REST API.

Experience with Flask, Pandas and NumPy is preferred.
"""


print("\n========== MASTER SKILLS CHECK ==========")

print("Total master skills:", len(ALL_SKILLS))

for skill in ALL_SKILLS:
    print("-", repr(skill))


print("\n========== REQUIRED SKILLS CHECK ==========")

required = [
    "Python",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "Scikit-learn",
    "NLP",
    "Computer Vision",
    "SQL",
    "Git",
    "REST API",
    "Flask",
    "Pandas",
    "NumPy"
]

for skill in required:

    if skill in ALL_SKILLS:
        print("FOUND   :", skill)
    else:
        print("MISSING :", skill)


print("\n========== ALIASES CHECK ==========")

print("Total aliases:", len(SKILL_ALIASES))

for alias, canonical in SKILL_ALIASES.items():
    print("-", repr(alias), "->", repr(canonical))


print("\n========== JOB DESCRIPTION ==========")

print(job_description)


print("\n========== DIRECT TEXT CHECK ==========")

text = job_description.lower()

for skill in required:

    if skill.lower() in text:
        print("TEXT FOUND   :", skill)
    else:
        print("TEXT MISSING :", skill)


print("\n========== EXTRACTED JOB SKILLS ==========")

job_skills = extract_job_skills(
    job_description,
    ALL_SKILLS
)

for skill in job_skills:
    print("-", skill)

print(
    "\nTotal skills:",
    len(job_skills)
)

print("\n========================================")