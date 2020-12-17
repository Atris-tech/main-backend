import mongoengine
import datetime
from .user_model import UserModel
from .workspace_model import WorkSpaceModel
from .tags_model import TagModel
from .notes_model import NotesModel


class CacheModel(mongoengine.Document):
    notes_name = mongoengine.StringField(required=True)
    user_id = mongoengine.ReferenceField(UserModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    workspace_id = mongoengine.ReferenceField(WorkSpaceModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    notes_id = mongoengine.ReferenceField(NotesModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    cache_notes_summary = mongoengine.StringField() # can be summary text or for small text, actual text
    tags = mongoengine.ListField(mongoengine.ReferenceField(TagModel))
    # text = mongoengine.StringField(max_length=None, default=None)
    audio_url = mongoengine.StringField()
    forced_alignment_for_first_audio = mongoengine.DictField()
    last_edited_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    meta = {
        'db_alias': 'core',
        'collection': 'cache'
    }
