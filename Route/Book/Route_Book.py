from fastapi import APIRouter , Depends
from pydantic import BaseModel , Field
from sqlalchemy.orm import Session
from sqlalchemy.sql.annotation import Annotated

from Database.connect.database_connect import get_db

router = APIRouter ( )


# Модель вывода книг
class BookModel ( BaseModel ) :
	id: int
	title: str
	author: str
	genre: str
	photo: bytes
	is_favorite: bool

class PaginationModelPage (BaseModel) :
	limit: int = Field( 5, ge=0, le=100, description = "Количество страниц" )
	offset: int = Field( 5, description = "Смещение для пагинаций" )

class BookListRequst ( BaseModel ) :
	jwt_token: str


@router.get ( "/" )
async def BookList ( request: BookListRequst, db: Session = Depends ( get_db ) ) -> BookModel:
	
	
	
	
	
	
	
	
	
	
	
	
	pass


""""
async def BookReader ( ) :
	pass
"""


class AddFavoriteBookRequst ( BaseModel ) :
	jwt_token: str
	id_book: int


async def AddFavoriteBook (
		request: AddFavoriteBookRequst ,
		
		) :
	pass


class DeleteFavoriteBookRequst ( BaseModel ) :
	jwt_token: str
	id_book: int


async def DeleteFavoriteBook ( request: DeleteFavoriteBookRequst ) :
	pass


async def ChangeStatusReaderBook ( ) :
	pass
