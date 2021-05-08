import uuid

from fastapi import APIRouter, Request, File, UploadFile, HTTPException, Header, Depends

from Services.auth.auth_services import token_check, update_user, get_user_data, check_user, remove_ref_token, \
    change_password
from Services.storage_services import StorageServices
from api.endpoints.auth.models import UserSettingModel, ChangePasswordModel
from error_constants import MaxProfileLength, MinProfileLength
from settings import MAX_PROFILE_PHOTO_SIZE, MIN_PROFILE_PHOTO_SIZE

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


def valid_content_length(content_length: int = Header(..., lt=50_000_000)):
    return content_length


@router.post("/change_profile/", status_code=200)
def change_dp(
        request: Request,
        file: UploadFile = File(...),
        content_length: int = Depends(valid_content_length)
):
    user_dict = token_check(request)
    file_data = file.file.read()
    if content_length < MIN_PROFILE_PHOTO_SIZE:
        raise HTTPException(
            status_code=MinProfileLength.code,
            detail=MinProfileLength.detail
        )
    elif content_length > MAX_PROFILE_PHOTO_SIZE:
        raise HTTPException(
            status_code=MaxProfileLength.code,
            detail=MaxProfileLength.detail
        )
    file_name = str(uuid.uuid4()) + file.filename
    url_dict = StorageServices().upload_file_blob_storage(file_data=file_data, file_name=file_name,
                                                          email=user_dict["email_id"],
                                                          profile=True)
    url_dict.pop('container_name')
    return url_dict


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


@router.post("/change_password/", status_code=200)
def change_password_call(
        change_password_obj:ChangePasswordModel,
        request: Request
):
    print(change_password_obj.old_password)
    user_dict = token_check(request)
    return change_password(
        user_dict= user_dict,
        old_password= change_password_obj.old_password,
        new_password= change_password_obj.new_password,
        verify_new_password= change_password_obj.verify_new_password,
    )

