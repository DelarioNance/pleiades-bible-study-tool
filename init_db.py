# init_db.py

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Session
import os
import requests

PRINT_SQL_STATEMENTS = False
DATABASE_URL = 'sqlite:///pleiades.db'
BIBLE_API = 'https://bible.helloao.org/api/eng_kjv'   # Replace with your actual API


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
    Base.metadata.drop_all(engine) # drops existing tables
    Base.metadata.create_all(engine) # creates non-existent .db file and non-existent tables

    with Session(engine) as session:
        # Books
        books = fetch_books()
        for curr_book_api_data in books:
            book_common_name = curr_book_api_data['commonName']
            book = Book(
                common_name=book_common_name,
                canonical_order=curr_book_api_data['order']
            )
            session.add(book) # add let's SQLAlchemy know to keep track of this new book object
            session.commit()

            print(f'   → {book.common_name}')

            # Chapters
            num_chapters = curr_book_api_data['numberOfChapters']
            for chapter_num in range(1, num_chapters + 1):
                chapter = Chapter(
                    book_id=book.id,
                    chapter_number=chapter_num
                )
                session.add(chapter)
                session.commit()

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
                    session.commit()

                    print(f'   → {book.common_name} {chapter_num}:{verse.verse_number}')

        print('🎉 Bible data successfully imported!')


if __name__ == '__main__':
    main()