from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Route.Admin.Route_Admin import router as admin_router
from Route.auth.Route_Auth import router as auth_router
from Route.author.Route_Author import router as author_router
from Route.Book.Route_Book import router as book_router
from Route.Statics.Route_Statics import router as statics_router

app = FastAPI ( )
#Изменение параметров Middleware
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"]
)
#Подключение маршрутизаторов
app.include_router ( auth_router , prefix = "/Auth" , tags = [ "Авторизация и регистрация" ] )
app.include_router ( author_router , prefix = "/Author" , tags = [ "Авторы" ] )
app.include_router ( book_router , prefix = "/Book" , tags = [ "Книги" ] )
app.include_router ( statics_router , prefix = "/Static" , tags = [ "Статистика" ] )
app.include_router ( admin_router , prefix = "/admin" , tags = [ "Админ панель" ] )
