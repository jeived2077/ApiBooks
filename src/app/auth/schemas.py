import re
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr , field_validator
from pydantic import Field
from pydantic_core.core_schema import FieldValidationInfo
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType, NameEmail
from log.log import logger

class RequestAuthModel ( BaseModel ) :
    login: str
    password: str
    
    @field_validator ( 'login' )
    @classmethod
    def validate_login ( cls , value ) :
        if len ( value ) < 3 :
            raise ValueError ( 'Логин слишком короткий.' )
        return value
    
    @field_validator ( 'password' )
    @classmethod
    def validate_password ( cls , value ) :
        if value is None :
            raise ValueError (
                'Не введён пароль'
                )
        return value


class CheckDataResponseModel ( BaseModel ) :
    success: bool | None = Field ( default = None )
    message: str | None = Field ( default = None )
  
class RequestEmailModel(BaseModel):
    email: EmailStr | None = Field ( default = None )
    @field_validator ( 'email' )
    @classmethod
    def validate_email ( cls , value ) :
        if value is None or not str(value).strip() :
            logger.error("Электронная почта не указана")
            raise HTTPException (
                status_code = 402 ,
                detail = "Электронная почта не указана"
                )
        
        return str(value).strip().lower()
      

    
class CheckResetPasswordRequestModel(BaseModel):
    email: EmailStr | None = Field ( default = None )
    code: int = Field(..., ge=1000, le=9999)
    password: str | None = Field ( default = None )
    password2: str | None = Field ( default = None )
    @field_validator ( 'password' )
    @classmethod
    def validate_password ( cls , value ) :
     if len ( value ) < 8 :
         raise ValueError ( 'Пароль имеет меньше 8 символов' )
     if not value :
         raise ValueError ( 'Не введён пароль' )
     if re.search ( r'[а-яА-ЯёЁ]' , value ) :
         raise ValueError ( 'Пароль не должен содержать кириллицу (русские буквы)' )
     if not re.search ( r'[^a-zA-Z0-9]' , value ) :
         raise ValueError ('Пароль должен содержать специальные символы.')
     return value
    @field_validator ( 'password2' )
    @classmethod
    def validate_password_check ( cls , value , info: FieldValidationInfo ) :
     if 'password' in info.data and value != info.data [ 'password' ] :
         raise ValueError ( 'Введенные пароли не совпадают' )
     return value
    @field_validator('code')
    @classmethod
    def validate_code(cls, value):
        if value is None:
            logger.error("Код подтверждения не указан")
            raise HTTPException(
                status_code=402,
                detail="Код подтверждения не указан",
            )
        if not (1000 <= value <= 9999):
            logger.error("Неверный код подтверждения")
            raise HTTPException(
                status_code=402,
                detail="Неверный код подтверждения",
            )
        return value

class CheckRegistationRequestModel ( BaseModel ) :
    first_name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(..., min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")
    login: str | None = Field ( default = None )
    password: str | None = Field ( default = None )
    password2: str | None = Field ( default = None )
    email: EmailStr | None = Field ( default = None )
    
    # проверка логина
    @field_validator ( 'login' )
    @classmethod
    def validate_login ( cls , value ) :
        if len ( value ) < 3 :
            logger.error("Логин слишком короткий.")
            raise ValueError ( 'Логин слишком короткий.' )
            
        return value
    
    
    
    
    #Поменять проверку email так как думал что по документации принимает email только в формате List библиотека fastapi_mail
    # проверка email
    @field_validator ( 'email' )
    @classmethod
    def validate_email ( cls , value ) :
        if value is None or not str(value).strip() :
            logger.error("Электронная почта не указана")
            raise HTTPException (
                status_code = 402 ,
                detail = "Электронная почта не указана"
                )
        # нормализуем email к нижнему регистру
        return str(value).strip().lower()
    
    @field_validator ( 'password' )
    @classmethod
    def validate_password ( cls , value ) :
        
        if len ( value ) < 8 :
            logger.error("Пароль должен содержать специальные символы.")
            # raise ValueError ( 'Пароль имеет меньше 8 символов' )
            raise HTTPException ( status_code = 402 , detail = f'Пароль должен содержать специальные символы.'
                )
            
        if not value :
            logger.error("Пароль должен содержать специальные символы.")
            # raise ValueError ( 'Не введён пароль' )
            raise HTTPException (status_code = 402 , detail = f'Пароль должен содержать специальные символы.'
                )
            
        if re.search ( r'[а-яА-ЯёЁ]' , value ) :
            logger.error("Пароль должен содержать специальные символы.")
            # raise ValueError ( 'Пароль не должен содержать кириллицу (русские буквы)' )
            raise HTTPException ( status_code = 402 , detail = f'Пароль должен содержать специальные символы.'
                )
            
        if not re.search ( r'[^a-zA-Z0-9]' , value ) :
            logger.error("Пароль должен содержать специальные символы.")
            # raise ValueError (
            #     'Пароль должен содержать специальные символы.'
            #     )
            raise HTTPException ( status_code = 402 , detail = f'Пароль должен содержать специальные символы.'
                )
            
        return value
    @field_validator ( 'password2' )
    @classmethod
    def validate_password_check ( cls , value , info: FieldValidationInfo ) :
        if 'password' in info.data and value != info.data [ 'password' ] :
            logger.error("Введенные пароли не совпадают")
            # raise ValueError ( 'Введенные пароли не совпадают' )
            raise HTTPException ( status_code = 402 , detail = f"Введенные пароли не совпадают" )
            
        return value
    
    
    
    
class ResetPasswordModel(BaseModel):
    password: str
    password2: str
    email: str
    

class EmailCodeRequestModel(BaseModel):
    email: str
    code: int = Field(..., ge=1000, le=9999)

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        if not value:
            logger.error("Электронная почта не указана")
            raise HTTPException(
                status_code=402,
                detail="Электронная почта не указана",
            )
        return value

    @field_validator('code')
    @classmethod
    def validate_code(cls, value):
        if value is None:
            logger.error("Код подтверждения не указан")
            raise HTTPException(
                status_code=402,
                detail="Код подтверждения не указан",
            )
        if not (1000 <= value <= 9999):
            logger.error("Неверный код подтверждения")
            raise HTTPException(
                status_code=402,
                detail="Неверный код подтверждения",
            )
        return value

    