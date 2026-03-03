from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Database.connect.database_connect import engine
# from app.admin.router import router as admin_router
from Database.model import UserTable
from app.auth.router import router as auth_router
# from app.author.router import router as author_router
# from app.book.router import router as book_router
# from app.statics.router import router as statics_router


app = FastAPI(title="Book")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/Auth", tags=["Авторизация и регистрация"])
# app.include_router(author_router, prefix="/Author", tags=["Авторы"])
# app.include_router(book_router, prefix="/Book", tags=["Книги"])
# app.include_router(statics_router, prefix="/Static", tags=["Статистика"])
# app.include_router(admin_router, prefix="/admin", tags=["Админ панель"])

