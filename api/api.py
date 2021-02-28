from fastapi import APIRouter
from .endpoints.auth import google_login, login, refresh_token, sign_up
from .endpoints import user_settings
from .endpoints.workspaces import workspace_management
from.endpoints.notes import upload_api
from .endpoints.notes import notes_management

api_router = APIRouter()
api_router.include_router(google_login.router, tags=["login"])
api_router.include_router(sign_up.router, tags=["sign-up"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(refresh_token.router, tags=["refresh_token"])
api_router.include_router(user_settings.router, tags=["user"])
api_router.include_router(workspace_management.router, tags=['workspaces'])
api_router.include_router(notes_management.router, tags=['notes'])
