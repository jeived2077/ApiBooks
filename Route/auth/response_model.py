from pydantic import BaseModel , validator , field_validator
from pydantic_core.core_schema import FieldValidationInfo
from sqlalchemy.orm import Session

from Database.User_Table import User_Table

db: Session = Session


class CheckDataResponseModel ( BaseModel ) :
	success: bool
	message: str
	
	# проверка на успешность на крайний случай
	@validator ( 'success' )
	def validate_success ( cls , v ) :
		if v == True | v == False :
			return v
		else :
			raise ValueError (
				'Не правильно проведена проверка'
				)


class CheckRegistationRequestModel ( BaseModel ) :
	login: str
	password: str
	password2: str
	email: str
	
	# проверка логина
	@validator ( 'login' )
	def validate_email ( cls , value ) :
		check_email = User_Table (
			login_user = value ,
			
			)
		
		check = db.first ( check_email )
		if check is None :
			return value
		else :
			raise ValueError (
				'Данный логин используется'
				)
	
	# проверка email
	@validator ( 'email' )
	def validate_email ( cls , value ) :
		check_email = User_Table (
			email = value ,
			
			)
		
		check = db.first ( check_email )
		if check is None :
			return value
		else :
			raise ValueError (
				'Данная почта используется'
				)
	
	@validator ( 'password' )
	def validate_password ( cls , value ) :
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
	
	@field_validator ( 'password2' )
	def validate_password ( cls , value , info: FieldValidationInfo ) :
		if 'password' in info.data and value != info.data [ 'password' ] :
			raise ValueError ( 'Введенные пароли не совпадают' )
		return value
