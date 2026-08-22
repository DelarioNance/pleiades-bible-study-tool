from fastapi import APIRouter
from src.api.services.chapter_service import fetch_verses_from_chapter_id

router = APIRouter(prefix="/v1/chapters")


@router.get("/{chapter_id}/verses")
def get_verses_from_chapter_id(chapter_id: int):
    return fetch_verses_from_chapter_id(chapter_id)