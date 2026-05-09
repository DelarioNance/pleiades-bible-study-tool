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

from src.etl.extract_books import extract_books
from src.etl.derive_chapters import derive_chapters_from_books
from src.etl.extract_verses import extract_all_verses_async
from src.etl.extract_crossrefs import extract_verse_crossrefs

from src.etl.transform_books import transform_books
from src.etl.transfom_verses import transform_verses
from src.etl.transform_crossrefs import transform_verse_crossrefs

from src.etl.drop_bible_db_tables import drop_bible_db_tables
from src.etl.create_tables import create_table
import src.etl.ddl_schemas as schemas

from src.utils.db import get_db_engine


async def main(
    bible_api_url,
    engine
):
    # -----------------------------
    # Extract
    # -----------------------------
    books_raw = extract_books(bible_api_url)
    chapters_derived = derive_chapters_from_books(books_raw)
    verses_raw = await extract_all_verses_async(books_raw, bible_api_url)
    verse_crossrefs_raw = extract_verse_crossrefs()

    # -----------------------------
    # Transform
    # -----------------------------
    books_transformed = transform_books(books_raw)
    verses_transformed = transform_verses(verses_raw)
    refs_transformed = transform_verse_crossrefs(verse_crossrefs_raw)

    # -----------------------------
    # Load
    # -----------------------------

    # SQLAlchemy syntax for a transaction. After the transaction block closes, a commit is ran.
    # We use a transaction so that the load phase never has X% completion where X% is neither 
    # 0% nor 100%.
    # https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine.begin
    with engine.begin() as conn:
        drop_bible_db_tables(conn, table_names_ordered=['verse_references', 'verses', 'chapters', 'books'])

        create_table(conn, schemas.books)
        create_table(conn, schemas.chapters)
        create_table(conn, schemas.verses)
        create_table(conn, schemas.verse_references)

        # load_books(session, books_transformed)
        # load_chapters(session, chapters_transformed)
        # load_verses(session, verses_transformed)
        # load_crossrefs(session, refs_transformed)


# asyncio.run(main("https://bible.helloao.org/api/eng_kjv", get_db_engine('sandbox')))