from pydantic import BaseModel , validator , model_validator , field_validator
from pydantic_core.core_schema import FieldValidationInfo


class RegistationResponseModel ( BaseModel ) :
	login: str
	password: str
	password2: str
	email: str
	
	# заглушка на проверку email
	
	@validator ( 'email' )
	def validate_email (cls, value ) :
		pass
	
	@validator ( 'password' )
	def validate_password (cls, value ) :
		if len ( value ) < 8 :
			raise ValueError ( 'Пароль имеет меньше 8 символов' )
		if not value :
			raise ValueError ( 'Не введён пароль' )
		if value.search ( r'[а-яА-ЯёЁ]' , value ) :
			raise ValueError ( 'Пароль не должен содержать кириллицу (русские буквы)' )
		if not value.search ( r'[^a-zA-Z0-9]' , value ) :
			raise ValueError (
				'Пароль должен содержать специальные символы.'
				)
		return value
	
	@field_validator ( 'password2')
	def validate_password (cls, value, info: FieldValidationInfo) :
		if 'password' in info.data and value != info.data [ 'password' ] :
			raise ValueError ( 'Введенные пароли не совпадают' )
		return value
	
		
	
	