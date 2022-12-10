from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.config import settings


engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False)
