from datetime import datetime , timedelta
from random import random

import bcrypt
from fastapi import HTTPException
from fastapi_mail import MessageSchema
from jose import jwt , JWTError
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from Database.model import UserTable
from Database.settings.settings import settings
from Route.auth.response_model import CheckDataResponseModel

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


class MethodsRegister ( BaseModel ) :
	
	# метод проверки данных пользователя
	@classmethod
	async def CheckDataRegister ( cls , db: Session , login , email ) :
		check_login = await db.execute (
			select ( UserTable.id_user ).where ( UserTable.login_user == login )
			).scalar ( )
		check_email = (
			await db.execute ( select ( UserTable.id_user ).where ( UserTable.email == email ) ).scalar ( )
		
		)
		check_login_result = check_login.scalars ( ).first ( )
		check_email_result = check_email.scalars ( ).first ( )
		if check_login_result :
			raise HTTPException ( status_code = 409 , detail = f"Данный  логин используется" )
		if check_email_result :
			raise HTTPException ( status_code = 409 , detail = f"Данная электронная почта используется" )
		return CheckDataResponseModel.success == True , CheckDataResponseModel.message == ("Все данные валидны. Можно "
		                                                                                   "переходить к отправке "
		                                                                                   "кода "
		                                                                                   "подтверждения.")
	
	# метод регистрации пользователя
	@classmethod
	async def Register ( cls , db: Session , login: str , password: str , email: str ) :
		try :
			salt = bcrypt.gensalt ( )
			hashed_password = bcrypt.hashpw ( password.encode ( 'utf-8' ) , salt )
			
			add_user = UserTable (
				login_user = login ,
				password_hashed = hashed_password.decode ( 'utf-8' ) ,
				salt = salt.decode ( 'utf-8' ) ,
				email = email ,
				role = "user"
				)
			db.add ( add_user )
			await db.commit ( )
			await db.refresh ( add_user )
			
			if add_user.id_user :
				
				return await cls.GenerateJwt (
					add_user.id_user , add_user.email , add_user.login_user ,
					add_user.role
					)
			else :
				return False
		except HTTPException as e :
			raise HTTPException ( status_code = 500 , detail = f"Ошибка в {e}" )
		except Exception as e :
			print ( e )
			raise HTTPException (
				status_code = 500 , detail = f"Произошла внутренняя ошибка при регистрации.  Подробнее {e}"
				)
	
	@classmethod
	# метод авторизации пользователя
	async def Auth ( cls , db: Session , login: str , password: str ) :
		try :
			login_check = await db.execute (
				select ( UserTable ).where ( UserTable.login_user == login )
				)
			
			check = login_check.scalars ( ).first ( )
			print ( check )
			if check is None :
				raise HTTPException ( status_code = 401 , detail = f"Данный логин не используется" )
			if check :
				
				check_password = bcrypt.checkpw (
					
					password.encode ( 'utf-8' ) ,
					
					check.password_hashed.encode ( 'utf-8' )
					)
				if check_password :
					return await cls.GenerateJwt ( check.id_user , check.login_user , check.email , check.role )
				else :
					raise HTTPException ( status_code = 401 , detail = f"Неверный пароль" )
			
			
			
			
			
			
			
			
			
			else :
				
				raise HTTPException ( status_code = 401 , detail = f"Пользователя такого не существует" )
		except Exception as e :
			raise HTTPException ( status_code = 401 , detail = f"Ошибка в авторизации пользователя Подробнее {e}" )
	
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
			
			# fm = FastMail ( conf )
			# await fm.send_message ( message )
			# print ( message )
			
			return HTTPException ( status_code = 200 , detail = { "Код был отправлен на почту" } )
		except Exception as e :
			return HTTPException ( status_code = 4000 , detail = { "Код не был отправлен на почту" } )
	
	# метод проверки кода пользователя с кодом получателя
	async def SendCode ( cls , code: int ) :
		
		pass
	
	# метод генерации токена
	async def GenerateJwt ( self , user_id , email , login , role = "user" ) :
		print ( user_id , email , login , role )
		try :
			# Получение данных пользователя
			payload_refresh = {
				"user_id" : user_id ,
				"email" : email ,
				"login" : login ,
				"role" : role ,
				"token_type" : "refresh" ,
				"exp" : datetime.utcnow ( ) + timedelta ( days = 365 ) ,
				"iat" : datetime.utcnow ( ) ,
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
				"token_type" : "access" ,
				"exp" : datetime.utcnow ( ) + timedelta ( minutes = 5 ) ,
				"iat" : datetime.utcnow ( ) ,
				}
			
			headers_access = {
				"kid" : "key-id-001" ,
				"typ" : "Refresh"
				}
			
			token_refresh = jwt.encode (
				payload_refresh , SECRET_KEY , algorithm = "HS256" , headers = headers_refresh
				)
			token_access = jwt.encode ( payload_access , SECRET_KEY , algorithm = "HS256" , headers = headers_access )
			
			return token_refresh , token_access
		except Exception as e :
			raise HTTPException ( status_code = 401 , detail = f"Ошибка в генерации ключей Подробнее {e}" )
	
	# Проверка токена
	async def VerifyJwt ( self , token ) :
		if not token :
			print ( "Отсутствует токен" )
		
		try :
			decoded = jwt.decode ( token , SECRET_KEY , algorithms = [ "HS256" ] )
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
	
	# Обновление токена
	async def RefreshToken ( self , expired_access_token: str , refresh_token: str ) :
		
		try :
			
			payload_access = jwt.decode (
				expired_access_token ,
				SECRET_KEY ,
				algorithms = [ ALGORITHM ] ,
				options = { "verify_signature" : False , "verify_exp" : False }
				)
			
			if payload_access.get ( "token_type" ) != "access" :
				raise HTTPException ( status_code = 403 , detail = "Предоставленный токен не является Access Token." )
		
		except JWTError :
			
			raise HTTPException (
				status_code = 401 , detail = "Недействительный Access Token (ошибка подписи/формата)."
				)
		
		try :
			payload_refresh = await self.VerifyJwt ( refresh_token , required_type = "refresh" )
		
		except HTTPException as e :
			
			if e.status_code == 401 :
				raise HTTPException (
					status_code = 401 , detail = "Сессия окончена. Refresh Token истёк. Требуется повторный вход."
					)
			raise e
		
		user_data = {
			"user_id" : payload_access.get ( "sub" ) ,
			"email" : payload_access.get ( "email" ) ,
			"login" : payload_access.get ( "login" ) ,
			"role" : payload_access.get ( "role" ) ,
			}
		
		new_refresh_token , new_access_token = await self.GenerateJwt (
			user_id = user_data [ "user_id" ] ,
			email = user_data [ "email" ] ,
			login = user_data [ "login" ] ,
			role = user_data [ "role" ]
			)
		
		return new_refresh_token , new_access_token
