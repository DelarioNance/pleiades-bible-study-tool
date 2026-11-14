import pandas as pd


def extract_verse_crossrefs(tsv_path):
    df = pd.read_csv(
        tsv_path,
        sep="\t",
        usecols=[
            "From Verse",
            "To Verse",
            "Votes",
        ],
        dtype=str,
    )

    return df
