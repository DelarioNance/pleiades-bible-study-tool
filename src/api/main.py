from fastapi import FastAPI
from .routers import book_router, chapter_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = FastAPI() # fastapi dev src/api/main.py 
app.include_router(book_router.router)
app.include_router(chapter_router.router)
app.mount(
    "/src/frontend/static",
    StaticFiles(directory="src/frontend/static"),
)

@app.get("/")
def read_index():
    return FileResponse("src/frontend/html/index.html")