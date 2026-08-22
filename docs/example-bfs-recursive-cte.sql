WITH RECURSIVE ref_tree AS (
	SELECT
		0 AS level
		, v.id AS verse_id
		, b.common_name AS book_name
		, c.chapter_number 
		, v.verse_number 
		, v.verse_text 
		, ARRAY[v.id] AS visited
	FROM books b
	INNER JOIN chapters c
		ON c.book_id = b.id
	INNER JOIN verses v
		ON v.chapter_id = c.id 
	WHERE v.id = 1
	UNION ALL
	SELECT
		rt.LEVEL + 1 AS level
		, vr.to_id 
		, b.common_name AS book_name
		, c.chapter_number 
		, v.verse_number 
		, v.verse_text 
		, array_append(rt.visited, vr.to_id)
	FROM verse_references vr
	INNER JOIN ref_tree rt
		ON rt.verse_id = vr.from_id 
	LEFT JOIN verses v
		ON v.id = vr.to_id 
	LEFT JOIN chapters c
		ON c.id = v.chapter_id 
	LEFT JOIN books b
		ON b.id = c.book_id 
	WHERE rt.LEVEL < 3 - 1
		AND vr.to_id <> all(rt.visited)
)
SELECT
	rt.LEVEL
	, rt.verse_id
	, rt.book_name
	, rt.chapter_number 
	, rt.verse_number 
	, rt.verse_text 
FROM ref_tree rt
;