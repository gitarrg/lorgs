"""Endpoints dealing with user authentication."""

# IMPORT STANDARD LIBARIES
import os

# IMPORT THIRD PARTY LIBARIES
import fastapi
import jwt

# IMPORT LOCAL LIBARIES
from lorgs.clients import discord
from lorgs.models.user import User


SECRET_KEY = os.getenv("SECRET_KEY") or "my-super-secret-key"
REDIRECT_URI = os.getenv("REDIRECT_URI") or "http://localhost:9001/login"


router = fastapi.APIRouter()


@router.get("/token")
async def get_token(response: fastapi.Response, code: str):
    """Exchange a Authorization Code for some user info."""
    response.headers["Cache-Control"] = "no-cache"

    # get the discord access token
    user_credentials = await discord.exchange_code(code, redirect_uri=REDIRECT_URI)
    if user_credentials.get("error"):
        return {
            "error": user_credentials.get("error"),
            "message": user_credentials.get("error_description") or ""
        }

    # load user info
    access_token: str = user_credentials.get("access_token") # type: ignore
    info = await discord.get_user_profile(access_token)
    if not info:
        return

    # find existing User
    user = User.get_or_create(discord_id=info.id, discord_tag=info.tag)
    if not user:
        raise ValueError("Invalid User")

    # grap info from signin (in case users arn't members of the discord server)
    user.discord_id = info.id
    user.discord_tag = info.tag
    await user.refresh()
    user.save()

    # encode everything into JWT
    # converting the ID to string due to numberical issues
    token_data = {"id": str(user.discord_id)}
    token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
    return {"token": token}


@router.get("/users")
async def get_user_all():
    return "many"


@router.get("/users/{user_id:int}")
async def get_user(response: fastapi.Response, user_id: int):
    response.headers["Cache-Control"] = f"private, max-age={60*5}"

    user = User.objects(discord_id=user_id).first()
    if not user:
        try:
            user = User(discord_id=user_id)
            await user.refresh()
        except ValueError:
            raise fastapi.HTTPException(status_code=404, detail="User not found")
        else:
            user.save()

    return user.to_dict()


@router.get("/users/{user_id:int}/refresh")
async def user_refresh(response: fastapi.Response, user_id: int):

    user = User.objects(discord_id=user_id).first()
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="User not found")

    await user.refresh()
    user.save()

    response.headers["Cache-Control"] = "no-cache"
    return user.to_dict()
