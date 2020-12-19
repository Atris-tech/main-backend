from fastapi import Form
from fastapi import APIRouter, HTTPException
from Services.auth_services import login
from pydantic import EmailStr
from settings import AUTH_REDIRECT_URL
from starlette.responses import RedirectResponse


router = APIRouter()


@router.post("/login/")
def register(
        email: EmailStr = Form(...),
        password: str = Form(...)
):
    token = login(email, password)
    if not token:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif token == "un-verified":
        raise HTTPException(status_code=401, detail="Email not Verified")
    else:
        return RedirectResponse(url=AUTH_REDIRECT_URL + token)