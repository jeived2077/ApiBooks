import asyncio
import random

import bcrypt
from fastapi_mail import FastMail, MessageSchema, MessageType

from config.settings import settings
from app.core.celery_app import celery_app
from log.log import logger


@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def reset_password(self, email: str):
    redis_conn = None
    try:
        logger.info("Начато работа: запись во временное хранилище + отправка кода на почту")
        expire_seconds: int = 900

        code = random.randint(1000, 9999)

        template = f"""
        <html>
          <body>
            <p>Hi !!!
              <br>Привет, вот код для сброса пароля <var>{code}</var>!!!</p>
          </body>
        </html>
        """

        user_data = {
            "email": email.lower(),
            "code": code,
        }

        key = f"temp_user:{email.lower()}"
        redis_conn = settings.redis_conn
        redis_conn.hset(name=key, mapping=user_data)
        redis_conn.expire(key, expire_seconds)

        message = MessageSchema(
            subject="Отправка кода для сброса пароля",
            recipients=[email],
            body=template,
            subtype=MessageType.html,
        )
        fm = FastMail(settings.mail_conf)
        asyncio.run(fm.send_message(message))
        logger.info("Отправлен код на почту")

        return {"status": "success", "key": key}
    except Exception as exc:
        logger.exception(f"Ошибка в reset_password: {exc}")
        raise self.retry(exc=exc)
    finally:
        if redis_conn is not None:
            redis_conn.close()


@celery_app.task(name="add_time_user", bind=True, max_retries=3, default_retry_delay=30)
def add_time_user(self, login: str, email: str, password: str):
    redis_conn = None
    try:
        logger.info("Начато работа: запись во временное хранилище + отправка кода на почту")
        expire_seconds: int = 900

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        code = random.randint(1000, 9999)

        template = f"""
        <html>
          <body>
            <p>Hi !!!
              <br>Привет, вот код для потверждения почты <var>{code}</var>!!!</p>
          </body>
        </html>
        """

        user_data = {
            "login": login,
            "email": email.lower(),
            "password": hashed_password,
            "code": code,
            "status": "pending",
        }

        key = f"temp_user:{email.lower()}"
        redis_conn = settings.redis_conn
        redis_conn.hset(name=key, mapping=user_data)
        redis_conn.expire(key, expire_seconds)

        message = MessageSchema(
            subject="Отправка кода для потверждение почты",
            recipients=[email],
            body=template,
            subtype=MessageType.html,
        )
        fm = FastMail(settings.mail_conf)
        asyncio.run(fm.send_message(message))
        logger.info("Отправлен код на почту")

        return {"status": "success", "key": key}
    except Exception as exc:
        logger.exception(f"Ошибка в add_time_user: {exc}")
        raise self.retry(exc=exc)
    finally:
        if redis_conn is not None:
            redis_conn.close()