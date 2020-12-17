from jose import JWTError, jwt
from typing import Optional
from datetime import datetime, timedelta
import settings
from db_models.models.user_model import UserModel
from passlib.context import CryptContext
from db_models.mongo_setup import global_init
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


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def sign_up(user_name, email, first_name, last_name, password):
    try:
        UserModel.objects.get(user_name=user_name)
        return False
    except UserModel.DoesNotExist:
        try:
            UserModel.objects.get(email_id=email)
            return False
        except UserModel.DoesNotExist:
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
                "picture": settings.DEFAULT_PROFILE_PIC
            }
            token = create_access_token(data)
            return token


def login(email_id, password):
    try:
        user_model_obj = UserModel.objects.get(email_id=email_id)
        password_hash = user_model_obj.password_hash
        if not verify_password(plain_password=password, hashed_password=password_hash):
            return False
        else:
            data = {
                "user_name": user_model_obj.user_name,
                "email": user_model_obj.email_id,
                "full name": user_model_obj.first_name + " " + user_model_obj.last_name,
                "picture": user_model_obj.image
            }
            token = create_access_token(data)
            return token
    except UserModel.DoesNotExist:
        return False

