from Services.storage_services import StorageServices
from Services.type_sense.type_sense_crud_service import delete_collection
from db_models.models.audio_model import Audio
from settings import TYPESENSE_AUDIO_INDEX


def delete_audios(notes_obj, container_name):
    print(container_name)
    audio_objs = Audio.objects.filter(notes_id=notes_obj)
    for audio_obj in audio_objs:
        print(audio_obj.blob_name)
        delete_collection(collections_id=str(audio_obj.id), index=TYPESENSE_AUDIO_INDEX)
        StorageServices().delete_blob(container_name=container_name, blob_name=audio_obj.blob_name)


def delete_single_audio(audio_obj, container_name):
    delete_collection(collections_id=str(audio_obj.id), index=TYPESENSE_AUDIO_INDEX)
    StorageServices().delete_blob(container_name=container_name, blob_name=audio_obj.blob_name)
    audio_obj.delete()
