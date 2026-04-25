# -----------------------------
# BOOKS
# -----------------------------
BOOKS_NORMAL = (
    {"books": [
        {"id": "GEN", "commonName": "Genesis", "order": 1},
        {"id": "EXO", "commonName": "Exodus", "order": 2},
    ]},
    [
        {"id": "GEN", "commonName": "Genesis", "order": 1},
        {"id": "EXO", "commonName": "Exodus", "order": 2},
    ]
)

BOOKS_EMPTY = (
    {"books": []},
    []
)

BOOKS_WITH_EXTRA_FIELDS = (
    {"books": [
        {"id": "LEV", "commonName": "Leviticus", "order": 3, "extra": "ignored"},
    ]},
    [
        {"id": "LEV", "commonName": "Leviticus", "order": 3, "extra": "ignored"},
    ]
)

EXTRACT_BOOKS_CASES = [
    BOOKS_NORMAL,
    BOOKS_EMPTY,
    BOOKS_WITH_EXTRA_FIELDS,
]
