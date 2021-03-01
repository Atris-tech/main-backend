from Services.redis_service import get_val
import urllib.request
from Services.stt_api_call_service import stt_api_call
from tasks.audio_file_upload_rq_task import audio_save_to_db
import os
import uuid
import shutil
from db_models.models.notes_model import NotesModel


def audio_preprocess(file_url,  note_id, file_name, blob_size):
    new_folder = "Upload/" + str(uuid.uuid4())
    os.mkdir(new_folder)
    filedata = urllib.request.urlopen(file_url)
    to_save_file_name = new_folder + "/" + str(uuid.uuid4()) + file_name
    with open(to_save_file_name, 'wb') as f:
        f.write(filedata.read())
    stt_end_point = get_val(key="STT_UPLOAD_URL")
    f_align_end_point = get_val(key="FORCED_ALIGN_UPLOAD_URL")
    sound_recog_endpoint = get_val(key="SOUND_RECOG_ENDPOINT")
    stt_data = stt_api_call(file_to_process=to_save_file_name, stt_end_point=stt_end_point,
                            f_align_end_point=f_align_end_point, sound_recog_endpoint=sound_recog_endpoint)
    shutil.rmtree(new_folder)
    notes_obj = NotesModel.objects.get(id=note_id)
    audio_save_to_db(file_size=blob_size, stt_data=stt_data, note_obj=notes_obj, url=file_url)