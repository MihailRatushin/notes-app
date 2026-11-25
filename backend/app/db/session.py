"""
Подключение к PostgreSQL и фабрика сессий.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url, echo=False)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    """Зависимость FastAPI: открывает сессию на запрос и закрывает её после."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()