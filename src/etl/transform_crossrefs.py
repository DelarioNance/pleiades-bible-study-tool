import re # using split method to split by multiple delimiters


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

    crossrefs_splitted = crossrefs_formatted.assign(
        ref_book=lambda df: df["ref_formatted"].apply(get_book_from_normalized_ref),
        ref_chapter=lambda df: df["ref_formatted"].apply(get_chapter_from_normalized_ref),
        ref_verse=lambda df: df["ref_formatted"].apply(get_verse_from_normalized_ref),
    )

    crossrefs_selected = crossrefs_splitted[[
        "book", 
        "chapter", 
        "verse", 
        "ref_book",
        "ref_chapter",
        "ref_verse",
    ]].rename(columns={
        "book": "from_book",
        "chapter": "from_chapter",
        "verse": "from_verse",
        "ref_book": "to_book",
        "ref_chapter": "to_chapter",
        "ref_verse": "to_verse",
    })

    # Could be worth creating an integration test for this even though the e2e test should catch it
    crossrefs_filtered = crossrefs_selected[
        ~(
            (crossrefs_selected["from_book"] == crossrefs_selected["to_book"]) &
            (crossrefs_selected["from_chapter"] == crossrefs_selected["to_chapter"]) &
            (crossrefs_selected["from_verse"] == crossrefs_selected["to_verse"])
        )
    ]

    crossrefs_out = crossrefs_filtered.to_dict(orient='records') # records orientation gives a list of dicts

    return crossrefs_out


def normalize_ref(ref):
    book_and_chapter, verses = ref.split(':') # Ex: "Genesis 1:1-3" → book_and_chapter = "Genesis 1", verses = "1-3"
    first_verse = re.split(r"[ ,\-]", verses)[0] # Ex: "1-3" → ["1", "3"] → first_verse = "1"
    ref_normalized = book_and_chapter + ':' + first_verse # Ex: "Genesis 1" + ":" + "1" → "Genesis 1:1"
    return ref_normalized


def get_book_from_normalized_ref(ref):
    book_and_chapter, _ = ref.split(':')
    book, _ = book_and_chapter.rsplit(' ', 1)
    return book


def get_chapter_from_normalized_ref(ref):
    book_and_chapter, _ = ref.split(':')
    chapter = book_and_chapter.split()[-1]
    return chapter


def get_verse_from_normalized_ref(ref):
    _, verse = ref.split(':')
    return verse