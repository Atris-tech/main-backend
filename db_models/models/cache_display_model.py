import mongoengine
import datetime
from .user_model import UserModel
from .workspace_model import WorkSpaceModel
from db_models.models import NotesModel
import mongoengine_goodjson as gj


class CacheModel(gj.Document):
    notes_name = mongoengine.StringField(required=True)
    user_id = mongoengine.ReferenceField(UserModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    workspace_id = mongoengine.ReferenceField(WorkSpaceModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    notes_id = mongoengine.ReferenceField(NotesModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    cache_notes_summary = mongoengine.StringField()
    tags = mongoengine.ListField(mongoengine.ReferenceField('TagModel'))
    tags_name = mongoengine.ListField()
    audio_url = mongoengine.StringField()
    forced_alignment_for_first_audio = mongoengine.DictField()
    last_edited_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    uds = mongoengine.StringField(default="False")
    # uds ==> User Defined Summary
    # AUTO if user has generated an ai summary
    # MANUAL -> manually added one
    # False -> Never Generated Summary
    meta = {
        'db_alias': 'core',
        'collection': 'cache'
    }
