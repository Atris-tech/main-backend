from fastapi import Request, Query, HTTPException

import error_constants
from Services.auth.auth_services import token_check
from Services.notes.notes_parsing_service import b64_to_html
from Services.notes.notes_saving_service import new_note, rename_notes, delete_notes, save_note, get_notes_data, duplicate_notes, move_notes
from Services.workspace_services import star_notes, book_mark_note, unstar, un_bookmark, \
    get_book_mark_notes
from settings import MIN_NOTES_ID, MAX_NOTES_ID
from .child_api_routes import routing
from .models import NotesEditingModel, NotesSavingModel, NotesRenameModel, NotesDeleteModel, NotesDuplicateModel,NotesMoveModel

router = routing()


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


@router.post("/star_note/", status_code=200)
def star_note_api(
        notes_id_obj: NotesDeleteModel,
        request: Request,
):
    user_dict = token_check(request)
    return star_notes(
        user_dict=user_dict,
        notes_id=notes_id_obj.notes_id
    )


@router.post("/un_star/", status_code=200)
def star_note_api(
        notes_id_obj: NotesDeleteModel,
        request: Request,
):
    user_dict = token_check(request)
    return unstar(
        user_dict=user_dict,
        notes_id=notes_id_obj.notes_id
    )


@router.post("/un_bookmark/", status_code=200)
def star_note_api(
        notes_id_obj: NotesDeleteModel,
        request: Request,
):
    user_dict = token_check(request)
    return un_bookmark(
        user_dict=user_dict,
        notes_id=notes_id_obj.notes_id
    )


@router.post("/bookmark_note/", status_code=200)
def star_note_api(
        notes_id_obj: NotesDeleteModel,
        request: Request,
):
    user_dict = token_check(request)
    return book_mark_note(user_dict=user_dict, notes_id=notes_id_obj.notes_id)


@router.get("/get_note/", status_code=200)
def get_notes_data_api(
        request: Request,
        notes_id: str = Query(None, min_length=MIN_NOTES_ID, max_length=MAX_NOTES_ID)
):
    if notes_id is not None:
        user_dict = token_check(request)
        return get_notes_data(
            user_dict=user_dict,
            note_id=notes_id
        )
    else:
        raise HTTPException(
            status_code=error_constants.BadRequest.code,
            detail=error_constants.BadRequest.detail
        )


@router.get("/get_all_bookmark_notes/", status_code=200)
def get_all_bookmark_notes(
        request: Request
):
    user_dict = token_check(request)
    return get_book_mark_notes(
        user_dict=user_dict
    )


@router.post("/duplicate_note/", status_code=200)
def duplicate_note_call(
        notes_duplicate_obj: NotesDuplicateModel,
        request: Request,

):
    print(notes_duplicate_obj.notes_id)
    user_dict = token_check(request)
    return duplicate_notes(
        user_dict=user_dict,
        workspace_id=notes_duplicate_obj.workspace_id,
        old_note_id=notes_duplicate_obj.notes_id
    )


@router.post("/move_note/", status_code=200)
def move_note_call(
        notes_move_obj: NotesMoveModel,
        request: Request,
):
    print(notes_move_obj.notes_id)
    user_dict = token_check(request)
    return move_notes(
        user_dict=user_dict,
        notes_id=notes_move_obj.notes_id,
        old_workspace_id=notes_move_obj.old_workspace_id,
        new_workspace_id=notes_move_obj.new_workspace_id
    )

