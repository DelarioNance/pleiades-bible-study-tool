# Standard library
import os

# Third‑party packages
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Session
import requests

# Local application imports (none in this file)


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
BIBLE_API = 'https://bible.helloao.org/api/eng_kjv'   # Replace with your actual API
PRINT_SQL_STATEMENTS = False


# ------------------------------------------------------------
# SQLAlchemy Base
# ------------------------------------------------------------
class Base(DeclarativeBase):
    pass


# ------------------------------------------------------------
# Models
# ------------------------------------------------------------
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    common_name = Column(String, nullable=False)
    canonical_order = Column(Integer, nullable=False)


class Chapter(Base):
    __tablename__ = 'chapters'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    chapter_number = Column(Integer, nullable=False)


class Verse(Base):
    __tablename__ = 'verses'

    id = Column(Integer, primary_key=True)
    chapter_id = Column(Integer, ForeignKey('chapters.id'), nullable=False)
    verse_number = Column(Integer, nullable=False)
    verbiage = Column(Text, nullable=False)


# ------------------------------------------------------------
# DB Helpers
# ------------------------------------------------------------
def reset_schemas(engine):
    Base.metadata.drop_all(engine) # drops existing tables (immediately)
    Base.metadata.create_all(engine) # creates non-existent .db file and non-existent tables


# ------------------------------------------------------------
# API Helpers
# ------------------------------------------------------------
def fetch_books():
    response = requests.get(f'{BIBLE_API}/books.json')
    books = response.json()['books']
    return books


def fetch_verses(api_book_id, api_chapter_number):
    response = requests.get(f'{BIBLE_API}/{api_book_id}/{api_chapter_number}.json')
    verses = response.json()['chapter']['content']
    return verses
   

# ------------------------------------------------------------
# Main DB Initialization
# ------------------------------------------------------------
def main():
    engine = create_engine(DATABASE_URL, echo=PRINT_SQL_STATEMENTS)
    reset_schemas(engine) # immediately recreates schemas (i.e., does not wait until script finishes)

    with Session(engine) as session:
        # Books
        books = fetch_books()
        for curr_book_api_data in books:
            book_common_name = curr_book_api_data['commonName']
            book = Book(
                common_name=book_common_name,
                canonical_order=curr_book_api_data['order']
            )
            session.add(book) # makes SQLAlchemy aware of the new book, but does not yet assign it an ID
            session.flush() # forces SQLAlchemy to assign an ID to the book so we can use it for the chapters

            print(f'   → {book.common_name}')

            # Chapters
            num_chapters = curr_book_api_data['numberOfChapters']
            for chapter_num in range(1, num_chapters + 1):
                chapter = Chapter(
                    book_id=book.id,
                    chapter_number=chapter_num
                )
                session.add(chapter)
                session.flush() # forces SQLAlchemy to assign an ID to the chapter so we can use it for the verses

                api_book_id = curr_book_api_data['id']

                print(f'   → {book.common_name} {chapter_num}')

                # Verses
                verses = fetch_verses(api_book_id, chapter_num)
                for curr_verse_api_data in verses:
                    verse = Verse(
                        chapter_id=chapter.id,
                        verse_number=curr_verse_api_data['number'],
                        verbiage=curr_verse_api_data['content'][0]
                    )
                    session.add(verse)

                    print(f'   → {book.common_name} {chapter_num}:{verse.verse_number}')

            session.commit()

        print('🎉 Bible data successfully imported!')


if __name__ == '__main__':
    main()