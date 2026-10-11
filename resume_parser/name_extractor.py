def extract_name(text):
    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip lines containing email
        if "@" in line:
            continue

        # Skip lines containing digits
        if any(ch.isdigit() for ch in line):
            continue

        # Skip common resume headings
        ignore_words = [
            "summary",
            "about",
            "education",
            "skills",
            "projects",
            "certificates",
            "experience",
            "technical skills",
            "strengths"
        ]

        if line.lower() in ignore_words:
            continue

        # Return the first short line as the name
        if len(line.split()) <= 5:
            return line

    return "Not Found"