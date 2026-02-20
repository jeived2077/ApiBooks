import re

from pydantic import BaseModel , field_validator
from pydantic import Field
from pydantic_core.core_schema import FieldValidationInfo



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
	
	


class CheckRegistationRequestModel ( BaseModel ) :
	login: str | None = Field ( default = None )
	password: str | None = Field ( default = None )
	password2: str | None = Field ( default = None )
	email: str | None = Field ( default = None )
	
	# проверка логина
	@field_validator ( 'login' )
	@classmethod
	def validate_login ( cls , value ) :
		if len ( value ) < 3 :
			raise ValueError ( 'Логин слишком короткий.' )
		return value
	
	# проверка email
	@field_validator ( 'email' )
	@classmethod
	def validate_email ( cls , value ) :
		if "@" not in value :
			raise ValueError (
				'Введён не правильный формат почты'
				)
		
		return value
	
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
			raise ValueError (
				'Пароль должен содержать специальные символы.'
				)
		return value
	
	@field_validator ( 'password2' )
	@classmethod
	def validate_password_check ( cls , value , info: FieldValidationInfo ) :
		if 'password' in info.data and value != info.data [ 'password' ] :
			raise ValueError ( 'Введенные пароли не совпадают' )
		return value
