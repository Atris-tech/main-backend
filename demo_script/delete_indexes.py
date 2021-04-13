import typesense

import settings

client = typesense.Client({
    'nodes': [{
        'host': settings.TYPESENSE_HOST,
        'port': '8108',
        'protocol': 'http'
    }],
    'api_key': settings.TYPESENSE_API_KEY,
    'connection_timeout_seconds': 5
})


if __name__ == '__main__':
    try:
        client.collections[settings.TYPESENSE_NOTES_INDEX].delete()
    except typesense.exceptions.ObjectNotFound:
        pass
    try:
        client.collections[settings.TYPESENSE_AUDIO_INDEX].delete()
    except typesense.exceptions.ObjectNotFound:
        pass
    try:
        client.collections[settings.TYPESENSE_IMAGES_INDEX].delete()
    except typesense.exceptions.ObjectNotFound:
        pass