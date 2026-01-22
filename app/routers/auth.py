from fastapi import APIRouter, Header, HTTPException
from auth.entra.validator import validate_entra_token, EntraTokenError

router = APIRouter()

@router.post("/auth/bootstrap")
def bootstrap(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = authorization.split(" ", 1)[1]

    try:
        entra_identity = validate_entra_token(token)
    except EntraTokenError:
        raise HTTPException(status_code=401, detail="Invalid Entra token")

    # TEMP RESPONSE FOR TESTING
    return entra_identity
