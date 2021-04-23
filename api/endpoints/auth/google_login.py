from random import randrange

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, HTTPException
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

import settings
from Services.auth.auth_services import check_user, user_name_gen, sign_up
from Services.auth.auth_services import login
from error_constants import UserBanned

router = APIRouter()
config = Config('.env')
oauth = OAuth(config)

oauth.register(
    name='google',
    server_metadata_url=settings.CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@router.get('/google-login/')
async def glogin(request: Request):
    redirect_uri = settings.AUTHLIB_REDIRECT_AUTH_URL
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = await oauth.google.parse_id_token(request, token)
    get_user = check_user(email=user["email"])
    if not get_user:
        get_user = check_user(user_name=user["given_name"])
        if get_user:
            user_name = user_name_gen()
            if get_user.user_name == user_name:
                user_name = user_name_gen() + str(randrange(1000))
                if get_user.user_name == user_name:
                    print("fucked up name")
                    return RedirectResponse(url=settings.LOGIN_PAGE)
            try:
                last_name = user["name"].split()[1].replace(" ", "").capitalize()
            except IndexError:
                last_name = None
            token_dict = sign_up(
                user_name=user_name.replace(" ", "").lower(),
                email=user["email"].replace(" ", "").lower(),
                first_name=user["name"].split()[0].replace(" ", "").capitalize(),
                last_name=last_name,
                picture=user["picture"],
                user_check=False
            )
            return RedirectResponse(url=settings.AUTH_REDIRECT_URL + "q=" + token_dict["access_token"] + "&ref=" +
                                        token_dict["ref_token"])
        else:
            print(user)
            try:
                last_name = user["name"].split()[1].replace(" ", "").capitalize()
            except IndexError:
                last_name = None
            token_dict = sign_up(
                user_name=user["given_name"].replace(" ", "").lower(),
                email=user["email"],
                first_name=user["name"].split()[0].replace(" ", "").capitalize(),
                last_name=last_name,
                picture=user["picture"],
                user_check=False
            )
            return RedirectResponse(url=settings.AUTH_REDIRECT_URL + "q=" + token_dict["access_token"] + "&ref=" +
                                        token_dict["ref_token"])
    else:
        token_dict = login(email_id=user["email"], password=False, user_obj=get_user, new_user=False)
        if token_dict == "user_banned":
            return HTTPException(
                status_code=UserBanned.code,
                detail=UserBanned.detail
            )
        else:
            return RedirectResponse(url=settings.AUTH_REDIRECT_URL + "q=" + token_dict["access_token"] + "&ref=" +
                                        token_dict["ref_token"])
