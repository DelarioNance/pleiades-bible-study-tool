books = """
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    common_name VARCHAR(100) NOT NULL,
    canonical_order INT NOT NULL
);
"""

chapters = """
CREATE TABLE chapters (
    id SERIAL PRIMARY KEY,
    book_id INT NOT NULL,
    chapter_number INT NOT NULL,

    CONSTRAINT fk_chapters_books
        FOREIGN KEY (book_id)
        REFERENCES books (id)
);
"""

verses = """
CREATE TABLE verses (
    id SERIAL PRIMARY KEY,
    chapter_id INT NOT NULL,
    verse_number INT NOT NULL,
    verse_text VARCHAR(500) NOT NULL,

    CONSTRAINT fk_verses_chapters
        FOREIGN KEY (chapter_id)
        REFERENCES chapters (id)
);
"""

verse_references = """
CREATE TABLE verse_references (
    id SERIAL PRIMARY KEY,
    from_id INT NOT NULL,
    to_id INT NOT NULL,

    CONSTRAINT fk_verse_references_from
        FOREIGN KEY (from_id)
        REFERENCES verses (id),

    CONSTRAINT fk_verse_references_to
        FOREIGN KEY (to_id)
        REFERENCES verses (id)
);
"""