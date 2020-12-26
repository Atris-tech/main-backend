from fastapi import APIRouter
from Services.auth.auth_services import login
from pydantic import EmailStr, BaseModel
from starlette.requests import Request


router = APIRouter()


class Login(BaseModel):
    email: EmailStr
    password: str


@router.post("/login/")
def sign_in(login_input: Login):
    token_dict = login(login_input.email, login_input.password, new_user=False)
    return token_dict