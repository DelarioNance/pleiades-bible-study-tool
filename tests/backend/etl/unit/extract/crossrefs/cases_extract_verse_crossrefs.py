import pandas as pd

class ExtractCases:
    VALID = [
        {
            "csv_read_output": pd.DataFrame.from_dict({
                "book": ["GEN", "EXO"],
                "chapter": [1, 2],
                "verse": [1, 2],
                "anchor": ["God", "He"],
                "references": ["REF1", "REF2"],
            }),
            "expected": pd.DataFrame.from_dict({
                "book": ["GEN", "EXO"],
                "chapter": [1, 2],
                "verse": [1, 2],
                "anchor": ["God", "He"],
                "references": ["REF1", "REF2"],
            }),
        }
    ]