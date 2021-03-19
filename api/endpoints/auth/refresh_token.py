from fastapi import APIRouter
from Services.auth.auth_services import token_check
from starlette.requests import Request


router = APIRouter()


@router.post("/get_access_token/")
def get_new_token(request: Request):
    request.receive
    return token_check(request, refresh_token=True)
