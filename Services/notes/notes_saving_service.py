from db_models.models.cache_display_model import CacheModel
from db_models.models.notes_model import NotesModel
from db_models.models.workspace_model import WorkSpaceModel
from fastapi import HTTPException
import error_constants
from mongoengine.queryset.visitor import Q
from db_models.models.user_model import UserModel
from Services.notes.notes_parsing_service import html_to_text
from Services.storage_services import upload_file_blob_storage, delete_blob
from Services.plan_helper import check_space
import uuid
from settings import MAX_CACHE_TEXT_WORDS


def check_notes(note_id, email, get_user=False):
    try:
        user_obj = UserModel.objects.get(email_id=email)
        notes_obj = NotesModel.objects.get(Q(user_id=user_obj) & Q(id=note_id))
        if get_user:
            return {"notes_obj": notes_obj, "user_obj": user_obj}
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
            status_code=error_constants.BAD_REQUEST["status_code"],
            detail=error_constants.BAD_REQUEST["detail"]
        )


def new_note(user_dict, work_space_id, notes_name=False):
    workspace_data = check_user_workspace(work_space_id, user_dict["email_id"])
    notes_model_obj = NotesModel()
    print("###################################################")
    print(workspace_data["workspace_obj"])
    notes_model_obj.workspace_id = workspace_data["workspace_obj"]
    notes_model_obj.user_id = workspace_data["user_obj"]
    notes_model_obj.notes_name = notes_name
    notes_model_obj.note_blob_id = str(uuid.uuid4())
    notes_model_obj.save()
    cache_model_obj = CacheModel()
    cache_model_obj.notes_name = notes_name
    cache_model_obj.notes_id = notes_model_obj
    cache_model_obj.user_id = workspace_data["user_obj"]
    cache_model_obj.workspace_id = workspace_data["workspace_obj"]
    cache_model_obj.save()
    return str(notes_model_obj.id)


def save_note(user_dict, work_space_id, to_save_data, notes_id=False):
    workspace_data = check_user_workspace(work_space_id, user_dict["email_id"])
    notes_model_obj = NotesModel.objects.get(Q(id=notes_id) & Q(workspace_id=workspace_data["workspace_obj"]))
    check_space(user_model_obj=workspace_data["user_obj"], note_obj=notes_model_obj,
                new_size_note=len(to_save_data), note_space_check=True)
    upload_file_blob_storage(file_data=to_save_data,
                             container_name=workspace_data["user_obj"].user_storage_notes_container_name,
                             user_model_obj=workspace_data["user_obj"], file_name=notes_model_obj.note_blob_id,
                             save_note=True)
    clean_txt = html_to_text(to_save_data)
    notes_model_obj.clean_text = clean_txt
    notes_model_obj.save()
    cache_model_obj = CacheModel.objects.get(notes_id=notes_model_obj)
    clean_txt_list = clean_txt.split()
    if len(clean_txt_list) < MAX_CACHE_TEXT_WORDS:
        cache_model_obj.cache_notes_summary = clean_txt
    else:
        clean_txt_list = clean_txt_list[:MAX_CACHE_TEXT_WORDS]
        cache_notes_text = ' '.join(word for word in clean_txt_list)
        cache_model_obj.cache_notes_summary = cache_notes_text
    cache_model_obj.save()
    return str(notes_model_obj.id)


def rename_notes(notes_id, new_notes_name, email):
    notes_model_object = check_notes(notes_id, email)
    notes_model_object.update(notes_name=new_notes_name)
    return True


def delete_notes(notes_id, email):
    check_notes_data = check_notes(notes_id, email, get_user=True)
    check_space(user_model_obj=check_notes_data["user_obj"], note_obj=check_notes_data["notes_obj"],
                new_size_note=0, note_space_check=True)

    """DELETE ALL TAGS AND CATCH FROM HERE"""
    catch_obj = CacheModel.objects.get(notes_id=notes_id)
    print("here 1")
    for tag_obj in catch_obj.tags:
        tag_obj.notes.remove(catch_obj)
        tag_obj.count -= 1
        if tag_obj.count == 0:
            tag_obj.delete()
        else:
            tag_obj.save()
    catch_obj.delete()
    check_notes_data["notes_obj"].delete()
    delete_blob(container_name=check_notes_data["user_obj"].user_storage_notes_container_name,
                blob_name=check_notes_data["notes_obj"].note_blob_id)
