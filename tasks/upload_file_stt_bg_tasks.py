import uuid
from Services.storage_services import upload_file_blob_storage
from Services.stt_api_call_service import stt_api_call
from Services.audio_upload_helper import audio_save_to_db
from Services.redis_service import get_list, get_val
from task_worker_config.celery import app


def upload_task(user_obj, file_data, file_name, notes_obj, blob_size, audio_request_id):
    print("in upload task")
    file_name = str(uuid.uuid4()) + file_name
    data = upload_file_blob_storage(file_data=file_data, file_name=file_name, user_model_obj=user_obj)
    print("data")
    print(data)
    if data:
        print("in data")
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
            app.send_task("tasks.audio_process_celery_task.audio_preprocess",
                          queue="stt_queue",
                          kwargs={
                              "file_url": str(url),
                              "note_id": str(notes_obj.id),
                              "file_name": str(file_name),
                              "blob_size": blob_size,
                              "audio_request_id": audio_request_id,
                              "container_name": data["container_name"],
                          })
