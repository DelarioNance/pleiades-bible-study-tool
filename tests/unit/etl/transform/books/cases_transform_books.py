class TransformCases:

    # -----------------------------------------------------
    # Valid cases
    # -----------------------------------------------------
    VALID = [
        {
            "input": [
                {
                    "id": "GEN",
                    "commonName": "Genesis",
                    "order": 1
                },
                {
                    "id": "EXO",
                    "commonName": "Exodus",
                    "order": 2
                }
            ],
            "expected": [
                {
                    "book_id": "GEN",
                    "common_name": "Genesis",
                    "common_number": 1,
                },
                {
                    "book_id": "EXO",
                    "common_name": "Exodus",
                    "common_number": 2
                }
            ]
        }
    ]

    # -----------------------------------------------------
    # Edge cases
    # -----------------------------------------------------
    EDGE = [
    ]

    # -----------------------------------------------------
    # Error cases
    # -----------------------------------------------------
    ERROR = [
    ]
