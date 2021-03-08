import binascii
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from Services.notes.notes_saving_service import new_notes, rename_notes, delete_notes
from Services.auth.auth_services import token_check
from typing import Optional
from error_constants import BAD_REQUEST
import base64
from icecream import ic

router = APIRouter()


class NotesEditingModel(BaseModel):
    work_space_id: str
    notes_name:  Optional[str] = "untitled"
    data: str


@router.post("/create_note/", status_code=200)
def create_user_notes(
        notes_editing_obj: NotesEditingModel,
        request: Request,

):
    try:
        binary_html = base64.b64decode(notes_editing_obj.data)
        html = binary_html.decode('utf8')
    except (binascii.Error, UnicodeDecodeError, Exception) as e:
        ic()
        ic(e)
        raise HTTPException(
            status_code=BAD_REQUEST["status_code"],
            detail=BAD_REQUEST["detail"]
        )
    print(notes_editing_obj.notes_name)
    user_dict = token_check(request)
    return new_notes(
        user_dict=user_dict,
        work_space_id=notes_editing_obj.work_space_id,
        notes_name=notes_editing_obj.notes_name,
        to_save_data=html
    )


class NotesRenameModel(BaseModel):
    old_notes_id: str
    new_notes_name: str


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
