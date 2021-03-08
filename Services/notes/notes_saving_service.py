from db_models.models.notes_model import NotesModel
from db_models.models.workspace_model import WorkSpaceModel
from fastapi import HTTPException
import error_constants
from mongoengine.queryset.visitor import Q
from db_models.models.user_model import UserModel
from Services.notes.notes_parsing_service import html_to_text


def check_notes(note_id, email):
    try:
        user_obj = UserModel.objects.get(email_id=email)
        notes_obj = NotesModel.objects.get(Q(user_id=user_obj) & Q(id=note_id))
        return notes_obj
    except (UserModel.DoesNotExist, NotesModel.DoesNotExist):
        raise HTTPException(
            status_code=error_constants.BAD_REQUEST["status_code"],
            detail=error_constants.BAD_REQUEST["detail"]
        )


def check_user_workspace(workspace_id, email):
    try:
        user_obj = UserModel.objects.get(email_id=email)
        workspace_obj = WorkSpaceModel.objects.get(Q(user_id=user_obj) & Q(id=workspace_id))
        print("in check user_manage")
        print(workspace_obj)
        return {"user_obj": user_obj, "workspace_obj": workspace_obj}
    except (UserModel.DoesNotExist, WorkSpaceModel.DoesNotExist):
        raise HTTPException(
            status_code=error_constants.INVALID_EMAIL["status_code"],
            detail=error_constants.INVALID_EMAIL["detail"]
        )


def new_notes(user_dict, work_space_id, notes_name, to_save_data):
    workspace_data = check_user_workspace(work_space_id, user_dict["email_id"])
    notes_model_obj = NotesModel()
    print("###################################################")
    print(workspace_data["workspace_obj"])
    notes_model_obj.workspace_id = workspace_data["workspace_obj"]
    notes_model_obj.user_id = workspace_data["user_obj"]
    notes_model_obj.work_space_name = notes_name
    notes_model_obj.data = to_save_data
    clean_txt = html_to_text(to_save_data)
    notes_model_obj.clean_text = clean_txt
    notes_model_obj.save()
    return str(notes_model_obj.id)


def rename_notes(notes_id, new_notes_name, email):
    notes_model_object = check_notes(notes_id, email)
    notes_model_object.update(notes_name=new_notes_name)
    return True


def delete_notes(notes_id, email):
    notes_model_obj = check_notes(notes_id, email)
    notes_model_obj.delete()
    return True
