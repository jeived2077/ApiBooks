
from datetime import datetime , timedelta
from random import random
import redis.asyncio as redis
import bcrypt
from fastapi import HTTPException, logger
from fastapi_mail import FastMail, MessageSchema
from jose import jwt , JWTError
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from Database.model import UserTable

from Database.settings.settings import settings
from Route.auth.response_model import CheckDataResponseModel
from Database.settings.celery_app import celery_app
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


class CeleryMethods():
	@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
	async def send_email_code(self, email: str):
		code = random.randint ( 1000 , 9999 )
		template = f"""
					        <html>
					        <body>


					<p>Hi !!!
					        <br>Привет, вот код для потверждения почты <var>{code}</var>!!!</p>


					        </body>
					        </html>
					        """
			
		message = MessageSchema (
			subject = "Отправка кода для потверждение почты" ,
		    recipients = email.dict ( ).get ( "email" ) ,
			body = template ,
			subtype = "html"
			)
			
		fm = FastMail ( settings.conf )
		await fm.send_message ( message )
		# logger (f"Отправленный"message )
        
        


    
	@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
	async def add_time_user(self, login: str, email: str, password: str, redis_conn: redis, expire_seconds: int = 900):
		try:
			# 1. Хэшируем пароль
			salt = bcrypt.gensalt()
			hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

			# 2. Данные пользователя
			user_data = {
				"login": login,
				"email": email.lower(),
				"password": hashed_password.decode("utf-8"),   
				"created_at": datetime.utcnow().isoformat(),
				"status": "pending"
				
			}

			
			

			
			key = f"temp_user:{email.lower()}"
			redis_conn.hset(name=key, mapping=user_data)
			redis_conn.expire(key, expire_seconds)
            
			

			
			return {"status": "success", "key": key}

		except Exception as exc:
			logger(f"Ошибка в добавление таблицу временных пользователей:{exc}" )
			raise self.retry(exc=exc)
		finally:
			if redis_conn:
				redis_conn.close()
	