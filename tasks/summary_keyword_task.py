from Services.redis_service import redis_publisher_serv
from task_worker_config.celery import app
from Services.summarization_api_call import summary_and_keywords_or_entity_api_call
from Services.type_sense.type_sense_crud_service import get_collection
from settings import TYPESENSE_NOTES_INDEX
from db_models.models.notes_model import NotesModel
from db_models.models.cache_display_model import CacheModel
from db_models.mongo_setup import global_init


def save_summary_and_key(notes_id, summary_api_endpoint, user_id, notes_model_obj):
    notes_data = get_collection(index=TYPESENSE_NOTES_INDEX, id=notes_id)
    clean_text = notes_data["clean_text"]
    data = summary_and_keywords_or_entity_api_call(text=clean_text, url=summary_api_endpoint)
    summary = data["summary"]
    notes_model_obj.summary = summary
    notes_model_obj.uds = "AUTO"
    notes_model_obj.save()
    cache_model_obj = CacheModel.objects.get(notes_id=notes_model_obj)
    cache_model_obj.uds = "AUTO"
    cache_model_obj.save()
    keywords = data["keywords"]
    """socket send for keywords"""
    to_send_ws_data = {
        "client_id": user_id,
        "data": {
            "status": "PROCESSED",
            "task": "Summary generation",
            "keywords": keywords,
            "notes_name": notes_model_obj.notes_name,
            "notes_id": notes_id,
            "workspace_id": str(notes_model_obj.workspace_id.id)
        }
    }
    print(to_send_ws_data)
    redis_publisher_serv(channel=str(user_id), data=to_send_ws_data)


@app.task(soft_time_limit=500, max_retries=3)
def summary_task(notes_id, summary_api_endpoint, user_id):
    global_init()
    try:
        notes_model_obj = NotesModel.objects.get(id=notes_id)
        save_summary_and_key(notes_id, summary_api_endpoint, user_id, notes_model_obj)
    except NotesModel.DoesNotExist:
        try:
            notes_model_obj = NotesModel.objects.get(id=notes_id)
            save_summary_and_key(notes_id, summary_api_endpoint, user_id, notes_model_obj)
        except NotesModel.DoesNotExist:
            print("the person deleted the note")
            to_send_ws_data = {
                "client_id": user_id,
                "data": {
                        "status": "FAILED",
                        "task": "Summary generation",
                        "notes_id": notes_id,
                        "detail": "Unknown Error Occurred or Note has been Deleted",
                }
            }
            print(to_send_ws_data)
            redis_publisher_serv(channel=str(user_id), data=to_send_ws_data)

