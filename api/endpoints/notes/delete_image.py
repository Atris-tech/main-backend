from fastapi import Request, APIRouter, HTTPException
from mongoengine import Q

from Services.audios.delete_audio_service import delete_single_audio
from Services.auth.auth_services import token_check
from api.endpoints.notes.models import ImageDeleteModel
from db_models.models.images_model import Image
from db_models.models.user_model import UserModel
from error_constants import BadRequest

router = APIRouter()


@router.post("/delete_image/", status_code=200)
def delete_audio(
        request: Request,
        image_delete_obj: ImageDeleteModel,
):
    user_dict = token_check(request)
    try:
        user_obj = UserModel.objects.get(email_id=user_dict["email_id"])
        image_obj = Image.objects.get(Q(user_id=user_obj) & Q(id=image_delete_obj.image_id))
        delete_single_audio(audio_obj=image_obj, container_name=user_obj.user_storage_container_name)
        return True
    except Image.DoesNotExist:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail + " or note deleted before"
        )
