"""Hand-verified expected BFS responses for the seeded test graphs.

Key: root verse_text. Value: the exact JSON the traversal endpoint should return.
Level keys are strings because JSON object keys are always strings.

The parent_text is used instead of parent_id to avoid hardcoding DB-generated 
verse_ids in the expected results. The parent_text is guaranteed to be unique 
in the seeded test data, so it can be used to look up the parent_id in the actual 
response.
"""

expected_bfs_results = {
    "TEST ROOT: No children": {
        "0": [
            {
                "book_canonical_order": 1001,
                "book_name": "TEST: Book A1",
                "chapter_number": 9001,
                "verse_number": 1,
                "verse_text": "TEST ROOT: No children",
                "parent_text": None,
                "link_strength": None,
            }
        ],
    },

    "TEST ROOT: 1 child": {
        "0": [
            {
                "book_canonical_order": 1001,
                "book_name": "TEST: Book A1",
                "chapter_number": 9001,
                "verse_number": 4,
                "verse_text": "TEST ROOT: 1 child",
                "parent_text": None,
                "link_strength": None,
            }
        ],
        "1": [
            {
                "book_canonical_order": 1002,
                "book_name": "TEST: Book B1",
                "chapter_number": 9002,
                "verse_number": 9,
                "verse_text": "TEST CHILD: 1 child - the child",
                "parent_text": "TEST ROOT: 1 child",
                "link_strength": 7,
            }
        ],
    },

    "TEST ROOT: 3 children, middle has children": {
        "0": [
            {
                "book_canonical_order": 1001,
                "book_name": "TEST: Book A1",
                "chapter_number": 9001,
                "verse_number": 5,
                "verse_text": "TEST ROOT: 3 children, middle has children",
                "parent_text": None,
                "link_strength": None,
            }
        ],
        "1": [
            {
                "book_canonical_order": 1002,
                "book_name": "TEST: Book B1",
                "chapter_number": 9002,
                "verse_number": 10,
                "verse_text": "TEST CHILD: Middle-child scenario child 1",
                "parent_text": "TEST ROOT: 3 children, middle has children",
                "link_strength": 30,
            },
            {
                "book_canonical_order": 1002,
                "book_name": "TEST: Book B1",
                "chapter_number": 9002,
                "verse_number": 11,
                "verse_text": "TEST CHILD: Middle-child scenario child 2",
                "parent_text": "TEST ROOT: 3 children, middle has children",
                "link_strength": 20,
            },
            {
                "book_canonical_order": 1002,
                "book_name": "TEST: Book B1",
                "chapter_number": 9002,
                "verse_number": 12,
                "verse_text": "TEST CHILD: Middle-child scenario child 3",
                "parent_text": "TEST ROOT: 3 children, middle has children",
                "link_strength": 10,
            },
        ],
        "2": [
            {
                "book_canonical_order": 1003,
                "book_name": "TEST: Book C1",
                "chapter_number": 9003,
                "verse_number": 10,
                "verse_text": "TEST GRANDCHILD: Middle-child scenario grandchild 1",
                "parent_text": "TEST CHILD: Middle-child scenario child 2",
                "link_strength": 14,
            },
            {
                "book_canonical_order": 1003,
                "book_name": "TEST: Book C1",
                "chapter_number": 9003,
                "verse_number": 11,
                "verse_text": "TEST GRANDCHILD: Middle-child scenario grandchild 2",
                "parent_text": "TEST CHILD: Middle-child scenario child 2",
                "link_strength": 13,
            },
            {
                "book_canonical_order": 1003,
                "book_name": "TEST: Book C1",
                "chapter_number": 9003,
                "verse_number": 12,
                "verse_text": "TEST GRANDCHILD: Middle-child scenario grandchild 3",
                "parent_text": "TEST CHILD: Middle-child scenario child 2",
                "link_strength": 12,
            },
        ],
    },

    "TEST ROOT: Dense at layers 0-1; sparse as layer 2": {
        "0": [
            {
                "book_canonical_order": 1001,
                "book_name": "TEST: Book A1",
                "chapter_number": 9001,
                "verse_number": 3,
                "verse_text": "TEST ROOT: Dense at layers 0-1; sparse as layer 2",
                "parent_text": None,
                "link_strength": None,
            }
        ],
        "1": [
            {
                "book_canonical_order": 1002,
                "book_name": "TEST: Book B1",
                "chapter_number": 9002,
                "verse_number": 6,
                "verse_text": "TEST CHILD: Dense 0-1 child 1",
                "parent_text": "TEST ROOT: Dense at layers 0-1; sparse as layer 2",
                "link_strength": 30,
            },
            {
                "book_canonical_order": 1002,
                "book_name": "TEST: Book B1",
                "chapter_number": 9002,
                "verse_number": 7,
                "verse_text": "TEST CHILD: Dense 0-1 child 2",
                "parent_text": "TEST ROOT: Dense at layers 0-1; sparse as layer 2",
                "link_strength": 20,
            },
            {
                "book_canonical_order": 1002,
                "book_name": "TEST: Book B1",
                "chapter_number": 9002,
                "verse_number": 8,
                "verse_text": "TEST CHILD: Dense 0-1 child 3",
                "parent_text": "TEST ROOT: Dense at layers 0-1; sparse as layer 2",
                "link_strength": 10,
            },
        ],
    },

    "TEST ROOT: Dense at layers 0-2": {
        "0": [
            {
                "book_canonical_order": 1001,
                "book_name": "TEST: Book A1",
                "chapter_number": 9001,
                "verse_number": 2,
                "verse_text": "TEST ROOT: Dense at layers 0-2",
                "parent_text": None,
                "link_strength": None,
            }
        ],
        "1": [
            {
                "book_canonical_order": 1002,
                "book_name": "TEST: Book B1",
                "chapter_number": 9002,
                "verse_number": 1,
                "verse_text": "TEST CHILD: Dense 0-2 child 1",
                "parent_text": "TEST ROOT: Dense at layers 0-2",
                "link_strength": 100,
            },
            {
                "book_canonical_order": 1002,
                "book_name": "TEST: Book B1",
                "chapter_number": 9002,
                "verse_number": 2,
                "verse_text": "TEST CHILD: Dense 0-2 child 2",
                "parent_text": "TEST ROOT: Dense at layers 0-2",
                "link_strength": 90,
            },
            {
                "book_canonical_order": 1002,
                "book_name": "TEST: Book B1",
                "chapter_number": 9002,
                "verse_number": 3,
                "verse_text": "TEST CHILD: Dense 0-2 child 3",
                "parent_text": "TEST ROOT: Dense at layers 0-2",
                "link_strength": 80,
            },
        ],
        "2": [
            {
                "book_canonical_order": 1003,
                "book_name": "TEST: Book C1",
                "chapter_number": 9003,
                "verse_number": 1,
                "verse_text": "TEST GRANDCHILD: Dense 0-2 grandchild 1.1",
                "parent_text": "TEST CHILD: Dense 0-2 child 1",
                "link_strength": 49,
            },
            {
                "book_canonical_order": 1003,
                "book_name": "TEST: Book C1",
                "chapter_number": 9003,
                "verse_number": 2,
                "verse_text": "TEST GRANDCHILD: Dense 0-2 grandchild 1.2",
                "parent_text": "TEST CHILD: Dense 0-2 child 1",
                "link_strength": 48,
            },
            {
                "book_canonical_order": 1003,
                "book_name": "TEST: Book C1",
                "chapter_number": 9003,
                "verse_number": 3,
                "verse_text": "TEST GRANDCHILD: Dense 0-2 grandchild 1.3",
                "parent_text": "TEST CHILD: Dense 0-2 child 1",
                "link_strength": 47,
            },
            {
                "book_canonical_order": 1003,
                "book_name": "TEST: Book C1",
                "chapter_number": 9003,
                "verse_number": 4,
                "verse_text": "TEST GRANDCHILD: Dense 0-2 grandchild 2.1",
                "parent_text": "TEST CHILD: Dense 0-2 child 2",
                "link_strength": 49,
            },
            {
                "book_canonical_order": 1003,
                "book_name": "TEST: Book C1",
                "chapter_number": 9003,
                "verse_number": 5,
                "verse_text": "TEST GRANDCHILD: Dense 0-2 grandchild 2.2",
                "parent_text": "TEST CHILD: Dense 0-2 child 2",
                "link_strength": 48,
            },
            {
                "book_canonical_order": 1003,
                "book_name": "TEST: Book C1",
                "chapter_number": 9003,
                "verse_number": 6,
                "verse_text": "TEST GRANDCHILD: Dense 0-2 grandchild 2.3",
                "parent_text": "TEST CHILD: Dense 0-2 child 2",
                "link_strength": 47,
            },
            {
                "book_canonical_order": 1003,
                "book_name": "TEST: Book C1",
                "chapter_number": 9003,
                "verse_number": 7,
                "verse_text": "TEST GRANDCHILD: Dense 0-2 grandchild 3.1",
                "parent_text": "TEST CHILD: Dense 0-2 child 3",
                "link_strength": 49,
            },
            {
                "book_canonical_order": 1003,
                "book_name": "TEST: Book C1",
                "chapter_number": 9003,
                "verse_number": 8,
                "verse_text": "TEST GRANDCHILD: Dense 0-2 grandchild 3.2",
                "parent_text": "TEST CHILD: Dense 0-2 child 3",
                "link_strength": 48,
            },
            {
                "book_canonical_order": 1003,
                "book_name": "TEST: Book C1",
                "chapter_number": 9003,
                "verse_number": 9,
                "verse_text": "TEST GRANDCHILD: Dense 0-2 grandchild 3.3",
                "parent_text": "TEST CHILD: Dense 0-2 child 3",
                "link_strength": 47,
            },
        ],
    },

    "TEST ROOT: Chain past depth limit (4 layers)": {
        "0": [
            {
                "book_canonical_order": 1001,
                "book_name": "TEST: Book A1",
                "chapter_number": 9001,
                "verse_number": 6,
                "verse_text": "TEST ROOT: Chain past depth limit (4 layers)",
                "parent_text": None,
                "link_strength": None,
            }
        ],
        "1": [
            {
                "book_canonical_order": 1002,
                "book_name": "TEST: Book B1",
                "chapter_number": 9002,
                "verse_number": 13,
                "verse_text": "TEST CHILD: Past-limit chain layer 1",
                "parent_text": "TEST ROOT: Chain past depth limit (4 layers)",
                "link_strength": 30,
            }
        ],
        "2": [
            {
                "book_canonical_order": 1003,
                "book_name": "TEST: Book C1",
                "chapter_number": 9003,
                "verse_number": 13,
                "verse_text": "TEST GRANDCHILD: Past-limit chain layer 2",
                "parent_text": "TEST CHILD: Past-limit chain layer 1",
                "link_strength": 20,
            }
        ],
        # No "3": the great-grandchild (book_d1) must be excluded by the depth limit.
    },
}