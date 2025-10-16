from fastapi import APIRouter

router = APIRouter ( )






class BookModel(BaseModel):
	id: int
	title: str
	author: str
	genre: str
	photo: bytes
	is_favorite: bool
	
	
	
	
	
	
	
	
	
	
@router.get("/")
async def BookList():
	
	
	
	pass



async def BookReader ( ) :
	pass


async def AddFavoriteBook ( ) :
	pass


async def DeleteFavoriteBook ( ) :
	pass


async def ChangeStatusReaderBook ( ) :
	pass
