from fastapi import Request, APIRouter, HTTPException
from mongoengine import Q
from Services.auth.auth_services import token_check
from db_models.models import NotesModel
from db_models.models.user_model import UserModel
from error_constants import BadRequest
from task_worker_config.celery import app
from .models import SmmryEntityModel
from Services.redis_service import get_val


router = APIRouter()


def entity_emotion_call(request: Request, smmry_reqst_obj: SmmryEntityModel):
    user_dict = token_check(request)
    user_obj = UserModel.objects.get(email_id=user_dict["email_id"])
    try:
        notes_obj = NotesModel.objects.get(Q(user_id=user_obj) & Q(id=smmry_reqst_obj.notes_id))
        EMOTION_ANALYSIS_ENDPOINT = get_val(key="EMOTION_ANALYSIS_ENDPOINT")
        ENTITY_ENDPOINT = get_val(key="ENTITY_ENDPOINT")
        app.send_task("tasks.entity_emotion_task.generate_entity_emotion",
                      queue="entity_queue",
                      kwargs={
                          "entity_endpoint": str(ENTITY_ENDPOINT),
                          "note_id": str(notes_obj.id),
                          "emotion_endpoint": str(EMOTION_ANALYSIS_ENDPOINT)
                      })
    except NotesModel.DoesNotExist:
        raise HTTPException(
            status_code=BadRequest.code,
            detail=BadRequest.detail
        )
