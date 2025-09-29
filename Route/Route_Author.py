from sys import prefix
from urllib.request import Request

from fastapi import APIRouter , HTTPException , Depends
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer
from pydantic import BaseModel , Field , field_validator
from sqlalchemy import select

router = APIRouter ( prefix = "/Book" , tags = [ "Авторы" ] )




@router.post("/add/{id}" , summary="Добавить авто в избранное")
async def AddFavoriteAuthor():
	pass
@router.delete("/delete/{id}" , summary="Удалить автора из избранного")
async def DeleteFavoriteAuthor():
	pass
@router.get("/", summary="Вывести данные автора книги")
async def AuthorWriteLine():
	pass

