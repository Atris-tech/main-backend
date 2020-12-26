from fastapi import Form
from fastapi import APIRouter, HTTPException, BackgroundTasks
<<<<<<<< HEAD:api/endpoints/auth/sign_up.py
from Services.auth.auth_services import sign_up, create_auth_url, check_user,\
    update_user_verification, token_check, create_verify_token
from Services.mail.mail_service import send_mail
from pydantic import EmailStr, BaseModel
from starlette.requests import Request
import error_constants


class SignUpModel(BaseModel):
    user_name: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str

========
from Services.auth_services import sign_up, create_auth_url, check_user, get_user_data, \
    create_access_token, verify_access_token, update_user
from Services.mail_service import send_mail
from pydantic import EmailStr
>>>>>>>> 7b1fc9a (removed acm added user auth removed uname from token):api/endpoints/sign_up.py

router = APIRouter()


@router.post("/register/", status_code=200)
<<<<<<<< HEAD:api/endpoints/auth/sign_up.py
def register(background_tasks: BackgroundTasks, register_obj: SignUpModel):
    username = register_obj.user_name.replace(" ", "").lower()
    user_obj = sign_up(
        user_name=username,
        email=register_obj.email.replace(" ", "").lower(),
        first_name=register_obj.first_name.replace(" ", "").lower(),
        last_name=register_obj.last_name.replace(" ", "").lower(),
        password=register_obj.password
    )

    token_data = create_verify_token(user_obj)
    token = token_data["token"]
    url = create_auth_url(token, type="verify")
    data = {"user": username, "url": url}
    background_tasks.add_task(send_mail, [str(register_obj.email)], "verify", data, "Verify your Atris Account")
    return True


class VerificationModel(BaseModel):
    type: str
    email: EmailStr
========
def register(
        background_tasks: BackgroundTasks,
        user_name: str = Form(...),
        email: EmailStr = Form(...),
        first_name: str = Form(...),
        last_name: str = Form(...),
        password: str = Form(...)
):
    token = sign_up(
        user_name, email, first_name, last_name,password=password 
    )
    if token:
        url = create_auth_url(token, type="verify")
        data = {"user": user_name, "url": url}
        background_tasks.add_task(send_mail, [str(email)], "verify", data)
        return {
            "access_token": token,
            "token_type": "bearer",
        }
    else:
        raise HTTPException(status_code=400, detail="User Name or Email does not exists")
>>>>>>>> 7b1fc9a (removed acm added user auth removed uname from token):api/endpoints/sign_up.py


@router.post("/resend-verification/", status_code=200)
def resend(
        background_tasks: BackgroundTasks,
        type: str = Form(...),
        email: EmailStr = Form(...),
):
    if check_user(email=email):
        data = get_user_data(email_address=email)
        token = create_access_token(data=data)
        if type == "verify":
            url = create_auth_url(token, type="verify")
            data = {"user": data["user_name"], "url": url}
            background_tasks.add_task(send_mail, [str(email)], "verify", data)
            return True
        elif type == "forgot_password":
            url = create_auth_url(token, type="forgot")
            data = {"user": data["user_name"], "url": url}
            background_tasks.add_task(send_mail, [str(email)], "forgot", data)
            return True
        else:
            return HTTPException(status_code=400, detail="Bad Request")
    else:
        raise HTTPException(status_code=400, detail="Email does not exists")


@router.post("/verify-user/", status_code=200)
def verification(
        token: str = Form(...)
):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token Expired")
    else:
<<<<<<<< HEAD:api/endpoints/auth/sign_up.py
        verification_status = update_user_verification(id=payload["id"], verified=True)
========
        verification_status = update_user(email=payload["email"], verified=True)
>>>>>>>> 7b1fc9a (removed acm added user auth removed uname from token):api/endpoints/sign_up.py
        if verification_status:
            return True
        else:
            raise HTTPException(status_code=400, detail="Email does not exists")


@router.post("/forgot-password/", status_code=200)
def reset(
        token: str = Form(...),
        password: str = Form(...)
):
<<<<<<<< HEAD:api/endpoints/auth/sign_up.py
    payload = token_check(request)
    verification_status = update_user_verification(id=payload["id"], password=forgot_password_obj.password)
    if verification_status:
        return True
========
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token Expired")
>>>>>>>> 7b1fc9a (removed acm added user auth removed uname from token):api/endpoints/sign_up.py
    else:
        verification_status = update_user(email=payload["email"], password=password)
        if verification_status:
            return True
        else:
            raise HTTPException(status_code=400, detail="Email does not exists")