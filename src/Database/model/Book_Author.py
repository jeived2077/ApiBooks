from datetime import datetime

from sqlalchemy import Column , String , Text , ForeignKey
from sqlalchemy import Integer , func
from sqlalchemy.orm import Mapped , mapped_column

from Database.connect.database_connect import Base



class Book_Author(Base):
	__tablename__ = 'book_author'
	id_bool_author: Mapped [ int ] = mapped_column ( primary_key = True, autoincrement = True )
	id_book: Mapped[int | None] = mapped_column(ForeignKey('books_Table.book_id', ondelete='CASCADE'))
	id_author: Mapped[int | None]= mapped_column(ForeignKey('author_table.id_author', ondelete='CASCADE'))
	
	
	
	