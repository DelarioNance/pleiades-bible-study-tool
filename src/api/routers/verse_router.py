from fastapi import APIRouter
from src.api.services.verse_service import run_bfs, fetch_verses_from_text

router = APIRouter(prefix="/v1/verses")


@router.get("/{verse_id}/traversal_results")
def get_bfs_results(verse_id: int):
    return run_bfs(verse_id)


@router.get("/search")
def search(text: str):
    return fetch_verses_from_text(verse_text=text)