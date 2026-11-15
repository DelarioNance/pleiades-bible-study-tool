from fastapi import APIRouter

import src.api.queries.books as book_queries
import src.api.queries.chapters as chapter_queries
import src.api.queries.verses as verse_queries

router = APIRouter(prefix="/v1/books")


@router.get("/")
def get_books(is_test: bool = False):
    return book_queries.get_books(is_test=is_test)


@router.get("/{book_id}/chapters")
def get_chapters_from_book_id(book_id: int):
    return chapter_queries.get_chapters_from_book_id(book_id)


@router.get("/{book_id}/chapters/{chapter_number}/verses")
def get_verses_from_book_id_and_chapter_number(book_id: int, chapter_number: int):
    return verse_queries.get_verses_from_book_id_and_chapter_number(
        book_id, chapter_number
    )
