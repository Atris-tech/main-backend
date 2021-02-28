from db_models.models.user_model import UserModel
from fastapi import HTTPException
from error_constants import SPACE_EXHAUSTED


def get_space(user_id):
    user_model_obj = UserModel.objects.get(id=user_id)
    return user_model_obj.space


def check_space(user_model_obj, note_obj=False, new_size_note=False, note_space_check=False, blob_size=False):
    if note_space_check:
        old_size_note = note_obj.note_size
        difference = new_size_note - old_size_note
    else:
        difference = blob_size
    if difference < 0:
        user_space = user_model_obj.space + difference
        user_model_obj.space = user_space
        user_model_obj.save()
        note_obj.note_size = new_size_note
        note_obj.save()
    else:
        user_space = user_model_obj.space - difference
        if user_space < 0:
            raise HTTPException(
                status_code=SPACE_EXHAUSTED["status_code"],
                detail=SPACE_EXHAUSTED["detail"]
            )
        else:
            user_model_obj.space = user_space
            user_model_obj.save()
            if not blob_size:
                note_obj.note_size = new_size_note
                note_obj.save()


def increase_quota_space(user_model_obj, to_increase):
    user_model_obj.space = user_model_obj.space + to_increase
    user_model_obj.save()