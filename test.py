from redis import StrictRedis
from settings import REDIS_PASSWORD, REDIS_HOSTNAME, REDIS_PORT
from rq import Queue
from test1 import count_words_at_url
import time


redis_conn = StrictRedis(
            host=REDIS_HOSTNAME,
            port=REDIS_PORT,
            password=REDIS_PASSWORD
        )

q = Queue("MYQUEUE", connection=redis_conn)
print("MYQUEUE")
for i in range(10):
    job = q.enqueue(count_words_at_url, 'http://nvie.com')
# print(job.result)

#time.sleep(2)
#print(job.result)
