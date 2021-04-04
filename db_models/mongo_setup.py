import mongoengine
from mongoengine import connect
import settings
import os


def string_to_bool(val:str)-> bool:
    if val == "True":
        return True
    elif val == "False":
        return False
    else:
        raise ValueError


def global_init():
    check_test = os.getenv("TESTING_ATRIS")
    check_test = string_to_bool(val=check_test)
    if check_test:
        print("test env")
        connect(db='atris_test', host='mongomock://localhost', alias='core')
    else:
        print("not test env")
        mongoengine.register_connection(
            db=settings.MONGO_DB,
            host=settings.MONGO_HOST,
            port=int(settings.MONGO_PORT),
            alias='core',
            authentication_source=settings.MONGO_DB,
            username=settings.MONGO_USER,
            password=settings.MONGO_PASSWORD,
            ssl=True,
            retrywrites=False
        )
        mongoengine.connect(
            db=settings.MONGO_DB,
            host=settings.MONGO_HOST,
            port=int(settings.MONGO_PORT),
            username=settings.MONGO_USER,
            password=settings.MONGO_PASSWORD,
        )
