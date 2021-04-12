import datetime

import mongoengine

from .user_model import UserModel


class TokenModel(mongoengine.Document):
    user = mongoengine.ReferenceField(UserModel)
    refresh_token = mongoengine.StringField()
    datetime = mongoengine.DateTimeField(default=datetime.datetime.now())
    token_status = mongoengine.StringField(default="Alive")

    meta = {
        'db_alias': 'core',
        'collection': 'tokens'
    }
