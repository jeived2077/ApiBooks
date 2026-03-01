"""
Celery приложение, доступное по пути `app.core.celery_app`.

Переиспользует уже настроенный экземпляр из `Database.settings.celery_app`.
"""

from Database.settings.celery_app import celery_app as celery_app  # noqa: F401

# alias для CLI: celery -A app.core.celery_app:app worker -l info
app = celery_app

__all__ = ["celery_app", "app"]

