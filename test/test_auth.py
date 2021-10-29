import asyncio

import dotenv
dotenv.load_dotenv() # pylint: disable=wrong-import-position

from lorgs import auth



async def test_exchange_code():
    """
    visit: https://discord.com/oauth2/authorize?client_id=903080290925293628&redirect_uri=https%3A%2F%2Florrgs.nw.r.appspot.com%2F&response_type=code&scope=identify
    and login to obtain a code
    """
    code = "ecaKBTj46NYK5yY6KJfjsyYNR9nmUu"
    creds = await auth.exchange_code(code)
    print(creds)


async def test_get_user_profile():
    """
    get creds via `auth.exchange_code`
    """
    creds = {'access_token': 'ACCESS_TOKEN', 'expires_in': 604800, 'refresh_token': '<REFRESH_TOKEN>', 'scope': 'identify', 'token_type': 'Bearer'}
    user_info = await auth.get_user_profile(creds['access_token'])
    print(user_info)


async def test_get_member_info():
    user_id = 392483139991240714  # thats me!
    member_info = await auth.get_member_info(user_id)
    print(member_info)


async def test_get_member_permissions():
    user_id = 392483139991240714  # thats me!

    member_info = await auth.get_member_permissions(user_id)
    print(member_info)


if __name__ == "__main__":
    # asyncio.run(test_exchange_code())
    # asyncio.run(test_get_user_profile())
    # asyncio.run(test_get_member_info())
    # asyncio.run(test_get_member_info())
    asyncio.run(test_get_member_permissions())
