import mongoengine
from .user_model import UserModel
from db_models.models.cache_display_model import CacheModel


class TagModel(mongoengine.Document):
    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        print("tag_model_called")
    user_id = mongoengine.ReferenceField(UserModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    tag_name = mongoengine.StringField(max_length=None, default=None)
    notes = mongoengine.ListField(mongoengine.ReferenceField(CacheModel))
    count = mongoengine.IntField(default=0)
    meta = {
        'db_alias': 'core',
        'collection': 'tags'
    }
