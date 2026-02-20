from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from select import select
from sqlalchemy.ext.asyncio import AsyncSession

from Database.model import UserTable , AuthorTable , FavoriteUserAuthor
from Route.auth.methods_route import MethodsRegister


class MethodsAuthor ( BaseModel ) :
	#Вывод подробных данных авторов
	@classmethod
	async def getAuthor_Detail ( cls , db: AsyncSession , token: str , id_author: str ) :
		try :
			login = MethodsRegister.VerifyJwt ( token )
			select_id_user = (select ( UserTable.id_user ).where ( UserTable.login_user == login ))
			select_id_user_result = select_id_user.scalars ( ).first ( )
			writeline_author = await db.execute (
				select (
					AuthorTable
					).where ( AuthorTable.id_author == id_author )
				)
			result_author = await db.execute ( writeline_author )
			return result_author.scalar ( ).all
		except HTTPException as e :
			raise HTTPException ( status_code = 500 , detail = f"Ошибка в {e}" )
		except Exception as e :
			print ( e )
			raise HTTPException (
				status_code = 500 , detail = f"Произошла внутренняя ошибка при регистрации.  Подробнее {e}"
				)
	#Добавление понравившихся авторов
	@classmethod
	async def add_favorite_author ( cls , db: AsyncSession , token: str , id_author: str ) :
		try :
			login: str = MethodsRegister.VerifyJwt ( token )
			if not login :
				raise HTTPException ( status_code = 401 , detail = "Invalid or expired token." )
			
			stmt = select ( UserTable.id_user ).where ( UserTable.login_user == login )
			id_user_result: UUID | None = (await db.execute ( stmt )).scalar_one_or_none ( )
			
			if id_user_result is None :
				raise HTTPException ( status_code = 404 , detail = "User not found." )
			
			insert_favorite_author = FavoriteUserAuthor (
				id_author = id_author ,
				id_user = id_user_result ,
				)
			
			db.add ( insert_favorite_author )
			await db.commit ( )
			await db.refresh ( insert_favorite_author )
			
			return insert_favorite_author
		
		except HTTPException :
			raise
		
		except Exception as e :
			print ( f"Database error during add_favorite_author: {e}" )
			raise HTTPException (
				status_code = 500 ,
				detail = "An internal error occurred while adding the favorite author. Please try again."
				)
	
	# Удаление понравившихся авторов
	@classmethod
	async def remove_favorite_author (  cls , db: AsyncSession , token: str , id_author: str ) :
		try :
			login: str = MethodsRegister.VerifyJwt ( token )
			if not login :
				raise HTTPException ( status_code = 401 , detail = "Invalid or expired token." )
			
			stmt = select ( UserTable.id_user ).where ( UserTable.login_user == login )
			id_user_result: UUID | None = (await db.execute ( stmt )).scalar_one_or_none ( )
			
			if id_user_result is None :
				raise HTTPException ( status_code = 404 , detail = "User not found." )
			
			insert_favorite_author = FavoriteUserAuthor (
				id_author = id_author ,
				id_user = id_user_result ,
				)
			
			db.delete ( insert_favorite_author )
			await db.commit ( )
			await db.refresh ( insert_favorite_author )
			
			return insert_favorite_author
		
		except HTTPException :
			raise
		
		except Exception as e :
			print ( f"Database error during add_favorite_author: {e}" )
			raise HTTPException (
				status_code = 500 ,
				detail = "An internal error occurred while adding the favorite author. Please try again."
				)
