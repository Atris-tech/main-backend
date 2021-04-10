import mongoengine
import datetime
import settings


class UserModel(mongoengine.Document):
    user_name = mongoengine.StringField(required=True)
    email_id = mongoengine.StringField(required=True)
    first_name = mongoengine.StringField(required=True)
    last_name = mongoengine.StringField()
    image = mongoengine.StringField()
    account_type = mongoengine.StringField(required=True)
    password_hash = mongoengine.StringField()
    account_created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    verified = mongoengine.BooleanField(default=False)
    plan = mongoengine.StringField(required=True, default="Free")
    space = mongoengine.FloatField(default=settings.MAX_FREE_ACCOUNT_USER_SPACE)
    space_occupied = mongoengine.FloatField(default=0)
    user_storage_notes_container_name = mongoengine.StringField()
    user_storage_container_name = mongoengine.StringField()
    meta = {
        'db_alias': 'core',
        'collection': 'users'
    }
