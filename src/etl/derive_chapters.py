def derive_chapters_from_books(
    books: list
):
    chapters = [
        {   
            "book_id": book["id"],
            "chapter_number": chapter_num
        }
        for book in books
        for chapter_num in range(1, book["numberOfChapters"] + 1)
    ]

    return chapters