"""
Пользователь. У одного пользователя много папок и много заметок.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Связи. cascade="all, delete-orphan" говорит: при удалении пользователя
    # SQLAlchemy сам удалит его папки и заметки (плюс на уровне БД стоит CASCADE).
    folders: Mapped[list["Folder"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    notes: Mapped[list["Note"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )