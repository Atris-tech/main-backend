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

search_requests = {
    'searches': [
        {
            'collection': 'notes11',
            'q': 'test',
            'filter_by': 'user_id:=12345a'
        }
    ]
}

common_search_params = {
    'query_by': ['title']
}

print(client.multi_search.perform(search_requests, common_search_params))
