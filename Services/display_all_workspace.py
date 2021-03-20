from db_models.models.workspace_model import WorkSpaceModel
from db_models.models.user_model import UserModel
import json


def display_workspace_catch(email):
    user_obj = UserModel.objects.get(email_id=email)
    cache_model_objs = WorkSpaceModel.objects.filter(user_id=user_obj)
    data = cache_model_objs.to_json()
    return json.loads(data)