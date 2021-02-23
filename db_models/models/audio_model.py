import mongoengine


class Audio(mongoengine.EmbeddedDocument):
    url = mongoengine.URLField(required=True)
    name = mongoengine.URLField(default="untitled")
    sound_recog_results = mongoengine.DictField()
    forced_alignment_data = mongoengine.DictField()