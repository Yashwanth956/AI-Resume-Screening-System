from resume_parser.ats_scorer import calculate_ats_score
from resume_parser.skills import extract_skills
from resume_parser.education import extract_education
from resume_parser.project import extract_projects
from resume_parser.experience import extract_experience
from resume_parser.jd_skill_extractor import extract_jd_skills

import pdfplumber
import os


# =========================================================
# RESUME FILE
# =========================================================

PDF_PATH = (
    r"C:\Users\Asus\OneDrive\Documents"
    r"\AI-Resume-Screening-System\uploads"
    r"\YASHWANTH_Resume(up).pdf"
)


# =========================================================
# CHECK FILE
# =========================================================

print("\n========== FILE CHECK ==========")

print("File:", PDF_PATH)
print("Exists:", os.path.exists(PDF_PATH))

if not os.path.exists(PDF_PATH):
    print("\nERROR: PDF does not exist.")
    raise SystemExit


# =========================================================
# EXTRACT PDF TEXT
# =========================================================

text = ""

print("\n========== PDF EXTRACTION ==========")

with pdfplumber.open(PDF_PATH) as pdf:

    print("Pages:", len(pdf.pages))

    for page_number, page in enumerate(
        pdf.pages,
        start=1
    ):

        page_text = page.extract_text()

        if page_text:

            print(
                f"Page {page_number}: Text found"
            )

            text += page_text + "\n"

        else:

            print(
                f"Page {page_number}: No text"
            )


# =========================================================
# JOB DESCRIPTION
# =========================================================

job_description = """
We are looking for an AI/ML Engineer.

Requirements:

Bachelor's degree in Computer Science,
Artificial Intelligence, Machine Learning,
or related engineering field.

Required technical skills:

Python
Machine Learning
Deep Learning
TensorFlow
Scikit-learn
NLP
Computer Vision
SQL
Pandas
NumPy
Git
REST API
Flask

Experience with Generative AI and data science
is preferred.

Freshers and recent graduates are welcome.
"""


# =========================================================
# EXTRACT RESUME DATA
# =========================================================

print("\n========== RESUME EXTRACTION ==========")

skills = extract_skills(text)

education = extract_education(text)

projects = extract_projects(text)

experience = extract_experience(text)


# =========================================================
# JOB SKILLS
# =========================================================
# Current project API:
# JD skills come from jd_skill_extractor.py

job_skills = extract_jd_skills(
    job_description
)


# =========================================================
# DISPLAY INPUT DATA
# =========================================================

print("\n========== RESUME SKILLS ==========")

for skill in skills:
    print("-", skill)

print("Total:", len(skills))


print("\n========== JOB SKILLS ==========")

for skill in job_skills:
    print("-", skill)

print("Total:", len(job_skills))


print("\n========== EDUCATION ==========")

print(education)


print("\n========== PROJECTS ==========")

for project in projects:
    print(project)


print("\n========== EXPERIENCE ==========")

print(experience)


# =========================================================
# ATS SCORE
# =========================================================

print("\n========== ATS ANALYSIS ==========")

result = calculate_ats_score(

    resume_skills=skills,

    job_skills=job_skills,

    resume_text=text,

    job_description=job_description,

    candidate_experience=experience,

    education=education,

    projects=projects
)


# =========================================================
# RESULTS
# =========================================================

print("\n========== ATS RESULTS ==========")

print(
    "Final ATS Score:",
    result["score"]
)

print(
    "Skill Score:",
    result["skill_score"]
)

print(
    "Keyword Score:",
    result["keyword_score"]
)

print(
    "Experience Score:",
    result["experience_score"]
)

print(
    "Education Score:",
    result["education_score"]
)

print(
    "Project Score:",
    result["project_score"]
)

print(
    "Resume Quality Score:",
    result["resume_quality_score"]
)


# =========================================================
# MATCHING
# =========================================================

print("\n========== MATCHING SKILLS ==========")

for skill in result["matching_skills"]:
    print("-", skill)


# =========================================================
# MISSING
# =========================================================

print("\n========== MISSING SKILLS ==========")

for skill in result["missing_skills"]:
    print("-", skill)


print("\n====================================")
print("ATS TEST COMPLETED")
print("====================================")
