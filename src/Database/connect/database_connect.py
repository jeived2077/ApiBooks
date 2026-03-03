from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncEngine , async_sessionmaker , create_async_engine , AsyncSession
from sqlalchemy.orm import DeclarativeBase

from config.settings import settings

DATABASE_URL = settings.get_db_url ( )

engine = create_async_engine ( url = DATABASE_URL )

AsyncSessionLocal = async_sessionmaker (
	engine ,
	expire_on_commit = False ,
	autoflush = False
	
	)
@property  
def db_engine(self) -> AsyncEngine:  
    return self._engine

async def get_db ( ) -> AsyncGenerator [ AsyncSession , None ] :
	async with AsyncSessionLocal ( ) as db :
		try :
			
			yield db
		finally :
			
			await db.close ( )


class Base ( AsyncAttrs , DeclarativeBase ) :
	__abstract__ = True
