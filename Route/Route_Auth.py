from urllib.request import Request

from fastapi import APIRouter , HTTPException , Depends
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer
from pydantic import BaseModel , Field , field_validator
from sqlalchemy import select
from starlette import status

router = APIRouter ( prefix = "/auth" , tags = [ "Авторизация и регистрация" ] )



class Token(BaseModel):
	access_token : str
	token_type : str
	
	
@router.get( "/login" , response_model=Token, summary = "Авторизация пользователя" )
async def login_auth(request : Request):
	pass
	
	
@router.get( "/register", summary = "Регистрация пользователя" )
async def register_auth(request : Request):
	pass


@router.push( "/reset_password", summary = "Сброс пароля" )
async def reset_password(request : Request):
	pass


async def rename_email(request : Request):
	pass

async def rename_avatar(request : Request):
	pass



async def rename_family(request : Request):
	pass


