from typing import Any

from fastapi import Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from extensions.security import decode_token
from models import User, Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/urlencode_login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"Authorization": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user: Optional[User] = await User.find_one({"id": user_id})
    if user is None:
        raise credentials_exception
    return user


async def admin_only(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        user: Optional[User] = await User.find_one({"id": user_id})
        assert user.is_admin
        return user
    except:
        HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"Authorization": "Bearer"},
        )


def Inbody(default: Any, *args, **kwargs) -> Any:
    return Body(default, *args, embed=True, **kwargs)
