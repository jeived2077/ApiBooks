from datetime import date

from sqlalchemy import Integer , ForeignKey
from sqlalchemy.orm import Mapped , mapped_column

from Database.connect.database_connect import Base


# Таблица книг
class BooksTable ( Base ) :
	__tablename__ = "books_Table"
	book_id: Mapped [ int ] = mapped_column ( Integer , primary_key = True , autoincrement = True )
	book_name: Mapped [ str ] = mapped_column ( nullable = False )
	year_Create: Mapped [ date ] = mapped_column ( nullable = False )
	genre_Id: Mapped [ int ] = mapped_column ( ForeignKey ( 'genre_table.genre_id' , ondelete = 'CASCADE' ) )
	saled_books: Mapped [ int ] = mapped_column ( nullable = False )
	image_books: Mapped [ bytes ] = mapped_column ( nullable = False )
	description: Mapped [ str ] = mapped_column ( nullable = False )
