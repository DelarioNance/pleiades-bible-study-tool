# cases_build_id_map.py

class BuildIdMapCases:
    VALID = [
        {
            "from_items": [
                {"book_id": "GEN"},
                {"book_id": "EXO"},
                {"book_id": "LEV"},
            ],
            "to_ids": [1, 2, 3],
            "key": "book_id",
            "expected": {
                "GEN": 1,
                "EXO": 2,
                "LEV": 3,
            },
        },
        {
            "from_items": [
                {
                    "a": 1,
                    "b": 2,
                    "c": 3,
                    "d": 4,
                    "e": 5,
                },
                {
                    "a": 10,
                    "b": 20,
                    "c": 30,
                    "d": 40,
                    "e": 50,
                },
            ],
            "to_ids": [100, 200],
            "key": ["a", "c", "d", "e"],
            "expected": {
                (1, 3, 4, 5): 100,
                (10, 30, 40, 50): 200,
            },
        }
    ]

    EDGE = []

    ERROR = []
