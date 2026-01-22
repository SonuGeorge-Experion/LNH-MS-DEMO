from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.entra.validator import validate_entra_token, EntraTokenError
from app.core.security import create_access_token, create_refresh_token
from app.schemas.auth import TokenResponse

security = HTTPBearer(auto_error=True)
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/bootstrap", response_model=TokenResponse)
def bootstrap(
    creds: HTTPAuthorizationCredentials = Depends(security),
):
    entra_token = creds.credentials

    try:
        entra_identity = validate_entra_token(entra_token)
    except EntraTokenError:
        raise HTTPException(status_code=401, detail="Invalid Entra token")

    # 🔐 Roles — TEMP
    # Later you can fetch from DB or another service
    roles = ["USER"]

    access_payload = {
        "sub": entra_identity["entra_oid"],
        "email": entra_identity["email"],
        "roles": roles,
    }

    access_token = create_access_token(access_payload)
    refresh_token = create_refresh_token(
        {"sub": entra_identity["entra_oid"]}
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )
