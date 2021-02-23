import redis
import settings
import json

redis_obj = redis.StrictRedis(host=settings.REDIS_HOSTNAME, port=settings.REDIS_PORT,
                              password=settings.REDIS_PASSWORD, ssl=True, decode_responses=True)


def set_val(key, val, json_type=False):
    print("set_value")
    if json_type:
        print("set_value")
        redis_obj.set(key, json.dumps(val))
        print("set value done1")
    else:
        redis_obj.set(key, str(val))


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
