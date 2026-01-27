from fastapi import Depends, HTTPException
from app.core.deps import get_current_user


def require_roles(*allowed_roles: str):
    def checker(user = Depends(get_current_user)):
        if not set(user["roles"]).intersection(allowed_roles):
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker