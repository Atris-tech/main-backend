from mongoengine import Q

from error_constants import BadRequest
from Services.type_sense.type_sense_configs.typesense_client import client
from settings import TYPESENSE_NOTES_INDEX, TYPESENSE_IMAGES_INDEX, TYPESENSE_AUDIO_INDEX
from fastapi import HTTPException
from Services.auth.auth_services import check_user
from db_models.models.user_model import UserModel
from db_models.models.cache_display_model import CacheModel
from db_models.models.tags_model import TagModel
from Services.type_sense.type_sense_crud_service import delete_collection
import json


def search_data(search_requests, common_search_params, notes=True):
    data = client.multi_search.perform(search_requests, common_search_params)
    search_results = list()
    if data['results'][0]['found'] >= 1:
        for result in data['results'][0]['hits']:
            try:
                if notes:
                    notes_id = result["document"]["id"]
                else:
                    notes_id = result["document"]["notes_id"]
                cache_model_obj = CacheModel.objects.get(notes_id=notes_id)
                data = json.loads(cache_model_obj.to_json())
                data['highlights'] = result['highlights']
                search_results.append(data)
            except CacheModel.DoesNotExist:
                delete_collection(collections_id=result["id"], index=TYPESENSE_NOTES_INDEX)
    return search_results


def search_notes(email, query):
    user_obj = UserModel.objects.get(email_id=email)
    search_requests = {
        'searches': [
            {
                'collection': TYPESENSE_NOTES_INDEX,
                'q': query,
                'filter_by': 'user_id:=' + str(user_obj.id)
            }
        ]
    }

    common_search_params = {
        'query_by': ['notes_name', 'clean_text', 'summary']
    }
    return search_data(search_requests, common_search_params, notes=True,)


def search_images(email, query,):
    user_obj = UserModel.objects.get(email_id=email)

    search_requests = {
        'searches': [
            {
                'collection': TYPESENSE_IMAGES_INDEX,
                'q': query,
                'filter_by': 'user_id:=' + str(user_obj.id)
            }
        ]
    }
    common_search_params = {
        'query_by': ['ocr', 'labels']
    }
    return search_data(search_requests, common_search_params, notes=False,)


def search_audio(email, query):
    user_obj = UserModel.objects.get(email_id=email)

    search_requests = {
        'searches': [
            {
                'collection': TYPESENSE_AUDIO_INDEX,
                'q': query,
                'filter_by': 'user_id:=' + str(user_obj.id)
            }
        ]
    }
    common_search_params = {
        'query_by': ['name', 'transcribe', 'sound_recog']
    }
    return search_data(search_requests, common_search_params, notes=False,)


def filter_tag(tag_id, email):
    user_obj = check_user(email=email)
    search_results = list()
    try:
        tag_obj = TagModel.objects.get(Q(user_id=user_obj)& Q(id=tag_id))
        tag_obj_data = json.loads(tag_obj.to_json())
        for cache_id in tag_obj_data["notes"]:
            try:
                cache_model_obj = CacheModel.objects.get(id=cache_id)
                data = json.loads(cache_model_obj.to_json())
                search_results.append(data)
            except CacheModel.DoesNotExist:
                print(tag_obj.notes)
                tag_obj_data["notes"].remove(cache_id)
                tag_obj_data["count"] = tag_obj_data["count"] - 1
                tag_obj = TagModel.from_json(json.dumps(tag_obj_data))
                if tag_obj.count <= 0:
                    tag_obj.delete()
                else:
                    tag_obj.save()
        return search_results
    except TagModel.DoesNotExist:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )