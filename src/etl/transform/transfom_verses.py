def transform_verses(verses_in):
    verses_out = [
        {
            "book_id": verse_info["book_id"],
            "chapter_number": verse_info["chapter_number"],
            "verse_number": verse_info["verse_number"],
            "verse_text": extract_text(verse_info["content"]),
        }
        for verse_info in verses_in
    ]

    return verses_out


def extract_text(content_list):
    # 1. Prefer dicts with a 'text' field (used to handle verses like Luke 13:24)
    for item in content_list:
        if isinstance(item, dict) and "text" in item:
            return normalize_text(item["text"])

    # 2. Otherwise, fall back to the first non-empty string
    for item in content_list:
        if isinstance(item, str):
            return normalize_text(item)

    raise ValueError("No valid text found in content_list")


def normalize_text(text):
    text_normalized = text.strip()

    if text.startswith("¶"):
        text_normalized = text[1:].strip()

    return text_normalized.strip()
