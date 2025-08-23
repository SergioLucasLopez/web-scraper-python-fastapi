from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.hn_scraper import scrape_first_30
from app.service import (
    filter_long_titles_sort_by_comments,
    filter_short_titles_sort_by_points,
)

app = FastAPI(title="HN Scraper")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    entries = await scrape_first_30()
    return templates.TemplateResponse(
        "index.html", {"request": request, "entries": entries, "mode": "todo"}
    )


@app.get("/filter/long", response_class=HTMLResponse)
async def long_titles(request: Request):
    entries = await scrape_first_30()
    res = filter_long_titles_sort_by_comments(entries)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "entries": res, "mode": ">5 palabras (por comentarios)"},
    )


@app.get("/filter/short", response_class=HTMLResponse)
async def short_titles(request: Request):
    entries = await scrape_first_30()
    res = filter_short_titles_sort_by_points(entries)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "entries": res, "mode": "≤5 palabras (por puntos)"},
    )


@app.get("/api/entries")
async def api_entries():
    entries = await scrape_first_30()
    return JSONResponse([e.__dict__ for e in entries])
