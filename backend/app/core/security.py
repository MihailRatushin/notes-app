"""
Хеширование паролей и работа с JWT.

Пароли храним только в виде bcrypt-хеша — восстановить исходный пароль
из хеша невозможно. Даже если БД утечёт, пароли пользователей не скомпрометированы.
"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings


def _to_bytes(password: str) -> bytes:
    """
    bcrypt работает максимум с 72 байтами пароля.
    Обрезаем лишнее, чтобы длинные пароли не приводили к ошибке.
    (На практике ни один нормальный пароль в 72 байта не упрётся.)
    """
    return password.encode("utf-8")[:72]


def hash_password(password: str) -> str:
    """Возвращает bcrypt-хеш строкой. Соль генерится автоматически."""
    return bcrypt.hashpw(_to_bytes(password), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, что plain_password соответствует сохранённому хешу."""
    try:
        return bcrypt.checkpw(_to_bytes(plain_password), hashed_password.encode("utf-8"))
    except ValueError:
        # Если хеш в БД битый — считаем, что пароль не подошёл.
        return False


def create_access_token(
    subject: int | str,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Создаёт JWT с полем sub (subject — обычно id пользователя)
    и exp (expiration — срок жизни).

    sub по стандарту JWT должен быть строкой, поэтому приводим.
    """
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    payload = {"sub": str(subject), "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict | None:
    """
    Расшифровывает токен. Возвращает payload или None,
    если токен просрочен / подпись неверна / токен испорчен.
    """
    try:
        return jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.PyJWTError:
        return None