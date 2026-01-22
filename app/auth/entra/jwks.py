import httpx
from functools import lru_cache
from app.core.config import settings

@lru_cache(maxsize=1)
def get_jwks():
    response = httpx.get(settings.ENTRA_JWKS_URL, timeout=5)
    response.raise_for_status()
    return response.json()
