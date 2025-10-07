from datetime import datetime
from random import random

import bcrypt
import jwt
from fastapi import HTTPException
from fastapi_mail import MessageSchema , FastMail , ConnectionConfig
from pydantic import BaseModel
from sqlalchemy.orm import Session

from Database.User_Table import User_Table

SECRET_KEY = "09d25e094faa****************f7099f6f0f4caa6cf63b88e8d3e7"

ALGORITHM = "HS256"
db: Session = Session

secret = "mysecret"

conf = ConnectionConfig (
	MAIL_USERNAME = from_ ,
	MAIL_PASSWORD = "************" ,
	MAIL_PORT = 587 ,
	MAIL_SERVER = "smtp.gmail.com" ,
	MAIL_TLS = True ,
	MAIL_SSL = False
	)


class MethodsRegister ( BaseModel ) :
	UserTable = User_Table
	
	@classmethod
	async def Check_data_Register ( cls , username ) :
		pass
	
	# метод регистрации пользователя
	@classmethod
	async def Register ( cls , login: str , password: str , email: str ) :
		try :
			salt = bcrypt.gensalt ( )
			hashed_password = bcrypt.hashpw ( password.encode ( 'utf-8' ) , salt )
			
			add_user = User_Table (
				login_user = login ,
				password_hashed = hashed_password ,
				salet = salt ,
				email = email ,
				)
			db.add ( add_user )
			db.commit ( "Зарегистрирован пользователь " )
			db.refresh ( add_user )
			check = db.first ( add_user )
			if (check) :
				
				return cls.GenerateJwt ( check.id_user , check.login_user , check.email )
			else :
				return False
		except Exception as e :
			pass
	
	@classmethod
	# метод авторизации пользователя
	async def Auth ( cls , login: str , password: str ) :
		try :
			
			check_user = User_Table (
				login_user = login ,
				
				)
			
			check = db.first ( check_user )
			if (check) :
				
				check_password = bcrypt.decode ( check.password_hashed , "utf-8" , check.salt )
				if (check_password == password) :
					return cls.GenerateJwt ( check.id_user , check.login_user , check.email )
				else :
					raise HTTPException ( status_code = 401 , detail = f"Неверный пароль" )
			
			
			
			
			
			
			
			
			
			else :
				
				raise HTTPException ( status_code = 401 , detail = f"Пользователя такого не существует" )
		except Exception as e :
			raise HTTPException ( status_code = 401 , detail = f"Ошибка в авторизации пользователя" )
	
	@classmethod
	# метод отправки кода на почту
	async def SendEmail ( cls , email: str ) :
		try :
			int
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
			
			fm = FastMail ( conf )
			await fm.send_message ( message )
			print ( message )
			
			return HTTPException ( status_code = 200 , detail = { "Код был отправлен на почту" } )
		except Exception as e :
			return HTTPException ( status_code = 4000 , detail = { "Код не был отправлен на почту" } )
	
	# метод проверки кода пользователя с кодом получателя
	async def SendCode ( cls , code: int ) :
		
		pass
	
	# метод генерации токена
	async def GenerateJwt ( self , user_id , email , login , role ) :
		try :
			# Получение данных пользователя
			payload_refresh = {
				"user_id" : user_id ,
				"email" : email ,
				"login" : login ,
				"role" : role ,
				"exp" : datetime.datetime.utcnow ( ) + datetime.timedelta ( years = 1 ) ,
				"iat" : datetime.datetime.utcnow ( ) ,
				}
			
			headers_refresh = {
				"kid" : "key-id-001" ,
				"typ" : "Refresh"
				}
			payload_access = {
				"user_id" : user_id ,
				"email" : email ,
				"login" : login ,
				"role" : role ,
				"exp" : datetime.datetime.utcnow ( ) + datetime.timedelta ( minute = 5 ) ,
				"iat" : datetime.datetime.utcnow ( ) ,
				}
			
			headers_access = {
				"kid" : "key-id-001" ,
				"typ" : "Refresh"
				}
			
			token_refresh = jwt.encode ( payload_refresh , secret , algorithm = "HS256" , headers = headers_refresh )
			token_access = jwt.encode ( payload_access , secret , algorithm = "HS256" , headers = headers_access )
			
			return token_refresh , token_access
		except Exception as e :
			raise HTTPException ( status_code = 401 , detail = f"Ошибка в генерации ключей" )
	
	async def VerifyJwt ( self , token ) :
		if not token :
			print ( "Отсутствует токен" )
		
		try :
			decoded = jwt.decode ( token , secret , algorithms = [ "HS256" ] )
			print ( f"Пользователь: {decoded [ 'user_id' ]}" )
		except jwt.ExpiredSignatureError :
			
			# Токен истёк
			
			raise HTTPException ( status_code = 401 , detail = f"Срок действия токена истёк" )
			print ( "Срок действия токена истёк" )
		except jwt.InvalidSignatureError :
			# Неверная подпись
			raise HTTPException ( status_code = 401 , detail = f"Подпись токена недействительна" )
			print ( "Подпись токена недействительна" )
		except jwt.InvalidAudienceError :
			# Неверная аудитория
			raise HTTPException ( status_code = 401 , detail = f"Токен предназначен для другой аудитории" )
			print ( "Токен предназначен для другой аудитории" )
		except jwt.InvalidIssuerError :
			# Неверный издатель
			raise HTTPException ( status_code = 401 , detail = f"Токен выдан неизвестным издателем" )
			print ( "Токен выдан неизвестным издателем" )
		except jwt.InvalidKeyError :
			# Неверный ключ
			raise HTTPException ( status_code = 401 , detail = f"Ключ недействителен" )
			print ( "Ключ недействителен" )
		except jwt.InvalidTokenError :
			# Базовое исключение для всех ошибок
			raise HTTPException ( status_code = 401 , detail = f"Токен недействителен" )
			print ( "Токен недействителен" )
		except jwt.DecodeError :
			# Ошибка декодирования
			raise HTTPException ( status_code = 401 , detail = f"Не удалось декодировать токен" )
			print ( "Не удалось декодировать токен" )
