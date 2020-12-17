from fastapi import APIRouter

from api.endpoints import google_login

api_router = APIRouter()
api_router.include_router(google_login.router, tags=["login"])