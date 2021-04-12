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

updated = {
    'id': '4545452343111',
    'user_id': '12345a',
    'title': 'I am updated1',
    'date': 12244
}

print(client.collections['notes11'].documents['4545452343111'].update(updated))
