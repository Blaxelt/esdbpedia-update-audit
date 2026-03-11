from fastapi import APIRouter, Path, HTTPException, Query
from app.core import article_store
from app.process_files.load_bz2 import run as load_dump

router = APIRouter()


@router.post("/articles/load")
def load_articles(date: str = Query(..., pattern=r"^\d{8}$", description="Dump date in YYYYMMDD format, e.g. 20260301")):
    result = load_dump(date)
    article_store.load(date)  # Reload index into memory after new dump
    return result


@router.get("/articles/{article_id}")
def get_article(article_id: str = Path(..., title="Article ID")):
    article = article_store.get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"text": article["text"]}


@router.get("/articles/{article_id}/next")
def get_next_article(article_id: str = Path(..., title="Article ID")):
    next_id = article_store.get_next_id(article_id)
    if not next_id:
        raise HTTPException(status_code=404, detail="No next article found")
    return {"id": next_id}


@router.get("/articles/{article_id}/prev")
def get_prev_article(article_id: str = Path(..., title="Article ID")):
    prev_id = article_store.get_prev_id(article_id)
    if not prev_id:
        raise HTTPException(status_code=404, detail="No previous article found")
    return {"id": prev_id}