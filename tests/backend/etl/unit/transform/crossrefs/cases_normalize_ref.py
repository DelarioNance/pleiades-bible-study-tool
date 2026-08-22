class NormalizeRefCases:

    # -----------------------------------------------------
    # Valid cases
    # -----------------------------------------------------
    VALID = [
        {
            "input": "John 3:16",
            "expected": "John 3:16"
        },
        {
            "input": "John 3:9-6",
            "expected": "John 3:9"
        },
        {
            "input": "John 3:9,16",
            "expected": "John 3:9"
        },
        {
            "input": "John 3:9, 16",
            "expected": "John 3:9"
        },
        {
            "input": "2 Thess 3:9-19, 8",
            "expected": "2 Thess 3:9"
        }
    ]

    # -----------------------------------------------------
    # Edge cases
    # -----------------------------------------------------
    EDGE = [
        # Add later if needed (e.g., extra spaces, weird punctuation)
    ]

    # -----------------------------------------------------
    # Error cases
    # -----------------------------------------------------
    ERROR = [
        # Add later if you want to test malformed input
    ]
