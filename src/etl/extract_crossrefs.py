import pandas as pd

def extract_verse_crossrefs(
    tsv_path: str = "data/verse_crossrefs_kjv.tsv"
):
    df = pd.read_csv(tsv_path, sep="\t", usecols=[
            "book", 
            "chapter", 
            "verse", 
            "references"
        ], dtype=str)

    return df
