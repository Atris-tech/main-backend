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

data = [
    {
        'id': '4545452343111',
        'user_id': '12345a',
        'title': 'test me',
        'date': 12244
    },
    {
        'id': '45324235454524',
        'user_id': '12345a',
        'title': 'new12 sad',
        'date': 12245
    },
    {
        'id': '45432454577524111',
        'user_id': '12346b',
        'title': 'test1 fd',
        'date': 12244
    }
]

for dic in data:
    print(client.collections['notes11'].documents.create(dic))
