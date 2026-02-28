from fastapi import APIRouter, Path
from app.api.deps import SessionDep
from app.models import Page, PageDetail

router = APIRouter()

@router.get("/articles/{article_id}", response_model=PageDetail)
def get_article(session: SessionDep, article_id: str = Path(..., title="Article ID")):
    article = session.get(Page, article_id)
    return PageDetail(text=article.text)