import base64
import json
import uuid

from fastapi import HTTPException
from mongoengine.queryset.visitor import Q

import error_constants
from Services.audios.delete_audio_service import delete_audios, delete_single_storage_object
from Services.audios.get_audio_data import get_all_audio_data
from Services.notes.generate_notes_difference import compare
from Services.notes.notes_parsing_service import html_to_text
from Services.plan_helper import check_space
from Services.storage_services import StorageServices
from Services.type_sense.type_sense_crud_service import get_collection, update_collection, delete_collection, \
    create_collection
from Services.type_sense.typesense_dic_generator import generate_typsns_data
from db_models.models.cache_display_model import CacheModel
from db_models.models.images_model import Image
from db_models.models.notes_model import NotesModel
from db_models.models.scribbles_model import Scribbles
from db_models.models.user_model import UserModel
from db_models.models.workspace_model import WorkSpaceModel
from db_models.models.tags_model import TagModel
from settings import MAX_CACHE_TEXT_WORDS
from settings import TYPESENSE_NOTES_INDEX


def generate_summary_from_clean_text(clean_txt):
    clean_txt_list = clean_txt.split()
    if len(clean_txt_list) < MAX_CACHE_TEXT_WORDS:
        summary = clean_txt
    else:
        clean_txt_list = clean_txt_list[:MAX_CACHE_TEXT_WORDS]
        cache_notes_text = ' '.join(word for word in clean_txt_list)
        summary = cache_notes_text
    return summary


def handle_clean_text(notes_obj, old_clean_text, new_clean_text, summary):
    difference = compare(str1=old_clean_text, str2=new_clean_text)
    notes_obj.difference = difference
    notes_obj.save()
    typesense_data = generate_typsns_data(notes_name=notes_obj.notes_name, summary=summary,
                                          clean_text=new_clean_text, obj=notes_obj)
    update_collection(data=typesense_data, index=TYPESENSE_NOTES_INDEX)


def check_notes(note_id, email, get_user=False):
    try:
        user_obj = UserModel.objects.get(email_id=email)
        notes_obj = NotesModel.objects.get(Q(user_id=user_obj) & Q(id=note_id))
        if get_user:
            return {"notes_obj": notes_obj, "user_obj": user_obj}
        return notes_obj
    except (UserModel.DoesNotExist, NotesModel.DoesNotExist):
        raise HTTPException(
            status_code=error_constants.BadRequest.code,
            detail=error_constants.BadRequest.detail
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
            status_code=error_constants.BadRequest.code,
            detail=error_constants.BadRequest.detail
        )


def new_note(user_dict, work_space_id, notes_name=False, return_notes_obj=False):
    workspace_data = check_user_workspace(work_space_id, user_dict["email_id"])
    notes_model_obj = NotesModel()
    print("###################################################")
    print(workspace_data["workspace_obj"])
    notes_model_obj.workspace_id = workspace_data["workspace_obj"]
    notes_model_obj.user_id = workspace_data["user_obj"]
    notes_model_obj.notes_name = notes_name
    notes_model_obj.note_blob_id = str(uuid.uuid4())
    notes_model_obj.save()
    tp_data = generate_typsns_data(obj=notes_model_obj, notes_name=notes_model_obj.notes_name, summary="",
                                   clean_text="")
    create_collection(index=TYPESENSE_NOTES_INDEX, data=tp_data)
    cache_model_obj = CacheModel()
    cache_model_obj.notes_name = notes_name
    cache_model_obj.notes_id = notes_model_obj
    cache_model_obj.user_id = workspace_data["user_obj"]
    cache_model_obj.workspace_id = workspace_data["workspace_obj"]
    cache_model_obj.save()
    if return_notes_obj:
        return notes_model_obj
    else:
        return str(notes_model_obj.id)


def save_note(user_dict, work_space_id, to_save_data, notes_id=False):
    workspace_data = check_user_workspace(work_space_id, user_dict["email_id"])
    notes_model_obj = check_notes(note_id=notes_id, email=user_dict["email_id"])
    check_space(user_model_obj=workspace_data["user_obj"], note_obj=notes_model_obj,
                new_size_note=len(to_save_data), note_space_check=True)
    StorageServices().upload_file_blob_storage(file_data=to_save_data,
                                               container_name=workspace_data[
                                                   "user_obj"].user_storage_notes_container_name,
                                               user_model_obj=workspace_data["user_obj"],
                                               file_name=notes_model_obj.note_blob_id,
                                               save_note=True)
    clean_txt = html_to_text(to_save_data)
    clean_text_data = get_collection(index=TYPESENSE_NOTES_INDEX, id=str(notes_model_obj.id))
    cache_model_obj = CacheModel.objects.get(notes_id=notes_model_obj)
    if clean_text_data is not None:
        summary = clean_txt
        old_clean_text = clean_text_data["clean_text"]
    else:
        # first time saving note
        old_clean_text = ""
        summary = generate_summary_from_clean_text(clean_txt)
    if cache_model_obj.uds == "False":
        cache_notes_summary = generate_summary_from_clean_text(clean_txt)
        cache_model_obj.cache_notes_summary = cache_notes_summary
    cache_model_obj.save()
    handle_clean_text(notes_model_obj, new_clean_text=clean_txt, old_clean_text=old_clean_text,
                      summary=summary)
    return str(notes_model_obj.id)


