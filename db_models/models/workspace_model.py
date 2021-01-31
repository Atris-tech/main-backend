import mongoengine
from .user_model import UserModel
import datetime


class WorkSpaceModel(mongoengine.Document):
    user_id = mongoengine.ReferenceField(UserModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    work_space_name = mongoengine.StringField(required=True, default="home")
    work_space_emoji = mongoengine.StringField(required=True)
    date = mongoengine.DateTimeField(default=datetime.datetime.now)
    meta = {
        'db_alias': 'core',
        'collection': 'workspaces'
    }
