from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from Database.model import BooksTable , GenreTable , AuthorTable , Book_Author , FavoriteUserBook , UserTable
from Database.settings.settings import settings
from Route.auth.methods_route import MethodsRegister

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


class MethodsBook ( BaseModel ) :
	#Получение списков книг
	@classmethod
	async def get_book ( cls , db: AsyncSession , token: str , limit: int = None ) :
		try:
			login = MethodsRegister.VerifyJwt ( token )
			
			writeline_book = await db.execute (
				select (
					BooksTable.book_id , BooksTable.book_name , BooksTable.image_books , BooksTable.description ,
					GenreTable.genre_name , AuthorTable.name , AuthorTable.family
					).where ( BooksTable.login_user == login ).limit ( limit ).join (
					BooksTable.book_id == Book_Author.id_book ,
					Book_Author.id_book == AuthorTable.id_author == AuthorTable.id_author
					)
				
				)
			result_book = await db.execute ( writeline_book )
			return result_book.scalar ( ).all
		except HTTPException as e :
			raise HTTPException ( status_code = 500 , detail = f"Ошибка в {e}" )
		except Exception as e :
			print ( e )
			raise HTTPException (
				status_code = 500 , detail = f"Произошла внутренняя ошибка при регистрации.  Подробнее {e}"
				)
	#Добавление книг в избранное
	@classmethod
	async def add_favorite_book ( cls , db: AsyncSession , token: str , id_book: int ) :
		try:
			login = MethodsRegister.VerifyJwt ( token )
			
			select_id_user = (select ( UserTable.id_user ).where ( UserTable.login_user == login ))
			select_id_user_result = select_id_user.scalars ( ).first ( )
			
			insert_book = FavoriteUserBook (
				
				Id_book = id_book ,
				Id_user = select_id_user_result
				
				)
			db.add ( insert_book )
			await db.commit ( )
			await db.refresh ( insert_book )
		except HTTPException as e :
			raise HTTPException ( status_code = 500 , detail = f"Ошибка в {e}" )
		except Exception as e :
			print ( e )
			raise HTTPException (
				status_code = 500 , detail = f"Произошла внутренняя ошибка при регистрации.  Подробнее {e}"
				)
	#Удаление книг из избранных
	@classmethod
	async def delete_favorite_book ( cls , db: AsyncSession , token: str, id_book: int ) :
		try:
			login = MethodsRegister.VerifyJwt ( token )
			
			select_id_user = (select ( UserTable.id_user ).where ( UserTable.login_user == login ))
			select_id_user_result = select_id_user.scalars ( ).first ( )
			delete_favorite_book = FavoriteUserBook (
				Id_book = id_book,
				Id_user = select_id_user_result
				)
			db.delete ( delete_favorite_book )
			await db.commit ( )
			await db.refresh ( delete_favorite_book )
		except HTTPException as e :
			raise HTTPException ( status_code = 500 , detail = f"Ошибка в {e}" )
		except Exception as e :
			print ( e )
			raise HTTPException (
				status_code = 500 , detail = f"Произошла внутренняя ошибка при регистрации.  Подробнее {e}"
				)
	@classmethod
	async def detail_book ( cls , db: AsyncSession , token: str , id_book: int ) :
		try:
			login = MethodsRegister.VerifyJwt ( token )
			select_id_user = (select ( UserTable.id_user ).where ( UserTable.login_user == login ))
			select_id_user_result = select_id_user.scalars ( ).first ( )
			writeline_book = await db.execute (
				select (
					
					GenreTable.genre_name , AuthorTable.name , AuthorTable.family
					).where ( BooksTable.book_id == id_book ).join (
					BooksTable.book_id == Book_Author.id_book ,
					Book_Author.id_book == AuthorTable.id_author == AuthorTable.id_author
					)
				
				)
			result_book = await db.execute ( writeline_book )
			return result_book.scalar ( ).all
		except HTTPException as e :
			raise HTTPException ( status_code = 500 , detail = f"Ошибка в {e}" )
		except Exception as e :
			print ( e )
			raise HTTPException (
				status_code = 500 , detail = f"Произошла внутренняя ошибка при регистрации.  Подробнее {e}"
				)
		
		
		
		
	
	@classmethod
	async def read_book ( cls , session: Session , jwt: str ) :
		pass
