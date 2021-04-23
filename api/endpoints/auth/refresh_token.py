from fastapi import APIRouter
from starlette.requests import Request

from Services.auth.auth_services import token_check

router = APIRouter()


@router.post("/get_access_token/")
def get_new_token(request: Request):
    return token_check(request, refresh_token=True)
