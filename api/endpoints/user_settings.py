from fastapi import FastAPI, APIRouter, Request, File, UploadFile, HTTPException
from settings import MAX_NAME_LENGTH, MIN_NAME_LENGTH
from pydantic import BaseModel, StrictStr
from Services.auth.auth_services import token_check, update_user, get_user_data, check_user, remove_ref_token
from Services.storage_services import upload_profile
from typing import Optional


router = APIRouter()
app = FastAPI()


class UserSettingModel(BaseModel):
    username:  Optional[StrictStr]
    firstname: StrictStr
    lastname: StrictStr

    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = MIN_NAME_LENGTH
        max_anystr_length = MAX_NAME_LENGTH


@router.post("/change_user/", status_code=200)
def change_user_settings(
        user_setting_obj: UserSettingModel,
        request: Request,

):
    user_dict = token_check(request)
    return update_user(
        email=user_dict["email_id"],
        user_name=user_setting_obj.username,
        first_name=user_setting_obj.firstname,
        last_name=user_setting_obj.lastname
    )


@router.post("/user_data/", status_code=200)
def get_user_setting_data(
        request: Request
):
    user_dict = token_check(request)
    return get_user_data(
        email_address=user_dict["email_id"],
        user_setting=True
    )


@router.post("/change_profile/", status_code=200)
def change_dp(
        request: Request,
        file: UploadFile = File(...)
):
    user_dict = token_check(request)
    file_data = file.file.read()
    return upload_profile(email=user_dict["email_id"], file_data=file_data, file_name=file.filename)


@router.post("/logout_all_devices", status_code=200)
def logout_from_all_devices(
        request: Request
):
    user_dict = token_check(request)
    user_obj = check_user(email=user_dict["email_id"])
    if not user_obj:
        raise HTTPException(status_code=400)
    else:
        remove_ref_token(user_obj)
        return True





