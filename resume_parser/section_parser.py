def extract_section(text, section_name, next_sections):
    """
    Extract text between one section heading
    and the next section heading.
    """

    lower_text = text.lower()

    start = lower_text.find(section_name.lower())

    if start == -1:
        return ""

    end = len(text)

    for section in next_sections:
        position = lower_text.find(
            section.lower(),
            start + len(section_name)
        )

        if position != -1 and position < end:
            end = position

    return text[start:end].strip()