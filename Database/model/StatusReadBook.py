from datetime import datetime

from sqlalchemy import Integer , ForeignKey , func
from sqlalchemy.orm import Mapped , mapped_column

from Database.connect.database_connect import Base


class ReadBookTable ( Base ) :
	
	__tablename__ = "readbook_table"
	id_read: Mapped [ int ] = mapped_column ( Integer , primary_key = True , autoincrement = True )
	id_book: Mapped [ str ] = mapped_column (ForeignKey ( 'books_Table.book_id' , ondelete = 'CASCADE' ), unique = True, nullable = True )
	id_user: Mapped [ str ] = mapped_column (ForeignKey ( 'user_table.id_user' , ondelete = 'CASCADE' ), unique = True, nullable = True )
	id_Status: Mapped [ str ] = mapped_column (ForeignKey ( 'status_table.id_status' , ondelete = 'CASCADE' ), unique = True, nullable = True )
	datetime_read: Mapped [ datetime ] = mapped_column ( server_default = func.now ( ) )