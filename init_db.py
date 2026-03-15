# ------------------------------------------------------------
# Standard library
# ------------------------------------------------------------
import os

# ------------------------------------------------------------
# Third‑party packages
# ------------------------------------------------------------
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine, Column, Integer, String, 
    ForeignKey, Text, insert
)
from sqlalchemy.orm import DeclarativeBase, Session
import requests
import asyncio # essentially an async version of requests
import aiohttp

# ------------------------------------------------------------
# Global Constants
# ------------------------------------------------------------

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
BIBLE_API = 'https://bible.helloao.org/api/eng_kjv'
PRINT_SQL_STATEMENTS = False
LOG_MODE = False


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
# General Helpers
# ------------------------------------------------------------
def log(message):
    if LOG_MODE:
        print(message)


def extract_verbiage(content_list):
    # typical case
    if isinstance(content_list[0], str):
        return content_list[0]
    
    # edge case (https://bible.helloao.org/api/eng_kjv/PSA/3.json) (https://bible.helloao.org/api/eng_kjv/MAT/6.json)
    if isinstance(content_list[0], dict): 
        for content_dict in content_list:
            if 'text' in content_dict:
                return content_dict['text']


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
    return response.json()['books']


async def fetch_verses(http_session, api_book_id, api_chapter_number):
    verses_url = f'{BIBLE_API}/{api_book_id}/{api_chapter_number}.json'
    async with http_session.get(verses_url) as response:
        json = await response.json()
        return json['chapter']['content']


# ------------------------------------------------------------
# Main DB Initialization
# ------------------------------------------------------------
async def main():
    engine = create_engine(DATABASE_URL, echo=PRINT_SQL_STATEMENTS)
    reset_schemas(engine)

    with Session(engine) as session:
        books = fetch_books()
        log(f"Fetched {len(books)} books")

        for book_metadata in books:
            book_common_name = book_metadata['commonName']

            # if book_common_name == 'Psalms':
            #     continue

            log("\n==============================")
            log(f"Processing book: {book_common_name}")
            log("==============================")

            book = Book(
                common_name=book_common_name,
                canonical_order=book_metadata['order']
            )
            session.add(book) # makes SQLAlchemy aware of the book object
            session.flush() # assigns ID primary key to the book object
            log(f"→ Inserted Book: {book.common_name} (id={book.id})")

            api_book_id = book_metadata['id']
            num_chapters = book_metadata['numberOfChapters']
            log(f"Book has {num_chapters} chapters")

            log("→ Fetching verses lists concurrently...")
            
            async with aiohttp.ClientSession() as http_session:
                verse_coroutines = [
                    fetch_verses(http_session, api_book_id, chapter_num)
                    for chapter_num in range(1, num_chapters + 1) # order will be used later to match verses to the correct chapter IDs when inserting into DB
                ]
            
            verse_lists = await asyncio.gather(*verse_coroutines) # [[verse, verse, verse], [verse, verse], ...]
            log(f"✓ Received verse_lists!")
            
            log(f"→ Inserting {num_chapters} chapters into DB...")
            chapter_insert_result = session.execute(
                insert(Chapter).returning(
                    Chapter.id
                    , Chapter.chapter_number
                ),
                [
                    {
                        'book_id': book.id,
                        'chapter_number': chapter_num,
                    } 
                    for chapter_num in range(1, num_chapters + 1)
                ]
            )

            inserted_chapters = chapter_insert_result.fetchall()
            log("✓ Inserted chapters!")

            
            log(f"→ Inserting verses into DB...")
            for chapter_id, chapter_num in inserted_chapters: # constructing insertion data with loops for easier debugging
                verse_insertion_data = []
                for verse_metadata in verse_lists[chapter_num-1]: # assumes that verse_lists are in the same order as chapter numbers, which should be true since we generated them in that order
                    log(f'{chapter_id}, {chapter_num}, {verse_metadata}')
                    if verse_metadata['type'] != 'verse':
                        continue # skips headers and other non-verse content
                    verse_number = verse_metadata['number']
                    verbiage = extract_verbiage(verse_metadata['content'])
                    verse_insertion_data.append({
                        'chapter_id': chapter_id,
                        'verse_number': verse_number,
                        'verbiage': verbiage,
                    })
                session.execute(
                    insert(Verse),
                    verse_insertion_data
                )
            log("✓ Inserted verses!")
    
            session.commit()

        log('🎉 Bible data successfully imported!')

if __name__ == '__main__':
    asyncio.run(main())