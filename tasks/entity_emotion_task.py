from Services.redis_service import redis_publisher_serv
from Services.summarization_api_call import summary_and_keywords_or_entity_api_call
from Services.type_sense.type_sense_crud_service import get_collection
from db_models.models import NotesModel
from settings import TYPESENSE_NOTES_INDEX
from task_worker_config.celery import app
from db_models.mongo_setup import global_init


def save_entity_emotiopns(notes_model_obj, notes_id, entity_endpoint, emotion_endpoint, user_id):
    notes_data = get_collection(index=TYPESENSE_NOTES_INDEX, id=notes_id)
    clean_text = notes_data["clean_text"]
    if len(clean_text) > 10:
        entity_data = summary_and_keywords_or_entity_api_call(text=clean_text, url=entity_endpoint)
        emotion = summary_and_keywords_or_entity_api_call(text=clean_text, url=emotion_endpoint)
        notes_model_obj.emotion = emotion
        notes_model_obj.entity_data = entity_data
        notes_model_obj.save()
        to_send_ws_data = {
            "client_id": user_id,
            "data": {
                "status": "PROCESSED",
                "task": "Entity Emotion generation",
                "notes_name": notes_model_obj.notes_name,
                "notes_id": notes_id,
                "workspace_id": str(notes_model_obj.workspace_id.id)
            }
        }
    else:
        to_send_ws_data = {
            "client_id": user_id,
            "data": {
                "status": "FAILED",
                "task": "Entity Emotion generation",
                "notes_id": notes_id,
                "detail": "not enough text to generate entity"
            }
        }
    return to_send_ws_data


@app.task(soft_time_limit=500, max_retries=3)
def generate_entity_emotion(notes_id, entity_endpoint, emotion_endpoint, user_id):
    global_init()
    try:
        notes_model_obj = NotesModel.objects.get(id=notes_id)
        to_send_ws_data = save_entity_emotiopns(notes_model_obj, notes_id, entity_endpoint, emotion_endpoint, user_id)

    except NotesModel.DoesNotExist:
        try:
            notes_model_obj = NotesModel.objects.get(id=notes_id)
            to_send_ws_data = save_entity_emotiopns(notes_model_obj, notes_id, entity_endpoint, emotion_endpoint,
                                                    user_id)
        except NotesModel.DoesNotExist:
            print("the person deleted the note")
            to_send_ws_data = {
                "client_id": user_id,
                "data": {
                    "status": "FAILED",
                    "task": "Entity Emotion generation",
                    "notes_id": notes_id,
                    "detail": "Unknown Error Occurred or Note has been Deleted",
                }
            }
    print(to_send_ws_data)
    redis_publisher_serv(channel=str(user_id), data=to_send_ws_data)
