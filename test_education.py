import os
import pdfplumber

from resume_parser.education import extract_education


# =========================================================
# PDF FILE
# =========================================================

PDF_FILE = r"C:\Users\Asus\OneDrive\Documents\AI-Resume-Screening-System\uploads\YASHWANTH_Resume(up).pdf"


# =========================================================
# CHECK FILE
# =========================================================

print("=" * 60)
print("EDUCATION EXTRACTION TEST")
print("=" * 60)

print("\nPDF FILE:")
print(PDF_FILE)

if not os.path.exists(PDF_FILE):
    print("\nERROR: PDF file does not exist.")
    print("Check the path and filename.")
    exit()

print("\nFile exists: TRUE")


# =========================================================
# EXTRACT PDF TEXT
# =========================================================

text = ""

try:

    with pdfplumber.open(PDF_FILE) as pdf:

        print("\nPages:", len(pdf.pages))

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

    print("\nERROR while reading PDF:")
    print(e)
    exit()


# =========================================================
# CHECK TEXT
# =========================================================

print("\n" + "=" * 60)
print("EXTRACTED TEXT CHECK")
print("=" * 60)

print(
    "Characters extracted:",
    len(text)
)

if not text.strip():

    print("\nERROR: No text extracted from PDF.")
    exit()


# =========================================================
# EDUCATION EXTRACTION
# =========================================================

print("\n" + "=" * 60)
print("EDUCATION RESULTS")
print("=" * 60)

try:

    education = extract_education(text)

except Exception as e:

    print("\nERROR inside extract_education():")
    print(type(e).__name__)
    print(e)
    exit()


# =========================================================
# DISPLAY RESULTS
# =========================================================

if not education:

    print("\nNo education records found.")

else:

    for index, item in enumerate(
        education,
        start=1
    ):

        print(f"\nEducation {index}")
        print("-" * 40)

        print(
            "Degree:",
            item.get("degree", "")
        )

        print(
            "Institution:",
            item.get("institution", "")
        )

        print(
            "Score:",
            item.get("score", "")
        )

        print(
            "Passing Year:",
            item.get("duration", "")
        )


# =========================================================
# TOTAL
# =========================================================

print("\n" + "=" * 60)

print(
    "TOTAL EDUCATION RECORDS:",
    len(education)
)

print("=" * 60)