from fastapi import APIRouter, HTTPException
from Services.auth.auth_services import refresh_token_utils
from starlette.requests import Request
import error_constants


router = APIRouter()


@router.post("/get_access_token/")
def get_new_token(
        request: Request
):
    token = request.headers.get("Authorization")
    if token is None:
        raise HTTPException(
            status_code=error_constants.TOKEN_NOT_EXIST["status_code"],
            detail=error_constants.TOKEN_NOT_EXIST["detail"]
        )
    token = token.split()
    token = token[1]
    return refresh_token_utils(ref_token=token)
