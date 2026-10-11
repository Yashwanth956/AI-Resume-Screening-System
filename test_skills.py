import pdfplumber

from resume_parser.skills import extract_skills


pdf_path = r"uploads\YASHWANTH_Resume(up).pdf"


text = ""

with pdfplumber.open(pdf_path) as pdf:

    for page in pdf.pages:

        page_text = (
            page.extract_text()
            or ""
        )

        text += (
            page_text
            + "\n"
        )


skills = extract_skills(
    text
)


print()
print("=" * 60)
print("EXTRACTED SKILLS FROM YASHWANTH PDF")
print("=" * 60)

for skill in skills:

    print(
        "-",
        skill
    )


print()
print(
    "Total Skills:",
    len(skills)
)

print("=" * 60)