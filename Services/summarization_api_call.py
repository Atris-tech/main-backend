import requests
import json
from settings import MICRO_SERVICES_ACCESS_TOKEN
import base64


def summary_and_keywords_or_entity_api_call(text, url):
    encoded = base64.b64encode(text.encode('utf8'))
    b64_string_txt = str(encoded, "utf-8")
    payload = {
        "text": b64_string_txt
    }
    headers = {
        'Authorization': 'Bearer ' + MICRO_SERVICES_ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return json.loads(response.text)


