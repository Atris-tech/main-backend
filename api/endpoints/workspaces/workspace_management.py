from fastapi import APIRouter, Request, HTTPException, BackgroundTasks

from Services.auth.auth_services import token_check
from Services.display_all_workspace import display_workspace_catch
from Services.workspace_services import new_workspace, delete_workspace, rename_workspace, display_all_caches
from api.endpoints.workspaces.models import WorkspaceEditingModel, WorkspaceRenameModel, WorkspaceDeleteModel, \
    WorkspaceCacheModel
from error_constants import BadRequest

router = APIRouter()


@router.post("/create_workspace/", status_code=200)
def create_user_workspace(
        workspace_editing_obj: WorkspaceEditingModel,
        request: Request,

):
    user_dict = token_check(request)
    return new_workspace(
        user_dict=user_dict,
        name=workspace_editing_obj.workspace_name,
        emoji=workspace_editing_obj.emoji
    )


@router.post("/rename_workspace/", status_code=200)
def rename_user_workspace(
        workspace_rename_obj: WorkspaceRenameModel,
        request: Request,

):
    if workspace_rename_obj.old_workspace_name and workspace_rename_obj.new_workspace_name or \
            workspace_rename_obj.emoji:
        user_dict = token_check(request)
        if not workspace_rename_obj.new_workspace_name and not workspace_rename_obj.emoji:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return rename_workspace(
            old_workspace_name=workspace_rename_obj.old_workspace_name,
            new_workspace_name=workspace_rename_obj.new_workspace_name,
            emoji=workspace_rename_obj.emoji,
            user_dict=user_dict,
        )
    else:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )


@router.post("/delete_workspace/", status_code=200)
def delete_user_workspace(
        workspace_delete_obj: WorkspaceDeleteModel,
        request: Request,
        background_tasks: BackgroundTasks

):
    user_dict = token_check(request)
    background_tasks.add_task(delete_workspace,
                              workspace_id=workspace_delete_obj.workspace_id,
                              user_dict=user_dict)
    return True


@router.post("/display_all_notes/", status_code=200)
def display_notes(
        workspace_obj: WorkspaceCacheModel,
        request: Request
):
    user_dict = token_check(request)
    return display_all_caches(
        workspace_id=workspace_obj.workspace_id,
        user_dict=user_dict
    )


@router.post("/display_workspaces/", status_code=200)
def display_workspace_method(
        request: Request
):
    user_dict = token_check(request)
    return display_workspace_catch(email=user_dict["email_id"])
