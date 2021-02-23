import mongoengine


class Canvas(mongoengine.EmbeddedDocument):
    content = mongoengine.DictField(required=True)
    name = mongoengine.StringField(max_length=120)