from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.auth.entra.validator import validate_entra_token, EntraTokenError
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.schemas.auth import TokenResponse

security = HTTPBearer(auto_error=True)
router = APIRouter()


@router.post("/bootstrap", response_model=TokenResponse)
def bootstrap(
    creds: HTTPAuthorizationCredentials = Depends(security),
):
    entra_token = creds.credentials
    try:
        entra_identity = validate_entra_token(entra_token)
        print(entra_identity)
    except EntraTokenError:
        raise HTTPException(status_code=401, detail="Invalid Entra token")

    access_payload = {
        "sub": entra_identity["entra_oid"],
        "user_name": entra_identity["user_name"],
        "roles": entra_identity["entra_roles"],
    }

    access_token = create_access_token(access_payload)
    refresh_token = create_refresh_token(
        {"sub": entra_identity["entra_oid"],
        "user_name": entra_identity["user_name"],
        "roles": entra_identity["entra_roles"],}
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    creds: HTTPAuthorizationCredentials = Depends(security),
):
    token = creds.credentials

    try:
        payload = jwt.decode(
            token,
            settings.REFRESH_SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        print(payload)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    payload = {
        "sub": payload["sub"],
        "user_name": payload["user_name"],
        "roles": payload["roles"]
    }

    return TokenResponse(
        access_token=create_access_token(payload),
        refresh_token=token,
    )
