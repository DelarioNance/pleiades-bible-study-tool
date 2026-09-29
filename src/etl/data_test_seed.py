TEST_BOOKS = [
    {"book_id": "book_a1", "common_name": "TEST: Book A1", "canonical_order": 1001},
    {"book_id": "book_b1", "common_name": "TEST: Book B1", "canonical_order": 1002},
    {"book_id": "book_c1", "common_name": "TEST: Book C1", "canonical_order": 1003},
]

# One chapter per test book. (book_id, chapter_number) pairs are unique.
TEST_CHAPTERS = [
    {"chapter_id": "chapter_a1", "book_id": "book_a1", "chapter_number": 9001},
    {"chapter_id": "chapter_b1", "book_id": "book_b1", "chapter_number": 9002},
    {"chapter_id": "chapter_c1", "book_id": "book_c1", "chapter_number": 9003},
]

# verse_number is assigned in list order per chapter by the loader.
TEST_VERSES = [
    # --- Layer 0: roots (book_a1) ---
    {"verse_id": "no_children_root",      "book_id": "book_a1", "chapter_number": 9001, "verse_number": 1, "verse_text": "TEST ROOT: No children"},
    {"verse_id": "dense_layers_0_2_root", "book_id": "book_a1", "chapter_number": 9001, "verse_number": 2, "verse_text": "TEST ROOT: Dense at layers 0-2"},
    {"verse_id": "dense_layers_0_1_root", "book_id": "book_a1", "chapter_number": 9001, "verse_number": 3, "verse_text": "TEST ROOT: Dense at layers 0-1; sparse as layer 2"},
    {"verse_id": "one_child_root",        "book_id": "book_a1", "chapter_number": 9001, "verse_number": 4, "verse_text": "TEST ROOT: 1 child"},
    {"verse_id": "middle_child_root",     "book_id": "book_a1", "chapter_number": 9001, "verse_number": 5, "verse_text": "TEST ROOT: 3 children, middle has children"},

    # --- Layer 1: children (book_b1) ---
    {"verse_id": "dense_layers_0_2_child_1", "book_id": "book_b1", "chapter_number": 9002, "verse_number": 1,  "verse_text": "TEST: Dense 0-2 child 1"},
    {"verse_id": "dense_layers_0_2_child_2", "book_id": "book_b1", "chapter_number": 9002, "verse_number": 2,  "verse_text": "TEST: Dense 0-2 child 2"},
    {"verse_id": "dense_layers_0_2_child_3", "book_id": "book_b1", "chapter_number": 9002, "verse_number": 3,  "verse_text": "TEST: Dense 0-2 child 3"},
    {"verse_id": "dense_layers_0_2_child_4", "book_id": "book_b1", "chapter_number": 9002, "verse_number": 4,  "verse_text": "TEST: Dense 0-2 child 4"},
    {"verse_id": "dense_layers_0_2_child_5", "book_id": "book_b1", "chapter_number": 9002, "verse_number": 5,  "verse_text": "TEST: Dense 0-2 child 5"},
    {"verse_id": "dense_layers_0_1_child_1", "book_id": "book_b1", "chapter_number": 9002, "verse_number": 6,  "verse_text": "TEST: Dense 0-1 child 1"},
    {"verse_id": "dense_layers_0_1_child_2", "book_id": "book_b1", "chapter_number": 9002, "verse_number": 7,  "verse_text": "TEST: Dense 0-1 child 2"},
    {"verse_id": "dense_layers_0_1_child_3", "book_id": "book_b1", "chapter_number": 9002, "verse_number": 8,  "verse_text": "TEST: Dense 0-1 child 3"},
    {"verse_id": "one_child_child_1",        "book_id": "book_b1", "chapter_number": 9002, "verse_number": 9,  "verse_text": "TEST: 1 child - the child"},
    {"verse_id": "middle_child_child_1",     "book_id": "book_b1", "chapter_number": 9002, "verse_number": 10, "verse_text": "TEST: Middle-child scenario child 1"},
    {"verse_id": "middle_child_child_2",     "book_id": "book_b1", "chapter_number": 9002, "verse_number": 11, "verse_text": "TEST: Middle-child scenario child 2"},
    {"verse_id": "middle_child_child_3",     "book_id": "book_b1", "chapter_number": 9002, "verse_number": 12, "verse_text": "TEST: Middle-child scenario child 3"},

    # --- Layer 2: grandchildren (book_c1) ---
    {"verse_id": "dense_layers_0_2_child_1_grandchild_1", "book_id": "book_c1", "chapter_number": 9003, "verse_number": 1,  "verse_text": "TEST: Dense 0-2 grandchild 1.1"},
    {"verse_id": "dense_layers_0_2_child_1_grandchild_2", "book_id": "book_c1", "chapter_number": 9003, "verse_number": 2,  "verse_text": "TEST: Dense 0-2 grandchild 1.2"},
    {"verse_id": "dense_layers_0_2_child_1_grandchild_3", "book_id": "book_c1", "chapter_number": 9003, "verse_number": 3,  "verse_text": "TEST: Dense 0-2 grandchild 1.3"},
    {"verse_id": "dense_layers_0_2_child_2_grandchild_1", "book_id": "book_c1", "chapter_number": 9003, "verse_number": 4,  "verse_text": "TEST: Dense 0-2 grandchild 2.1"},
    {"verse_id": "dense_layers_0_2_child_2_grandchild_2", "book_id": "book_c1", "chapter_number": 9003, "verse_number": 5,  "verse_text": "TEST: Dense 0-2 grandchild 2.2"},
    {"verse_id": "dense_layers_0_2_child_2_grandchild_3", "book_id": "book_c1", "chapter_number": 9003, "verse_number": 6,  "verse_text": "TEST: Dense 0-2 grandchild 2.3"},
    {"verse_id": "dense_layers_0_2_child_3_grandchild_1", "book_id": "book_c1", "chapter_number": 9003, "verse_number": 7,  "verse_text": "TEST: Dense 0-2 grandchild 3.1"},
    {"verse_id": "dense_layers_0_2_child_3_grandchild_2", "book_id": "book_c1", "chapter_number": 9003, "verse_number": 8,  "verse_text": "TEST: Dense 0-2 grandchild 3.2"},
    {"verse_id": "dense_layers_0_2_child_3_grandchild_3", "book_id": "book_c1", "chapter_number": 9003, "verse_number": 9,  "verse_text": "TEST: Dense 0-2 grandchild 3.3"},
    {"verse_id": "middle_child_child_2_grandchild_1",     "book_id": "book_c1", "chapter_number": 9003, "verse_number": 10, "verse_text": "TEST: Middle-child scenario grandchild 1"},
    {"verse_id": "middle_child_child_2_grandchild_2",     "book_id": "book_c1", "chapter_number": 9003, "verse_number": 11, "verse_text": "TEST: Middle-child scenario grandchild 2"},
    {"verse_id": "middle_child_child_2_grandchild_3",     "book_id": "book_c1", "chapter_number": 9003, "verse_number": 12, "verse_text": "TEST: Middle-child scenario grandchild 3"},
]


