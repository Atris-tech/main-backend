from mongoengine import Q
from fastapi import HTTPException
from error_constants import BadRequest, EntityLengthError
from db_models.models.notes_model import NotesModel
from db_models.models.cache_display_model import CacheModel
from Services.type_sense.type_sense_crud_service import get_collection, update_collection
from Services.type_sense.typesense_dic_generator import generate_typsns_data
from settings import TYPESENSE_NOTES_INDEX, NOTES_SUMMARY_DIFFERENCE_THRESHOLD, MAX_SUMMARY_ENTITY_LENGTH
from Services.notes.notes_saving_service import generate_summary_from_clean_text
from task_worker_config.celery import app
from Services.redis_service import get_val


def handle_summary(user_obj, smmry_reqst_obj):
    try:
        notes_obj = NotesModel.objects.get(Q(user_id=user_obj) & Q(id=smmry_reqst_obj.notes_id))
        print(str(notes_obj.id))
        notes_data = get_collection(index=TYPESENSE_NOTES_INDEX, id=str(notes_obj.id))
        # print(notes_data)
        if smmry_reqst_obj.summary:
            print("mannual summary")
            print(smmry_reqst_obj.summary)
            if notes_data is None:
                tps_data = generate_typsns_data(obj=notes_obj, summary=smmry_reqst_obj.summary, clean_text="",
                                     notes_name=notes_obj.notes_name)
            else:
                tps_data = generate_typsns_data(obj=notes_obj, summary=smmry_reqst_obj.summary, notes_name=notes_obj.notes_name,
                                     clean_text=notes_data["clean_text"])

            update_collection(index=TYPESENSE_NOTES_INDEX, data=tps_data)
            notes_obj.uds = "MANUAL"
            notes_obj.save()
            cache_display_model = CacheModel.objects.get(notes_id=notes_obj)
            cache_display_model.uds = "MANUAL"
            cache_display_model.cache_notes_summary = generate_summary_from_clean_text(
                clean_txt=notes_data["clean_text"])
            cache_display_model.save()
        else:
            print("ai summary")
            "AI SUMMARY"
            if notes_data is None:
                length_violation = EntityLengthError(entity="notes_length", your_length=0, min_length=True, empty=True)
                raise HTTPException(
                    status_code=length_violation.code,
                    detail=length_violation.detail
                )
            else:
                print(len(notes_data["clean_text"]))
                if len(notes_data["clean_text"]) < NOTES_SUMMARY_DIFFERENCE_THRESHOLD:
                    print("min thresh")
                    length_violation = EntityLengthError(entity="notes_length", your_length=0, min_length=True,
                                                         empty=True)
                    raise HTTPException(
                        status_code=length_violation.code,
                        detail=length_violation.detail
                    )
                elif len(notes_data["clean_text"]) > MAX_SUMMARY_ENTITY_LENGTH:
                    print("max thresh")
                    length_violation = EntityLengthError(entity="notes_length",
                                                         your_length=len(notes_data["clean_text"]),
                                                         length=MAX_SUMMARY_ENTITY_LENGTH)
                    raise HTTPException(
                        status_code=length_violation.code,
                        detail=length_violation.detail
                    )
                else:
                    url = get_val(key="SUMMARY_KEYWORDS_ENDPOINT")
                    """generate_summary_from_clean_text"""
                    app.send_task("tasks.summary_keyword_task.summary_task",
                                  queue="summary_queue",
                                  kwargs={
                                      "summary_api_endpoint": str(url),
                                      "notes_id": str(notes_obj.id),
                                      "user_id": str(user_obj.id)
                                  })

    except NotesModel.DoesNotExist:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )
