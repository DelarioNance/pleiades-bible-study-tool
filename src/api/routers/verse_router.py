from fastapi import APIRouter

import src.api.queries.graph_traversals as graph_traversal_queries
import src.api.queries.verses as verse_queries

router = APIRouter(prefix="/v1/verses")


@router.get("/{verse_id}/traversal_results")
def get_bfs_results(verse_id: int):
    return graph_traversal_queries.run_bfs(verse_id)


@router.get("/search")
def search(text: str):
    return verse_queries.get_verses_from_verse_text(verse_text=text)
