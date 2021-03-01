from fastapi import Request, File, UploadFile, HTTPException, Header, Depends,BackgroundTasks, Form, APIRouter
from Services.auth.auth_services import token_check
from db_models.models.user_model import UserModel
from db_models.models.workspace_model import WorkSpaceModel
from tasks.upload_file_stt_bg_tasks import upload_task
from db_models.models.notes_model import NotesModel
import uuid
from mongoengine.queryset.visitor import Q
from error_constants import BAD_REQUEST
from Services.plan_helper import check_space
from .notes_management import router


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
    try:
        work_space_obj = WorkSpaceModel.objects.get(id=work_space_id)
        notes_obj = NotesModel.objects(Q(user_id=user_obj) & Q(workspace_id=work_space_obj) & Q(id=notes_id))
        print("*********************************************************")
        print(content_length)
        check_space(user_model_obj=user_obj, blob_size=content_length)

    except NotesModel.DoesNotExist:
        raise HTTPException(
            status_code=BAD_REQUEST["status_code"],
            detail=BAD_REQUEST["detail"]
        )
    file_data = file.file.read()
    """upload file in background task and call rq process in background"""

    background_tasks.add_task(upload_task, user_obj=user_obj, notes_obj=notes_obj,
                              file_data=file_data, file_name=str(uuid.uuid4()) + file.filename)
    return True
