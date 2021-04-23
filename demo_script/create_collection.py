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

books_schema = {
    'name': 'notes11',
    'fields': [
        {'name': 'title', 'type': 'string'},
        {'name': 'id', 'type': 'string'},
        {'name': 'user_id', 'type': 'string', "facet": True},
        {'name': 'date', 'type': 'int32'},
    ],
    'default_sorting_field': 'date'
}

print(client.collections.create(books_schema))
