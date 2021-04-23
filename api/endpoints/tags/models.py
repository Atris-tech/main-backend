from fastapi import HTTPException
from pydantic import BaseModel, validator

from error_constants import EntityLengthError, BadRequest
from settings import MAX_TAGS_NAME, MIN_NOTES_ID, MAX_NOTES_ID


class TagsApiModel(BaseModel):
    tags_name: list
    workspace_id: str
    notes_id: str

    @validator('*')
    def never_empty(cls, v, field):
        if not v:
            error_obj = EntityLengthError(entity=str(field.name), empty=True)
            raise HTTPException(status_code=error_obj.code, detail=error_obj.detail)
        return v

    @validator('tags_name')
    def has_max_length(cls, v, field):
        max_length = MAX_TAGS_NAME
        for val in v:
            if type(val) != str:
                raise HTTPException(
                    status_code=BadRequest.code,
                    detail=BadRequest.detail
                )
            if len(val) > max_length:
                error_obj = EntityLengthError(entity=str(field.name), length=max_length, your_length=len(v))
                raise HTTPException(
                    status_code=error_obj.code,
                    detail=error_obj.detail
                )
            return v

    @validator('workspace_id', 'notes_id')
    def has_min_length(cls, v):
        min_length = MIN_NOTES_ID
        max_length = MAX_NOTES_ID
        if len(v) < min_length or len(v) > max_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v


class TagsDeleteModel(BaseModel):
    tag_id: str
    notes_id: str

    @validator('tag_id', 'notes_id')
    def has_min_length(cls, v):
        min_length = MIN_NOTES_ID
        max_length = MAX_NOTES_ID
        if len(v) < min_length or len(v) > max_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v
