from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Integer , func
from sqlalchemy.orm import Mapped , mapped_column

from Database.connect.database_connect import Base

#Таблица понравившихся жанров
class FavoriteUserGenre ( Base ) :
	__tablename__ = "favorite_user_genre"
	favorite_id: Mapped [ int ] = mapped_column ( Integer , primary_key = True , autoincrement = True )
	Id_user: Mapped [ int ] = mapped_column (
		ForeignKey ( 'user_table.id_user' , ondelete = 'CASCADE' ) , nullable = False
		)
	Id_genre: Mapped [ int ] = mapped_column (
		ForeignKey ( 'genre_table.genre_id' , ondelete = 'CASCADE' ) , nullable = False
		)
	datetime_favorite: Mapped [ datetime ] = mapped_column ( server_default = func.now ( ) )
