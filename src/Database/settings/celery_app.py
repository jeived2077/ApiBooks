from celery import Celery

from config.settings import settings


get_redis_url = settings.get_redis_url()


celery_app = Celery(
    "celery_worker",  
    broker=get_redis_url,
    )
celery_app.conf.update(
    # Настройки сериализации
    task_serializer="json",  
    accept_content=["json"],  
    result_serializer="json",  
    
    # Настройки времени
    timezone="Europe/Moscow", 
    enable_utc=True,  
    
    # Настройки отслеживания
    task_track_started=True, 
    task_ignore_result=True,
    result_backend=None,
    
    # Настройки таймаутов
    task_time_limit=30 * 60,  
    task_soft_time_limit=25 * 60,  
    
    # Настройки воркера
    worker_prefetch_multiplier=1,  
    worker_max_tasks_per_child=1000, 
    
    # Настройки очередей
    task_default_queue="default",  
    task_routes={
        "app.tasks.email_tasks.*": {"queue": "email"},
        "app.tasks.file_tasks.*": {"queue": "files"},
        "app.tasks.report_tasks.*": {"queue": "reports"},
    },
    
    # Настройки повторных попыток
    task_acks_late=True,  # Подтверждать выполнение задачи только после успешного завершения
    worker_disable_rate_limits=False,  # Не отключать ограничения скорости
    
    # Настройки логирования
    worker_log_format="[%(asctime)s: %(levelname)s/%(processName)s] %(message)s",
    worker_task_log_format="[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s",

    # Явно импортируем модуль с задачами, чтобы воркер их зарегистрировал
    imports=("app.workers.tasks",),

    # Чтобы HTTP-запросы не зависали при недоступном Redis
    broker_connection_timeout=5,
    broker_transport_options={
        "socket_connect_timeout": 5,
        "socket_timeout": 5,
    },
)


# alias для CLI: `celery -A Database.settings.celery_app:app worker -l info`
app = celery_app