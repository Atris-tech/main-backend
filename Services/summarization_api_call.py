import requests
import json
from settings import MICRO_SERVICES_ACCESS_TOKEN


def summary_and_keywords_or_entity_api_call(text, url):
    payload = {
        "text": text
    }
    headers = {
        'Authorization': 'Bearer ' + MICRO_SERVICES_ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return json.loads(response.text)


