import typesense

client = typesense.Client({
    'nodes': [{
        'host': "52.188.18.233",
        'port': '8108',
        'protocol': 'http'
    }],
    'api_key': "a882fbadb8add13fcfdf347c43c5f3e8acb71076fa76c59c04b03a7710939816895b8ac45bab80d1d3e67adc4e8d3a44ce38805e10aaada0e49b979a874c6801",
    'connection_timeout_seconds': 5
})


TYPESENSE_NOTES_INDEX = "atris_notes_index"
TYPESENSE_IMAGES_INDEX = "atris_images_index"
TYPESENSE_AUDIO_INDEX = "atris_audio_index"

notes_schema = {
    'name': TYPESENSE_NOTES_INDEX,
    'fields': [
        {'name': 'id', 'type': 'string'},
        {'name': 'user_id', 'type': 'string'},
        {'name': 'date', 'type': 'int32'},
        {'name': 'clean_text', 'type': 'string'},
        {'name': 'summary', 'type': 'string'}
    ],
    'default_sorting_field': 'date'
}

print(client.collections.create(notes_schema))

images_schema = {
    'name': TYPESENSE_IMAGES_INDEX,
    'fields': [
        {'name': 'id', 'type': 'string'},
        {'name': 'user_id', 'type': 'string'},
        {'name': 'date', 'type': 'int32'},
        {'name': 'notes_id', 'type': 'string'},
        {'name': 'ocr', 'type': 'string'},
        {'name': 'labels', 'type': 'string[]'}
    ],
    'default_sorting_field': 'date'
}
print(client.collections.create(images_schema))
audio_schema = {
    'name': TYPESENSE_AUDIO_INDEX,
    'fields': [
        {'name': 'id', 'type': 'string'},
        {'name': 'user_id', 'type': 'string'},
        {'name': 'date', 'type': 'int32'},
        {'name': 'notes_id', 'type': 'string'},
        {'name': 'transcribe', 'type': 'string'},
        {'name': 'sound_recog', 'type': 'string[]'}
    ],
    'default_sorting_field': 'date'
}
print(client.collections.create(audio_schema))
