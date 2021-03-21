import mongoengine
from .user_model import UserModel
from .workspace_model import WorkSpaceModel
from .canvas_model import Canvas
from .audio_model import Audio
from .images_model import Image
import datetime
import mongoengine_goodjson


class NotesModel(mongoengine.Document):
    user_id = mongoengine.ReferenceField(UserModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    workspace_id = mongoengine.ReferenceField(WorkSpaceModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    notes_name = mongoengine.StringField(default="untitled")
    tags = mongoengine.ListField(mongoengine.ReferenceField('TagModel'))
    note_blob_id = mongoengine.StringField(required=True)
    clean_text = mongoengine.StringField(default="", required=True)
    summary_data = mongoengine.StringField()
    key_words = mongoengine.ListField()
    entity_data = mongoengine.DictField()
    canvases = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Canvas))
    images = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Image))
    audios = mongoengine.ListField(mongoengine.ReferenceField(Audio))
    last_edited_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    note_size = mongoengine.FloatField(default=0)

    meta = {
        'db_alias': 'core',
        'collection': 'notes'
    }