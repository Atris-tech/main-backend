from fastapi import APIRouter
from .endpoints.search import search_api
from .endpoints.auth import google_login, login, refresh_token, sign_up
from .endpoints.auth import user_settings
from .endpoints.notes import notes_management_api
from .endpoints.tags import tag_management
from .endpoints.workspaces import workspace_management
from .endpoints import save_celery_data_hook

api_router = APIRouter()
api_router.include_router(google_login.router, tags=["login"])
api_router.include_router(sign_up.router, tags=["sign-up"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(refresh_token.router, tags=["refresh_token"])
api_router.include_router(user_settings.router, tags=["user"])
api_router.include_router(workspace_management.router, tags=['workspaces'])
api_router.include_router(notes_management_api.router, tags=['notes'])
api_router.include_router(tag_management.router, tags=['tags'])
api_router.include_router(search_api.router, tags=['image_search'])
api_router.include_router(search_api.router, tags=['audio_search'])
api_router.include_router(search_api.router, tags=['note_search'])
api_router.include_router(save_celery_data_hook.router, tags=['celery_hook'])

