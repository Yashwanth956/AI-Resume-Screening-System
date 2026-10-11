# ============================================================
# test_career_break.py
# Regression test for career-break exclusion
# ============================================================

from resume_parser.experience import extract_experience


def check(name, condition):
    if condition:
        print(f"[PASS] {name}")
        return True

    print(f"[FAIL] {name}")
    return False


career_break_resume = """
KIRAN KUMAR

PROFESSIONAL EXPERIENCE

Data Analyst | SampleMetric Solutions | Chennai
July 2024 - September 2026
Built dashboards and automated reporting.

Junior Data Analyst | DemoRetail Insights | Hyderabad
July 2021 - December 2023
Prepared sales datasets and monthly reports.

CAREER BREAK
January 2024 - June 2024
Planned personal break. No employment during this period.

PROJECTS
Public Retail Dataset Analysis
"""

result = extract_experience(
    career_break_resume
)

print("\nCareer-break result:")
print(result)

passed = 0
total = 0

total += 1
passed += check(
    "Career break excluded from date_ranges",
    "January 2024 - June 2024"
    not in result.get(
        "date_ranges",
        []
    )
)

total += 1
passed += check(
    "Career break excluded from records",
    all(
        record.get("date_range")
        != "January 2024 - June 2024"
        for record in result.get(
            "records",
            []
        )
    )
)

total += 1
passed += check(
    "Calculated employment is 4.75 years",
    result.get(
        "calculated_years"
    ) == 4.75
)

total += 1
passed += check(
    "Total employment is 4.75 years",
    result.get(
        "total_years"
    ) == 4.75
)


normal_resume = """
PROFESSIONAL EXPERIENCE

Python Intern | Example Labs
January 2024 - June 2024
Built Python automation scripts.

PROJECTS
Automation Tool
"""

normal_result = extract_experience(
    normal_resume
)

print("\nNormal employment result:")
print(normal_result)

total += 1
passed += check(
    "Normal six-month employment retained",
    "January 2024 - June 2024"
    in normal_result.get(
        "date_ranges",
        []
    )
)

total += 1
passed += check(
    "Normal six-month employment equals 0.5 years",
    normal_result.get(
        "calculated_years"
    ) == 0.5
)


print()
print("=" * 60)
print(
    f"CAREER-BREAK TESTS: {passed}/{total} PASSED"
)
print("=" * 60)

if passed != total:
    raise SystemExit(1)
