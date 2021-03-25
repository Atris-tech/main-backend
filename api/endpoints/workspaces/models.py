from typing import Optional
from pydantic import BaseModel, validator
from settings import MAX_WORKSPACE_NAME_LENGTH, MIN_WORKSPACE_ID, MAX_WORKSPACE_ID, MIN_WORKSPACE_NAME_LENGTH
from error_constants import BadRequest, EntityLengthError
from fastapi import HTTPException


class WorkspaceEditingModel(BaseModel):
    workspace_name:  str
    emoji: str

    @validator('*')
    def never_empty(cls, v, field):
        if not v:
            error_obj = EntityLengthError(entity=str(field.name), empty=True)
            raise HTTPException(status_code=error_obj.code, detail=error_obj.detail)
        return v

    @validator('workspace_name')
    def has_max_length(cls, v, field):
        max_length = MAX_WORKSPACE_NAME_LENGTH
        if len(v) > max_length:
            error_obj = EntityLengthError(entity=str(field.name), length=max_length, your_length=len(v))
            raise HTTPException(
                status_code=error_obj.code,
                detail=error_obj.detail
            )
        return v

    @validator('workspace_name')
    def has_min_length(cls, v, field):
        min_length = MIN_WORKSPACE_NAME_LENGTH
        if len(v) < min_length:
            error_obj = EntityLengthError(entity=str(field.name), length=min_length, your_length=len(v))
            raise HTTPException(
                status_code=error_obj.code,
                detail=error_obj.detail
            )
        return v


class WorkspaceRenameModel(BaseModel):
    old_workspace_name: str
    new_workspace_name: Optional[str]
    emoji: Optional[str]

    @validator('*')
    def never_empty(cls, v, field):
        if not v:
            error_obj = EntityLengthError(entity=str(field.name), empty=True)
            raise HTTPException(status_code=error_obj.code, detail=error_obj.detail)
        return v

    @validator('old_workspace_name', 'new_workspace_name')
    def has_max_length(cls, v, field):
        max_length = MAX_WORKSPACE_NAME_LENGTH
        if len(v) > max_length:
            error_obj = EntityLengthError(entity=str(field.name), length=max_length, your_length=len(v))
            raise HTTPException(
                status_code=error_obj.code,
                detail=error_obj.detail
            )
        return v


class WorkspaceDeleteModel(BaseModel):
    workspace_id:  str

    @validator('workspace_id')
    def has_min_length(cls, v):
        min_length = MIN_WORKSPACE_ID
        max_length = MAX_WORKSPACE_ID
        if len(v) < min_length or len(v) > max_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v


class WorkspaceCacheModel(BaseModel):
    workspace_id:  str

    @validator('workspace_id')
    def has_min_length(cls, v):
        min_length = MIN_WORKSPACE_ID
        max_length = MAX_WORKSPACE_ID
        if len(v) < min_length or len(v) > max_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v
