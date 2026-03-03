import datetime
from typing import List

from authx import AuthX, AuthXConfig
from app.main import app
from app.workers.tasks import add_time_user,reset_password
from log.log import logger
from random import random
import redis.asyncio as redis
import bcrypt
from fastapi import HTTPException
from fastapi_mail import MessageSchema
from jose import jwt , JWTError
from pydantic import BaseModel, EmailStr
from sqlalchemy import Update, select
from sqlalchemy.orm import Session
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType, NameEmail
from Database.model import UserTable
from app.core.celery_app import celery_app
from config.settings import settings

from app.auth.schemas import CheckDataResponseModel


#Конфигурация токена
config = AuthXConfig(
    JWT_SECRET_KEY=settings.SECRET_KEY, 
    JWT_TOKEN_LOCATION=["headers"],
    JWT_ACCESS_TOKEN_EXPIRES= datetime.timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE)
)
auth = AuthX(config=config)
auth.handle_errors(app)
class MethodsRegister ( BaseModel ) :
    
    
    # метод проверки данных пользователя
    @classmethod
    async def CheckDataRegister (cls, db: Session, login: str, email: str, password: str, fist_name: str, last_name:str) :
        try:
            logger.info(f"Входящие данные {login},{email}")
            
            check_login = await db.execute (
                select ( UserTable.id_user ).where ( UserTable.login_user == login )
                )
            check_email = (
                await db.execute ( select ( UserTable.id_user ).where ( UserTable.email == email ) )

            )
  
            check_login_result = check_login.scalars ( ).first ( )
            check_email_result = check_email.scalars ( ).first ( )
        
            if check_login_result :
                raise HTTPException ( status_code = 409 , detail = f"Данный  логин используется" )
            if check_email_result :
                raise HTTPException ( status_code = 409 , detail = f"Данная электронная почта используется" )
    
            logger.info("Проверка данных успешно проведена")

            add_time_user.apply_async(
                kwargs={"login": login, "email": email, "password": password, "fist_name": fist_name, "last_name": last_name},
                retry=False,
            )
            
        except HTTPException as e :
            raise HTTPException ( status_code = 500 , detail = f"Ошибка в {e}" )
        except Exception as e :
            raise HTTPException (
                status_code = 500 , detail = f"Произошла внутренняя ошибка при регистрации.  Подробнее {e}"
                )
        
        
        
        
        
        
        
        
        return CheckDataResponseModel(
        success=True,
        message="Данные прошли проверку",
        
    )
    @classmethod
    async def ResetPassword(cls, db: Session, code: int, email: str, password: str):
        try:
            logger.info(f'Входящие данные email: {email}, code: {code}, password: {password}')
            key = f"temp_user:{email.lower()}"
            redis_conn = settings.redis_conn
            user_data = redis_conn.hgetall(name=key)
            logger.info(user_data)
            logger.info(f"Код с бд {user_data.get("code")}")
            if user_data.get("code") != str(code):
                raise HTTPException (
                status_code = 419 , detail = f"Неправильный код"
                )
            
            
            logger.info(f'Проверка кода прошла успешна начата изменение пароля в бд')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
            change_password = db.execute(Update(UserTable).where(UserTable.email == email).values(password_hashed = hashed_password))
            #Нужно добавить проверку выполнения запроса сюда
            # change_password_result = change_password.scalars ( ).first ( )
            redis_conn.delete(key)
            return CheckDataResponseModel(
        success=True,
        message="Пароль был изменён",
        )
                
        except HTTPException as e :
            raise HTTPException ( status_code = 500 , detail = f"Ошибка в {e}" )
        except Exception as e :
        
            raise HTTPException (
                status_code = 500 , detail = f"Произошла внутренняя ошибка при сбросе пароля  Подробнее {e}"
                )
        finally:
            redis_conn.close()
            
        
    @classmethod
    async def SendEmailReset(cls, db: Session, email: str):
        try:
            logger.info(f'Входящие данные email: {email}')
            check_email = await db.execute (
                select (UserTable.email).where (UserTable.email == email)
            )
            check_email_result = check_email.scalars().first()
            
            if check_email_result is None:
                raise HTTPException ( status_code = 404 , detail = f"Данного пользователя с привязанной данной электронной почтой отсутствует" )
            logger.info(f'Проверка на привязку почты прошла успешна')
            logger.info(f'Начата отправка кода на почту')
            reset_password.apply_async(
                kwargs={"email": email},
                retry=False,
            )
            return CheckDataResponseModel(success = True, message = "Отправлен код на почту")
        except HTTPException as e :
            raise HTTPException ( status_code = 500 , detail = f"Ошибка в {e}" )
        except Exception as e :
            raise HTTPException (
                status_code = 500 , detail = f"Произошла внутренняя ошибка при регистрации.  Подробнее {e}"
                )
        
    
        
            
         
            
     
         
         
         
   




        
    







    
    @classmethod
    async def Register ( cls , db: Session , email: str, code: int ) :
        try :
            key = f"temp_user:{email.lower()}"
            redis_conn = settings.redis_conn
            user_data = redis_conn.hgetall(name=key)
            logger.info(user_data)
            if user_data is None:
                raise HTTPException (
                status_code = 402 , detail = f"Отсутствуют данные"
                )
            if user_data.get("code") != code:
                raise HTTPException (
                status_code = 419 , detail = f"Неправильный код"
                )
            add_user = UserTable(
            login_user=user_data.get("login"),
            password_hashed=user_data.get("password"),
            email=user_data.get("email"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            role="user",
                        )
            db.add ( add_user )
            await db.commit ( )
            await db.refresh ( add_user )
            redis_conn.delete(key)
            if add_user.id_user :
                return auth.create_access_token(uid=add_user.login_user, scopes=["users:read", "posts:write"])
                # return await cls.GenerateJwt (
                #     add_user.id_user , add_user.email , add_user.login_user ,
                #     add_user.role
                #     )
            else :
                return False
        except HTTPException as e :
            raise HTTPException ( status_code = 500 , detail = f"Ошибка в {e}" )
        except Exception as e :
            print ( e )
            raise HTTPException (
                status_code = 500 , detail = f"Произошла внутренняя ошибка при регистрации.  Подробнее {e}"
                )
        finally:
            redis_conn.close()
    
    
    
    
    
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
                    return auth.create_access_token(uid=login, scopes=["users:read", "posts:write"])
                    # return await cls.GenerateJwt ( check.id_user , check.login_user , check.email , check.role )
                else :
                    raise HTTPException ( status_code = 401 , detail = f"Неверный пароль" )
            
            
            
            
            
            
            
            
            
            else :
                
                raise HTTPException ( status_code = 401 , detail = f"Пользователя такого не существует" )
        except Exception as e :
            raise HTTPException ( status_code = 401 , detail = f"Ошибка в авторизации пользователя Подробнее {e}" )
    #Эти функции будут удалены и заменены будут библиотекой
    # # метод генерации токена
    # async def GenerateJwt ( self , user_id , email , login , role = "user" ) :
    #     print ( user_id , email , login , role )
    #     try :
    #         # Получение данных пользователя
    #         payload_refresh = {
    #             "user_id" : user_id ,
    #             "email" : email ,
    #             "login" : login ,
    #             "role" : role ,
    #             "token_type" : "refresh" ,
    #             "exp" : datetime.datetime.utcnow ( ) + datetime.timedelta ( days = 365 ) ,
    #             "iat" : datetime.datetime.utcnow ( ) ,
    #             }
            
    #         headers_refresh = {
    #             "kid" : "key-id-001" ,
    #             "typ" : "Refresh"
    #             }
    #         payload_access = {
    #             "user_id" : user_id ,
    #             "email" : email ,
    #             "login" : login ,
    #             "role" : role ,
    #             "token_type" : "access" ,
    #             "exp" : datetime.datetime.utcnow ( ) + datetime.timedelta ( minutes = 5 ) ,
    #             "iat" : datetime.datetime.utcnow ( ) ,
    #             }
            
    #         headers_access = {
    #             "kid" : "key-id-001" ,
    #             "typ" : "Refresh"
    #             }
            
    #         token_refresh = jwt.encode (
    #             payload_refresh , SECRET_KEY , algorithm = "HS256" , headers = headers_refresh
    #             )
    #         token_access = jwt.encode ( payload_access , SECRET_KEY , algorithm = "HS256" , headers = headers_access )
    #         # Переделал возвращение в таком формате
    #         return {
    #             "token_refresh": token_refresh,
    #             "token_access": token_access
    #         }
    #     except Exception as e :
    #         raise HTTPException ( status_code = 401 , detail = f"Ошибка в генерации ключей Подробнее {e}" )
        
    
                
                
        
    # @classmethod
    # # Проверка токена
    # async def VerifyJwt ( cls , token ) :
    #     if not token :
    #         print ( "Отсутствует токен" )
        
    #     try :
    #         decoded = jwt.decode ( token , SECRET_KEY , algorithms = [ "HS256" ] )
    #         print ( f"Пользователь: {decoded [ 'user_id' ]}" )
    #     except jwt.ExpiredSignatureError :
            
    #         # Токен истёк
            
    #         raise HTTPException ( status_code = 401 , detail = f"Срок действия токена истёк" )
    #         print ( "Срок действия токена истёк" )
    #     except jwt.InvalidSignatureError :
    #         # Неверная подпись
    #         raise HTTPException ( status_code = 401 , detail = f"Подпись токена недействительна" )
    #         print ( "Подпись токена недействительна" )
    #     except jwt.InvalidAudienceError :
    #         # Неверная аудитория
    #         raise HTTPException ( status_code = 401 , detail = f"Токен предназначен для другой аудитории" )
    #         print ( "Токен предназначен для другой аудитории" )
    #     except jwt.InvalidIssuerError :
    #         # Неверный издатель
    #         raise HTTPException ( status_code = 401 , detail = f"Токен выдан неизвестным издателем" )
    #         print ( "Токен выдан неизвестным издателем" )
    #     except jwt.InvalidKeyError :
    #         # Неверный ключ
    #         raise HTTPException ( status_code = 401 , detail = f"Ключ недействителен" )
    #         print ( "Ключ недействителен" )
    #     except jwt.InvalidTokenError :
    #         # Базовое исключение для всех ошибок
    #         raise HTTPException ( status_code = 401 , detail = f"Токен недействителен" )
    #         print ( "Токен недействителен" )
    #     except jwt.DecodeError :
    #         # Ошибка декодирования
    #         raise HTTPException ( status_code = 401 , detail = f"Не удалось декодировать токен" )
    #         print ( "Не удалось декодировать токен" )
    # @classmethod
    # # Обновление токена
    # async def RefreshToken ( self , expired_access_token: str , refresh_token: str ) :
        
    #     try :
            
    #         payload_access = jwt.decode (
    #             expired_access_token ,
    #             SECRET_KEY ,
    #             algorithms = [ ALGORITHM ] ,
    #             options = { "verify_signature" : False , "verify_exp" : False }
    #             )
            
    #         if payload_access.get ( "token_type" ) != "access" :
    #             raise HTTPException ( status_code = 403 , detail = "Предоставленный токен не является Access Token." )
        
    #     except JWTError :
            
    #         raise HTTPException (
    #             status_code = 401 , detail = "Недействительный Access Token (ошибка подписи/формата)."
    #             )
        
    #     try :
    #         payload_refresh = await self.VerifyJwt ( refresh_token , required_type = "refresh" )
        
    #     except HTTPException as e :
            
    #         if e.status_code == 401 :
    #             raise HTTPException (
    #                 status_code = 401 , detail = "Сессия окончена. Refresh Token истёк. Требуется повторный вход."
    #                 )
    #         raise e
        
    #     user_data = {
    #         "user_id" : payload_access.get ( "sub" ) ,
    #         "email" : payload_access.get ( "email" ) ,
    #         "login" : payload_access.get ( "login" ) ,
    #         "role" : payload_access.get ( "role" ) ,
    #         }
        
    #     new_refresh_token , new_access_token = await self.GenerateJwt (
    #         user_id = user_data [ "user_id" ] ,
    #         email = user_data [ "email" ] ,
    #         login = user_data [ "login" ] ,
    #         role = user_data [ "role" ]
    #         )
        
    #     return new_refresh_token , new_access_token
