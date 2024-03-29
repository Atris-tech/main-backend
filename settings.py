import os

import sentry_sdk
from dotenv import load_dotenv

load_dotenv()

# API DOCS PROJECT NAME
PROJECT_NAME = "ATRIS Backend"
# JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))
# TOKEN
REFRESH_TOKEN_EXPIRE_YEAR = int(os.getenv("REFRESH_TOKEN_EXPIRE_YEAR"))
EMAIL_TOKEN_EXPIRY_HOURS = int(os.getenv("EMAIL_TOKEN_EXPIRY_HOURS"))
# GOOGLE LOGIN
CONF_URL = os.getenv("CONF_URL")
BACKEND_CORS_ORIGINS = os.getenv("CORS_ORIGINS").split(",")
AUTH_REDIRECT_URL = os.getenv("AUTH_REDIRECT_URL")
AUTHLIB_REDIRECT_AUTH_URL = os.getenv("AUTHLIB_REDIRECT_AUTH_URL")

# DB
MONGO_DB = os.getenv("MONGO_DB")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
# EMAIL CONFIG
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = int(os.getenv("MAIL_PORT"))
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_TLS = True
MAIL_SSL = False
# REDIRECT URLS
VERIFY_USER_URL = os.getenv("VERIFY_USER_URL")
FORGOT_PASSWORD_URL = os.getenv("FORGOT_PASSWORD_URL")
LOGIN_PAGE = os.getenv("LOGIN_PAGE")
# REDIS
REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_DB = os.getenv("REDIS_DB")
REDIS_URI = "redis://:" + REDIS_PASSWORD + "@" + REDIS_HOSTNAME + ":" + REDIS_PORT + "/" + REDIS_DB
# name
MAX_NAME_LENGTH = int(os.getenv("MAX_NAME_LENGTH"))
MIN_NAME_LENGTH = int(os.getenv("MIN_NAME_LENGTH"))
MAX_USERNAME_LENGTH = int(os.getenv("MAX_USERNAME_LENGTH"))
# workspace
MAX_WORKSPACE_NAME_LENGTH = int(os.getenv("MAX_WORKSPACE_NAME_LENGTH"))
MIN_WORKSPACE_NAME_LENGTH = int(os.getenv("MIN_WORKSPACE_NAME_LENGTH"))
MIN_WORKSPACE_ID = int(os.getenv("MIN_WORKSPACE_ID"))
MAX_WORKSPACE_ID = int(os.getenv("MAX_WORKSPACE_ID"))
# notes
MAX_NOTES_NAME_LENGTH = int(os.getenv("MAX_NOTES_NAME_LENGTH"))
MAX_NOTES_ID = int(os.getenv("MAX_NOTES_ID"))
MIN_NOTES_ID = int(os.getenv("MIN_NOTES_ID"))
MAX_NOTE_SIZE = int(os.getenv("MAX_NOTE_SIZE"))
# tags
MAX_TAGS_NAME = int(os.getenv("MAX_TAGS_NAME"))
MAX_TAGS_ID = int(os.getenv("MAX_TAGS_ID"))
MIN_TAGS_ID = int(os.getenv("MIN_TAGS_ID"))
# password
MAX_PASSWORD_LENGTH = int(os.getenv("MAX_PASSWORD_LENGTH"))
MIN_PASSWORD_LENGTH = int(os.getenv("MIN_PASSWORD_LENGTH"))
# Azure blob storage
AZURE_BLOB_STORAGE_NAME = os.getenv('AZURE_BLOB_STORAGE_NAME')
AZURE_BLOB_STORAGE_URL = os.getenv("AZURE_BLOB_STORAGE_URL")
AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
# Image/audio extensions
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
# MAX FILE/NOTE SIZES
MAX_PROFILE_PHOTO_SIZE = int(os.getenv("MAX_PROFILE_PHOTO_SIZE"))
MIN_PROFILE_PHOTO_SIZE = int(os.getenv("MIN_PROFILE_PHOTO_SIZE"))
MAX_FREE_ACCOUNT_USER_SPACE = int(os.getenv("MAX_FREE_ACCOUNT_USER_SPACE"))
MIN_AUDIO_LENGTH = int(os.getenv("MIN_AUDIO_LENGTH"))
MAX_CACHE_TEXT_WORDS = int(os.getenv("MAX_CACHE_TEXT_WORDS"))
MICRO_SERVICES_ACCESS_TOKEN = os.getenv("MICRO_SERVICES_ACCESS_TOKEN")
NOTES_SUMMARY_DIFFERENCE_THRESHOLD = int(os.getenv("NOTES_SUMMARY_DIFFERENCE_THRESHOLD"))
MAX_AUDIO_LENGTH = int(os.getenv("MAX_AUDIO_LENGTH"))
MIN_IMAGE_LENGTH = int(os.getenv("MIN_IMAGE_LENGTH"))
MAX_IMAGE_LENGTH = int(os.getenv("MAX_IMAGE_LENGTH"))
# MAX SUMMARY ENTITY LENGTH
MAX_SUMMARY_ENTITY_LENGTH = int(os.getenv("MAX_SUMMARY_ENTITY_LENGTH"))
TYPESENSE_API_KEY = os.getenv("TYPESENSE_API_KEY")
TYPESENSE_HOST = os.getenv("TYPESENSE_HOST")
TYPESENSE_NOTES_INDEX = os.getenv("TYPESENSE_NOTES_INDEX")
TYPESENSE_IMAGES_INDEX = os.getenv("TYPESENSE_IMAGES_INDEX")
TYPESENSE_AUDIO_INDEX = os.getenv("TYPESENSE_AUDIO_INDEX")

PROJECT_DIR = os.path.dirname(__file__)
IMAGE_RECOG_PROBABILITY_THRESHOLD = float(os.getenv("IMAGE_RECOG_PROBABILITY_THRESHOLD"))

SENTRY_KEY_URL = os.getenv("SENTRY_KEY_URL")
MAIL_GUN_API_KEY = os.getenv("MAIL_GUN_API_KEY")
MAIL_GUN_API_ENDPOINT = os.getenv("MAIL_GUN_API_ENDPOINT")


def sentry_logs_init():
    sentry_sdk.init(
        SENTRY_KEY_URL
    )


active_connections = []


def get_ws_clients():
    return active_connections
