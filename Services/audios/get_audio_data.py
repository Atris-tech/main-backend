import datetime
import urllib.parse as urlparse
from urllib.parse import parse_qs

import dateutil.parser
from dateutil.tz import tzutc
from fastapi.exceptions import HTTPException
from mongoengine import Q

from Services.storage_services import StorageServices
from db_models.models.audio_model import Audio
from db_models.models.user_model import UserModel
from error_constants import BadRequest


def check_audio_url_expired(url):
    parsed = urlparse.urlparse(url)
    params = parse_qs(parsed.query)
    to_check_date = dateutil.parser.isoparse(params["se"][0])
    current_date = datetime.datetime.now(tz=tzutc())
    return current_date > to_check_date


def get_audio_data(notes_id, email):
    try:
        user_obj = UserModel.objects.get(email_id=email)
        audio_objs = Audio.objects.filter(Q(user_id=user_obj) & Q(notes_id=notes_id))
        to_send_data_array = list()
        for audio_obj in audio_objs:
            to_send_data = dict()
            to_send_data["name"] = audio_obj.name
            if check_audio_url_expired(audio_obj.url):
                url = StorageServices().regenerate_url(container_name=user_obj.user_storage_container_name,
                                                       blob_name=audio_obj.blob_name)
                if url is not None:
                    to_send_data["url"] = url
                    audio_obj.url = url
                    audio_obj.update(url=url)
                    print("url updated")
                else:
                    print("None Url")
            else:
                to_send_data["url"] = audio_obj.url
            to_send_data["sound_recog_results"] = audio_obj.sound_recog_results
            to_send_data["alignments"] = audio_obj.forced_alignment_data
            to_send_data_array.append(to_send_data)
        return to_send_data_array
    except Audio.DoesNotExist:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )
