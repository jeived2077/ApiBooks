from datetime import date

from pydantic import BaseModel


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