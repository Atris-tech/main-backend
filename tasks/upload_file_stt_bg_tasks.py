import uuid
from Services.storage_services import upload_file_blob_storage
from Services.stt_api_call_service import stt_api_call
from redis import Redis
from settings import REDIS_PASSWORD, REDIS_HOSTNAME, REDIS_PORT
from rq import Queue
from tasks.audio_process_rq_task import audio_preprocess
from tasks.audio_file_upload_rq_task import audio_save_to_db
from Services.redis_service import get_list, get_val

redis_conn = Redis(
            host=REDIS_HOSTNAME,
            port=REDIS_PORT,
            password=REDIS_PASSWORD
        )


def upload_task(user_obj, file_data, file_name, notes_obj, blob_size):
    print("in upload task")
    file_name = str(uuid.uuid4()) + file_name
    data = upload_file_blob_storage(email=user_obj.email_id, file_data=file_data,
                                   file_name=file_name, bg=True)
    if data:
        print("in data")
        container_name = data["container_name"]
        url = data["url"]
        direct_api_supported_plans = get_list("DIRECT_STT_API_PLANS")
        if user_obj.plan in direct_api_supported_plans:
            stt_end_point = get_val(key="STT_UPLOAD_URL")
            f_align_end_point = get_val(key="FORCED_ALIGN_UPLOAD_URL")
            sound_recog_endpoint = get_val(key="SOUND_RECOG_ENDPOINT")
            stt_data = stt_api_call(stt_end_point=stt_end_point, file_to_process=file_data, file_name=file_name,
                                    binary=True, f_align_end_point=f_align_end_point,
                                    sound_recog_endpoint=sound_recog_endpoint)
            audio_save_to_db(file_size=blob_size, stt_data=stt_data, note_obj=notes_obj, url=url)
            """websocket code here"""
        else:
            q = Queue("Public", connection=redis_conn)
            job = q.enqueue_job(audio_preprocess, url, notes_obj.id, file_name, container_name)
