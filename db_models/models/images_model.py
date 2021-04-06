import datetime
import mongoengine
from db_models.models.user_model import UserModel


class Image(mongoengine.Document):
    user_id = mongoengine.ReferenceField(UserModel, reverse_delete_rule=mongoengine.CASCADE, required=True)
    url = mongoengine.URLField(required=True)
    image_size = mongoengine.FloatField()
    last_edited_date = mongoengine.DateField(default=datetime.datetime.now())
    meta = {
        'db_alias': 'core',
        'collection': 'images'
    }
