import mongoengine


class Canvas(mongoengine.Document):
    content = mongoengine.DictField(required=True)
    name = mongoengine.StringField(max_length=120)
    canvas_size = mongoengine.FloatField()
    meta = {
        'db_alias': 'core',
        'collection': 'scribles'
    }
