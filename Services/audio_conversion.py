import os
import subprocess
import uuid
from settings import MIME_TYPES_AUDIO
import magic


def check_mime_type(file):
    mime_type = magic.from_file(file, mime=True)
    file_extension = None
    for key, val in MIME_TYPES_AUDIO.items():
        if str(mime_type) == val:
            file_extension = key
            return file_extension
    return file_extension


def convert_audio_handler(file, remove_file=False):
    file_extension = check_mime_type(file)
    if file_extension is not None:
        converted_file = convert_audio(source_format=file_extension, file=file)
        if remove_file:
            os.remove(file)
        return converted_file
    else:
        if remove_file:
            os.remove(file)
        return None


def convert_audio(source_format, file):
    if source_format == "wav":
        pass
    else:
        target_file = str(uuid.uuid4()) + ".wav"
        if source_format == "mp3" or source_format == "aiff":
            subprocess.call(["sox", file, target_file])
        elif source_format == "m4a" or source_format == "aac":
            subprocess.call(["ffmpeg", "-i", file, target_file])
        os.remove(file)
        return target_file
