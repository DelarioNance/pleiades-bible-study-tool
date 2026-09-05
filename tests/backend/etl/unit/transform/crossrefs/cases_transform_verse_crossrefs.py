import pandas as pd

class TransformVerseCrossrefsCases:

    # -----------------------------------------------------
    # Valid cases
    # -----------------------------------------------------
    VALID = [
        {
            # No loop here — keep as-is
            "input": pd.DataFrame([
                {
                    "From Verse": "John.3.16",
                    "To Verse": "John.3.16",
                    "Votes": "5"
                }
            ]),
            "expected": [
                # ❌ This is a loop (John 3:16 → John 3:16)
                # Since loops are now removed, expected output is EMPTY.
            ]
        },

        {
            "input": pd.DataFrame([
                {
                    "From Verse": "1 Thess.4.5",
                    "To Verse": "John.3.16",
                    "Votes": "5"
                },
                {
                    "From Verse": "1 Thess.4.5",
                    "To Verse": "1 Thess.4.5",
                    "Votes": "5"
                }
            ]),
            "expected": [
                # ❌ Remove the loop (1 Thess 4:5 → 1 Thess 4:5)
                {
                    "from_book_name": "1 Thess",
                    "from_chapter_num": "4",
                    "from_verse_num": "5",
                    "to_book_name": "John",
                    "to_chapter_num": "3",
                    "to_verse_num": "16",
                    "num_votes": "5",
                }
            ]
        },

        {
            # No loops here — keep both
            "input": pd.DataFrame([
                {
                    "From Verse": "Genesis.1.1",
                    "To Verse": "John.1.1",
                    "Votes": "5"
                },
                {
                    "From Verse": "Genesis.1.1",
                    "To Verse": "Hebrews.11.3",
                    "Votes": "5"
                }
            ]),
            "expected": [
                {
                    "from_book_name": "Genesis",
                    "from_chapter_num": "1",
                    "from_verse_num": "1",
                    "to_book_name": "John",
                    "to_chapter_num": "1",
                    "to_verse_num": "1",
                    "num_votes": "5"
                },
                {
                    "from_book_name": "Genesis",
                    "from_chapter_num": "1",
                    "from_verse_num": "1",
                    "to_book_name": "Hebrews",
                    "to_chapter_num": "11",
                    "to_verse_num": "3",
                    "num_votes": "5"
                }
            ]
        },

        {
            # No loops here — keep all
            "input": pd.DataFrame([
                {
                    "From Verse": "2Cor.8.28",
                    "To Verse": "Genesis.50.20",
                    "Votes": "5"
                },
                {
                    "From Verse": "Rom.8.28",
                    "To Verse": "2Tim.1.2",
                    "Votes": "5"
                },
                {
                    "From Verse": "2Cor.8.28",
                    "To Verse": "2Tim.23.1",
                    "Votes": "5"
                }
            ]),
            "expected": [
                {
                    "from_book_name": "2Cor",
                    "from_chapter_num": "8",
                    "from_verse_num": "28",
                    "to_book_name": "Genesis",
                    "to_chapter_num": "50",
                    "to_verse_num": "20",
                    "num_votes": "5",
                },
                {
                    "from_book_name": "Rom",
                    "from_chapter_num": "8",
                    "from_verse_num": "28",
                    "to_book_name": "2Tim",
                    "to_chapter_num": "1",
                    "to_verse_num": "2",
                    "num_votes": "5",
                },
                {
                    "from_book_name": "2Cor",
                    "from_chapter_num": "8",
                    "from_verse_num": "28",
                    "to_book_name": "2Tim",
                    "to_chapter_num": "23",
                    "to_verse_num": "1",
                    "num_votes": "5",
                }
            ]
        }
    ]

    # -----------------------------------------------------
    # Edge cases
    # -----------------------------------------------------
    EDGE = [
        # Add later if needed
    ]

    # -----------------------------------------------------
    # Error cases
    # -----------------------------------------------------
    ERROR = [
        # Add malformed inputs here if needed
    ]
