from src.etl.data.seed.test_data import TEST_BOOKS, TEST_CHAPTERS, TEST_VERSES
from src.etl.ddl.rebuild_ddl import rebuild_ddl
from src.etl.derive.derive_chapters import derive_chapters_from_books
from src.etl.extract.extract_books import extract_books
from src.etl.extract.extract_crossrefs import extract_verse_crossrefs
from src.etl.extract.extract_verses import extract_verses_async
from src.etl.load.load_books import load_books_non_test, load_books_test
from src.etl.load.load_chapters import load_chapters_non_test, load_chapters_test
from src.etl.load.load_crossrefs import (
    load_verse_crossrefs_non_test,
    load_verse_crossrefs_test,
)
from src.etl.load.load_verses import load_verses_non_test, load_verses_test
from src.etl.transform.transfom_verses import transform_verses
from src.etl.transform.transform_books import transform_books
from src.etl.transform.transform_crossrefs import transform_verse_crossrefs
from src.etl.utils import build_id_map

# May want to make these configurable in the future
BIBLE_API_URL = "https://bible.helloao.org/api/eng_kjv"
CROSSREF_DATA_PATH = "src/etl/data/src/open_bible_info_verse_crossrefs_kjv.tsv"


async def pipeline(
    engine,
    load_test_data=False,  # default to False to reduce chance of test data in prod
):
    # -----------------------------
    # Extract
    # -----------------------------
    print("Extracting books...")
    books_raw = extract_books(BIBLE_API_URL)

    print("Extracting chapters...")
    chapters_derived = derive_chapters_from_books(books_raw)

    print("Extracting verses...")
    verses_raw = await extract_verses_async(books_raw, BIBLE_API_URL)

    print("Extracting cross-references...")
    verse_crossrefs_raw = extract_verse_crossrefs(CROSSREF_DATA_PATH)

    # -----------------------------
    # Transform
    # -----------------------------
    print("Transforming books...")
    books_transformed = transform_books(books_raw)

    print("Transforming verses...")
    verses_transformed = transform_verses(verses_raw)

    print("Transforming cross-references...")
    refs_transformed = transform_verse_crossrefs(verse_crossrefs_raw)

    with (
        engine.begin() as conn  # Atomic transaction block (https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine.begin)
    ):
        # -----------------------------
        # Pre-Load
        # -----------------------------
        print("Rebuilding table(s) and function(s)...")
        rebuild_ddl(conn)

        # -----------------------------
        # Load
        # -----------------------------
        print("Loading real books...")
        db_book_ids = load_books_non_test(conn, books_transformed)
        book_id_mapping_api_to_db = build_id_map(
            books_transformed, db_book_ids, "book_id"
        )

        print("Loading real chapters...")
        db_chapter_ids = load_chapters_non_test(
            conn, chapters_derived, book_id_mapping_api_to_db
        )
        chapter_id_mapping_api_to_db = build_id_map(
            chapters_derived, db_chapter_ids, ["book_id", "chapter_number"]
        )

        print("Loading real verses...")
        db_verse_ids = load_verses_non_test(
            conn, verses_transformed, chapter_id_mapping_api_to_db
        )
        verse_id_mapping_api_to_db = build_id_map(
            verses_transformed,
            db_verse_ids,
            ["book_id", "chapter_number", "verse_number"],
        )

        print("Loading real cross-references...")
        load_verse_crossrefs_non_test(
            conn, refs_transformed, verse_id_mapping_api_to_db
        )

        if load_test_data:
            print("Loading test books...")
            db_test_book_ids = load_books_test(conn)
            test_book_id_mapping = build_id_map(TEST_BOOKS, db_test_book_ids, "book_id")

            print("Loading test chapters...")
            db_test_chapter_ids = load_chapters_test(conn, test_book_id_mapping)
            test_chapter_id_mapping = build_id_map(
                TEST_CHAPTERS, db_test_chapter_ids, ["book_id", "chapter_number"]
            )

            print("Loading test verses...")
            db_test_verse_ids = load_verses_test(conn, test_chapter_id_mapping)
            test_verse_id_mapping = build_id_map(
                TEST_VERSES,
                db_test_verse_ids,
                ["book_id", "chapter_number", "verse_number"],
            )

            print("Loading test cross-references...")
            load_verse_crossrefs_test(conn, test_verse_id_mapping)
