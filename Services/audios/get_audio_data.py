from mongoengine import Q
from Services.type_sense.type_sense_crud_service import get_collection
from db_models.models.audio_model import Audio
from db_models.models.user_model import UserModel
from fastapi.exceptions import HTTPException
from error_constants import BadRequest
from settings import TYPESENSE_AUDIO_INDEX


def get_audio_data(audio_id, email):
    try:
        user_obj = UserModel.objects.get(email_id=email)
        audio_obj = Audio.objects.get(Q(user_id=user_obj) & Q(id=audio_id))
        data = get_collection(id=str(audio_obj.id), index=TYPESENSE_AUDIO_INDEX)
        to_send_data = dict()
        to_send_data["url"] = audio_obj.url
        to_send_data["transcribe"] = data["transcribe"]
        to_send_data["sound_recog_results"] = data["sound_recog"]
        to_send_data["alignments"] = audio_obj.forced_alignment_data
        to_send_data["name"] = data["name"]
        return to_send_data
    except Audio.DoesNotExist:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )

