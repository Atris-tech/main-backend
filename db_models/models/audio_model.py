import datetime
import mongoengine
from db_models.models.user_model import UserModel
from db_models.models.notes_model import NotesModel


class Audio(mongoengine.Document):
    user_id = mongoengine.ReferenceField(UserModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    notes_id = mongoengine.ReferenceField(NotesModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    y_axis = mongoengine.StringField(default=None)
    url = mongoengine.URLField(required=True)
    name = mongoengine.StringField(default="untitled")
    blob_name = mongoengine.StringField()
    stt = mongoengine.StringField(default=None)
    sound_recog_results = mongoengine.ListField(default=None)
    forced_alignment_data = mongoengine.DictField(default=None)
    blob_size = mongoengine.FloatField()
    last_edited_date = mongoengine.DateField(default=datetime.datetime.now())
    meta = {
        'db_alias': 'core',
        'collection': 'audios'
    }