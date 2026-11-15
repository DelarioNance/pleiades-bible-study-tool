from sqlalchemy import text

from tests.etl.constants import NUM_VERSES


def test_correct_number_of_verses(conn_from_etl_run):
    query = text("SELECT COUNT(id) FROM verses WHERE is_test = FALSE;")
    (count,) = conn_from_etl_run.execute(query).one()

    assert count == NUM_VERSES, (
        f"Expected {NUM_VERSES} total verses, but ETL produced {count}"
    )


def test_no_verse_text_has_surrounding_whitespace(conn_from_etl_run):
    query = text("""
        SELECT id, verse_text
        FROM verses
        WHERE verse_text != TRIM(verse_text);
    """)

    bad = conn_from_etl_run.execute(query).fetchall()

    assert bad == [], f"Verses with leading/trailing whitespace found: {bad}"


def test_no_verse_text_contains_pilcrow(conn_from_etl_run):
    query = text("""
        SELECT id, verse_text
        FROM verses
        WHERE verse_text LIKE '%¶%';
    """)

    pilcrows = conn_from_etl_run.execute(query).fetchall()

    assert pilcrows == [], f"Verses containing a pilcrow (¶) found: {pilcrows}"
