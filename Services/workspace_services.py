from db_models.models.workspace_model import WorkSpaceModel
from db_models.models.user_model import UserModel
from fastapi import HTTPException
from error_constants import BadRequest
import emoji
from mongoengine.queryset.visitor import Q
from db_models.models.cache_display_model import CacheModel
import json


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
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )


def check_emoji(string):
    emoji_dict = emoji.emoji_lis(string)
    if len(emoji_dict) == 0:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )
    elif len(emoji_dict) > 1:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )
    if emoji_dict[0]["emoji"] != string:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )


def new_workspace(user_dict, name, emoji):
    check_emoji(emoji)
    user_object_model = UserModel.objects.get(email_id=user_dict["email_id"])
    if check_workspace(name = name, user_obj=user_object_model, create_check=True):
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
    workspace_model_obj.delete()
    return True


def display_all_caches(workspace_id, user_dict):
    user_object_model = UserModel.objects.get(email_id=user_dict["email_id"])
    try:
        cache_model_objs = CacheModel.objects.filter(Q(user_id=user_object_model) & Q(workspace_id=workspace_id))
        return json.loads(cache_model_objs.to_json())
    except CacheModel.DoesNotExist:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )
