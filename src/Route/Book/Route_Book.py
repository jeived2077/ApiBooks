from fastapi import APIRouter , Depends
from pydantic import BaseModel , Field
from sqlalchemy.orm import Session

from Database.connect.database_connect import get_db
from Route.Book.methods_route import MethodsBook

router = APIRouter ( )



class PaginationModelPage ( BaseModel ) :
	limit: int = Field ( 5 , ge = 0 , le = 100 , description = "Количество страниц" )
	offset: int = Field ( 5 , description = "Смещение для пагинаций" )





@router.get ( "/" )
async def BookList ( jwt_token:str , db: Session = Depends ( get_db ) )  :
	return await MethodsBook.get_book(db, jwt_token)


""""
async def BookReader ( ) :
	pass
"""


class AddFavoriteBookRequst ( BaseModel ) :
	jwt_token: str
	id_book: int

@router.post ( "/add/favorite{id_book}", summary = "Добавить книгу в  избранные"  )
async def AddFavoriteBook (
		request: AddFavoriteBookRequst ,
		db: Session = Depends ( get_db )
		) :
	return await MethodsBook.add_favorite_book(db, request.jwt_token, request.id_book)


class DeleteFavoriteBookRequst ( BaseModel ) :
	jwt_token: str
	id_book: int

@router.delete ( "/add/favorite{id_book}", summary = "Удалить книгу из избранных" )
async def DeleteFavoriteBook ( request: DeleteFavoriteBookRequst , db: Session = Depends ( get_db ) ) :
	return await MethodsBook.delete_favorite_book(db, request)


async def ChangeStatusReaderBook ( ) :
	pass
