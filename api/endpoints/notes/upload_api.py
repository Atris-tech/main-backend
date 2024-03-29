import uuid

from fastapi import Request, File, UploadFile, HTTPException, Header, Depends, BackgroundTasks, Form, APIRouter
from mongoengine.queryset.visitor import Q

from Services.auth.auth_services import token_check
from Services.plan_helper import check_space
from Services.storage_services import StorageServices
from db_models.models.notes_model import NotesModel
from db_models.models.user_model import UserModel
from db_models.models.workspace_model import WorkSpaceModel
from db_models.models.images_model import Image
from db_models.models.tags_model import TagModel
from error_constants import BadRequest, MinAudioLength, MaxAudioLength, MaxImageLength
from settings import MIN_AUDIO_LENGTH, MAX_AUDIO_LENGTH, MAX_IMAGE_LENGTH, MAX_NOTES_ID, MIN_NOTES_ID
from tasks.image_process_bg_task import index_image
from tasks.upload_file_stt_bg_tasks import upload_task

router = APIRouter()


def valid_content_length(content_length: int = Header(..., lt=50_000_000)):
    return content_length


@router.post("/upload_audio/", status_code=200)
def upload_audio(
        background_tasks: BackgroundTasks,
        request: Request,
        audio_request_id: str = Form(...),
        file: UploadFile = File(...),
        notes_id: str = Form(...),
        content_length: int = Depends(valid_content_length),
        y_axis: str = Form(default=None),
        work_space_id: str = Form(None, max_length=MAX_NOTES_ID, min_length=MAX_NOTES_ID)
):
    if work_space_id is None or audio_request_id is None or notes_id is None:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )
    print(y_axis)
    user_dict = token_check(request)
    user_obj = UserModel.objects.get(email_id=user_dict["email_id"])
    print("content_length")
    print(content_length)
    if content_length < MIN_AUDIO_LENGTH:
        raise HTTPException(
            status_code=MinAudioLength.code,
            detail=MinAudioLength.detail
        )
    elif content_length > MAX_AUDIO_LENGTH:
        raise HTTPException(
            status_code=MaxAudioLength.code,
            detail=MaxAudioLength.detail
        )

    try:
        WorkSpaceModel.objects.get(Q(user_id=user_obj) & Q(id=work_space_id))
        notes_obj = NotesModel.objects.get(Q(user_id=user_obj) & Q(id=notes_id))
        print("*********************************************************")
        print(content_length)
        check_space(user_model_obj=user_obj, blob_size=content_length)

    except (NotesModel.DoesNotExist, WorkSpaceModel.DoesNotExist):
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )
    file_data = file.file.read()
    check_space(user_model_obj=user_obj, blob_size=content_length)
    background_tasks.add_task(upload_task, user_obj=user_obj, notes_id=str(notes_obj.id),
                              file_data=file_data, file_name=str(uuid.uuid4()) + file.filename,
                              original_file_name=file.filename,
                              blob_size=content_length, audio_request_id=audio_request_id, y_axis=y_axis,
                              workspace_id=work_space_id, note_name=notes_obj.notes_name)
    return True


@router.post("/upload_image/", status_code=200)
def upload_image(
        background_tasks: BackgroundTasks,
        request: Request,
        file: UploadFile = File(...),
        notes_id: str = Form(...),
        content_length: int = Depends(valid_content_length)

):
    user_dict = token_check(request)
    user_obj = UserModel.objects.get(email_id=user_dict["email_id"])
    if content_length > MAX_IMAGE_LENGTH:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )
    elif content_length > MAX_AUDIO_LENGTH:
        raise HTTPException(
            status_code=MaxImageLength.code,
            detail=MaxImageLength.detail
        )
    try:
        notes_obj = NotesModel.objects.get(Q(user_id=user_obj) & Q(id=notes_id))
        print(content_length)
        check_space(user_model_obj=user_obj, blob_size=content_length)

    except (NotesModel.DoesNotExist, WorkSpaceModel.DoesNotExist):
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )
    file_data = file.file.read()
    print("in upload task")
    file_name = str(uuid.uuid4()) + file.filename
    data = StorageServices().upload_file_blob_storage(file_data=file_data, file_name=file_name, user_model_obj=user_obj)
    print("data")
    print(data)
    image_model_obj = Image()
    image_model_obj.image_size = content_length
    image_model_obj.blob_name = file_name
    image_model_obj.user_id = user_obj
    image_model_obj.notes_id = notes_obj
    image_model_obj.save()
    background_tasks.add_task(index_image, file_data=file_data, image_model_obj=image_model_obj,
                              file_name=file_name)
    return str(image_model_obj.id)
