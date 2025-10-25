import base64

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select , desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from Database.model import BooksTable , GenreTable , AuthorTable , Book_Author , FavoriteUserBook , UserTable
from Database.settings.settings import settings
from Route.Book.response_model import BookModel
from Route.auth.methods_route import MethodsRegister

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


class MethodsBook ( BaseModel ) :
	# Получение списков книг
	@classmethod
	async def get_book ( cls , db: AsyncSession , token: str , limit: int = 6 ) :
		try :
			login = await MethodsRegister.VerifyJwt ( token )
			select_id_user = (select ( UserTable.id_user ).where ( UserTable.login_user == login ))
			id_user = db.execute ( select_id_user )
			
			writeline_popular_book = await db.execute (
				select (
					BooksTable.book_id ,
					BooksTable.book_name ,
					BooksTable.image_books ,
					AuthorTable.name ,
					AuthorTable.family
					)
				.join (
					Book_Author , BooksTable.book_id == Book_Author.id_book
					)
				.join (
					AuthorTable , Book_Author.id_author == AuthorTable.id_author
					)
				.order_by ( BooksTable.book_id )
				
				)
			popular_rows = writeline_popular_book.unique ( ).all ( )
			
			popular_books_model = [ ]
			for row in popular_rows :
				(book_id , book_name , image_books , author_name , author_family) = row
				
				check_liked = db.execute (
					select ( FavoriteUserBook ).where (
						FavoriteUserBook.Id_book == book_id , FavoriteUserBook.Id_user == id_user
						)
					)
				result = db.scalar ( check_liked )
				if result is not None :
					check_liked_bool = False
				else :
					check_liked_bool = True
				
				encoded_photo = base64.b64encode ( image_books ).decode ( 'utf-8' )
				book_model = BookModel (
					id = book_id ,
					title = book_name ,
					
					author = f"{author_name} {author_family}" ,
					photo = encoded_photo ,
					is_favorite = check_liked_bool
					)
				popular_books_model.append ( book_model )
			
			new_query = select (
				BooksTable.book_id ,
				BooksTable.book_name ,
				BooksTable.image_books ,
				AuthorTable.name ,
				AuthorTable.family
				).join (
				Book_Author , BooksTable.book_id == Book_Author.id_book
				).join (
				AuthorTable , Book_Author.id_author == AuthorTable.id_author
				).order_by ( desc ( BooksTable.book_id )
			                 
			                 )
			
			new_results = await db.execute ( new_query )
			new_rows = new_results.unique ( ).all ( )
			
			new_books_model = [ ]
			for row in new_rows :
				(book_id , book_name , image_books , author_name , author_family) = row
				check_liked = db.execute (
					select ( FavoriteUserBook ).where (
						book_id == FavoriteUserBook.Id_book , id_user == FavoriteUserBook.Id_user
						)
					)
				result = db.scalar ( check_liked )
				if result is not None :
					check_liked_bool = False
				else :
					check_liked_bool = True
				encoded_photo = base64.b64encode ( image_books ).decode ( 'utf-8' )
				book_model = BookModel (
					id = book_id ,
					title = book_name ,
					author = f"{author_name} {author_family}" ,
					photo = encoded_photo ,
					is_favorite = check_liked_bool
					)
				new_books_model.append ( book_model )
			
			return new_books_model , popular_books_model
		
		except HTTPException as e :
			raise HTTPException ( status_code = 500 , detail = f"Ошибка в {e}" )
		except Exception as e :
			print ( e )
			raise HTTPException (
				status_code = 500 , detail = f"Произошла внутренняя ошибка при регистрации.  Подробнее {e}"
				)
	
	# Добавление книг в избранное
	@classmethod
	async def add_favorite_book ( cls , db: AsyncSession , token: str , id_book: int ) :
		try :
			login = await MethodsRegister.VerifyJwt ( token )
			select_id_user = (select ( UserTable.id_user).where ( UserTable.login_user == login ))
			id_user = (await db.execute(select_id_user)).scalar_one_or_none()
			if id_user is None :
				
				raise HTTPException ( status_code = 401 , detail = "Не найден пользователь" )
			insert_book = FavoriteUserBook (
				Id_user = id_user,
				Id_book = id_book,
				
				
				)
			db.add ( insert_book )
			await db.commit ( )
			await db.refresh ( insert_book )
		except HTTPException as e :
			raise HTTPException ( status_code = 500 , detail = f"Ошибка в {e}" )
		except Exception as e :
			print ( e )
			raise HTTPException (
				status_code = 500 , detail = f"Произошла внутренняя ошибка при добавлении в избранное книгу.  Подробнее {e}"
				)
	
	# Удаление книг из избранных
	@classmethod
	async def delete_favorite_book ( cls , db: AsyncSession , token: str , id_book: int ) :
		try :
			login = MethodsRegister.VerifyJwt ( token )
			
			select_id_user = (select ( UserTable.id_user ).where ( UserTable.login_user == login ))
			select_id_user_result = select_id_user.scalars ( ).first ( )
			delete_favorite_book = FavoriteUserBook (
				Id_book = id_book ,
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
		try :
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
