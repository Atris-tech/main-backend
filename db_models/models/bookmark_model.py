import mongoengine

from db_models.models.cache_display_model import CacheModel
from db_models.models.user_model import UserModel


class BookMarkModel(mongoengine.Document):
    user_id = mongoengine.ReferenceField(UserModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    cache_id = mongoengine.ReferenceField(CacheModel, reverse_delete_rule=mongoengine.CASCADE, required=True)

    meta = {
        'db_alias': 'core',
        'collection': 'bookmarks'
    }
