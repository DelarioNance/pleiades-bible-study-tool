from api.queries.utils import fetch_all, fetch_one


def get_books(is_test: bool = False):
    sql = """
        SELECT
            b.id
            , b.common_name
            , b.canonical_order
        FROM books b
        WHERE b.is_test = :is_test
        ;
    """
    params = {"is_test": is_test}
    rows = fetch_all(sql, params)

    return [
        {"id": row.id, "name": row.common_name, "order": row.canonical_order}
        for row in rows
    ]


def get_book_from_book_name(book_name):
    sql = """
        SELECT
            b.id
            , b.common_name
            , b.canonical_order
        FROM books b 
        WHERE b.common_name = :book_name
        ;
    """

    params = {"book_name": book_name}
    row = fetch_one(sql, params)

    return {"id": row.id, "name": row.common_name, "order": row.canonical_order}
