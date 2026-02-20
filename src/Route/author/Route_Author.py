from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from Route.author.methods_route import MethodsAuthor
from Route.author.respose_model import AcessRequest

router = APIRouter ( )


# @router.post ( "/add/{id}" , summary = "Добавить автора в избранное" )
# async def AddFavoriteAuthor (
# 		id_author: str, token_acces:str , db: AsyncSession
# 		) :
# 	return MethodsAuthor.add_favorite_author (db, token_acces, id_author  )

#
# @router.delete ( "/delete/{id}" , summary = "Удалить автора из избранного" )
# async def DeleteFavoriteAuthor ( requestAccess: AcessRequest , id_author: str , db: AsyncSession
#
#
#
#
# 		) :
# 	return MethodsAuthor.delete_favorite_author ( )
#
#
# @router.get ( "/" , summary = "Вывести данные автора книги" )
# async def AuthorWriteLine ( ) :
# 	return MethodsAuthor.getAuthor_Detail()
