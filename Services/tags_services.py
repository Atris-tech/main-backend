from fastapi import HTTPException
from icecream import ic
from mongoengine.queryset.visitor import Q

import error_constants
from Services.auth.auth_services import check_user
from db_models.models.cache_display_model import CacheModel
from db_models.models.notes_model import NotesModel
from db_models.models.tags_model import TagModel
from db_models.models.workspace_model import WorkSpaceModel
from error_constants import BadRequest


def add_tag(name, user_obj):
    try:
        tag_obj = TagModel.objects.get(Q(user_id=user_obj) & Q(tag_name=name))
        ic()
        ic(tag_obj.notes)
        return tag_obj
    except TagModel.DoesNotExist:
        tag_obj = TagModel(user_id=user_obj, tag_name=name)
        return tag_obj


def check_user_notes(notes_id, user_obj, workspace_obj):
    try:
        note_obj = NotesModel.objects.get(
            Q(user_id=user_obj) & Q(id=notes_id) & Q(workspace_id=workspace_obj))
        ic()
        ic(note_obj)
        return note_obj
    except NotesModel.DoesNotExist:
        raise HTTPException(
            status_code=error_constants.BadRequest.code,
            detail=error_constants.BadRequest.detail
        )


def add_tag_catch(user_obj, tag_obj, notes_obj, workspace_obj):
    try:
        cache_model_obj = CacheModel.objects.get(Q(user_id=user_obj) & Q(notes_id=notes_obj))
        if tag_obj not in cache_model_obj.tags:
            cache_model_obj.tags.append(tag_obj)
            cache_model_obj.tags_name.append(tag_obj.tag_name)
        cache_model_obj.save()
        return cache_model_obj
    except CacheModel.DoesNotExist:
        cache_model_obj = CacheModel(
            notes_name=notes_obj.notes_name,
            user_id=user_obj,
            workspace_id=workspace_obj,
            notes_id=notes_obj
        )
        if tag_obj not in cache_model_obj.tags:
            cache_model_obj.tags.append(tag_obj)
        cache_model_obj.save()
        return cache_model_obj


def create_new_tag(email, tag_name, notes_id, workspace_id):
    user_obj = check_user(email=email)
    if not user_obj:
        raise HTTPException(
            status_code=error_constants.TokenDoesNotExist.code,
            detail=error_constants.TokenDoesNotExist.detail
        )
    try:
        workspace_obj = WorkSpaceModel.objects.get(Q(user_id=user_obj) & Q(id=workspace_id))
    except WorkSpaceModel.DoesNotExist:
        print("%%%%%%%%%%")
        raise HTTPException(
            status_code=error_constants.BadRequest.code,
            detail=error_constants.BadRequest.detail
        )
    note_obj = check_user_notes(notes_id=notes_id, user_obj=user_obj, workspace_obj=workspace_obj)
    ic()
    ic(note_obj)
    ic(note_obj.tags)
    tag_obj = add_tag(name=tag_name, user_obj=user_obj)
    tag_obj.save()
    cache_model_obj = add_tag_catch(user_obj, tag_obj, note_obj, workspace_obj)
    if cache_model_obj not in tag_obj.notes:
        tag_obj.notes.append(cache_model_obj)
        tag_obj.save()
    if tag_obj not in note_obj.tags:
        print("in not note_obj")
        tag_obj.count = tag_obj.count + 1
        tag_obj.save()
        note_obj.tags.append(tag_obj)
        note_obj.tags_name.append(tag_obj.tag_name)
        note_obj.save()
    return str(tag_obj.id)


def remove_tag(tag_id, notes_id, email):
    user_obj = check_user(email=email)
    if not user_obj:
        raise HTTPException(
            status_code=error_constants.InvalidEmailError.code,
            detail=error_constants.InvalidEmailError.detail
        )
    try:
        note_obj = NotesModel.objects.get(Q(user_id=user_obj) & Q(id=notes_id))
        tag_obj = TagModel.objects.get(Q(user_id=user_obj) & Q(id=tag_id))
        note_obj.tags.remove(tag_obj)
        note_obj.save()
        catch_model_obj = CacheModel.objects.get(notes_id=note_obj)
        catch_model_obj.tags.remove(tag_obj)
        catch_model_obj.tags_name.remove(tag_obj.tag_name)
        catch_model_obj.save()
        tag_obj.notes.remove(catch_model_obj)
        tag_obj.count -= 1
        if tag_obj.count == 0:
            tag_obj.delete()
        else:
            tag_obj.save()
        return True
    except (TagModel.DoesNotExist, NotesModel.DoesNotExist, ValueError):
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )


def recommend_tag(tag_query_name, email):
    user_obj = check_user(email=email)
    if not user_obj:
        raise HTTPException(
            status_code=error_constants.InvalidEmailError.code,
            detail=error_constants.InvalidEmailError.detail
        )
    try:
        tag_objs = TagModel.objects.filter(Q(user_id=user_obj) & Q(tag_name__istartswith=tag_query_name))
        resp = list()
        for tag_obj in tag_objs:
            resp.append({
                "tag_id": str(tag_obj.id),
                "tag_name": tag_obj.tag_name
            })
        return resp
    except TagModel.DoesNotExist:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )
