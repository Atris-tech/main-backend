import os
import warnings
warnings.filterwarnings('ignore')
import nemo.collections.asr as nemo_asr
import urllib.request
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
import subprocess
import magic
import uuid

app = FastAPI(host = '0.0.0.0', port = 8080)


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
#punctuation = nemo_nlp.models.PunctuationCapitalizationModel.from_pretrained(model_name='Punctuation_Capitalization_with_DistilBERT').cuda()


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


def transcribe(file_name):
    # Convert our audio sample to text
    files = [file_name]
    raw_text = ''
    text = ''
    # for fname, transcription in zip(files, quartznet.transcribe(paths2audio_files=files)):
    #     raw_text = transcription
    raw_text = jasper.transcribe(paths2audio_files=files)[0]
    # Add capitalization and punctuation
    # res = punctuation.add_punctuation_capitalization(queries=[raw_text])
    # text = res[0]
    os.remove(file_name)
    return raw_text


class File(BaseModel):
    url: HttpUrl


@app.post("/uploadfile/")
def create_upload_file(url_obj: File):
    filedata = urllib.request.urlopen(url_obj.url)
    file_name = str(uuid.uuid4()) + os.path.basename(filedata.geturl())
    print(file_name)
    with open(file_name, 'wb') as f:
        f.write(filedata.read())
    file_extension = check_mime_type(file_name)
    if file_extension is not None:
        converted_file = convert_audio(source_format=file_extension, file=file_name)
        stt_data = transcribe(converted_file)
        return stt_data
    else:
        return False