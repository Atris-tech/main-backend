from db_models.models.user_model import UserModel
from db_models.models.token_model import TokenModel
from Services.redis_service import set_val


def ban_user(email):
    user_obj = UserModel.objects.get(email_id=email)
    token_obj = TokenModel.objects.get(user=user_obj)
    token_obj.token_status = "Dead"
    token_obj.save()
    ref_token = token_obj.refresh_token
    if ref_token is not None:
        set_val(ref_token, {"banned": True}, json_type=True)


def unban_user(email):
    user_obj = UserModel.objects.get(email_id=email)
    token_obj = TokenModel.objects.get(user=user_obj)
    token_obj.token_status = "Alive"
    token_obj.save()
    ref_token = token_obj.refresh_token
    if ref_token is not None:
        set_val(ref_token, None, json_type=True)