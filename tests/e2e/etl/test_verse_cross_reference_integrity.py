from sqlalchemy import text

def test_no_cross_reference_loops(conn_from_etl_run):
    query = text("""
        SELECT id, from_id, to_id
        FROM verse_references
        WHERE from_id = to_id;
    """)

    loops = conn_from_etl_run.execute(query).fetchall()

    assert loops == [], f"Cross‑reference loops found: {loops}"


def test_every_cross_reference_has_head(conn_from_etl_run):
    query = text("""
        SELECT id
        FROM verse_references
        WHERE from_id IS NULL;
    """)

    missing_heads = conn_from_etl_run.execute(query).fetchall()

    assert missing_heads == [], f"Cross‑references missing head verse: {missing_heads}"


def test_every_cross_reference_has_tail(conn_from_etl_run):
    query = text("""
        SELECT id
        FROM verse_references
        WHERE to_id IS NULL;
    """)

    missing_tails = conn_from_etl_run.execute(query).fetchall()

    assert missing_tails == [], f"Cross‑references missing tail verse: {missing_tails}"


def test_cross_reference_tail_is_valid_verse(conn_from_etl_run):
    query = text("""
        SELECT vr.id, vr.to_id
        FROM verse_references vr
        LEFT JOIN verses v ON vr.to_id = v.id
        WHERE v.id IS NULL;
    """)

    invalid_tails = conn_from_etl_run.execute(query).fetchall()

    assert invalid_tails == [], f"Cross‑references with invalid tail verse: {invalid_tails}"


def test_cross_reference_head_is_valid_verse(conn_from_etl_run):
    query = text("""
        SELECT vr.id, vr.from_id
        FROM verse_references vr
        LEFT JOIN verses v ON vr.from_id = v.id
        WHERE v.id IS NULL;
    """)

    invalid_heads = conn_from_etl_run.execute(query).fetchall()

    assert invalid_heads == [], f"Cross‑references with invalid head verse: {invalid_heads}"
