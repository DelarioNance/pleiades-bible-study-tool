def transform_books(books_in):
    books_out = [
        {
            "book_id": book_info["id"],
            "common_name": book_info["commonName"],
            "common_number": book_info["order"],
        }
        for book_info in books_in
    ]

    return books_out