TEST_VERSE_REFERENCES = [
    # --- dense_layers_0_2: top 3 children (votes 100/90/80) each have 3 children;
    #     children 4 and 5 are lower-vote extras with no children ---
    # root -> children
    {"from_book_id": "book_a1", "from_chapter_number": 9001, "from_verse_number": 2, "to_book_id": "book_b1", "to_chapter_number": 9002, "to_verse_number": 1, "num_votes": 100},  # dense_layers_0_2_root -> child_1
    {"from_book_id": "book_a1", "from_chapter_number": 9001, "from_verse_number": 2, "to_book_id": "book_b1", "to_chapter_number": 9002, "to_verse_number": 2, "num_votes": 90},   # -> child_2
    {"from_book_id": "book_a1", "from_chapter_number": 9001, "from_verse_number": 2, "to_book_id": "book_b1", "to_chapter_number": 9002, "to_verse_number": 3, "num_votes": 80},   # -> child_3
    {"from_book_id": "book_a1", "from_chapter_number": 9001, "from_verse_number": 2, "to_book_id": "book_b1", "to_chapter_number": 9002, "to_verse_number": 4, "num_votes": 10},   # -> child_4
    {"from_book_id": "book_a1", "from_chapter_number": 9001, "from_verse_number": 2, "to_book_id": "book_b1", "to_chapter_number": 9002, "to_verse_number": 5, "num_votes": 5},    # -> child_5
    # child_1 -> grandchildren 1.1-1.3
    {"from_book_id": "book_b1", "from_chapter_number": 9002, "from_verse_number": 1, "to_book_id": "book_c1", "to_chapter_number": 9003, "to_verse_number": 1, "num_votes": 49},
    {"from_book_id": "book_b1", "from_chapter_number": 9002, "from_verse_number": 1, "to_book_id": "book_c1", "to_chapter_number": 9003, "to_verse_number": 2, "num_votes": 48},
    {"from_book_id": "book_b1", "from_chapter_number": 9002, "from_verse_number": 1, "to_book_id": "book_c1", "to_chapter_number": 9003, "to_verse_number": 3, "num_votes": 47},
    # child_2 -> grandchildren 2.1-2.3
    {"from_book_id": "book_b1", "from_chapter_number": 9002, "from_verse_number": 2, "to_book_id": "book_c1", "to_chapter_number": 9003, "to_verse_number": 4, "num_votes": 49},
    {"from_book_id": "book_b1", "from_chapter_number": 9002, "from_verse_number": 2, "to_book_id": "book_c1", "to_chapter_number": 9003, "to_verse_number": 5, "num_votes": 48},
    {"from_book_id": "book_b1", "from_chapter_number": 9002, "from_verse_number": 2, "to_book_id": "book_c1", "to_chapter_number": 9003, "to_verse_number": 6, "num_votes": 47},
    # child_3 -> grandchildren 3.1-3.3
    {"from_book_id": "book_b1", "from_chapter_number": 9002, "from_verse_number": 3, "to_book_id": "book_c1", "to_chapter_number": 9003, "to_verse_number": 7, "num_votes": 49},
    {"from_book_id": "book_b1", "from_chapter_number": 9002, "from_verse_number": 3, "to_book_id": "book_c1", "to_chapter_number": 9003, "to_verse_number": 8, "num_votes": 48},
    {"from_book_id": "book_b1", "from_chapter_number": 9002, "from_verse_number": 3, "to_book_id": "book_c1", "to_chapter_number": 9003, "to_verse_number": 9, "num_votes": 47},

    # --- dense_layers_0_1: 3 children, no grandchildren ---
    {"from_book_id": "book_a1", "from_chapter_number": 9001, "from_verse_number": 3, "to_book_id": "book_b1", "to_chapter_number": 9002, "to_verse_number": 6, "num_votes": 30},  # dense_layers_0_1_root -> child_1
    {"from_book_id": "book_a1", "from_chapter_number": 9001, "from_verse_number": 3, "to_book_id": "book_b1", "to_chapter_number": 9002, "to_verse_number": 7, "num_votes": 20},  # -> child_2
    {"from_book_id": "book_a1", "from_chapter_number": 9001, "from_verse_number": 3, "to_book_id": "book_b1", "to_chapter_number": 9002, "to_verse_number": 8, "num_votes": 10},  # -> child_3

    # --- one_child: exactly one child ---
    {"from_book_id": "book_a1", "from_chapter_number": 9001, "from_verse_number": 4, "to_book_id": "book_b1", "to_chapter_number": 9002, "to_verse_number": 9, "num_votes": 7},   # one_child_root -> one_child_child_1

    # --- middle_child: votes 30 > 20 > 10; only the 20-vote (middle) child has children ---
    {"from_book_id": "book_a1", "from_chapter_number": 9001, "from_verse_number": 5, "to_book_id": "book_b1", "to_chapter_number": 9002, "to_verse_number": 10, "num_votes": 30},  # middle_child_root -> child_1
    {"from_book_id": "book_a1", "from_chapter_number": 9001, "from_verse_number": 5, "to_book_id": "book_b1", "to_chapter_number": 9002, "to_verse_number": 11, "num_votes": 20},  # -> child_2
    {"from_book_id": "book_a1", "from_chapter_number": 9001, "from_verse_number": 5, "to_book_id": "book_b1", "to_chapter_number": 9002, "to_verse_number": 12, "num_votes": 10},  # -> child_3
    # middle_child_child_2 -> grandchildren
    {"from_book_id": "book_b1", "from_chapter_number": 9002, "from_verse_number": 11, "to_book_id": "book_c1", "to_chapter_number": 9003, "to_verse_number": 10, "num_votes": 14},
    {"from_book_id": "book_b1", "from_chapter_number": 9002, "from_verse_number": 11, "to_book_id": "book_c1", "to_chapter_number": 9003, "to_verse_number": 11, "num_votes": 13},
    {"from_book_id": "book_b1", "from_chapter_number": 9002, "from_verse_number": 11, "to_book_id": "book_c1", "to_chapter_number": 9003, "to_verse_number": 12, "num_votes": 12},
]