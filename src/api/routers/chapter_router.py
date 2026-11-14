from fastapi import APIRouter

import src.api.queries.verses as verse_queries

router = APIRouter(prefix="/v1/chapters")


@router.get("/{chapter_id}/verses")
def get_verses_from_chapter_id(chapter_id: int):
    return verse_queries.get_verses_from_chapter_id(chapter_id)
