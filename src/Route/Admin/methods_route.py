from pydantic import BaseModel


class MethodsAdmin(BaseModel)
	@classmethod
	async def AddBook( cls, book ) :
		pass
	@classmethod
	async def DeleteBook( cls, book ) :
		pass
	@classmethod
	async def UpdateBook( cls, book ) :
		pass
	@classmethod
	async def GetBooks( cls, book ) :
		pass
	@classmethod
	async def AddAuthor( cls, author ) :
		pass
	
	@classmethod
	async def AddBookAuthor ( cls , author ) :
		pass
	
	@classmethod
	async def DeleteBookAuthor ( cls , author ) :
		pass
	@classmethod
	async def DeleteAuthor( cls, author ) :
		pass
	@classmethod
	async def UpdateAuthor( cls, author ) :
		pass
	@classmethod
	async def GetAuthors( cls, author ) :
		pass
	@classmethod
	async def AddGenre( cls, genre ) :
		pass
	@classmethod
	async def DeleteGenre( cls, genre ) :
		pass
	@classmethod
	async def UpdateGenre( cls, genre ) :
		pass
	@classmethod
	async def GetGenres( cls, genre ) :
		pass
	