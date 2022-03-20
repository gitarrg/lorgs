"""Endpoints dealing with user authentication."""

# IMPORT STANDARD LIBARIES
import os

# IMPORT THIRD PARTY LIBARIES
from fastapi_cache.decorator import cache
import fastapi
import jwt

# IMPORT LOCAL LIBARIES
from lorgs import auth


SECRET_KEY = os.getenv("SECRET_KEY") or "my-super-secret-key"


router = fastapi.APIRouter()


@router.get("/token")
async def get_token(code: str):
    """Exchange a Authorization Code for some user info."""

    # get the discord access token
    user_credentials = await auth.exchange_code(code)
    access_token = user_credentials.get("access_token")
    if not access_token:
        return {
            "error": user_credentials.get("error"),
            "message": user_credentials.get("error_description", "")
        }

    # load user info
    profile = await auth.get_user_profile(access_token)
    permissions = await auth.get_member_permissions(profile["id"])

    # encode everything into JWT
    user_info = {
        "name": profile.get("username"),
        "id": profile.get("id"),
        "permissions": list(permissions),
    }
    token = jwt.encode(user_info, SECRET_KEY, algorithm="HS256")

    # return
    return {"token": token}


@router.get("/info/{user_id:int}")
@cache()
async def get_user_info(user_id: int):
    member_info = await auth.get_member_info(user_id)
    return member_info.get("user") or {}
