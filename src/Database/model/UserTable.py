import datetime

from sqlalchemy import Integer , DateTime
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import Mapped , mapped_column

from Database.connect.database_connect import Base


# Таблица пользователей
class UserTable ( Base ) :
	__tablename__ = "user_table"
	id_user: Mapped [ int ] = mapped_column ( Integer , primary_key = True , autoincrement = True )
	login_user: Mapped [ str ] = mapped_column ( unique = True, nullable = True )
	password_hashed: Mapped [ str ] = mapped_column ( unique = True, nullable = True )
	created_at: Mapped [ datetime.datetime ] = mapped_column (
		DateTime ( ) , server_default = func.now ( )
		)
	email: Mapped [ str ] = mapped_column ( unique = True, nullable = True )
	role: Mapped [ str ] = mapped_column (  server_default = "user", nullable = True )
