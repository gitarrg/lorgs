"""Endpoints dealing with user authentication."""

# IMPORT STANDARD LIBARIES
import os
import typing

# IMPORT THIRD PARTY LIBARIES
from fastapi_cache.decorator import cache
import fastapi
import jwt
import pydantic


# IMPORT LOCAL LIBARIES
from lorgs import auth
from lorgs.models.user import User


SECRET_KEY = os.getenv("SECRET_KEY") or "my-super-secret-key"


class UserData(pydantic.BaseModel):
    discord_id: int
    discord_tag: str
    extra_roles: typing.List[str]


router = fastapi.APIRouter()


def _get_user(discord_id=0, discord_tag="", create=True):

    user = User.objects(discord_id=discord_id).first()
    if user:
        return user

    user = User.objects(discord_tag=discord_tag).first()
    if user:
        return user

    if create:
        return User(
            discord_id=discord_id,
            discord_tag=discord_tag,
        )


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
    info = await auth.get_user_profile(access_token)
    if not info:
        return

    discord_id = info.get("id")
    discord_tag = "{username}#{discriminator}".format(**info)

    # find existing User
    user = _get_user(discord_id=discord_id, discord_tag=discord_tag)

    # grap info from signin (in case users arn't members of the discord server)
    user.discord_id = discord_id
    user.discord_tag = discord_tag
    user.discord_avatar = info.get("avatar")
    await user.refresh()
    user.save()

    # encode everything into JWT
    # TODO: could drop the encoding?
    token_data = {"id": user.discord_id}
    token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
    return {"token": token}


# OLD: to be removed
@router.get("/info/{user_id:int}")
@cache()
async def get_user_info(user_id: int):
    member_info = await auth.get_member_info(user_id)
    return member_info.get("user") or {}


@router.get("/users")
async def get_user():
    return "many"


@router.post("/users")
async def add_user(info: UserData):
    user = User.objects(discord_id=info.discord_id).first()
    if user:
        raise fastapi.HTTPException(status_code=409, detail="User already exists.")

    user = User(
        discord_id=info.discord_id,
        discord_tag=info.discord_tag,
        extra_roles=info.extra_roles,
    )
    user.save()
    return "ok"


@router.get("/users/{user_id:int}")
@cache()
async def get_user2(user_id: int):
    user = User.objects(discord_id=user_id).first()
    if not user:
        user = User(discord_id=user_id)
        await user.refresh()
        user.save()
        # raise fastapi.HTTPException(status_code=404, detail="User not found")

    return user.to_dict()


@router.get("/users/{user_id:int}/refresh")
@cache()
async def user_refresh(user_id: int):

    user = User.objects(discord_id=user_id).first()
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="User not found")

    await user.refresh()
    user.save()

    return user.to_dict()
