import requests


def extract_verses_in_chapter(
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


