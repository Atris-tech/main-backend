import datetime

import mongoengine

from db_models.models import NotesModel
from db_models.models.user_model import UserModel


class Scribbles(mongoengine.Document):
    user_id = mongoengine.ReferenceField(UserModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    note_id = mongoengine.ReferenceField(NotesModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    blob_name = mongoengine.StringField(required=True)
    name = mongoengine.StringField(max_length=120, default="untitled")
    canvas_size = mongoengine.FloatField()
    y_axis = mongoengine.FloatField()
    last_edited_date = mongoengine.DateField(default=datetime.datetime.now())
    meta = {
        'db_alias': 'core',
        'collection': 'scribbles'
    }
