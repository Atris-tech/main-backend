import redis
import settings
import json

tendis_obj = redis.Redis(host=settings.TENDIS_HOSTNAME, port=settings.TENDIS_PORT,
                         password=settings.TENDIS_PASSWORD, ssl=True, decode_responses=True)


def set_val(key, val):

    tendis_obj.set(key, val)


def get_val(key, json_type=False):
    if json_type:
        try:
            u_data = redis_obj.get(key)
            if u_data is not None:
                data = json.loads(u_data)
                return data
            else:
                return None
        except ValueError:
            return False
    else:
        return redis_obj.get(key)
