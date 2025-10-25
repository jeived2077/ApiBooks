from fastapi import APIRouter

router = APIRouter ( )





router.get("/get_Statics", summary = "Получение статистики")
async def get_statics() :
	pass