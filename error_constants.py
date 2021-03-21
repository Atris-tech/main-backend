class UserBanned:
    code = 400
    detail = "user_banned"


class TokenDoesNotExist:
    code = 401
    detail = "token_not_exist"


class RfTokenExpiredInvalid:
    code = 400
    detail = "refresh_token_expired/invalid"


class IncorrectPassword:
    code = 401
    detail = "incorrect_password"


class VerificationError:
    code = 400
    detail = "unverified"


class InvalidEmailError:
    code = 400
    detail = "invalid_email"


class TokenExpired:
    code = 401
    detail = "token expired or invalid"


class UserNameTaken:
    code = 422
    detail = "user name taken"


class EmailIdExists:
    code = 422
    detail = "email already exists"


class EmailAlreadyVerified:
    code = 400
    detail = "email already verified"


class InvalidUserName:
    code = 400
    detail = "invalid_email"


class InvalidFileType:
    code = 415
    detail = "invalid_file_type"


class FileSizeExceeded:
    code = 413
    detail = "file_size_exceeded"


class BadRequest:
    code = 400
    detail = "incorrect or bad request"


class SpaceExhausted:
    code = 422
    detail = "plan storage limit exceeded"


class NoteSizeExceeded:
    code = 422
    detail = "note size exceeded"


class MaxTagsNameExceeded:
    code = 422
    detail = "tag_name should not be more than 15 characters long"


class EntityLengthError:
    def __init__(self, entity, your_length=False, length=False, min_length=False, empty=False):
        self.code = 422
        if min_length:
            length_violation = "min_length"
        elif empty:
            length_violation = "empty_field"
        else:
            length_violation = "max_length"
        error_data = {
            "entity": entity,
            "length_violation": length_violation,
        }
        if not empty:
            error_data["length"] = length
            error_data["param_length"] = your_length
        self.detail = error_data
