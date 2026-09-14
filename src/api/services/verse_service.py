from collections import defaultdict

from fastapi import HTTPException
from src.api.db import engine
from sqlalchemy import text


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

def run_bfs(start_verse_id: int, max_depth_limit: int = 2, max_neighbor_limit: int = 3):
    try:
        with engine.connect() as conn:
            rows = conn.execute(text("""
                WITH RECURSIVE verse_references_ranked AS (
                    SELECT
                        vr.from_id
                        , vr.to_id
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
                ), 
                verse_references_filtered AS (
                    SELECT
                        vrr.from_id
                        , vrr.to_id
                        , vrr.to_book_name
                        , vrr.to_chapter_number
                        , vrr.to_verse_number
                        , vrr.to_verse_text
                        , vrr.num_votes
                        , vrr.reference_rank
                    FROM verse_references_ranked vrr
                    WHERE vrr.reference_rank <= :max_neighbor_limit
                ), 
                ref_tree AS (
                    -- Base Case: Get output row corresponding to level (i.e., the starting verse)
                    SELECT
                        0 AS level
                        , v.id AS verse_id
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
                "max_neighbor_limit": max_neighbor_limit
            }).fetchall()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    layered = defaultdict(list)
    for row in rows:
        layered[row.level].append({
            "verse_id": row.verse_id,
            "book_name": row.book_name,
            "chapter_number": row.chapter_number,
            "verse_number": row.verse_number,
            "verse_text": row.verse_text,
            "parent_id": row.parent_id,
            "link_strength": row.num_votes
        })
    return dict(layered)