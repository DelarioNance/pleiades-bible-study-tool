def transform_verses(
    verses_in
):
    verses_out = [
        {
            "book_id": verse_info["book_id"],
            "chapter_number": verse_info["chapter_number"],
            "verse_number": verse_info["verse_number"],
            "verse_text": extract_text(verse_info["content"][0])
        }
        for verse_info in verses_in
    ]

    return verses_out


def extract_text(content_item):
        # Case 1: already a string
        if isinstance(content_item, str):
            text = content_item

        # Case 2: dict with a 'text' field
        elif isinstance(content_item, dict) and "text" in content_item:
            text = content_item["text"]

        # Unsupported shape
        else:
            raise TypeError(f"Unsupported verse content format: {content_item}")

        # Normalize whitespace
        text = text.strip()

        # Remove leading pilcrow ¶ if present (doesn't handle case where there are multiple pilcrows)
        if text.startswith("¶"):
            text = text[1:].lstrip()

        return text