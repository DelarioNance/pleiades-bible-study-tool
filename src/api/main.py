from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse # informs docs of an HTML repsonse
from .routers import book_router, chapter_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


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
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "defaultBookName": default_book_name,
            "defaultChapterNumber": default_chapter_number,
            "defaultVerseNumber": default_verse_number,
            "defaultDepth": default_depth,
        }
    )