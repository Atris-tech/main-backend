from db_models.models.user_model import UserModel
from fastapi import HTTPException
from error_constants import SPACE_EXHAUSTED
from settings import MAX_NOTE_SIZE, MAX_FREE_ACCOUNT_USER_SPACE
from error_constants import NOTE_SIZE_EXCEEDED


def get_space(user_id):
    user_model_obj = UserModel.objects.get(id=user_id)
    return user_model_obj.space


def check_space(user_model_obj, note_obj=False, new_size_note=False, note_space_check=False, blob_size=False):
    if note_space_check:
        old_size_note = note_obj.note_size
        print("new size of note")
        print(new_size_note)
        print("old size of note")
        print(old_size_note)
        if new_size_note > MAX_NOTE_SIZE:
            raise HTTPException(
                status_code=NOTE_SIZE_EXCEEDED["status_code"],
                detail=NOTE_SIZE_EXCEEDED["detail"]
            )
        difference = new_size_note - old_size_note
        print("difference")
        print(difference)
    else:
        difference = blob_size
        print("difference")
        print(difference)
    if difference < 0:
        print("in if difference")
        print("user_space")
        print(user_model_obj.space)
        user_space = user_model_obj.space + abs(difference)
        if user_model_obj.plan == "Free" and user_space > MAX_FREE_ACCOUNT_USER_SPACE:
            user_model_obj.space = MAX_FREE_ACCOUNT_USER_SPACE
        print("updated user space")
        print(user_space)
        user_model_obj.space = user_space
        user_model_obj.space_occupied = user_model_obj.space_occupied - abs(difference)
        user_model_obj.save()
        note_obj.note_size = new_size_note
    else:
        print("in else")
        print("user_space")
        print(user_model_obj.space)
        user_space = user_model_obj.space - difference
        user_model_obj.space_occupied = user_model_obj.space_occupied + difference
        print("updated user space")
        print(user_space)
        if user_space < 0 and user_model_obj.plan == "Free":
            raise HTTPException(
                status_code=SPACE_EXHAUSTED["status_code"],
                detail=SPACE_EXHAUSTED["detail"]
            )
        elif user_model_obj.space_occupied > user_space and user_model_obj.plan == "Free":
            raise HTTPException(
                status_code=SPACE_EXHAUSTED["status_code"],
                detail=SPACE_EXHAUSTED["detail"]
            )
        else:
            user_model_obj.space = user_space
            user_model_obj.save()
            if not blob_size:
                note_obj.note_size = new_size_note


def increase_quota_space(user_model_obj, to_increase):
    user_model_obj.space = user_model_obj.space + to_increase
    user_model_obj.save()