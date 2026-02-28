from sqlmodel import Session, create_engine

DATABASE_URL = "postgresql+psycopg://tfm:tfm@localhost:5432/articles"

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session