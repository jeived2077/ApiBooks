from sqlalchemy import Integer
from sqlalchemy.orm import Mapped , mapped_column

from Database.connect.database_connect import Base


class StatusTable ( Base ) :
	__tablename__ = "status_table"
	id_status: Mapped [ int ] = mapped_column ( Integer , primary_key = True , autoincrement = True )
	status_name: Mapped [ str ] = mapped_column ( unique = True, nullable = True )