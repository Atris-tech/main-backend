from datetime import datetime

from coolname import generate_slug
from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext

import error_constants
import settings
from Services.redis_service import get_val, set_val, redis_obj
from db_models.models.token_model import TokenModel
from db_models.models.user_model import UserModel
from db_models.mongo_setup import global_init

global_init()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_jwt_token(data, expire_date_time):
    print(data)
    to_encode = data.copy()
    to_encode.update({"exp": expire_date_time})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt


def verify_jwt_token(token, verify=False, forgot_password=False, refresh_token=False):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if verify and payload["token_type"] == "verify":
            print("here in verify")
            return payload
        elif verify and payload["token_type"] != "verify":
            print("here in verify and not verify")
            raise HTTPException(
                status_code=error_constants.BadRequest.code,
                detail=error_constants.BadRequest.detail
            )
        elif not verify and payload["token_type"] == "verify":
            print("here in not verify and token verify")
            raise HTTPException(
                status_code=error_constants.BadRequest.code,
                detail=error_constants.BadRequest.detail
            )
        if forgot_password and payload["token_type"] == "forgot_password":
            print("here in forgot password")
            return payload
        elif forgot_password and payload["token_type"] != "forgot_password":
            print("print here in forgot password and token not forgot password")
            raise HTTPException(
                status_code=error_constants.BadRequest.code,
                detail=error_constants.BadRequest.detail
            )
        elif not forgot_password and payload["token_type"] == "forgot_password":
            print("print here in not forgot password and token forgot password")
            raise HTTPException(
                status_code=error_constants.BadRequest.code,
                detail=error_constants.BadRequest.detail
            )
        if refresh_token and payload["token_type"] == "refresh_token":
            print("print here in refresh token")
            return payload
        elif refresh_token and payload["token_type"] != "refresh_token":
            print("print here in refresh token and token not refresh token")
            raise HTTPException(
                status_code=error_constants.BadRequest.code,
                detail=error_constants.BadRequest.detail
            )
        elif not refresh_token and payload["token_type"] == "refresh_token":
            print("print here in not refresh token and token refresh token")
            raise HTTPException(
                status_code=error_constants.BadRequest.code,
                detail=error_constants.BadRequest.detail
            )
        print("access token")
        return payload
    except JWTError as e:
        """LOG JWT ERROR HERE"""
        print(e)
        return False


def create_verify_token(user_obj, verify=False, forgot_password=False):
    user_dict = dict()
    if verify:
        user_dict["token_type"] = "verify"
    if forgot_password:
        user_dict["token_type"] = "forgot_password"
    user_dict["email_id"] = user_obj.email_id
    user_dict["user_name"] = user_obj.user_name
    user_dict["id"] = str(user_obj.id)
    expiry_year = datetime.now() + relativedelta(hours=settings.EMAIL_TOKEN_EXPIRY_HOURS)
    token = create_jwt_token(data=user_dict, expire_date_time=expiry_year.timestamp())
    return {"token": token, "user_data": user_dict}


def create_ref_token(email=False, user_obj=False, token_obj=False):
    user_dict = dict()
    if email:
        user_obj = UserModel.objects.get(email_id=email)
    """Create refresh token here"""
    print("in create ref")
    print(user_obj.email_id)
    user_dict["token_type"] = "refresh_token"
    user_dict["email_id"] = user_obj.email_id
    user_dict["account_type"] = user_obj.account_type
    user_dict["verified"] = user_obj.verified
    expiry_year = datetime.now() + relativedelta(years=settings.REFRESH_TOKEN_EXPIRE_YEAR)
    ref_token = create_jwt_token(data=user_dict, expire_date_time=expiry_year.timestamp())
    print(ref_token)
    print("referesh token created")
    if token_obj:
        print("in token obj")
        token_obj.refresh_token = ref_token
        token_obj.save()
    else:
        print("in else token obj")
        token_obj = TokenModel(user=user_obj, refresh_token=ref_token)
        token_obj.save()
    user_dict["plan"] = user_obj.plan
    user_dict.pop("verified", None)
    user_dict["token_type"] = "access_token"
    expiry_min = datetime.now() + relativedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    print("above create jwt token")
    access_token = create_jwt_token(data=user_dict, expire_date_time=expiry_min.timestamp())
    print(access_token)
    set_val(ref_token, user_dict, json_type=True)
    print("set value done")
    return {"ref_token": ref_token, "access_token": access_token}


