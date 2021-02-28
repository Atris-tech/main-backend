from db_models.models.notes_model import NotesModel
from db_models.models.workspace_model import WorkSpaceModel
from fastapi import HTTPException
import error_constants
from error_constants import BAD_REQUEST
from mongoengine.queryset.visitor import Q
from db_models.models.user_model import UserModel
from Services.notes.notes_parsing_service import html_to_text


def check_notes(name):
    try:
        NotesModel.objects.get(notes_name=name)
        return True
    except NotesModel.DoesNotExist:
        return False


def check_user_workspace(workspace_name, email):
    try:
        user_obj = UserModel.objects.get(email_id=email)
        WorkSpaceModel.objects(Q(user_id=user_obj) & Q(work_space_name=workspace_name))
        return True
    except UserModel.DoesNotExist:
        raise HTTPException(
            status_code=error_constants.INVALID_EMAIL["status_code"],
            detail=error_constants.INVALID_EMAIL["detail"]
        )


def new_notes(user_dict, name, data, email):
    check_user_workspace(name, email)
    print(user_dict["email_id"])
    user_object_model = UserModel.objects.get(email_id=user_dict["email_id"])
    notes_model_obj = NotesModel()
    notes_model_obj.user_id = user_object_model
    notes_model_obj.work_space_name = name
    notes_model_obj.data = data
    clean_txt = html_to_text(data)
    notes_model_obj.clean_text = clean_txt
    notes_model_obj.save()
    return True


def rename_notes(old_notes_name, new_notes_name=False):
    try:
        notes_model_object = NotesModel.objects.get(notes_name=old_notes_name)
        if new_notes_name:
            notes_model_object.update(notes_name=new_notes_name)
        return True
    except NotesModel.DoesNotExist:
        raise HTTPException(
            status_code=BAD_REQUEST["status_code"],
            detail=BAD_REQUEST["detail"]
        )


def delete_notes(notes_name):
    try:
        notes_model_obj = NotesModel.objects.get(notes_name=notes_name)
        notes_model_obj.delete()
        return True
    except NotesModel.DoesNotExist:
        raise HTTPException(
            status_code=BAD_REQUEST["status_code"],
            detail=BAD_REQUEST["detail"]
        )
