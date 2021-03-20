USER_BANNED = {
    "status_code": 400,
    "detail": "user_banned"
}
TOKEN_NOT_EXIST = {
    "status_code": 401,
    "detail": "token_not_exist"
}
RF_TOKEN_EXPIRED_INVALID = {
    "status_code": 400,
    "detail": "refresh_token_expired/invalid"
}
INCORRECT_PASSWORD = {
    "status_code": 401,
    "detail": "incorrect_password"
}
VERIFICATION_ERROR = {
    "status_code": 400,
    "detail": "unverified"
}
INVALID_EMAIL = {
    "status_code": 400,
    "detail": "invalid_email"
}
TOKEN_EXPIRED = {
    "status_code": 401,
    "detail": "token expired or invalid"
}
USER_NAME_TAKEN = {
    "status_code": 422,
    "detail": "user name taken"
}
EMAIL_ID_EXISTS = {
    "status_code": 422,
    "detail": "email already exists"
}
EMAIL_ALREADY_VERIFIED = {
    "status_code": 400,
    "detail": "email already verified"
}
INVALID_USER_NAME = {
    "status_code": 400,
    "detail": "invalid_email"
}
INVALID_FILE_TYPE = {
    "status_code": 415,
    "detail": "invalid_file_type"
}
FILE_SIZE_EXCEEDED = {
    "status_code": 413,
    "detail": "file_size_exceeded"
}
BAD_REQUEST = {
    "status_code": 400,
    "detail": "incorrect or bad request"
}
SPACE_EXHAUSTED = {
    "status_code": 422,
    "detail": "plan storage limit exceeded"
}
NOTE_SIZE_EXCEEDED = {
    "status_code": 422,
    "detail": "note size exceeded"
}
MAX_TAGS_NAME_EXCEEDED = {
    "status_code": 422,
    "detail": "tag_name should not be more than 15 characters long"
}