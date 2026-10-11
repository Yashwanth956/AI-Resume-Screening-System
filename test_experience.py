import os
import pdfplumber

from resume_parser.experience import extract_experience


PDF_PATH = r"C:\Users\Asus\OneDrive\Documents\AI-Resume-Screening-System\uploads\YASHWANTH_Resume(up).pdf"


print("\n========== EXPERIENCE TEST ==========\n")

print("File:", PDF_PATH)
print("Exists:", os.path.exists(PDF_PATH))

if not os.path.exists(PDF_PATH):
    print("\nERROR: PDF file does not exist.")
    exit()


# =========================================================
# EXTRACT PDF TEXT
# =========================================================

text = ""

try:

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
                    f"Page {page_number}: No text found"
                )

except Exception as e:

    print("\nPDF ERROR:")
    print(e)
    exit()


# =========================================================
# EXPERIENCE EXTRACTION
# =========================================================

print("\n========== EXTRACTED EXPERIENCE ==========\n")

try:

    experience = extract_experience(text)

except Exception as e:

    print("\nERROR inside extract_experience():")
    print(type(e).__name__)
    print(e)
    exit()


# =========================================================
# DISPLAY
# =========================================================

print("Total Years:")
print(
    experience.get(
        "total_years",
        0
    )
)

print("\nStated Years:")
print(
    experience.get(
        "stated_years",
        0
    )
)

print("\nCalculated Years:")
print(
    experience.get(
        "calculated_years",
        0
    )
)

print("\nJob Titles:")
print(
    experience.get(
        "job_titles",
        []
    )
)

print("\nDate Ranges:")
print(
    experience.get(
        "date_ranges",
        []
    )
)

print("\nExperience Records:")
print(
    experience.get(
        "records",
        []
    )
)

print("\n========================================")