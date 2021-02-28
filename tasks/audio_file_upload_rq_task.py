import uuid
from Services.audio_conversion import convert_audio_handler
from Services.storage_services import upload_file_blob_storage, delete_blob
from db_models.models.audio_model import Audio
from db_models.models.notes_model import NotesModel
from pathlib import Path
import os
import urllib.request


def audio_upload(container_id, stt_data, note_id, file=False, url=False, file_name=False):
    if url:
        new_folder = "Upload/" + str(uuid.uuid4())
        os.mkdir(new_folder)
        filedata = urllib.request.urlopen(url)
        to_save_file_name = new_folder + "/" + str(uuid.uuid4()) + file_name
        with open(to_save_file_name, 'wb') as f:
            f.write(filedata.read())
        target_file = convert_audio_handler(to_save_file_name, remove_file=True)
        os.rmdir(new_folder)
        delete_blob(container_name=container_id, blob_name=file_name)
    else:
        target_file = convert_audio_handler(file, remove_file=True)
    target_file_pathlib_obj = Path(target_file)
    target_file_name = target_file_pathlib_obj.name
    target_file_size = target_file_pathlib_obj.stat().st_size
    if target_file is not None:
        blob_data = upload_file_blob_storage(file_name=target_file_name, file_data=target_file,
                                             container_name=container_id)
        stt = stt_data["transcribe"]
        sound_recog = stt_data["sound_recog_results"]
        f_align_data = stt_data["f_align"]
        audio_model_obj = Audio(url=blob_data["url"], blob_name=target_file_name, blob_size=target_file_size,
                                sound_recog_results=sound_recog, forced_alignment_data=f_align_data, stt=stt)
        notes_model_obj = NotesModel.objects.get(id=note_id)
        notes_model_obj.audios.append(audio_model_obj)
        notes_model_obj.save()
