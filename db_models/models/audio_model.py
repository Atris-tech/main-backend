import mongoengine


class Audio(mongoengine.Document):
    url = mongoengine.URLField(required=True)
    name = mongoengine.StringField(default="untitled")
    blob_name = mongoengine.StringField()
    stt = mongoengine.StringField()
    sound_recog_results = mongoengine.ListField()
    forced_alignment_data = mongoengine.DictField()
    blob_size = mongoengine.FloatField()
    meta = {
        'db_alias': 'core',
        'collection': 'audios'
    }