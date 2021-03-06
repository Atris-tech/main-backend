from db_models.models.workspace_model import WorkSpaceModel
from db_models.models.user_model import UserModel
from fastapi import HTTPException
from error_constants import BAD_REQUEST
import emoji


def check_workspace(name):
    try:
        WorkSpaceModel.objects.get(work_space_name=name)
        return True
    except WorkSpaceModel.DoesNotExist:
        return False


def check_emoji(string):
    emoji_dict = emoji.emoji_lis(string)
    if len(emoji_dict) == 0:
        raise HTTPException(
            status_code=BAD_REQUEST["status_code"],
            detail=BAD_REQUEST["detail"]
        )
    elif len(emoji_dict) > 1:
        raise HTTPException(
            status_code=BAD_REQUEST["status_code"],
            detail=BAD_REQUEST["detail"]
        )
    if emoji_dict[0]["emoji"] != string:
        raise HTTPException(
            status_code=BAD_REQUEST["status_code"],
            detail=BAD_REQUEST["detail"]
        )


def new_workspace(user_dict, name, emoji):
    check_emoji(emoji)
    if check_workspace(name):
        raise HTTPException(
            status_code=200,
            detail="workspace exists"
        )
    else:
        print(user_dict["email_id"])
        user_object_model = UserModel.objects.get(email_id=user_dict["email_id"])
        workspace_model_obj = WorkSpaceModel()
        workspace_model_obj.user_id = user_object_model
        workspace_model_obj.work_space_name = name
        workspace_model_obj.work_space_emoji = emoji
        workspace_model_obj.save()
        return str(workspace_model_obj.id)


def rename_workspace(old_workspace_name, new_workspace_name=False, emoji=False):
    check_emoji(emoji)
    print("emoji here")
    try:
        workspace_model_object = WorkSpaceModel.objects.get(work_space_name=old_workspace_name)
        if new_workspace_name:
            workspace_model_object.update(work_space_name=new_workspace_name)
        if emoji:
            workspace_model_object.update(work_space_emoji=emoji)
        if not emoji and not new_workspace_name:
            raise HTTPException(
                status_code=BAD_REQUEST["status_code"],
                detail=BAD_REQUEST["detail"]
            )
        return True
    except WorkSpaceModel.DoesNotExist:
        raise HTTPException(
            status_code=BAD_REQUEST["status_code"],
            detail=BAD_REQUEST["detail"]
        )


def delete_workspace(workspace_name):
    try:
        workspace_model_obj = WorkSpaceModel.objects.get(work_space_name=workspace_name)
        workspace_model_obj.delete()
        return True
    except WorkSpaceModel.DoesNotExist:
        raise HTTPException(
            status_code=BAD_REQUEST["status_code"],
            detail=BAD_REQUEST["detail"]
        )
