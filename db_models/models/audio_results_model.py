import datetime
import mongoengine
from db_models.models.user_model import UserModel
from db_models.models.notes_model import NotesModel
from db_models.models.audio_model import Audio


class AudioResultsModel(mongoengine.Document):
    user_id = mongoengine.ReferenceField(UserModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    notes_id = mongoengine.ReferenceField(NotesModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    audio_id = mongoengine.ReferenceField(Audio, reverse_delete_rule=mongoengine.CASCADE, required=True)
    url = mongoengine.URLField(required=True)
    blob_name = mongoengine.StringField()
    stt = mongoengine.StringField(default=None)
    sound_recog_results = mongoengine.ListField(default=None)
    forced_alignment_data = mongoengine.DictField(default=None)
    blob_size = mongoengine.FloatField()
    last_edited_date = mongoengine.DateField(default=datetime.datetime.now())
    meta = {
        'db_alias': 'core',
        'collection': 'audios_results'
    }
