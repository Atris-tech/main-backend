from Services.storage_services import upload_file_blob_storage
from redis import Redis
from settings import REDIS_PASSWORD, REDIS_HOSTNAME, REDIS_PORT
from rq import Queue
import requests


def upload_task(email, file_data, file_name):

    url = upload_file_blob_storage(email=email, file_data=file_data,
                                   file_name=file_name)

    redis_conn = Redis(
        host=REDIS_HOSTNAME,
        port=REDIS_PORT,
        password=REDIS_PASSWORD
    )

    q = Queue("Public", connection=redis_conn)


