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
            return content_item

        # Case 2: dict with a 'text' field
        if isinstance(content_item, dict) and "text" in content_item:
            return content_item["text"]

        # Unsupported shape
        raise TypeError(f"Unsupported verse content format: {content_item}")