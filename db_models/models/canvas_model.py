import mongoengine


class Canvas(mongoengine.EmbeddedDocument):
    content = mongoengine.DictField(required=True)
    name = mongoengine.StringField(max_length=120)
    canvas_size = mongoengine.FloatField()
