import os
import warnings
warnings.filterwarnings('ignore')
import nemo.collections.asr as nemo_asr
from nemo.collections import nlp as nemo_nlp
from fastapi import FastAPI, File, UploadFile, Form
import subprocess
import magic
import uuid
import requests
import json


app = FastAPI(host='0.0.0.0', port = 8080)


MIME_TYPES_AUDIO = {
    "mp3": "audio/mpeg",
    "wav": "audio/x-wav",
    "m4a": "video/mp4",
    "aiff": "audio/x-aiff",
    "aac": "audio/x-hx-aac-adts"
}

# Instantiate pre-trained NeMo models
# Speech Recognition model - QuartzNet
jasper = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name="Jasper10x5Dr-En").cuda()
# Punctuation and capitalization model
punctuation = nemo_nlp.models.PunctuationCapitalizationModel.from_pretrained(model_name='Punctuation_Capitalization_with_DistilBERT').cuda()


def convert_audio(source_format, file):
    target_file = str(uuid.uuid4()) + ".wav"
    if source_format == "wav":
        subprocess.call(["sox", file, "-r", "16000", "-c", "1", target_file])
    elif source_format == "mp3":
        subprocess.call(["sox", file, "-r", "16000", "-c", "1", target_file])
    elif source_format == "m4a":
        subprocess.call(["ffmpeg", "-i", file, "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", target_file])
    elif source_format == "aiff":
        subprocess.call(["sox", file, "-r", "16000", "-c", "1", target_file])
    elif source_format == "aac":
        subprocess.call(["ffmpeg", "-i", file, "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", target_file])
    os.remove(file)
    return target_file



def check_mime_type(file):
    mime_type = magic.from_file(file, mime=True)
    file_extension = None
    for key, val in MIME_TYPES_AUDIO.items():
        if str(mime_type) == val:
            file_extension = key
            return file_extension
    return file_extension


def transcribe(file_name, f_align_url, sound_recog_url):
    # Convert our audio sample to text
    files = [file_name]
    raw_text = ''
    text = ''
    # for fname, transcription in zip(files, quartznet.transcribe(paths2audio_files=files)):
    #     raw_text = transcription
    raw_text = jasper.transcribe(paths2audio_files=files)[0]
    # Add capitalization and punctuation
    res = punctuation.add_punctuation_capitalization(queries=[raw_text])
    text = res[0]
    print(res)
    payload = {'transcript': text}
    files = [
      ('audio', (file_name, open(file_name, 'rb'), 'application/octet-stream'))
    ]
    response = requests.request("POST", f_align_url, data=payload, files=files)
    f_align = response.text

    files = [
        ('audio', (file_name, open(file_name, 'rb'), 'audio/wav'))
    ]

    response = requests.request("POST", sound_recog_url, files=files)

    sound_recog_results = response.text
    sound_recog_results = json.loads(sound_recog_results)
    sound_recog_predictions = list()
    for result in sound_recog_results["predictions"]:
        if result["probability"] > 0.4:
            sound_recog_predictions.append(result["label"])
    os.remove(file_name)
    return {"transcribe": text, "f_align": json.loads(f_align), "sound_recog_results": sound_recog_predictions}


@app.post("/uploadfile/")
def create_upload_file(file: UploadFile = File(...), f_align_url: str = Form(...), sound_recog_url: str = Form(...)):
    file_name = file.filename
    print(file_name)
    with open(file_name, 'wb') as f:
        f.write(file.file.read())
    file_extension = check_mime_type(file_name)
    if file_extension is not None:
        converted_file = convert_audio(source_format=file_extension, file=file_name)
        stt_data = transcribe(converted_file, f_align_url, sound_recog_url)
        return stt_data
    else:
        return False