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
                        {"type": "verse", "number": 1, "content": "In the beginning..."},
                        {"type": "verse", "number": 2, "content": "And the earth was..."},
                        {"type": "heading", "text": "Some heading"},
                    ]
                }
            },
            "expected": [
                {
                    "book_id": "GEN",
                    "chapter_number": 1,
                    "verse_number": 1,
                    "content": "In the beginning...",
                },
                {
                    "book_id": "GEN",
                    "chapter_number": 1,
                    "verse_number": 2,
                    "content": "And the earth was...",
                },
            ],
        }
    ]

    # -----------------------------------------------------
    # Edge cases (graceful handling)
    # -----------------------------------------------------
    EDGE = [
        # Missing number field
        {
            "book_id": "GEN",
            "chapter": 1,
            "api_output": {
                "chapter": {
                    "content": [
                        {"type": "verse", "content": "Missing number field"},
                    ]
                }
            },
            "expected": [
                {
                    "book_id": "GEN",
                    "chapter_number": 1,
                    "verse_number": None,
                    "content": "Missing number field",
                }
            ],
        },

        # Missing content field
        {
            "book_id": "GEN",
            "chapter": 1,
            "api_output": {
                "chapter": {
                    "content": [
                        {"type": "verse", "number": 5},
                    ]
                }
            },
            "expected": [
                {
                    "book_id": "GEN",
                    "chapter_number": 1,
                    "verse_number": 5,
                    "content": None,
                }
            ],
        },

        # Missing both number and content
        {
            "book_id": "GEN",
            "chapter": 1,
            "api_output": {
                "chapter": {
                    "content": [
                        {"type": "verse"},
                    ]
                }
            },
            "expected": [
                {
                    "book_id": "GEN",
                    "chapter_number": 1,
                    "verse_number": None,
                    "content": None,
                }
            ],
        },

        # Non-verse types ignored
        {
            "book_id": "EX",
            "chapter": 9,
            "api_output": {
                "chapter": {
                    "content": [
                        {"type": "note", "text": "Footnote"},
                        {"type": "unknown", "text": "Ignored"},
                        {"type": "heading", "text": "Heading"},
                    ]
                }
            },
            "expected": [],  # No verses
        },
    ]

    # -----------------------------------------------------
    # Error cases (structural failures)
    # -----------------------------------------------------
    ERROR = [
        
    ]
