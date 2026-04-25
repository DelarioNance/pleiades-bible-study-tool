"""
Orchestrates the full Bible ETL ingestion process.

This module coordinates the Extract → Transform → Load phases for:
- books
- chapters
- verses
- cross-references

Extraction and transformation occur outside the database transaction.
All loading happens inside a single atomic transaction to ensure that
either the entire ingestion succeeds or none of it is applied.
"""

from sqlalchemy.orm import Session

from extract_books import extract_books
from bible_ingestion.extract_verses_in_chapter import extract_chapters
from bible_ingestion.extract_verses_in_chapter import extract_verses_in_chapter
from extract_crossrefs import extract_crossrefs
from transform_books import transform_books
from transform_chapters import transform_chapters
from transform_verses import transform_verses
from transform_crossrefs import transform_crossrefs
from load_books import load_books
from load_chapters import load_chapters
from load_verses import load_verses
from load_crossrefs import load_crossrefs
from clear_bible_database_data import clear_bible_database_data
from utils.db import get_db_engine


def main(
    bible_api_url: str = "https://bible.helloao.org/api/eng_kjv",
    engine=None
):
    # -----------------------------
    # Extract
    # -----------------------------
    books_raw = extract_books(bible_api_url)
    verses_raw = []
    for book in books_raw:
        num_chapters = book['numberOfChapters']
        for chapter in range(1, num_chapters + 1):
            verses_raw.extend(extract_verses_in_chapter(book['id'], chapter))
    refs_raw = extract_crossrefs()

    # -----------------------------
    # Transform
    # -----------------------------
    books_transformed = transform_books(books_raw)
    chapters_transformed = transform_chapters(chapters_raw)
    verses_transformed = transform_verses(verses_raw)
    refs_transformed = transform_crossrefs(refs_raw)

    # -----------------------------
    # Load
    # -----------------------------
    if engine is None:
        engine = get_db_engine('test')  # default to test environment for safety

    with Session(engine) as session:
        with session.begin(): # using session.begin() for atomicity
            clear_bible_database_data(session)
            load_books(session, books_transformed)
            load_chapters(session, chapters_transformed)
            load_verses(session, verses_transformed)
            load_crossrefs(session, refs_transformed)
