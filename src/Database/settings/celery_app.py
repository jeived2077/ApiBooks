import ssl
from celery import Celery
from Database.settings import settings
celery_app = Celery(
    "api_books_worker",
    broker=settings.settings.get_redis_url(),
    backend=settings.settings.get_redis_url(),
)


if settings.settings.REDIS_SSL:
    ssl_options = {"ssl_cert_reqs": ssl.CERT_NONE}
    celery_app.conf.update(
        broker_use_ssl=ssl_options,
        redis_backend_use_ssl=ssl_options,
    )


celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    enable_utc=True,
    timezone="Europe/Moscow",
    broker_connection_retry_on_startup=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)



celery_app.autodiscover_tasks(["app.tasks"])