from fastapi import APIRouter, Path, HTTPException
from sqlmodel import select, cast
from sqlalchemy import Integer
from app.api.deps import SessionDep
from app.models import Page, PageDetail

router = APIRouter()

@router.get("/articles/{article_id}", response_model=PageDetail)
def get_article(session: SessionDep, article_id: str = Path(..., title="Article ID")):
    article = session.get(Page, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return PageDetail(text=article.text)

@router.get("/articles/{article_id}/next")
def get_next_article(session: SessionDep, article_id: str = Path(..., title="Article ID")):
    stmt = select(Page.id).where(cast(Page.id, Integer) > cast(article_id, Integer)).order_by(cast(Page.id, Integer).asc()).limit(1)
    next_id = session.exec(stmt).first()
    if not next_id:
        raise HTTPException(status_code=404, detail="No next article found")
    return {"id": next_id}

@router.get("/articles/{article_id}/prev")
def get_prev_article(session: SessionDep, article_id: str = Path(..., title="Article ID")):
    stmt = select(Page.id).where(cast(Page.id, Integer) < cast(article_id, Integer)).order_by(cast(Page.id, Integer).desc()).limit(1)
    prev_id = session.exec(stmt).first()
    if not prev_id:
        raise HTTPException(status_code=404, detail="No previous article found")
    return {"id": prev_id}