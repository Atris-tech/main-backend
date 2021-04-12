from fastapi import APIRouter

from Services.auth.auth_services import login
from api.endpoints.auth.models import Login

router = APIRouter()


@router.post("/login/")
def sign_in(login_input: Login):
    token_dict = login(login_input.email, login_input.password, new_user=False)
    return token_dict
