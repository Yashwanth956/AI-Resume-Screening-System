import re


def extract_email(text):
    """
    Extract email address from resume text.
    Handles spaces around @ and common PDF extraction issues.
    """

    if not text:
        return "Not Found"

    # Remove markdown/mailto artifacts
    cleaned_text = text.replace("mailto:", " ")

    # Fix spaces around @
    cleaned_text = re.sub(
        r"\s*@\s*",
        "@",
        cleaned_text
    )

    # Email pattern
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    match = re.search(
        pattern,
        cleaned_text
    )

    if match:
        return match.group(0).strip()

    return "Not Found"


def extract_phone(text):
    """
    Extract phone number from resume text.

    Handles common formats such as:
    +91 9876543210
    +91-9876543210
    +91 98765 43210
    9876543210
    98765-43210
    (040) 12345678
    """

    if not text:
        return "Not Found"

    # Normalize common PDF extraction characters
    cleaned_text = text.replace(
        "\u00a0",
        " "
    )

    # -----------------------------------------------------
    # Indian mobile number with country code
    # -----------------------------------------------------

    patterns = [

        r"\+91[\s\-\.]*[6-9]\d{4}[\s\-\.]?\d{5}",

        r"\+91[\s\-\.]*[6-9]\d{9}",

        r"\b[6-9]\d{4}[\s\-\.]?\d{5}\b",

        r"\b[6-9]\d{9}\b",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            cleaned_text
        )

        if match:

            phone = match.group(0)

            # Normalize spaces/hyphens
            phone = re.sub(
                r"[\s\-\.]+",
                "",
                phone
            )

            return phone

    # -----------------------------------------------------
    # Other international/common phone formats
    # -----------------------------------------------------

    general_pattern = (
        r"(?:\+\d{1,3}[\s\-\.]?)?"
        r"\d{3,5}[\s\-\.]?\d{3,5}"
        r"[\s\-\.]?\d{3,5}"
    )

    matches = re.findall(
        general_pattern,
        cleaned_text
    )

    for phone in matches:

        digits = re.sub(
            r"\D",
            "",
            phone
        )

        # Avoid very short numbers
        if 10 <= len(digits) <= 15:

            return phone.strip()

    return "Not Found"