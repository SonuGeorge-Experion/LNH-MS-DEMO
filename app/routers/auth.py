from fastapi import Depends, APIRouter, Header, HTTPException
from app.auth.entra.validator import validate_entra_token, EntraTokenError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=True)


router = APIRouter()

@router.post("/bootstrap")
def bootstrap(
    creds: HTTPAuthorizationCredentials = Depends(security)
    ):
    token = creds.credentials

    try:
        entra_identity = validate_entra_token(token)
    except EntraTokenError:
        raise HTTPException(status_code=401, detail="Invalid Entra token")

    # TEMP RESPONSE FOR TESTING
    return entra_identity
