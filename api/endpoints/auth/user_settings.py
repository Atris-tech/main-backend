from fastapi import APIRouter, Request, File, UploadFile, HTTPException

from Services.auth.auth_services import token_check, update_user, get_user_data, check_user, remove_ref_token
from Services.storage_services import StorageServices
from api.endpoints.auth.models import UserSettingModel

router = APIRouter()


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
    return StorageServices().upload_file_blob_storage(file_data=file_data, file_name=file.filename,
                                                      email=user_dict["email_id"],
                                                      profile=True)


@router.post("/logout_all_devices/", status_code=200)
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
