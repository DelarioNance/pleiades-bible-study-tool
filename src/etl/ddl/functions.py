get_filtered_verse_reference_graph = """
CREATE OR REPLACE FUNCTION get_filtered_verse_reference_graph()
RETURNS TABLE (
    from_id INT,
    to_id INT,
    to_book_canonical_order INT,
    to_book_name TEXT,
    to_chapter_number INT,
    to_verse_number INT,
    to_verse_text TEXT,
    num_votes INT,
    reference_rank INT
)
LANGUAGE sql
AS $$
WITH verse_references_ranked AS (
    SELECT
        vr.from_id
        , vr.to_id
        , b.canonical_order AS to_book_canonical_order
        , b.common_name AS to_book_name
        , c.chapter_number AS to_chapter_number
        , v.verse_number AS to_verse_number
        , v.verse_text AS to_verse_text
        , vr.num_votes
        , RANK() OVER (
            PARTITION BY vr.from_id 
            ORDER BY 
                vr.num_votes DESC
                , b.canonical_order 
                , c.chapter_number 
                , v.verse_number 
        ) AS reference_rank -- no ties should occur if scriptures are unique in the DB
    FROM verse_references vr
    LEFT JOIN verses v 
        ON v.id = vr.to_id 
    LEFT JOIN chapters c
        ON c.id = v.chapter_id 
    LEFT JOIN books b
        ON b.id = c.book_id 
)
SELECT
    vrr.from_id
    , vrr.to_id
    , vrr.to_book_canonical_order
    , vrr.to_book_name
    , vrr.to_chapter_number
    , vrr.to_verse_number
    , vrr.to_verse_text
    , vrr.num_votes
    , vrr.reference_rank
FROM verse_references_ranked vrr
WHERE vrr.reference_rank <= 3
$$;
"""