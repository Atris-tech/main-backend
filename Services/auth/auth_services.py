from dateutil.relativedelta import relativedelta
from jose import JWTError, jwt
from Services.redis_service import get_val, set_val
from datetime import datetime
import settings
from db_models.models.user_model import UserModel
from passlib.context import CryptContext
from db_models.mongo_setup import global_init
from coolname import generate_slug
from db_models.models.token_model import TokenModel
from fastapi import HTTPException
import error_constants


global_init()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_jwt_token(data, expire_date_time):
    to_encode = data.copy()
    to_encode.update({"exp": expire_date_time})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError as e:
        """LOG JWT ERROR HERE"""
        print(e)
        return False


def create_verify_token(user_obj):
    user_dict = dict()
    user_dict["token_type"] = "verify"
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
    user_dict["token_type"] = "refresh_token"
    user_dict["email_id"] = user_obj.email_id
    user_dict["user_name"] = user_obj.user_name
    user_dict["account_type"] = user_obj.account_type
    user_dict["verified"] = user_obj.verified
    expiry_year = datetime.now() + relativedelta(years=settings.REFRESH_TOKEN_EXPIRE_YEAR)
    ref_token = create_jwt_token(data=user_dict, expire_date_time=expiry_year.timestamp())
    if token_obj:
        token_obj.refresh_token = ref_token
        token_obj.save()
    else:
        token_obj = TokenModel(user=user_obj, refresh_token=ref_token)
        token_obj.save()
    user_dict["plan"] = user_obj.plan
    user_dict.pop("verified", None)
    user_dict["token_type"] = "access_token"
    expiry_min = datetime.now() + relativedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_jwt_token(data=user_dict, expire_date_time=expiry_min.timestamp())
    set_val(ref_token, user_dict, json_type=True)
    return {"ref_token": ref_token, "access_token": access_token}


def get_ref_token(user_obj):
    try:
        token_obj = TokenModel.objects.get(user=user_obj)
        ref_token = token_obj.refresh_token
        print(ref_token)
        payload = verify_jwt_token(ref_token)
        if payload:
            user_dict = get_val(ref_token, json_type=True)
            if user_dict is not None:
                if "banned" in user_dict:
                    print("USER BANNED")
                    raise HTTPException(
                        status_code=error_constants.USER_BANNED["status_code"],
                        detail=error_constants.USER_BANNED["detail"]
                    )
                expiry_min = datetime.now() + relativedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_jwt_token(data=user_dict, expire_date_time=expiry_min.timestamp())
                set_val(ref_token, user_dict, json_type=True)
                return {"ref_token": ref_token, "access_token": access_token}
            else:
                return create_ref_token(user_obj=user_obj, token_obj=token_obj)
        else:
            return create_ref_token(user_obj=user_obj, token_obj=token_obj)
    except TokenModel.DoesNotExist:
        return create_ref_token(user_obj=user_obj)


def refresh_token_utils(ref_token=False, user_obj=False, new_user=True):
    if ref_token:
        """get access token"""
        if verify_jwt_token(ref_token):
            user_dict = get_val(ref_token, json_type=True)
            if "banned" in user_dict:
                print("USER BANNEDDD")
                raise HTTPException(
                    status_code=error_constants.USER_BANNED["status_code"],
                    detail=error_constants.USER_BANNED["detail"]
                )
            elif not user_dict:
                raise HTTPException(
                    status_code=error_constants.TOKEN_NOT_EXIST["status_code"],
                    detail=error_constants.TOKEN_NOT_EXIST["detail"]
                )
            else:
                expiry_min = datetime.now() + relativedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_jwt_token(data=user_dict, expire_date_time=expiry_min.timestamp())
                return access_token
        else:
            raise HTTPException(
                status_code=error_constants.RF_TOKEN_EXPIRED_INVALID["status_code"],
                detail=error_constants.RF_TOKEN_EXPIRED_INVALID["detail"]
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
            return False
    else:
        try:
            user_obj = UserModel.objects.get(user_name=user_name)
            return user_obj
        except UserModel.DoesNotExist:
            return False


def sign_up(user_name, email, first_name, last_name, picture=False, password=False, user_check=True):
    if user_check:
        if check_user(user_name=user_name):
            raise HTTPException(
                status_code=error_constants.USER_NAME_TAKEN["status_code"],
                detail=error_constants.USER_NAME_TAKEN["detail"]
            )
        elif check_user(email=email):
            raise HTTPException(
                status_code=error_constants.EMAIL_ID_EXISTS["status_code"],
                detail=error_constants.EMAIL_ID_EXISTS["detail"]
            )
    user_model_obj = UserModel()
    user_model_obj.user_name = user_name.lower()
    user_model_obj.first_name = first_name
    user_model_obj.last_name = last_name
    user_model_obj.email_id = email
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


def get_user_data(user_name=False, email_address=False, user_obj=False):
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


def login(email_id, password=True, user_obj=False, new_user=True):
    try:
        user_model_obj = UserModel.objects.get(email_id=email_id)
        if password:
            password_hash = user_model_obj.password_hash
            if not verify_password(plain_password=password, hashed_password=password_hash):
                raise HTTPException(
                    status_code=error_constants.INCORRECT_PASSWORD["status_code"],
                    detail=error_constants.INCORRECT_PASSWORD["detail"]
                )
            if not user_model_obj.verified:
                raise HTTPException(
                    status_code=error_constants.VERIFICATION_ERROR["status_code"],
                    detail=error_constants.VERIFICATION_ERROR["detail"]
                )

        if not new_user:
            print("in no new user")
            return refresh_token_utils(user_obj=user_model_obj, new_user=new_user)

        return refresh_token_utils(user_obj=user_obj)
    except UserModel.DoesNotExist:
        raise HTTPException(
            status_code=error_constants.INVALID_EMAIL["status_code"],
            detail=error_constants.INVALID_EMAIL["detail"]
        )


def update_user(email=False, user_name=False, password=False, first_name=False, last_name=False,
                verified=False, id=False):
    try:
        if user_name:
            user_model_obj = UserModel.objects.get(email_id=email)
            user_model_obj.update(user_name=user_name)
            return True
        elif password:
            password_hash = get_password_hash(password)
            user_model_obj = UserModel.objects.get(id=id)
            user_model_obj.update(password_hash=password_hash)
            return True
        elif first_name:
            user_model_obj = UserModel.objects.get(email_id=email)
            user_model_obj.update(first_name=first_name)
            return True
        elif last_name:
            user_model_obj = UserModel.objects.get(email_id=email)
            user_model_obj.update(last_name=last_name)
            return True
        elif verified:
            user_model_obj = UserModel.objects.get(id=id)
            user_model_obj.update(verified=verified)
            return True
    except UserModel.DoesNotExist:
        return False


def user_name_gen():
    username = generate_slug(2).lower()
    return username


def token_check(request):
    token = request.headers.get("Authorization")
    if token is None:
        raise HTTPException(
            status_code=error_constants.TOKEN_NOT_EXIST["status_code"],
            detail=error_constants.TOKEN_NOT_EXIST["detail"]
        )
    token = token.split()
    token = token[1]
    payload = verify_jwt_token(token)
    if payload:
        return payload
    else:
        raise HTTPException(
            status_code=error_constants.TOKEN_EXPIRED["status_code"],
            detail=error_constants.TOKEN_EXPIRED["detail"]
        )