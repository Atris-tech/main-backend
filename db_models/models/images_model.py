import mongoengine


class Image(mongoengine.Document):
    url = mongoengine.URLField(required=True)
    image_labels = mongoengine.ListField()
    image_ocr = mongoengine.StringField()
    image_size = mongoengine.FloatField()
    meta = {
        'db_alias': 'core',
        'collection': 'images'
    }