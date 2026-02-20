from sqlalchemy import Integer
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy.ext.declarative import declarative_base
from Database.connect.database_connect import Base , engine


#Таблица Жанров
class GenreTable ( Base ) :
	
	__tablename__ = "genre_table"
	genre_id: Mapped [ int ] = mapped_column ( Integer , primary_key = True , autoincrement = True )
	genre_name: Mapped [ str ] = mapped_column ( nullable = False, unique = True )
