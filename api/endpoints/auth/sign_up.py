from fastapi import APIRouter, HTTPException, BackgroundTasks
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


router = APIRouter()


@router.post("/register/", status_code=200)
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


@router.post("/resend-verification/", status_code=200)
def resend(
        background_tasks: BackgroundTasks,
        verification_model_obj: VerificationModel
):
    user_obj = check_user(email=verification_model_obj.email)
    if user_obj:
        token_data = create_verify_token(user_obj)
        token = token_data["token"]
        data = token_data["user_data"]
        if verification_model_obj.type == "verify":
            if user_obj.verified:
                raise HTTPException(
                    status_code=error_constants.EMAIL_ALREADY_VERIFIED["status_code"],
                    detail=error_constants.EMAIL_ALREADY_VERIFIED["detail"]
                )
            url = create_auth_url(token, type="verify")
            data = {"user": data["user_name"], "url": url}
            background_tasks.add_task(send_mail, [str(verification_model_obj.email)], "verify", data,
                                      "Verify your Atris Account")
            return True
        elif verification_model_obj.type == "forgot_password":
            url = create_auth_url(token, type="forgot")
            data = {"user": data["user_name"], "url": url}
            background_tasks.add_task(send_mail, [str(verification_model_obj.email)], "forgot", data,
                                      "Reset your Atris Account")
            return True
        else:
            return HTTPException(status_code=400)
    else:
        raise HTTPException(
            status_code=error_constants.INVALID_EMAIL["status_code"],
            detail=error_constants.INVALID_EMAIL["detail"]
        )


@router.post("/verify-user/", status_code=200)
def verification(
         request: Request
):
    payload = token_check(request)
    if not payload:
        raise HTTPException(
            status_code=error_constants.TOKEN_EXPIRED["status_code"],
            detail=error_constants.TOKEN_EXPIRED["detail"]
        )
    else:
        verification_status = update_user_verification(id=payload["id"], verified=True)
        if verification_status:
            return True
        else:
            raise HTTPException(status_code=400)


class ForgotPasswordModel(BaseModel):
    password: str


@router.post("/forgot-password/", status_code=200)
def reset(
        request: Request,
        forgot_password_obj: ForgotPasswordModel
):
    payload = token_check(request)
    verification_status = update_user_verification(id=payload["id"], password=forgot_password_obj.password)
    if verification_status:
        return True
    else:
        raise HTTPException(status_code=400)