import mongoengine
from .user_model import UserModel
from .workspace_model import WorkSpaceModel
import datetime
import mongoengine_goodjson as gj


class NotesModel(gj.Document):
    user_id = mongoengine.ReferenceField(UserModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    workspace_id = mongoengine.ReferenceField(WorkSpaceModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    notes_name = mongoengine.StringField(default="untitled")
    tags = mongoengine.ListField(mongoengine.ReferenceField('TagModel'))
    tags_name = mongoengine.ListField()
    note_blob_id = mongoengine.StringField(required=True)
    key_words = mongoengine.ListField()
    entity_data = mongoengine.DictField()
    last_edited_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    note_size = mongoengine.FloatField(default=0)
    difference = mongoengine.FloatField(default=0)
    emotion = mongoengine.StringField()
    summary = mongoengine.StringField()
    uds = mongoengine.StringField(default="False")
    # uds ==> User Defined Summary
    # AUTO if user has generated an ai summary
    # MANUAL -> manually added one
    # False -> Never Generated Summary

    meta = {
        'db_alias': 'core',
        'collection': 'notes'
    }
