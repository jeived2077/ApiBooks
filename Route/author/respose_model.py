from pydantic import BaseModel
from datetime import date

class AuthorModel (BaseModel) :
	id_author: int
	name: str
	family: str
	description: str
	photo: bytes
	date: date
	
	
	
