import mongoengine
from .user_model import UserModel
from .workspace_model import WorkSpaceModel
from .tags_model import TagModel
from .canvas_model import Canvas
from .audio_model import Audio
from .images_model import Image
import datetime


class NotesModel(mongoengine.Document):
    user_id = mongoengine.ReferenceField(UserModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    workspace_id = mongoengine.ReferenceField(WorkSpaceModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    notes_name = mongoengine.StringField(default="untitled")
    tags = mongoengine.ListField(mongoengine.ReferenceField(TagModel))
    data = mongoengine.DictField(required=True)
    clean_text = mongoengine.StringField(required=True)
    summary_data = mongoengine.StringField()
    key_words = mongoengine.ListField()
    entity_data = mongoengine.DictField()
    canvases = mongoengine.ListField(mongoengine.EmbeddedDocument(Canvas))
    images = mongoengine.ListField(mongoengine.EmbeddedDocument(Image))
    audios = mongoengine.ListField(mongoengine.EmbeddedDocument(Audio))
    last_edited_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    note_size = mongoengine.FloatField()
    meta = {
        'db_alias': 'core',
        'collection': 'notes'
    }