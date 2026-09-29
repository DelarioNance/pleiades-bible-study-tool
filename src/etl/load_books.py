from sqlalchemy import MetaData, insert, bindparam

from src.etl.data_test_seed import TEST_BOOKS


def load_books_non_test(conn, books):
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=conn)
    books_table = metadata_obj.tables['books']

    # run print(insert_stmt) to see the backend SQL statement
    insert_stmt = (
        insert(books_table)
        .values(
            common_name=bindparam('common_name'),
            canonical_order=bindparam('common_number'),
            is_test=False
        )
        .returning(books_table.c.id)
    )

    result = conn.execute(insert_stmt, books)
    db_book_ids = [row.id for row in result]
    
    return db_book_ids


def load_books_test(conn):
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=conn)
    books_table = metadata_obj.tables['books']

    insert_stmt = (
        insert(books_table)
        .values(
            common_name=bindparam('common_name'),
            canonical_order=bindparam('canonical_order'),
            is_test=True
        )
        .returning(books_table.c.id, sort_by_parameter_order=True)
    )

    test_books = [
        {'common_name': book['common_name'], 'canonical_order': book['canonical_order']}
        for book in TEST_BOOKS
    ]
    result = conn.execute(insert_stmt, test_books)
    db_book_ids = [row.id for row in result]

    return db_book_ids