from task_worker_config.celery import app
from Services.summarization_api_call import summary_and_keywords_or_entity_api_call
from Services.type_sense.type_sense_crud_service import get_collection
from settings import TYPESENSE_NOTES_INDEX
from db_models.models.notes_model import NotesModel
from db_models.models.cache_display_model import CacheModel


@app.task(soft_time_limit=500, max_retries=3)
def summary_task(notes_id, summary_api_endpoint):
    try:
        notes_model_obj = NotesModel.objects.get(id=notes_id)
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
    except NotesModel.objects.DoesNotExist:
        print("the person deleted the note")

