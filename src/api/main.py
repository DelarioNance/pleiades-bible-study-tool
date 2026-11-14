from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.api.queries.books import get_book_from_book_name
from src.api.queries.chapters import (
    get_chapter_from_book_id_and_chapter_number,
)
from src.api.queries.verses import (
    get_verse_from_chapter_id_and_verse_number,
)

from .routers import book_router, chapter_router, verse_router

_UI_SRC_PATH = "src/ui"
UI_STATIC_PATH = f"{_UI_SRC_PATH}/static"
UI_TEMPLATES_PATH = _UI_SRC_PATH  # index.html is in the root of the UI dir since it's the only template we have for now

app = FastAPI()  # fastapi dev src/api/main.py
app.include_router(book_router.router)
app.include_router(chapter_router.router)
app.include_router(verse_router.router)
app.mount(
    f"/{UI_STATIC_PATH}",
    StaticFiles(directory=UI_STATIC_PATH),
)

templates = Jinja2Templates(directory=UI_TEMPLATES_PATH)


@app.get("/", response_class=HTMLResponse)
def read_index(
    request: Request,
    default_book_name: str = "Job",
    default_chapter_number: int = 38,
    default_verse_number: int = 31,
    default_depth: int = 3,  # depth is currently not supported
):
    # The default scripture is arbitrary
    default_book_id = get_book_from_book_name(default_book_name)["book_id"]
    default_chapter_id = get_chapter_from_book_id_and_chapter_number(
        default_book_id, default_chapter_number
    )["chapter_id"]
    default_verse_id = get_verse_from_chapter_id_and_verse_number(
        default_chapter_id, default_verse_number
    )["verse_id"]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "defaultBookID": default_book_id,
            "defaultBookName": default_book_name,
            "defaultChapterID": default_chapter_id,
            "defaultChapterNumber": default_chapter_number,
            "defaultVerseID": default_verse_id,
            "defaultVerseNumber": default_verse_number,
            "defaultDepth": default_depth,
        },
    )
