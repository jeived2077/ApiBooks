"""
Обёртка над существующими настройками, чтобы использовать единый путь `app.core.settings`.
"""

from config.settings import Settings, settings  # type: ignore[F401]

__all__ = ["Settings", "settings"]

