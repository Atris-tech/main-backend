from jose import JWTError, jwt
import jose
from typing import Optional
from datetime import datetime, timedelta
import settings
from db_models.models.user_model import UserModel
from passlib.context import CryptContext
from db_models.mongo_setup import global_init
from .mail_body_return_service import mail_body
global_init()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_access_token(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jose.exceptions.ExpiredSignatureError:
        return False


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
            UserModel.objects.get(email_id=email)
            return True
        except UserModel.DoesNotExist:
            return False
    else:
        try:
            UserModel.objects.get(user_name=user_name)
            return True
        except UserModel.DoesNotExist:
            return False


def sign_up(user_name, email, first_name, last_name, password):
    if check_user(user_name=user_name):
        return False
    elif check_user(email=email):
        return False
    else:
        user_model_obj = UserModel()
        user_model_obj.user_name = user_name
        user_model_obj.first_name = first_name
        user_model_obj.last_name = last_name
        user_model_obj.email_id = email
        user_model_obj.password_hash = get_password_hash(password)
        user_model_obj.account_type = "Normal"
        user_model_obj.save()
        data = {
            "user_name": user_name,
            "email": email,
            "full name": first_name + " " + last_name,
        }
        token = create_access_token(data)
        return token


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


def login(email_id, password):
    try:
        user_model_obj = UserModel.objects.get(email_id=email_id)
        password_hash = user_model_obj.password_hash
        if not verify_password(plain_password=password, hashed_password=password_hash):
            return False
        elif not user_model_obj.verified:
            return "un-verified"

        else:
            data = get_user_data(user_obj=user_model_obj)
            token = create_access_token(data)
            return token
    except UserModel.DoesNotExist:
        return False


def update_user(email, user_name=False, password=False, first_name=False, last_name=False,
                verified=False):
    try:
        if user_name:
            user_model_obj = UserModel.objects.get(email_id=email)
            user_model_obj.update(user_name=user_name)
            return True
        elif password:
            password_hash = get_password_hash(password)
            user_model_obj = UserModel.objects.get(email_id=email)
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
            user_model_obj = UserModel.objects.get(email_id=email)
            user_model_obj.update(verified=verified)
            return True
    except UserModel.DoesNotExist:
        return False