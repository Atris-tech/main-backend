from fastapi import Form
from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.auth_services import sign_up, create_auth_url, check_user, get_user_data, \
    create_access_token, verify_access_token, update_user
from Services.mail_service import send_mail
from pydantic import EmailStr

router = APIRouter()


@router.post("/register/", status_code=200)
def register(
        background_tasks: BackgroundTasks,
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
        url = create_auth_url(token, type="verify")
        data = {"user": user_name, "url": url}
        background_tasks.add_task(send_mail, [str(email)], "verify", data)
        return {
            "access_token": token,
            "token_type": "bearer",
        }
    else:
        raise HTTPException(status_code=400, detail="User Name or Email does not exists")


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
        verification_status = update_user(email=payload["email"], verified=True)
        if verification_status:
            return True
        else:
            raise HTTPException(status_code=400, detail="Email does not exists")


@router.post("/forgot-password/", status_code=200)
def reset(
        token: str = Form(...),
        password: str = Form(...)
):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token Expired")
    else:
        verification_status = update_user(email=payload["email"], password=password)
        if verification_status:
            return True
        else:
            raise HTTPException(status_code=400, detail="Email does not exists")