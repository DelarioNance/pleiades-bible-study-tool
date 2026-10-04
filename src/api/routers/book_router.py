from fastapi import APIRouter
from src.api.services.book_service import (
    fetch_books,
    fetch_chapters_from_book_id,
    fetch_verses_from_book_id_and_chapter_number
)

router = APIRouter(prefix="/v1/books")


@router.get("/")
def get_books(is_test: bool = False):
    return fetch_books(is_test=is_test)


@router.get("/{book_id}/chapters") # https://fastapi.tiangolo.com/tutorial/path-params/
def get_chapters_from_book_id(book_id: int):
    return fetch_chapters_from_book_id(book_id)


@router.get("/{book_id}/chapters/{chapter_number}/verses")
def get_verses_from_book_id_and_chapter_number(book_id: int, chapter_number: int):
    return fetch_verses_from_book_id_and_chapter_number(book_id, chapter_number)
