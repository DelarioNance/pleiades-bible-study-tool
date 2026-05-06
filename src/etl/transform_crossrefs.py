import re # regex module for string manipulation


def transform_verse_crossrefs(
    crossrefs_in
):
    crossrefs_in_splitted = crossrefs_in.assign(
        refs_list=lambda df: df["references"].str.split('|') # <series>.str.<method> tells Pandas to apply the <method> each row of the series
    )

    crossrefs_in_exploded = (
        crossrefs_in_splitted
        .explode('refs_list')
        .reset_index(drop=True)
        .rename(columns={"refs_list": "ref"})
    )

    crossrefs_formatted = crossrefs_in_exploded.assign(
        ref_formatted=lambda df: df["ref"].apply(normalize_ref)
    )

    crossrefs_selected = crossrefs_formatted[[
        "book", 
        "chapter", 
        "verse", 
        "ref_formatted"
    ]].rename(columns={"ref_formatted": "ref"})

    crossrefs_out = crossrefs_selected.to_dict(orient='records') # records orientation gives a list of dicsts

    return crossrefs_out


def normalize_ref(ref):
    book_and_chapter, verses = ref.split(':') # Ex: "Genesis 1:1-3" → book_and_chapter = "Genesis 1", verses = "1-3"
    first_verse = re.split(r"[ ,\-]", verses)[0] # Ex: "1-3" → ["1", "3"] → first_verse = "1"
    ref_normalized = book_and_chapter + ':' + first_verse # Ex: "Genesis 1" + ":" + "1" → "Genesis 1:1"
    return ref_normalized