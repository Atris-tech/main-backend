from fastapi import APIRouter
from Services.access_management_service import ban_user, unban_user
from pydantic import EmailStr, BaseModel
from starlette.requests import Request


class BanModel(BaseModel):
    email: EmailStr

router = APIRouter()

@router.post("/ban/")
def ban(ban_obj:BanModel):
    ban_user(ban_obj.email)
    return True

@router.post("/un_ban/")
def ban(ban_obj: BanModel):
    unban_user(ban_obj.email)
    return True