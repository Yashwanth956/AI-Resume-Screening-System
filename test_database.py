# test_database.py
# ============================================================
# DATABASE REGRESSION TEST
# ============================================================

from pathlib import Path

from database.db_manager import (
    init_db,
    save_analysis,
    get_analysis,
    list_analyses,
    delete_analysis,
)


TEST_DB = Path("database") / "test_resume_screening.db"


def remove_test_db():
    if TEST_DB.exists():
        TEST_DB.unlink()


def main():

    print()
    print("=" * 68)
    print("DATABASE REGRESSION TEST")
    print("=" * 68)

    remove_test_db()

    # --------------------------------------------------------
    # Initialize
    # --------------------------------------------------------

    path = init_db(TEST_DB)

    assert path.exists()

    print("Database created:", path)

    # --------------------------------------------------------
    # Fresher sample
    # --------------------------------------------------------

    fresher_id = save_analysis(
        resume_filename="fresher_sample.pdf",
        candidate_name="Sample Fresher",
        email="fresher@example.com",
        phone="9000000001",

        resume_skills=[
            "Python",
            "Machine Learning",
            "NLP",
        ],

        education=[
            {
                "degree": "B.Tech Computer Science",
                "institution": "Sample University",
                "score": "CGPA: 8.0",
                "duration": "2022 - 2026",
            }
        ],

        experience={
            "total_years": 0.0,
            "stated_years": 0.0,
            "calculated_years": 0.0,
            "records": [],
        },

        projects=[
            {
                "title": "Resume Screening System",
                "technologies": [
                    "Python",
                    "NLP",
                ],
                "description": [
                    "Built a resume screening project."
                ],
            }
        ],

        job_description=(
            "AI/ML Engineer. Freshers welcome. "
            "Python and Machine Learning required."
        ),

        job_skills=[
            "Python",
            "Machine Learning",
        ],

        ats_result={
            "score": 82.5,
            "skill_score": 100,
            "keyword_score": 75,
            "experience_score": 100,
            "education_score": 100,
            "project_score": 50,
            "resume_quality_score": 80,
            "experience_requirement": {
                "min_years": 0.0,
                "max_years": 1.0,
                "has_requirement": True,
                "requirement_type": "fresher",
                "matched_text": "fresher",
            },
            "matching_skills": [
                "Python",
                "Machine Learning",
            ],
            "missing_skills": [],
        },

        job_match_result={
            "match_score": 100,
            "match_category": "Strong Match",
        },

        recommended_roles=[
            {
                "role": "AI/ML Engineer",
                "score": 80,
                "matched_count": 3,
                "total_skills": 9,
                "matching_skills": [
                    "python",
                    "machine learning",
                    "nlp",
                ],
                "missing_skills": [
                    "pytorch",
                ],
                "core_matches": [
                    "python",
                    "machine learning",
                ],
            }
        ],

        db_path=TEST_DB,
    )

    # --------------------------------------------------------
    # Experienced sample
    # --------------------------------------------------------

    experienced_id = save_analysis(
        resume_filename="experienced_sample.pdf",
        candidate_name="Sample Experienced",
        email="experienced@example.com",
        phone="9000000002",

        resume_skills=[
            "Python",
            "Flask",
            "REST API",
            "SQL",
        ],

        education=[
            {
                "degree": "B.Tech",
                "institution": "Sample Institute",
                "score": "CGPA: 8.2",
                "duration": "2018 - 2022",
            }
        ],

        experience={
            "total_years": 4.08,
            "stated_years": 4.0,
            "calculated_years": 4.08,
            "records": [
                {
                    "job_title": "Python Developer",
                    "date_range":
                        "October 2022 - Present",
                    "start": "2022-10",
                    "end": "Present",
                }
            ],
        },

        projects=[],

        job_description=(
            "Python Developer with 3+ years "
            "of experience. Python, Flask and "
            "REST API required."
        ),

        job_skills=[
            "Python",
            "Flask",
            "REST API",
        ],

        ats_result={
            "score": 88,
            "skill_score": 100,
            "keyword_score": 80,
            "experience_score": 100,
            "education_score": 100,
            "project_score": 0,
            "resume_quality_score": 100,
            "experience_requirement": {
                "min_years": 3.0,
                "max_years": None,
                "has_requirement": True,
                "requirement_type": "minimum",
                "matched_text": "3+ years",
            },
            "matching_skills": [
                "Python",
                "Flask",
                "REST API",
            ],
            "missing_skills": [],
        },

        job_match_result={
            "match_score": 100,
            "match_category": "Strong Match",
        },

        recommended_roles=[
            {
                "role": "Python Developer",
                "score": 90,
                "matched_count": 4,
                "total_skills": 8,
                "matching_skills": [
                    "python",
                    "flask",
                    "rest api",
                    "sql",
                ],
                "missing_skills": [
                    "django",
                    "fastapi",
                ],
                "core_matches": [
                    "python",
                    "flask",
                    "rest api",
                ],
            }
        ],

        db_path=TEST_DB,
    )

    assert fresher_id > 0
    assert experienced_id > fresher_id

    # --------------------------------------------------------
    # Read back
    # --------------------------------------------------------

    fresher = get_analysis(
        fresher_id,
        TEST_DB
    )

    experienced = get_analysis(
        experienced_id,
        TEST_DB
    )

    assert fresher is not None
    assert experienced is not None

    assert fresher["candidate_name"] == "Sample Fresher"
    assert fresher["total_experience"] == 0.0
    assert len(fresher["resume_skills"]) == 3
    assert len(fresher["education"]) == 1
    assert len(fresher["projects"]) == 1
    assert len(fresher["recommended_roles"]) == 1
    assert (
        fresher["experience_requirement"][
            "requirement_type"
        ]
        == "fresher"
    )

    assert (
        experienced["candidate_name"]
        == "Sample Experienced"
    )
    assert experienced["total_experience"] == 4.08
    assert len(
        experienced["experience_records"]
    ) == 1
    assert (
        experienced["recommended_roles"][0][
            "role"
        ]
        == "Python Developer"
    )

    # --------------------------------------------------------
    # List
    # --------------------------------------------------------

    rows = list_analyses(
        db_path=TEST_DB
    )

    assert len(rows) == 2

    # --------------------------------------------------------
    # Delete / cascade
    # --------------------------------------------------------

    deleted = delete_analysis(
        fresher_id,
        TEST_DB
    )

    assert deleted is True

    assert get_analysis(
        fresher_id,
        TEST_DB
    ) is None

    rows_after_delete = list_analyses(
        db_path=TEST_DB
    )

    assert len(rows_after_delete) == 1

    print()
    print("Fresher insert/read: PASS")
    print("Experienced insert/read: PASS")
    print("Child records: PASS")
    print("List analyses: PASS")
    print("Delete cascade: PASS")

    print()
    print("=" * 68)
    print("REGRESSION STATUS: PASS")
    print("=" * 68)

    # Keep the project directory clean.
    remove_test_db()


if __name__ == "__main__":
    main()
