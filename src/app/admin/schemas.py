from datetime import date
from typing import Optional

from pydantic import BaseModel, field_validator

#Валидация добавление автора
class RequestAddAuthor(BaseModel):
    name_author: str
    family_author: str
    image: Optional[bytes] = None
    information: str
    date_author: date
    token_access: str
    token_refresh: str
    @field_validator('name_author')
    @classmethod
    def validate_name(cls, value):
        if len(value) < 3:
            raise ValueError ( 'Слишком короткие инициалы.' )
        if (value) is None:
            raise ValueError ( 'Отсутствуют инициалы автора' )
        if " " in value is None:
            raise ValueError ( 'Нету отступов между инициалами ' )
            
        return value
    #Доделать валидацию даты смерти автора
    @field_validator('date_death')
    @classmethod
    def validate_death(cls,value):
        if value > date.today:
            raise ValueError ( 'Дата смерти автора не может быть позже настоящего времени' )
        return value
    @field_validator("information")
    @classmethod
    def validate_information(cls,value):
        if value is None:
            raise ValueError ( 'Не написана подробная информация о авторе' )
        if len(value) > 500:
            raise ValueError ( 'Подробная информация привышает 500 символов')
        return value
    
            
            
class RequestAddAuthor(BaseModel) :
	name: str
	family: str
	description: str
	photo: bytes
	date: date
	
class RequestAddBook(BaseModel) :
	id: int
	title: str
	author: str
	photo: str
	is_favorite: bool
	type: str
	
	
class RequestAddGenre(BaseModel) :
	name_genre: str


class RequestAddBookGenre(BaseModel) :
	id_book: int
	id_genre: int


class RequestAddAuthorBook(BaseModel) :
	id_book: int
	id_author: int
	
class AccessToken(BaseModel):
	access_token: str



class AddText(BaseModel):
	text: str
	id_book: int
	page: int    
    