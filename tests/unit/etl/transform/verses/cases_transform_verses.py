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
        },
        {
            # Verse text begins with ¶ — transform should strip it
            "input": [
                {
                    "book_id": "PSA",
                    "chapter_number": 23,
                    "verse_number": 1,
                    "content": ["¶The Lord is my shepherd"]
                }
            ],
            "expected": [
                {
                    "book_id": "PSA",
                    "chapter_number": 23,
                    "verse_number": 1,
                    "verse_text": "The Lord is my shepherd"
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
        },
        {
            # 1st content value is a dict
            "input": [
                {
                    "book_id": "EX",
                    "chapter_number": 9,
                    "verse_number": 1,
                    "content": [{"text": "Only one verse"}, "Extra text ignored"]
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
        },
        {
            # 1st content value is a dict AND begins with ¶
            "input": [
                {
                    "book_id": "PSA",
                    "chapter_number": 23,
                    "verse_number": 2,
                    "content": [{"text": "¶He maketh me to lie down in green pastures"}]
                }
            ],
            "expected": [
                {
                    "book_id": "PSA",
                    "chapter_number": 23,
                    "verse_number": 2,
                    "verse_text": "He maketh me to lie down in green pastures"
                }
            ]
        }
    ]

    # -----------------------------------------------------
    # Error cases
    # -----------------------------------------------------
    ERROR = [
    ]
