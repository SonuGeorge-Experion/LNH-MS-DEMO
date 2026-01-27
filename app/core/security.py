from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(
        seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload["type"] = "access"

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def create_refresh_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=3)
    payload["type"] = "refresh"

    return jwt.encode(
        payload,
        settings.REFRESH_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
