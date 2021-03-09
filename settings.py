import os
from dotenv import load_dotenv


load_dotenv()
PROJECT_NAME = "ATRIS Backend"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_YEAR = int(os.getenv("REFRESH_TOKEN_EXPIRE_YEAR"))
EMAIL_TOKEN_EXPIRY_HOURS= int(os.getenv("EMAIL_TOKEN_EXPIRY_HOURS"))
CONF_URL = os.getenv("CONF_URL")
BACKEND_CORS_ORIGINS = [os.getenv("CORS_ORIGINS")]
AUTH_REDIRECT_URL = os.getenv("AUTH_REDIRECT_URL")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
DEFAULT_PROFILE_PIC = os.getenv("DEFAULT_PROFILE_PIC")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = int(os.getenv("MAIL_PORT"))
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_TLS = True
MAIL_SSL = False
VERIFY_USER_URL = os.getenv("VERIFY_USER_URL")
FORGOT_PASSWORD_URL = os.getenv("FORGOT_PASSWORD_URL")
LOGIN_PAGE = os.getenv("LOGIN_PAGE")
REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_DB = os.getenv("REDIS_DB")
MAX_NAME_LENGTH = int(os.getenv("MAX_NAME_LENGTH"))
MIN_NAME_LENGTH = int(os.getenv("MIN_NAME_LENGTH"))
AZURE_BLOB_STORAGE_CONNECTION_STRING = os.getenv('AZURE_BLOB_STORAGE_CONNECTION_STRING')
AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
MIME_TYPES_IMAGES = {
    "jpg": "image/jpeg",
    "png": "image/png"
}
MIME_TYPES_AUDIO = {
    "mp3": "audio/mpeg",
    "wav": "audio/x-wav",
    "m4a": "audio/m4a",
    "mp4": "audio/mp4",
    "aiff": "audio/x-aiff",
    "aac": "audio/x-hx-aac-adts"
}
MAX_PROFILE_PHOTO_SIZE = int(os.getenv("MAX_PROFILE_PHOTO_SIZE"))