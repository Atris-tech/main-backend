import mongoengine


class Audio(mongoengine.EmbeddedDocument):
    url = mongoengine.URLField(required=True)
    name = mongoengine.URLField(default="untitled")
    blob_name = mongoengine.StringField()
    stt = mongoengine.StringField()
    sound_recog_results = mongoengine.ListField()
    forced_alignment_data = mongoengine.DictField()
    blob_size = mongoengine.FloatField()