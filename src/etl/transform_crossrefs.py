def transform_verse_crossrefs(crossrefs_in):
    crossrefs_normalized = crossrefs_in.assign(
        from_ref_normalized=lambda df: df["From Verse"].apply(normalize_ref),
        to_ref_normalized=lambda df: df["To Verse"].apply(normalize_ref),
    )

    # Split normalized refs into book/chapter/verse
    crossrefs_splitted = crossrefs_normalized.assign(
        from_book_name=lambda df: df["from_ref_normalized"].apply(get_book_from_normalized_ref),
        from_chapter_num=lambda df: df["from_ref_normalized"].apply(get_chapter_from_normalized_ref),
        from_verse_num=lambda df: df["from_ref_normalized"].apply(get_verse_from_normalized_ref),
        to_book_name=lambda df: df["to_ref_normalized"].apply(get_book_from_normalized_ref),
        to_chapter_num=lambda df: df["to_ref_normalized"].apply(get_chapter_from_normalized_ref),
        to_verse_num=lambda df: df["to_ref_normalized"].apply(get_verse_from_normalized_ref),
    )

    # Select and rename columns to match loader expectations
    crossrefs_selected = crossrefs_splitted[[
        "from_book_name",
        "from_chapter_num",
        "from_verse_num",
        "to_book_name",
        "to_chapter_num",
        "to_verse_num",
        "Votes",
    ]].rename(columns={
        "Votes": "num_votes",
    })

    # Filter out self-references
    crossrefs_filtered = crossrefs_selected[
        ~(
            (crossrefs_selected["from_book_name"] == crossrefs_selected["to_book_name"]) &
            (crossrefs_selected["from_chapter_num"] == crossrefs_selected["to_chapter_num"]) &
            (crossrefs_selected["from_verse_num"] == crossrefs_selected["to_verse_num"])
        )
    ]

    crossrefs_out = crossrefs_filtered.to_dict(orient="records")
    return crossrefs_out


def normalize_ref(ref):
    # Handles "Gen.1.3", "Rev.2.1-Eph.6.24"
    first_scripture = ref.split("-")[0].strip()
    book, chapter, verse = first_scripture.split(".")
    return f"{book}.{chapter}.{verse}"


def get_book_from_normalized_ref(ref):
    book, _, _ = ref.split(".")
    return book


def get_chapter_from_normalized_ref(ref):
    _, chapter, _ = ref.split(".")
    return chapter


def get_verse_from_normalized_ref(ref):
    _, _, verse = ref.split(".")
    return verse
