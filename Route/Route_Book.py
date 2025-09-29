from urllib.request import Request

from fastapi import APIRouter , HTTPException , Depends
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer
from pydantic import BaseModel , Field , field_validator
from sqlalchemy import select

router = APIRouter ( prefix = "/Book" , tags = [ "Книги" ] )

async def BookReader():
	pass



async def AddFavoriteBook():
	pass


async def DeleteFavoriteBook():
	pass

async def ChangeStatusReaderBook():
	pass