def get_ref_token(user_obj):
    try:
        token_obj = TokenModel.objects.get(user=user_obj)
        ref_token = token_obj.refresh_token
        print(ref_token)
        if token_obj.token_status == "Dead":
            raise HTTPException(
                status_code=error_constants.UserBanned.code,
                detail=error_constants.UserBanned.detail
            )
        if ref_token is None:
            return create_ref_token(user_obj=user_obj, token_obj=token_obj)
        else:
            print("get ref else")
            payload = verify_jwt_token(token=ref_token, refresh_token=True)
            print(payload)
            if payload:
                user_dict = get_val(ref_token, json_type=True)
                print(user_dict)
                if user_dict is not None:
                    if "banned" in user_dict:
                        raise HTTPException(
                            status_code=error_constants.UserBanned.code,
                            detail=error_constants.UserBanned.detail
                        )
                    expiry_min = datetime.now() + relativedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
                    access_token = create_jwt_token(data=user_dict, expire_date_time=expiry_min.timestamp())
                    set_val(ref_token, user_dict, json_type=True)
                    return {"ref_token": ref_token, "access_token": access_token}
                else:
                    print("user dict null")
                    return create_ref_token(user_obj=user_obj, token_obj=token_obj)
            else:
                return create_ref_token(user_obj=user_obj, token_obj=token_obj)
    except TokenModel.DoesNotExist:
        return create_ref_token(user_obj=user_obj)


def remove_ref_token(user_obj):
    try:
        token_obj = TokenModel.objects.get(user=user_obj)
        refresh_token = token_obj.refresh_token
        token_obj.update(refresh_token=None)
        redis_obj.delete(str(refresh_token))
    except TokenModel.DoesNotExist:
        pass


def refresh_token_utils(ref_token=False, user_obj=False, new_user=True):
    if ref_token:
        """get access token"""
        if verify_jwt_token(ref_token, refresh_token=True):
            user_dict = get_val(ref_token, json_type=True)
            if user_dict is None:
                raise HTTPException(
                    status_code=error_constants.TokenDoesNotExist.code,
                    detail=error_constants.TokenDoesNotExist.detail
                )
            if "banned" in user_dict:
                raise HTTPException(
                    status_code=error_constants.UserBanned.code,
                    detail=error_constants.UserBanned.detail
                )
            else:
                expiry_min = datetime.now() + relativedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_jwt_token(data=user_dict, expire_date_time=expiry_min.timestamp())
                return access_token
        else:
            raise HTTPException(
                status_code=error_constants.RfTokenExpiredInvalid.code,
                detail=error_constants.RfTokenExpiredInvalid.detail
            )
    if not new_user:
        return get_ref_token(user_obj)
    else:
        return create_ref_token(user_obj=user_obj)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_auth_url(token, type):
    if type == "verify":
        url = settings.VERIFY_USER_URL + token
        return url
    elif type == "forgot":
        url = settings.FORGOT_PASSWORD_URL + token
        return url


def check_user(email=False, user_name=False):
    if email:
        try:
            user_obj = UserModel.objects.get(email_id=email)
            return user_obj
        except UserModel.DoesNotExist:
            print("user model doesnot exists")
            return False
    else:
        try:
            user_name = str(user_name).lower()
            user_obj = UserModel.objects.get(user_name=user_name)
            return user_obj
        except UserModel.DoesNotExist:
            return False


def sign_up(user_name, email, first_name, last_name, picture=False, password=False, user_check=True):
    if user_check:
        if check_user(user_name=user_name):
            raise HTTPException(
                status_code=error_constants.UserNameTaken.code,
                detail=error_constants.UserNameTaken.detail
            )
        elif check_user(email=email):
            raise HTTPException(
                status_code=error_constants.EmailIdExists.code,
                detail=error_constants.EmailIdExists.detail
            )
    user_model_obj = UserModel()
    user_model_obj.user_name = user_name.lower()
    user_model_obj.first_name = first_name
    user_model_obj.last_name = last_name
    user_model_obj.email_id = email
    space = get_val("FREE_USER_SPACE")
    user_model_obj.space = space
    if user_check:
        user_model_obj.password_hash = get_password_hash(password)
        user_model_obj.account_type = "Normal"
        user_model_obj.save()
        return user_model_obj
    else:
        user_model_obj.account_type = "Third Party Oath"
        user_model_obj.image = picture
        user_model_obj.verified = True
        user_model_obj.save()
        return refresh_token_utils(user_obj=user_model_obj)


