from pydantic import BaseModel


# Модель вывода книг
class BookModel ( BaseModel ) :
	id: int
	title: str
	author: str
	photo: str
	is_favorite: bool
	type: str