from fastapi import FastAPI, APIRouter, Request, HTTPException
from pydantic import BaseModel
from Services.notes.notes_saving_service import new_notes, rename_notes, delete_notes
from Services.auth.auth_services import token_check
from typing import Optional
from error_constants import BAD_REQUEST


router = APIRouter()


class NotesEditingModel(BaseModel):
    work_space_id: str
    notes_name:  Optional[str] = "untitled"
    data: str


@router.post("/create_notes/", status_code=200)
def create_user_notes(
        notes_editing_obj: NotesEditingModel,
        request: Request,

):
    print(notes_editing_obj.notes_name)
    user_dict = token_check(request)
    return new_notes(
        user_dict=user_dict,
        work_space_id=notes_editing_obj.work_space_id,
        notes_name=notes_editing_obj.notes_name,
        to_save_data=notes_editing_obj.data
    )


class NotesRenameModel(BaseModel):
    old_notes_name: str
    new_notes_name: Optional[str]


@router.post("/rename_notes/", status_code=200)
def rename_user_notes(
        notes_rename_obj: NotesRenameModel,
        request: Request,

):
    token_check(request)
    if not notes_rename_obj.new_notes_name:
        raise HTTPException(
            status_code=BAD_REQUEST["status_code"],
            detail=BAD_REQUEST["detail"]
        )
    return rename_notes(
        old_notes_name=notes_rename_obj.old_notes_name,
        new_notes_name=notes_rename_obj.new_notes_name,
    )


class NotesDeleteModel(BaseModel):
    notes_name:  str


@router.post("/delete_notes/", status_code=200)
def delete_user_notes(
        notes_delete_obj: NotesDeleteModel,
        request: Request,

):
    token_check(request)
    return delete_notes(
        notes_name=notes_delete_obj.notes_name
    )
