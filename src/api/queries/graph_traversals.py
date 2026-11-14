from collections import defaultdict

from api.queries.utils import fetch_all


def run_bfs(start_verse_id: int, max_depth_limit: int = 2):
    sql = """
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
    """

    params = {"start_verse_id": start_verse_id, "max_depth_limit": max_depth_limit}

    rows = fetch_all(sql, params)

    layered_result = defaultdict(list)
    for row in rows:
        layered_result[row.level].append(
            {
                "verse_id": row.verse_id,
                "book_canonical_order": row.book_canonical_order,
                "book_name": row.book_name,
                "chapter_number": row.chapter_number,
                "verse_number": row.verse_number,
                "verse_text": row.verse_text,
                "parent_id": row.parent_id,
                "link_strength": row.num_votes,
            }
        )

    for layer in layered_result:
        layered_result[layer].sort(
            key=lambda x: (
                x["book_canonical_order"],
                x["chapter_number"],
                x["verse_number"],
            )
        )

    return dict(layered_result)
