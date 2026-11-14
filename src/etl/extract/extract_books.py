import requests


def extract_books(api_base_url):
    response = requests.get(f"{api_base_url}/books.json")
    books_raw = response.json()["books"]

    return books_raw
