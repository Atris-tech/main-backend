import mongoengine
import datetime
from settings import DEFAULT_PROFILE_PIC


class UserModel(mongoengine.Document):
    user_name = mongoengine.StringField(required=True)
    email_id = mongoengine.StringField(required=True)
    first_name = mongoengine.StringField(required=True)
    last_name = mongoengine.StringField(required=True)
    image = mongoengine.StringField(default=DEFAULT_PROFILE_PIC)
    account_type = mongoengine.StringField(required=True)
    password_hash = mongoengine.StringField()
    account_created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    meta = {
        'db_alias': 'core',
        'collection': 'users'
    }