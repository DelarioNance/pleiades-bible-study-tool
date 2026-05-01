def transform_verses(
    verses_in
):
    verses_out = [
        {
            "book_id": verse_info["book_id"],
            "chapter_number": verse_info["chapter_number"],
            "verse_number": verse_info["verse_number"],
            "verse_text": verse_info["content"][0]
        }
        for verse_info in verses_in
    ]

    return verses_out