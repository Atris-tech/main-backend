import uuid
from Services.storage_services import upload_file_blob_storage
from redis import Redis
from settings import REDIS_PASSWORD, REDIS_HOSTNAME, REDIS_PORT
from rq import Queue
from tasks import audio_process_rq_task
from Services.redis_service import get_list


redis_conn = Redis(
            host=REDIS_HOSTNAME,
            port=REDIS_PORT,
            password=REDIS_PASSWORD
        )


def upload_task(user_obj, file_data, file_name, notes_obj, work_space_obj):
    file_name = str(uuid.uuid4()) + file_name
    url = upload_file_blob_storage(email=user_obj.email_id, file_data=file_data,
                                   file_name=file_name)

    direct_api_supported_plans = get_list("DIRECT_STT_API_PLANS")
    if user_obj.plan in direct_api_supported_plans:
        """direct api call stt"""
        q = Queue(str(user_obj.id), connection=redis_conn)
        """send for conversion and upload"""
        pass
    else:
        q = Queue("Public", connection=redis_conn)
        job = q.enqueue_job(audio_process_rq_task, )

