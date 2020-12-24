from fastapi import APIRouter

from api.endpoints import google_login, sign_up, login, access_management, refresh_token

api_router = APIRouter()
api_router.include_router(google_login.router, tags=["login"])
api_router.include_router(sign_up.router, tags=["sign-up"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(refresh_token.router, tags=["refresh_token"])
api_router.include_router(access_management.router, tags=["access control management"])