from Services.summarization_api_call import summary_and_keywords_or_entity_api_call
from Services.type_sense.type_sense_crud_service import get_collection
from db_models.models import NotesModel
from settings import TYPESENSE_NOTES_INDEX
from task_worker_config.celery import app
from db_models.mongo_setup import global_init

global_init()


@app.task(soft_time_limit=500, max_retries=3)
def generate_entity_emotion(notes_id, entity_endpoint, emotion_endpoint):
    try:
        notes_model_obj = NotesModel.objects.get(id=notes_id)
        notes_data = get_collection(index=TYPESENSE_NOTES_INDEX, id=notes_id)
        clean_text = notes_data["clean_text"]
        entity_data = summary_and_keywords_or_entity_api_call(text=clean_text, url=entity_endpoint)
        emotion = summary_and_keywords_or_entity_api_call(text=clean_text, url=emotion_endpoint)
        notes_model_obj.emotion = emotion
        notes_model_obj.entity_data = entity_data
        notes_model_obj.save()
    except NotesModel.DoesNotExist:
        print("the person deleted the note")
