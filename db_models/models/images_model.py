import datetime

import mongoengine

from db_models.models import NotesModel
from db_models.models.user_model import UserModel


class Image(mongoengine.Document):
    user_id = mongoengine.ReferenceField(UserModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    notes_id = mongoengine.ReferenceField(NotesModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    image_size = mongoengine.FloatField()
    blob_name = mongoengine.StringField()
    last_edited_date = mongoengine.DateField(default=datetime.datetime.now())
    meta = {
        'db_alias': 'core',
        'collection': 'images'
    }