def get_user_data(user_name=False, email_address=False, user_obj=False, user_setting=False):
    if user_obj:
        data = {
            "user_name": user_obj.user_name,
            "email": user_obj.email_id,
            "full name": user_obj.first_name + " " + user_obj.last_name,
            "picture": user_obj.image
        }
        return data
    elif email_address:
        user_obj = UserModel.objects.get(email_id=email_address)
        if user_setting:
            data = {
                "user_name": user_obj.user_name,
                "first_name": user_obj.first_name,
                "last_name": user_obj.last_name,
                "picture": user_obj.image
            }
        else:
            data = {
                "user_name": user_obj.user_name,
                "email": user_obj.email_id,
                "full name": user_obj.first_name + " " + user_obj.last_name,
                "picture": user_obj.image
            }
        return data
    elif user_name:
        user_obj = UserModel.objects.get(user_name=user_name)
        data = {
            "user_name": user_obj.user_name,
            "email": user_obj.email_id,
            "full name": user_obj.first_name + " " + user_obj.last_name,
            "picture": user_obj.image
        }
        return data


def login(email_id: str, password: bool = True, user_obj=False, new_user=True):
    try:
        print(email_id)
        email_id = email_id.lower()
        user_model_obj = UserModel.objects.get(email_id=email_id)
        print(user_model_obj.user_name)
        print(user_model_obj.password_hash)
        print(user_model_obj.verified)
        if password:
            password_hash = user_model_obj.password_hash
            a = verify_password(plain_password=password, hashed_password=password_hash)
            print("a")
            print(a)
            if not a:
                raise HTTPException(
                    status_code=error_constants.IncorrectPassword.code,
                    detail=error_constants.IncorrectPassword.detail
                )
            if not user_model_obj.verified:
                raise HTTPException(
                    status_code=error_constants.VerificationError.code,
                    detail=error_constants.VerificationError.detail
                )

        if not new_user:
            return refresh_token_utils(user_obj=user_model_obj, new_user=new_user)

        return refresh_token_utils(user_obj=user_obj)
    except UserModel.DoesNotExist:
        raise HTTPException(
            status_code=error_constants.InvalidEmailError.code,
            detail=error_constants.InvalidEmailError.detail
        )


def update_user_verification(password=False, verified=False, id=False):
    try:
        if password:
            password_hash = get_password_hash(password)
            user_model_obj = UserModel.objects.get(id=id)
            user_model_obj.update(password_hash=password_hash)
            remove_ref_token(user_model_obj)
            return True
        elif verified:
            user_model_obj = UserModel.objects.get(id=id)
            user_model_obj.update(verified=verified)
            return True
    except UserModel.DoesNotExist:
        return False


def update_user(email=False, user_name=False, first_name=False, last_name=False):
    try:
        user_model_obj = UserModel.objects.get(email_id=email)
        if user_name:
            try:
                UserModel.objects.get(user_name=user_name)
                raise HTTPException(
                    status_code=error_constants.UserNameTaken.code,
                    detail=error_constants.UserNameTaken.detail
                )
            except UserModel.DoesNotExist:
                user_model_obj.user_name = user_name
        if first_name:
            user_model_obj.first_name = first_name
        if last_name:
            user_model_obj.last_name = last_name
        user_model_obj.save()
        return True
    except UserModel.DoesNotExist:
        raise HTTPException(
            status_code=error_constants.InvalidEmailError.code,
            detail=error_constants.InvalidEmailError.detail
        )


def user_name_gen():
    username = generate_slug(2).lower()
    return username


def token_check(request, verify=False, forgot_password=False, refresh_token=False):
    token = request.headers.get("Authorization")
    if token is None:
        raise HTTPException(
            status_code=error_constants.TokenDoesNotExist.code,
            detail=error_constants.TokenDoesNotExist.detail
        )
    token = token.split()
    token = token[1]
    if verify:
        payload = verify_jwt_token(token, verify=True)
        return payload
    if forgot_password:
        payload = verify_jwt_token(token, forgot_password=True)
        return payload
    if refresh_token:
        return refresh_token_utils(ref_token=token)
    print("here in payload")
    payload = verify_jwt_token(token)
    if payload:
        print(payload)
        return payload
    else:
        raise HTTPException(
            status_code=error_constants.TokenExpired.code,
            detail=error_constants.TokenExpired.detail
        )
