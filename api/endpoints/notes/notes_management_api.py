from fastapi import Request
from pydantic import BaseModel, validator, AnyStrMinLengthError, AnyStrMaxLengthError
from Services.notes.notes_saving_service import new_note, rename_notes, delete_notes, save_note
from Services.auth.auth_services import token_check
from typing import Optional
from .child_api_routes import routing
from Services.notes.notes_parsing_service import b64_to_html

router = routing()


class NotesEditingModel(BaseModel):
    work_space_id: str
    notes_name:  Optional[str] = "untitled"

    @validator('notes_name')
    def has_max_length(cls, v):
        max_length = 300
        if len(v) > max_length:
            raise AnyStrMaxLengthError(limit_value=max_length)
        return v

    @validator('workspace_id')
    def has_min_length(cls, v):
        min_length = 24
        if len(v) < min_length:
            raise AnyStrMinLengthError(limit_value=min_length)
        return v


@router.post("/create_note/", status_code=200)
def create_user_note(
        notes_editing_obj: NotesEditingModel,
        request: Request,

):
    print(notes_editing_obj.notes_name)
    user_dict = token_check(request)
    return new_note(
        user_dict=user_dict,
        work_space_id=notes_editing_obj.work_space_id,
        notes_name=notes_editing_obj.notes_name,
    )


class NotesSavingModel(BaseModel):
    notes_id:  str
    work_space_id: str
    data: str

    @validator('workspace_id', 'notes_id')
    def has_min_length(cls, v):
        min_length = 24
        if len(v) < min_length:
            raise AnyStrMinLengthError(limit_value=min_length)
        return v


@router.post("/save_note/", status_code=200)
def create_user_notes(
        notes_saving_obj: NotesSavingModel,
        request: Request,

):
    html = b64_to_html(notes_saving_obj.data)
    user_dict = token_check(request)
    return save_note(
        user_dict=user_dict,
        work_space_id=notes_saving_obj.work_space_id,
        notes_id=notes_saving_obj.notes_id,
        to_save_data=html
    )


class NotesRenameModel(BaseModel):
    old_notes_id: str
    new_notes_name: str

    @validator('old_notes_id')
    def has_min_length(cls, v):
        min_length = 24
        if len(v) < min_length:
            raise AnyStrMinLengthError(limit_value=min_length)
        return v

    @validator('new_notes_name')
    def has_max_length(cls, v):
        max_length = 300
        if len(v) > max_length:
            raise AnyStrMaxLengthError(limit_value=max_length)
        return v


@router.post("/rename_note/", status_code=200)
def rename_user_notes(
        notes_rename_obj: NotesRenameModel,
        request: Request,

):
    user_dict = token_check(request)
    return rename_notes(
        notes_id=notes_rename_obj.old_notes_id,
        new_notes_name=notes_rename_obj.new_notes_name,
        email=user_dict["email_id"]
    )


class NotesDeleteModel(BaseModel):
    notes_id:  str

    @validator('notes_id')
    def has_min_length(cls, v):
        min_length = 24
        if len(v) < min_length:
            raise AnyStrMinLengthError(limit_value=min_length)
        return v


@router.post("/delete_note/", status_code=200)
def delete_user_notes(
        notes_delete_obj: NotesDeleteModel,
        request: Request,

):
    user_dict = token_check(request)
    return delete_notes(
        notes_id=notes_delete_obj.notes_id,
        email=user_dict["email_id"]
    )
