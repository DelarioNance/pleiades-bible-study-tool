# cases_derive_chapters.py

class DeriveChapterCases:

    # -----------------------------------------------------
    # Valid cases
    # -----------------------------------------------------
    VALID = [
        {
            "books": [
                {"id": "GEN", "numberOfChapters": 3},
                {"id": "EXO", "numberOfChapters": 2},
            ],
            "expected": [
                {"book_id": "GEN", "chapter_number": 1},
                {"book_id": "GEN", "chapter_number": 2},
                {"book_id": "GEN", "chapter_number": 3},
                {"book_id": "EXO", "chapter_number": 1},
                {"book_id": "EXO", "chapter_number": 2},
            ],
        }
    ]

    # -----------------------------------------------------
    # Edge cases
    # -----------------------------------------------------
    EDGE = [
        {
            # Book with zero chapters (valid but produces no output)
            "books": [
                {"id": "OB", "numberOfChapters": 0}
            ],
            "expected": []
        },
        {
            # Multiple books with mixed chapter counts
            "books": [
                {"id": "PSA", "numberOfChapters": 1},
                {"id": "JOB", "numberOfChapters": 0},
                {"id": "RUT", "numberOfChapters": 4},
            ],
            "expected": [
                {"book_id": "PSA", "chapter_number": 1},
                {"book_id": "RUT", "chapter_number": 1},
                {"book_id": "RUT", "chapter_number": 2},
                {"book_id": "RUT", "chapter_number": 3},
                {"book_id": "RUT", "chapter_number": 4},
            ],
        }
    ]

    # -----------------------------------------------------
    # Error cases
    # -----------------------------------------------------
    ERROR = [
        {
            # Missing numberOfChapters
            "books": [
                {"id": "GEN"}
            ],
            "expected_exception": KeyError
        },
        {
            # Missing id
            "books": [
                {"numberOfChapters": 5}
            ],
            "expected_exception": KeyError
        },
        {
            # Wrong type for numberOfChapters
            "books": [
                {"id": "GEN", "numberOfChapters": "fifty"}
            ],
            "expected_exception": TypeError
        },
    ]
