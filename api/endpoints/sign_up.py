from fastapi import Form
from fastapi import APIRouter, HTTPException
from Services.auth_services import sign_up
from pydantic import EmailStr


router = APIRouter()


@router.post("/register/")
def register(
        user_name: str = Form(...),
        email: EmailStr = Form(...),
        first_name: str = Form(...),
        last_name: str = Form(...),
        password: str = Form(...)
):
    token = sign_up(
        user_name, email, first_name, last_name, password
    )
    if token:
        return {
            "access_token": token,
            "token_type": "bearer",
        }
    else:
        raise HTTPException(status_code=400, detail="User Name or Email exists")
