from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from datetime import timedelta
from Services.auth_services import create_access_token
import settings
from fastapi import APIRouter
from Services.auth_services import check_user, user_name_gen, sign_up
from random import randrange


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


@router.get('/google-login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = await oauth.google.parse_id_token(request, token)
    data_dict = {
        "user_name": user["given_name"],
        "email": user["email"],
        "Full Name": user["name"],
        "picture": user["picture"]
    }
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=data_dict, expires_delta=access_token_expires
    )
    if not check_user(email=user["email"]):
        if check_user(user_name=user["given_name"]):
            user_name = user_name_gen()
            if check_user(user_name=user_name):
                user_name = user_name_gen() + str(randrange(1000))
                if check_user(user_name=user_name):
                    return RedirectResponse(url=settings.LOGIN_PAGE)
            access_token = sign_up(
                user_name=user_name,
                email=user["email"],
                first_name=user["name"].split()[0],
                last_name=user["name"].split()[1],
                picture=user["picture"],
                user_check=False
            )
            return RedirectResponse(url=settings.AUTH_REDIRECT_URL + access_token)
        else:
            access_token = sign_up(
                user_name=user["given_name"],
                email=user["email"],
                first_name=user["name"].split()[0],
                last_name=user["name"].split()[1],
                picture=user["picture"],
                user_check=False
            )
            return RedirectResponse(url=settings.AUTH_REDIRECT_URL + access_token)
    else:
        return RedirectResponse(url=settings.AUTH_REDIRECT_URL + access_token)
