import typesense
import settings
from Services.summarization_api_call import summary_and_keywords_or_entity_api_call
import json


client = typesense.Client({
    'nodes': [{
        'host': settings.TYPESENSE_HOST,
        'port': '8108',
        'protocol': 'http'
    }],
    'api_key': settings.TYPESENSE_API_KEY,
    'connection_timeout_seconds': 5
})

data = client.collections[settings.TYPESENSE_NOTES_INDEX].documents['6069d522ab33f1969265049a'].retrieve()
print(type(data["clean_text"]))
print(data["clean_text"])
# print(summary_and_keywords_or_entity_api_call(, url="http://20.39.54.134:8005/get_summery/"))