import requests
import asyncio
import aiohttp

def extract_verses_in_chapter_sync(
    book_id: str,
    chapter: int,
    api_base_url: str = "https://bible.helloao.org/api/eng_kjv"
):
    response = requests.get(f"{api_base_url}/{book_id}/{chapter}.json")
    data = response.json()
    content_items = data['chapter']['content']
    verses_raw = [
        item for item in content_items
        if item.get("type") == "verse"
    ]

    return verses_raw


async def extract_verses_in_chapter_async(
    http_session,
    book_id: str,
    chapter: int,
    api_base_url: str = "https://bible.helloao.org/api/eng_kjv"
):
    url = f"{api_base_url}/{book_id}/{chapter}.json"

    async with http_session.get(url) as response:
        json = await response.json()    
        
    content_items = json['chapter']['content']
    chapter_verses_raw = [
        {
            "book_id": book_id,
            "chapter_number": chapter,
            "verse_number": item.get("number"),
            "content": item.get("content")
        } 
        for item in content_items
        if item.get("type") == "verse"
    ]

    return chapter_verses_raw


async def extract_all_verses_async(books_raw, api_base_url):
    async with aiohttp.ClientSession() as http_session:
        coroutines = [
            extract_verses_in_chapter_async(
                http_session, 
                book['id'], 
                chapter,
                api_base_url
            )
            for book in books_raw  
            for chapter in range(1, book['numberOfChapters'] + 1)
        ]
        verses_per_chapter_raw = await asyncio.gather(*coroutines)

    all_verses_raw = [verse for chapter_verses in verses_per_chapter_raw for verse in chapter_verses]

    return all_verses_raw


def extract_all_verses_sync(books_raw, api_base_url):
    all_verses_raw = []
    for book in books_raw:
        num_chapters = book['numberOfChapters']
        for chapter in range(1, num_chapters + 1):
            all_verses_raw.extend(extract_verses_in_chapter_sync(book['id'], chapter))

    return all_verses_raw