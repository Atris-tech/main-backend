from Services.type_sense.type_sense_crud_service import delete_collection
from Services.storage_services import delete_blob
from settings import TYPESENSE_AUDIO_INDEX
from db_models.models.cache_display_model import CacheModel
from db_models.models.audio_model import Audio


def delete_audios(notes_obj, container_name):
    audio_objs = Audio.objects.filter(notes_id=notes_obj)
    for audio_obj in audio_objs:
        print(audio_obj)
        print(audio_obj.id)
        print(audio_obj.name)
        print(container_name)
        print(audio_obj.blob_name)
        delete_collection(collections_id=str(audio_obj.id), index=TYPESENSE_AUDIO_INDEX)
        delete_blob(container_name=container_name, blob_name=audio_obj.blob_name)


def delete_single_audio(audio_obj, notes_obj, container_name):
    delete_collection(collections_id=str(audio_obj.id), index=TYPESENSE_AUDIO_INDEX)
    delete_blob(container_name=container_name, blob_name=audio_obj.blob_name)
    if notes_obj.audios[0] == audio_obj.id:
        cache_display_model = CacheModel.objects.get(notes_id=notes_obj)
        cache_display_model.audio_url = None
        cache_display_model.forced_alignment_for_first_audio = None
        cache_display_model.save()
    notes_obj.audios.remove(audio_obj)
    notes_obj.save()
    audio_obj.delete()
