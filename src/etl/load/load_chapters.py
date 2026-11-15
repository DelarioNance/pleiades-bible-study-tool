from sqlalchemy import MetaData, bindparam, insert

from src.etl.data.seed.test_data import TEST_CHAPTERS


def load_chapters_non_test(conn, chapters, book_id_mapping_api_to_db):
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=conn)
    chapters_table = metadata_obj.tables["chapters"]

    insert_stmt = (
        insert(chapters_table)
        .values(
            book_id=bindparam("db_book_id"),
            chapter_number=bindparam("chapter_number"),
            is_test=False,
        )
        .returning(chapters_table.c.id)
    )

    chapters_with_db_book_ids = [
        {**chapter, "db_book_id": book_id_mapping_api_to_db[chapter["book_id"]]}
        for chapter in chapters
    ]

    result = conn.execute(insert_stmt, chapters_with_db_book_ids)
    db_chapter_ids = [row.id for row in result]

    return db_chapter_ids


def load_chapters_test(conn, test_book_id_mapping):
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=conn)
    chapters_table = metadata_obj.tables["chapters"]

    insert_stmt = (
        insert(chapters_table)
        .values(
            book_id=bindparam("book_id"),
            chapter_number=bindparam("chapter_number"),
            is_test=True,
        )
        .returning(chapters_table.c.id)
    )

    test_chapters_with_db_book_ids = [
        {
            "book_id": test_book_id_mapping[chapter["book_id"]],
            "chapter_number": chapter["chapter_number"],
        }
        for chapter in TEST_CHAPTERS
    ]

    result = conn.execute(insert_stmt, test_chapters_with_db_book_ids)
    return [row.id for row in result]
