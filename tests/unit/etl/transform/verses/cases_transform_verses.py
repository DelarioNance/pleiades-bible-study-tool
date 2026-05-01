class TransformCases:

    # -----------------------------------------------------
    # Valid cases
    # -----------------------------------------------------
    VALID = [
        {
            "input": [
                {
                    "book_id": "GEN",
                    "chapter_number": 1,
                    "verse_number": 1,
                    "content": ["In the beginning..."]
                },
                {
                    "book_id": "GEN",
                    "chapter_number": 1,
                    "verse_number": 2,
                    "content": ["And the earth was..."]
                }
            ],
            "expected": [
                {
                    "book_id": "GEN",
                    "chapter_number": 1,
                    "verse_number": 1,
                    "verse_text": "In the beginning..."
                },
                {
                    "book_id": "GEN",
                    "chapter_number": 1,
                    "verse_number": 2,
                    "verse_text": "And the earth was..."
                }
            ]
        }
    ]

    # -----------------------------------------------------
    # Edge cases
    # -----------------------------------------------------
    EDGE = [
        {
            # Multiple content strings — transform should take the first
            "input": [
                {
                    "book_id": "EX",
                    "chapter_number": 9,
                    "verse_number": 1,
                    "content": ["Only one verse", "Extra text ignored"]
                }
            ],
            "expected": [
                {
                    "book_id": "EX",
                    "chapter_number": 9,
                    "verse_number": 1,
                    "verse_text": "Only one verse"
                }
            ]
        }
    ]

    # -----------------------------------------------------
    # Error cases
    # -----------------------------------------------------
    ERROR = [
    ]
