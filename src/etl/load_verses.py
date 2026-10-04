from sqlalchemy import MetaData, insert, bindparam

from src.etl.data_test_seed import TEST_VERSES


def load_verses_non_test(conn, verses, chapter_id_mapping_api_to_db):
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=conn)
    verses_table = metadata_obj.tables['verses']

    insert_stmt = (
        insert(verses_table)
        .values(
            chapter_id=bindparam('db_chapter_id'),
            verse_number=bindparam('verse_number'),
            verse_text=bindparam('verse_text'),
            is_test=False
        )
        .returning(verses_table.c.id)
    )

    verses_with_db_chapter_ids = [
        {
            **verse,
            'db_chapter_id': chapter_id_mapping_api_to_db[(verse['book_id'], verse['chapter_number'])]
        }
        for verse in verses
    ]

    result = conn.execute(insert_stmt, verses_with_db_chapter_ids)
    db_verse_ids = [row.id for row in result]

    return db_verse_ids


def load_verses_test(conn, test_chapter_id_mapping):
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=conn)
    verses_table = metadata_obj.tables['verses']

    insert_stmt = (
        insert(verses_table)
        .values(
            chapter_id=bindparam('db_chapter_id'),
            verse_number=bindparam('verse_number'),
            verse_text=bindparam('verse_text'),
            is_test=True
        )
        .returning(verses_table.c.id)
    )

    test_verses_with_db_chapter_ids = [
        {
            **verse,
            'db_chapter_id': test_chapter_id_mapping[(verse['book_id'], verse['chapter_number'])]
        }
        for verse in TEST_VERSES
    ]

    result = conn.execute(insert_stmt, test_verses_with_db_chapter_ids)
    db_verse_ids = [row.id for row in result]

    return db_verse_ids