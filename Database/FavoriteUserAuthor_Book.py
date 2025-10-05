from datetime import datetime


from sqlalchemy import Column , INTEGER , Integer , ForeignKey, BOOLEAN, DateTime, String


class User_Table( Base ):
	__tablename__ = "nested_comments"
	id_nestcomm = Column ( Integer , primary_key = True, autoincrement=True )
	id_commit = Column ( INTEGER , ForeignKey ( "users.id_user" , ondelete = "CASCADE" ) , nullable = False )
	id_user = Column ( INTEGER , ForeignKey ( "users.id_user" , ondelete = "CASCADE" ) , nullable = False )
	text_comment = Column ( String , nullable = False , default = None )
	datetime_create = Column ( DateTime , nullable = False , default = datetime.now )
	is_edited = Column ( BOOLEAN , nullable = False , default = False )