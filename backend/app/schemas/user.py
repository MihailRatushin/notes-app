"""
Pydantic-схемы для пользователя.

Pydantic-схема — это «описание» JSON, который приходит/уходит через API.
Модель SQLAlchemy (app/models) — это таблица в БД.
Не путай: UserRead ≠ User. Пользователь из БД не отдаётся наружу целиком
(там hashed_password), наружу уходит UserRead.
"""

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    """Что приходит на /register."""

    # 3–50 символов, только буквы/цифры/подчёркивание.
    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    # 6–100 символов. В реальных проектах требуют сложнее, для учёбы хватит.
    password: str = Field(min_length=6, max_length=100)


class UserRead(BaseModel):
    """Что уходит наружу. Пароля здесь нет — и не должно быть."""

    id: int
    username: str

    # from_attributes=True разрешает Pydantic читать атрибуты
    # прямо из ORM-объекта (User), а не только из dict.
    model_config = ConfigDict(from_attributes=True)