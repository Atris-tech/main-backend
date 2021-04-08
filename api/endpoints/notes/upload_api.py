from fastapi import Request, File, UploadFile, HTTPException, Header, Depends, BackgroundTasks, Form, APIRouter
from Services.auth.auth_services import token_check
from Services.storage_services import upload_file_blob_storage
from db_models.models.user_model import UserModel
from db_models.models.workspace_model import WorkSpaceModel
from tasks.image_process_bg_task import index_image
from tasks.upload_file_stt_bg_tasks import upload_task
from db_models.models.notes_model import NotesModel
import uuid
from mongoengine.queryset.visitor import Q
from error_constants import BadRequest, MinAudioLength, MaxAudioLength, MaxImageLength
from Services.plan_helper import check_space
from settings import MIN_AUDIO_LENGTH, MAX_AUDIO_LENGTH, MIN_IMAGE_LENGTH, MAX_IMAGE_LENGTH

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
        y_axis: str = Form(default=None)
):
    print(y_axis)
    user_dict = token_check(request)
    user_obj = UserModel.objects.get(email_id=user_dict["email_id"])
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

    background_tasks.add_task(upload_task, user_obj=user_obj, notes_id=str(notes_obj.id),
                              file_data=file_data, file_name=str(uuid.uuid4()) + file.filename,
                              original_file_name=file.filename,
                              blob_size=content_length, audio_request_id=audio_request_id, y_axis=y_axis)
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
    data = upload_file_blob_storage(file_data=file_data, file_name=file_name, user_model_obj=user_obj)
    print("data")
    print(data)
    url = data["url"]
    background_tasks.add_task(index_image, file_data=file_data, url=url, notes_model_obj=notes_obj,
                              content_length=content_length, user_obj=user_obj,
                              file_name=file_name)
    return url
