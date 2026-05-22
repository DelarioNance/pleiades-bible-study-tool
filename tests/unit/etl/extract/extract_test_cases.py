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

# -----------------------------
# VERSES
# -----------------------------

VERSES_NORMAL = (
    {
        "chapter": {
            "content": [
                {"type": "verse", "number": 1, "content": ["In the beginning..."]},
                {"type": "verse", "number": 2, "content": ["And the earth was..."]},
            ]
        }
    },
    [
        {"type": "verse", "number": 1, "content": ["In the beginning..."]},
        {"type": "verse", "number": 2, "content": ["And the earth was..."]},
    ]
)

VERSES_MIXED_CONTENT = (
    {
        "chapter": {
            "content": [
                {"type": "heading", "text": "The Creation"},
                {"type": "verse", "number": 1, "content": ["In the beginning..."]},
                {"type": "paragraph"},
                {"type": "verse", "number": 2, "content": ["And the earth was..."]},
            ]
        }
    },
    [
        {"type": "verse", "number": 1, "content": ["In the beginning..."]},
        {"type": "verse", "number": 2, "content": ["And the earth was..."]},
    ]
)

VERSES_WITH_FOOTNOTE = (
    {
        "chapter": {
            "content": [
                {
                    "type": "verse",
                    "number": 6,
                    "content": ["And Seth lived...", {"noteId": 57}]
                }
            ]
        }
    },
    [
        {
            "type": "verse",
            "number": 6,
            "content": ["And Seth lived...", {"noteId": 57}]
        }
    ]
)

VERSES_MIXED_CONTENT_TYPES = (
    {
        "chapter": {
            "content": [
                {
                    "type": "verse",
                    "number": 9,
                    "content": [
                        "¶ And Enos lived ninety years, and begat Cainan:",
                        {"noteId": 58},
                        "additional text"
                    ]
                }
            ]
        }
    },
    [
        {
            "type": "verse",
            "number": 9,
            "content": [
                "¶ And Enos lived ninety years, and begat Cainan:",
                {"noteId": 58},
                "additional text"
            ]
        }
    ]
)

VERSES_NO_VERSES = (
    {
        "chapter": {
            "content": [
                {"type": "heading", "text": "Genealogy"},
                {"type": "paragraph"},
                {"type": "note", "noteId": 12},
            ]
        }
    },
    []
)

VERSES_MISSING_TYPE = (
    {
        "chapter": {
            "content": [
                {"number": 1, "content": ["Missing type field"]},
                {"type": "verse", "number": 2, "content": ["Valid verse"]},
            ]
        }
    },
    [
        {"type": "verse", "number": 2, "content": ["Valid verse"]}
    ]
)

VERSES_EMPTY_CONTENT = (
    {
        "chapter": {
            "content": []
        }
    },
    []
)

# Malformed cases (these expect exceptions, not normal output)
VERSES_MALFORMED_CONTENT = (
    {
        "chapter": {
            "content": "not a list"
        }
    },
    TypeError
)

VERSES_MISSING_CHAPTER_KEY = (
    {},
    KeyError
)

VERSES_MISSING_CONTENT_KEY = (
    {
        "chapter": {}
    },
    KeyError
)

EXTRACT_VERSES_CASES = [
    VERSES_NORMAL,
    VERSES_MIXED_CONTENT,
    VERSES_WITH_FOOTNOTE,
    VERSES_MIXED_CONTENT_TYPES,
    VERSES_NO_VERSES,
    VERSES_MISSING_TYPE,
    VERSES_EMPTY_CONTENT,
    VERSES_MALFORMED_CONTENT,
    VERSES_MISSING_CHAPTER_KEY,
    VERSES_MISSING_CONTENT_KEY,
]
