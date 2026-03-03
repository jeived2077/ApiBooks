import fastapi
from log.log import logger
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.schemas import CheckDataResponseModel, CheckRegistationRequestModel, CheckResetPasswordRequestModel, EmailCodeRequestModel, RequestAuthModel, RequestEmailModel

from Database.connect.database_connect import get_db
from config.settings import Settings
from app.auth.services import MethodsRegister





router = fastapi.APIRouter ( )


@router.post ( "/refresh_token" , summary = "Обновление токена" )
async def refresh_token ( access_token : str, refresh_token : str) :
    return await MethodsRegister.RefreshToken(access_token , refresh_token )

@router.post ( "/login" , summary = "Авторизация пользователя" )
async def login_auth ( data: RequestAuthModel , db: Session = fastapi.Depends ( get_db ) ) :
    return await MethodsRegister.Auth ( db , data.login , data.password )


@router.post (
    "/check_data_register" , summary = "Проверка данных для авторизации" ,
    response_model = CheckDataResponseModel
    )
async def check_data_register ( data: CheckRegistationRequestModel, db: Session = fastapi.Depends ( get_db ) ) :
    return await MethodsRegister.CheckDataRegister(
        db=db,
        login=data.login,
        email=data.email,
        password=data.password,
        fist_name=data.first_name,
        last_name=data.last_name,
    )
    
    
    
    
    







@router.post ( "/register" , summary = "Регистрация пользователя" )
async def register_auth ( data: EmailCodeRequestModel , db: Session = fastapi.Depends ( get_db ) ) :
    return await MethodsRegister.Register ( db , data.email, data.code )


@router.patch ( "/reset_password" , summary = "Сброс пароля" )
async def reset_password (data: CheckResetPasswordRequestModel, db: Session = fastapi.Depends ( get_db )  ) :
    return await MethodsRegister.ResetPassword(
        db=db,
        email=data.email,
        code=data.code,
        password=data.password
    )

@router.post ( "/reset_password_email" , summary = "Ввод email для сброса пароля" )
async def reset_password_email (data: RequestEmailModel, db: Session = fastapi.Depends ( get_db ) ) :
    return await MethodsRegister.SendEmailReset(
        db=db,
        email=data.email,
    )

@router.patch ( "/change_email" , summary = "Изменение электронной почты" )
async def rename_email ( ) :
    pass


@router.patch ( "/change_avatar" , summary = "Изменение фотографии профиля" )
async def rename_avatar ( ) :
    pass


