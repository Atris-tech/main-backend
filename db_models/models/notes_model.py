import mongoengine
from .user_model import UserModel
from .workspace_model import WorkSpaceModel
from .tags_model import TagModel
import datetime


class NotesModel(mongoengine.Document):
    user_id = mongoengine.ReferenceField(UserModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    workspace_id = mongoengine.ReferenceField(WorkSpaceModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    notes_name = mongoengine.StringField(required=True)
    tags = mongoengine.ListField(mongoengine.ReferenceField(TagModel))
    data = mongoengine.DictField(required=True)
    clean_text = mongoengine.StringField(required=True)
    summary_data = mongoengine.StringField()
    key_words = mongoengine.ListField()
    entity_data = mongoengine.DictField()
    canvas_data = mongoengine.DictField()
    image_captions = mongoengine.ListField()
    image_ocr = mongoengine.StringField()
    sound_recog_results = mongoengine.DictField()
    forced_alignment_data = mongoengine.DictField()
    last_edited_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    meta = {
        'db_alias': 'core',
        'collection': 'notes'
    }
