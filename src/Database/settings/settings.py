from fastapi_mail import ConnectionConfig
from pydantic_settings import BaseSettings, SettingsConfigDict
import redis

class Settings(BaseSettings):
    # PostgreSQL
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str

    SECRET_KEY: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    REDIS_SSL: bool = False          
    REDIS_DB: int = 0

    model_config = SettingsConfigDict(
        env_file=(".env",),
        env_file_encoding="utf-8",
        extra="ignore",
    )
    conf = ConnectionConfig(
    MAIL_USERNAME ="username",
    MAIL_PASSWORD = "**********",
    MAIL_FROM = "test@email.com",
    MAIL_PORT = 465,
    MAIL_SERVER = "mail server",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

    def get_redis_url(self) -> str:
        scheme = "rediss" if self.REDIS_SSL else "redis"
        password = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"{scheme}://{password}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    def get_db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()   
redis_conn = redis.from_url(
            settings.get_redis_url(),
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=10,
        )