"""
Заметка. Принадлежит пользователю, может лежать в папке (или без неё).
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False, default="")

    # server_default — значение по умолчанию на стороне PostgreSQL (NOW()).
    # onupdate — SQLAlchemy сам подставит NOW() при каждом UPDATE строки.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # folder_id может быть NULL — заметка без папки.
    # ondelete="SET NULL" — если папку удалили, заметка не удаляется.
    folder_id: Mapped[int | None] = mapped_column(
        ForeignKey("folders.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    folder: Mapped["Folder | None"] = relationship(back_populates="notes")
    user: Mapped["User"] = relationship(back_populates="notes")