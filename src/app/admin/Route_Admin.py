from fastapi import APIRouter
import fastapi
from requests import Session

from Database.connect.database_connect import get_db
from app.admin.response_model import RequestAddAuthor

router = APIRouter ( )

@router.post("/add_author", summary="Добавление автора")
async def AddAuthor (data: RequestAddAuthor, db: Session = fastapi.Depends ( get_db )) :
    pass



# async def DeleteAuthor ( ) :
# 	pass


# async def AddBook ( ) :
# 	pass


# async def DeleteBook ( ) :
# 	pass


# async def ChangeBook ( ) :
# 	pass


# async def ChangeStatusBook ( ) :
# 	pass
