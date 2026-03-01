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
    result: str | None = Field ( default = None )
    
    
class CheckResetPasswordRequestModel(BaseModel):
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

class CheckRegistationRequestModel ( BaseModel ) :
    login: str | None = Field ( default = None )
    password: str | None = Field ( default = None )
    password2: str | None = Field ( default = None )
    email: List[EmailStr] | None = Field ( default = None )
    
    # проверка логина
    @field_validator ( 'login' )
    @classmethod
    def validate_login ( cls , value ) :
        if len ( value ) < 3 :
            logger.error("Логин слишком короткий.")
            raise ValueError ( 'Логин слишком короткий.' )
            
        return value
    
    # проверка email
    @field_validator ( 'email' )
    @classmethod
    def validate_email ( cls , value ) :
        
        if not value or len(value) == 0 :
            logger.error("Электронная почта не указана")
            raise HTTPException (
                status_code = 402 ,
                detail = "Электронная почта не указана"
                )
        
        
        return value
    
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
class RegisterRequestModel(BaseModel):
    email: EmailStr
    code: int = Field(..., ge=100000, le=999999)

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
        if not (100000 <= value <= 999999):
            logger.error("Неверный код подтверждения")
            raise HTTPException(
                status_code=402,
                detail="Неверный код подтверждения",
            )
        return value

    