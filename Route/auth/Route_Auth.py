from fastapi import APIRouter

from Route.auth.response_model import CheckRegistationRequestModel , CheckDataResponseModel

router = APIRouter ( )


@router.get ( "/login" , summary = "Авторизация пользователя" )
async def login_auth ( ) :
	pass


@router.get (
	"/check_data_register" , summary = "Проверка данных для авторизации" ,
	response_model = CheckDataResponseModel
	)
async def check_data_register ( data: CheckRegistationRequestModel ) :
	return CheckDataResponseModel (
		success = True ,
		message = "Все данные валидны. Можно переходить к отправке кода подтверждения."
		)


@router.get ( "/register" , summary = "Регистрация пользователя" )
async def register_auth ( ) :
	pass


@router.patch ( "/reset_password" , summary = "Сброс пароля" )
async def reset_password ( ) :
	pass


@router.patch ( "/change_email" , summary = "Изменение электронной почты" )
async def rename_email ( ) :
	pass


@router.patch ( "/change_avatar" , summary = "Изменение фотографии профиля" )
async def rename_avatar ( ) :
	pass


async def dispatch_registration_code ( ) :
	pass


async def dispatch_registration_code2 ( ) :
	pass
