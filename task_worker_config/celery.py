from celery import Celery
import settings


app = Celery(
    main="audio_process",
    backend=f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOSTNAME}:{settings.REDIS_PORT}/{settings.REDIS_DB}',
    broker=f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOSTNAME}:{settings.REDIS_PORT}/{settings.REDIS_DB}',
)
app.autodiscover_tasks()
app.conf.update(task_track_started=True)
app.conf.imports = ['tasks.audio_process_celery_task']