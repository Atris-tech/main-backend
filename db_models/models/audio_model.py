import mongoengine


class Audio(mongoengine.Document):
    url = mongoengine.URLField(required=True)
    name = mongoengine.StringField(default="untitled")
    blob_name = mongoengine.StringField()
    stt = mongoengine.StringField(default=None)
    sound_recog_results = mongoengine.ListField(default=None)
    forced_alignment_data = mongoengine.DictField(default=None)
    blob_size = mongoengine.FloatField()
    meta = {
        'db_alias': 'core',
        'collection': 'audios'
    }