from uuid import uuid4

from fastapi import Request, File, UploadFile, Depends, BackgroundTasks, Form, APIRouter, Header, HTTPException
from mongoengine import Q

import error_constants
from Services.auth.auth_services import token_check
from Services.plan_helper import check_space
from Services.storage_services import StorageServices
from db_models.models import NotesModel
from db_models.models.scribbles_model import Scribbles
from db_models.models.user_model import UserModel
from db_models.models.tags_model import TagModel
from settings import MIN_NOTES_ID, MAX_NOTES_ID
import json

router = APIRouter()


def valid_content_length(content_length: int = Header(..., lt=50_000_000)):
    return content_length


@router.post("/upload_scribble/", status_code=200)
def upload_scribble(background_tasks: BackgroundTasks,
                    request: Request,
                    file: UploadFile = File(...),
                    note_id: str = Form(None, min_length=MIN_NOTES_ID, max_length=MAX_NOTES_ID),
                    y_axis: float = Form(default=None),
                    name: str = Form(default=None),
                    content_length: int = Depends(valid_content_length)
                    ):
    if note_id is not None:
        user_dict = token_check(request)
        user_obj = UserModel.objects.get(email_id=user_dict["email_id"])
        try:
            notes_obj = NotesModel.objects.get(Q(user_id=user_obj) & Q(id=note_id))
            try:
                json.load(file.file)
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=error_constants.InvalidFileType.code,
                    detail=error_constants.InvalidFileType.detail
                )
            container = user_obj.user_storage_container_name
            check_space(user_model_obj=user_obj, blob_size=content_length)
            scribble_blob_id = str(uuid4())
            scribble_obj = Scribbles(
                user_id=user_obj,
                note_id=notes_obj,
                blob_name=scribble_blob_id,
                name=name,
                y_axis=y_axis,
                canvas_size=content_length
            ).save()
            file.file.seek(0)
            background_tasks.add_task(
                StorageServices().upload_file_blob_storage,
                file_data=file.file.read(),
                container_name=container,
                file_name=scribble_blob_id
            )
            return str(scribble_obj.id)

        except NotesModel.DoesNotExist:
            raise HTTPException(
                status_code=error_constants.BadRequest.code,
                detail=error_constants.BadRequest.detail
            )
    else:
        raise HTTPException(
            status_code=error_constants.BadRequest.code,
            detail=error_constants.BadRequest.detail
        )
