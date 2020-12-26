from fastapi import FastAPI, APIRouter, Request, status
from settings import MAX_NAME_LENGTH, MIN_NAME_LENGTH
from pydantic import BaseModel, StrictStr
from Services.auth.auth_services import token_check, update_user


router = APIRouter()
app = FastAPI()


class UserSettingModel(BaseModel):
    username: StrictStr
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







