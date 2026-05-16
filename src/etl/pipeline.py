"""
Runs the full Bible ETL ingestion pipeline.

This module orchestrates the three major phases of the pipeline:

    Extract  →  Transform  →  Load

The pipeline ingests the complete Bible dataset, including:
- Books
- Chapters (derived from book metadata)
- Verses (fetched asynchronously for performance)
- Cross‑references (external dataset)

All loading is performed inside a single atomic SQL transaction to ensure
that the database is never left in a partially‑ingested state. Extraction 
and transformation occur outside the database transaction.

This ETL pipeline is not intended to be executed directly.
Instead, run it through the command‑line driver:

    python -m src.etl.run_etl <environment>
"""


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

from src.etl.load_books import load_books
from src.etl.build_id_map import build_id_map
from src.etl.load_chapters import load_chapters
from src.etl.load_verses import load_verses
from src.etl.load_crossrefs import load_verse_crossrefs


async def main(
    bible_api_url,
    engine
):
    # -----------------------------
    # Extract
    # -----------------------------
    print("Extracting books...")
    books_raw = extract_books(bible_api_url)

    print("Extracting chapters...")
    chapters_derived = derive_chapters_from_books(books_raw)

    print("Extracting verses...")
    verses_raw = await extract_all_verses_async(books_raw, bible_api_url)

    print("Extracting cross-references...")
    verse_crossrefs_raw = extract_verse_crossrefs()

    # -----------------------------
    # Transform
    # -----------------------------
    print("Transforming books...")
    books_transformed = transform_books(books_raw)

    print("Transforming verses...")
    verses_transformed = transform_verses(verses_raw)

    print("Transforming cross-references...")
    refs_transformed = transform_verse_crossrefs(verse_crossrefs_raw)
    
    with engine.begin() as conn:
        # -----------------------------
        # Pre-Load
        # -----------------------------
        print("Dropping existing tables...")
        drop_bible_db_tables(conn, table_names_ordered=['verse_references', 'verses', 'chapters', 'books'])

        print("Creating tables...")
        create_table(conn, schemas.books)
        create_table(conn, schemas.chapters)
        create_table(conn, schemas.verses)
        create_table(conn, schemas.verse_references)

        # -----------------------------
        # Load
        # -----------------------------
        print("Loading books...")
        db_book_ids = load_books(conn, books_transformed)
        book_id_mapping_api_to_db = build_id_map(books_transformed, db_book_ids, 'book_id')

        print("Loading chapters...")
        db_chapter_ids = load_chapters(conn, chapters_derived, book_id_mapping_api_to_db)
        chapter_id_mapping_api_to_db = build_id_map(chapters_derived, db_chapter_ids, ['book_id', 'chapter_number'])

        print("Loading verses...")
        db_verse_ids = load_verses(conn, verses_transformed, chapter_id_mapping_api_to_db)
        verse_id_mapping_api_to_db = build_id_map(
            verses_transformed,
            db_verse_ids,
            ['book_id', 'chapter_number', 'verse_number']
        )

        print("Loading cross-references...")
        load_verse_crossrefs(conn, refs_transformed, verse_id_mapping_api_to_db)
