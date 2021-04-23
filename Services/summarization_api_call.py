import base64
import json

import requests

from settings import MICRO_SERVICES_ACCESS_TOKEN


def summary_and_keywords_or_entity_api_call(text, url):
    encoded = base64.b64encode(text.encode('utf8'))
    b64_string_txt = str(encoded, "utf-8")
    payload = json.dumps({
        "text": b64_string_txt
    })
    headers = {
        'Authorization': 'Bearer ' + MICRO_SERVICES_ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)
