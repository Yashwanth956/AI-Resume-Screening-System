from resume_parser.project import extract_projects
import pdfplumber


PDF_PATH = r"C:\Users\Asus\OneDrive\Documents\AI-Resume-Screening-System\uploads\YASHWANTH_Resume(up).pdf"


print("\n========== PROJECT TEST ==========\n")


# ---------------------------------------------------------
# CHECK FILE
# ---------------------------------------------------------

import os

print("File:", PDF_PATH)
print("Exists:", os.path.exists(PDF_PATH))

if not os.path.exists(PDF_PATH):
    print("\nERROR: PDF file does not exist.")
    exit()


# ---------------------------------------------------------
# EXTRACT PDF TEXT
# ---------------------------------------------------------

text = ""

try:

    with pdfplumber.open(PDF_PATH) as pdf:

        print("Pages:", len(pdf.pages))

        for page_number, page in enumerate(pdf.pages, start=1):

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

except Exception as e:

    print("PDF ERROR:", e)
    exit()


# ---------------------------------------------------------
# EXTRACT PROJECTS
# ---------------------------------------------------------

projects = extract_projects(text)


# ---------------------------------------------------------
# DISPLAY
# ---------------------------------------------------------

print("\n========== EXTRACTED PROJECTS ==========\n")


if not projects:

    print("NO PROJECTS FOUND")

else:

    for index, project in enumerate(
        projects,
        start=1
    ):

        print(f"\nPROJECT {index}")
        print("--------------------------------")

        print(project)


print("\n========================================")