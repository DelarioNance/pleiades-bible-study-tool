# cases_extract_books.py
class ExtractCases:
    VALID = [
        {
            "api_output": {
                "books": [
                    {"id": "GEN", "commonName": "Genesis", "order": 1},
                    {"id": "EXO", "commonName": "Exodus", "order": 2},
                ]
            },
            "expected": [
                {"id": "GEN", "commonName": "Genesis", "order": 1},
                {"id": "EXO", "commonName": "Exodus", "order": 2},
            ],
        }
    ]

    EDGE = [
        # Extra fields
        {
            "api_output": {
                "books": [
                    {
                        "id": "LEV",
                        "commonName": "Leviticus",
                        "order": 3,
                        "extra": "ignored",
                    }
                ]
            },
            "expected": [
                {
                    "id": "LEV",
                    "commonName": "Leviticus",
                    "order": 3,
                    "extra": "ignored",
                }
            ],
        }
    ]

    ERROR = [
    ]
