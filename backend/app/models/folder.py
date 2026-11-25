"""
Папка. Принадлежит одному пользователю, содержит много заметок.
"""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Folder(Base):
    __tablename__ = "folders"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user: Mapped["User"] = relationship(back_populates="folders")

    # ВАЖНО: здесь НЕ ставим delete-orphan — при удалении папки
    # заметки должны остаться, у них просто folder_id станет NULL.
    notes: Mapped[list["Note"]] = relationship(back_populates="folder")