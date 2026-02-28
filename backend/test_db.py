from sqlmodel import Session, select, cast
from sqlalchemy import Integer
from app.core.db import engine
from app.models import Page

with Session(engine) as session:
    stmt = select(Page.id).where(cast(Page.id, Integer) > cast('170000000', Integer)).order_by(cast(Page.id, Integer).asc()).limit(1)
    res = session.exec(stmt).first()
    print("Next:", res)
