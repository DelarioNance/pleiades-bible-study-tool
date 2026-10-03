from collections import defaultdict

from fastapi import HTTPException
from src.api.db import engine
from sqlalchemy import text

# Much of the code assumes a max neighbor count of 3, 
# so the code will need to be updated if a dynamic 
# max neighbor count is desired in the future.

def get_verse_info_from_chapter_id_and_verse_number(chapter_id, verse_number):
    try:
        with engine.connect() as conn:
            row = conn.execute(text("""
                SELECT
                    v.id 
                    , v.verse_number 
                    , v.verse_text
                FROM chapters c 
                INNER JOIN verses v
                    ON v.chapter_id = c.id 
                WHERE c.id = :chapter_id
                    AND v.verse_number = :verse_number
                ;
            """), {
                "chapter_id": chapter_id,
                "verse_number": verse_number
            }).fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if row is None:
        raise HTTPException(status_code=404, detail="Verse not found")
    
    return {
        "id": row.id,
        "number": row.verse_number,
        "text": row.verse_text
    }


def fetch_verses_from_text(verse_text: str):
    try:
        with engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT
                    v.id
                FROM verses v
                WHERE v.verse_text ILIKE :verse_text
                ;
            """), {
                "verse_text": verse_text
            }).fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if not rows:
        raise HTTPException(status_code=404, detail="No verses found matching the text")
    
    return [
        {
            "id": row.id
        }
        for row in rows
    ]

def run_bfs(start_verse_id: int, max_depth_limit: int = 2):
    try:
        with engine.connect() as conn:
            rows = conn.execute(text("""
                WITH RECURSIVE verse_references_filtered AS (
                    SELECT *
                    FROM get_filtered_verse_reference_graph()
                ),
                ref_tree AS (
                    -- Base Case: Get output row corresponding to level (i.e., the starting verse)
                    SELECT
                        0 AS level
                        , v.id AS verse_id
                        , b.canonical_order AS book_canonical_order
                        , b.common_name AS book_name
                        , c.chapter_number 
                        , v.verse_number 
                        , v.verse_text 
                        , NULL::int AS parent_id
                        , NULL::int AS num_votes
                        , ARRAY[v.id] AS visited -- -- track visited verse IDs to prevent cycles
                    FROM verses v
                    INNER JOIN chapters c
                        ON c.id = v.chapter_id 
                    INNER JOIN books b
                        ON b.id = c.book_id
                    WHERE v.id = :start_verse_id
                    UNION ALL
                    -- Recursive Step: Get output rows corresponding to the next level
                    SELECT
                        rt.level + 1 AS level
                        , vrf.to_id AS verse_id
                        , b.canonical_order AS book_canonical_order
                        , b.common_name AS book_name
                        , c.chapter_number 
                        , v.verse_number 
                        , v.verse_text 
                        , rt.verse_id AS parent_id
                        , vrf.num_votes AS num_votes
                        , array_append(rt.visited, vrf.to_id)
                    FROM ref_tree rt
                    INNER JOIN verse_references_filtered vrf
                        ON vrf.from_id = rt.verse_id
                    INNER JOIN verses v
                        ON v.id = vrf.to_id 
                    INNER JOIN chapters c
                        ON c.id = v.chapter_id 
                    INNER JOIN books b
                        ON b.id = c.book_id 
                    WHERE rt.level < :max_depth_limit
                        AND vrf.to_id <> all(rt.visited)
                )
                SELECT
                    rt.LEVEL
                    , rt.verse_id
                    , rt.book_canonical_order
                    , rt.book_name
                    , rt.chapter_number 
                    , rt.verse_number 
                    , rt.verse_text 
                    , rt.parent_id 
                    , rt.num_votes
                FROM ref_tree rt
                ;
            """), {
                "start_verse_id": start_verse_id,
                "max_depth_limit": max_depth_limit,
            }).fetchall()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    layered_result = defaultdict(list)
    for row in rows:
        layered_result[row.level].append({
            "verse_id": row.verse_id,
            "book_canonical_order": row.book_canonical_order,
            "book_name": row.book_name,
            "chapter_number": row.chapter_number,
            "verse_number": row.verse_number,
            "verse_text": row.verse_text,
            "parent_id": row.parent_id,
            "link_strength": row.num_votes
        })

    for layer in layered_result:
        layered_result[layer].sort(key=lambda x: (
            x["book_canonical_order"], 
            x["chapter_number"], 
            x["verse_number"]
        ))

    return dict(layered_result)
