import requests
import json
from Services.redis_service import get_val
import urllib.request
import uuid
import os


def audio_preprocess(file_url):

    url = get_val(key="STT_UPLOAD_URL")

    payload = {
        "url": file_url
    }
    payload = json.dumps(payload)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    stt_text = response.text

    url = get_val(key="FORCED_ALIGN_UPLOAD_URL")

    payload = {'transcript': stt_text}
    filedata = urllib.request.urlopen(file_url)
    file_name = str(uuid.uuid4()) + os.path.basename(filedata.geturl())
    print(file_name)
    with open(file_name, 'wb') as f:
        f.write(filedata.read())
    files = [
      ('audio', ('1.m4a', filedata.read(), 'application/octet-stream'))
    ]
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
