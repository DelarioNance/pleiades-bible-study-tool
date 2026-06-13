from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse # informs docs of an HTML repsonse
from .routers import book_router, chapter_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.api.services.book_service import get_book_info_from_book_name
from src.api.services.chapter_service import get_chapter_info_from_book_id_and_chapter_number
from src.api.services.verse_service import get_verse_info_from_chapter_id_and_verse_number

app = FastAPI() # fastapi dev src/api/main.py 
app.include_router(book_router.router)
app.include_router(chapter_router.router)
app.mount(
    "/src/frontend/static",
    StaticFiles(directory="src/frontend/static"),
)

templates = Jinja2Templates(directory='src/frontend/templates')


@app.get("/", response_class=HTMLResponse) 
def read_index(
    request:Request,
    default_book_name: str = 'John',
    default_chapter_number: int = 3,
    default_verse_number: int = 16,
    default_depth: int = 2,
):
    """
    Examples:
    http://127.0.0.1:8000/
    http://127.0.0.1:8000/?default_book_name=Genesis
    http://127.0.0.1:8000/?default_book_name=Genesis&default_chapter_number=1
    http://127.0.0.1:8000/?default_book_name=Genesis&default_chapter_number=1&default_verse_number=5
    """
    default_book_id = get_book_info_from_book_name(default_book_name)['id']
    default_chapter_id = get_chapter_info_from_book_id_and_chapter_number(default_book_id, default_chapter_number)['id']
    default_verse_id = get_verse_info_from_chapter_id_and_verse_number(default_chapter_id, default_verse_number)['id']

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "defaultBookID": default_book_id,
            "defaultBookName": default_book_name,
            "defaultChapterID": default_chapter_id,
            "defaultChapterNumber": default_chapter_number,
            "defaultVerseID": default_verse_id,
            "defaultDepth": default_depth,
        }
    )