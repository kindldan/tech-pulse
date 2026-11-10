from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from parser import collect_all
import asyncio

app = FastAPI(title="Tech Pulse")
templates = Jinja2Templates(directory="templates")

# Простой кэш на 5 минут
_cache = {"data": None, "ts": 0}

async def get_data(force=False):
    import time
    now = time.time()
    if force or not _cache["data"] or now - _cache["ts"] > 300:
        _cache["data"] = await collect_all()
        _cache["ts"] = now
    return _cache["data"]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    data = await get_data()
    return templates.TemplateResponse("index.html", {"request": request, "data": data})


@app.get("/api/refresh")
async def refresh():
    data = await get_data(force=True)
    return data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)