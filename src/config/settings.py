
import os

from celery import Celery
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
    ACCESS_TOKEN_EXPIRE: int
    # Redis
    REDIS_HOST: str = '0.0.0.0'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_SSL: bool = False
    REDIS_DB: int = 0
    
    MAIL_USERNAME: str 
    MAIL_PASSWORD: str 
    MAIL_FROM: str 
    MAIL_PORT: int 
    MAIL_SERVER: str 
    MAIL_STARTTLS: bool 
    MAIL_SSL_TLS: bool 
    USE_CREDENTIALS: bool 
    VALIDATE_CERTS: bool 
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )   
    
  
      
    
    def get_db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
    def get_redis_url(self) -> str:
        
        auth = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @property
    def mail_conf(self) -> ConnectionConfig:
        return ConnectionConfig(
            MAIL_USERNAME=self.MAIL_USERNAME,
            MAIL_PASSWORD=self.MAIL_PASSWORD,
            MAIL_FROM=self.MAIL_FROM,
            MAIL_PORT=self.MAIL_PORT,
            MAIL_SERVER=self.MAIL_SERVER,
            MAIL_STARTTLS=self.MAIL_STARTTLS,
            MAIL_SSL_TLS=self.MAIL_SSL_TLS,
            
        )

    @property
    def redis_conn(self):
        return redis.from_url(
            self.get_redis_url(),
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=10,
        )

settings = Settings()
