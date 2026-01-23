from jose import jwt, JWTError
from app.auth.entra.jwks import get_jwks
from app.core.config import settings

class EntraTokenError(Exception):
    pass

def validate_entra_token(token: str) -> dict:
    try:
        jwks = get_jwks()
        header = jwt.get_unverified_header(token)
        kid = header["kid"]

        key = next(k for k in jwks["keys"] if k["kid"] == kid)
        # print(key)
        claims = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=settings.ENTRA_AUDIENCE,
            issuer=settings.ENTRA_ISSUER,
        )

    except StopIteration:
        raise EntraTokenError("Signing key not found")
    except JWTError as e:
        raise EntraTokenError(str(e))

    # REQUIRED CLAIMS
    for claim in ("oid", "tid"):
        if claim not in claims:
            raise EntraTokenError(f"Missing claim: {claim}")
    print("hi")
    print(claims)

    return {
        "entra_oid": claims["oid"],
        "entra_tid": claims["tid"],
        "entra_aud": claims["aud"],
        "entra_scp": claims["scp"],
        "email": claims.get("preferred_username") or claims.get("upn"),
    }
