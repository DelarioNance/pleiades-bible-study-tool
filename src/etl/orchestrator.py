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

import asyncio
from sqlalchemy.orm import Session

from src.etl.extract_books import extract_books
from src.etl.extract_verses import extract_all_verses_async
from src.etl.extract_crossrefs import extract_verse_crossrefs
from src.utils.db import get_db_engine

async def main(
    bible_api_url: str = "https://bible.helloao.org/api/eng_kjv",
    engine=None
):
    # -----------------------------
    # Extract
    # -----------------------------
    books_raw = extract_books(bible_api_url)
    all_verses_raw = await extract_all_verses_async(books_raw, bible_api_url)
    verse_crossrefs_raw = extract_verse_crossrefs()

    # # -----------------------------
    # # Transform
    # # -----------------------------
    # books_transformed = transform_books(books_raw)
    # chapters_transformed = transform_chapters(chapters_raw)
    # verses_transformed = transform_verses(verses_raw)
    # refs_transformed = transform_crossrefs(refs_raw)

    # # -----------------------------
    # # Load
    # # -----------------------------
    # if engine is None:
    #     engine = get_db_engine('test')  # default to test environment for safety

    # with Session(engine) as session:
    #     with session.begin(): # using session.begin() for atomicity
    #         clear_bible_database_data(session)
    #         load_books(session, books_transformed)
    #         load_chapters(session, chapters_transformed)
    #         load_verses(session, verses_transformed)
    #         load_crossrefs(session, refs_transformed)