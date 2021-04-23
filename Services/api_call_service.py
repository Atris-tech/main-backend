import json
from pathlib import Path

import requests

from settings import MICRO_SERVICES_ACCESS_TOKEN


def api_call(file_to_process, end_point=False, f_align_end_point=False, sound_recog_endpoint=False, binary=False,
             file_name=False, no_payload=False, status=False, image=False):
    if not no_payload:
        print("in api call")
        payload = {'f_align_url': f_align_end_point,
                   'sound_recog_url': sound_recog_endpoint
                   }
        headers = {
            'Authorization': 'Bearer ' + MICRO_SERVICES_ACCESS_TOKEN,
        }
        print("PAYLOAD")
        print(payload)
    if binary:
        if image:
            print("in if")
            files = [
                ('image', (file_name, file_to_process, 'application/octet-stream'))
            ]
        else:
            print("in if")
            files = [
                ('file', (file_name, file_to_process, 'application/octet-stream'))
            ]
    else:
        print("in api else")
        print(str(Path(file_to_process).name))
        files = [
            ('file', (str(Path(file_to_process).name), open(file_to_process, 'rb'), 'application/octet-stream'))
        ]
    if not no_payload:
        response = requests.request("POST", end_point, data=payload, files=files, headers=headers)
        print("##################RESPONSE###############################")
    else:
        response = requests.request("POST", end_point, files=files, headers=headers)
    if status:
        return {
            "response_data": json.loads(response.text),
            "status_code": response.status_code
        }
    return json.loads(response.text)
