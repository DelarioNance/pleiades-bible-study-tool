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
                    "book": "John",
                    "chapter": "3",
                    "verse": "16",
                    "references": "John 3:16"
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
                    "book": "1 Thess",
                    "chapter": "4",
                    "verse": "5",
                    "references": "1 Thess 4:5|John 3:16"
                }
            ]),
            "expected": [
                # ❌ Remove the loop (1 Thess 4:5 → 1 Thess 4:5)
                {
                    "from_book": "1 Thess",
                    "from_chapter": "4",
                    "from_verse": "5",
                    "to_book": "John",
                    "to_chapter": "3",
                    "to_verse": "16"
                }
            ]
        },

        {
            # No loops here — keep both
            "input": pd.DataFrame([
                {
                    "book": "Genesis",
                    "chapter": "1",
                    "verse": "1",
                    "references": "John 1:1|Hebrews 11:3"
                }
            ]),
            "expected": [
                {
                    "from_book": "Genesis",
                    "from_chapter": "1",
                    "from_verse": "1",
                    "to_book": "John",
                    "to_chapter": "1",
                    "to_verse": "1"
                },
                {
                    "from_book": "Genesis",
                    "from_chapter": "1",
                    "from_verse": "1",
                    "to_book": "Hebrews",
                    "to_chapter": "11",
                    "to_verse": "3"
                }
            ]
        },

        {
            # No loops here — keep all
            "input": pd.DataFrame([
                {
                    "book": "Romans",
                    "chapter": "8",
                    "verse": "28",
                    "references": "Genesis 50:20|James 1:2|Psalm 23:1"
                }
            ]),
            "expected": [
                {
                    "from_book": "Romans",
                    "from_chapter": "8",
                    "from_verse": "28",
                    "to_book": "Genesis",
                    "to_chapter": "50",
                    "to_verse": "20"
                },
                {
                    "from_book": "Romans",
                    "from_chapter": "8",
                    "from_verse": "28",
                    "to_book": "James",
                    "to_chapter": "1",
                    "to_verse": "2"
                },
                {
                    "from_book": "Romans",
                    "from_chapter": "8",
                    "from_verse": "28",
                    "to_book": "Psalm",
                    "to_chapter": "23",
                    "to_verse": "1"
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
