from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, validator
from pydantic import EmailStr, StrictStr

from error_constants import EntityLengthError, BadRequest
from settings import MAX_USERNAME_LENGTH, MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH, MAX_NAME_LENGTH, MIN_NAME_LENGTH


class SignUpModel(BaseModel):
    user_name: str
    email: EmailStr
    first_name: StrictStr
    last_name: StrictStr
    password: str

    class Config:
        anystr_strip_whitespace = True

    @validator('*')
    def never_empty(cls, v, field):
        if not v:
            error_obj = EntityLengthError(entity=str(field.name), empty=True)
            raise HTTPException(status_code=error_obj.code, detail=error_obj.detail)
        return v

    @validator('first_name', 'last_name', 'user_name', 'password')
    def has_max_length(cls, v, field):
        if field.name == "user_name":
            max_length = MAX_USERNAME_LENGTH
        elif field.name == "password":
            max_length = MAX_PASSWORD_LENGTH
        else:
            max_length = MAX_NAME_LENGTH
        if len(v) > max_length:
            error_obj = EntityLengthError(entity=str(field.name), length=max_length, your_length=len(v))
            raise HTTPException(
                status_code=error_obj.code,
                detail=error_obj.detail
            )
        return v

    @validator('first_name', 'last_name', 'password')
    def has_min_length(cls, v, field):
        print(cls)
        if field.name == "password":
            min_length = MIN_PASSWORD_LENGTH
        else:
            min_length = MIN_NAME_LENGTH
        if len(v) < min_length:
            error_obj = EntityLengthError(entity=str(field.name), min_length=True, length=min_length, your_length=len(v)
                                          )
            raise HTTPException(
                status_code=error_obj.code,
                detail=error_obj.detail
            )
        return v


class VerificationModel(BaseModel):
    type: str
    email: EmailStr


class ForgotPasswordModel(BaseModel):
    password: str

    @validator('*')
    def never_empty(cls, v, field):
        if not v:
            error_obj = EntityLengthError(entity=str(field.name), empty=True)
            raise HTTPException(status_code=error_obj.code, detail=error_obj.detail)
        return v

    @validator('*')
    def has_max_length(cls, v, field):
        max_length = MAX_PASSWORD_LENGTH
        if len(v) > max_length:
            error_obj = EntityLengthError(entity=str(field.name), length=max_length, your_length=len(v))
            raise HTTPException(
                status_code=error_obj.code,
                detail=error_obj.detail
            )
        return v

    @validator('*')
    def has_min_length(cls, v, field):
        min_length = MIN_PASSWORD_LENGTH
        if len(v) < min_length:
            error_obj = EntityLengthError(entity=str(field.name), min_length=True, length=min_length,
                                          your_length=len(v))
            raise HTTPException(
                status_code=error_obj.code,
                detail=error_obj.detail
            )
        return v


class Login(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def has_max_length(cls, v, field):
        max_length = MAX_PASSWORD_LENGTH
        if len(v) > max_length:
            error_obj = EntityLengthError(entity=str(field.name), length=max_length, your_length=len(v))
            raise HTTPException(
                status_code=error_obj.code,
                detail=error_obj.detail
            )
        return v


class UserSettingModel(BaseModel):
    username: Optional[StrictStr]
    firstname: StrictStr
    lastname: StrictStr

    @validator('firstname', 'lastname', 'username')
    def has_max_length(cls, v, field):
        if field.name == "user_name":
            max_length = MAX_USERNAME_LENGTH
        else:
            max_length = MAX_NAME_LENGTH
        if len(v) > max_length:
            error_obj = EntityLengthError(entity=str(field.name), length=max_length, your_length=len(v))
            raise HTTPException(
                status_code=error_obj.code,
                detail=error_obj.detail
            )
        return v

    @validator('firstname', 'lastname')
    def has_min_length(cls, v, field):
        min_length = MIN_NAME_LENGTH
        if len(v) < min_length:
            error_obj = EntityLengthError(entity=str(field.name), min_length=True, length=min_length, your_length=len(v)
                                          )
            raise HTTPException(
                status_code=error_obj.code,
                detail=error_obj.detail
            )
        return v

    @validator('*')
    def never_empty(cls, v, field):
        if not v:
            error_obj = EntityLengthError(entity=str(field.name), empty=True)
            raise HTTPException(status_code=error_obj.code, detail=error_obj.detail)
        return v


class ChangePasswordModel(BaseModel):

    email_id: EmailStr
    old_password: str
    new_password: str

    @validator('old_password', 'new_password')
    def has_min_length(cls, v):
        min_length = MIN_PASSWORD_LENGTH
        max_length = MAX_PASSWORD_LENGTH
        if len(v) < min_length or len(v) > max_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v