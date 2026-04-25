"""
Extracts raw book metadata from a user-specified API.

This module performs the **Extract** phase for Bible book data. It retrieves
the canonical list of KJV books directly from the API and returns a dictionary
keyed by the API's stable book identifiers.

No transformation or database interaction occurs here. The caller (typically
the ETL orchestrator) is responsible for:

- providing the API base URL
- invoking the Transform phase on the returned data
- passing transformed data into the Load phase
"""

import requests


def extract_books(
    api_base_url: str = "https://bible.helloao.org/api/eng_kjv"
):
    response = requests.get(f"{api_base_url}/books.json")
    books_raw = response.json()['books']

    return books_raw


