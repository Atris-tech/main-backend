import requests
from pathlib import Path
import json


def stt_api_call(file_to_process, stt_end_point, f_align_end_point, sound_recog_endpoint, binary=False, file_name=False):
    print("in api call")
    payload = {'f_align_url': f_align_end_point,
               'sound_recog_url': sound_recog_endpoint
               }
    if binary:
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
    response = requests.request("POST", stt_end_point, data=payload, files=files)
    print("##################RESPONSE###############################")
    print(response.text)
    return json.loads(response.text)
