import os
import subprocess
import uuid


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