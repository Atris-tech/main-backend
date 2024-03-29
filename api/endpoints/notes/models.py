from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, validator

from error_constants import BadRequest, EntityLengthError, MaxSummaryLength
from settings import MAX_NOTES_NAME_LENGTH, MIN_NOTES_ID, MAX_NOTES_ID, MAX_SUMMARY_ENTITY_LENGTH


class NotesEditingModel(BaseModel):
    work_space_id: str
    notes_name: Optional[str] = "untitled"

    @validator('*')
    def never_empty(cls, v, field):
        if not v:
            error_obj = EntityLengthError(entity=str(field.name), empty=True)
            raise HTTPException(status_code=error_obj.code, detail=error_obj.detail)
        return v

    @validator('notes_name')
    def has_max_length(cls, v, field):
        max_length = MAX_NOTES_NAME_LENGTH
        if len(v) > max_length:
            error_obj = EntityLengthError(entity=str(field.name), length=max_length, your_length=len(v))
            raise HTTPException(
                status_code=error_obj.code,
                detail=error_obj.detail
            )
        return v

    @validator('work_space_id')
    def has_min_length(cls, v):
        min_length = MIN_NOTES_ID
        max_length = MAX_NOTES_ID
        if len(v) < min_length or len(v) > max_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v


class NotesSavingModel(BaseModel):
    notes_id: str
    work_space_id: str
    data: str

    @validator('work_space_id', 'notes_id')
    def has_min_length(cls, v):
        min_length = MIN_NOTES_ID
        max_length = MAX_NOTES_ID
        if len(v) < min_length or len(v) > max_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v


class NotesRenameModel(BaseModel):
    old_notes_id: str
    new_notes_name: str

    @validator('*')
    def never_empty(cls, v, field):
        if not v:
            error_obj = EntityLengthError(entity=str(field.name), empty=True)
            raise HTTPException(status_code=error_obj.code, detail=error_obj.detail)
        return v

    @validator('old_notes_id')
    def has_min_length(cls, v):
        min_length = MIN_NOTES_ID
        if len(v) < min_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v

    @validator('new_notes_name')
    def has_max_length(cls, v, field):
        max_length = MAX_NOTES_NAME_LENGTH
        if len(v) > max_length:
            error_obj = EntityLengthError(entity=str(field.name), length=max_length, your_length=len(v))
            raise HTTPException(
                status_code=error_obj.code,
                detail=error_obj.detail
            )
        return v


class NotesDeleteModel(BaseModel):
    notes_id: str

    @validator('notes_id')
    def has_min_length(cls, v):
        min_length = MIN_NOTES_ID
        max_length = MAX_NOTES_ID
        if len(v) < min_length or len(v) > max_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v


class NotesDuplicateModel(BaseModel):
    notes_id: str
    workspace_id: str

    @validator('notes_id')
    def has_min_length(cls, v):
        min_length = MIN_NOTES_ID
        max_length = MAX_NOTES_ID
        if len(v) < min_length or len(v) > max_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v


class NotesMoveModel(BaseModel):
    notes_id: str
    old_workspace_id: str
    new_workspace_id: str

    @validator('notes_id', 'old_workspace_id', 'new_workspace_id')
    def has_min_length(cls, v):
        min_length = MIN_NOTES_ID
        max_length = MAX_NOTES_ID
        if len(v) < min_length or len(v) > max_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v


class SmmryEntityModel(BaseModel):
    notes_id: str
    summary: Optional[str]

    @validator('notes_id')
    def has_min_length(cls, v):
        min_length = MIN_NOTES_ID
        max_length = MAX_NOTES_ID
        if len(v) < min_length or len(v) > max_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v

    @validator('summary')
    def has_max_length(cls, v):
        max_length = MAX_SUMMARY_ENTITY_LENGTH
        if len(v) > max_length:
            raise HTTPException(
                status_code=MaxSummaryLength.code,
                detail=MaxSummaryLength.detail
            )
        return v


class AudioDeleteModel(BaseModel):
    audio_id: str

    @validator('audio_id')
    def has_min_length(cls, v):
        min_length = MIN_NOTES_ID
        max_length = MAX_NOTES_ID
        if len(v) < min_length or len(v) > max_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v


class ImageDeleteModel(BaseModel):
    image_id: str

    @validator('image_id')
    def has_min_length(cls, v):
        min_length = MIN_NOTES_ID
        max_length = MAX_NOTES_ID
        if len(v) < min_length or len(v) > max_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v


class AudioRenameModel(BaseModel):
    audio_id: str
    new_name: str

    @validator('audio_id')
    def has_min_length(cls, v):
        min_length = MIN_NOTES_ID
        max_length = MAX_NOTES_ID
        if len(v) < min_length or len(v) > max_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v

    @validator('new_name')
    def has_max_length(cls, v, field):
        max_length = MAX_NOTES_NAME_LENGTH
        if len(v) > max_length:
            error_obj = EntityLengthError(entity=str(field.name), length=max_length, your_length=len(v))
            raise HTTPException(
                status_code=error_obj.code,
                detail=error_obj.detail
            )
        return v


class CreateScribbleModel(BaseModel):
    note_id: str
    y_axis: Optional[str] = None
    name: Optional[str] = "untitled"

    @validator('note_id')
    def has_min_length(cls, v):
        min_length = MIN_NOTES_ID
        max_length = MAX_NOTES_ID
        if len(v) < min_length or len(v) > max_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v

    @validator('name')
    def has_max_length(cls, v, field):
        max_length = MAX_NOTES_NAME_LENGTH
        if len(v) > max_length:
            error_obj = EntityLengthError(entity=str(field.name), length=max_length, your_length=len(v))
            raise HTTPException(
                status_code=error_obj.code,
                detail=error_obj.detail
            )
        return v


class GetScribble(BaseModel):
    scribble_id: str

    @validator('scribble_id')
    def has_min_length(cls, v):
        min_length = MIN_NOTES_ID
        max_length = MAX_NOTES_ID
        if len(v) < min_length or len(v) > max_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v


class RenameScribble(BaseModel):
    scribble_id: str
    name: str

    @validator('scribble_id')
    def has_min_length(cls, v):
        min_length = MIN_NOTES_ID
        max_length = MAX_NOTES_ID
        if len(v) < min_length or len(v) > max_length:
            raise HTTPException(
                status_code=BadRequest.code,
                detail=BadRequest.detail
            )
        return v

    @validator('name')
    def has_max_length(cls, v, field):
        max_length = MAX_NOTES_NAME_LENGTH
        if len(v) > max_length:
            error_obj = EntityLengthError(entity=str(field.name), length=max_length, your_length=len(v))
            raise HTTPException(
                status_code=error_obj.code,
                detail=error_obj.detail
            )
        return v