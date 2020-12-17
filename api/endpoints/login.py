from fastapi import Form
from fastapi import APIRouter, HTTPException
from Services.auth_services import login
from pydantic import EmailStr


router = APIRouter()


@router.post("/login/")
def register(
        email: EmailStr = Form(...),
        password: str = Form(...)
):
    token = login(email, password)
    if not token:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif token:
        return {
            "access_token": token,
            "token_type": "bearer",
        }