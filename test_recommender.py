# test_recommender.py
# Regression test for current role recommender

from resume_parser.role_recommender import recommend_job_roles

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

recommendations = recommend_job_roles(
    resume_skills,
    top_n=10
)

print()
print("=" * 60)
print("JOB ROLE RECOMMENDATIONS")
print("=" * 60)

for index, recommendation in enumerate(recommendations, start=1):
    print()
    print(f"#{index} {recommendation['role']}")
    print(f"Score: {recommendation['score']}%")
    print(
        f"Matched Skills: "
        f"{recommendation['matched_count']}/"
        f"{recommendation['total_skills']}"
    )

    print("\nMatching Skills:")
    for skill in recommendation.get("matching_skills", []):
        print("  -", skill)

    print("\nCore Matches:")
    for skill in recommendation.get("core_matches", []):
        print("  -", skill)

    print("\nMissing Skills:")
    for skill in recommendation.get("missing_skills", []):
        print("  -", skill)

assert len(recommendations) == 10, (
    f"Expected 10 recommendations, got {len(recommendations)}"
)

expected_top_five = [
    ("AI/ML Engineer", 92.0),
    ("Machine Learning Engineer", 72.01),
    ("Data Scientist", 60.58),
    ("Python Developer", 60.3),
    ("Computer Vision Engineer", 58.48),
]

actual_top_five = [
    (item["role"], item["score"])
    for item in recommendations[:5]
]

assert actual_top_five == expected_top_five, (
    "Top-5 role regression detected.\n"
    f"Expected: {expected_top_five}\n"
    f"Actual:   {actual_top_five}"
)

ai_ml = recommendations[0]

assert ai_ml.get("missing_skills") == ["pytorch"], (
    "AI/ML Engineer should only be missing PyTorch. "
    f"Got: {ai_ml.get('missing_skills')}"
)

python_dev = next(
    item
    for item in recommendations
    if item["role"] == "Python Developer"
)

python_matching = set(
    python_dev.get("matching_skills", [])
)

expected_python_matches = {
    "flask",
    "git",
    "github",
    "python",
    "rest api",
    "sql",
}

assert expected_python_matches.issubset(python_matching), (
    "Python Developer matching skills regression detected.\n"
    f"Expected at least: {sorted(expected_python_matches)}\n"
    f"Actual: {sorted(python_matching)}"
)

assert python_dev.get("missing_skills") == [
    "django",
    "fastapi"
], (
    "Python Developer missing skills regression detected. "
    f"Got: {python_dev.get('missing_skills')}"
)

print()
print("=" * 60)
print("REGRESSION STATUS: PASS")
print("=" * 60)
