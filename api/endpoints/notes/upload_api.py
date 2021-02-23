from fastapi import APIRouter
from fastapi import FastAPI, APIRouter, Request, File, UploadFile, HTTPException, Header, Depends, BackgroundTasks
from Services.auth.auth_services import token_check
from Services.storage_services import upload_file_blob_storage
import uuid

router = APIRouter()


def valid_content_length(content_length: int = Header(..., lt=50_000_000)):
    return content_length


@router.post("/upload_api/", status_code=200, dependencies=[Depends(valid_content_length)])
def upload_audio(
        background_tasks: BackgroundTasks,
        request: Request,
        file: UploadFile = File(...),
):
    user_dict = token_check(request)
    file_data = file.file.read()
    """upload file in background task and call rq process in background"""

    background_tasks.add_task(upload_file_blob_storage, email=user_dict["email_id"], file_data=file_data,
                              file_name=str(uuid.uuid4()) + file.filename)
    """Check plan info here"""
    """direct api call if premium plan"""
    """send to queue if free plan"""
    """get the upload url and send to rq worker"""
    return url
