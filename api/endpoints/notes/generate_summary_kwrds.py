from fastapi import Request, APIRouter

from Services.auth.auth_services import token_check
from Services.notes.summary_management_service import handle_summary
from db_models.models.user_model import UserModel
from .models import SmmryEntityModel

router = APIRouter()


@router.post("/gen_smry_kwrds/", status_code=200)
def gen_smmry_kwrds(request: Request, smmry_reqst_obj: SmmryEntityModel):
    user_dict = token_check(request)
    user_obj = UserModel.objects.get(email_id=user_dict["email_id"])
    return handle_summary(user_obj, smmry_reqst_obj)
