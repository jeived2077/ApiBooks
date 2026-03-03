from fastapi import HTTPException, logger
from pydantic import BaseModel
from requests import Session
from sqlalchemy import insert

from Database.model.Author_Table import AuthorTable
from app import db
from app.admin.schemas import RequestAddAuthor
from app.auth.services import MethodsRegister


class MethodsAdmin(BaseModel):
    
    #Надо доделать добавление авторов щас занялся с переделкой работы jwt
    @classmethod
    async def AddAuthor(cls, data: RequestAddAuthor):
        try:
            logger.info(f"Входящие данные {data}")
            check_token = MethodsRegister.VerifyJwt(data.token_refresh)
            if check_token
            if data.image is None:
                add_author = db.execute(insert(AuthorTable).values(name=data.name_author, family = data.family_author, information=data.information: str
, date_author = data.date_author))
                
                
                
                
                
                
                
                
        except HTTPException as e :
            raise HTTPException ( status_code = 500 , detail = f"Ошибка в {e}" )
        except Exception as e :
            raise HTTPException (
                status_code = 500 , detail = f"Произошла внутренняя ошибка при добавлении автора.  Подробнее {e}"
                )
        