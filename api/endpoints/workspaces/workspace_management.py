from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from Services.workspace_services import new_workspace, delete_workspace, rename_workspace
from Services.auth.auth_services import token_check
from typing import Optional
from error_constants import BAD_REQUEST


router = APIRouter()


class WorkspaceEditingModel(BaseModel):
    workspace_name:  str
    emoji: str


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


class WorkspaceRenameModel(BaseModel):
    old_workspace_name: str
    new_workspace_name: Optional[str]
    emoji: Optional[str]


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
                status_code=BAD_REQUEST["status_code"],
                detail=BAD_REQUEST["detail"]
            )
        return rename_workspace(
            old_workspace_name=workspace_rename_obj.old_workspace_name,
            new_workspace_name=workspace_rename_obj.new_workspace_name,
            emoji=workspace_rename_obj.emoji,
            user_dict=user_dict,
        )
    else:
        raise HTTPException(
            status_code=BAD_REQUEST["status_code"],
            detail=BAD_REQUEST["detail"]
        )


class WorkspaceDeleteModel(BaseModel):
    workspace_name:  str


@router.post("/delete_workspace/", status_code=200)
def delete_user_workspace(
        workspace_delete_obj: WorkspaceDeleteModel,
        request: Request,

):
    user_dict = token_check(request)
    return delete_workspace(
        workspace_name=workspace_delete_obj.workspace_name,
        user_dict=user_dict,
    )
