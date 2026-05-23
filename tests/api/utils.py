def get_books(test_client):
    return test_client.get("/v1/books").json()


def get_book_by_order(test_client, book_order):
    books = test_client.get("/v1/books/").json()
    chosen_book = next(book for book in books if book["order"] == book_order)
    return chosen_book


def get_chapters_by_book(test_client, book_id):
    chapters = test_client.get(f"/v1/books/{book_id}/chapters").json()
    return chapters


def get_verses_by_book_and_chapter(test_client, book_id, chapter_number):
    verses = test_client.get(f"/v1/books/{book_id}/chapters/{chapter_number}/verses").json()
    return verses


def get_chapter_by_book_order_and_chapter_number(test_client, book_order, chapter_number):
    chosen_book = get_book_by_order(test_client, book_order)
    chapters = get_chapters_by_book(test_client, chosen_book["id"])
    chosen_chapter = next(chapter for chapter in chapters if chapter["number"] == chapter_number)
    return chosen_chapter


def get_verses_by_chapter_id(test_client, chapter_id):
    verses = test_client.get(f"/v1/chapters/{chapter_id}/verses").json()
    return verses
