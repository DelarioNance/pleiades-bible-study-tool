from sqlalchemy import MetaData, insert, bindparam

def load_books(conn, books):
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=conn)
    books_table = metadata_obj.tables['books']

    # run print(insert_stmt) to see the backend SQL statement
    insert_stmt = (
        insert(books_table)
        .values(
            common_name=bindparam('common_name'),
            canonical_order=bindparam('common_number') 
        )
        .returning(books_table.c.id)
    )

    result = conn.execute(insert_stmt, books)
    db_book_ids = [row.id for row in result]
    
    return db_book_ids