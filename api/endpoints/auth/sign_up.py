from fastapi import APIRouter, HTTPException, BackgroundTasks
from starlette.requests import Request

import error_constants
from Services.auth.auth_services import sign_up, create_auth_url, check_user, \
    update_user_verification, token_check, create_verify_token
from Services.mail.mail_service import email_builder
from api.endpoints.auth.models import SignUpModel, VerificationModel, ForgotPasswordModel

router = APIRouter()


@router.post("/register/", status_code=200)
def register(background_tasks: BackgroundTasks, register_obj: SignUpModel):
    username = register_obj.user_name.replace(" ", "").lower()
    user_obj = sign_up(
        user_name=username,
        email=register_obj.email.replace(" ", "").lower(),
        first_name=register_obj.first_name.replace(" ", "").capitalize(),
        last_name=register_obj.last_name.replace(" ", "").capitalize(),
        password=register_obj.password
    )

    token_data = create_verify_token(user_obj, verify=True)
    token = token_data["token"]
    url = create_auth_url(token, type="verify")
    email_variable = {
        "FIRSTNAME": register_obj.first_name.replace(" ", "").capitalize(),
        "URL": url
    }
    background_tasks.add_task(email_builder, str(register_obj.email), email_variable, "Verify your Atris Account",
                              "verify_user")
    email_variable = {
        "FIRSTNAME": register_obj.first_name.replace(" ", "").capitalize(),
    }
    background_tasks.add_task(email_builder, str(register_obj.email), email_variable, "Welcome to Atris",
                              "welcome")
    return True


@router.post("/resend-verification/", status_code=200)
def resend(
        background_tasks: BackgroundTasks,
        verification_model_obj: VerificationModel
):
    user_obj = check_user(email=verification_model_obj.email)
    if user_obj:

        if verification_model_obj.type == "verify":
            token_data = create_verify_token(user_obj, verify=True)
            token = token_data["token"]
            data = token_data["user_data"]
            if user_obj.verified:
                raise HTTPException(
                    status_code=error_constants.EmailAlreadyVerified.code,
                    detail=error_constants.EmailAlreadyVerified.detail
                )
            url = create_auth_url(token, type="verify")
            email_variable = {
                "FIRSTNAME": data["user_name"],
                "URL": url
            }
            background_tasks.add_task(email_builder, str(verification_model_obj.email), email_variable,
                                      "Verify your Atris Account",
                                      "verify_user")
            return True
        elif verification_model_obj.type == "forgot_password":
            token_data = create_verify_token(user_obj, forgot_password=True)
            token = token_data["token"]
            data = token_data["user_data"]
            url = create_auth_url(token, type="forgot")
            email_variable = {
                "FIRSTNAME": data["user_name"],
                "URL": url
            }
            background_tasks.add_task(email_builder, str(verification_model_obj.email), email_variable,
                                      "Reset your Atris Account Password",
                                      "forgot_password")
            return True
        else:
            return HTTPException(status_code=400)
    else:
        raise HTTPException(
            status_code=error_constants.InvalidEmailError.code,
            detail=error_constants.InvalidEmailError.detail
        )


@router.post("/verify-user/", status_code=200)
def verification(
        request: Request
):
    payload = token_check(request, verify=True)
    verification_status = update_user_verification(id=payload["id"], verified=True)
    if verification_status:
        return True
    else:
        raise HTTPException(status_code=400)


@router.post("/forgot-password/", status_code=200)
def reset(
        request: Request,
        forgot_password_obj: ForgotPasswordModel
):
    payload = token_check(request, forgot_password=True)
    verification_status = update_user_verification(id=payload["id"], password=forgot_password_obj.password)
    if verification_status:
        return True
    else:
        raise HTTPException(status_code=400)
