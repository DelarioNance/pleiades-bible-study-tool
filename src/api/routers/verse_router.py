from fastapi import APIRouter
from src.api.services.verse_service import run_bfs, find_densest_verse_id, find_sparsest_verse_id

router = APIRouter(prefix="/v1/verses")


@router.get("/{verse_id}/traversal_results")
def get_bfs_results(verse_id: int):
    return run_bfs(verse_id)


@router.get("/densest")
def get_densest_verse_id():
    return find_densest_verse_id()


@router.get("/sparsest")
def get_sparsest_verse_id():
    return find_sparsest_verse_id()