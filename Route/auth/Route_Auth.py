from fastapi import APIRouter , Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from Database.connect.database_connect import get_db
from Route.auth.methods_route import MethodsRegister
from Route.auth.response_model import CheckRegistationRequestModel , CheckDataResponseModel , RequestAuthModel

router = APIRouter ( )


@router.post ( "/refresh_token" , summary = "Обновление токена" )
async def refresh_token ( access_token : str, refresh_token : str) :
	return await MethodsRegister.RefreshToken(access_token , refresh_token )


@router.post ( "/generate_token" , summary = "Генерация токена токена" )
async def generate_token ( ) :
	pass


@router.post ( "/check_token" , summary = "Проверка на валидность токена" )
async def check_token ( ) :
	pass


@router.post ( "/login" , summary = "Авторизация пользователя" )
async def login_auth ( data: RequestAuthModel , db: Session = Depends ( get_db ) ) :
	return await MethodsRegister.Auth ( db , data.login , data.password )


@router.post (
	"/check_data_register" , summary = "Проверка данных для авторизации" ,
	response_model = CheckDataResponseModel
	)
async def check_data_register ( data: CheckRegistationRequestModel ) :
	# return await MethodsRegister.CheckDataRegister(data.login, data.email)
	pass


class RegisterRequestModel ( BaseModel ) :
	email: str
	password: str
	login: str


@router.post ( "/register" , summary = "Регистрация пользователя" )
async def register_auth ( data: RegisterRequestModel , db: Session = Depends ( get_db ) ) :
	return await MethodsRegister.Register ( db , data.email , data.password , data.login )


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
