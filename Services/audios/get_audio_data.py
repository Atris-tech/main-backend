from mongoengine import Q
from Services.type_sense.type_sense_crud_service import get_collection
from db_models.models.audio_model import Audio
from db_models.models.user_model import UserModel
from fastapi.exceptions import HTTPException
from error_constants import BadRequest
from settings import TYPESENSE_AUDIO_INDEX


def get_audio_data(notes_id, email):
    try:
        user_obj = UserModel.objects.get(email_id=email)
        audio_objs = Audio.objects.filter(Q(user_id=user_obj) & Q(notes_id=notes_id))
        to_send_data_array = list()
        for audio_obj in audio_objs:
            data = get_collection(id=str(audio_obj.id), index=TYPESENSE_AUDIO_INDEX)
            to_send_data = dict()
            to_send_data["url"] = audio_obj.url
            if "transcribe" in data:
                to_send_data["transcribe"] = data["transcribe"]
            if "sound_recog_results" in data:
                to_send_data["sound_recog_results"] = data["sound_recog"]
            if "alignments" in data:
                to_send_data["alignments"] = audio_obj.forced_alignment_data
            to_send_data["name"] = data["name"]
            to_send_data_array.append(to_send_data)
        return to_send_data_array
    except Audio.DoesNotExist:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )

