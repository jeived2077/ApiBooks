from datetime import datetime

from sqlalchemy import ForeignKey , func
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from Database.connect.database_connect import Base


# Таблица понравившихся авторов
class FavoriteUserAuthor ( Base ) :
	__tablename__ = "favorite_user_author_table"
	id_favorite: Mapped [ int ] = mapped_column ( primary_key = True , autoincrement = True )
	id_author: Mapped [ int ] = mapped_column ( ForeignKey ( 'author_table.id_author', ondelete = 'CASCADE' ) , nullable = False )
	id_user: Mapped [ int ] = mapped_column ( ForeignKey ( 'user_table.id_user', ondelete = 'CASCADE' ) , nullable = False )
	datetime_favorite: Mapped [ datetime ] = mapped_column ( server_default = func.now ( ) )
