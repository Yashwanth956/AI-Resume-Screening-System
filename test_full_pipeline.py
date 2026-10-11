import os
import pdfplumber

from resume_parser.parser import extract_email, extract_phone
from resume_parser.name_extractor import extract_name
from resume_parser.skills import extract_skills
from resume_parser.education import extract_education
from resume_parser.experience import extract_experience
from resume_parser.project import extract_projects
from resume_parser.jd_skill_extractor import extract_jd_skills
from resume_parser.ats_scorer import calculate_ats_score
from resume_parser.role_recommender import recommend_job_roles


PDF_PATH = r"uploads\YASHWANTH_Resume(up).pdf"

JOB_DESCRIPTION = """
AI/ML Engineer

We are looking for a fresher / entry-level AI/ML Engineer with knowledge of
Python, Artificial Intelligence, Machine Learning, Deep Learning,
Natural Language Processing (NLP), Computer Vision, Generative AI,
TensorFlow, PyTorch, Scikit-learn, data preprocessing and feature engineering.

The candidate should have a Bachelor's degree in Artificial Intelligence,
Machine Learning, Computer Science, Information Technology, or a related field.

Hands-on academic or personal projects are acceptable.
"""


def heading(number, title):
    print()
    print("=" * 70)
    print(f"{number}. {title}")
    print("=" * 70)


def match_category(score):
    if score >= 80:
        return "Strong Match"
    if score >= 60:
        return "Good Match"
    if score >= 40:
        return "Moderate Match"
    return "Low Match"


def read_pdf_text(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"
    return text.strip()


def main():
    print("=" * 70)
    print("          AI RESUME SCREENING & JOB RECOMMENDATION")
    print("=" * 70)

    if not os.path.exists(PDF_PATH):
        print()
        print("ERROR: Resume PDF not found.")
        print("Expected path:")
        print(PDF_PATH)
        return

    heading(1, "PDF EXTRACTION")

    try:
        text = read_pdf_text(PDF_PATH)
    except Exception as error:
        print("Could not read PDF:", error)
        return

    print("Resume:", PDF_PATH)
    print("File Exists:", os.path.exists(PDF_PATH))
    print("Extracted Characters:", len(text))

    if not text:
        print("No text extracted from resume.")
        return

    heading(2, "CANDIDATE DETAILS")

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)

    print("Name:", name)
    print("Email:", email)
    print("Phone:", phone)

    heading(3, "RESUME SKILL EXTRACTION")

    skills = extract_skills(text) or []

    for skill in skills:
        print("-", skill)

    print()
    print("Total Resume Skills:", len(skills))

    heading(4, "EDUCATION EXTRACTION")

    education = extract_education(text) or []

    if education:
        for index, item in enumerate(education, start=1):
            print()
            print(f"Education #{index}")
            print("Degree:", item.get("degree", ""))
            print("Institution:", item.get("institution", ""))
            print("Score:", item.get("score", ""))
            print("Duration:", item.get("duration", ""))
    else:
        print("No education detected.")

    heading(5, "EXPERIENCE EXTRACTION")

    experience = extract_experience(text) or {}

    print("Total Experience:", experience.get("total_years", 0), "years")
    print("Stated Years:", experience.get("stated_years", 0))
    print("Calculated Years:", experience.get("calculated_years", 0))
    print("Job Titles:", experience.get("job_titles", []))
    print("Date Ranges:", experience.get("date_ranges", []))

    heading(6, "PROJECT EXTRACTION")

    projects = extract_projects(text) or []

    if projects:
        for index, project in enumerate(projects, start=1):
            print()
            print(f"Project #{index}")
            print("Title:", project.get("title", ""))
            print("Technologies:", project.get("technologies", []))

            descriptions = project.get("description", [])

            if descriptions:
                print("Description:")
                for description in descriptions:
                    print("-", description)
    else:
        print("No projects detected.")

    print()
    print("Total Projects:", len(projects))

    heading(7, "JOB SKILL EXTRACTION")

    job_skills = extract_jd_skills(JOB_DESCRIPTION) or []

    for skill in job_skills:
        print("-", skill)

    print()
    print("Total Job Skills:", len(job_skills))

    heading(8, "ATS ANALYSIS")

    ats_result = calculate_ats_score(
        resume_skills=skills,
        job_skills=job_skills,
        resume_text=text,
        job_description=JOB_DESCRIPTION,
        candidate_experience=experience,
        education=education,
        projects=projects,
    ) or {}

    ats_score = ats_result.get("score", 0)
    skill_score = ats_result.get("skill_score", 0)
    keyword_score = ats_result.get("keyword_score", 0)
    experience_score = ats_result.get("experience_score", 0)
    education_score = ats_result.get("education_score", 0)
    project_score = ats_result.get("project_score", 0)
    resume_quality_score = ats_result.get("resume_quality_score", 0)

    matching_skills = ats_result.get("matching_skills", [])
    missing_skills = ats_result.get("missing_skills", [])

    print("Final ATS Score:", ats_score, "%")
    print("Skill Score:", skill_score, "%")
    print("Keyword Score:", keyword_score, "%")
    print("Experience Score:", experience_score, "%")
    print("Education Score:", education_score, "%")
    print("Project Score:", project_score, "%")
    print("Resume Quality Score:", resume_quality_score, "%")

    if "experience_requirement" in ats_result:
        print("Experience Requirement:", ats_result.get("experience_requirement"))

    if "project_matching_skills" in ats_result:
        print("Project Matching Skills:", ats_result.get("project_matching_skills"))

    heading(9, "MATCHING SKILLS")

    if matching_skills:
        for skill in matching_skills:
            print("-", skill)
    else:
        print("No matching skills.")

    heading(10, "MISSING SKILLS")

    if missing_skills:
        for skill in missing_skills:
            print("-", skill)
    else:
        print("No missing required skills.")

    heading(11, "JOB MATCH ANALYSIS")

    match_score = skill_score

    print("Match Score:", match_score, "%")
    print("Match Category:", match_category(match_score))

    heading(12, "RECOMMENDED JOB ROLES")

    recommendations = recommend_job_roles(
        resume_skills=skills,
        top_n=10,
    ) or []

    if recommendations:
        for index, result in enumerate(recommendations, start=1):
            print()
            print(f"#{index} {result.get('role', '')}")
            print("Score:", result.get("score", 0), "%")

            if "matched_count" in result and "total_skills" in result:
                print(
                    "Matched Skills:",
                    result.get("matched_count", 0),
                    "/",
                    result.get("total_skills", 0),
                )

            print("Matching Skills:", result.get("matching_skills", []))

            if result.get("core_matches") is not None:
                print("Core Matches:", result.get("core_matches", []))

            print("Missing Skills:", result.get("missing_skills", []))
    else:
        print("No job-role recommendations generated.")

    heading(13, "FINAL SUMMARY")

    print("Candidate:", name)
    print("ATS Score:", ats_score, "%")
    print("Job Match:", match_score, "%")
    print("Match Category:", match_category(match_score))

    print()
    print("Top Recommended Roles:")

    for index, result in enumerate(recommendations[:5], start=1):
        print(
            f"{index}. "
            f"{result.get('role', '')} "
            f"({result.get('score', 0)}%)"
        )

    print()
    print("=" * 70)
    print("                 PIPELINE COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()

