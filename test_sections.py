import os
import pdfplumber

from resume_parser.sections import print_sections


# =========================================================
# PDF FILE
# =========================================================

PDF_FILE = r"C:\Users\Asus\OneDrive\Documents\AI-Resume-Screening-System\uploads\YASHWANTH_Resume(up).pdf"


# =========================================================
# CHECK FILE
# =========================================================

print("\n========== FILE CHECK ==========")

print("File:", PDF_FILE)

print("Exists:", os.path.exists(PDF_FILE))

if not os.path.exists(PDF_FILE):

    print("\nERROR: PDF file does not exist.")
    print("Check the filename and location.")

    raise SystemExit


# =========================================================
# EXTRACT TEXT
# =========================================================

print("\n========== PDF EXTRACTION ==========")

text = ""

with pdfplumber.open(PDF_FILE) as pdf:

    print("Pages:", len(pdf.pages))

    for page_number, page in enumerate(pdf.pages, start=1):

        page_text = page.extract_text()

        print(
            f"Page {page_number}:",
            "Text found" if page_text else "NO TEXT"
        )

        if page_text:

            text += page_text + "\n"


# =========================================================
# CHECK TEXT
# =========================================================

print("\n========== TEXT CHECK ==========")

print("Characters extracted:", len(text))

if not text.strip():

    print("ERROR: No text was extracted from PDF.")

    raise SystemExit


print("\nFirst 1000 characters:\n")

print(text[:1000])


# =========================================================
# SECTION DETECTION
# =========================================================

print_sections(text)