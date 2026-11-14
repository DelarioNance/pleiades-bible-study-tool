class GetBookCases:

    # -----------------------------------------------------
    # Valid cases
    # -----------------------------------------------------
    VALID = [
        {
            "input": "John.3.16",
            "expected": "John"
        },
        {
            "input": "1 Thess.4.5",
            "expected": "1 Thess"
        },
        {
            "input": "1Thess.4.5",
            "expected": "1Thess"
        },
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
        # Add malformed inputs here if you want to test exceptions
    ]
