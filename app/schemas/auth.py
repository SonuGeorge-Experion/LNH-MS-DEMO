from pydantic import BaseModel
from typing import List

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class AccessTokenPayload(BaseModel):
    sub: str
    email: str
    roles: List[str]
