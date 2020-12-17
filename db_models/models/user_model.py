import mongoengine
import datetime


class UserModel(mongoengine.Document):
    user_name = mongoengine.StringField(required=True)
    first_name = mongoengine.StringField(required=True)
    last_name = mongoengine.StringField(required=True)
    image = mongoengine.StringField()
    account_type = mongoengine.StringField(required=True)
    password_hash = mongoengine.StringField()
    account_created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    meta = {
        'db_alias': 'core',
        'collection': 'users'
    }