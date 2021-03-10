import mongoengine
import settings


def global_init():
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
