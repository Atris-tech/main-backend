import json

import emoji
from fastapi import HTTPException
from mongoengine.queryset.visitor import Q

from Services.notes.notes_saving_service import delete_notes
from db_models.models import NotesModel
from db_models.models.bookmark_model import BookMarkModel
from db_models.models.cache_display_model import CacheModel
from db_models.models.user_model import UserModel
from db_models.models.workspace_model import WorkSpaceModel
from error_constants import BadRequest, WorkspaceExist


def check_workspace(user_obj, id=False, name=False, create_check=False):
    try:
        if name:
            workspace_obj = WorkSpaceModel.objects.get(Q(user_id=user_obj) & Q(work_space_name=name))
        else:
            workspace_obj = WorkSpaceModel.objects.get(Q(user_id=user_obj) & Q(id=id))
        return workspace_obj
    except WorkSpaceModel.DoesNotExist:
        if create_check:
            return False
        else:
            raise HTTPException(
                status_code=WorkspaceExist.code,
                detail=WorkspaceExist.detail
            )


def check_emoji(string):
    demojized_string = emoji.demojize(string)
    print(string)
    print(type(string))
    emoji_dict = emoji.emoji_lis(string)
    print("emoji dict")
    print(emoji_dict)
    if len(emoji_dict) == 0:
        print("emoji length 0")
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )
    elif len(emoji_dict) > 1:
        print("emoji length > 1")
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )
    valid_emoji_found = emoji_dict[0]["emoji"]
    demojized_valid_emoji = emoji.demojize(valid_emoji_found)
    if demojized_valid_emoji != demojized_string:
        print("bad emoji")
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )


def new_workspace(user_dict, name, emoji):
    check_emoji(emoji)
    user_object_model = UserModel.objects.get(email_id=user_dict["email_id"])
    if check_workspace(name=name, user_obj=user_object_model, create_check=True):
        raise HTTPException(
            status_code=200,
            detail="workspace exists"
        )
    else:
        print(user_dict["email_id"])
        workspace_model_obj = WorkSpaceModel()
        workspace_model_obj.user_id = user_object_model
        workspace_model_obj.work_space_name = name
        workspace_model_obj.work_space_emoji = emoji
        workspace_model_obj.save()
        return str(workspace_model_obj.id)


def rename_workspace(user_dict, old_workspace_name, new_workspace_name=False, emoji=False):
    if emoji:
        check_emoji(emoji)
    print("emoji here")
    user_object_model = UserModel.objects.get(email_id=user_dict["email_id"])
    workspace_model_object = check_workspace(name=old_workspace_name, user_obj=user_object_model)
    if new_workspace_name:
        workspace_model_object.update(work_space_name=new_workspace_name)
    if emoji:
        workspace_model_object.update(work_space_emoji=emoji)
    if not emoji and not new_workspace_name:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )
    return True


def delete_workspace(workspace_id, user_dict):
    user_object_model = UserModel.objects.get(email_id=user_dict["email_id"])
    workspace_model_obj = check_workspace(id=workspace_id, user_obj=user_object_model)
    notes_objs = NotesModel.objects.filter(workspace_id=workspace_model_obj)
    for notes_obj in notes_objs:
        delete_notes(notes_obj.id, user_dict["email_id"])
    workspace_model_obj.delete()
    return True


def display_all_caches(workspace_id, user_dict):
    user_object_model = UserModel.objects.get(email_id=user_dict["email_id"])
    try:
        data = list()
        cache_model_objs = CacheModel.objects.filter(Q(user_id=user_object_model) & Q(workspace_id=workspace_id))
        for cache_model_obj in cache_model_objs:
            cache_data = json.loads(cache_model_obj.to_json())
            try:
                BookMarkModel.objects.get(cache_id=cache_model_obj)
                cache_data["bookmark"] = True
            except BookMarkModel.DoesNotExist:
                cache_data["bookmark"] = False
            data.append(cache_data)
        return data
    except CacheModel.DoesNotExist:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )


def generate_obj_json_list(obj_list):
    cache_notes = list()
    for model_obj in obj_list:
        cache_notes.append(json.loads(model_obj.cache_id.to_json()))
    return cache_notes


def display_book_mark_notes(user_dict):
    user_object_model = UserModel.objects.get(email_id=user_dict["email_id"])
    try:
        book_mark_note_objs = BookMarkModel.objects.filter(user_id=user_object_model)
        return generate_obj_json_list(book_mark_note_objs)
    except CacheModel.DoesNotExist:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )


def get_cache_object(user_dict, notes_id):
    user_object_model = UserModel.objects.get(email_id=user_dict["email_id"])
    try:
        cache_model_obj = CacheModel.objects.get(Q(user_id=user_object_model) & Q(notes_id=notes_id))
        return cache_model_obj
    except CacheModel.DoesNotExist:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )


def star_notes(user_dict, notes_id):
    cache_model_obj = get_cache_object(user_dict, notes_id)
    if not cache_model_obj.star:
        cache_model_obj.update(star=True)
        return True
    else:
        return False


def unstar(user_dict, notes_id):
    cache_model_obj = get_cache_object(user_dict, notes_id)
    if cache_model_obj.star:
        cache_model_obj.update(star=False)
        return True
    else:
        return False


def un_bookmark(user_dict, notes_id):
    cache_model_obj = get_cache_object(user_dict, notes_id)
    try:
        book_mark_obj = BookMarkModel.objects.get(cache_id=cache_model_obj)
        book_mark_obj.delete()
        return True
    except BookMarkModel.DoesNotExist:
        return False


def book_mark_note(user_dict, notes_id):
    user_object_model = UserModel.objects.get(email_id=user_dict["email_id"])
    try:
        cache_model_obj = CacheModel.objects.get(Q(user_id=user_object_model) & Q(notes_id=notes_id))
        try:
            print("in try")
            BookMarkModel.objects.get(cache_id=cache_model_obj)
            return False
        except BookMarkModel.DoesNotExist:
            print("in except")
            BookMarkModel(user_id=user_object_model, cache_id=cache_model_obj).save()
            return True
    except CacheModel.DoesNotExist:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )


def get_book_mark_notes(user_dict):
    try:
        user_object_model = UserModel.objects.get(email_id=user_dict["email_id"])
        book_mark_notes_objs = BookMarkModel.objects.filter(user_id=user_object_model)
        data = list()
        for obj in book_mark_notes_objs:
            cache_obj = obj.cache_id
            data.append(json.loads(cache_obj.to_json()))
        return data
    except BookMarkModel.DoesNotExist:
        return None
