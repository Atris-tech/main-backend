import redis
import settings
import json

redis_obj = redis.StrictRedis(host=settings.REDIS_HOSTNAME, port=settings.REDIS_PORT,
                              password=settings.REDIS_PASSWORD, ssl=True, decode_responses=True)


def set_val(key, val, json_type=False):
    if json_type:
        redis_obj.set(key, json.dumps(val))
    else:
        redis_obj.set(key, str(val))


def get_val(key, json_type=False):
    if json_type:
        try:
            data = json.loads(redis_obj.get(key))
            return data
        except ValueError:
            return False
    else:
        return redis_obj.get(key)
