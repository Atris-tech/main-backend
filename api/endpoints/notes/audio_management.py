from fastapi import Request, APIRouter, Query, HTTPException
from mongoengine import Q

from Services.audios.delete_audio_service import delete_single_audio
from Services.audios.get_audio_data import get_all_audio_data, get_single_audio_data
from Services.auth.auth_services import token_check
from Services.type_sense.type_sense_crud_service import get_collection, update_collection
from api.endpoints.notes.models import AudioDeleteModel, AudioRenameModel
from db_models.models.audio_model import Audio
from db_models.models.user_model import UserModel
from error_constants import BadRequest
from settings import MIN_NOTES_ID, MAX_NOTES_ID
from settings import TYPESENSE_AUDIO_INDEX

router = APIRouter()


@router.get("/get_audios/", status_code=200)
def get_audio_data_api(
        request: Request,
        notes_id: str = Query(None, min_length=MIN_NOTES_ID, max_length=MAX_NOTES_ID),
):
    user_dict = token_check(request)
    return


@router.get("/get_audio_data/", status_code=200)
def get_audio_data(
        request: Request,
        audio_id: str = Query(None, min_length=MIN_NOTES_ID, max_length=MAX_NOTES_ID),
):
    user_dict = token_check(request)
    try:
        user_obj = UserModel.objects.get(email_id=user_dict["email_id"])
        audio_obj = Audio.objects.get(Q(user_id=user_obj) & Q(id=audio_id))
        return get_single_audio_data(audio_obj=audio_obj, user_obj=user_obj)
    except Audio.DoesNotExist:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail + " or note deleted before"
        )


@router.post("/delete_audio/", status_code=200)
def delete_audio(
        request: Request,
        audio_delete_obj: AudioDeleteModel,
):
    user_dict = token_check(request)
    try:
        user_obj = UserModel.objects.get(email_id=user_dict["email_id"])
        audio_obj = Audio.objects.get(Q(user_id=user_obj) & Q(id=audio_delete_obj.audio_id))
        delete_single_audio(audio_obj=audio_obj, container_name=user_obj.user_storage_container_name)
        return True
    except Audio.DoesNotExist:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail + " or note deleted before"
        )


@router.post("/rename_audio/", status_code=200)
def rename_audio(
        request: Request,
        audio_rename_obj: AudioRenameModel,
):
    user_dict = token_check(request)
    try:
        user_obj = UserModel.objects.get(email_id=user_dict["email_id"])
        audio_obj = Audio.objects.get(Q(user_id=user_obj) & Q(id=audio_rename_obj.audio_id))
        audio_obj.name = audio_rename_obj.new_name
        audio_obj.save()
        data = get_collection(index=TYPESENSE_AUDIO_INDEX, id=str(audio_obj.id))
        if data is not None:
            data["name"] = audio_rename_obj.new_name
            update_collection(data=data, index=TYPESENSE_AUDIO_INDEX)
            return True
        else:
            print("user deleted audio file")
            return False
    except Audio.DoesNotExist:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )
