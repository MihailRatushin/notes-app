"""
Зависимости FastAPI, которые переиспользуются в роутерах.

get_current_user — главная. Она превращает HTTP-запрос
с заголовком Authorization: Bearer <токен> в объект User из БД.

Если токена нет / он невалиден / пользователя нет — возвращается 401.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import get_db
from app.models import User

# tokenUrl — адрес, куда Swagger UI будет отправлять форму логина.
# Полный путь: /api/auth/login (см. include_router в main.py).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.get(User, int(user_id))
    if user is None:
        raise credentials_exception

    return user