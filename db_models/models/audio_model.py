import mongoengine

from db_models.models.notes_model import NotesModel
from db_models.models.user_model import UserModel


class Audio(mongoengine.Document):
    user_id = mongoengine.ReferenceField(UserModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    notes_id = mongoengine.ReferenceField(NotesModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    y_axis = mongoengine.StringField(default=None)
    name = mongoengine.StringField(default="untitled")
    meta = {
        'db_alias': 'core',
        'collection': 'audios'
    }
