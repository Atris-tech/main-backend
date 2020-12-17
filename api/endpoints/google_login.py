from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from datetime import timedelta
from Services.auth_services import create_access_token
import settings
from fastapi import APIRouter


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
    return RedirectResponse(url=settings.AUTH_REDIRECT_URL + access_token)
