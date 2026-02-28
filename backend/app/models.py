from sqlmodel import SQLModel, Field

class Page(SQLModel, table=True):
    """Page model"""
    __tablename__ = "pages"

    id: str = Field(default=None, primary_key=True)
    title: str
    text: str
    status: str

class PageDetail(SQLModel):
    """Page detail model"""
    text: str