from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from Services.workspace_services import new_workspace, delete_workspace, rename_workspace
from Services.auth.auth_services import token_check
from typing import Optional
from error_constants import BAD_REQUEST
from Services.display_all_workspace import display_workspace_catch


router = APIRouter()


class WorkspaceEditingModel(BaseModel):
    workspace_name:  str
    emoji: str

    @validator('workspace_name')
    def has_max_length(cls, v):
        max_length = 50
        if len(v) > max_length:
            raise AnyStrMaxLengthError(limit_value=max_length)
        return v


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

    @validator('old_workspace_name', 'new_workspace_name')
    def has_max_length(cls, v):
        max_length = 50
        if len(v) > max_length:
            raise AnyStrMaxLengthError(limit_value=max_length)
        return v


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


class WorkspaceDeleteModel(BaseModel):
    workspace_id:  str

    class Config:
        min_anystr_length = 24
        error_msg_templates = {
            'value_error.any_str.max_length': 'max_length:{limit_value}',
        }


@router.post("/delete_workspace/", status_code=200)
def delete_user_workspace(
        workspace_delete_obj: WorkspaceDeleteModel,
        request: Request,

):
    user_dict = token_check(request)
    return delete_workspace(
        workspace_id=workspace_delete_obj.workspace_id,
        user_dict=user_dict,
    )
