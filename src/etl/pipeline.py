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
from src.etl.ddl.schemas import books, chapters, verses, verse_references
from src.etl.create_or_replace_functions import create_or_replace_function
from src.etl.ddl.functions import get_filtered_verse_reference_graph

from src.etl.load_books import load_books_non_test, load_books_test
from src.etl.build_id_map import build_id_map
from src.etl.load_chapters import load_chapters_non_test, load_chapters_test
from src.etl.load_verses import load_verses_non_test, load_verses_test
from src.etl.load_crossrefs import load_verse_crossrefs_non_test, load_verse_crossrefs_test
from src.etl.data_test_seed import TEST_BOOKS, TEST_CHAPTERS, TEST_VERSES


async def pipeline(
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
    verse_crossrefs_raw = extract_verse_crossrefs("data/open_bible_info_verse_crossrefs_kjv.tsv")

    # -----------------------------
    # Transform
    # -----------------------------
    print("Transforming books...")
    books_transformed = transform_books(books_raw)

    print("Transforming verses...")
    verses_transformed = transform_verses(verses_raw)

    print("Transforming cross-references...")
    refs_transformed = transform_verse_crossrefs(verse_crossrefs_raw)
    
    with engine.begin() as conn: # Atomic transaction block (https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine.begin)
        # -----------------------------
        # Pre-Load
        # -----------------------------
        print("Dropping existing tables...")
        drop_bible_db_tables(conn, table_names_ordered=['verse_references', 'verses', 'chapters', 'books'])

        print("Creating tables...")
        create_table(conn, books)
        create_table(conn, chapters)
        create_table(conn, verses)
        create_table(conn, verse_references)

        print("Creating functions...")
        create_or_replace_function(conn, get_filtered_verse_reference_graph)

        # -----------------------------
        # Load (non-test data)
        # -----------------------------
        # print("Loading real books...")
        # db_book_ids = load_books_non_test(conn, books_transformed)
        # book_id_mapping_api_to_db = build_id_map(books_transformed, db_book_ids, 'book_id')

        # print("Loading real chapters...")
        # db_chapter_ids = load_chapters_non_test(conn, chapters_derived, book_id_mapping_api_to_db)
        # chapter_id_mapping_api_to_db = build_id_map(chapters_derived, db_chapter_ids, ['book_id', 'chapter_number'])

        # print("Loading real verses...")
        # db_verse_ids = load_verses_non_test(conn, verses_transformed, chapter_id_mapping_api_to_db)
        # verse_id_mapping_api_to_db = build_id_map(
        #     verses_transformed,
        #     db_verse_ids,
        #     ['book_id', 'chapter_number', 'verse_number']
        # )

        # print("Loading real cross-references...")
        # load_verse_crossrefs_non_test(conn, refs_transformed, verse_id_mapping_api_to_db)

        # -----------------------------
        # Load (test data)
        # -----------------------------
        print("Loading test books...")
        db_test_book_ids = load_books_test(conn)
        test_book_id_mapping = build_id_map(TEST_BOOKS, db_test_book_ids, 'book_id')

        print("Loading test chapters...")
        db_test_chapter_ids = load_chapters_test(conn, test_book_id_mapping)
        test_chapter_id_mapping = build_id_map(TEST_CHAPTERS, db_test_chapter_ids, ['book_id', 'chapter_number'])

        print("Loading test verses...")
        db_test_verse_ids = load_verses_test(conn, test_chapter_id_mapping)
        test_verse_id_mapping = build_id_map(
            TEST_VERSES,
            db_test_verse_ids,
            ['book_id', 'chapter_number', 'verse_number']
        )

        print("Loading test cross-references...")
        load_verse_crossrefs_test(conn, test_verse_id_mapping)