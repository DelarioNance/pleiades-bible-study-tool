# cases_extract_verses_in_chapter.py

class ExtractCases:

    # -----------------------------------------------------
    # Valid cases
    # -----------------------------------------------------
    VALID = [
        {
            "book_id": "GEN",
            "chapter": 1,
            "api_output": {
                "chapter": {
                    "content": [
                        {"type": "verse", "verse": 1, "text": "In the beginning..."},
                        {"type": "verse", "verse": 2, "text": "And the earth was..."},
                        {"type": "heading", "text": "Some heading"},
                    ]
                }
            },
            "expected": [
                {"type": "verse", "verse": 1, "text": "In the beginning..."},
                {"type": "verse", "verse": 2, "text": "And the earth was..."},
            ],
        }
    ]

    # -----------------------------------------------------
    # Edge cases
    # -----------------------------------------------------
    EDGE = [
        {
            "book_id": "GEN",
            "chapter": 1,
            "api_output": {
                "chapter": {
                    "content": [
                        {"type": "verse", "verse": 1, "text": "Only one verse"},
                        {"type": "note", "text": "Footnote"},
                        {"type": "unknown", "text": "Ignored"},
                    ]
                }
            },
            "expected": [
                {"type": "verse", "verse": 1, "text": "Only one verse"},
            ],
        }
    ]

    # -----------------------------------------------------
    # Error cases
    # -----------------------------------------------------
    ERROR = [
        {
            "book_id": "GEN",
            "chapter": 1,
            "api_output": {},  # missing chapter key
            "expected_exception": KeyError,
        },
        {
            "book_id": "GEN",
            "chapter": 1,
            "api_output": {"chapter": {}},  # missing content
            "expected_exception": KeyError,
        },
    ]
