from sqlalchemy import MetaData, insert, bindparam

def load_chapters(conn, chapters, book_id_mapping_api_to_db):
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=conn)
    chapters_table = metadata_obj.tables['chapters']

    insert_stmt = (
        insert(chapters_table)
        .values(
            book_id=bindparam('db_book_id'),
            chapter_number=bindparam('chapter_number'),
        )
        .returning(chapters_table.c.id)
    )

    chapters_with_db_book_ids = [
        {
            **chapter,
            'db_book_id': book_id_mapping_api_to_db[chapter['book_id']]
        }
        for chapter in chapters
    ]

    result = conn.execute(insert_stmt, chapters_with_db_book_ids)
    db_chapter_ids = [row.id for row in result]
    
    return db_chapter_ids