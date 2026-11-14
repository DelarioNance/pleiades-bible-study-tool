import pandas as pd

class ExtractCases:
    VALID = [
        {
            "csv_read_output": pd.DataFrame.from_dict({
                "From Verse": ["GEN", "EXO"],
                "To Verse": ["GEN.1.1", "EXO.2.2"],
                "Votes": [5, 10]
            }),
            "expected": pd.DataFrame.from_dict({
                "From Verse": ["GEN", "EXO"],
                "To Verse": ["GEN.1.1", "EXO.2.2"],
                "Votes": [5, 10]
            }),
        }
    ]