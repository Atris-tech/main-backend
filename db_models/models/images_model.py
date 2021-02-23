import mongoengine


class Image(mongoengine.EmbeddedDocument):
    url = mongoengine.URLField(required=True)
    image_captions = mongoengine.ListField()
    image_ocr = mongoengine.StringField()