def rename_notes(notes_id, new_notes_name, email):
    notes_model_object = check_notes(notes_id, email)
    data = get_collection(index=TYPESENSE_NOTES_INDEX, id=str(notes_model_object.id))
    if data is not None:
        tp_data = generate_typsns_data(obj=notes_model_object, notes_name=new_notes_name, summary=data["summary"],
                                       clean_text=data["clean_text"])
        update_collection(index=TYPESENSE_NOTES_INDEX, data=tp_data)
    notes_model_object.update(notes_name=new_notes_name)
    return True


def delete_notes(notes_id, email):
    check_notes_data = check_notes(notes_id, email, get_user=True)
    notes_obj = check_space(user_model_obj=check_notes_data["user_obj"], note_obj=check_notes_data["notes_obj"],
                            new_size_note=0, note_space_check=True)
    delete_collection(index=TYPESENSE_NOTES_INDEX, collections_id=str(notes_id))
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
    delete_audios(notes_obj,
                  check_notes_data["user_obj"].user_storage_container_name)
    """DELETE IMAGES"""
    image_objs = Image.objects.filter(notes_id=notes_obj)
    for image_obj in image_objs:
        delete_single_storage_object(obj=image_obj,
                                     container_name=check_notes_data["user_obj"].user_storage_container_name)
    """DELETE DRAWINGS"""
    scrible_objs = Scribbles.objects.filter(note_id=notes_obj)
    for scrible_obj in scrible_objs:
        delete_single_storage_object(obj=scrible_obj,
                                     container_name=check_notes_data["user_obj"].user_storage_container_name,
                                     tps_del=False)
    notes_container_name = check_notes_data["user_obj"].user_storage_notes_container_name
    if notes_container_name is not None:
        StorageServices().delete_blob(container_name=notes_container_name,
                                      blob_name=check_notes_data["notes_obj"].note_blob_id)
    notes_obj.delete()
    return True


def get_notes_data(user_dict, note_id):
    to_send_data = dict()
    user_object_model = UserModel.objects.get(email_id=user_dict["email_id"])
    try:
        notes_model_obj = NotesModel.objects.get(Q(id=note_id) & Q(user_id=user_object_model))
        notes_container_name = user_object_model.user_storage_notes_container_name
        notes_dict = json.loads(notes_model_obj.to_json())
        if notes_container_name is not None:
            notes_raw = StorageServices().download_blob(
                container_name=user_object_model.user_storage_notes_container_name,
                blob_id=notes_model_obj.note_blob_id)
            if notes_raw is not None:
                to_send_data["notes_data"] = base64.b64encode(notes_raw)
            else:
                to_send_data["notes_data"] = None
        else:
            to_send_data["notes_data"] = None
        to_send_data["tags_id"] = notes_dict["tags"]
        to_send_data["tags_name"] = notes_dict["tags_name"]
        if "summary_data" in notes_dict:
            to_send_data["notes_summary"] = notes_dict["summary_data"]
        to_send_data["entity_data"] = notes_dict["entity_data"]
        to_send_data["last_edited_date"] = notes_dict["last_edited_date"]
        to_send_data["notes_name"] = notes_dict["notes_name"]
        if notes_dict["uds"] == "AUTO":
            to_send_data["summary"] = notes_dict["summary"]
        elif notes_dict["uds"] == "MANUAL":
            data = get_collection(index=TYPESENSE_NOTES_INDEX, id=note_id)
            if data is not None:
                to_send_data["summary"] = data["summary"]
            else:
                to_send_data["summary"] = None
        else:
            to_send_data["summary"] = None
        if "emotion" in notes_dict:
            to_send_data["emotion"] = notes_dict["emotion"]
        else:
            to_send_data["emotion"] = None
        to_send_data["audios"] = get_all_audio_data(notes_model_obj, user_dict["email_id"])
        scribbles = list()
        for scribble_obj in Scribbles.objects.filter(note_id=note_id):
            scribbles.append(
                {
                    "id": str(scribble_obj.id),
                    "name": scribble_obj.name,
                    "y_axis": scribble_obj.y_axis
                }
            )
        to_send_data["scribbles"] = scribbles
        return to_send_data
    except NotesModel.DoesNotExist:
        raise HTTPException(
            status_code=error_constants.BadRequest.code,
            detail=error_constants.BadRequest.detail
        )


def duplicate_notes(user_dict, workspace_id, old_note_id):
    user_object_model = UserModel.objects.get(email_id=user_dict["email_id"])
    old_notes_obj = NotesModel.objects.get(Q(id=old_note_id) & Q(user_id=user_object_model))
    new_notes_obj = new_note(user_dict, workspace_id, notes_name=old_notes_obj.notes_name + "(Copy)",
                             return_notes_obj=True)
    notes_raw = StorageServices().download_blob(
        container_name=user_object_model.user_storage_notes_container_name,
        blob_id=old_notes_obj.note_blob_id)
    return save_note(user_dict, work_space_id=workspace_id, to_save_data=notes_raw, notes_id=new_notes_obj.id)


def move_notes(user_dict, notes_id, old_workspace_id,  new_workspace_id):
    check_workspace_dic = check_user_workspace(old_workspace_id, email=user_dict["email_id"])
    user_obj = check_workspace_dic["user_obj"]
    old_workspace_obj = check_workspace_dic["workspace_obj"]
    notes_obj = NotesModel.objects.get(Q(user_id=user_obj) & Q(id=notes_id) & Q(workspace_id=old_workspace_obj))
    check_workspace_dic = check_user_workspace(new_workspace_id, email=user_dict["email_id"])
    new_workspace_obj = check_workspace_dic["workspace_obj"]
    notes_obj.workspace_id = notes_obj.update(workspace_id=new_workspace_obj)
    CacheModel.objects.get(notes_id=notes_obj).update(workspace_id=new_workspace_obj)
    return True
