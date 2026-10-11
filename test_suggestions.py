# ============================================================
# test_suggestions.py
# AI Resume Screening & Job Recommendation System
# ============================================================

from resume_parser.suggestions import generate_suggestions


def contains_text(items, text):
    text = text.lower()
    return any(
        text in str(item).lower()
        for item in items
    )


def run_test(name, condition):
    if condition:
        print(f"[PASS] {name}")
        return True

    print(f"[FAIL] {name}")
    return False


passed = 0
total = 0


# ============================================================
# TEST 1
# LOW ATS + MISSING LLM + IRRELEVANT PROJECTS
# ============================================================

suggestions = generate_suggestions(
    ats_score=40,
    missing_skills=["LLM"],
    projects=[
        {
            "title": "API Monitoring Dashboard",
            "technologies": ["Flask"],
            "description": [
                "Created a Flask application."
            ]
        }
    ],
    experience={
        "total_years": 2.58
    },
    ats_result={
        "skill_score": 0,
        "keyword_score": 50,
        "experience_score": 100,
        "education_score": 100,
        "project_score": 0,
        "resume_quality_score": 100
    },
    recommended_roles=[
        {
            "role": "Python Developer",
            "missing_skills": [
                "django",
                "github"
            ]
        }
    ],
    job_skills=["LLM"]
)

checks = [
    contains_text(
        suggestions,
        "ats score is low"
    ),
    contains_text(
        suggestions,
        "llm"
    ),
    contains_text(
        suggestions,
        "projects"
    ),
    contains_text(
        suggestions,
        "python developer"
    ),
    not contains_text(
        suggestions,
        "build practical experience"
    )
]

total += 1
passed += run_test(
    "Low ATS / LLM suggestions",
    all(checks)
)


# ============================================================
# TEST 2
# FRESHER ACCEPTED BY JD
# ============================================================

suggestions = generate_suggestions(
    ats_score=85,
    missing_skills=[],
    projects=[
        {
            "title": "Machine Learning Project",
            "technologies": [
                "Python",
                "Machine Learning"
            ]
        }
    ],
    experience={
        "total_years": 0
    },
    ats_result={
        "skill_score": 100,
        "keyword_score": 80,
        "experience_score": 100,
        "education_score": 100,
        "project_score": 100,
        "resume_quality_score": 100
    },
    recommended_roles=[],
    job_skills=[
        "Python",
        "Machine Learning"
    ]
)

total += 1
passed += run_test(
    "Fresher is not incorrectly penalized",
    not contains_text(
        suggestions,
        "build practical experience"
    )
)


# ============================================================
# TEST 3
# STRONG PROFILE
# ============================================================

suggestions = generate_suggestions(
    ats_score=95,
    missing_skills=[],
    projects=[
        {
            "title": "Relevant Project",
            "technologies": ["Python"]
        },
        {
            "title": "Backend Project",
            "technologies": ["FastAPI"]
        }
    ],
    experience={
        "total_years": 2
    },
    ats_result={
        "skill_score": 100,
        "keyword_score": 100,
        "experience_score": 100,
        "education_score": 100,
        "project_score": 100,
        "resume_quality_score": 100
    },
    recommended_roles=[],
    job_skills=[
        "Python",
        "FastAPI"
    ]
)

total += 1
passed += run_test(
    "Strong profile receives positive default message",
    contains_text(
        suggestions,
        "strongly aligned"
    )
)


# ============================================================
# TEST 4
# PROJECTS EXIST BUT DO NOT MATCH JD
# ============================================================

suggestions = generate_suggestions(
    ats_score=70,
    missing_skills=["LLM"],
    projects=[
        {
            "title": "Sales Dashboard",
            "technologies": [
                "Power BI",
                "SQL"
            ]
        }
    ],
    experience={
        "total_years": 3
    },
    ats_result={
        "skill_score": 0,
        "keyword_score": 60,
        "experience_score": 100,
        "education_score": 100,
        "project_score": 0,
        "resume_quality_score": 100
    },
    recommended_roles=[],
    job_skills=["LLM"]
)

total += 1
passed += run_test(
    "Project relevance mismatch detected",
    contains_text(
        suggestions,
        "do not currently demonstrate"
    )
)


# ============================================================
# FINAL RESULT
# ============================================================

print()
print("=" * 60)
print(
    f"SUGGESTION TESTS: {passed}/{total} PASSED"
)
print("=" * 60)

if passed != total:
    raise SystemExit(1)
