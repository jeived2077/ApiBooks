from urllib.request import Request

from fastapi import APIRouter , HTTPException , Depends
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer
from pydantic import BaseModel , Field , field_validator
from sqlalchemy import select

router = APIRouter ( prefix = "/Book" , tags = [ "Авторы" ] )





async def AddAuthor():
	pass
async def DeleteAuthor():
	pass


async def AddBook():
	pass
async def DeleteBook():
	pass


async def ChangeBook():
	pass

async def ChangeStatusBook():
	pass
