import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass

def make_engine():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is required")
    return create_engine(url, pool_pre_ping=True, pool_recycle=300)

_engine = None

def get_session():
    global _engine
    if _engine is None:
        _engine = make_engine()
    with sessionmaker(bind=_engine)() as session:
        yield session
