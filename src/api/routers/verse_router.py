from fastapi import APIRouter
from src.api.services.verse_service import run_bfs

router = APIRouter(prefix="/v1/verses")


@router.get("/{verse_id}/traversal_results")
def get_bfs_results(verse_id: int):
    return run_bfs(verse_id)