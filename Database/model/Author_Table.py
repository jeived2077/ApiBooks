from datetime import date

from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column , Mapped

from Database.connect.database_connect import Base


# Класс таблицы Авторов
class AuthorTable ( Base ) :
	__tablename__ = "author_table"
	id_author: Mapped [ int ] = mapped_column ( Integer , primary_key = True , autoincrement = True )
	name: Mapped[str]= mapped_column ( nullable = False  )
	family: Mapped [ str ] = mapped_column ( nullable = False  )
	photo: Mapped [ bytes ] = mapped_column ( nullable = False )
	information: Mapped [ str ] = mapped_column ( nullable = False )
	date_author: Mapped [ date ] = mapped_column ( nullable = False )
	
