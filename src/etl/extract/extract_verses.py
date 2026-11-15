import asyncio

import aiohttp


async def extract_verses_in_chapter_async(
    http_session, book_id: str, chapter: int, api_base_url: str
):
    url = f"{api_base_url}/{book_id}/{chapter}.json"

    async with http_session.get(url) as response:
        json = await response.json()

    content_items = json["chapter"]["content"]
    verses_raw = [
        {
            "book_id": book_id,
            "chapter_number": chapter,
            "verse_number": item.get("number"),
            "content": item.get("content"),
        }
        for item in content_items
        if item.get("type") == "verse"
    ]

    return verses_raw


async def extract_verses_async(books_raw, api_base_url):
    async with aiohttp.ClientSession() as http_session:
        coroutines = [
            extract_verses_in_chapter_async(
                http_session, book["id"], chapter, api_base_url
            )
            for book in books_raw
            for chapter in range(1, book["numberOfChapters"] + 1)
        ]
        verses_per_chapter_raw = await asyncio.gather(*coroutines)

    verses_raw = [
        verse for chapter_verses in verses_per_chapter_raw for verse in chapter_verses
    ]

    return verses_raw
