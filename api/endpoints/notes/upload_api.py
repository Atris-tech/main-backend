from fastapi import Request, File, UploadFile, HTTPException, Header, Depends, BackgroundTasks, Form, APIRouter
from Services.auth.auth_services import token_check
from db_models.models.user_model import UserModel
from db_models.models.workspace_model import WorkSpaceModel
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
        file: UploadFile = File(...),
        notes_id: str = Form(...),
        work_space_id: str = Form(...),
        content_length: int = Depends(valid_content_length)
):
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
        work_space_obj = WorkSpaceModel.objects.get(Q(user_id=user_obj) & Q(id=work_space_id))
        notes_obj = NotesModel.objects.get(Q(user_id=user_obj) & Q(workspace_id=work_space_obj) & Q(id=notes_id))
        print("*********************************************************")
        print(content_length)
        check_space(user_model_obj=user_obj, blob_size=content_length)

    except (NotesModel.DoesNotExist, WorkSpaceModel.DoesNotExist):
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )
    file_data = file.file.read()

    background_tasks.add_task(upload_task, user_obj=user_obj, notes_obj=notes_obj,
                              file_data=file_data, file_name=str(uuid.uuid4()) + file.filename,
                              blob_size=content_length)
    return True

@router.post("/upload_image/", status_code=200)
def upload_image(
background_tasks: BackgroundTasks,
        request: Request,
        file: UploadFile = File(...),
        notes_id: str = Form(...),
        work_space_id: str = Form(...),
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
        notes_obj = NotesModel.objects.get(Q(user_id=user_obj) & Q(workspace_id=work_space_obj) & Q(id=notes_id))
        print("*********************************************************")
        print(content_length)
        check_space(user_model_obj=user_obj, blob_size=content_length)

    except (NotesModel.DoesNotExist, WorkSpaceModel.DoesNotExist):
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )
    file_data = file.file.read()

    background_tasks.add_task(upload_task, user_obj=user_obj, notes_obj=notes_obj,
                              file_data=file_data, file_name=str(uuid.uuid4()) + file.filename,
                              blob_size=content_length)
    return True


