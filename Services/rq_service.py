from redis import Redis
from settings import REDIS_PASSWORD, REDIS_HOSTNAME, REDIS_PORT
from rq import Queue


redis_conn = Redis(
    host=REDIS_HOSTNAME,
    port=REDIS_PORT,
    password=REDIS_PASSWORD
)

q = Queue(connection=redis_conn)


def audio_process_task(audio_url):
    """tasks
    download file from azure
    1. stt api call
    2. get text
    3. forced alignment
    4. save to db
    5. update state
    """