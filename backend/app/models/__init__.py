"""
Все модели должны быть импортированы здесь.
Alembic смотрит на Base.metadata, а модели попадают в неё
только после импорта их Python-модулей.
"""

from app.models.folder import Folder
from app.models.note import Note
from app.models.user import User

__all__ = ["User", "Folder", "Note"]