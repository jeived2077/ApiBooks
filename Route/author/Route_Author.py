from fastapi import APIRouter

router = APIRouter ( )


@router.post ( "/add/{id}" , summary = "Добавить авто в избранное" )
async def AddFavoriteAuthor ( ) :
	pass


@router.delete ( "/delete/{id}" , summary = "Удалить автора из избранного" )
async def DeleteFavoriteAuthor ( ) :
	pass


@router.get ( "/" , summary = "Вывести данные автора книги" )
async def AuthorWriteLine ( ) :
	pass
