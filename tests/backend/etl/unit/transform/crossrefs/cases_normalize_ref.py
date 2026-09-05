class NormalizeRefCases:

    # -----------------------------------------------------
    # Valid cases
    # -----------------------------------------------------
    VALID = [
        {
            "input": "John.3.16",
            "expected": "John.3.16"
        },
        {
            "input": "1 Thess.4.5",
            "expected": "1 Thess.4.5"
        },
        {
            "input": "1Thess.4.5",
            "expected": "1Thess.4.5"
        },
        {
            "input": "1Thess.4.5 - 2Cor.5.6",
            "expected": "1Thess.4.5"
        },
        {
            "input": "1Thess.4.5-2Cor.5.6",
            "expected": "1Thess.4.5"
        },
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
